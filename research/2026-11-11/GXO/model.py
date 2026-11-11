"""Conditional GXO pre-event capital tests, NOT a cleared valuation. USD millions.
Run python model.py; all scenario inputs are analyst assumptions, not guidance.
FCFF deducts full economic asset investment, including finance-lease additions.
Financing-only cash schedule restores new lease funding and repays principal once.
"""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
BASE_REV=13836.; SHARES=114.636
DEBT=2839.; FINLEASE=487.; CASH=340.; DERIVATIVE=103.; OVERDRAFT=2.
CASES={
 'bear':dict(growth=.02,m1=.026,m5=.028,m10=.028,capex=.042,tax=.28,wacc=.11,g=.02,roic=.10,cash_floor=.02,nci=70,kd=.075),
 'base':dict(growth=.045,m1=.031,m5=.040,m10=.042,capex=.039,tax=.26,wacc=.095,g=.025,roic=.12,cash_floor=.015,nci=60,kd=.065),
 'bull':dict(growth=.065,m1=.033,m5=.050,m10=.055,capex=.038,tax=.25,wacc=.09,g=.03,roic=.15,cash_floor=.01,nci=50,kd=.06)}

def run(s):
 rev=BASE_REV; cash=CASH; lease=FINLEASE; debt=DEBT-FINLEASE; rows=[]; maxdraw=0
 for i in range(1,11):
  transition=max(0,(i-5)/5)
  growth=s['growth']+(s['g']-s['growth'])*transition
  newrev=rev*(1+growth)
  margin=s['m1']+(s['m5']-s['m1'])*(i-1)/4 if i<=5 else s['m5']+(s['m10']-s['m5'])*transition
  ebit=newrev*margin; nopat=ebit*(1-s['tax']); da=newrev*.034
  nwc=(newrev-rev)*.08
  terminal_style_investment=da+nopat*growth/s['roic']-nwc
  investment=newrev*s['capex'] if i<=5 else newrev*s['capex']*(1-transition)+terminal_style_investment*transition
  cashcap=min(investment,newrev*.025); leaseadd=investment-cashcap
  fcff=nopat+da-investment-nwc
  # Cash financing diagnostic only, no changes to FCFF valuation.
  interest=(debt+lease)*s['kd']; leaseprincipal=min(lease,82. if i==1 else lease/6)
  maturity={1:284.,3:600.,5:967.,8:500.}.get(i,0.)
  # Scheduled old debt maturities cannot exceed remaining balance after prior cash sweeps.
  maturity=min(maturity,debt)
  cf_after_interest=fcff-interest*(1-s['tax'])
  cash_before=cash+cf_after_interest+leaseadd-leaseprincipal-maturity-5
  floor=newrev*s['cash_floor']; draw=max(0,floor-cash_before)
  # No shareholder payout; surplus retires other debt, then accumulates.
  remaining_debt=debt-maturity+draw
  sweep=min(max(0,cash_before+draw-floor),remaining_debt)
  cash=cash_before+draw-sweep; debt=remaining_debt-sweep
  lease=lease+leaseadd-leaseprincipal; maxdraw=max(maxdraw,draw)
  rows.append(dict(year=i,period_end=f'{2026+i}-09-30',stage='explicit' if i<=5 else 'transition',revenue=newrev,growth=growth,ebit_margin=margin,ebit=ebit,nopat=nopat,da=da,change_nwc=nwc,cash_capex=cashcap,finance_lease_additions=leaseadd,economic_investment=investment,fcff=fcff,pv=fcff/(1+s['wacc'])**i,interest=interest,lease_principal=leaseprincipal,scheduled_old_debt_maturity=maturity,required_refinancing=draw,discretionary_debt_paydown=sweep,cash=cash,finance_lease_debt=lease,other_debt=debt))
  rev=newrev
 tnopat=rev*(1+s['g'])*s['m10']*(1-s['tax'])
 reinv=tnopat*s['g']/s['roic']; tfcff=tnopat-reinv
 tv=tfcff/(s['wacc']-s['g']); pvtv=tv/(1+s['wacc'])**10
 ev=sum(x['pv'] for x in rows)+pvtv
 excess=max(0,CASH-BASE_REV*s['cash_floor'])
 claims=DEBT+DERIVATIVE+OVERDRAFT+s['nci']-excess
 return dict(inputs=s,rows=rows,terminal_nopat=tnopat,terminal_net_reinvestment=reinv,terminal_fcff=tfcff,ev=ev,equity=ev-claims,unfloored_equity_residual_per_share=(ev-claims)/SHARES,conditional_per_share=max(0,ev-claims)/SHARES,terminal_pv_share=pvtv/ev,claims=claims,excess_cash=excess,max_annual_refinancing=maxdraw,funding_status='conditional: refinancing and renewed facilities not committed; annual schedule cannot prove seasonal liquidity')

def main():
 results={k:run(v) for k,v in CASES.items()}
 # Reverse solves year5 and year10 margins jointly; fixes first year and all other base assumptions.
 lo,hi=.01,.15
 for _ in range(100):
  mid=(lo+hi)/2; c=copy.copy(CASES['base']);c['m10']=mid;c['m5']=mid-.002
  if run(c)['conditional_per_share']<55.32:lo=mid
  else:hi=mid
 reverse=dict(reference_price=55.32,price_status='Nov10 scanner and multiple secondary close observations; conflicting source55.31, not canonical',required_year10_margin=mid,required_year5_margin=mid-.002,holding='base growth, investment, tax, WACC, terminal ROIC, initial margin and claims fixed; Sep30 anchor, no Nov10 stub')
 sensitivities=[]
 for w in [.085,.095,.105,.115]:
  for g in [.015,.025,.035]:
   s=copy.copy(CASES['base']);s.update(wacc=w,g=g)
   sensitivities.append(dict(wacc=w,g=g,conditional_per_share=run(s)['conditional_per_share']))
 out=dict(as_of='2026-11-11',valuation_anchor='2026-09-30',canonical_fair_value=None,canonical_entry=None,decision_ready=False,scenario_status='illustrative economic stress tests pending independent audit; not probability-weighted',scenarios=results,reverse=reverse,sensitivity=sensitivities)
 (P/'results.json').write_text(json.dumps(out,indent=2))
 for k,v in results.items():
  with open(P/f'forecast_{k}.csv','w') as f:
   wr=csv.DictWriter(f,fieldnames=v['rows'][0]);wr.writeheader();wr.writerows(v['rows'])
  print(k,round(v['conditional_per_share'],2),'TV%',round(v['terminal_pv_share']*100,1),'maxrefinancing',round(v['max_annual_refinancing'],1))
 print('reverse',reverse)
 assert sum([3507,3298,3441,3590])==13836
 for k,v in results.items():
  assert len(v['rows'])==10 and v['terminal_net_reinvestment']>0
  for x in v['rows']:
   assert abs(x['cash_capex']+x['finance_lease_additions']-x['economic_investment'])<1e-8
   assert abs(x['fcff']-(x['nopat']+x['da']-x['economic_investment']-x['change_nwc']))<1e-8
   assert x['finance_lease_debt']>=0 and x['other_debt']>=0
if __name__=='__main__':main()
