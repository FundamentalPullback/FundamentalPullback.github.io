#!/usr/bin/env python3
"""Offline stdlib-only build. Input is minimal factual records, no SEC network dependency."""
import json,csv,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parent
raw=json.loads((P/'numeric_inputs.json').read_text()); facts=raw['facts']; cells={}; ledger=[]
FLOW=['revenue','ebit','net_income_consolidated','net_income_attributable','nci_income','eps_diluted','cfo','capex','sbc','dda']
STOCK=['cash','cash_including_restricted','restricted_cash_current','restricted_cash_noncurrent','debt','debt_current','debt_noncurrent','nci_equity']
def add(p,m,v,method,refs,source=None):
 key=p+'.'+m;cells[key]=v
 record={'cell':key,'value':v,'unit':'USD/share' if m=='eps_diluted' else ('percent' if m.endswith('_margin_pct') else 'USD million'),'method':method,'dependencies':refs,'source':source}
 ledger.append(record)
for p,ms in facts.items():
 for m,x in ms.items():add(p,m,x['value'],'reported',[],x)
def derive(p,m,refs,fn,method):
 if p+'.'+m not in cells and all(r in cells for r in refs):add(p,m,round(fn(*[cells[r] for r in refs]),8),method,refs)
for p in facts:
 derive(p,"debt",[p+".debt_current",p+".debt_noncurrent"],lambda a,b:a+b,"Current debt plus noncurrent debt")
for y in [2024,2025,2026]:
 for q in [1,2,3]:
  for m in FLOW:
   if m=='eps_diluted':continue
   refs=[f'YTD{q}_{y}.{m}']+([f'YTD{q-1}_{y}.{m}'] if q>1 else [])
   derive(f'Q{q}_{y}',m,refs,lambda a,b=0:a-b,'YTD difference' if q>1 else 'Q1 equals YTD1')
for y in [2024,2025]:
 for m in FLOW:
  if m=='eps_diluted':continue
  derive(f'Q4_{y}',m,[f'FY{y}.{m}',f'YTD3_{y}.{m}'],lambda a,b:a-b,'FY minus latest nine-month comparator; see CFO discrepancy flag')
 for m in STOCK:derive(f'Q4_{y}',m,[f'FY{y}.{m}'],lambda a:a,'Year-end balance')
for y in [2025,2026]:
 p=f'TTM_Q3_{y}'
 for m in FLOW:
  if m=='eps_diluted':
   derive(p,m,[f'Q4_{y-1}.{m}']+[f'Q{q}_{y}.{m}' for q in [1,2,3]],lambda *a:sum(a),'Sum of four directly reported quarterly EPS; rounded sum, not GAAP TTM EPS')
  else:derive(p,m,[f'FY{y-1}.{m}',f'YTD3_{y}.{m}',f'YTD3_{y-1}.{m}'],lambda a,b,c:a+b-c,'Prior FY plus current nine months minus prior nine months')
 for m in STOCK:derive(p,m,[f'Q3_{y}.{m}'],lambda a:a,'Quarter-end balance, not summed')
periods=[f'FY{y}' for y in range(2019,2026)]+[f'Q{q}_{y}' for y,qs in [(2024,[4]),(2025,[1,2,3,4]),(2026,[1,2,3])] for q in qs]+['TTM_Q3_2025','TTM_Q3_2026']
for p in periods:
 derive(p,'restricted_cash_total',[p+'.cash_including_restricted',p+'.cash'],lambda a,b:a-b,'Total cash including restricted minus unrestricted cash')
 derive(p,'restricted_cash_noncurrent',[p+'.restricted_cash_total',p+'.restricted_cash_current'],lambda a,b:a-b,'Total restricted less current restricted')
 derive(p,'net_debt',[p+'.debt',p+'.cash'],lambda a,b:a-b,'Debt less cash; restricted cash not deducted; no smelter debt exclusion')
 derive(p,'fcf_consolidated',[p+'.cfo',p+'.capex'],lambda a,b:a-b,'Consolidated CFO minus capital expenditures; not shareholder owner earnings')
 derive(p,'fcf_after_sbc_consolidated',[p+'.fcf_consolidated',p+'.sbc'],lambda a,b:a-b,'Consolidated CFO-capex-SBC diagnostic; not owner earnings')
 derive(p,'ebit_margin_pct',[p+'.ebit',p+'.revenue'],lambda a,b:a/b*100,'Operating income divided by revenue, percent')
 derive(p,'nci_income',[p+'.net_income_consolidated',p+'.net_income_attributable'],lambda a,b:a-b,'Consolidated net income minus attributable income')
metrics=FLOW+STOCK+['restricted_cash_total','net_debt','fcf_consolidated','fcf_after_sbc_consolidated','ebit_margin_pct']
rows=[{'period':p,**{m:cells.get(p+'.'+m) for m in metrics},'capex_software_separate':None} for p in periods]
flags=['Q3 2026 uses unaudited October 27 release; latest retrieved 10-Q is June 30, 2026.','CFO nine-month 2025: latest comparative 4942 vs original 4917. Reason not established. Q4 2025 latest-comparative residual 668 vs direct release693; TTM current 6192 vs direct-quarter sum6217. Neither silently harmonized.','Capital expenditure is reported total productive-asset expenditure. Separate software capex not disclosed in inputs, never assumed zero.','FY2022 EPS is blank because a direct reported figure was not retained. TTM EPS is sum of four rounded directly reported quarters, not a filing EPS.','FY2019 NCI source tag sign fails the income bridge; normalized NCI derives from consolidated minus attributable income; original tag retained separately.','Balance and cash flow are consolidated, except Morenci72% proportionate share. PTFI and Cerro Verde include100% before NCI. Not parent-only owner cash flow.']
checks=[]
for p in periods:
 a=[cells.get(p+'.'+m) for m in ['net_income_consolidated','net_income_attributable','nci_income']]
 if all(x is not None for x in a):
  assert abs(a[0]-a[1]-a[2])<.01,(p,a)
  checks.append(p+' NI consolidated = attributable + NCI')
for m in FLOW:
 k='TTM_Q3_2026.'+m
 if k in cells and m!='eps_diluted':
  qs=[cells.get('Q4_2025.'+m)]+[cells.get(f'Q{q}_2026.'+m) for q in [1,2,3]]
  if all(x is not None for x in qs):assert abs(cells[k]-sum(qs))<.01,(m,qs,cells[k])
assert cells['Q4_2025.eps_diluted']==.28
assert cells['Q4_2024.eps_diluted']==.19
assert cells['TTM_Q3_2026.cfo']==6192
(P/'history.json').write_text(json.dumps({'as_of':raw['as_of'],'units':'USD million except EPS and margin','periods':rows,'flags':flags},indent=2)+'\n')
with (P/'history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
with (P/'ledger.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['cell','value','unit','method','dependencies','url','source_locator_or_tag'])
 for x in ledger:
  s=x['source'] or {};w.writerow([x['cell'],x['value'],x['unit'],x['method'],';'.join(x['dependencies']),s.get('url',''),s.get('locator',s.get('tag',''))])
(P/'qa.txt').write_text('PASS: '+str(len(checks))+' net-income perimeter checks; TTM additivity checks; direct Q4 EPS; CFO discrepancy retained.\n'+'\n'.join(flags)+'\n')
(P/'checksums.txt').write_text(''.join(hashlib.sha256((P/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in ['numeric_inputs.json','rebuild_history.py','history.json','history.csv','ledger.json','ledger.csv','qa.txt']))
print(json.dumps(rows[-1],indent=2))
