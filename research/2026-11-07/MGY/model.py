"""Conditional finite reserve-bucket cash model, not current whole-equity NAV."""
import json,csv,pathlib
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());a=[x for x in csv.DictReader((p/'daily_closes.csv').open()) if x['date']<='2026-11-06'];v=list(csv.DictReader((p/'volume_screen_input.csv').open()))
def ema(n):
 z=float(a[0]['close'])
 for x in a[1:]:z+=(float(x['close'])-z)*2/(n+1)
 return z
screen={'date':'2026-11-06','close':23.67,'shares_m_date':'2026-11-02','shares_m':266.311001,'market_cap_m':23.67*266.311001,'ema20':ema(20),'ema50':ema(50),'pullback_252_high_pct':100*(1-23.67/max(float(x['high']) for x in a[-252:])),'volume20':sum(float(x['volume']) for x in v)/len(v),'ttm_op_margin':h['TTM2026']['ebit']/h['TTM2026']['revenue'],'ttm_parent_net_margin':h['TTM2026']['net_parent']/h['TTM2026']['revenue']}
# Annual production base: issuer combined Q2 adjusted base. Non-oil split is an explicit Q3 proxy.
oil0=78*.365;total0=158*.365;gasfrac=(19425/6)/(19425/6+3037);gas0=(total0-oil0)*gasfrac*6;ngl0=(total0-oil0)*(1-gasfrac)
# Historical buckets only, minus an illustrative full-year combined 2026 production allowance.
budget={'oil':79.8+196.4548-oil0,'gas':404.1+205.4224-gas0,'ngl':63+40.5368-ngl0}
collars=[(2.7,70.83,88.68),(2.275,70,82.31),(.920,70,80.08)]
swaps=[(2.066605,63.46),(1.982790,65.02),(.893666,67.37),(.866955,66.34)]
def hedge(wti):return sum(q*(max(f-wti,0)-max(wti-c,0)) for q,f,c in collars)+sum(q*(k-wti) for q,k in swaps)
rows=[];out={}
for name,wti,gasprice,nglprice,late,beta in [('stress',55,2,15,-.10,1.5),('central',70,3,20,-.07,1.25),('upside',85,4,25,-.04,1.0)]:
 remaining=budget.copy();qty={'oil':oil0,'gas':gas0,'ngl':ngl0};pv=0;ke=.0486+beta*.0441;wacc=.77*ke+.23*.06625*(1-.21);grosscap=0
 for t in range(1,11):
  growth=.045 if t==1 else .045*(5-t)/4 if t<=5 else late*(t-5)/5
  for k in qty:qty[k]=min(qty[k]*(1+growth),remaining[k]);remaining[k]-=qty[k]
  q=qty['oil']+qty['gas']/6+qty['ngl'];infl=1.02**(t-1)
  rev=qty['oil']*(wti-2)+qty['gas']*gasprice+qty['ngl']*nglprice
  hed=hedge(wti) if t==1 else 0 # only disclosed existing contracts, not forecasting a hedge program
  cashcost=(q*(6+1.95+.60)+45)*infl # fixed corporate cost retained; SBC economic allowance .60/boe
  productiontax=.06*rev
  # All drilling + a separately identified extra-physical budget; scalable only with funded production.
  cap=925*(q/(total0*1.045))*infl;othercap=25*infl;grosscap+=cap+othercap
  # Use ordinary normalized tax from year one; Q4 low cash tax is not perpetuated.
  tax=max(0,(rev+hed-cashcost-productiontax-q*14.5)*.21)
  cf=rev+hed-cashcost-productiontax-tax-cap-othercap
  pv+=cf/(1+wacc)**t
  rows.append({'case':name,'year':2026+t,'growth_assumption':growth,'oil_mmbbl':qty['oil'],'gas_bcf':qty['gas'],'ngl_mmbbl':qty['ngl'],'production_mmboe':q,'revenue':rev,'existing_hedge_settlement':hed,'cash_cost_including_sbc':cashcost,'productiontax':productiontax,'normalized_income_tax':tax,'funded_dc_capex':cap,'additional_capital_allowance':othercap,'conditional_cash':cf,'wacc':wacc,'pv_cash':cf/(1+wacc)**t})
 out[name]={'pv_finite_cash_bucket':pv,'remaining_historical_budget':remaining,'ke_assumed':ke,'wacc_assumed':wacc,'funded_capital_total':grosscap,'whole_equity_value':None,'unmodeled_resources_and_tail':None}
# One-year funding inverse includes actual 2027 hedge curve and conservative normalized tax, before interest/closure.
def yearone(wti, hedged=True):
 q=total0*1.045;rev=oil0*1.045*(wti-2)+gas0*1.045*3+ngl0*1.045*20;cost=q*(6+1.95+.60)+45;tax=max(0,(rev+(hedge(wti) if hedged else 0)-cost-.06*rev-q*14.5)*.21);return rev+(hedge(wti) if hedged else 0)-cost-.06*rev-tax-925-25
lo,hi=0,200
for _ in range(100):
 m=(lo+hi)/2
 if yearone(m)>0:hi=m
 else:lo=m
lo_un,hi_un=0,200
for _ in range(100):
 m=(lo_un+hi_un)/2
 if yearone(m,False)>0:hi_un=m
 else:lo_un=m
r={'unhedged_funding_inverse_before_interest_and_closure':(lo_un+hi_un)/2,'scope':'partial finite historical reserve bucket, not current engineering NAV','screen':screen,'historical_budget_after_assumed_2026_production':budget,'scenarios':out,'funding_inverse_WTI_before_interest_and_closure':(lo+hi)/2,'MEH_equals_WTI_assumption':True,'current_nci':0,'nci_zero_source':'February 2026 cancellation/exchange, September 10-Q Note 12','unknown_legal_claims':None,'terminal_value':None,'approved_value':None,'approved_entry':None}
(p/'model_results.json').write_text(json.dumps(r,indent=2));(p/'screen.json').write_text(json.dumps(screen,indent=2))
with (p/'finite_cash_scenarios.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(r,indent=2))
