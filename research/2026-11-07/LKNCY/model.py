"""Conditional RMB operating EV only. No approved ADS price or complete equity bridge."""
import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());base=h['TTM2026'];rev0=base['revenue'];stock0=6884.123;da0=1557.383+1416.033-1123.074;life=stock0/da0;k=stock0/rev0;cm0=(base['ebit']+da0)/rev0
rows=[];out={}
for name,start,g,cm_end,beta,premium,tax in [('stress',.08,.02,.14,1.5,.035,.30),('central',.12,.025,.16,1.25,.03,.28),('upside',.16,.03,.18,1,.025,.25)]:
 ke=.015868+beta*.0441+premium;wacc=.95*ke+.05*.04*(1-tax);rev=rev0;stock=stock0;pv=0
 for t in range(1,11):
  growth=start+(g-start)*(t-1)/9;cm=cm0+(cm_end-cm0)*t/10;old=rev;rev*=1+growth;da=stock/life;cap=da+k*(rev-old);ebit=rev*cm-da;nwc=.03*(rev-old);cf=ebit*(1-tax)+da-cap-nwc;stock+=cap-da;pv+=cf/(1+wacc)**t
  rows.append({'case':name,'year':2026+t,'revenue':rev,'growth':growth,'cash_operating_margin_after_rent_sbc_and_expensed_tech':cm,'physical_stock_end':stock,'physical_da':da,'funded_capex':cap,'ebit':ebit,'cash_tax':ebit*tax,'incremental_working_capital':nwc,'conditional_fcff':cf,'discount_rate':wacc})
 rev11=rev*(1+g);da11=stock/life;cap11=da11+g*stock;fcff11=(rev11*cm_end-da11)*(1-tax)+da11-cap11-.03*(rev11-rev);tv=fcff11/(wacc-g)
 # Every terminal dollar of growth funds equipment and working capital; rent/technology/SBC stay expensed.
 out[name]={'operating_EV_RMB_m_conditional':pv+tv/(1+wacc)**10,'PV_years1_10':pv,'terminal_year10_value':tv,'terminal_fcff11':fcff11,'terminal_capex11':cap11,'terminal_da11':da11,'ke_RMB_assumed':ke,'wacc_RMB_assumed':wacc,'g':g,'terminal_funding_cash_margin_zero_fcff':(da11+((cap11-da11)+.03*(rev11-rev))/(1-tax))/rev11,'approved_value':None}
a=[x for x in csv.DictReader((p/'daily_closes.csv').open()) if x['date']<='2026-11-06'];v=list(csv.DictReader((p/'volume_screen_input.csv').open()))
def ema(n):
 z=float(a[0]['close'])
 for x in a[1:]:z+=(float(x['close'])-z)*2/(n+1)
 return z
screen={'close_USD_ADS':34,'date':'2026-11-06','ordinary_per_ADS':8,'volume20_ADS':sum(float(x['volume']) for x in v)/len(v),'ema20':ema(20),'ema50':ema(50),'pullback_252_high_pct':100*(1-34/max(float(x['high']) for x in a[-252:])),'ttm_operating_margin':base['ebit']/rev0,'ttm_net_margin':base['net_parent']/rev0,'current_exact_diluted_ADS_count':None,'capex_TTM':None}
r={'scope':'RMB conditional operating EV; no complete equity/ADS valuation','scenarios':out,'screen':screen,'physical_life_assumed_years':life,'physical_stock_sales_ratio':k,'opening_cash_margin':cm0,'excess_remittable_cash':None,'current_preferred_dilution_bridge':None,'unvalued_long_term_investment':None,'unquantified_claims':None,'approved_value':None,'approved_entry':None}
(p/'model_results.json').write_text(json.dumps(r,indent=2));(p/'screen.json').write_text(json.dumps(screen,indent=2))
with (p/'model_years.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(r,indent=2))
