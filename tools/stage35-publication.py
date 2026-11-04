#!/usr/bin/env python3
"""Offline Stage 3.5 publication contract. Never contacts Sheets or authorizes trades."""
import argparse, copy, datetime, json, math, os, re, sys
from pathlib import Path
LABELS={'ready':'Apta para Stage 3.5','blocked':'Aprobada Stage 3, bloqueada','watch':'En observación','wait_price':'Esperar precio','rejected':'Descartada'}
FIELDS=('Profundidad','Decisión','Ejecución','Ejecución (EN)')
KEYS=('Ticker','Informe (ID)','Fecha análisis')
def require(ok,msg):
 if not ok: raise ValueError(msg)
def load(p):return json.loads(Path(p).read_text())
def read_dec(root):
 text=(root/'data/dec.js').read_text();prefix='window.FP=window.FP||{};FP.dec='
 require(text.startswith(prefix),'Unsupported dec.js encoding')
 return json.loads(text[len(prefix):].strip().rstrip(';'))
def analysis_date(value):
 """ISO date or whole Google Sheets serial; never truncate time or guess locale."""
 if type(value) in (int,float):
  require(math.isfinite(value) and value==int(value),'Analysis date must be a whole finite Sheet serial')
  try:return (datetime.date(1899,12,30)+datetime.timedelta(days=int(value))).isoformat()
  except (OverflowError,ValueError):raise ValueError('Analysis date serial out of range')
 require(isinstance(value,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',value),'Analysis date must be ISO YYYY-MM-DD or numeric whole Sheet serial')
 return datetime.date.fromisoformat(value).isoformat()
def key(row,h):
 values=[row[h.index(k)] if h.index(k)<len(row) else '' for k in KEYS]
 return (str(values[0]),str(values[1]),analysis_date(values[2]))
def mapped_rows(snapshot):
 """Require explicit source geometry; sparse header+row cannot become row 2."""
 require(type(snapshot.get('sheetId')) is int,'Missing numeric sheetId')
 if 'rowIndices' in snapshot:
  require('startRowIndex' not in snapshot and 'contiguous' not in snapshot,'Ambiguous source geometry: choose rowIndices OR contiguous range')
  rows=snapshot['rowIndices']
  require(isinstance(rows,list) and len(rows)==len(snapshot['values']),'rowIndices must map every values row including header')
  require(all(type(i) is int and i>=0 for i in rows) and len(set(rows))==len(rows),'rowIndices must be unique nonnegative actual zero-based row indexes')
  return rows
 require(snapshot.get('contiguous') is True and type(snapshot.get('startRowIndex')) is int and snapshot['startRowIndex']>=0,'Ambiguous Sheet rows: supply contiguous:true + startRowIndex for an unfiltered range, or explicit rowIndices for every returned row')
 return list(range(snapshot['startRowIndex'],snapshot['startRowIndex']+len(snapshot['values'])))
def unique(values,k):
 h=values[0]; hits=[(i,row) for i,row in enumerate(values[1:],1) if any(v not in ('',None) for v in row) and key(row,h)==k]
 require(len(hits)==1,'Missing or duplicate canonical row: '+repr(k));return hits[0]
def contracts(root):
 registry=load(root/'data/stage35-assessments.json');require(registry.get('schemaVersion')==1,'Unknown assessment schema')
 out=[];seen=set();paths=set()
 for a in registry['assessments']:
  k=(a['ticker'],a['reportId'],analysis_date(a['analysisDate']));require(k not in seen,'Duplicate assessment key');seen.add(k)
  relative=Path(a['ticket']);p=(root/relative).resolve();require(p.is_relative_to(root.resolve()) and p.suffix=='.json','Unsafe ticket path');paths.add(p)
  t=load(p);state=t.get('publication');require(state==a['publication'],'Ticket versus registry publication mismatch: '+a['ticker'])
  require(t['ticker']==a['ticker'] and t['stage']=='Stage 3.5','Ticket identity/stage mismatch')
  require(t['as_of_utc']==a['assessedAt'],'Ticket assessment date mismatch')
  require(state['eligibility'] in LABELS,'Unknown eligibility')
  require(state['execution'] in ('suspended','not_authorized'),'Authorized execution requires separate supported reviewed workflow')
  require(t.get('trade_authorized') is False and type(t.get('approved_quantity')) is int and t['approved_quantity']==0,'Unapproved assessment cannot authorize quantity/trade')
  for f in ('operative_M','operative_stop_S','fundamental_buy_max','technical_buy_max','buy_signal'):
   require(f in t and t[f] is None,'Unapproved ticket has operative field: '+f)
  es='Suspendida: ' if state['execution']=='suspended' else ''
  en='Suspended: ' if state['execution']=='suspended' else ''
  expected={'Profundidad':'Stage 3 completo · Stage 3.5 en espera' if state['eligibility']=='ready' else 'Stage 3 completo', 'Decisión':LABELS[state['eligibility']], 'Ejecución':es+'sin entrada autorizada. Cantidad nueva 0. Sin señal, techo ni stop operativo. '+state.get('executionConditionEs','Requiere ficha nueva antes de cualquier entrada.'), 'Ejecución (EN)':en+'no entry authorized. New quantity 0. No signal, ceiling or operative stop. '+state.get('executionConditionEn','A new plan is required before any entry.')}
  out.append((k,a,t,expected))
 # Every structured ticket under research is registered; no ticker-specific match.
 for p in (root/'research').rglob('*.json'):
  try:d=load(p)
  except (ValueError,UnicodeDecodeError):continue
  if isinstance(d,dict) and d.get('stage')=='Stage 3.5' and 'approved_quantity' in d:
   require(p.resolve() in paths,'Unregistered Stage 3.5 ticket: '+str(p.relative_to(root)))
 return out

def project(root,values):
 result=copy.deepcopy(values);h=result[0]
 for k,a,t,expected in contracts(root):
  i,row=unique(result,k)
  require(analysis_date(row[h.index('Fecha análisis')])==analysis_date(a['analysisDate']),'Date mismatch')
  require(not any(analysis_date(r[h.index('Fecha análisis')])>analysis_date(a['analysisDate']) for r in result[1:] if len(r)>h.index('Fecha análisis') and r[h.index('Ticker')]==a['ticker']), 'Stale assessment superseded by newer decision')
  require(row[h.index('Decisión')]!='En cartera','Do not overwrite held classification; separate add-on assessment required')
  require(row[h.index('Máximo condicionado')] in ('',None),'Unapproved decision has operative ceiling')
  for field,v in expected.items():
   j=h.index(field)
   while len(row)<=j:row.append('')
   row[j]=v
 return result

def sheet_plan(root,snapshot,projected):
 row_indices=mapped_rows(snapshot)
 values=snapshot['values'];h=values[0]; requests=[];checks=[]
 for k,a,t,expected in contracts(root):
  idx,row=unique(values,k);localrow=unique(projected,k)[1]
  require(not any(analysis_date(r[h.index('Fecha análisis')])>analysis_date(a['analysisDate']) for r in values[1:] if len(r)>h.index('Fecha análisis') and r[h.index('Ticker')]==a['ticker']), 'Sheet has newer decision; refuse stale mapped update')
  require(row[h.index('Decisión')]!='En cartera','Sheet row held; do not overwrite')
  for field,value in expected.items():
   col=h.index(field);actual=row[col] if col<len(row) else ''
   checks.append({'key':list(k),'field':field,'expected':value,'rowIndex':row_indices[idx],'columnIndex':col})
   if actual!=value:requests.append({'updateCells':{'range':{'sheetId':snapshot['sheetId'],'startRowIndex':row_indices[idx],'endRowIndex':row_indices[idx]+1,'startColumnIndex':col,'endColumnIndex':col+1},'rows':[{'values':[{'userEnteredValue':{'stringValue':value}}]}],'fields':'userEnteredValue'}})
 return {'requests':requests,'verification':checks,'scope':'Only four canonical status fields. No network writes performed. Obtain actual Sheet read-back before publication.'}

def validate(root,readback):
 dec=read_dec(root);require(project(root,dec)==dec,'Local decisions disagree with structured assessment; run plan/apply-local and inspect changes')
 require(readback is not None,'BLOCKED: canonical Sheet write/read-back evidence not supplied')
 require(not readback.get('fixtureOnly',False),'BLOCKED: test fixture is not canonical Sheet evidence')
 require(readback.get('source')=='google-sheets-readback','Require actual connected-Sheets read-back, not a planned payload')
 captured=datetime.datetime.fromisoformat(readback['capturedAt'].replace('Z','+00:00'));require(captured.tzinfo is not None,'Readback timestamp must have timezone')
 for k,a,t,expected in contracts(root):
  require(captured>=datetime.datetime.fromisoformat(a['assessedAt'].replace('Z','+00:00')),'Readback predates assessment')
  h=readback['values'][0];idx,row=unique(readback['values'],k)
  require(not any(analysis_date(r[h.index('Fecha análisis')])>analysis_date(a['analysisDate']) for r in readback['values'][1:] if len(r)>h.index('Fecha análisis') and r[h.index('Ticker')]==a['ticker']), 'Read-back contains a newer decision; assessment is stale')
  for field,v in expected.items():require(row[h.index(field)]==v,'BLOCKED: unapplied/mismatched canonical Sheet status '+repr(k)+' '+field)
 return True

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['plan','apply-local','validate']);p.add_argument('--site-root',type=Path,default=Path(__file__).resolve().parent.parent);p.add_argument('--sheet-snapshot',type=Path);p.add_argument('--output',type=Path);p.add_argument('--sheet-readback',type=Path,default=os.environ.get('STAGE35_SHEET_READBACK'));a=p.parse_args();root=a.site_root.resolve()
 if a.command=='validate':validate(root,load(a.sheet_readback) if a.sheet_readback else None);print('Stage 3.5 local decisions and supplied Sheet read-back agree. Eligibility is not execution authorization.');return
 require(a.sheet_snapshot and a.output,'plan/apply-local requires --sheet-snapshot and private --output')
 require(not a.output.resolve().is_relative_to(root),'Keep Sheet payload/evidence outside public site root')
 rows=project(root,read_dec(root));plan=sheet_plan(root,load(a.sheet_snapshot),rows);a.output.mkdir(parents=True,exist_ok=True)
 (a.output/'sheet-updateCells.json').write_text(json.dumps({'requests':plan['requests']},ensure_ascii=False,indent=2));(a.output/'verification.json').write_text(json.dumps(plan['verification'],ensure_ascii=False,indent=2));(a.output/'dec.js').write_text('window.FP=window.FP||{};FP.dec='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n')
 if a.command=='apply-local':(root/'data/dec.js').write_bytes((a.output/'dec.js').read_bytes())
 print('Prepared '+str(len(plan['requests']))+' minimal Sheet cell updates. NOT APPLIED. Publication remains blocked until actual Sheet read-back agrees.')
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,OSError) as e:print('Stage 3.5 publication BLOCKED: '+str(e),file=sys.stderr);sys.exit(1)
