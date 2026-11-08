"""USD millones; escenarios condicionales, no valores aprobados. Python 3, sin dependencias."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
H=json.loads((P/'financial_history.json').read_text()); SALES=H['TTM2026']['revenue_ex_reimbursements']; SHARES=259.4; PRICE=281.61
# Margen GAAP después de remuneración, alquileres y amortización; SBC no se añade.
SCENARIOS={'prudente':dict(sales1=17200,growth=.03,margin1=.18,margin10=.20,wacc=.10,g=.02,physical=.018,renewal=.074,expense_credit=0,growth_capital=.30,claims=600), 'central':dict(sales1=18000,growth=.05,margin1=.20,margin10=.235,wacc=.09,g=.025,physical=.016,renewal=.074,expense_credit=.020,growth_capital=.25,claims=300), 'favorable':dict(sales1=18800,growth=.07,margin1=.22,margin10=.27,wacc=.08,g=.03,physical=.015,renewal=.074,expense_credit=.035,growth_capital=.20,claims=100)}
# Créditos de renovación representan costes ya incluidos en margen, NO ahorro de caja automático.
def model(a, growth=None, wacc=None):
 first_year_organic_growth=a['growth'];a=a.copy();a['growth']=a['growth'] if growth is None else growth;a['wacc']=a['wacc'] if wacc is None else wacc
 rows=[];prev=SALES;pv=0
 for y in range(1,11):
  growth_rate=a['growth'] if y<=5 else a['growth']+(a['g']-a['growth'])*(y-5)/5
  sales=a['sales1'] if y==1 else prev*(1+growth_rate);m=a['margin1']+(a['margin10']-a['margin1'])*(y-1)/9
  nopat=sales*m*.76;dep=sales*.015;amort=sales*.074;replacement=sales*a['physical'];renewal=sales*max(0,a['renewal']-a['expense_credit'])
  # Año 1: exceso sobre TTM incluye anualización AP; no se presume totalmente orgánico ni se vuelve a comprar AP.
  organic_delta=prev*first_year_organic_growth if y==1 else sales-prev;growth_spend=organic_delta*a['growth_capital'];wc=organic_delta*.10
  fcff=nopat+dep+amort-replacement-renewal-growth_spend-wc;pv+=fcff/(1+a['wacc'])**y
  rows.append(dict(year=y,sales=sales,margin=m,nopat=nopat,depreciation=dep,amortization=amort,physical_replacement=replacement,intangible_replacement=renewal,growth_investment=growth_spend,delta_wc=wc,net_reinvestment=replacement+renewal+growth_spend+wc-dep-amort,growth_rate=growth_rate,fcff=fcff));prev=sales
 sales=prev*(1+a['g']);delta=sales-prev
 terminal=sales*a['margin10']*.76+sales*(.015+.074)-sales*(a['physical']+max(0,a['renewal']-a['expense_credit']))-delta*(a['growth_capital']+.10)
 tv=terminal/(a['wacc']-a['g']);ev=pv+tv/(1+a['wacc'])**10
 # Deuda principal incluye financiación de primas. No se netea un activo no verificado.
 bridge=dict(gross_debt=13091,earnouts=590,nci=33,tax_uncertainty_last_annual=30,pension_last_annual=2,declared_dividend_deducted=0,claims_and_other_unallocated_reserve=a['claims'],operating_cash=SALES*.03,unrestricted_cash=-935)
 claims=sum(bridge.values());equity=ev-claims
 return dict(assumptions=a,rows=rows,terminal_fcff=terminal,enterprise_value=ev,terminal_pv_weight=tv/(1+a['wacc'])**10/ev,bridge=bridge,net_claims=claims,equity=equity,price=max(0,equity/SHARES),raw_price=equity/SHARES)
def main():
 result={k:model(v) for k,v in SCENARIOS.items()};lo,hi=-.02,.40
 for i in range(100):
  mid=(lo+hi)/2
  if model(SCENARIOS['central'],growth=mid)['price']<PRICE:lo=mid
  else:hi=mid
 result['inverse']={'growth_years_2_to_5':(lo+hi)/2,'price':PRICE,'other_assumptions':'central, fixed first-year sales18000 and organic funding5%; growth fades years6-10 to2.5%; final margin23.5%'}
 result['approval']={'approved_values':None,'approved_price':None,'entry_approved':False,'stage3_complete':False,'capital_calibration_validated':False}
 result['cost_capital']={'rf':.0486,'rf_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','erp_source_rf':.0529,'beta_assumed':1.0,'kd_assumed':.055,'mixed_dates':True}
 result['sensitivity']=[dict(wacc=w,growth=g,price=model(SCENARIOS['central'],growth=g,wacc=w)['price']) for w in [.08,.09,.10] for g in [.03,.05,.07]]
 (P/'model_results.json').write_text(json.dumps(result,indent=2))
 for k in SCENARIOS:
  rows=result[k]['rows']
  with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print(json.dumps({k:result[k]['price'] for k in SCENARIOS}));print(result['inverse'])
if __name__=='__main__':main()
