"""Offline, stdlib-only reproduction from portable extracted SEC numeric facts."""
import json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
facts=json.loads((ROOT/'source_numeric_facts.json').read_text())
MAP={'revenue':'Revenues','ebit':'OperatingIncomeLoss','parent_net_income':'NetIncomeLoss','gaap_diluted_eps':'EarningsPerShareDiluted','cfo':'NetCashProvidedByUsedInOperatingActivities','da':'DepreciationDepletionAndAmortization','sbc':'ShareBasedCompensation','cash_capex':'PaymentsToAcquirePropertyPlantAndEquipment','financing_receivables_cash_use':'IncreaseDecreaseInFinanceReceivables','finance_originations_rounded':'PaymentsToAcquireFinanceReceivables'}
def get(start,end,tag,seg=None):
 matches=[r for r in facts if r.get('startdate')==start and r.get('enddate')==end and r['tag']=='us-gaap:'+tag and (not r.get('dimensions') if seg is None else r.get('dimensions',{}).get('us-gaap:StatementBusinessSegmentsAxis')==seg and len(r.get('dimensions',{}))==2)]
 if not matches:return None
 vals={r['value'] for r in matches}
 assert len(vals)==1,(start,end,tag,vals)
 return matches[0]['value']/(1 if 'PerShare' in tag else 1e6)
def period(label,start,end):
 p={'period':label,'start':start,'end':end}
 for k,t in MAP.items():p[k]=get(start,end,t)
 for label,seg in [('isg','dell:InfrastructureSolutionsGroupMember'),('csg','dell:ClientSolutionsMember')]:
  for suffix,t in [('revenue','Revenues'),('ebit','OperatingIncomeLoss')]:p[label+'_'+suffix]=get(start,end,t,seg)
 return p
p={}
for label,start,end in [('FY2024','2023-02-04','2024-02-02'),('FY2025','2024-02-03','2025-01-31'),('FY2026','2025-02-01','2026-01-30'),('H1FY2025','2024-02-03','2024-08-02'),('H1FY2026','2025-02-01','2025-08-01'),('H1FY2027','2026-01-31','2026-07-31'),('9MFY2026','2025-02-01','2025-10-31'),('Q3FY2026','2025-08-02','2025-10-31'),('Q1FY2027','2026-01-31','2026-05-01'),('Q2FY2027','2026-05-02','2026-07-31')]:p[label]=period(label,start,end)
keys=list(p['FY2026'])[3:]
# Quarter cash flows are cumulative differences; income statements and segments use direct quarterly reports.
for q,a,b in [('Q3FY2026','9MFY2026','H1FY2026'),('Q2FY2027','H1FY2027','Q1FY2027')]:
 for k in keys:
  if p[q][k] is None and p[a][k] is not None and p[b][k] is not None and k!='gaap_diluted_eps':p[q][k]=round(p[a][k]-p[b][k],6)
p['Q4FY2026']={'period':'Q4FY2026','start':'2025-11-01','end':'2026-01-30',**{k:round(p['FY2026'][k]-p['9MFY2026'][k],6) if p['FY2026'][k] is not None and p['9MFY2026'][k] is not None else None for k in keys}}
p['Q4FY2026']['gaap_diluted_eps']=get('2025-11-01','2026-01-30','EarningsPerShareDiluted') # Published earnings release, not FY minus nine-month EPS.
for label,annual,new,old,start,end,eps in [('TTM','FY2026','H1FY2027','H1FY2026','2025-08-02','2026-07-31',sum(p[q]['gaap_diluted_eps'] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])),('PriorTTM','FY2025','H1FY2026','H1FY2025','2024-08-03','2025-08-01',sum(get(a,b,'EarningsPerShareDiluted') for a,b in [('2024-08-03','2024-11-01'),('2024-11-02','2025-01-31'),('2025-02-01','2025-05-02'),('2025-05-03','2025-08-01')]))]:
 p[label]={'period':label,'start':start,'end':end,**{k:round(p[annual][k]+p[new][k]-p[old][k],6) if all(p[x][k] is not None for x in [annual,new,old]) else None for k in keys}}
 p[label]['gaap_diluted_eps']=round(eps,2)
for r in p.values():
 r['cfo_less_cash_capex']=round(r['cfo']-r['cash_capex'],6) if r['cfo'] is not None and r['cash_capex'] is not None else None
 r['ebit_margin_pct']=round(100*r['ebit']/r['revenue'],4)
 r['cfo_less_capex_and_sbc']=round(r['cfo_less_cash_capex']-r['sbc'],6) if r['cfo_less_cash_capex'] is not None and r['sbc'] is not None else None
out={'units':'USD millions except diluted EPS USD/share; cash_capex and financing_receivables_cash_use positive denote use; finance originations rounded to nearest $100m','periods':list(p.values()),'ttm_yoy_pct':{k:round(100*(p['TTM'][k]/p['PriorTTM'][k]-1),4) for k in ['revenue','ebit','parent_net_income','gaap_diluted_eps','cfo','cfo_less_cash_capex']}}
(ROOT/'normalized_history.json').write_text(json.dumps(out,indent=2)+'\n')
with (ROOT/'normalized_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(p['FY2026']));w.writeheader();w.writerows(p.values())
print(json.dumps(out,indent=2))
