from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text())
scenarios={'bear':dict(growth=.015,margin5=.085,margin10=.08,wacc=.125,g=.015,roic=.12,tax=.24),'base':dict(growth=.06,margin5=.115,margin10=.105,wacc=.105,g=.02,roic=.15,tax=.22),'bull':dict(growth=.09,margin5=.135,margin10=.12,wacc=.09,g=.025,roic=.20,tax=.20)}
bridge=f['cash']-f['revolver_debt']-f['finance_leases']-f['utb_historical']-f['interest_penalty_historical']-f['operating_cash_reserve']-f['postquarter_buybacks']-f['lease_guarantee_stress']
def calc(s,capex_delta=0.,margin_delta=0.,cash_delta=0.,tax_override=None):
 tax=s['tax'] if tax_override is None else tax_override;prevrev=f['revenue_ttm'];prevmargin=f['ebit_anchor']/prevrev;prevnopat=f['ebit_anchor']*(1-tax);rows=[]
 for y in range(1,11):
  growth=s['growth'] if y<=5 else s['growth']+(s['g']-s['growth'])*(y-5)/5
  margin=(prevmargin+(s['margin5']-prevmargin)*y/5 if y<=5 else s['margin5']+(s['margin10']-s['margin5'])*(y-5)/5)+margin_delta
  rev=prevrev*(1+growth);ebit=rev*margin;nopat=ebit*(1-tax);da=rev*.037;capex=rev*(.045+capex_delta);finnew=rev*.005;dnwc=(rev-prevrev)*.01;physical=capex+finnew-da+dnwc;economic=max(0,nopat-prevnopat)/s['roic'];investment=max(physical,economic);reserve=investment-physical;fcff=nopat-investment
  rows.append(dict(year=y,revenue=rev,growth=growth,margin=margin,ebit=ebit,tax=tax,nopat=nopat,da=da,capex=capex,new_finance_lease_assets=finnew,delta_nwc=dnwc,physical_reinvestment=physical,economic_reinvestment=economic,additional_reinvestment_reserve=reserve,fcff=fcff,pv=fcff/(1+s['wacc'])**y));prevrev=rev;prevnopat=nopat
 rev=prevrev*(1+s['g']);nopat=rev*(s['margin10']+margin_delta)*(1-tax);physical=rev*(.045+capex_delta+.005-.037)+(rev-prevrev)*.01;economic=max(0,nopat-prevnopat)/s['roic'];investment=max(physical,economic);fcff=nopat-investment;tv=fcff/(s['wacc']-s['g']);pvt=tv/(1+s['wacc'])**10;ev=sum(r['pv'] for r in rows)+pvt;equity=ev+bridge+cash_delta
 return dict(assumptions=s,rows=rows,terminal=dict(revenue=rev,nopat=nopat,physical_reinvestment=physical,economic_reinvestment=economic,reinvestment=investment,fcff=fcff,value=tv,pv=pvt),ev=ev,equity=equity,bridge=bridge+cash_delta,value_per_share=equity/f['shares_diluted_q1'],terminal_weight=pvt/ev)
r={k:calc(v) for k,v in scenarios.items()};sens={}
for name,args in [('capex_plus_1pp',{'capex_delta':.01}),('margin_minus_1pp',{'margin_delta':-.01}),('margin_plus_1pp',{'margin_delta':.01}),('tax_26pct',{'tax_override':.26}),('no_postquarter_buyback_reserve',{'cash_delta':65.}),('no_lease_guarantee_stress',{'cash_delta':6.7})]:sens[name]=calc(scenarios['base'],**args)['value_per_share']
# Monotonic margin-shift reverse; not a predicted margin or price target.
lo,hi=-.05,.20
assert calc(scenarios['base'],margin_delta=lo)['value_per_share']<=f['price']<=calc(scenarios['base'],margin_delta=hi)['value_per_share']
sweep=[{'shift':-.05+i*.0025,'value':calc(scenarios['base'],margin_delta=-.05+i*.0025)['value_per_share']} for i in range(101)]
assert all(b['value']>=a['value']-1e-8 for a,b in zip(sweep,sweep[1:]))
for _ in range(100):
 mid=(lo+hi)/2
 if calc(scenarios['base'],margin_delta=mid)['value_per_share']<f['price']:lo=mid
 else:hi=mid
out=dict(status='Exploratory FCFF conditional on uncalibrated discount rates, capital proxies and calendar; independent audit completed for conditional exploratory scope',cases=r,sensitivities=sens,reverse_margin_shift=(lo+hi)/2,reverse_first_year_fcff=calc(scenarios['base'],margin_delta=(lo+hi)/2)['rows'][0]['fcff'],reverse_sweep=sweep,reverse_funding_assured=False,reverse_value=calc(scenarios['base'],margin_delta=(lo+hi)/2)['value_per_share'],approved_entry=False,latestCompleted=False)
(p/'model.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:round(v['value_per_share'],4) for k,v in r.items()},'bridge',bridge,'sens',sens)
