"""VFC independent ten-year retained-business FCFF. USDm except per share.
2026-11-04 research; Nov3 regular close. No trades. Run to reproduce JSON/CSV.
All forward margins are economic EBIT AFTER SBC, rents and recurring operating/restructuring costs.
Historical retained cash is not invented; forecast assumptions are explicitly separate.
"""
from pathlib import Path
import json,csv,copy,math
P=Path(__file__).parent
PRICE=20.04;REV0=9350.599
COMMON=393.639062;EXISTING_AWARD_PROXY=399.680-393.369;SHARES=COMMON+EXISTING_AWARD_PROXY
CLAIMS=dict(cash=442.951,minimum_operating_cash=200.,financial_debt_carrying=3538.589,debt_principal_uplift_proxy=19.534,pension_deficit=77.265,consulting_liability=2.1,restructuring_liability=24.607,legacy_tax_reserve_assumed=100.)
RF=.0495;ERP=.05;BETA=1.4;DEBT_SPREAD=.023;TARGET_DEBT_WEIGHT=.22;TAX=.28
COST_EQUITY=RF+BETA*ERP;COST_DEBT=RF+DEBT_SPREAD;INDICATIVE_WACC=COST_EQUITY*(1-TARGET_DEBT_WEIGHT)+COST_DEBT*(1-TAX)*TARGET_DEBT_WEIGHT
SCENARIOS={
 'adverse':dict(growth=[-.02,-.02,0,0,.01,.01,.01,.015,.015,.015],margin=[.065,.06,.06,.065,.065,.065,.065,.065,.065,.065],wacc=.12,g=.015,roic=.10,sc=3.,wc_ratio=.16,da_ratio=.025,maintenance=1.05,year1_extra_wc=150.,tax=.30),
 'central':dict(growth=[.025,.035,.04,.035,.03,.03,.025,.025,.025,.025],margin=[.082,.092,.10,.10,.10,.10,.10,.10,.10,.10],wacc=.105,g=.025,roic=.15,sc=4.,wc_ratio=.14,da_ratio=.025,maintenance=1.,year1_extra_wc=75.,tax=[.28,.27,.26,.25,.25,.25,.25,.25,.25,.25]),
 'favorable':dict(growth=[.045,.055,.05,.045,.04,.035,.03,.03,.025,.025],margin=[.085,.10,.11,.115,.12,.12,.12,.12,.12,.12],wacc=.095,g=.03,roic=.20,sc=5.,wc_ratio=.12,da_ratio=.025,maintenance=1.,year1_extra_wc=25.,tax=[.26,.25,.24,.23,.23,.23,.23,.23,.23,.23]),
}
def bisect(f,lo,hi):
 fl=f(lo);fh=f(hi)
 if fl*fh>0:return None
 for _ in range(130):
  mid=(lo+hi)/2;fm=f(mid)
  if fl*fm<=0:hi=mid
  else:lo=mid;fl=fm
 return (lo+hi)/2

def claim_amount(c=CLAIMS):
 return c['financial_debt_carrying']+c['debt_principal_uplift_proxy']+c['pension_deficit']+c['consulting_liability']+c['restructuring_liability']+c['legacy_tax_reserve_assumed']-c['cash']+c['minimum_operating_cash']

def equity(ev,c=CLAIMS,shares=SHARES):return max(0,ev-claim_amount(c))/shares

def project(p,c=CLAIMS,price=PRICE,shares=SHARES):
 p=copy.deepcopy(p);rows=[];rev=REV0
 for i in range(10):
  old=rev;rev*=1+p['growth'][i];ebit=rev*p['margin'][i];tax_rate=p['tax'][i] if isinstance(p['tax'],list) else p['tax'];tax=max(ebit,0)*tax_rate;nopat=ebit-tax;da=rev*p['da_ratio'];dwc=p['wc_ratio']*(rev-old)+(p['year1_extra_wc'] if i==0 else 0)
  # No permanent harvesting of assets: maintenance >= depreciation; growth capital includes working capital.
  growth_reinvestment=max(0,rev-old)/p['sc'];growth_wc=max(0,p['wc_ratio']*(rev-old))
  capex=da*p['maintenance']+max(0,growth_reinvestment-growth_wc)
  # ROIC-linked mature capital cost phased in over years8-10, avoiding a free terminal transition.
  blend=max(0,(i-6)/3)
  roic_net_investment=nopat*max(p['growth'][i],0)/p['roic']
  capex=max(capex,da+blend*max(0,roic_net_investment-dwc))
  fcff=nopat+da-capex-dwc
  rows.append(dict(year=i+1,revenue=rev,growth=p['growth'][i],ebit_margin=p['margin'][i],ebit=ebit,cash_tax_rate=tax_rate,cash_tax=tax,nopat=nopat,da=da,capex_total=capex,change_wc=dwc,fcff=fcff,pv_fcff=fcff/(1+p['wacc'])**(i+1),sbc_treatment='Already expensed inside EBIT; not added back or deducted again',normal_restructuring_treatment='Already expensed inside economic margin'))
 terminal_tax=p['tax'][-1] if isinstance(p['tax'],list) else p['tax'];terminal_revenue=rev*(1+p['g']);terminal_nopat=terminal_revenue*p['margin'][-1]*(1-terminal_tax);terminal_reinvestment=terminal_nopat*p['g']/p['roic'];terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(p['wacc']-p['g']);pv_tv=tv/(1+p['wacc'])**10;ev=sum(r['pv_fcff'] for r in rows)+pv_tv;value=equity(ev,c,shares);market_ev=price*shares+claim_amount(c)
 irr=bisect(lambda d:sum(r['fcff']/(1+d)**r['year'] for r in rows)+tv/(1+d)**10-market_ev,-.50,.75)
 # Stylized equity cash-distribution/refinancing proxy, not share-price CAGR or forecast dividends.
 # Treat other initial claims paid from equity at inception; excesscash distributed; financial debt held/refinanced then repaid terminally.
 debt=c['financial_debt_carrying']+c['debt_principal_uplift_proxy'];other=claim_amount(c)-debt
 rate_path=[.0425,.05]+[.065]*8
 eq_cf=[r['fcff']-debt*rate_path[i]*(1-r['cash_tax_rate']) for i,r in enumerate(rows)]
 eq_initial=price*shares+other;eq_terminal=tv-debt
 eqirr=bisect(lambda d:sum(cf/(1+d)**(i+1) for i,cf in enumerate(eq_cf))+eq_terminal/(1+d)**10-eq_initial,-.50,.9)
 return dict(params=p,years=rows,terminal_revenue=terminal_revenue,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,terminal_ev=tv,pv_terminal=pv_tv,terminal_share=pv_tv/ev,enterprise_value=ev,equity_value=max(0,ev-claim_amount(c)),per_share=value,upside=value/price-1,ten_year_revenue_cagr=(rev/REV0)**.1-1,enterprise_price=market_ev,enterprise_fixed_exit_irr=irr,equity_distribution_refinancing_proxy_irr=eqirr,equity_initial=eq_initial,equity_cashflows=eq_cf,equity_terminal=eq_terminal)

def build():
 out={'as_of':'2026-11-04','quote':dict(price=PRICE,date='2026-11-03 regular close',scanner_price=19.99,scanner_price_context='After-hours 18:01ET, kept distinct from regular20.04'), 'units':'USD millions except per-share and ratios','periods':'NTM1–NTM10 annualized forward periods using retained September2026TTM revenue anchor; not literal FY2027–FY2036; year-end discount convention, approximate annual forecast','retained_ttm_revenue':REV0,'claims':CLAIMS,'current_common_shares':COMMON,'existing_award_increment_proxy':EXISTING_AWARD_PROXY,'economic_share_denominator':SHARES,'net_claims':claim_amount(),'capital_cost':dict(risk_free=RF,risk_free_date='2026-11-03',risk_free_source='https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve',beta_assumed=BETA,erp_assumed=ERP,cost_equity=COST_EQUITY,cost_debt= COST_DEBT,debt_spread_assumed=DEBT_SPREAD,target_debt_weight=TARGET_DEBT_WEIGHT,tax=TAX,indicative_wacc=INDICATIVE_WACC,central_selected_wacc=.105),'scenarios':{k:project(p) for k,p in SCENARIOS.items()}}
 out['wacc_g_sensitivity']=[]
 for w in [.09,.095,.10,.105,.11,.12]:
  for g in [.015,.02,.025,.03]:
   p=copy.deepcopy(SCENARIOS['central']);p.update(wacc=w,g=g);z=project(p);out['wacc_g_sensitivity'].append(dict(wacc=w,g=g,value=z['per_share']))
 out['growth_margin_joint']=[]
 for gs in [-.02,0,.02,.04]:
  for ms in [-.02,0,.02,.04]:
   p=copy.deepcopy(SCENARIOS['central']);p['growth']=[x+gs for x in p['growth']];p['margin']=[x+ms*min(1,i/3) for i,x in enumerate(p['margin'])];z=project(p);out['growth_margin_joint'].append(dict(growth_shift=gs,margin_shift=ms,value=z['per_share'],revenue_cagr=z['ten_year_revenue_cagr'],terminal_margin=p['margin'][-1]))
 out['reverse_joint']=[]
 for w in [.095,.105,.12]:
  for target in [.08,.10,.12,.14]:
   def f(gs):
    p=copy.deepcopy(SCENARIOS['central']);p['growth']=[x+gs for x in p['growth']];shift=target-p['margin'][-1];p['margin']=[x+shift*min(1,i/3) for i,x in enumerate(p['margin'])];p['wacc']=w;return project(p)
   gs=bisect(lambda x:f(x)['per_share']-PRICE,-.045,.20)
   if gs is not None:
    z=f(gs);out['reverse_joint'].append(dict(wacc=w,year10_margin=target,growth_shift=gs,revenue_cagr=z['ten_year_revenue_cagr'],year10_revenue=z['years'][-1]['revenue'],first_year_margin=z['years'][0]['ebit_margin'],value=z['per_share']))
 out['cash_claim_sensitivities']=[]
 for reserve in [0,200,400]:
  for tax in [0,100,268.721]:
   c=copy.deepcopy(CLAIMS);c['minimum_operating_cash']=reserve;c['legacy_tax_reserve_assumed']=tax
   out['cash_claim_sensitivities'].append(dict(min_cash=reserve,legacy_tax_reserve=tax,value=equity(out['scenarios']['central']['enterprise_value'],c)))
 out['operating_sensitivities']=[]
 changes=[('no_extra_wc',{'year1_extra_wc':0}),('extra_wc200',{'year1_extra_wc':200}),('slower_capital_turnover',{'sc':2.5}),('faster_capital_turnover',{'sc':6}),('maintenance110pct',{'maintenance':1.1}),('terminal_roic10pct',{'roic':.10}),('terminal_roic20pct',{'roic':.20})]
 for n,ch in changes:
  p=copy.deepcopy(SCENARIOS['central']);p.update(ch);z=project(p);out['operating_sensitivities'].append(dict(case=n,value=z['per_share']))
 out['price_return_grid']=[]
 for price in [10,12,14,16,18,20.04,22,25]:
  z=project(SCENARIOS['central'],price=price);out['price_return_grid'].append(dict(price=price,enterprise_irr=z['enterprise_fixed_exit_irr'],equity_proxy_irr=z['equity_distribution_refinancing_proxy_irr']))
 out['tax_sensitivities']=[]
 for name,path in [('flat28pct',.28),('partial25pct',[.28,.27,.26,.25,.25,.25,.25,.25,.25,.25]),('reach23pct',[.28,.26,.24,.23,.23,.23,.23,.23,.23,.23])]:
  z=copy.deepcopy(SCENARIOS['central']);z['tax']=path;r=project(z);out['tax_sensitivities'].append(dict(case=name,value=r['per_share']))
 constructive=copy.deepcopy(SCENARIOS['favorable']);constructive['growth']=[.04]*10;constructive['margin']=[.085,.10,.11]+[.12]*7;constructive['tax']=[.28,.26,.24]+[.23]*7
 out['constructive_tax_margin_path']=project(constructive)
 def reverse_constructive(growth):
  z=copy.deepcopy(constructive);z['growth']=[growth]*10;return project(z)
 cg=bisect(lambda x:reverse_constructive(x)['per_share']-PRICE,-.02,.10)
 out['reverse_constructive']=dict(revenue_cagr=cg,value=reverse_constructive(cg)['per_share'],year10_margin=.12,wacc=.095,g=.03,roic=.20,tax=[.28,.26,.24]+[.23]*7)
 # Specific plausible turnaround joint alternative, not calibrated to force a pass.
 p=copy.deepcopy(SCENARIOS['central']);p['growth']=[.035,.045,.045,.04,.035,.035,.03,.03,.03,.03];p['margin']=[.0825,.095,.10,.105,.105,.105,.105,.105,.105,.105];p.update(wacc=.10,roic=.175);out['plausible_joint_alternative']=project(p)
 out['share_sensitivity']=[dict(shares=x,value=equity(out['scenarios']['central']['enterprise_value'],shares=x)) for x in [COMMON,SHARES,SHARES+4.]]
 (P/'model_results.json').write_text(json.dumps(out,indent=2))
 for n,z in out['scenarios'].items():
  with (P/(n+'_10_year_fcff.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=list(z['years'][0]));w.writeheader();w.writerows(z['years'])
 return out
if __name__=='__main__':
 o=build()
 for k,z in o['scenarios'].items():print(k,{x:round(z[x],4) for x in ['per_share','upside','ten_year_revenue_cagr','terminal_share','enterprise_fixed_exit_irr','equity_distribution_refinancing_proxy_irr']},'y10',z['years'][-1]['revenue'])
 print('alt',o['plausible_joint_alternative']['per_share']);print('reverse',o['reverse_joint'])
