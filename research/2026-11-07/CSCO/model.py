import json,pathlib,csv
P=pathlib.Path(__file__).parent
keys=['revenue','ebit','net_income','cfo','capex','da_and_other','sbc']
raw={'FY2024':[53803,12181,10320,10880,670,2507,3074],'FY2025':[56654,11760,10180,14193,905,2811,3641],'FY2026':[63325,15368,13267,14177,1410,2540,3830],'Q1FY2026':[14883,3363,2860,3212,323,606,1055],'H1FY2026':[30232,7144,6035,5034,606,1265,1989],'9MFY2026':[46073,11104,9408,8791,1020,1902,2903],'9MFY2025':[41981,8673,7630,9959,688,2176,2693]}
h={p:dict(zip(keys,v)) for p,v in raw.items()}
for name,a,b in [('Q2FY2026','H1FY2026','Q1FY2026'),('Q3FY2026','9MFY2026','H1FY2026'),('Q4FY2026','FY2026','9MFY2026')]:h[name]={k:h[a][k]-h[b][k] for k in keys}
h['TTM_Jul2026']=h['FY2026'].copy();h['TTM_Jul2025']=h['FY2025'].copy()
for x in h.values():x['fcf_company']=x['cfo']-x['capex'];x['fcf_less_sbc_diagnostic']=x['fcf_company']-x['sbc']
price=93.85;shares=3987;cash=15918;operating_cash=.02*63325;debt_principal=23002+6700;tax_claim_proxy=2424
netclaims=debt_principal-(cash-operating_cash)+tax_claim_proxy
# Operating leases remain operating in margins/capex; no duplicate lease debt.
# R&D and SBC expensed. Intangible amortization addback exactly matched by a replacement cash reserve.
def calc(g1,gsteady,margin,wacc,gt=.025,roic=.18,wc=.25,physical_cap=.025,stress=0):
 rev=63325;prior_margin=15368/63325;pv=0;rows=[];ic=50285+29533-(15918-operating_cash)
 for y in range(1,11):
  g=g1 if y==1 else gsteady if y<=5 else gsteady+(gt-gsteady)*(y-5)/5
  nr=rev*(1+g);m=15368/63325+(margin-15368/63325)*min(y/3,1)
  eb=nr*m;nop=eb*.8;dphys=nr*.011;di=nr*(1863/63325);cap=nr*physical_cap;im=di
  nw=wc*(nr-rev);netrein=cap+im-dphys-di+nw
  # Supplement growth capital to a conservative incremental ROIC ceiling rather than free high growth.
  # Consistent current-NOPAT retention convention, including positive margin improvement.
  funded_growth=max(g,(1+g)*m/prior_margin-1)
  roicneed=max(0,nop*funded_growth/roic)
  extra=max(0,roicneed-netrein);netrein+=extra
  f=nop-netrein-(stress if y==1 else 0);pv+=f/(1+wacc)**y;ic+=netrein
  rows.append(dict(year=y,funded_profit_growth=funded_growth,revenue=nr,growth=g,ebit_margin=m,ebit=eb,nopat=nop,physical_da=dphys,intangible_amortization=di,physical_capex=cap,intangible_replacement=im,working_capital_investment=nw,additional_growth_investment=extra,net_reinvestment=netrein,fcff=f,invested_capital=ic,roic_on_ending_capital=nop/ic))
  rev=nr;prior_margin=m
 nr=rev*(1+gt);nop=nr*margin*.8;floor=nr*(physical_cap-.011)+wc*(nr-rev);reinv=max(nop*gt/roic,floor);tf=nop-reinv;tv=tf/(wacc-gt);ev=pv+tv/(1+wacc)**10;eq=ev-netclaims
 assert all(x['physical_capex']>=x['physical_da'] and x['intangible_replacement']>=x['intangible_amortization'] and x['net_reinvestment']>=0 for x in rows)
 return dict(price=eq/shares,enterprise_value=ev,equity_value=eq,net_claims=netclaims,wacc=wacc,g1=g1,growth_years2to5=gsteady,terminal_margin=margin,terminal_growth=gt,incremental_roic_ceiling=roic,working_capital_intensity=wc,physical_capex_ratio=physical_cap,terminal_physical_floor=floor,terminal_reinvestment=reinv,terminal_fcff=tf,terminal_weight=tv/(1+wacc)**10/ev,stress_cash_year1=stress,rows=rows)
cases={'prudente':calc(.08,.04,.24,.11,gt=.02,roic=.14,wc=.35,physical_cap=.028,stress=17165*.1),'intermedio':calc(72800/63325-1,.08,.26,.10),'expansivo':calc(.18,.13,.29,.09,gt=.03,roic=.22,wc=.2,physical_cap=.023)}
lo,hi=.0,.5
for _ in range(100):
 m=(lo+hi)/2
 if calc(72800/63325-1,m,.26,.10)['price']<price:lo=m
 else:hi=m
inverse=calc(72800/63325-1,(lo+hi)/2,.26,.10)
# Market-value weights, not book weights. Beta and debt spread assumptions explicitly analyst-selected.
ke=.0486+1.2*.0441;kd=.0486+.012;dw=debt_principal/(debt_principal+price*shares);wacc=ke*(1-dw)+kd*.8*dw
r=dict(as_of='2026-11-08',post_event=False,earnings_event='2026-11-12 16:30 America/New_York',event_gate='Revisar tras resultados antes de aprobar entrada; no autorización de atravesar evento',approved_values=None,approved_price=None,entry_approved=False,history=h,quote={'price':price,'date':'2026-11-06','session':'Nasdaq regular close 16:00 EST','source_quality':'secondary corroborated','historical_scanner_price':113.64,'historical_scanner_date':'2026-10-15'},bridge={'cash_and_marketable_investments':cash,'operating_cash':operating_cash,'principal_notes':23002,'commercial_paper_rounded':6700,'total_debt_book':29533,'tax_uncertain_timing_claim_proxy':tax_claim_proxy,'net_claims':netclaims,'shares_diluted_proxy':shares,'shares_basic_aug27':3942.586873,'operating_lease_liabilities_not_added':1652,'finance_receivables_remain_operating':8332,'nonmarketable_investments_not_added':True,'pension_incremental_adjustment':None,'pension_note':'No quantified separate funded deficit identified; not asserted zero liability'},cost_of_capital={'rf_10y_2026_11_06':.0486,'erp_2026_11_01':.0441,'erp_source_riskfree':.0529,'parameter_dates_not_matched':True,'beta_assumed':1.2,'ke':ke,'kd_assumed':kd,'debt_weight':dw,'wacc_anchor':wacc},conditional_cases=cases,inverse_growth_years2to5=inverse,normalization={'sbc_addback':False,'restructuring_addback':False,'rd_expensed':True,'tax_rate_assumed':.20,'physical_da_reference':700,'intangible_amortization_reference':1863,'intangible_replacement_matches_amortization':True,'no_tax_shield_in_perpetuity_without_replacement':True},quality_flags=['FY2024 contains only post-March18 Splunk; FY2025/26 full year','Latest reported TTM is full FY2026; Oct24 quarter ended but unpublished as of cut','GAAP margins keep SBC and R&D; not nonGAAP35% margins','Working capital includes financing/inventory/contract commissions needs; no perpetual free advances','Supply commitments not all added as debt; stress tests incremental cash loss','10year funded illustrative cases, not certified fair values','Pending primary postevent statements and current bridge rollforward'])
(P/'results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False))
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values())).keys()));w.writeheader();w.writerows({'period':p,**v} for p,v in h.items())
print(json.dumps({'cases':{k:v['price'] for k,v in cases.items()},'inverse_growth':inverse['growth_years2to5'],'wacc_anchor':wacc,'netclaims':netclaims},indent=2))
