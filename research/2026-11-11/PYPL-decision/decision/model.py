"""Explicit FCFE reconstruction from A122 disclosed assumptions; USD millions.
Not an exact restoration of an unavailable original workbook. All choices exposed.
No debt subtraction or cash addition: net margins include financing costs and
credit funding is retained in equity cash flow. No free buybacks assumed.
"""
import json
from pathlib import Path
B=Path(__file__).parent
P={'sales_ttm':34295,'shares_proxy':858,'price':58.78,'date':'2026-11-10 16:00 EST','rf':.0498,'erp':.0441,'beta':1.32}
def value(growth=.03,margin0=.14,margin5=.145,credit=.02,ke=.115,g=.025,roe=.20,shares=858,permanent_credit=False,extra_cash=0):
 rev=P['sales_ttm']; rows=[]
 for y in range(1,11):
  fade=max(0,(y-5)/5);gr=growth if y<=5 else growth+(g-growth)*fade
  prev=rev;rev*=1+gr;m=margin0+(margin5-margin0)*min(y/5,1);ni=rev*m
  da=rev*.025;capex=rev*.025;acquis=rev*.005;cfunding=rev*credit;nwc=(rev-prev)*.05
  explicit=capex+acquis+cfunding+nwc-da
  terminal_reinvest=ni*g/roe
  # Blend net reinvestment, not both regimes stacked. Alternative keeps credit
  # and acquisitions fully funded through perpetuity.
  reinvest=explicit if permanent_credit else explicit*(1-fade)+terminal_reinvest*fade
  fcfe=ni-reinvest
  rows.append(dict(year=y,revenue=rev,growth=gr,net_margin=m,net_income=ni,da=da,capex=capex,acquisitions=acquis,credit_funding=cfunding,nwc=nwc,explicit_reinvestment=explicit,roe_reinvestment=terminal_reinvest,blended_reinvestment=reinvest,fcfe=fcfe,pv=fcfe/(1+ke)**y))
 term=rows[-1]['fcfe']*(1+g);pvt=term/(ke-g)/(1+ke)**10;eq=sum(r['pv'] for r in rows)+pvt+extra_cash
 return dict(assumptions=dict(growth=growth,margin0=margin0,margin5=margin5,credit=credit,ke=ke,g=g,roe=roe,shares=shares,permanent_credit=permanent_credit,extra_cash=extra_cash),rows=rows,terminal_fcfe=term,terminal_pv=pvt,equity=eq,value=eq/shares,terminal_fraction=pvt/eq)
if __name__=='__main__':
 obs=P['rf']+P['beta']*P['erp'];norm=P['rf']+P['erp']
 cases={'reconstructed_base':value(),'adverse':value(growth=0,margin0=.12,margin5=.12,credit=.025,ke=.125,g=.02,roe=.15),'recovery':value(growth=.06,margin0=.145,margin5=.165,credit=.015,ke=.105,g=.03,roe=.25),'base_observed_rate':value(ke=obs),'base_normalized_rate':value(ke=norm),'base_permanent_funding':value(permanent_credit=True),'observed_permanent_funding':value(ke=obs,permanent_credit=True),'base_basic_share_sensitivity':value(shares=830.658298)}
 sens={f'rate{rate}_credit{credit}':value(ke=rate,credit=credit) for rate in [.095,.105,.115,.125] for credit in [.01,.02,.03]}
 roots={}
 for name,kwargs in [('legacy_rate',{}),('observed_rate',{'ke':obs}),('permanent_funding',{'permanent_credit':True})]:
  lo,hi=-.02,.15
  for _ in range(100):
   mid=(lo+hi)/2
   if value(growth=mid,**kwargs)['value']<P['price']:lo=mid
   else:hi=mid
  roots[name]={'growth':mid,'value':value(growth=mid,**kwargs)['value']}
 out=dict(inputs=P,rates={'observed':obs,'normalized':norm},cases=cases,sensitivity=sens,price_implied_growth=roots,legacy_reference={'base':57.27,'adverse':33.93,'recovery':91.81,'reconstruction_is_not_exact_original':True})
 (B/'results.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(roots)
