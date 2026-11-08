"""GGG: USD millones, valoración FCFF reproducible con supuestos explícitos."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
keys='sales ebit net_income cfo capex da sbc rd'.split()
a={'FY2023':[2195.606,646.843,506.511,651.017,184.775,74.321,30.229,82.822],'FY2024':[2113.316,570.098,486.084,621.700,106.737,86.749,31.892,87.230],'FY2025':[2236.604,624.797,521.839,683.591,45.669,107.433,34.333,82.297],'9M2024':[1564.644,440.080,377.376,436.486,92.788,62.054,27.312,65.076],'9M2025':[1643.448,466.218,389.352,487.262,33.646,75.744,24.495,60.357],'9M2026':[1717.081,460.986,384.994,463.439,47.649,77.629,23.553,60.389],'Q12026':[540.144,137.775,118.506,120.248,12.141,28.602,7.549,19.974],'H12026':[1130.696,312.869,263.433,297.965,28.516,51.643,15.569,39.799]}
h={p:dict(zip(keys,v)) for p,v in a.items()}
def sub(a,b):return {k:round(h[a][k]-h[b][k],6) for k in keys}
h['Q42025']=sub('FY2025','9M2025');h['Q22026']=sub('H12026','Q12026');h['Q32026']=sub('9M2026','H12026')
for y in [2025,2026]:h[f'TTM{y}-09']={k:round(h[f'FY{y-1}'][k]+h[f'9M{y}'][k]-h[f'9M{y-1}'][k],6) for k in keys}
t=h['TTM2026-09'];shares=163.021;price=67.86;cash=139.818;debt=104.479;opcash=.03*t['sales'];pension=56.913+20.759;deferred=8.970;contingent=1.593;dividend=47.348
claims=debt+opcash+pension+deferred+contingent+dividend-cash
# No automatic NOPAT*g/ROIC add-on: product development already expenses productivity investment.
# Growth capital explicitly funds capacity and WC; ROIC diagnostic, not capitalizing R&D twice.
def calc(first,g,margin,wacc,gt,capacity,wc,maintenance,intangible,fee_reserve,rd_coverage=.25):
 sales=t['sales'];rows=[];pv=0;prior_nopat=None;startmargin=(t['ebit']-9-fee_reserve)/t['sales']
 for year in range(1,11):
  old=sales;gy=first/old-1 if year==1 else g if year<=5 else g+(gt-g)*(year-5)/5
  sales*=1+gy;scale=sales/2500;m=startmargin+(margin-startmargin)*min(year/3,1);eb=sales*m;n=eb*.79
  pda=80*scale;ida=intangible*scale;maint=maintenance*scale
  organic_increment=max(0,sales-old-(146.6 if year==1 else 0));growthcap=capacity*organic_increment;pcap=max(pda,maint)+growthcap;rd_cover=min(ida,sales*.036*rd_coverage);icap=max(0,ida-rd_cover);wcneed=wc*organic_increment
  # Conservative constant-policy adjustment: no second amortization tax shield for renewal assumed expensed in R&D.
  renewal_tax_adjustment=rd_cover*.21
  fc=n+pda+ida-pcap-icap-wcneed-renewal_tax_adjustment
  reinv=pcap-pda+wcneed;ir=((sales-old)*m*.79/reinv) if reinv>0 and year>1 else None
  economic_net_reinvestment=reinv-rd_cover+renewal_tax_adjustment
  total_profit_roic=((n-prior_nopat)/economic_net_reinvestment) if prior_nopat is not None and economic_net_reinvestment>0 else None
  prior_nopat=n
  pv+=fc/(1+wacc)**year
  rows.append(dict(year=year,sales=sales,growth=gy,ebit_margin=m,ebit=eb,nopat=n,physical_da=pda,intangible_da=ida,physical_maintenance=max(pda,maint),organic_increment_for_new_funding=organic_increment,capacity_growth_capex=growthcap,total_physical_capex=pcap,intangible_replacement=icap,intangible_renewal_covered_by_expensed_rd=rd_cover,working_capital=wcneed,physical_wc_net_reinvestment=reinv,net_reinvestment=economic_net_reinvestment,renewal_tax_adjustment=renewal_tax_adjustment,sales_only_roic_diagnostic=ir,incremental_roic_diagnostic=total_profit_roic,fcff=fc,rd_expensed_reference=sales*.036,sbc_expensed=True))
 sr=sales*(1+gt);np=sr*margin*.79;pd=80*sr/2500;pc=max(pd,maintenance*sr/2500)+capacity*sales*gt;wcend=wc*sales*gt;nr=pc-pd+wcend;renew_credit=min(intangible*sr/2500,sr*.036*rd_coverage);tax_adj=renew_credit*.21;economic_nr=nr-renew_credit+tax_adj;tf=np-economic_nr;tv=tf/(wacc-gt);ev=pv+tv/(1+wacc)**10
 return dict(first_year_sales=first,growth_years2to5=g,margin=margin,wacc=wacc,terminal_growth=gt,capacity_per_incremental_sales=capacity,wc_per_incremental_sales=wc,maintenance_base=maintenance,intangible_replacement_base=intangible,upfront_fee_uncertainty_reserve=fee_reserve,rd_coverage_fraction=rd_coverage,rows=rows,terminal_fcff=tf,terminal_physical_wc_net_reinvestment=nr,terminal_net_reinvestment=economic_nr,terminal_renewal_tax_adjustment=tax_adj,terminal_reinvestment_rate=economic_nr/np,terminal_physical_capex=pc,terminal_physical_da=pd,terminal_intangible_replacement=max(0,intangible*sr/2500-sr*.036*rd_coverage),terminal_intangible_renewal_covered_by_expensed_rd=renew_credit,ev=ev,terminal_share_ev=tv/(1+wacc)**10/ev,claims=claims,price=(ev-claims)/shares)
cases={'prudente':calc(2450,.025,.25,.105,.02,.40,.30,100,35,10),'intermedio':calc(2500,.05,.275,.095,.025,.32,.25,90,30,5),'expansivo':calc(2600,.075,.30,.085,.03,.30,.22,85,30,0)}
lo,hi=0,.3
for _ in range(100):
 m=(lo+hi)/2
 if calc(2500,m,.275,.095,.025,.32,.25,90,30,5)['price']<price:lo=m
 else:hi=m
inv=calc(2500,(lo+hi)/2,.275,.095,.025,.32,.25,90,30,5)
assert abs(inv['price']-price)<1e-6
ke=.0486+1.10*.0441;kd=.0486+.012;dw=debt/(shares*price+debt);wa=ke*(1-dw)+kd*.79*dw
checks={k:sum(h[p][k] for p in ['Q42025','Q12026','Q22026','Q32026'])-t[k] for k in keys};assert max(abs(x) for x in checks.values())<1e-6
r=dict(asof='2026-11-08',history=h,quote={'date':'2026-11-06','price':price,'session':'NYSE regular close','quality':'secondary corroborated','scanner_date':'2026-10-21','scanner_price':75.33,'opportunity':80},bridge={'cash':cash,'debt':debt,'operating_cash_assumed':opcash,'pension_gross_deficits_2025_proxy':pension,'pension_surplus_not_added':44.785,'deferred_comp_2026':deferred,'insurance_cash_value_not_added':31.600,'contingent_consideration':contingent,'dividend_payable_sep25':dividend,'netclaims':claims,'basic_shares_oct7':160.375132,'diluted_q3_proxy':shares,'operating_leases_not_added':30.215,'acquisition_cash_cost_not_subtracted_again':461.985},capital_cost={'rf_nov6':.0486,'erp_nov1':.0441,'erp_source_riskfree':.0529,'parameter_dates_not_matched':True,'beta_assumed':1.1,'ke':ke,'kd_assumed':kd,'wacc_anchor':wa},proforma_valco={'9M2026_sales':1824.031,'9M2025_sales':1749.917,'9M2026_netincome':395.192,'9M2025_netincome':375.132,'Q32026_sales':611.271,'Q32025_sales':581.294,'Q32026_netincome':125.913,'Q32025_netincome':139.246,'not_cashflow':True},rd_coverage_sensitivity={str(f):calc(2500,.05,.275,.095,.025,.32,.25,90,30,5,rd_coverage=f)["price"] for f in [0,.25,.5]},conditional_cases=cases,inverse_growth=inv,checks=checks,approved_values=None,approved_price=None,entry_approved=False)
(P/'results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False))
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+keys);w.writeheader();w.writerows(dict(period=p,**v) for p,v in h.items())
print(json.dumps({'prices':{k:v['price'] for k,v in cases.items()},'inverse':inv['growth_years2to5'],'wacc':wa,'claims':claims,'ttm':t},indent=2))
