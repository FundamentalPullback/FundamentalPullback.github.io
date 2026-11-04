"""FRPT transparent 10-year FCFF, release-based November 4 2026.
USD millions except share price. Deterministic research model, not trade instruction.
No source mutation; execute directly to write model_results and full year schedules.
"""
from pathlib import Path
import math,json,csv,copy
P=Path(__file__).parent
PRICE=69.60;REV0=1206.299;HOUSE0=15.5;BUY0=122.;NET_REALIZATION=REV0/(HOUSE0*BUY0)
DA_DEFINITION_BRIDGE=2.851/1206.299 # TTM total CFO D&A less issuer EBITDA-reconciliation D&A, as fraction of sales
CASH=345.860;CASH_RESERVE=30.;CONVERT_PRINCIPAL=402.5;FINANCE_LEASE_DEBT=28.539
COMMON=48.329;CONVERT_SHARES=402.5*14.3516/1000
ORDINARY_INCREMENT=54.742-48.426-CONVERT_SHARES
SHARES=COMMON+ORDINARY_INCREMENT
CAP=120.23;RF=.0491;VOL=.45;OPTION_YEARS=513/365.25
# Existing finance leases treated as debt; operating rents remain in forecast margins.
# Conversion lower call and matching purchased capped-call strike cancel economically; residual high-strike call valued below.
SCENARIOS={
 'adverse':dict(hh=[.005,.005,0,0,0,0,0,0,0,0],buy=[.03,.03,.025,.025,.025,.025,.025,.025,.025,.025],ebitda=[.185,.18,.18,.185,.19,.195,.20,.20,.20,.20],sbc=[.04]*10,da=[.08,.08,.08,.075,.075,.075,.075,.075,.075,.075],wacc=.115,g=.02,roic=.10,capacity0=1500,util=.82,capacity_per_capex=2.0,maintenance=[1.05]*10,capex_floor=[150,140,0,0,0,0,0,0,0,0],tax_shelter=25,price_growth=.015),
 'central':dict(hh=[.04,.035,.035,.03,.03,.025,.025,.02,.015,.01],buy=[.07,.06,.05,.045,.04,.035,.03,.03,.025,.025],ebitda=[.205,.22,.235,.245,.25,.25,.25,.25,.25,.25],sbc=[.03]*10,da=[.078,.075,.072,.069,.066,.064,.062,.06,.06,.06],wacc=.1025,g=.03,roic=.18,capacity0=1600,util=.85,capacity_per_capex=3.0,maintenance=[.85,.9,.95,1,1,1,1,1,1,1],capex_floor=[140,130,0,0,0,0,0,0,0,0],tax_shelter=35,price_growth=.02),
 'favorable':dict(hh=[.07,.07,.07,.06,.06,.05,.045,.04,.035,.03],buy=[.07,.06,.055,.055,.05,.045,.04,.035,.03,.03],ebitda=[.21,.23,.25,.265,.275,.28,.285,.285,.285,.285],sbc=[.025]*10,da=[.075,.072,.069,.065,.062,.06,.06,.06,.06,.06],wacc=.095,g=.035,roic=.22,capacity0=1650,util=.88,capacity_per_capex=3.5,maintenance=[.85,.9,.95,1,1,1,1,1,1,1],capex_floor=[140,140,0,0,0,0,0,0,0,0],tax_shelter=40,price_growth=.02),
}
def norm_cdf(z):return (1+math.erf(z/math.sqrt(2)))/2
def residual_option(s,vol=VOL,years=OPTION_YEARS):
 if s<=0:return 0.
 if years<=0:return CONVERT_SHARES*max(0,s-CAP)
 d1=(math.log(s/CAP)+(RF+.5*vol*vol)*years)/(vol*math.sqrt(years));d2=d1-vol*math.sqrt(years)
 return CONVERT_SHARES*(s*norm_cdf(d1)-CAP*math.exp(-RF*years)*norm_cdf(d2))
def bisect(fn,lo,hi):
 flo=fn(lo);fhi=fn(hi)
 if flo*fhi>0:return None
 for _ in range(150):
  mid=(lo+hi)/2;fm=fn(mid)
  if fm*flo<=0:hi=mid
  else:lo=mid;flo=fm
 return (lo+hi)/2

def equity_value(ev,shares=SHARES,cash=CASH,reserve=CASH_RESERVE,vol=VOL):
 before_option=ev+cash-reserve-CONVERT_PRINCIPAL-FINANCE_LEASE_DEBT
 if before_option<=0:return {'per_share':0.,'equity_before_residual_option':before_option,'residual_option':0.}
 v=bisect(lambda x:x*shares+residual_option(x,vol)-before_option,.000001,max(500,before_option/shares*1.2))
 return {'per_share':v,'equity_before_residual_option':before_option,'residual_option':residual_option(v,vol),'common_equity':v*shares}

def project(params):
 p=copy.deepcopy(params);rows=[];r=REV0;hh=HOUSE0;br=BUY0;cap=p['capacity0'];ppe=1141.357;shelter=p['tax_shelter'];wc0=.05*r
 for i in range(10):
  prev=r;hh*=1+p['hh'][i];br*=1+p['buy'][i];r=hh*br*NET_REALIZATION;growth=r/prev-1
  da=r*p['da'][i];sbc=r*p['sbc'][i];issuer_ebitda_proxy=r*p['ebitda'][i];da_bridge=r*DA_DEFINITION_BRIDGE;ebitda_pre_sbc=issuer_ebitda_proxy+da_bridge;ebit=ebitda_pre_sbc-sbc-da
  normtax=max(0,ebit*.25);benefit=min(shelter,normtax*.8);shelter-=benefit;cash_tax=normtax-benefit;nopat=ebit-cash_tax
  # Net cash tax benefit is bounded analytical reserve, not the full accounting DTA or disclosed current NOL principal.
  dwc=.05*(r-prev)
  cap_before=cap*(1+p['price_growth']);required=r/p['util'];gap=max(0,required-cap_before)
  maintenance=da*p['maintenance'][i];growthcap=gap/p['capacity_per_capex'];cashcap=max(p['capex_floor'][i],maintenance+growthcap)
  # Mature reinvestment normalization transitions in years 8–10, consistent with a finite terminal ROIC.
  transition=max(0,(i-6)/3);normal_nopat=ebit*.75
  capital_floor=da+max(0,normal_nopat*growth/p['roic']-dwc)
  cashcap=max(cashcap,(1-transition)*cashcap+transition*capital_floor)
  growthcap_actual=max(0,cashcap-maintenance);cap=cap_before+growthcap_actual*p['capacity_per_capex'];ppe+=cashcap-da
  fcff=nopat+da-cashcap-dwc
  rows.append(dict(year=i+1,households_m=hh,retail_buy_rate=br,net_revenue=r,revenue_growth=growth,issuer_adjusted_ebitda_proxy=issuer_ebitda_proxy,da_definition_bridge=da_bridge,economic_ebitda_before_sbc=ebitda_pre_sbc,sbc=sbc,da=da,ebit=ebit,ebit_margin=ebit/r,cash_tax=cash_tax,temporary_tax_benefit=benefit,nopat=nopat,maintenance_capex_estimate=maintenance,expansion_capacity_capex_estimate=growthcap_actual,capex_total=cashcap,change_operating_wc=dwc,fcff=fcff,effective_revenue_capacity=cap,utilization=r/cap,net_ppe=ppe,discount_factor=(1+p['wacc'])**(-(i+1)),pv_fcff=fcff/(1+p['wacc'])**(i+1)))
 last=rows[-1];terminal_rev=last['net_revenue']*(1+p['g']);terminal_ebit=terminal_rev*last['ebit_margin'];terminal_nopat=terminal_ebit*.75;terminal_reinvest=terminal_nopat*p['g']/p['roic'];terminal_fcff=terminal_nopat-terminal_reinvest;tv=terminal_fcff/(p['wacc']-p['g']);pv_tv=tv/(1+p['wacc'])**10;ev=sum(q['pv_fcff'] for q in rows)+pv_tv;eq=equity_value(ev)
 enterprise_price=PRICE*SHARES+residual_option(PRICE)+CONVERT_PRINCIPAL+FINANCE_LEASE_DEBT-(CASH-CASH_RESERVE)
 enterprise_irr=bisect(lambda rate:sum(q['fcff']/(1+rate)**q['year'] for q in rows)+tv/(1+rate)**10-enterprise_price,-.5,.6)
 # Shareholder cash-distribution proxy: current excess cash distributed at t0, remaining net borrowings held/refinanced; after-tax interest deducted, terminal debt repaid.
 debt=CONVERT_PRINCIPAL+FINANCE_LEASE_DEBT
 interest_rates=[.03,.04]+[.06]*8
 equity_cash=[q['fcff']-debt*interest_rates[i]*.75 for i,q in enumerate(rows)]
 # Conservative residual option payout at the end of year2 using its current modeled fair liability accrued at risk-free; no additional cash/share dilution beyond this liability.
 option_now=residual_option(PRICE);equity_cash[1]-=option_now*(1+RF)**2
 eq_initial=PRICE*SHARES-(CASH-CASH_RESERVE)
 eq_terminal=tv-debt
 equity_irr=bisect(lambda rate:sum(cf/(1+rate)**(i+1) for i,cf in enumerate(equity_cash))+eq_terminal/(1+rate)**10-eq_initial,-.5,.8)
 return dict(params=p,years=rows,terminal_revenue=terminal_rev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvest,terminal_fcff=terminal_fcff,terminal_ev=tv,pv_terminal=pv_tv,terminal_share=pv_tv/ev,enterprise_value=ev,**eq,upside=eq['per_share']/PRICE-1,revenue_cagr=(rows[-1]['net_revenue']/REV0)**.1-1,enterprise_price=enterprise_price,enterprise_fixed_exit_irr=enterprise_irr,equity_distribution_proxy_irr=equity_irr,equity_distribution_cashflows=equity_cash,equity_distribution_terminal=eq_terminal,equity_initial_net_outlay=eq_initial)

def build_all():
 out={'as_of':'2026-11-04 after Q3 release; pre-call','price':PRICE,'price_date':'2026-11-03 regular close','history_period_end':'2026-09-30','da_definition_bridge_ratio':DA_DEFINITION_BRIDGE,'forecast_periods':'NTM1 to NTM10, rolling annual model from September 2026 TTM; not calendar FY2027-2036','claim_inputs':dict(cash=CASH,minimum_operating_cash=CASH_RESERVE,convertible_principal=CONVERT_PRINCIPAL,finance_lease_debt=FINANCE_LEASE_DEBT,common_shares=COMMON,ordinary_increment_proxy=ORDINARY_INCREMENT,shares=SHARES,convert_shares=CONVERT_SHARES,cap=CAP,residual_option_market_price=residual_option(PRICE),option_years=OPTION_YEARS,option_volatility_assumed=VOL),'scenarios':{k:project(v) for k,v in SCENARIOS.items()}}
 # Joint sensitivity: revenue household/buy growth levels, profitability, WACC simultaneously; no unconditional pass threshold.
 joint=[]
 for growth_shift in [-.02,0,.02,.04]:
  for margin_shift in [-.02,0,.02,.04]:
   p=copy.deepcopy(SCENARIOS['central']);p['hh']=[max(0,x+growth_shift/2) for x in p['hh']];p['buy']=[max(0,x+growth_shift/2) for x in p['buy']];p['ebitda']=[x+margin_shift*i/9 for i,x in enumerate(p['ebitda'])]
   z=project(p);joint.append(dict(annual_growth_component_shift=growth_shift,ebitda_margin_shift=margin_shift,price=z['per_share'],cagr=z['revenue_cagr'],year10_margin=z['years'][-1]['ebit_margin']))
 out['joint_growth_margin_sensitivity']=joint
 out['discount_terminal_sensitivity']=[]
 for w in [.09,.095,.1025,.11,.115]:
  for g in [.02,.025,.03,.035]:
   p=copy.deepcopy(SCENARIOS['central']);p.update(wacc=w,g=g);z=project(p);out['discount_terminal_sensitivity'].append(dict(wacc=w,terminal_growth=g,value=z['per_share']))
 # Reverse using same capacity, tax, claim and reinvestment mechanics; growth is shifted in both household and spend drivers.
 rev=[]
 for margin_shift in [0,.02,.04]:
  for w in [.095,.1025,.115]:
   def f(shift):
    p=copy.deepcopy(SCENARIOS['central']);p['hh']=[x+shift/2 for x in p['hh']];p['buy']=[x+shift/2 for x in p['buy']];p['ebitda']=[x+margin_shift*i/9 for i,x in enumerate(p['ebitda'])];p['wacc']=w;return project(p)
   shift=bisect(lambda x:f(x)['per_share']-PRICE,-.015,.25)
   if shift is not None:
    z=f(shift);rev.append(dict(wacc=w,ebitda_margin_shift=margin_shift,driver_shift=shift,cagr=z['revenue_cagr'],year10_revenue=z['years'][-1]['net_revenue'],year10_households=z['years'][-1]['households_m'],year10_buy_rate=z['years'][-1]['retail_buy_rate'],year10_ebit_margin=z['years'][-1]['ebit_margin'],value=z['per_share']))
 out['reverse_joint']=rev
 out['claim_sensitivity']=[]
 central_ev=out['scenarios']['central']['enterprise_value']
 for vol in [.30,.45,.60]:
  for sd in [-.30,0,.30]:
   z=equity_value(central_ev,shares=SHARES+sd,vol=vol)
   out['claim_sensitivity'].append(dict(option_volatility=vol,ordinary_share_change_m=sd,value=z['per_share']))
 out['operating_sensitivities']=[]
 for key, changes in [('lower_capacity_productivity',dict(capacity_per_capex=2.0)),('higher_capacity_productivity',dict(capacity_per_capex=4.0)),('no_tax_shelter',dict(tax_shelter=0)),('no_maintenance_holiday',dict(maintenance=[1.0]*10))]:
  p=copy.deepcopy(SCENARIOS['central']);p.update(changes);z=project(p);out['operating_sensitivities'].append(dict(case=key,value=z['per_share']))
 alt=copy.deepcopy(SCENARIOS['central']);alt['hh']=[x+.015 for x in alt['hh']];alt['buy']=[x+.015 for x in alt['buy']];alt['ebitda']=[x+.02*i/9 for i,x in enumerate(alt['ebitda'])];alt.update(wacc=.095,roic=.20)
 out['plausible_joint_alternative']=project(alt)
 alt_std=copy.deepcopy(alt);alt_std.update(wacc=.1025,roic=.18);out['alternative_at_central_capital_cost']=project(alt_std)
 out['central_price_return_grid']=[]
 for price in [40,45,50,55,60,65,69.6,75]:
  enterprise_price=price*SHARES+residual_option(price)+CONVERT_PRINCIPAL+FINANCE_LEASE_DEBT-(CASH-CASH_RESERVE)
  z=out['scenarios']['central'];ir=bisect(lambda rate:sum(q['fcff']/(1+rate)**q['year'] for q in z['years'])+z['terminal_ev']/(1+rate)**10-enterprise_price,-.5,.6)
  out['central_price_return_grid'].append(dict(price=price,enterprise_fixed_exit_irr=ir))
 (P/'model_results.json').write_text(json.dumps(out,indent=2))
 for k,z in out['scenarios'].items():
  with (P/(k+'_10_year_fcff.csv')).open('w') as f:
   wr=csv.DictWriter(f,fieldnames=list(z['years'][0]));wr.writeheader();wr.writerows(z['years'])
 return out
if __name__=='__main__':
 o=build_all()
 for k,z in o['scenarios'].items():print(k,{x:(round(z[x],4) if z[x] is not None else None) for x in ['per_share','upside','revenue_cagr','terminal_share','enterprise_fixed_exit_irr','equity_distribution_proxy_irr']},'year10',z['years'][-1]['net_revenue'],z['years'][-1]['ebit_margin'])
 print('Reverse',o['reverse_joint'])
