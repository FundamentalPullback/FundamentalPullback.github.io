import pathlib,json,csv
P=pathlib.Path(__file__).parent
# Finite 2027-36 cash-program diagnostic. Not an engineering NAV or whole company equity.
# Post-Eagle Ford operating scope, reference value at end2026. Unmodeled assets and residual reserves remain unknown.
def hedge(o,g,yr):
 days=365 if yr==2027 else 366
 if yr==2027:
  oil=(37000*(73.59-o)+94466*(max(59.61-o,0)-max(o-88.38,0))+57397*(max(57.25-o,0)-max(47.25-o,0)-max(o-73.14,0)))*days/1e6
  gas=490000*(max(3.17-g,0)-max(g-5.33,0))*days/1e6
 elif yr==2028:oil=9250*(73.59-o)*days/1e6;gas=0
 else:oil=gas=0
 return oil+gas
def calc(name,wt,hh,decline,unit_infl,discount):
 a=[];pv=0;oil=525.;ngl=320.;gas=4530.;cum=[0,0,0];annualFCF=[]
 for i in range(10):
  y=2027+i;days=366 if y in (2028,2032,2036) else 365
  # Explicit assumption: 320kb/d NGL, residual gas fits company total1.6m boe/day, not issuer breakdown.
  ob=oil*days/1000;nb=ngl*days/1000;gb=gas*days/1000;boe=ob+nb+gb/6
  rev=ob*wt*.985+nb*wt*.245+gb*hh*.65
  prodtax=.065*rev
  operating=boe*9.3*(1+unit_infl)**i+40*(1+unit_infl)**i
  h=hedge(wt,hh,y)
  cap=5300*(.2+.8*(boe/(1600*365/1000)))*(1+unit_infl)**i
  othercap=900 if i==0 else (408.5 if i==1 else 200*(1+unit_infl)**i)
  # Conservative budget tax shield through DD&A proxy, not historical deferred tax zero.
  depletion=11*boe
  tax=.22*max(rev-prodtax-operating+h-depletion,0)
  fcf=rev-prodtax-operating+h-tax-cap-othercap
  pv+=fcf/(1+discount)**(i+1)
  cum=[cum[0]+ob,cum[1]+nb,cum[2]+gb]
  a.append(dict(year=y,oil_mmbbl=ob,ngl_mmbbl=nb,gas_bcf=gb,total_mmboe=boe,revenue=rev,production_taxes=prodtax,operating_and_corporate_cost=operating,modeled_outright_hedges=h,cash_tax_proxy=tax,core_capex=cap,land_pipeline_other_capex=othercap,pre_financing_cash=fcf))
  # Explicit convergence: decline increases linearly by 5pts through year10, not free flat output.
  d=decline+.05*i/9;oil*=1-d;ngl*=1-d;gas*=1-d
 with (P/('forecast_'+name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=a[0]);w.writeheader();w.writerows(a)
 return {'wti':wt,'henry_hub':hh,'initial_decline_assumption':decline,'cost_inflation':unit_infl,'discount_rate_assumption':discount,'cash_window_pv_end2026_before_closure_basis_hedges_and_unmodeled_assets':pv,'cumulative_oil_mmbbl':cum[0],'cumulative_ngl_mmbbl':cum[1],'cumulative_gas_bcf':cum[2],'cumulative_mmboe':cum[0]+cum[1]+cum[2]/6,'terminal_unmodeled_asset_value':None,'current_whole_equity_value':None,'working_capital_cash_adjustment':None,'tax_basis_and_decline_calibration_validated':False,'approved_value':None,'year1_cash_before_financing':a[0]['pre_financing_cash']}
E=42.21*1139.714310;D=10636
cost={}
for n,b,kd in [('stress',1.8,.068),('central',1.5,.062),('high',1.2,.058)]:
 ke=.0486+b*.0441+.01;w=ke*E/(E+D)+kd*.78*D/(E+D)
 cost[n]={'rf_2026_11_06':.0486,'erp_2026_11_01':.0441,'beta_assumed':b,'execution_premium_assumed':.01,'ke':ke,'kd_assumed_not_bond_quote':kd,'wacc_conditional':w}
res={n:calc(n,*v,cost[n]['wacc_conditional']) for n,v in {'stress':(60,2.5,.15,.04),'central':(80,3.,.10,.025),'high':(100,4.5,.07,.02)}.items()}
def cash1(o):
 rev=525*.365*o*.985+320*.365*o*.245+4530*.365*3*.65
 pretax=rev*.935-584*9.3-40+hedge(o,3,2027)
 return pretax-.22*max(pretax-11*584,0)-5300-900
lo,hi=0,150
for _ in range(100):
 mid=(lo+hi)/2
 if cash1(mid)<1500+550*.78:lo=mid
 else:hi=mid
inverse={'WTI_to_fund_2027_budget_dividend1500_and_assumed_financing550_after_tax_HH3':(lo+hi)/2,'note':'Not inverse equity valuation; excludes mandatory debt repayment, sale proceeds and basis hedges.'}

# Published historical reserve/standardized measure reconciliation, never used as current EV.
reserve={'DVN_2025_mmboe':2428,'CTRA_2025_mmboe':2565.282,'sum_2025_mmboe':4993.282,'sum_oil_mmbbl':961+385.483,'sum_ngl_mmbbl':720+428.028,'sum_gas_bcf':4482+10511,'DVN_2025_standardized_measure':18765,'CTRA_2025_standardized_measure':13597,'sum_historical_standardized_measure':32362,'current_post_merger_post_sale_reserves':None,'current_corporate_NAV':None}
bridge={'date':'2026-09-30','cash':352,'restricted_cash_excluded':61,'carrying_debt':10636,'finance_leases':42,'operating_leases':523,'aro_carrying_value_not_future_closure_cash':1241,'legacy_decommissioning_liability':120,'net_derivative_liability':724,'investment_book_value_not_fair_value':1074,'solitude_contributed':83,'solitude_expected_total':500,'solitude_unfunded_expected':417,'solitude_max_exposure_including_funded':900,'eagle_ford_pending_gross_proceeds':4200,'eagle_ford_expected_net_proceeds':3500,'sale_completed':False,'nonquantified_environmental_legal_claims':None,'shares_m_oct23':1139.714310,'price_nov6':42.21,'market_cap':1139.714310*42.21,'approved_value':None}
# Primary sources-and-uses is independently reconciled, not a valuation.
plan={'date':'2026-11-05','oil_2027_kbd':525,'total_2027_kboed':1600,'assumed_strip_WTI':80,'assumed_strip_HH':3,'cfo_before_working_capital':12000,'net_sale_proceeds':3500,'core_capital':5300,'pipeline_ground_game':900,'debt_retirement':1500,'dividend':1500,'excess':6300,'identity_difference':12000+3500-5300-900-1500-1500-6300}
(P/'model_results.json').write_text(json.dumps({'scope':'Finite cash window, not corporate NAV. Residual engineering, closure schedule, basis derivatives and unmodeled equity investments unknown, not zero.','scenarios':res,'cost_of_capital':cost,'inverse_2027_funding':inverse,'reserve_reconciliation':reserve,'claims_bridge':bridge,'issuer_2027_sources_uses':plan,'approved_value':None,'approved_entry':None},indent=2))
print(json.dumps(res,indent=2))
