from pathlib import Path
import json
p=Path(__file__).parent
f=json.loads((p/'facts/inputs.json').read_text())
h=json.loads((p/'history/history.json').read_text())['rows'];a=next(r for r in h if r['period']=='TTM2026') if any(r['period']=='TTM2026' for r in h) else h[-1]
# Fixed disclosed TTM anchors independently tie out to history in qa.py.
REV=666.1; EBIT=97.1; TAX=.25; SHARES=87.7
BRIDGE=f['cash']-f['debt']-f['utb']-f['deferred_comp']-f['cash_repatriation_stress']-.3
CASES={'bear':dict(g=.02,m1=.12,m5=.13,mt=.12,wacc=.125,gt=.01,roic=.12),'base':dict(g=.08,m1=.16,m5=.18,mt=.17,wacc=.11,gt=.02,roic=.15),'bull':dict(g=.13,m1=.18,m5=.23,mt=.21,wacc=.095,gt=.025,roic=.20)}
def calc(c,capex_rate=.05,bridge=BRIDGE,shares=SHARES,margin_on_installed_capacity=False):
 rows=[];rev=REV;prev_nopat=EBIT*(1-TAX);pv=0
 for y in range(1,11):
  g=c['g'] if y<=5 else c['g']+(c['gt']-c['g'])*(y-5)/5
  m=c['m1']+(c['m5']-c['m1'])*(y-1)/4 if y<=5 else c['m5']+(c['mt']-c['m5'])*(y-5)/5
  prior_rev=rev;rev*=1+g;nopat=rev*m*(1-TAX)
  depreciation=rev*21.9/666.1;amort=16.1*(1-y/10);da=depreciation+amort;capex=rev*capex_rate;nwc=max(0,rev-prior_rev)*.30
  physical=capex-da+nwc;economic=(nopat*max(0,g) if margin_on_installed_capacity else max(0,nopat-prev_nopat))/c['roic'];reinvestment=max(0,physical,economic);reserve=reinvestment-physical
  fcff=nopat-reinvestment;pv_fcff=fcff/(1+c['wacc'])**y;pv+=pv_fcff
  rows.append(dict(year=y,revenue=rev,growth=g,margin=m,nopat=nopat,depreciation=depreciation,amortization=amort,da=da,capex=capex,delta_nwc=nwc,physical_reinvestment=physical,economic_reinvestment=economic,additional_reinvestment_reserve=reserve,reinvestment=reinvestment,fcff=fcff,pv_fcff=pv_fcff));prev_nopat=nopat
 tr=rev*(1+c['gt']);tn=tr*c['mt']*(1-TAX);tp=tr*capex_rate-tr*21.9/666.1+(tr-rev)*.30;te=tn*c['gt']/c['roic'];ti=max(0,tp,te);tf=tn-ti;tv=tf/(c['wacc']-c['gt']);pt=tv/(1+c['wacc'])**10;ev=pv+pt
 return dict(assumptions=c,rows=rows,terminal=dict(revenue=tr,nopat=tn,physical_reinvestment=tp,economic_reinvestment=te,reinvestment=ti,fcff=tf,value=tv,pv=pt),ev=ev,bridge=bridge,equity=ev+bridge,value_per_share=(ev+bridge)/shares,shares=shares,terminal_share_pct=pt/ev*100)
r={k:calc(c) for k,c in CASES.items()}
sens={}
for w in [.095,.11,.125]:
 for g in [.01,.02,.03]:
  c=dict(CASES['base'],wacc=w,gt=g);sens[f'wacc{w}_g{g}']=calc(c)['value_per_share']
for k,b in [('include_syntiant_at_carrying_not_fair_value',BRIDGE+89.3),('no_repatriation_stress',BRIDGE+3),('double_repatriation_stress',BRIDGE-3),('no_deferred_comp_reserve',BRIDGE+13.7)]:sens[k]=calc(CASES['base'],bridge=b)['value_per_share']
sens['margin_on_installed_capacity_sales_growth_funding']=calc(CASES['base'],margin_on_installed_capacity=True)['value_per_share']
sens['capex_6pct']=calc(CASES['base'],capex_rate=.06)['value_per_share'];sens['shares_plus_point3_million']=calc(CASES['base'],shares=88)['value_per_share']
# Reverse margin: scan first, solve only demonstrated bracket, keeping same investment formula.
scan=[]
for i in range(-100,401):
 d=i/1000;c=dict(CASES['base']);c.update(m1=c['m1']+d,m5=c['m5']+d,mt=c['mt']+d)
 if min(c['m1'],c['m5'],c['mt'])<=0:continue
 scan.append([d,calc(c)['value_per_share']])
roots=[]
for x,z in zip(scan,scan[1:]):
 if (x[1]-f['price'])*(z[1]-f['price'])<=0:
  lo=x[0];hi=z[0]
  for _ in range(60):
   mid=(lo+hi)/2;c=dict(CASES['base']);c.update(m1=c['m1']+mid,m5=c['m5']+mid,mt=c['mt']+mid)
   if calc(c)['value_per_share']<f['price']:lo=mid
   else:hi=mid
  roots.append((lo+hi)/2)
out=dict(classification='Exploratory FCFF research only; not calibrated WACC or integral valuation',anchors=dict(revenue=REV,ebit=EBIT,da=38,depreciation=21.9,amortization=16.1,tax=TAX),cases=r,sensitivities=sens,reverse_margin_shift_roots=roots,reverse_scan_min=min(v for d,v in scan),reverse_scan_max=max(v for d,v in scan),owner_fcf=None,integral_equity_bridge=None)
(p/'model.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:round(v['value_per_share'],4) for k,v in r.items()},'bridge',BRIDGE,'reverse',roots)
