import json,csv,math,pathlib
P=pathlib.Path(__file__).parent
# USD millions. Analyst assumptions, not company guidance or verified intrinsic values.
A={'valuation_date':'2026-11-10','stub_years':51/365,'stub_fcff_assumed':0,'reference_price':261.56,'reference_price_status':'Nov10 scanner matched Stock Analysis regular close 16:00 EST; cross-provider discrepancies retained','shares_proxy':253.831,'cash':3943,'operating_cash_reserve':1000,'debt_principal':11039,'nci_economic_claim':1000,'earnout_credit':0,'base_revenue':10463+3850,'base_revenue_status':'9M actual plus Q4 guidance midpoint, not reported FY2026','risk_free':.0498,'erp_assumed':.05,'beta_assumed':1.25,'debt_cost_assumed':.06,'tax':.20,'jv_funding':[565+117,117,117,0,0,0,0,0,0,0],'jv_timing_status':'Conservative modeled 2027 VSMC565 plus ESMC351 evenly 2027-29; actual schedule only deadlines disclosed'}
# WACC calculated from scanner equity proxy and principal debt; no claim of estimated beta.
E=A['reference_price']*A['shares_proxy'];D=A['debt_principal'];A['calibrated_wacc']=(E*(A['risk_free']+A['beta_assumed']*A['erp_assumed'])+D*A['debt_cost_assumed']*(1-A['tax']))/(E+D)
S={'bear':{'growth':[-.05,.02,.03,.03,.03],'margin':[.26,.27,.275,.28,.28],'tax':.23,'sc':.9,'terminal_margin':.27,'terminal_roic':.12,'g':.02,'wacc':.115},'base':{'growth':[.08,.07,.06,.05,.05],'margin':[.31,.315,.32,.32,.32],'tax':.20,'sc':1.2,'terminal_margin':.30,'terminal_roic':.15,'g':.025,'wacc':A['calibrated_wacc']},'bull':{'growth':[.12,.10,.09,.08,.07],'margin':[.33,.34,.35,.35,.35],'tax':.19,'sc':1.5,'terminal_margin':.33,'terminal_roic':.18,'g':.03,'wacc':.09}}
def calc(s,w=None,g=None,growth_override=None):
 s=dict(s);w=s['wacc'] if w is None else w;g=s['g'] if g is None else g
 rows=[];r=A['base_revenue'];ic=12465+10978-3943 # reported equity incl NCI + debt carrying - cash; diagnostic
 for i in range(10):
  f=max(0,(i-4)/5);growth=(s['growth'][i] if i<5 else s['growth'][-1]*(1-f)+g*f)
  if growth_override is not None: growth=growth_override if i<5 else growth_override*(1-f)+g*f
  margin=s['margin'][i] if i<5 else s['margin'][-1]*(1-f)+s['terminal_margin']*f
  sc=s['sc']*(1-f)+(s['terminal_roic']/(s['terminal_margin']*(1-s['tax'])))*f
  new=r*(1+growth);ebit=new*margin;nopat=ebit*(1-s['tax']);da=new*.05;maintenance=da
  delta=max(new-r,0);nwc=delta*.16;jv=A['jv_funding'][i];budget=delta/sc;core=max(0,budget-nwc-jv)
  reinvest=nwc+jv+core;fcff=nopat+da-maintenance-reinvest;ic+=reinvest
  rows.append(dict(year=2027+i,revenue=new,growth=growth,margin=margin,ebit=ebit,tax=s['tax'],nopat=nopat,da=da,maintenance=maintenance,nwc=nwc,jv=jv,core_growth_capital=core,net_reinvestment=reinvest,fcff=fcff,pv=fcff/(1+w)**(i+1+A['stub_years']),sales_capital=sc,invested_capital_diagnostic=ic,roic_diagnostic=nopat/ic));r=new
 tn=rows[-1]['nopat']*(1+g);tr=tn*g/s['terminal_roic'];tfcf=tn-tr;tv=tfcf/(w-g);pvt=tv/(1+w)**(10+A['stub_years']);ev=sum(x['pv'] for x in rows)+pvt
 eq=ev+A['cash']-A['operating_cash_reserve']-A['debt_principal']-A['nci_economic_claim']
 return {'value_per_share':eq/A['shares_proxy'],'ev':ev,'equity':eq,'terminal_pv_share':pvt/ev,'terminal_fcff':tfcf,'terminal_reinvestment':tr,'terminal_roic':s['terminal_roic'],'wacc':w,'g':g,'rows':rows}
R={k:calc(s) for k,s in S.items()}
for k,v in R.items():
 with open(P/(k+'_forecast.csv'),'w') as f:
  wr=csv.DictWriter(f,fieldnames=v['rows'][0].keys());wr.writeheader();wr.writerows(v['rows'])
lo,hi=0,.4
for _ in range(100):
 mid=(lo+hi)/2
 if calc(S['base'],growth_override=mid)['value_per_share']<A['reference_price']:lo=mid
 else:hi=mid
reverse={'constant_growth_years1to5_required':mid,'revenue_year5':calc(S['base'],growth_override=mid)['rows'][4]['revenue'],'all_other_inputs':'base fixed; growth fades to terminal in years6-10'}
sensitivity=[{'wacc':w,'g':g,'value':calc(S['base'],w,g)['value_per_share']} for w in [.09,.10,.11,.12] for g in [.015,.025,.035]]
provider_wacc=(E*(A['risk_free']+1.86*A['erp_assumed'])+D*A['debt_cost_assumed']*(1-A['tax']))/(E+D)
provider_stress={'published_beta':1.86,'source':'https://stockanalysis.com/stocks/nxpi/statistics/','beta_definition':'provider 5-year; Yahoo snippet describes monthly; not independent regression','wacc':provider_wacc,'conditional_base_value':calc(S['base'],w=provider_wacc)['value_per_share']}
(P/'provider_beta_stress.json').write_text(json.dumps(provider_stress,indent=2))
result={'provider_beta_stress':provider_stress,'assumptions':A,'scenarios':R,'reverse':reverse,'sensitivity':sensitivity,'canonical':{'fair_value':None,'entry_price':None,'stage3_pass':False},'status':'conditional analyst model; independent audit and peer/quote/sharecount gates open'}
(P/'model_results.json').write_text(json.dumps(result,indent=2));(P/'assumptions.json').write_text(json.dumps({'common':A,'scenarios':S},indent=2))
print(json.dumps({'values':{k:round(v['value_per_share'],2) for k,v in R.items()},'wacc':A['calibrated_wacc'],'reverse':reverse,'terminal_share':{k:v['terminal_pv_share'] for k,v in R.items()}},indent=2))
assert sum(A['jv_funding'])==916
assert all(len(x['rows'])==10 for x in R.values())
assert all(abs(x['fcff']-(x['nopat']-x['net_reinvestment']))<1e-8 for v in R.values() for x in v['rows'])
