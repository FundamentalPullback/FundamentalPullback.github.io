import pathlib,json,re,csv
p=pathlib.Path(__file__).parent
labels={'investment_income':'Total investment income |','nii':'Net investment income |','pik':'Total PIK interest income |','interest_cost':'Interest |','sbc':'Stock-based compensation |','realized':'Total net realized gain (loss) |','unrealized':'Total net change in unrealized appreciation (depreciation) |','net_income':'Net increase (decrease) in net assets resulting from operations |','net_expenses':'Total net operating expenses |'}
def vals(l):
 a=[]
 for x in l.split(' | '):
  if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):a.append(0 if x=='—' else float(x.replace(',','').replace('(','-').replace(')',''))/1000)
 return a
def get(file,n):
 entry=json.loads((p/'financial_source_inputs.json').read_text())[file]
 assert entry['columns']==n
 return entry['values']
annual=get('2026-02-12_htgc-20251231.htm.rows',3);a=get('2026-10-29_htgc-20260930.htm.rows',4);b=get('2025-10-30_htgc-20250930.htm.rows',4);h=get('2026-07-30_htgc-20260630.htm.rows',4);q=get('2026-05-05_htgc-20260331.htm.rows',2)
def row(label,d,i):return {'period':label,**{k:v[i] for k,v in d.items()}}
out=[row('FY2023',annual,2),row('FY2024',annual,1),row('FY2025',annual,0)]
out.append({'period':'Q4_2025',**{k:v[0]-a[k][3] for k,v in annual.items()}});out +=[row('Q1_2026',q,0),row('Q2_2026',h,0),row('Q3_2026',a,0)]
for name,d,idx in [('TTM202609',a,0),('TTM202509',b,1)]:out.append({'period':name,**{k:v[idx]+d[k][2]-d[k][3] for k,v in annual.items()}})
for r in out:r['nii_less_pik_not_cashflow']=r['nii']-r['pik']
for k in annual:assert abs(sum(r[k] for r in out[3:7])-out[7][k])<1e-7,k
(p/'history.json').write_text(json.dumps(out,indent=2));w=csv.DictWriter((p/'history.csv').open('w'),fieldnames=out[0]);w.writeheader();w.writerows(out);print(json.dumps(out,indent=2))
