import pathlib,json,re,csv
p=pathlib.Path(__file__).parent
labels={'revenue':'Oil and gas sales |','operating':'Income from operations |','net':'Net income |','parent_net':'Net income attributable to Class A Common Stock |','cfo':'Net cash provided by operating activities |','development':'Drilling and development capital expenditures |','other_capex':'Purchases of other property and equipment |','acquisitions':'Acquisition of oil and natural gas properties, net |','sbc':'Stock-based compensation expense |','da':'Depreciation, depletion and amortization |','derivatives':'Net gain (loss) on derivative instruments |','interest':'Interest expense |','cash_tax':'Cash paid (refunded) for income taxes |'}
cf=['cfo','development','other_capex','acquisitions','sbc','cash_tax']
def nums(l):
 l=l.replace(' | )',')');a=[]
 for x in l.split(' | '):
  if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):a.append(0 if x=='—' else float(x.replace(',','').replace('(','-').replace(')',''))/1000)
 return a
def get(file,n):
 entry=json.loads((p/'financial_source_inputs.json').read_text())[file]
 assert entry['columns']==n
 return entry['values']
annual=get('2026-02-26_pr-20251231.htm.rows',3);q3=get('2026-11-05_pr-20260930.htm.rows',4);q2=get('2026-08-06_pr-20260630.htm.rows',4);q1=get('2026-05-07_pr-20260331.htm.rows',2);old=get('2025-11-06_pr-20250930.htm.rows',4)
out=[{'period':'FY'+str(y),**{k:v[i] for k,v in annual.items()}} for y,i in [(2023,2),(2024,1),(2025,0)]]
out.append({'period':'Q4_2025',**{k:v[0]-q3[k][1 if k in cf else 3] for k,v in annual.items()}})
out.append({'period':'Q1_2026',**{k:v[0] for k,v in q1.items()}})
for label,cur,prev in [('Q2_2026',q2,q1),('Q3_2026',q3,q2)]:out.append({'period':label,**{k:v[0]-(prev[k][0] if k in cf else 0) for k,v in cur.items()}})
for label,cur,ai in [('TTM202609',q3,0),('TTM202509',old,1)]:out.append({'period':label,**{k:v[ai]+cur[k][0 if k in cf else 2]-cur[k][1 if k in cf else 3] for k,v in annual.items()}})
for r in out:
 r['cfo_less_dev_othercapex']=r['cfo']+r['development']+r['other_capex'];r['cash_after_acquisitions']=r['cfo_less_dev_othercapex']+r['acquisitions']
for k in annual:assert abs(sum(x[k] for x in out[3:7])-out[7][k])<1e-7,k
(p/'history.json').write_text(json.dumps(out,indent=2));w=csv.DictWriter((p/'history.csv').open('w'),fieldnames=out[0]);w.writeheader();w.writerows(out);print(json.dumps(out,indent=2))
