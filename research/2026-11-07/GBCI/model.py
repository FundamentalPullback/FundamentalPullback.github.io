"""GBCI residual-income illustration, not decision-ready. USD/share; no net-debt deduction for a bank."""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
B0=4339.861/130.218983
PRICE=48.16
# GAAP common equity includes AOCI and goodwill. No assumed AOCI reversal, buybacks or acquisitions.
def ri(roe1,roe5,roet,ke,growth,g=.025):
 b=B0; pv=0; rows=[]
 for y in range(1,11):
  r=roe1+(roe5-roe1)*(y-1)/4 if y<=5 else roe5+(roet-roe5)*(y-5)/5
  gy=growth if y<=5 else growth+(g-growth)*(y-5)/5
  eps=b*r; retained=b*gy; fcfe=eps-retained; residual=eps-ke*b; disc=(1+ke)**y
  rows.append(dict(year=y,opening_book=b,roe=r,eps=eps,growth=gy,retained=retained,distribution=fcfe,residual=residual,pv_ri=residual/disc,closing_book=b+retained))
  pv+=residual/disc;b+=retained
 terminal=(roet-ke)*b/(ke-g);pvt=terminal/(1+ke)**10
 # FCFE equivalence: terminal distribution = (ROE-g)*book.
 fcfe_value=sum(x['distribution']/(1+ke)**x['year'] for x in rows)+(roet-g)*b/(ke-g)/(1+ke)**10
 value=B0+pv+pvt
 return dict(value=value,book_initial=B0,pv_explicit_residual=pv,pv_terminal_residual=pvt,terminal_residual_share=pvt/value,fcfe_equivalent=fcfe_value,tieout=value-fcfe_value,ke=ke,g=g,roe_terminal=roet,rows=rows)
cases={'adverso':(.075,.08,.08,.115,.025),'central':(.092,.105,.10,.10,.04),'favorable':(.105,.125,.115,.09,.055)}
out={k:ri(*v) for k,v in cases.items()}
lo,hi=.08,.25
for _ in range(80):
 mid=(lo+hi)/2
 if ri(mid,mid,mid,.10,.04)['value']<PRICE:lo=mid
 else:hi=mid
out['reverse_constant_roe']=(lo+hi)/2
out['price']=PRICE
out['capm_reference']={'treasury_yield':.0486,'beta_5y_monthly':.77,'erp_nov1':.0441,'raw_ke':.0486+.77*.0441,'convention':'Treasury unadjusted, ERP unadjusted; no double addition of US default spread; reference only. Scenario Ke 9-11.5% analyst overlay.'}
out['sensitivity']=[{'ke':k,'g':g,'value':ri(.092,.105,.10,k,.04,g)['value']} for k in [.09,.10,.11,.12] for g in [.015,.025,.035]]
# Mechanical two-year stress, not a regulatory capital forecast: same-size balance sheet.
nii=1101.067; loans=21619.530; tax=.213; shares=130.433235
out['stress']={'nii_decline_200bp_year2':nii*.0545,'extra_credit_provision_50bp':loans*.005,'net_income_hit_aftertax':(nii*.0545+loans*.005)*(1-tax),'eps_hit':(nii*.0545+loans*.005)*(1-tax)/shares,'not_validated':'No RWA, deposit-run, asset-sale losses or holding-company remittance cascade; do not approve.'}
(P/'results.json').write_text(json.dumps(out,indent=2))
for k in cases:
 with (P/f'{k}-projection.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=out[k]['rows'][0]);w.writeheader();w.writerows(out[k]['rows'])
print(json.dumps({k:{f:v[f] for f in ['value','tieout','pv_terminal_residual']} for k,v in out.items() if k in cases},indent=2));print('reverse',out['reverse_constant_roe'],'stress',out['stress'])
