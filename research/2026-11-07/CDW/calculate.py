"""Reproduce CDW research calculations. USD millions. Only derived inputs are shipped.
Run: python calculate.py. All forecast numbers are analyst scenarios, not company guidance.
"""
import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent
I=json.loads((P/'inputs.json').read_text());H=copy.deepcopy(I['reported'])
def sub(a,b):return {k:round(v-b[k],8) for k,v in a.items() if isinstance(v,(float,int)) and k in b}
for yr in [2025,2026]:
 H['Q2'+str(yr)]=sub(H['H1'+str(yr)],H['Q1'+str(yr)])
 H['Q3'+str(yr)]=sub(H['9M'+str(yr)],H['H1'+str(yr)])
H['Q42025']=sub(H['FY2025'],H['9M2025']);H['Q42024']=sub(H['FY2024'],H['9M2024'])
for yr in [2025,2026]:
 a,b,c=H['FY'+str(yr-1)],H['9M'+str(yr)],H['9M'+str(yr-1)]
 H['TTM'+str(yr)]={k:round(a[k]+b[k]-c[k],8) for k in a if isinstance(a[k],(int,float)) and k in b and k in c}
for p,h in H.items():
 h['fcf']=h['cfo']-h['capex'];h['gross_margin']=h['gross_profit']/h['sales'];h['ebit_margin']=h['ebit']/h['sales'];h['fcf_conversion']=h['fcf']/h['net_income'];h['cash_wc_change']=sum(h[k] for k in ['ar_change','inventory_change','other_assets_change','trade_payables_change','other_liabilities_change'])
 h['fcff_cash_proxy']=h['fcf']-h['sbc']+h['interest_net']*(1-.26)
# Cash proxy includes temporary WC, deferred taxes and other CFO reconciling items; not normalized forecast FCFF.
C=I['capital'];bridge=C['debt_face_including_receivable_finance']+C['product_financing']-max(0,C['cash']-C['minimum_cash_assumption'])
# First five years detailed, five transition years. SBC/rent remain in margins. No future buybacks or unpaid acquisition-driven revenue.
cases={
 'adverse':{'growth':[.00,.02,.03,.03,.03],'margin':[.073,.073,.074,.074,.075],'terminal_margin':.075,'g':.02,'wacc':.1025,'roic':.12,'nwc':.16,'capex':.0065,'depreciation':.005},
 'central':{'growth':[.07,.06,.05,.045,.04],'margin':[.078,.079,.08,.08,.08],'terminal_margin':.08,'g':.025,'wacc':.09,'roic':.15,'nwc':.13,'capex':.006,'depreciation':.005},
 'favorable':{'growth':[.10,.09,.08,.07,.06],'margin':[.08,.082,.084,.085,.085],'terminal_margin':.085,'g':.03,'wacc':.08,'roic':.18,'nwc':.10,'capex':.0055,'depreciation':.005}}
# Acquisition amortization removed from EBIT and D&A simultaneously; cash tax assessed on EBITA conservatively, no permanent acquisition-tax shield.
def value(s,growth_override=None,wacc=None,g=None,full_period_economic=False):
 s=copy.deepcopy(s);w=wacc or s['wacc'];tg=s['g'] if g is None else g;assert w>tg
 if growth_override is not None:s['growth']=[growth_override]*5
 rev=H['TTM2026']['sales'];rows=[];previous_nopat=(H['TTM2026']['ebit']+H['TTM2026']['acquired_amortization'])*.74
 for year in range(1,11):
  rate=s['growth'][year-1] if year<=5 else s['growth'][-1]+(tg-s['growth'][-1])*(year-5)/5
  margin=s['margin'][year-1] if year<=5 else s['margin'][-1]+(s['terminal_margin']-s['margin'][-1])*(year-5)/5
  old=rev;rev*=1+rate;ebita=rev*margin;nopat=ebita*.74;da=rev*s['depreciation'];capex=rev*s['capex'];nwc=(rev-old)*s['nwc'];physical=capex-da+nwc;economic=max(0,nopat-previous_nopat)/s['roic'];reinvestment=max(physical,economic) if full_period_economic else physical;fcff=nopat-reinvestment;incremental_roic=(nopat-previous_nopat)/physical if physical else None;previous_nopat=nopat
  rows.append(dict(year=year,sales=rev,growth=rate,ebita_margin=margin,ebita=ebita,nopat=nopat,da_ex_acquired_amort=da,capex_including_software=capex,delta_nwc=nwc,physical_net_reinvestment=physical,economic_net_reinvestment=economic,net_reinvestment=reinvestment,implied_incremental_roic=incremental_roic,fcff=fcff,pv=fcff/(1+w)**year))
 r11=rev*(1+tg);n11=r11*s['terminal_margin']*.74;economic=n11*tg/s['roic'];physical=r11*(s['capex']-s['depreciation'])+(r11-rev)*s['nwc'];reinv=max(economic,physical);fcf11=n11-reinv;tv=fcf11/(w-tg);pvt=tv/(1+w)**10;ev=sum(r['pv'] for r in rows)+pvt
 return {'years':rows,'terminal':{'sales':r11,'nopat':n11,'economic_reinvestment':economic,'physical_plus_nwc_reinvestment':physical,'reinvestment':reinv,'fcff':fcf11,'pv':pvt,'weight':pvt/ev},'enterprise_value':ev,'net_financial_claims':bridge,'equity_value':ev-bridge,'per_share':(ev-bridge)/C['diluted_shares_assumption']}
V={k:value(v)for k,v in cases.items()}
STRESS={k:value(v,full_period_economic=True)for k,v in cases.items()}
lo,hi=-.05,.3
for _ in range(100):
 mid=(lo+hi)/2
 if value(cases['central'],growth_override=mid)['per_share']<I['price']['close']:lo=mid
 else:hi=mid
inverse={'first_five_year_equal_growth':(lo+hi)/2,'fixed_central_margin_and_capital_assumptions':True,'target_price':I['price']['close']}
sensitivity=[{'wacc':w,'g':g,'value':value(cases['central'],wacc=w,g=g)['per_share']} for w in [.08,.09,.10,.11]for g in [.015,.02,.025,.03]]
qa={'ten_years_all_cases':all(len(x['years'])==10 for x in V.values()),'terminal_funding_max':all(x['terminal']['reinvestment']>=max(x['terminal']['economic_reinvestment'],x['terminal']['physical_plus_nwc_reinvestment'])-1e-8 for x in V.values()),'fy2025_quarters_tie_sales':abs(H['Q42025']['sales']+H['9M2025']['sales']-H['FY2025']['sales'])<1e-6,'ttm_quarters_tie_sales':abs(sum(H[p]['sales']for p in ['Q42025','Q12026','Q22026','Q32026'])-H['TTM2026']['sales'])<1e-6,'sbc_not_added_back':True,'product_finance_separate_from_operating_nwc':True,'no_free_buybacks':True,'status':'screen-grade; not entry approval','unresolved':['Normalized cash-tax and software maintenance split are analyst assumptions, not verified management forecasts.','Full acquisition contribution and contingent-consideration review remain incomplete.','Normalized working-capital forecast is a ratio proxy; multiyear software customer/vendor timing may diverge.','No technical Stage 3.5 or long-term trend verification.']}
O={'history':H,'case_assumptions':cases,'valuation':V,'inverse':inverse,'sensitivity':sensitivity,'full_period_economic_stress':STRESS,'qa':qa}
# Write after all QA checks are attached below.
with (P/'history.csv').open('w')as f:
 cols=['period','sales','gross_profit','gross_margin','ebit','ebit_margin','net_income','cfo','capex','fcf','da','sbc','cash_wc_change','fcff_cash_proxy'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(dict(period=p,**h)for p,h in H.items())
with (P/'forecast.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(V['central']['years'][0]));w.writeheader();w.writerows(dict(case=c,**r)for c,v in V.items()for r in v['years'])
with (P/'forecast-stress.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(STRESS['central']['years'][0]));w.writeheader();w.writerows(dict(case=c,**r)for c,v in STRESS.items()for r in v['years'])
qa['full_period_stress_funded']=all(r['net_reinvestment']>=max(r['physical_net_reinvestment'],r['economic_net_reinvestment'])-1e-8 for v in STRESS.values()for r in v['years'])
qa['stage3Complete']=False;qa['approvedValuation']=None
(P/'qa.json').write_text(json.dumps(qa,indent=2))
(P/'calculations.json').write_text(json.dumps(O,indent=2))
print(json.dumps({'values':{k:round(v['per_share'],2)for k,v in V.items()},'inverse':inverse,'history':{p:H[p]for p in ['TTM2026','TTM2025']},'qa':qa},indent=2))
