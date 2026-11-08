import json,csv, pathlib
P=pathlib.Path(__file__).parent
keys=['sales','ebit','netincome','cfo','capex_cash','da','sbc_expensed','sbc_capitalized','transaction','advertising_other','rd']
v={'FY2023':[3042,-2142,-1622,586,54,43,2756,56,2171,871,2312],'FY2024':[3378,489,457,687,64,56,300,35,2420,958,604],'FY2025':[3742,498,447,971,61,91,352,42,2677,1065,650],'9M2024':[2495,334,309,534,52,39,214,27,1804,691,449],'9M2025':[2750,401,366,788,49,65,253,33,1979,771,479],'9M2026':[3157,499,403,1085,46,97,341,31,2242,915,561],'Q12026':[1019,182,144,268,16,30,80,11,733,286,164],'H12026':[2062,325,256,762,29,62,221,21,1478,584,366]}
# 9M2024 capitalized SBC verified separately; all dollar amounts rounded issuer millions.
h={k:dict(zip(keys,a)) for k,a in v.items()}
def diff(a,b):return {k:h[a][k]-h[b][k] for k in keys}
h['Q42025']=diff('FY2025','9M2025');h['Q22026']=diff('H12026','Q12026');h['Q32026']=diff('9M2026','H12026')
for yr in ['2025','2026']:
 prev='FY2024' if yr=='2025' else 'FY2025';sub='9M2024' if yr=='2025' else '9M2025'
 h['TTM'+yr]={k:h[prev][k]+h['9M'+yr][k]-h[sub][k] for k in keys}
for a in h.values():a['fcf_reported']=a['cfo']-a['capex_cash'];a['fcf_after_sbc_proxy']=a['fcf_reported']-a['sbc_expensed']-a['sbc_capitalized']
with open(P/'financial_history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2025']));w.writeheader();w.writerows(dict(period=p,**a) for p,a in h.items())
price=58.12;shares=236.630090+4.417+5.010
cashbridge={'cash':830,'short_securities':97,'long_securities':8,'restricted_excluded':93,'operating_reserve':410,'legal_accrual':89,'indirect_taxes_current':30,'indirect_tax_long':18,'insurance_uncovered':4,'caper_cash':40,'financial_debt':0,'excess_net':344}
cases={'prudente':dict(sales1=4500,g=.05,gt=.02,margin=.15,margin1=.14,wacc=.12,renewal=1.25,growth_capital=.45,caper=50),'intermedio':dict(sales1=4650,g=.09,gt=.025,margin=.22,margin1=.17,wacc=.11,renewal=1.15,growth_capital=.35,caper=40),'favorable':dict(sales1=4800,g=.13,gt=.03,margin=.27,margin1=.20,wacc=.10,renewal=1.05,growth_capital=.30,caper=30)}
def run(c):
 rows=[];sales=4149
 for y in range(1,12):
  growth=c['g'] if y<=5 else c['g']+(c['gt']-c['g'])*min((y-5)/5,1)
  new=c['sales1'] if y==1 else sales*(1+growth);delta=new-sales
  margin=c['margin1']+(c['margin']-c['margin1'])*min((y-1)/5,1)
  ebit=new*margin;nopat=ebit*.77;da=new*123/4149
  renewal=da*c['renewal'];wc=.15*delta;growthfixed=(c['growth_capital']-.15)*delta
  fcff=nopat+da-renewal-wc-growthfixed
  rows.append(dict(year=y,sales=new,ebit=ebit,nopat=nopat,da=da,replacement_physical_software_intangibles=renewal,growth_wc=wc,growth_fixed_intangible=growthfixed,fcff=fcff,net_reinvestment=renewal-da+wc+growthfixed,rd_and_sbc_categories_overlap=True,expense_budget_verified=False,rd_expensed_reference=new*.17,sbc_expensed_reference=new*.10,incremental_roic_diagnostic=(nopat-(rows[-1]['nopat'] if rows else 596*.77))/(wc+growthfixed) if delta else None));sales=new
 pv=sum(r['fcff']/(1+c['wacc'])**r['year'] for r in rows[:10]);tv=rows[10]['fcff']/(c['wacc']-c['gt']);ptv=tv/(1+c['wacc'])**10;excess=344+40-c['caper'];ev=pv+ptv
 return dict(assumptions=c,years=rows,ev=ev,equity=ev+excess,price=(ev+excess)/shares,terminal_ev_weight=ptv/ev,net_excess_cash=excess)
out={k:run(v) for k,v in cases.items()}
a,b=0,.50
for _ in range(100):
 m=(a+b)/2;c=dict(cases['intermedio'],g=m)
 if run(c)['price']<price:a=m
 else:b=m
# Cash election, no automatic stock exposure or assumed probability. Illustrative time states.
event=[]
for t in [1,1.5,2]:
 pv=65/1.11**t;failure=out['intermedio']['price']
 event.append(dict(years=t,cash_offer=65,conditional_pv=pv,gross_spread=65/price-1,annualized_if_success=(65/price)**(1/t)-1,success_probability=None,price_minus_discounted_cash_offer=price-pv,failure_value_hypothesis=failure))
res=dict(asof='2026-11-08',price=price,price_date='2026-11-06 regular close secondary',shares_proxy=shares,history=h,cash_bridge=cashbridge,cases=out,inverse_growth_years2to5=(a+b)/2,event=event,approved_values=None,approved_price=None,entry_approved=False,cost_of_capital={'rf':.0486,'rf_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','erp_source_riskfree':.0529,'beta_assumed':1.4,'ke_anchor':.0486+1.4*.0441,'parameter_dates_not_matched':True},stage3_pass=False,stage3_5_pass=False)
json.dump(res,open(P/'results.json','w'),indent=2)
print({k:v['price'] for k,v in out.items()},'inverse',res['inverse_growth_years2to5'],'shares',shares)
res['sensitivity']=[{'wacc':w,'terminal_growth':g,'price':run(dict(cases['intermedio'],wacc=w,gt=g))['price']} for w in [.10,.11,.12] for g in [.02,.025,.03]]
res['share_sensitivity']={str(k):out['intermedio']['equity']/(shares*k) for k in [.95,1,1.05]}
res['event_mixed_at_current_dash_price']=48.75+.0843*179.67
res['tax_shield_full_book_upper_bound_per_share']=564/shares
json.dump(res,open(P/'results.json','w'),indent=2)
