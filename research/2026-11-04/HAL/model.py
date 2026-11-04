"""HAL 10-year FCFF, USD millions, Nov 4 2026. Run with Python standard library.
All forecasts are analyst assumptions, not issuer guidance unless explicitly labeled.
No annual SBC add-back or assumed buybacks. No terminal multiple.
"""
from pathlib import Path
from copy import deepcopy
import json,csv,math
P=Path(__file__).parent
PRICE=34.07
SHARES_BASIC=827.126342
SHARES=SHARES_BASIC+1.0 # Q3 diluted minus basic weighted average; proxy not actual award inventory
REV0=22476.0
BRIDGE={'debt_principal_proxy':7222.0,'finance_leases_last_annual':183.0,'cash':-1843.0,'operating_cash_reserve':750.0,'international_pension_deficit_last_annual':200.0,'minority_economic_claim':120.0,'legacy_tax_cash_reserve_last_annual':155.0,'keystone_unquantified_incremental_net_value':0.0}
CLAIMS=sum(BRIDGE.values())
CASES={
'adverse':dict(growth=[-.05,-.04,.02,.03,.025,.02,.02,.02,.02,.02],margins=[.115,.105,.115,.125,.13,.13,.13,.13,.13,.13],tax=.25,wacc=.1175,g=.02,roic=.10,da_pct=.054,maint_da=1.05,sales_capital=1.75,wc_pct=.22,other_cash_pre_tax_pct=.0035,extra_wc=[250,100,0,0,0,0,0,0,0,0]),
'central':dict(growth=[.05,.045,.035,.03,.03,.025,.025,.025,.025,.025],margins=[.145,.15,.155,.155,.155,.154,.153,.152,.151,.15],tax=.23,wacc=.105,g=.025,roic=.14,da_pct=.0525,maint_da=1.0,sales_capital=2.5,wc_pct=.20,other_cash_pre_tax_pct=.0025,extra_wc=[100,0,0,0,0,0,0,0,0,0]),
'favorable':dict(growth=[.065,.07,.06,.05,.045,.04,.035,.03,.03,.03],margins=[.15,.16,.17,.175,.175,.174,.173,.172,.171,.17],tax=.21,wacc=.0925,g=.03,roic=.18,da_pct=.0525,maint_da=1.0,sales_capital=3.0,wc_pct=.18,other_cash_pre_tax_pct=.0015,extra_wc=[0,0,0,0,0,0,0,0,0,0])}

def irr(flows):
 lo,hi=-.5,1
 def pv(r):return sum(f/(1+r)**t for t,f in enumerate(flows))
 if pv(lo)*pv(hi)>0:return None
 for _ in range(180):
  mid=(lo+hi)/2
  if pv(mid)>0:lo=mid
  else:hi=mid
 return (lo+hi)/2

def run(a,claims=CLAIMS,shares=SHARES,price=PRICE):
 rows=[];rev=REV0
 for i in range(10):
  prior=rev;gr=a['growth'][i];rev*=1+gr;ebit=rev*a['margins'][i]
  leakage=rev*a['other_cash_pre_tax_pct'];nopat=(ebit-leakage)*(1-a['tax']);da=rev*a['da_pct']
  # Year1-5 financed organic growth: total marginal investment includes WC, never add both twice.
  # During contractions release trade WC only, not disposal of productive capital at book.
  dwc=(rev-prior)*a['wc_pct']+a['extra_wc'][i]
  growth_fixed=max(0,(rev-prior)*(1/a['sales_capital']-a['wc_pct']))
  capex=rev*a['capex_pct_override'] if a.get('capex_pct_override') is not None else da*a['maint_da']+growth_fixed
  organic_reinv=capex-da+dwc
  # From year6 through10 fade net reinvestment toward sustainable g/ROIC, eliminating terminal cliff.
  fade=max(0,(i-4)/5)
  target_reinv=nopat*max(gr,0)/a['roic']
  reinv=organic_reinv*(1-fade)+target_reinv*fade
  capex=da+reinv-dwc
  fcff=nopat-reinv;df=(1+a['wacc'])**(i+1)
  rows.append(dict(year=i+1,revenue=rev,growth=gr,ebit_margin=a['margins'][i],ebit=ebit,other_cash_pre_tax=leakage,tax_rate=a['tax'],nopat=nopat,da=da,capex_including_finance_asset_replacement=capex,delta_wc=dwc,reinvestment=reinv,fcff=fcff,pv_fcff=fcff/df,transition_weight=fade))
 t=rows[-1];terminal_nopat=t['nopat']*(1+a['g']);terminal_reinv=terminal_nopat*a['g']/a['roic'];terminal_fcff=terminal_nopat-terminal_reinv;tv=terminal_fcff/(a['wacc']-a['g']);pv_tv=tv/(1+a['wacc'])**10;ev=sum(x['pv_fcff'] for x in rows)+pv_tv;equity=ev-claims;value=equity/shares
 market_ev=price*shares+claims
 business_irr=irr([-market_ev]+[x['fcff'] for x in rows[:-1]]+[rows[-1]['fcff']+tv])
 # Equity return proxy at unchanged net claim and gross financing; not a price CAGR.
 # Average cash financing cost5.8% is an analyst assumption; distinct from marginal6.45% in WACC.
 interest=(7222+183)*.058*(1-a['tax']);nci=12
 equity_flows=[-price*shares]+[x['fcff']-interest-nci for x in rows[:-1]]+[rows[-1]['fcff']-interest-nci+tv-claims]
 return dict(assumptions=a,rows=rows,ev=ev,equity=equity,value=value,upside=value/price-1,pv_terminal_share=pv_tv/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,terminal_fcff=terminal_fcff,terminal_value=tv,pv_terminal=pv_tv,market_enterprise_claim_basis=market_ev,implied_business_annual_return=business_irr,implied_equity_annual_return_proxy=irr(equity_flows))

def solve(func,target,lo,hi):
 if (func(lo)-target)*(func(hi)-target)>0:return None
 for _ in range(120):
  mid=(lo+hi)/2
  if func(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2

def main():
 results={k:run(v) for k,v in CASES.items()}
 # Reverse joint conditions: flat explicit growth and first-year margin, fade to a common sustainable margin.
 def joint(gr,margin,wacc=.105,tax=.23,sc=2.5,roic=.14,g=.025):
  a=deepcopy(CASES['central']);a.update(growth=[gr]*5+[gr+(g-gr)*i/5 for i in range(1,6)],margins=[.145+(margin-.145)*min(i,3)/3 for i in range(10)],wacc=wacc,tax=tax,sales_capital=sc,roic=roic,g=g)
  return run(a)
 reverse=[]
 for m in [.14,.15,.16,.17,.18]:
  gr=solve(lambda q:joint(q,m)['value'],PRICE,-.02,.18)
  reverse.append({'sustainable_ebit_margin_after_sbc_and_routine_cost':m,'growth_years1_5_required':gr,'other_assumptions':'central except converged margin and first-five-year growth; growth fades to 2.5% by year10'})
 joint_grid=[{'growth_first5':gr,'margin':m,'value':joint(gr,m)['value']} for gr in [.02,.04,.06,.08] for m in [.14,.15,.16,.17]]
 sensitivities={}
 for w in [.0925,.10,.105,.11,.1175]:
  for g in [.015,.02,.025,.03]:
   a=deepcopy(CASES['central']);a.update(wacc=w,g=g);sensitivities[f'{w:.4f}/{g:.4f}']=run(a)['value']
 additional={}
 a=deepcopy(CASES['central']);a['growth']=[.05,.045,-.08,.07,.04,.03,.025,.025,.025,.025];a['margins']=[.145,.15,.115,.14,.15,.15,.15,.15,.15,.15];additional['one_downcycle']=run(a)
 additional['constructive_4pct_16margin']=joint(.04,.16,.10,.22,2.75,.16,.025)
 for label,change in [('cash_reserve_zero',-750),('cash_reserve_1250',500),('nopA_full_640_plus_assumed_interest_100_today',740),('finance_leases_zero_stress',-183),('finance_leases_250_stress',67),('minority_at_book',-77),('keystone_100m_net_destruction',100),('keystone_100m_net_creation',-100)]:additional[label]={'value':run(CASES['central'],CLAIMS+change)['value']}
 for rate in [.0025,.005,.01]:
  a=deepcopy(CASES['central']);a['margins']=[m+(.005-rate) for m in a['margins']];additional[f'routine_cost_reserve_{rate}']=run(a)
 for sc in [1.75,2,2.5,3]:
  a=deepcopy(CASES['central']);a['sales_capital']=sc;additional[f'incremental_sales_capital_{sc}']={'value':run(a)['value']}
 for margin in [.14,.15,.16,.17]:
  a=deepcopy(CASES['central']);a['margins']=[.145+(margin-.145)*min(i,3)/3 for i in range(10)];additional[f'fixed_margin_{margin}']={'value':run(a)['value']}
 for cp in [.049,.055,.065]:
  a=deepcopy(CASES['central']);a['capex_pct_override']=cp;additional[f'explicit_capex_pct_{cp}']=run(a)
 for sh in [SHARES_BASIC,SHARES+2,SHARES+5]:additional[f'shares_{sh}']={'value':run(CASES['central'],shares=sh)['value'],'favorable':run(CASES['favorable'],shares=sh)['value']}
 for cost in [100,250,500]:
  a=deepcopy(CASES['central']);a['extra_wc'][0]+=cost;additional[f'extra_wc_{cost}']={'value':run(a)['value']}
 out={'asof':'2026-11-04','financial_cutoff':'2026-09-30; filing 2026-10-23','price':PRICE,'price_date':'2026-11-03 regular close','base_revenue_ttm':REV0,'shares_basic':SHARES_BASIC,'economic_diluted_shares_proxy':SHARES,'bridge':BRIDGE,'net_claims':CLAIMS,'equity_irr_proxy_assumptions':{'average_cash_financing_cost':.058,'marginal_debt_cost_used_in_wacc':.0645,'average_cash_financing_cost_is_observed':False,'constant_claims_and_refinancing_proxy_not_expected_equity_return':True},'wacc_build':{'risk_free':.0495,'beta_assumption':1.4,'equity_risk_premium_assumption':.05,'cost_equity':.1195,'debt_yield_assumption':.0645,'tax_shield':.23,'target_debt_weight':.2,'computed_wacc':.8*.1195+.2*.0645*.77,'rounded_central_wacc':.105},'results':results,'reverse_margin_growth':reverse,'joint_sensitivity':joint_grid,'wacc_g_sensitivity':sensitivities,'additional_scenarios':additional}
 (P/'model_results.json').write_text(json.dumps(out,indent=2))
 for k,v in results.items():
  with (P/(k+'_10_year_fcff.csv')).open('w')as f:w=csv.DictWriter(f,fieldnames=list(v['rows'][0]));w.writeheader();w.writerows(v['rows'])
 print('claims',CLAIMS)
 for k,v in results.items():print(k,'value',v['value'],'ev',v['ev'],'Y1 FCFF',v['rows'][0]['fcff'],'Y1 capex',v['rows'][0]['capex_including_finance_asset_replacement'],'returns',v['implied_business_annual_return'],v['implied_equity_annual_return_proxy'])
 print('reverse',reverse);print('constructive',additional['constructive_4pct_16margin']['value'],'downcycle',additional['one_downcycle']['value'])
 return out
if __name__=='__main__':main()
