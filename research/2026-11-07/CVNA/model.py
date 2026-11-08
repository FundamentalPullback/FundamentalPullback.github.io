"""FCFF de contraste, NO aprobado. USD millones; acciones millones pos split.
Modelo deliberadamente separa crecimiento físico y financiación. No se suman
entradas de deuda a FCFF. TRA/DTA requieren conciliación antes de aprobación.
"""
import json,pathlib
P=pathlib.Path(__file__).parent
PRICE=73.57; SHARES=1127.041
SALES=27451.; MARGIN=2399/SALES
# Capital operativo aproximado, sin caja restringida, DTA ni leases operativos.
IC0=3456+896+557+320+227-1574+2914+51+12+1000
CASES={
 'conservador':dict(growth=[.15,.12,.10,.08,.06,.05,.04,.03,.025,.025],margin=.08,capex=.018,da=.01,nwc=.16,wacc=.095,g=.025),
 'base':dict(growth=[.30,.25,.20,.16,.12,.10,.08,.06,.04,.03],margin=.115,capex=.015,da=.01,nwc=.14,wacc=.095,g=.03),
 'favorable':dict(growth=[.38,.32,.27,.22,.18,.13,.09,.06,.04,.03],margin=.125,capex=.015,da=.01,nwc=.14,wacc=.095,g=.03)}
def calc(c,tra=2230,dta=0,cash=2049):
 sales=SALES;ic=IC0;pv=0;rows=[]
 for y,growth in enumerate(c['growth'],1):
  old=sales;sales*=1+growth;m=MARGIN+(c['margin']-MARGIN)*min(y/5,1)
  nopat=sales*m*.75;da=sales*c['da'];capex=sales*c['capex'];wc=(sales-old)*c['nwc'];acq=.002*sales
  reinv=capex+acq-da+wc;ic+=reinv;fcff=nopat-reinv;pv+=fcff/(1+c['wacc'])**y
  rows.append(dict(year=y,revenue=sales,ebit_margin=m,nopat=nopat,da=da,physical_capex_including_financed=capex,acquisitions=acq,delta_working_capital=wc,reinvestment=reinv,capital_end=ic,fcff=fcff))
 # Original diagnostic assumes stable capital turns. Its implied physical capex
 # can drop abruptly: retain only with explicit validation flags and comparison.
 g=c['g'];terminal_nopat=nopat*(1+g);terminal_reinvestment=ic*g
 terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(c['wacc']-g);pv_tv=tv/(1+c['wacc'])**10;ev=pv+pv_tv
 equity=ev+cash-5161-100-tra+dta
 terminal_sales=sales*(1+g)
 implied_capex=da*(1+g)+terminal_reinvestment-c['nwc']*sales*g-.002*terminal_sales
 constant_capex=c['capex']*terminal_sales
 constant_reinvestment=constant_capex+.002*terminal_sales-da*(1+g)+c['nwc']*sales*g
 constant_fcff=terminal_nopat-constant_reinvestment
 constant_pv_tv=constant_fcff/(c['wacc']-g)/(1+c['wacc'])**10
 constant_ev=pv+constant_pv_tv
 constant_value=(constant_ev+cash-5161-100-tra+dta)/SHARES
 ttm_units=596641+602103-433119
 units=sales/(SALES/ttm_units)
 support=True if units<=1500000 else (False if units>3000000 else None)
 terminal_diagnostics=dict(year10_capex=capex,year11_implied_capex=implied_capex,
  year10_capex_sales=c['capex'],year11_implied_capex_sales=implied_capex/terminal_sales,
  capex_change_year11_vs_year10=implied_capex-capex,capex_change_pct=implied_capex/capex-1,
  reduction_vs_constant_capex=constant_capex-implied_capex,
  reinvestment_continuity_validated=False,original_diagnostic_only=True,
  year10_units_at_ttm_revenue_per_unit=units,built_capacity_units=1500000,
  real_estate_potential_units=3000000,within_declared_footprint=units<=3000000,
  capacity_support=support,capacity_assessment_horizon='year10_only',terminal_capacity_verified=False,incremental_expansion_funding_verified=False,
  note='Unit equivalence holds mix and prices constant; not a unit forecast. Null support means unverified buildout within footprint; false exceeds footprint.')
 terminal_sensitivity=dict(method='Constant capex/sales, D&A/sales, acquisitions/sales and working-capital ratio',
  value=constant_value,enterprise_value=constant_ev,terminal_weight=constant_pv_tv/constant_ev,
  terminal_capex=constant_capex,terminal_reinvestment=constant_reinvestment,terminal_fcff=constant_fcff,
  terminal_year11_capital_end=ic+constant_reinvestment,
  immediate_terminal_roic=terminal_nopat/(ic+constant_reinvestment),
  eventual_steady_state_roic=c['margin']*.75*g/((c['capex']+.002-c['da'])*(1+g)+c['nwc']*g),
  capex_intensity_continuity=True,capacity_support=support,valuation_approved=False,
  note='Does not force capital to grow at g immediately; accumulated capital converges under continued investment. No new per-car assumption.')
 return dict(terminal_diagnostics=terminal_diagnostics,constant_capex_terminal_sensitivity=terminal_sensitivity,value=equity/SHARES,enterprise_value=ev,equity_value=equity,terminal_weight=pv_tv/ev,terminal_roic=nopat/ic,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,terminal_year11_capex=da*(1+g)+terminal_reinvestment-c['nwc']*sales*g-.002*sales*(1+g),rows=rows,bridge=dict(cash_excess=cash,debt=5161,finance_leases=100,tra=tra,dta=dta,fully_converted_diluted_shares=SHARES),assumptions=c)
def solve_margin():
 lo,hi=0,.50
 for _ in range(100):
  mid=(lo+hi)/2;c={**CASES['base'],'margin':mid}
  if calc(c)['value']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
if __name__=='__main__':
 out={'status':'material_partial_not_approved','approved_fair_value':None,'approved_price_ceiling':None,'price':PRICE,'price_date':'2026-11-06','currency':'USD','units':'millions except per share','initial_operating_capital_proxy':IC0,'scenarios':{n:calc(c) for n,c in CASES.items()},'sensitivity_wacc':{str(w):calc({**CASES['base'],'wacc':w})['value'] for w in [.085,.095,.105]},'claims_sensitivity':{'gross_TRA_no_DTA':calc(CASES['base'])['value'],'no_TRA_no_DTA':calc(CASES['base'],tra=0)['value'],'face_DTA_less_face_TRA_NOT_PV':calc(CASES['base'],dta=2905)['value']},'inverse_margin_same_growth':solve_margin(),'missing':['Present value of tax benefits and TRA with full conversion and normalized taxation','Durable capital turns after reconditioning expansion and loan-retention needs','Independently justified normalized company beta and WACC; sector anchor alone insufficient'],'validation_flags':{'terminal_reinvestment_continuity_validated':False,'original_scenarios_diagnostic_only':True,'favorable_capacity_supported':False,'valuation_approved':False},'classification':'Contraste analítico no utilizable como precio aprobado'}
 (P/'model_results.json').write_text(json.dumps(out,indent=2)); print({k:v for k,v in out.items() if k!='scenarios'});print({k:round(v['value'],2) for k,v in out['scenarios'].items()})
