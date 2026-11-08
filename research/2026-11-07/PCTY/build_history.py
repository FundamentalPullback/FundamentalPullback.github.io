import json,pathlib,re
P=pathlib.Path(__file__).parent
labels={'revenue':'Total revenues','recurring':'Recurring and other revenue','float_income':'Interest income on funds held for clients','ebit':'Operating income','net_income':'Net income','cfo':'Net cash provided by operating activities','sbc':'Stock-based compensation expense','da':'Depreciation and amortization expense','software_cash':'Capitalized internal-use software costs','ppe_cash':'Purchases of property and equipment','contract_net_cash':'Deferred contract costs','software_amort':'Amortization of capitalized internal-use software costs','rd_capitalized_total':'Capitalized portion of research and development'}
def get(file):
 lines=json.loads((P/'financial_source_inputs.json').read_text())[file];out={}
 for k,l in labels.items():
  matches=[x for x in lines if x.split(' | ')[0]==l and '%' not in x]
  if k=='contract_net_cash':matches=[x for x in matches if '(' in x]
  if not matches:continue
  vals=[]
  for x in matches[0].split(' | ')[1:]:
   if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):vals.append(-float(x[1:-1].replace(',',''))/1000 if x.startswith('(') else float(x.replace(',','').replace('—','0'))/1000)
  out[k]=vals
 return out
annual=get('2026-08-05_pcty-20260630.htm.rows');a={str(y):{k:v[i] for k,v in annual.items() if len(v)==3} for i,y in enumerate([2024,2025,2026])}
qfiles={'q1_27':'2026-11-06_pcty-20260930.htm.rows','q3_26':'2026-05-08_pcty-20260331.htm.rows','q2_26':'2026-02-06_pcty-20251231.htm.rows','q1_26':'2025-11-05_pcty-20250930.htm.rows'}
raw={k:get(v) for k,v in qfiles.items()};q={}
for tag,d in raw.items():q[tag]={k:v[-1] if len(v)==2 else v[1] for k,v in d.items() if v}
# Quarterly income statements contain prior/current quarter then prior/current year to date. Cash flow only prior/current year to date.
flow=['cfo','sbc','da','software_cash','ppe_cash','contract_net_cash']
for k in flow:
 if k in q['q3_26'] and k in q['q2_26']:q['q3_26'][k]-=raw['q2_26'][k][-1]
 if k in q['q2_26'] and k in q['q1_26']:q['q2_26'][k]-=raw['q1_26'][k][-1]
q['q4_26']={k:a['2026'][k]-sum(q[z][k] for z in ['q1_26','q2_26','q3_26']) for k in a['2026'] if all(k in q[z] for z in ['q1_26','q2_26','q3_26'])}
ttm={}
for y,i in [(2026,1),(2025,0)]:
 d=raw['q1_27'] if y==2026 else raw['q1_26'];ttm[str(y)]={k:a[str(y)][k]+d[k][-1]-d[k][0] for k in a[str(y)] if k in d and len(d[k])==2}
for d in list(a.values())+list(q.values())+list(ttm.values()):
 if all(k in d for k in ['cfo','software_cash','ppe_cash','sbc']):d['fcf']=d['cfo']+d['software_cash']+d['ppe_cash'];d['owner_cash_after_expensed_sbc']=d['fcf']-d['sbc']
j={'units':'USD millions; negative cash investment signs','annual':a,'quarters':q,'paired_ttm':ttm,'raw':raw,'source_map':qfiles,'quarter_method':'Q4=annual minus nine months; Q2/Q3 CF differences; income standalone columns'}
(P/'history.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2))
