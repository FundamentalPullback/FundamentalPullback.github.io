"""Offline stdlib-only operating comparison. Run python reproduce.py."""
import pathlib,json,csv
P=pathlib.Path(__file__).resolve().parent;S=json.loads((P/'source_numeric_subsets.json').read_text())
def get(t,label,i):
 return next(x['values'][i] for x in S[t]['rows'] if x['label']==label)
rows=[]
for ticker in ['ECL','MMM']:
 t=ticker.lower(); inc=t+'_7';cf=t+'_10'
 for period,idx in [('Q3 2026',0),('Q3 2025',1),('9M2026',2),('9M2025',3)]:
  rev=get(inc,'Net sales',idx);op=get(inc,'Operating income',idx)
  r={'ticker':ticker,'period':period,'revenue':rev,'gaap_operating_income':op,'operating_margin_pct':round(op/rev*100,4),'reported_diluted_eps':get(inc,'Diluted' if t=='ecl' else 'Earnings per share — diluted',idx),'cfo':None,'capex':None,'actual_cfo_less_capex':None,'depreciation_amortization':None,'sbc':None,'source_tables':[inc]}
  if period.startswith('9M'):
   i=idx-2;r['cfo']=get(cf,'Cash provided by operating activities' if t=='ecl' else 'Net cash provided by (used in) operating activities',i);r['capex']=-get(cf,'Capital expenditures' if t=='ecl' else 'Purchases of property, plant and equipment (PP&E)',i)
   r['actual_cfo_less_capex']=round(r['cfo']-r['capex'],3)
   r['depreciation_amortization']=round(get(cf,'Depreciation',i)+get(cf,'Amortization',i),3) if t=='ecl' else get(cf,'Depreciation and amortization',i)
   r['sbc']=get(cf,'Share-based compensation expense' if t=='ecl' else 'Stock-based compensation expense',i);r['source_tables'].append(cf)
  rows.append(r)
(P/'operating_peers.json').write_text(json.dumps({'units':'USD millions except EPS (USD/share) and percentages','scope':'Limited operating reference; no valuation or market multiples; quarterly cash-flow fields deliberately null because source cash-flow statements cover 9M','rows':rows},indent=2)+'\n')
with (P/'operating_peers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))
