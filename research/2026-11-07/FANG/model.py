"""Conditional finite operating cash window, not reserve-certified NAV or equity valuation."""
import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());a=list(csv.DictReader((p/'daily_closes.csv').open()));a=[x for x in a if x['date']<='2026-11-06']
def ema(n):
 z=float(a[0]['close'])
 for x in a[1:]:z+=(float(x['close'])-z)*2/(n+1)
 return z
v=list(csv.DictReader((p/'volume_screen_input.csv').open()));price=178.96;shares=279.167841
screen={'close_date':'2026-11-06','regular_close':price,'shares_m_2026_10_30':shares,'cap_m':price*shares,'ema20':ema(20),'ema50':ema(50),'pullback_252_high_pct':100*(1-price/max(float(x['high']) for x in a[-252:])),'volume20':sum(float(x['volume']) for x in v)/len(v),'ttm_ebit_margin':h['TTM2026']['ebit']/h['TTM2026']['revenue'],'ttm_parent_net_margin':h['TTM2026']['net_parent']/h['TTM2026']['revenue'],'ema_initialization':'first archived daily close, two-year series'}
# Physical annual scale from company 2026 guidance; gas/NGL ratio from Q3 actual mix.
# Reserve table includes subsidiaries; no minority allocation is inferred.
q0=1015*365/1000;oil_share=524/1015;gas_share=(1-oil_share)*(135002/6)/(135002/6+24330);ngl_share=1-oil_share-gas_share
cases=[('stress',55,0,14,.04,.10,1.5),('central',70,1,18,.02,.07,1.25),('upside',85,2,22,.00,.04,1.0)]
allrows=[];out={}
for name,oil,gas,ngl,d1,d2,beta in cases:
 ke=.0486+beta*.0441;wacc=.8*ke+.2*.06*(1-.23);q=q0;pv=0;cum=0;rows=[]
 for year in range(1,11):
  # Explicit decline transition in years 6-10. No new zero-cost reserves.
  decline=d1 if year<=5 else d1+(d2-d1)*(year-5)/5
  q=min(q*(1-decline),max(0,3617.856-q0-cum));cum+=q;infl=1.02**(year-1)
  rev=q*(oil_share*oil+gas_share*6*gas+ngl_share*ngl)
  cashcost=q*(6.075+1.4+.6+.30)*infl # LOE/GPT/cash G&A and economic SBC allowance
  production_tax=.065*rev;depletion=q*14 # hypothetical tax base only, not asset renewal assumption
  tax=max(0,(rev-cashcost-production_tax-depletion)*.205)
  # Pay full base drilling budget; no capex cut just because output falls.
  capex=3975*infl
  # Additional disclosed fixed-power costs spread evenly where issuer only gives cumulative totals.
  power=28 if year==2 else 66 if year in [3,4] else 359/4 if year in [5,6,7,8] else 0
  cf=rev-cashcost-production_tax-tax-capex-power
  pv+=cf/(1+wacc)**year
  rows.append({'case':name,'year':2026+year,'decline':decline,'production_mmboe':q,'oil_realized_assumption':oil,'revenue':rev,'cash_operating_cost_including_sbc':cashcost,'production_taxes':production_tax,'cash_income_tax_assumed':tax,'funded_drilling_capex':capex,'additional_power_contract':power,'conditional_asset_cash':cf,'discount_rate':wacc,'pv_cash':cf/(1+wacc)**year})
 out[name]={'pv_ten_year_cash_window':pv,'cumulative_mmboe':cum,'cumulative_oil_mmbbl_proxy':cum*oil_share,'cumulative_gas_bcf_proxy':cum*gas_share*6,'cumulative_ngl_mmbbl_proxy':cum*ngl_share,'product_specific_reserve_budget_validated':False,'conditional_ke':ke,'conditional_wacc':wacc,'terminal_value':None,'whole_equity_value':None}
 allrows+=rows
# Year-one oil price funding breakeven with central gas/NGL, before interest, minority, closure/JV/dividends.
def cf(o):
 q=q0*.98;rev=q*(oil_share*o+gas_share*6+ngl_share*18);cost=q*(6.075+1.4+.6+.30);return rev-cost-.065*rev-max(0,(rev-cost-.065*rev-q*14)*.205)-3975
lo,hi=0,200
for _ in range(100):
 mid=(lo+hi)/2
 if cf(mid)>0:hi=mid
 else:lo=mid
r={'scope':'finite conditional asset cash window, no current full NAV or stock target','screen':screen,'scenarios':out,'funding_inverse_realized_oil_not_WTI':(lo+hi)/2,'not_modeled':['future hedge settlements and basis','separate Viper minority economics','exact reserve depletion/development schedule','corporate/JV funding and closure timing','working capital and complete current equity bridge'],'unvalued_tail':None,'approved_value':None,'approved_entry':None}
(p/'model_results.json').write_text(json.dumps(r,indent=2));(p/'screen.json').write_text(json.dumps(screen,indent=2))
with (p/'finite_cash_scenarios.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=allrows[0]);w.writeheader();w.writerows(allrows)
print(json.dumps(r,indent=2))
