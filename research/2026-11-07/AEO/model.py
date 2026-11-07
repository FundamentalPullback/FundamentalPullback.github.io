"""AEO screening FCFF, USD millions; assumptions not company forecasts.
Run python model.py. Retains ordinary SBC in EBIT, operating leases in rent.
"""
import json,pathlib
P=pathlib.Path(__file__).parent
REVENUE=5749.621
PRICE=19.92
SHARES=172.0
BRIDGE={'cash':147.954,'operating_cash_reserve':147.954,'financial_debt':55.0,'nonoperating_investments_credited':0.0,'minority_claim_reserve':5.0,'tax_contingency_reserve':10.0,'pension_claim':0.0,'operating_leases_subtracted':0.0}
CASES={
 'adverso':dict(growth=[-.02,0,.01,.015,.015],margins=[.045,.045,.0475,.05,.05],wacc=.12,g=.015,roic=.10,terminal_margin=.05),
 'central':dict(growth=[.04,.04,.035,.03,.025],margins=[.065,.0675,.07,.0725,.075],wacc=.105,g=.02,roic=.12,terminal_margin=.07),
 'favorable':dict(growth=[.06,.055,.05,.045,.04],margins=[.075,.08,.085,.09,.09],wacc=.095,g=.025,roic=.15,terminal_margin=.085)}
def calc(c,margin_shift=0,wacc=None,g=None):
 w=c['wacc'] if wacc is None else wacc; g=c['g'] if g is None else g
 assert w>g and c['roic']>g
 r=REVENUE; rows=[]; pv=0
 for year in range(1,11):
  if year<=5:
   gr=c['growth'][year-1]; m=c['margins'][year-1]+margin_shift
  else:
   a=(year-5)/5;gr=c['growth'][-1]*(1-a)+g*a;m=c['margins'][-1]*(1-a)+c['terminal_margin']*a+margin_shift
  prior=r;r*=1+gr;nopat=r*m*.75;da=r*.038;capex=r*.045;nwc=(r-prior)*.12
  structural=capex-da+nwc
  reinvest=structural if year<=5 else structural*(1-(year-5)/5)+nopat*gr/c['roic']*((year-5)/5)
  fcff=nopat-reinvest;discount=(1+w)**year;pv+=fcff/discount
  rows.append(dict(year=year,revenue=r,growth=gr,ebit_margin=m,ebit=r*m,tax=.25,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,structural_net_reinvestment=structural,transition_weight=max(0,(year-5)/5),transition_reinvestment_adjustment=reinvest-structural,component_status=('explicit_assumptions' if year<=5 else 'diagnostic_only_not_underwritten_component_forecasts'),net_reinvestment=reinvest,fcff=fcff,pv=fcff/discount))
 tn=r*(1+g)*(c['terminal_margin']+margin_shift)*.75;tf=tn*(1-g/c['roic']);tv=tf/(w-g);ptv=tv/(1+w)**10;ev=pv+ptv
 equity=ev+BRIDGE['cash']-BRIDGE['operating_cash_reserve']-BRIDGE['financial_debt']-BRIDGE['minority_claim_reserve']-BRIDGE['tax_contingency_reserve']
 return dict(value=equity/SHARES,ev=ev,equity=equity,pv_explicit=pv,pv_terminal=ptv,terminal_weight=ptv/ev,terminal_nopat=tn,terminal_fcff=tf,rows=rows)
res={k:calc(v) for k,v in CASES.items()}
lo,hi=-.04,.10
for _ in range(100):
 mid=(lo+hi)/2
 if calc(CASES['central'],mid)['value']<PRICE:lo=mid
 else:hi=mid
res['inverse']={'price':PRICE,'margin_shift_all_years':(lo+hi)/2,'year1_margin':.065+(lo+hi)/2,'year5_margin':.075+(lo+hi)/2,'terminal_margin':.07+(lo+hi)/2,'other_inputs':'central unchanged'}
res['sensitivity']=[{'wacc':w,'g':g,'value':calc(CASES['central'],wacc=w,g=g)['value']} for w in [.095,.105,.115] for g in [.015,.02,.025]]
res['capital_sensitivity_per_share']={'release_all_balance_cash':147.954/SHARES,'credit_35m_investment':35/SHARES,'credit_80m_investments':80/SHARES,'extra_100m_debt':-100/SHARES,'extra_10m_claim':-10/SHARES,'shares_170':res['central']['equity']/170,'shares_174':res['central']['equity']/174}
res['crosschecks']={'gaap_fy2024_pe_at_reference':PRICE/1.68,'fy2023_ebit_margin':222.717/5261.770,'fy2024_ebit_margin':427.303/5328.652,'fy2025_ebit_margin':226.222/5547.236,'ttm_limited_ex_refund_margin':286.948/REVENUE,'normalized_ttm_ebit_multiple':(PRICE*SHARES+70)/286.948,'central_year1_fcff_yield_on_ev':res['central']['rows'][0]['fcff']/(PRICE*SHARES+70)}
res['status']='screen-grade; conditional screening model, not approved intrinsic value or Stage 3 completion'
res['assumptions']={'cases':CASES,'bridge':BRIDGE,'shares':SHARES,'starting_revenue':REVENUE,'price':PRICE,'da_sales':.038,'capex_sales':.045,'incremental_nwc_sales':.12,'tax':.25,'transition':'Years6-10 blend structural net reinvestment toward NOPAT*growth/terminalROIC. Total net_reinvestment is authoritative; displayed D&A/capex/delta_nwc after year5 are diagnostic structural components, not an underwritten physical cash-flow forecast. Adjustment equals transition_weight*(NOPAT*growth/ROIC-structural). No operating reconciliation is claimed; terminal rent/SBC retained'}
assert all(x['terminal_weight']>0 and x['terminal_weight']<1 for k,x in res.items() if k in CASES)
P.joinpath('results.json').write_text(json.dumps(res,indent=2))
print(json.dumps({k:res[k]['value'] for k in CASES}));print(json.dumps(res['inverse']))
