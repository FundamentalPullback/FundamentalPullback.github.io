"""HD FCFF valuation, as of 2026-11-07. USD millions except per share.
Run: python model.py. No third-party dependencies.
All historical values transcribed from primary reports identified in sources.json.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
hist={
 'FY2023':dict(sales=152669,ebit=21689,net=15143,da=3247,cfo=21172,capex=3226,sbc=380,interest=1943),
 'FY2024':dict(sales=159514,ebit=21526,net=14806,da=3761,cfo=19810,capex=3485,sbc=442,interest=2321),
 'FY2025':dict(sales=164683,ebit=20890,net=14156,da=4121,cfo=16325,capex=3679,sbc=522,interest=2412),
 'H1_2025':dict(sales=85133,ebit=11688,net=7984,da=1998,cfo=8968,capex=1723,sbc=288,interest=1190),
 'H1_2026':dict(sales=89626,ebit=11820,net=8055,da=2188,cfo=11422,capex=1724,sbc=326,interest=1194),
 'Q3_2025':dict(sales=41352,ebit=5353,net=3601,da=3042-1998,cfo=12978-8968,capex=2621-1723,sbc=408-288,interest=628),
 'Q4_2025':dict(sales=38198,ebit=3849,net=2571,da=4121-3042,cfo=16325-12978,capex=3679-2621,sbc=522-408,interest=594),
 'Q1_2026':dict(sales=41765,ebit=4981,net=3289,da=1081,cfo=6032,capex=844,sbc=178,interest=611),
 'Q2_2026':dict(sales=47861,ebit=6839,net=4766,da=1107,cfo=5390,capex=880,sbc=148,interest=583)}
hist['TTM']={k:hist['FY2025'][k]+hist['H1_2026'][k]-hist['H1_2025'][k] for k in hist['FY2025']}
for v in hist.values():v.update(fcf=v['cfo']-v['capex'],margin=v['ebit']/v['sales'])
PRICE=343.47
# Spot outstanding Aug18 + Q2 incremental dilution. No forecast repurchases.
SHARES=997.689626+2
DEBT=4248+4697+43951 # includes finance leases 303+2791
CASH=2085
OPERATING_CASH=2000 # assumption, bounded in sensitivity
EXCESS_CASH=max(0,CASH-OPERATING_CASH)
R0=hist['TTM']['sales']; EBIT0=hist['TTM']['ebit']-685
TAX=.243
SC={
 'adverso':dict(growth=[.005,.01,.02,.025,.025],margins=[.115,.115,.118,.12,.12],wacc=.095,g=.02,roic=.18,terminal_roic=.15,terminal_margin=.12),
 'central':dict(growth=[.03,.035,.04,.04,.035],margins=[.122,.125,.128,.13,.132],wacc=.085,g=.025,roic=.25,terminal_roic=.20,terminal_margin=.132),
 'favorable':dict(growth=[.045,.05,.055,.05,.045],margins=[.125,.13,.135,.14,.14],wacc=.075,g=.03,roic=.30,terminal_roic=.25,terminal_margin=.14)}
def dcf(s):
 rows=[];rev=R0
 for i in range(1,11):
  t=max(0,(i-5)/5)
  growth=s['growth'][i-1] if i<=5 else s['growth'][-1]*(1-t)+s['g']*t
  margin=s['margins'][i-1] if i<=5 else s['margins'][-1]*(1-t)+s['terminal_margin']*t
  roic=s['roic']*(1-t)+s['terminal_roic']*t
  old=rev;rev*=1+growth;nopat=rev*margin*(1-TAX)
  # Reinvestment intensity g/ROIC is imposed consistently in every year, then
  # allocated to net working capital and capital expenditure, not counted twice.
  reinvest=nopat*growth/roic;wc=(rev-old)*.08;da=rev*.025
  capex=da+reinvest-wc;fcff=nopat+da-capex-wc
  assert capex>0 and abs(fcff-(nopat-reinvest))<1e-6
  rows.append(dict(year=i,sales=rev,growth=growth,margin=margin,nopat=nopat,da=da,capex=capex,delta_wc=wc,reinvestment=reinvest,roic=roic,fcff=fcff,pv=fcff/(1+s['wacc'])**i))
 n11=rev*(1+s['g'])*s['terminal_margin']*(1-TAX);re11=n11*s['g']/s['terminal_roic'];f11=n11-re11
 tv=f11/(s['wacc']-s['g']);pvtv=tv/(1+s['wacc'])**10;ev=sum(r['pv'] for r in rows)+pvtv;eq=ev-DEBT+EXCESS_CASH
 return dict(assumptions=s,forecast=rows,terminal_sales=rev*(1+s['g']),terminal_da=rev*(1+s['g'])*.025,terminal_delta_wc=rev*s['g']*.08,terminal_capex=rev*(1+s['g'])*.025+re11-rev*s['g']*.08,terminal_nopat=n11,terminal_reinvestment=re11,terminal_fcff=f11,pv_terminal=pvtv,ev=ev,equity=eq,per_share=eq/SHARES,terminal_weight=pvtv/ev,mos=1-PRICE/(eq/SHARES))
def bisect(fn,target,lo,hi):
 if not fn(lo)<=target<=fn(hi):return None
 for _ in range(100):
  x=(lo+hi)/2
  if fn(x)<target:lo=x
  else:hi=x
 return (lo+hi)/2
base=SC['central']
def invgrowth(x):return dcf(dict(base,growth=[x]*5))['per_share']
def invmargin(x):return dcf(dict(base,margins=[x]*5,terminal_margin=x))['per_share']
res={k:dcf(v) for k,v in SC.items()}
sensitivity=[dict(wacc=w,g=g,value=dcf(dict(base,wacc=w,g=g))['per_share']) for w in [.075,.08,.085,.09,.095] for g in [.02,.025,.03]]
market_equity=PRICE*SHARES;rf=.0486;erp=.0441;beta=.95;kd=rf+.009
wacc=(rf+beta*erp)*market_equity/(market_equity+DEBT)+kd*(1-TAX)*DEBT/(market_equity+DEBT)
# CFO-based owner-cash reconciliation; not identical to forward normalized FCFF.
ttm=hist['TTM'];bridge={'reported_cfo':ttm['cfo'],'cash_capex':-ttm['capex'],'reported_fcf':ttm['fcf'],'economic_sbc':-ttm['sbc'],'net_interest_after_tax':(2416-141)*(1-TAX),'refund_after_tax':-685*(1-TAX),'fcff_cfo_proxy':ttm['fcf']-ttm['sbc']+(2416-141-685)*(1-TAX)}
out=dict(asof='2026-11-07',currency='USD millions',regular_close=dict(price=PRICE,date='2026-11-06',time='16:00 EST / 21:00 UTC',scanner_last=343.50),history=hist,normalized_ttm_ebit=EBIT0,normalized_ttm_margin=EBIT0/R0,bridge=dict(debt=DEBT,finance_leases_included=3094,operating_leases_not_deducted=9671,cash=CASH,operating_cash=OPERATING_CASH,excess_cash=EXCESS_CASH,shares=SHARES,minority=0,pension_debt=0),cfo_reconciliation=bridge,cost_of_capital=dict(rf=rf,erp=erp,beta=beta,cost_debt=kd,calculated_wacc=wacc,adopted_wacc=.085),scenarios=res,sensitivity=sensitivity,inverse=dict(five_year_flat_sales_growth=invgrowth and bisect(invgrowth,PRICE,-.01,.2),flat_operating_margin=bisect(invmargin,PRICE,.08,.25)),crosschecks=dict(market_pe_reported=market_equity/ttm['net'],market_ev_ebit_normalized=(market_equity+DEBT-EXCESS_CASH)/EBIT0,market_fcf_yield=ttm['fcf']/market_equity,reported_roic=.248),proxy_bounds=dict(cash_zero_to_all_per_share=CASH/SHARES,extra_500_debt_per_share=500/SHARES,extra_2shares_value=dcf(base)['equity']/SHARES-dcf(base)['equity']/(SHARES+2)),status='research_complete_conditional_audited')
# Audit: distinguish reported-period decline from a constant-week/perimeter comparison.
out['matched_history'] = dict(prior_ttm_ebit=21601, prior_ttm_net=14629,
 current_ttm_weeks=52,prior_ttm_weeks=53,constant_perimeter=False,
 reported_ttm_ebit_growth=ttm['ebit']/21601-1,
 refund_adjusted_ttm_ebit_growth=EBIT0/21601-1,
 h1_equal_26week_ebit_growth=(hist['H1_2026']['ebit']-685)/hist['H1_2025']['ebit']-1,
 note='TTM compares 52 against 53 weeks; H1 compares 26 against 26 weeks but neither is acquisition-neutral.')
out['cfo_reconciliation']['refund_inventory_cash_timing']=-45
out['cfo_reconciliation']['fcff_proxy_after_refund_inventory_timing']=bridge['fcff_cfo_proxy']-45
out['cfo_reconciliation']['limitations']='Normalized tax on 685 EBIT refund; 45 remaining cash refund is inventory timing; actual refund tax cash timing unavailable. Proxy is not sustainable FCFF.'
out['cost_of_capital'].update(rf_date='2026-11-06',erp_date='2026-11-01',beta_observed='2026-11-07',
 erp_source_posture='November snapshot directly read at query-bearing source URL; canonical URL has stale September snapshot.',
 convention='Raw Treasury plus unadjusted implied ERP, not default-adjusted ERP. Source monthly ERP uses 5.29% Treasury, model refreshes Treasury to November 6 ten-year 4.86%; not a same-date joint estimate.')
original_r0=R0
R0=original_r0*1.02
out['proxy_bounds']['base_sales_plus2pct_value']=dcf(base)['per_share']
R0=original_r0
out['proxy_bounds']['reinvesment_roic_20pct_value']=dcf(dict(base,roic=.20))['per_share']
out['proxy_bounds']['reinvesment_roic_30pct_value']=dcf(dict(base,roic=.30))['per_share']
# Additional economic capex 0.5% of sales each year and perpetuity.
capex_pv=sum(r['sales']*.005/(1+base['wacc'])**r['year'] for r in res['central']['forecast'])+res['central']['terminal_sales']*.005/(base['wacc']-base['g'])/(1+base['wacc'])**10
out['proxy_bounds']['capex_plus_minus_50bp_sales_per_share']=capex_pv/SHARES
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'history.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=['period']+list(hist['TTM']));wr.writeheader();wr.writerows(dict(period=k,**v) for k,v in hist.items())
for k,r in res.items():
 with (P/f'forecast_{k}.csv').open('w') as f:
  wr=csv.DictWriter(f,fieldnames=list(r['forecast'][0]));wr.writeheader();wr.writerows(r['forecast'])
print(json.dumps({'values':{k:v['per_share'] for k,v in res.items()},'inverse':out['inverse'],'wacc':wacc,'bridge':bridge,'ttm':ttm,'sensitivity':sensitivity},indent=2))
