from pathlib import Path
import json,csv,re
P=Path(__file__).parent
# Source statement cells in USD thousands. Table indexes are zero-based in captured HTML.
def row(s,t,label,col):
 a=json.loads((P/'sources'/f'{s}_tables.json').read_text())[t]['rows'];r=next(r for r in a if r and r[0]==label)
 n=[]
 for x in r[1:]:
  if x=='—':n.append(0)
  elif re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?',x): n.append(float(x.replace(',','').replace('(','-').replace(')','')))
 return int(n[col])
labels={'revenue':'Revenues','ebit':'Operating income','net_income':'Net income','da':'Depreciation and amortization','cfo':'Net cash provided by operating activities','cash_capex':'Additions to property and equipment','sbc':'Stock-based compensation','acquisitions':'Acquisitions, net of cash acquired'}
a={};source_map={}
def make(name,s,inc,cf,ic,cc,net):
 v={}
 for k,l in labels.items():
  if k=='net_income':l=net
  v[k]=row(s,inc if k in ['revenue','ebit','net_income'] else cf,l,ic if k in ['revenue','ebit','net_income'] else cc)
 for k in ['cash_capex','acquisitions']:v[k]=-v[k]
 a[name]=v;source_map[name]={'source':s,'income_table':inc,'cash_table':cf,'income_column':ic,'cash_column':cc}
for i,y in enumerate([2025,2024,2023]):make('FY'+str(y),'S3',37,40,i,i,'Net income')
make('9M2026','S1',18,22,2,0,'Net (loss) income');make('9M2025','S1',18,22,3,1,'Net (loss) income');make('9M2024','S6',18,22,3,1,'Net income')
make('H12026','S4',18,22,2,0,'Net income (loss)');make('Q12026','S5',18,22,0,0,'Net loss')
def diff(name,x,y):a[name]={k:a[x][k]-a[y][k] for k in labels}
diff('Q42025','FY2025','9M2025');diff('Q22026','H12026','Q12026');diff('Q32026','9M2026','H12026')
for yr in [2025,2026]:a['TTMSep'+str(yr)]={k:a['FY'+str(yr-1)][k]-a['9M'+str(yr-1)][k]+a['9M'+str(yr)][k] for k in labels}
for v in a.values():v['simple_fcf']=v['cfo']-v['cash_capex'];v['fcf_less_sbc_diagnostic']=v['simple_fcf']-v['sbc']
for k in labels:assert sum(a[x][k] for x in ['Q42025','Q12026','Q22026','Q32026'])==a['TTMSep2026'][k]
metrics={k+'_growth_pct':100*(a['TTMSep2026'][k]/a['TTMSep2025'][k]-1) for k in ['revenue','ebit','cfo','simple_fcf']}
metrics.update(q3_simple_fcf=80805-78187,q3_simple_fcf_prior=93565-65925,q3_adjusted_fcf=80805-78187+331+17671+6350+1255+4606+132,nine_month_adjusted_fcf=241831-200475+971+38281+19111+5731+4606+1025,nine_month_adjusted_fcf_gap=111081-(241831-200475),net_principal_debt=1393985-11741,operating_lease_liabilities=12264+77150,closure_rollforward=192722+10890+2726+11919-7147,shares_oct15=62655943+988200,market_cap_scanner_m=(62655943+988200)*92.7/1e6,q3_ebit_plus_impairment=15649+13593,adjusted_ebitda_margin_q3=133471/559231*100,prior_adjusted_ebitda_margin_q3=119853/485351*100)
out={'units':'USD thousands, except explicit metrics','source_map':source_map,'periods':a,'metrics':metrics,'rounding_notes':['Q3 D&A directly 88066 versus cumulative-derived88065; Q2 directly88498 versus derived88499. Difference1 means $1000, not a changed economic conclusion.'],'valuation':None,'entryApproved':False}
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in a.items())
print(json.dumps(out,indent=2))
