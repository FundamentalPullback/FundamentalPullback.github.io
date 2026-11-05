from pathlib import Path
import json,csv,copy,math
P=Path(__file__).parent
D=json.loads((P/'model/inputs.json').read_text());R=D['reported'];C=D['capital_estimates'];DI=D['discount_inputs'];M=D['metadata']
SH=R['shares_oct19']+R['dilutive_awards_q3'];equity=SH*M['price'];dw=R['nominal_debt_sep27_rounded']/(equity+R['nominal_debt_sep27_rounded']);beta=DI['observed_beta']*(1-DI['normalization_weight_to_one'])+DI['normalization_weight_to_one'];ke=DI['risk_free']+beta*DI['erp'];W=ke*(1-dw)+DI['cost_of_debt']*(1-DI['debt_tax_rate'])*dw

def schedule(case,ultra=False,growth_shift=0,margin_shift=0):
 x=case['ultra'] if ultra else case;revenue=x['revenue'] if ultra else R['revenue_2026_guidance_mid']-R['cas_2026_guidance'];out=[]
 for i in range(10):
  fade=0 if i<5 else (i-4)/5
  g=x['growth'][i] if i<5 else x['growth'][-1]+fade*(x['terminal_growth']-x['growth'][-1])
  g+=growth_shift*(1-fade)
  margin=(x['margin'][i] if i<5 else x['margin'][-1]+fade*(x['terminal_margin']-x['margin'][-1]))+margin_shift
  tax=case['tax'][i] if i<5 else case['tax'][-1]+fade*(.21-case['tax'][-1])
  previous=revenue;revenue*=1+g;ebit=revenue*margin;nopat=ebit*(1-tax)
  da=revenue*x['da_pct'];capex=revenue*x['capex_pct'];wc=(revenue-previous)*x['incremental_wc_pct']
  reinvest_initial=capex-da+wc
  reinvest_roic=nopat*g/x['terminal_roic']
  reinvest=reinvest_initial*(1-fade)+reinvest_roic*fade
  extra=0 if ultra else (case['additional_wc'][i] if i<5 else 0)
  integration=(x['integration_cash'][i] if i<5 else 0) if ultra else 0
  # Previously expensed program losses are separately paid here; forecast margins have no repeat addback of these provisions.
  reserve=(case['program_cash'][i] if i<5 else 0) if not ultra else 0
  ula=(case['ula_support'][i] if i<5 else 0) if not ultra else 0
  env=(R['environment_liability']-R['environment_recovery_asset']*C['environment_recoverability'])/5 if i<5 and not ultra else 0
  fcff=nopat-reinvest-extra-(reserve+integration+env)*(1-tax)-ula
  out.append(dict(year=2027+i,year_index=i+1,time=M['first_cashflow_time']+i,revenue=revenue,growth=g,core_ebit_margin=margin,ebit=ebit,cash_tax_rate=tax,nopat=nopat,da=da,capex_before_transition=capex,incremental_wc=wc,transition_weight=fade,reinvestment=reinvest,additional_wc=extra,prior_program_cash=reserve,ula_cash_support=ula,environment_cash=env,integration_cash=integration,fcff=fcff))
 return out

def valuation(name='base',wacc=None,growth_shift=0,margin_shift=0,cas_years=None,cash_shift=0,terminal_g=None,terminal_roic=None):
 case=copy.deepcopy(D['cases'][name]);wacc=(W if case['wacc']=='calculated' else case['wacc']) if wacc is None else wacc
 if terminal_g is not None:case['terminal_growth']=terminal_g
 if terminal_roic is not None:case['terminal_roic']=terminal_roic
 rows=schedule(case,False,growth_shift,margin_shift);ur=schedule(case,True)
 def pv(rows,x):
  end=rows[-1];nopat=end['revenue']*(1+x['terminal_growth'])*end['core_ebit_margin']*(1-.21);fcff=nopat*(1-x['terminal_growth']/x['terminal_roic']);terminal=fcff/(wacc-x['terminal_growth']);discounted=terminal/(1+wacc)**end['time'];explicit=sum(r['fcff']/(1+wacc)**r['time'] for r in rows)
  return dict(explicit_pv=explicit,terminal_nopat=nopat,terminal_fcff=fcff,terminal_value=terminal,terminal_pv=discounted,ev=explicit+discounted,terminal_share=discounted/(explicit+discounted))
 core=pv(rows,case);ultra=pv(ur,case['ultra']);n=case['cas_runoff_years'] if cas_years is None else cas_years
 # Frozen-plan contractual cost recoveries are finite. They are removed from core revenue/EBIT, so they are added only here.
 pension_recovery=[]
 for i in range(1,n+1):
  receipt=R['cas_2026_guidance']*max(0,1-i/n);tm=M['first_cashflow_time']+i-1;tax=case['tax'][min(i-1,4)] if i<=5 else .21
  pension_recovery.append(dict(year=2026+i,pretax_recovery=receipt,tax_rate=tax,pv=receipt*(1-tax)/(1+wacc)**tm))
 cas_pv=sum(x['pv'] for x in pension_recovery)
 pension=(R['pension_liability_sep27']*case['pension_claim_multiplier']+C['nonqualified_net_claim'])*(1-C['pension_tax_shield'])
 cash=R['cash_sep27']-R['ultra_purchase']+C['unreported_cash_change_after_sep27_ex_ultra']-C['minimum_operating_cash']-C['ultra_closing_adjustment']+cash_shift
 eq=core['ev']+ultra['ev']+cas_pv-pension-R['nominal_debt_sep27_rounded']+cash
 return dict(case=name,wacc=wacc,core=core,ultra=ultra,cas_recovery_pv=cas_pv,pension_claim_aftertax=pension,net_excess_cash_proforma=cash,nominal_debt=R['nominal_debt_sep27_rounded'],equity_value=eq,shares=SH,value_per_share=eq/SH,price=M['price'],upside=eq/SH/M['price']-1,margin_of_safety=1-M['price']/(eq/SH),core_forecast=rows,ultra_forecast=ur,pension_recovery_schedule=pension_recovery)

def solve(fn,target,lo,hi):
 a,b=fn(lo)-target,fn(hi)-target
 if a*b>0:return None
 for _ in range(100):
  mid=(lo+hi)/2;v=fn(mid)-target
  if a*v<=0:hi=mid;b=v
  else:lo=mid;a=v
 return (lo+hi)/2

if __name__=='__main__':
 out={n:valuation(n) for n in D['cases']}
 for n,v in out.items():
  for tag,key in [('core','core_forecast'),('ultra','ultra_forecast'),('pension','pension_recovery_schedule')]:
   rows=v[key]
   with (P/'model'/f'{n}_{tag}_forecast.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 rev=dict(wacc_at_current_price=solve(lambda w:valuation(wacc=w)['value_per_share'],M['price'],.04,.15),margin_shift_at_current_price=solve(lambda m:valuation(margin_shift=m)['value_per_share'],M['price'],-.05,.05),first5_growth_shift_at_current_price=solve(lambda g:valuation(growth_shift=g)['value_per_share'],M['price'],-.08,.12))
 sens=[]
 for w in [.052,.06,W,.065,.07,.075,.08,.09]:
  for g in [.015,.02,.025,.03]:sens.append({'wacc':w,'terminal_growth':g,'value':valuation(wacc=w,terminal_g=g)['value_per_share']})
 with(P/'model/sensitivity.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=sens[0]);w.writeheader();w.writerows(sens)
 checks=dict(combined_growth_minus_2pp_margin_minus_50bp=valuation(growth_shift=-.02,margin_shift=-.005)['value_per_share'],growth_minus_2pp=valuation(growth_shift=-.02)['value_per_share'],margin_minus_50bp=valuation(margin_shift=-.005)['value_per_share'],zero_cas_value=valuation(cas_years=0)['value_per_share'],eight_year_cas=valuation(cas_years=8)['value_per_share'],twenty_year_cas=valuation(cas_years=20)['value_per_share'],cash_minus_1500=valuation(cash_shift=-1500)['value_per_share'],cash_plus_1500=valuation(cash_shift=1500)['value_per_share'],terminal_roic_12=valuation(terminal_roic=.12)['value_per_share'],terminal_roic_20=valuation(terminal_roic=.20)['value_per_share'],market_debt_bridge_change_per_share=(R['nominal_debt_sep27_rounded']-R['debt_fair_value_sep27'])/SH)
 result=dict(metadata=M,discount_calibration=dict(beta_raw=DI['observed_beta'],beta_normalized=beta,cost_equity=ke,cost_debt=DI['cost_of_debt'],debt_weight=dw,wacc=W,normalization_is_analyst_estimate=True),cases=out,reverse=rev,sensitivity=sens,robustness=checks,source_labels='See source_ledger.json and assumptions.md',status='screen-grade',valuation_approved=False,entry_approved=False)
 (P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({'values':{n:v['value_per_share']for n,v in out.items()},'discount':result['discount_calibration'],'reverse':rev,'robustness':checks},indent=2))
