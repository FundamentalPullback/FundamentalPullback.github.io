from pathlib import Path
import json,csv,re
P=Path(__file__).parent
def row(s,t,label,col):
 r=next(r for r in json.loads((P/'sources'/f'{s}_tables.json').read_text())[t]['rows'] if r and r[0]==label)
 nums=[]
 for v in r[1:]:
  v=v.replace('\u200b','').strip()
  if v in ['—','–']:nums.append(0)
  elif re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?',v):nums.append(float(v.replace(',','').replace('(','-').replace(')','')))
 return int(nums[col])
labels={'revenue':'Total revenue','ebit':'Income from operations','parent_net':'Net income attributable to Texas Roadhouse, Inc. and subsidiaries','da':'Depreciation and amortization','cfo':'Net cash provided by operating activities','capex':'Capital expenditures—property and equipment','sbc':'Share-based compensation expense','acquisitions':'Acquisitions of franchise restaurants, net of cash acquired'}
a={};maps={}
def make(name,s,it,ct,ic,cc):
 v={k:row(s,it if k in ['revenue','ebit','parent_net'] else ct,l,ic if k in ['revenue','ebit','parent_net'] else cc) for k,l in labels.items()}
 for k in ['capex','acquisitions']:v[k]=-v[k]
 a[name]=v;maps[name]=[s,it,ct,ic,cc]
for i,y in enumerate([2025,2024,2023]):make('FY'+str(y),'S3',109,111,i,i)
make('9M2026','S1',9,14,2,0);make('9M2025','S1',9,14,3,1);make('9M2024','S6',7,10,3,1)
make('H12026','S4',7,10,2,0);make('Q12026','S5',7,9,0,0)
def calc(n,*terms):a[n]={k:sum(sign*a[p][k] for sign,p in terms) for k in labels}
calc('Q42025',(1,'FY2025'),(-1,'9M2025'));calc('Q22026',(1,'H12026'),(-1,'Q12026'));calc('Q32026',(1,'9M2026'),(-1,'H12026'))
calc('TTM2026',(1,'FY2025'),(-1,'9M2025'),(1,'9M2026'));calc('TTM2025',(1,'FY2024'),(-1,'9M2024'),(1,'9M2025'))
for v in a.values():v.update(simple_fcf=v['cfo']-v['capex'],cash_after_acquisitions=v['cfo']-v['capex']-v['acquisitions'],fcf_less_sbc_diagnostic=v['cfo']-v['capex']-v['sbc'],ebit_margin_pct=100*v['ebit']/v['revenue'])
checks={k:sum(a[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])==a['TTM2026'][k] for k in labels};assert all(checks.values())
diag={'9m_cfo_growth_pct':100*(a['9M2026']['cfo']/a['9M2025']['cfo']-1),'9m_simple_fcf_growth_pct':100*(a['9M2026']['simple_fcf']/a['9M2025']['simple_fcf']-1),'ttm_revenue_growth_pct':100*(a['TTM2026']['revenue']/a['TTM2025']['revenue']-1),'ttm_ebit_growth_pct':100*(a['TTM2026']['ebit']/a['TTM2025']['ebit']-1),'cash_taxes_reduction':61786-25905,'cash_less_debt':141412-50000,'operating_leases':33585+1032210,'market_cap_at_scanner_m':65.625375*191.1296,'q3_restaurant_margin_bridge':102988-7171+9626+60317+3596+59282,'9m_fcf_after_acq_sbc':a['9M2026']['cash_after_acquisitions']-a['9M2026']['sbc']}
out={'units':'USD thousands unless labeled otherwise','scanner':{'date':'2026-11-09','opportunity':70,'price':191.1296},'source_maps':maps,'periods':a,'diagnostics':diag,'quarter_tieout':checks,'status':'factual partial; no canonical valuation or entry approval'}
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in a.items())
print(json.dumps(out,indent=2))
