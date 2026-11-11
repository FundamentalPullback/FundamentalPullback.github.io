"""CHDN conditional decision model. USDm. No approved target/entry.
Consolidated FCFF excludes equity-method earnings; affiliates valued as equity cash,
not consolidated EBITDA or book investment. No second affiliate-debt deduction.
"""
import json,copy
from pathlib import Path
P=Path(__file__).parent
A=json.loads((P/'actuals.json').read_text())['TTM2026']
price=101.96; shares=68.548342
rf=.0498; erp=.0441; beta_observed=.77; beta_normalized=1.; kd=.065; tax=.26
E=price*shares; debt=4748
ke=rf+beta_normalized*erp
wacc=ke*E/(E+debt)+kd*(1-tax)*debt/(E+debt)
bridge=dict(debt=debt,excess_cash=0,minority=24,finance_lease_proxy=27.8,liability_awards=14,shares=shares)
base=dict(growth=.04,margin=.26,g=.025,roic=.10,wacc=wacc,ke=ke+.02,jv_growth=.025,jv_cash=130.3*.9,jv_parent_tax=149*.26,project_caps=[350,320],bridge=bridge)
def run(c):
 rev=A['revenue']; prior=A['ebit']*(1-tax); m0=A['ebit']/rev
 pv=jp=0; dist=c['jv_cash']; rows=[]
 for y in range(1,11):
  growth=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  oldrev=rev;rev*=1+growth; margin=m0+(c['margin']-m0)*min(y,5)/5
  nopat=rev*margin*(1-tax); da=rev*.078; wc=(rev-oldrev)*.02
  growth_inv=max(0,(prior*growth if c.get('growth_only_capital') else nopat-prior))/c['roic']; capex=da+growth_inv-wc
  if y<=len(c['project_caps']):capex=max(capex,c['project_caps'][y-1])
  fcff=nopat+da-capex-wc;pv+=fcff/(1+c['wacc'])**y
  jg=c['jv_growth'] if y<=5 else c['jv_growth']+(c['g']-c['jv_growth'])*(y-5)/5
  dist*=1+jg; parent_tax=c['jv_parent_tax']*(dist/c['jv_cash']) if c['jv_cash'] else 0; net_dist=dist-parent_tax; jp+=net_dist/(1+c['ke'])**y
  rows.append(dict(year=y,revenue=rev,margin=margin,nopat=nopat,da=da,capex=capex,delta_wc=wc,fcff=fcff,jv_distribution=dist,parent_affiliate_tax=parent_tax,net_affiliate_cash=net_dist));prior=nopat
 tv=nopat*(1+c['g'])*(1-c['g']/c['roic'])/(c['wacc']-c['g'])/(1+c['wacc'])**10
 jtv=net_dist*(1+c['g'])/(c['ke']-c['g'])/(1+c['ke'])**10
 b=c['bridge'];operating=pv+tv;jv=jp+jtv
 eq=operating+jv+b['excess_cash']-b['debt']-b['minority']-b['finance_lease_proxy']-b['liability_awards']
 return dict(per_share=max(0,eq/b['shares']),equity=eq,operating_ev=operating,jv_equity=jv,operating_terminal_share=tv/operating,rows=rows)
cases={'central_normalized':base,'efficiency_growth_only':dict(base,growth_only_capital=True),'recovery_efficiency':dict(base,growth=.065,margin=.28,g=.025,roic=.12,jv_growth=.035,jv_cash=130.3,growth_only_capital=True),'hurdle_9':dict(base,wacc=.09),'adverse':dict(base,growth=.01,margin=.23,g=.015,roic=.08,wacc=.10,ke=.13,jv_cash=130.3*.8,jv_growth=0),'recovery':dict(base,growth=.065,margin=.28,g=.025,roic=.12,jv_growth=.035,jv_cash=130.3),'generous_affiliate_earnings_payout':dict(base,jv_cash=149,jv_parent_tax=0,bridge=dict(bridge,excess_cash=167,liability_awards=0))}
sens={}
sens['zero_incremental_parent_tax']=run(dict(base,jv_parent_tax=0))['per_share']
sens['tax_distributions_instead_of_earnings']=run(dict(base,jv_parent_tax=130.3*.9*.26))['per_share']
for k,v in [('kd_6',.06),('kd_7',.07),('kd_8',.08)]:sens[k]=run(dict(base,wacc=ke*E/(E+debt)+v*(1-tax)*debt/(E+debt)))['per_share']
for r in [.12,.15,.20]:sens['central_roic_'+str(r)]=run(dict(base,roic=r,growth_only_capital=True))['per_share']
for cap in [100,200,300]:sens['extra_project_year1_'+str(cap)]=run(dict(base,project_caps=[350+cap,320]))['per_share']
for j in [100,130.3,149,175]:sens['jv_cash_'+str(j)]=run(dict(base,jv_cash=j))['per_share']
inverse={}
for w in [wacc,.09,.10]:
 lo,hi=.1,.6
 if run(dict(base,wacc=w,margin=hi))['per_share']<price:
  inverse[str(w)]=None; continue
 for _ in range(100):
  mid=(lo+hi)/2
  if run(dict(base,wacc=w,margin=mid))['per_share']<price:lo=mid
  else:hi=mid
 inverse[str(w)]=(lo+hi)/2
out=dict(as_of='2026-11-11',ticker='CHDN',price={'regular_close':price,'date':'2026-11-10','time':'16:00 EST','afterhours_excluded':102.5},inputs=dict(rf=rf,erp=erp,beta_observed=beta_observed,beta_normalized_assumption=beta_normalized,kd_assumption=kd,ke=ke,wacc=wacc,bridge=bridge),cases={k:dict(assumptions=v,result=run(v)) for k,v in cases.items()},sensitivity=sens,inverse_year5_margin=inverse)
(P/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'wacc':wacc,'cases':{k:v['result']['per_share'] for k,v in out['cases'].items()},'sens':sens,'inverse':inverse},indent=2))
