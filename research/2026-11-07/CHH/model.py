"""CHH: USD millones, FCFF condicional. Ejecutar python model.py; sólo biblioteca estándar."""
from pathlib import Path
import json,csv
P=Path(__file__).parent
keys='revenues franchise_fees reimb_revenues reimb_expenses ebit net_income cfo capex_other capex_hotels da_core da_system key_amort key_cash sbc'.split()
raw={
'FY2023':[1544.165,652.060,647.577,680.410,375.028,258.507,296.554,47.717,68.560,45.038,30.697,20.024,98.316,40.514],
'FY2024':[1584.839,669.637,638.192,656.344,463.773,299.665,319.403,39.102,106.750,51.953,18.907,28.702,112.164,38.440],
'FY2025':[1596.793,673.197,616.204,663.336,448.399,369.946,270.447,38.924,106.871,59.715,19.554,31.966,83.444,38.321],
'9M2024':[1195.069,511.450,477.076,501.857,344.554,223.861,236.540,33.620,81.239,38.545,14.314,20.584,84.085,28.120],
'9M2025':[1206.643,515.931,460.207,504.437,346.945,306.264,184.757,26.927,85.307,42.932,14.295,25.020,62.359,32.576],
'9M2026':[1239.665,540.834,460.164,552.264,270.651,142.554,121.914,25.612,37.533,50.567,17.076,30.051,103.993,15.371],
'Q12026':[340.575,149.631,123.904,161.787,60.034,20.304,-23.174,10.065,16.819,16.821,5.115,9.580,42.842,8.292],
'H12026':[781.337,337.167,287.228,359.452,164.172,84.642,67.362,17.900,27.292,33.634,11.228,20.201,72.169,12.536]}
h={p:dict(zip(keys,v)) for p,v in raw.items()}
def delta(a,b):return {k:round(h[a][k]-h[b][k],6) for k in keys}
h['Q42025']=delta('FY2025','9M2025');h['Q22026']=delta('H12026','Q12026');h['Q32026']=delta('9M2026','H12026')
for y in [2025,2026]:h['TTM092'+str(y)[1:]]={k:round(h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k],6) for k in keys}
# Explicit aliases to avoid any ambiguous period label.
h['TTM2025-09']=h.pop('TTM092025');h['TTM2026-09']=h.pop('TTM092026')
t=h['TTM2026-09']; core=t['revenues']-t['reimb_revenues']; deficit=t['reimb_expenses']-t['reimb_revenues']
normalized_sbc=38.; ebcore=t['ebit']+deficit+24.268+6.035-(normalized_sbc-t['sbc'])-2.
shares=45.076;price=118.91;debt=400+450+600+500+242.1+1.85;cash=170.594;opcash=50.;netclaims=debt-(cash-opcash)+130-34+(54.076-47.549)
# Harvest EV is separately sensitized; cash consideration deducted once. No invented pro forma revenue.
def calc(g,margin,wacc,gt,keycash,sysdef,loans,roic,harvest,stress=0):
 r=core;prior_nopat=(ebcore-sysdef)*.74;pv=0;rows=[]
 for y in range(1,11):
  gy=g if y<=5 else g+(gt-g)*(y-5)/5
  old=r;r*=1+gy;ratio=r/core;m=ebcore/core+(margin-ebcore/core)*min(y/3,1)
  sd=sysdef*ratio;eb=r*m-sd;nop=eb*.74
  ida=32*ratio;pda=(t['da_core']+t['da_system']-32)*ratio;ka=t['key_amort']*ratio
  pcap=max(70*ratio,pda);icap=ida;kc=max(keycash*ratio,ka);lend=loans*ratio;wc=.2*(r-old)
  net=pcap-pda+kc-ka+lend+wc
  funded_growth=max(0,gy,nop/prior_nopat-1)
  extra=max(0,nop*funded_growth/roic-net)
  prior_nopat=nop
  fc=nop+pda+ida+ka-pcap-icap-kc-lend-wc-extra-(stress if y==1 else 0)
  pv+=fc/(1+wacc)**y
  rows.append(dict(year=y,funded_profit_growth=funded_growth,core_revenue=r,growth=gy,core_margin=m,system_deficit=sd,ebit=eb,nopat=nop,physical_da=pda,intangible_da=ida,key_amort=ka,physical_capex=pcap,intangible_replacement=icap,key_cash=kc,lending_equity_funding=lend,working_capital=wc,roic_extra_funding=extra,fcff=fc))
 last=rows[-1];rn=r*(1+gt);n=(rn*margin-sysdef*rn/core)*.74
 floor=(last['physical_capex']-last['physical_da']+last['key_cash']-last['key_amort']+last['lending_equity_funding'])*(1+gt)+.2*r*gt
 tr=max(n*gt/roic,floor);terminal=n-tr;tv=terminal/(wacc-gt);ev=pv+tv/(1+wacc)**10
 return dict(growth_years1to5=g,margin=margin,wacc=wacc,terminal_growth=gt,key_cash_base=keycash,system_deficit_base=sysdef,loan_equity_funding_base=loans,incremental_roic_cap=roic,harvest_ev_assumption=harvest,rows=rows,terminal_nopat=n,terminal_net_reinvestment=tr,terminal_fcff=terminal,ev=ev,terminal_share_ev=tv/(1+wacc)**10/ev,net_claims=netclaims,equity_residual=ev+harvest-netclaims,raw_equity_per_share=(ev+harvest-netclaims)/shares,price=max(0,(ev+harvest-netclaims)/shares))
cases={'prudente':calc(.025,.45,.105,.02,140,95,40,.12,65,59), 'intermedio':calc(.05,.48,.095,.025,125,45,30,.16,130),'expansivo':calc(.07,.52,.085,.03,100,0,20,.20,195)}
lo,hi=.30,1.0
for _ in range(100):
 mid=(lo+hi)/2
 if calc(.05,mid,.095,.025,125,45,30,.16,130)['price']<price:lo=mid
 else:hi=mid
inv=calc(.05,(lo+hi)/2,.095,.025,125,45,30,.16,130)
inverse_solved=abs(inv['price']-price)<1e-6
inverse_boundary=inv
if not inverse_solved:inv=None
ke=.0486+1.3*.0441;kd=.0486+.015;dw=debt/(debt+shares*price);wacc=ke*(1-dw)+kd*.74*dw
checks={k:sum(h[p][k] for p in ['Q42025','Q12026','Q22026','Q32026'])-t[k] for k in keys};assert max(abs(v) for v in checks.values())<1e-6
res=dict(as_of='2026-11-08',units='USD millones salvo precio/acción',history=h,quote={'price':price,'date':'2026-11-06','session':'NYSE cierre regular 16:00 EST','source':'StockAnalysis corroborado FT/ChartExchange; secundario','scanner_price':111.16,'scanner_date':'2026-10-30','opportunity':80},normalization={'core_revenue':core,'gaap_ebit':t['ebit'],'system_deficit':deficit,'termination_addback':24.268,'hotel_impairment_addback':6.035,'sbc_normalized':normalized_sbc,'ttm_sbc':t['sbc'],'sold_hotels_ebit_assumed_removed':2.,'core_ebit':ebcore,'system_deficit_recovery_asset_added':0,'sbc_added_back_to_fcff':False},bridge={'debt_principal_rounded':debt,'book_debt':2177.105,'cash':cash,'operating_cash_assumed':opcash,'harvest_cash_cost':130,'hotel_sales_net_estimate':34,'deferred_comp_net_proxy':54.076-47.549,'net_claims':netclaims,'shares_diluted_q3_proxy':shares,'basic_oct26':44.508546,'operating_leases_not_added':102.315,'affiliate_and_notes_values_not_added':'Operating assets required for franchise economics; no separate asset uplift'},capital_cost={'rf_nov6':.0486,'erp_nov1':.0441,'erp_source_riskfree':.0529,'parameter_dates_not_matched':True,'beta_assumed':1.3,'ke':ke,'kd_assumed':kd,'market_debt_weight':dw,'wacc_anchor':wacc},conditional_cases=cases,inverse_margin=inv,inverse_status=('solved' if inverse_solved else 'No solution in tested core EBIT margin range30–100%; boundary sensitivity is not target margin'),inverse_boundary_sensitivity=inverse_boundary,checks=checks,approved_values=None,approved_price=None,entry_approved=False)
(P/'results.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+keys);w.writeheader();w.writerows(dict(period=p,**v) for p,v in h.items())
print(json.dumps({'prices':{k:v['price'] for k,v in cases.items()},'inverse_margin':inv['margin'] if inv else None,'bridge':netclaims,'wacc_anchor':wacc,'ttm':t,'core_ebit':ebcore},indent=2))
