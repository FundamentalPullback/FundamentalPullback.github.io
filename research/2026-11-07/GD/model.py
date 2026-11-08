"""GD: historia verificable + DCF condicional 10 años, no valor aprobado. USD millones."""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
A={2023:dict(revenue=42272,ebit=4245,net_income=3315,cfo=4710,capex=904,da=863,sbc=181,eps=12.02),2024:dict(revenue=47716,ebit=4796,net_income=3782,cfo=4112,capex=916,da=886,sbc=183,eps=13.63),2025:dict(revenue=52550,ebit=5356,net_income=4210,cfo=5120,capex=1161,da=924,sbc=196,eps=15.45)}
Y={2024:dict(revenue=34378,ebit=3373,net_income=2634,cfo=1952,capex=561,da=646,sbc=137),2025:dict(revenue=38171,ebit=3904,net_income=3067,cfo=3559,capex=552,da=672,sbc=146),2026:dict(revenue=42141,ebit=4407,net_income=3514,cfo=5745,capex=918,da=698,sbc=169)}
Q={'2025Q4':{k:A[2025][k]-Y[2025][k] for k in Y[2025]},'2026Q1':dict(revenue=13481,ebit=1420,net_income=1125,cfo=2155,capex=203,da=232,sbc=40,eps=4.10),'2026Q2':dict(revenue=14094,ebit=1460,net_income=1160,cfo=1880,capex=234,da=231,sbc=67,eps=4.24),'2026Q3':dict(revenue=14566,ebit=1527,net_income=1229,cfo=1710,capex=481,da=235,sbc=62,eps=4.49)}
T={y:{k:A[y-1][k]+Y[y][k]-Y[y-1][k] for k in Y[y]} for y in [2025,2026]}
for x in [*A.values(),*Q.values(),*T.values()]:x['fcf_reported']=x['cfo']-x['capex'];x['op_margin']=x['ebit']/x['revenue']
price=354.06;shares=273.8;rev0=T[2026]['revenue'];ebit0=T[2026]['ebit'];selected_nwc=2529+8906+9124-3166-11083
# Explicit conservative bridge. Unknown claims are NOT zero; excluded => conditional result.
bridge=dict(cash_reported=4388,operating_cash_assumption=.02*rev0,debt_principal=7070,finance_lease_assumption_stale_2025=392,retirement_liability_proxy_not_net_deficit=545,unknown_claim_liability=None)
bridge['excess_cash']=bridge['cash_reported']-bridge['operating_cash_assumption']
bridge['known_conditional_net_claims']=7070+392+545-bridge['excess_cash']
rf=.0486;erp=.0441;beta_observed=.30;beta_assumed=1.;ke=rf+erp*beta_assumed;kd=rf+.01;dw=7070/(price*270.2+7070);wacc=ke*(1-dw)+kd*.8*dw
# Scenario parameters are analyst hypotheses. No probability estimates, no approved case.
assumptions={'adverso':dict(growth=.02,gt=.02,m1=.095,m10=.09,wacc=.10,capex=.035,nwc=.17), 'central':dict(growth=.06,gt=.03,m1=.105,m10=.11,wacc=.09,capex=.03,nwc=.15), 'favorable':dict(growth=.08,gt=.03,m1=.11,m10=.12,wacc=.085,capex=.032,nwc=.14)}
def dcf(p,constant_growth=None,margin_shift=0):
 r=rev0;nwc=selected_nwc;rows=[];pv=0
 for y in range(1,11):
  g=p['growth'] if y<=5 else p['growth']+(p['gt']-p['growth'])*(y-5)/5
  if constant_growth is not None:g=constant_growth
  r*=1+g;m=p['m1']+(p['m10']-p['m1'])*(y-1)/9+margin_shift;ebit=r*m;nopat=ebit*.8;da=r*.016;capex=r*p['capex'];new_nwc=r*p['nwc'];dnwc=new_nwc-nwc;nwc=new_nwc;fcff=nopat+da-capex-dnwc;df=(1+p['wacc'])**y;pv+=fcff/df
  rows.append(dict(year=y,revenue=r,growth=g,margin=m,ebit=ebit,tax_rate=.2,nopat=nopat,da=da,capex=capex,nwc=nwc,delta_nwc=dnwc,net_reinvestment=capex-da+dnwc,fcff=fcff,pv=fcff/df))
 terminal_revenue=rows[-1]['revenue']*(1+p['gt']);terminal_nopat=rows[-1]['nopat']*(1+p['gt']);terminal_da=terminal_revenue*.016;terminal_capex=terminal_revenue*p['capex'];terminal_dnwc=terminal_revenue*p['nwc']-rows[-1]['nwc'];terminal_reinvestment=terminal_capex-terminal_da+terminal_dnwc;terminal_roic_implied=terminal_nopat*p['gt']/terminal_reinvestment;terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(p['wacc']-p['gt']);pvtv=tv/(1+p['wacc'])**10;ev=pv+pvtv;eq=ev-bridge['known_conditional_net_claims'];value=eq/shares
 return dict(parameters=p,rows=rows,terminal_revenue=terminal_revenue,terminal_da=terminal_da,terminal_capex=terminal_capex,terminal_delta_nwc=terminal_dnwc,terminal_roic_implied=terminal_roic_implied,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,terminal_value=tv,pv_terminal=pvtv,terminal_share=pvtv/ev,enterprise_value=ev,conditional_equity_value=eq,conditional_per_share=value,upside=value/price-1)
C={k:dcf(v) for k,v in assumptions.items()}
lo,hi=-.05,.2
for _ in range(100):
 mid=(lo+hi)/2
 if dcf(assumptions['central'],constant_growth=mid)['conditional_per_share']<price:lo=mid
 else:hi=mid
inverse=dict(required_10year_constant_revenue_growth=(lo+hi)/2,other_assumptions='Central margin path, explicit reinvestment, 9% WACC, 3% terminal growth, unknown claims excluded')
sensitivity=[]
for w in [.08,.09,.10]:
 for g in [.02,.03,.035]:
  p=assumptions['central']|dict(wacc=w,gt=g);z=dcf(p);sensitivity.append(dict(wacc=w,gt=g,conditional_per_share=z['conditional_per_share']))
O=dict(ticker='GD',as_of='2026-11-08',research_status='partial_material_accounting_investigation',stage3_completed=False,stage35_approved=False,approved_values=None,approved_price=None,price=dict(regular_close=price,date='2026-11-06',time='16:00 America/New_York',scanner_last=356.35,scanner_date='2026-11-05',opportunity=90),annual=A,ytd=Y,quarters=Q,ttm=T,ttm_growth={k:T[2026][k]/T[2025][k]-1 for k in ['revenue','ebit','net_income','cfo','capex','fcf_reported']},bridge=bridge,shares_diluted_proxy=shares,selected_nwc=selected_nwc,cost_of_capital=dict(rf=rf,rf_date='2026-11-06',rf_source_status='Primary US Treasury November 6 table independently verified; archived tool extract',erp=erp,erp_date='2026-11-01',erp_source='Damodaran primary',beta_observed=beta_observed,erp_source_rf=.0529,beta_observed_source='Yahoo 5y monthly snapshot 2026-11-08',beta_assumed=beta_assumed,ke_assumed=ke,mechanical_observed_beta_ke=rf+erp*beta_observed,kd_assumed=kd,debt_market_weight_proxy=dw,wacc_assumed_calculated=wacc,warning='No risk estimate for investigation. Rounded scenario WACC not observed market quote.'),conditional_cases=C,inverse=inverse,sensitivity=sensitivity,primary_gate='Electric Boat SEC/DOJ/OIG accounting investigations: no estimable loss range. No target approved.',known_model_limitations=['Quarter-end balance not rolled to valuation date','Finance leases proxy at FY2025, current total leases 2014 not split in Q3','Retirement liability 545 is proxy, not refreshed net pension deficit','Variable consideration and investigations not assigned zero fair liability','Terminal ROIC and investment productivity not independently validated','SBC retained in margin; fixed diluted shares no free buyback benefit'])
(P/'results.json').write_text(json.dumps(O,indent=2,ensure_ascii=False))
with (P/'financial_history.csv').open('w') as f:
 fields=['revenue','ebit','net_income','cfo','capex','fcf_reported','da','sbc','op_margin'];w=csv.writer(f);w.writerow(['period']+fields)
 for label,d in [(str(k),v) for k,v in A.items()]+list(Q.items())+[(f'TTM_Q3_{k}',v) for k,v in T.items()]:w.writerow([label]+[d.get(k) for k in fields])
assert all(abs(sum(v[k] for v in Q.values())-T[2026][k])<.01 for k in Y[2026])
assert all(r['net_reinvestment']>0 and abs(r['fcff']-(r['nopat']-r['net_reinvestment']))<1e-8 for c in C.values() for r in c['rows'])
assert all(c['parameters']['gt']<c['parameters']['wacc'] and c['terminal_roic_implied']>c['parameters']['gt'] for c in C.values())
print(json.dumps({'ttm':T,'growth':O['ttm_growth'],'wacc':wacc,'cases':{k:{t:v[t] for t in ['conditional_per_share','upside','terminal_share']} for k,v in C.items()},'inverse':inverse},indent=2))

assert all(abs(c['terminal_fcff']-c['rows'][-1]['fcff']*(1+c['parameters']['gt']))<1e-7 for c in C.values())
