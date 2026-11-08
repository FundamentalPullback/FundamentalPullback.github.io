"""RPM: deterministic research support, USD million; no trading instruction.
Run python model.py. Sources and judgment separated in report.md/sources.json.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
# Primary statements, FY 2024/25/26; quarter FY27Q1 and FY26Q1.
fields=['sales','gross','sga','restruct','impairment','net','da','sbc','cfo','capex','shares']
annual={2024:[7335.277,3014.589,2113.585,30.008,0,588.397,171.251,25.925,1122.305,213.970,128.340],2025:[7372.644,3050.478,2150.537,24.979,11.352,688.688,193.840,27.042,768.190,229.930,128.204],2026:[7863.422,3258.225,2292.130,42.612,0,661.392,213.490,32.848,898.708,223.507,127.554]}
annual={str(k):dict(zip(fields,v)) for k,v in annual.items()}
q1=dict(zip(fields,[2215.593,913.962,559.768,5.157,0,256.357,53.075,9.601,263.936,58.505,127.240]))
oldq1=dict(zip(fields,[2113.743,893.216,573.534,8.814,0,227.605,51.464,5.475,237.510,62.461,127.950]))
oldoldq1=dict(zip(fields,[1968.789,836.673,526.146,7.202,0,227.692,46.185,6.226,248.059,50.742,None])) # FY25Q1 from FY26Q2 prior 6m less prior Q2, CF prior Q1 comparator.
q2=dict(zip(fields,[1909.895,780.167,549.465,4.531,0,161.207,103.507-51.464,14.574-5.475,583.209-237.510,111.797-62.461,127.649]))
q3=dict(zip(fields,[1607.949,634.816,533.872,19.855,0,51.364,155.798-103.507,24.459-14.574,656.672-583.209,159.639-111.797,127.507]))
q4={k:annual['2026'][k]-oldq1[k]-q2[k]-q3[k] for k in fields if k!='shares'};q4['shares']=None
quarters={'2026Q2':q2,'2026Q3':q3,'2026Q4':q4,'2027Q1':q1}
ttm={k:annual['2026'][k]+q1[k]-oldq1[k] for k in fields if k!='shares'}
prior={k:annual['2025'][k]+oldq1[k]-oldoldq1[k] for k in fields if k!='shares'}
def enrich(x):
 x['operating_ebit']=x['gross']-x['sga']-x['restruct']-x['impairment'];x['fcf_reported']=x['cfo']-x['capex'];x['fcf_after_sbc']=x['fcf_reported']-x['sbc'];return x
for x in list(annual.values())+list(quarters.values())+[ttm,prior]:enrich(x)
# Strip disposal and earnout gains, keep all restructuring/impairment/SBC.
base_sales=ttm['sales'];base_ebit=ttm['operating_ebit']-(14.418+4.945)-(6.093+10.505)
price=103.31;shares=127.53;debt=2406.525;cash=312.842;cash_floor=.02*base_sales
pension_claim=25.170+26.069;nci=1.509;earnout=.408
bridge=debt+pension_claim+nci+earnout-max(0,cash-cash_floor)
rf=.0529;erp=.0441;beta=1.02;kd=.0593;tax=.24
# Market equity, market-value debt disclosed Aug31; mixed-date capital weight sensitivity disclosed.
market_debt=2279.883;equity=price*shares;ke=rf+beta*erp
wacc=ke*equity/(equity+market_debt)+kd*(1-tax)*market_debt/(equity+market_debt)
CASES={'adverso':dict(growth=.02,margin=.115,terminal_margin=.11,g=.02,roic=.12),'central':dict(growth=.04,margin=.13,terminal_margin=.13,g=.025,roic=.15),'favorable':dict(growth=.055,margin=.145,terminal_margin=.14,g=.03,roic=.18)}
def model(c,w=wacc,save=False):
 sales=base_sales;op=base_ebit*(1-tax);rows=[];pv=0
 for y in range(1,11):
  transition=max(0,(y-5)/5);growth=c['growth']+(c['g']-c['growth'])*transition
  margin=(base_ebit/base_sales+(c['margin']-base_ebit/base_sales)*y/5) if y<=5 else c['margin']+(c['terminal_margin']-c['margin'])*transition
  prevsales=sales;sales*=1+growth;ebit=sales*margin;nopat=ebit*(1-tax)
  da=sales*.027;capex_floor=sales*.03;dnwc=(sales-prevsales)*.18
  growth_funding=max(0,(nopat-op)/c['roic']);rein=max(capex_floor-da+dnwc,growth_funding)
  capex=da+rein-dnwc;fcff=nopat+da-capex-dnwc;pv_cf=fcff/(1+w)**y;pv+=pv_cf
  rows.append(dict(year=y,sales=sales,growth=growth,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,dnwc=dnwc,reinvestment=rein,fcff=fcff,pv=pv_cf));op=nopat
 tv_sales=sales*(1+c['g']);tv_nopat=op*(1+c['g']);tv_rein=tv_nopat*c['g']/c['roic'];tv_da=tv_sales*.027;tv_dnwc=(tv_sales-sales)*.18;tv_capex=tv_da+tv_rein-tv_dnwc;tv_fcff=tv_nopat+tv_da-tv_capex-tv_dnwc;tv=(tv_nopat-tv_rein)/(w-c['g']);pvt=tv/(1+w)**10;ev=pv+pvt
 return dict(value=(ev-bridge)/shares,ev=ev,equity=ev-bridge,pv_flows=pv,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_nopat=tv_nopat,terminal_reinvestment=tv_rein,terminal_sales=tv_sales,terminal_da=tv_da,terminal_capex=tv_capex,terminal_dnwc=tv_dnwc,terminal_fcff=tv_fcff,rows=rows)
results={k:model(c) for k,c in CASES.items()}
def solve(param,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2;c=CASES['central'].copy();c[param]=mid
  if param=='margin':c['terminal_margin']=mid
  if model(c)['value']<price:lo=mid
  else:hi=mid
 return (lo+hi)/2
inverse={p:solve(p,*b) for p,b in {'growth':(-.01,.20),'margin':(.08,.30)}.items()}
sensitivity=[dict(wacc=w,g=g,value=model(dict(CASES['central'],g=g),w)['value']) for w in [wacc-.01,wacc,wacc+.01] for g in [.02,.025,.03]]
for name,r in results.items():
 with (P/f'forecast_{name}.csv').open('w') as f:
  wr=csv.DictWriter(f,fieldnames=r['rows'][0]);wr.writeheader();wr.writerows(r['rows'])
checks={'ten_years':all(len(r['rows'])==10 for r in results.values()),'fcff_identity':all(abs(x['nopat']+x['da']-x['capex']-x['dnwc']-x['fcff'])<1e-8 for r in results.values() for x in r['rows']),'terminal_funding':all(c['g']<wacc for c in CASES.values()),'quarter_tie':all(abs(sum(q[k] for q in quarters.values())-ttm[k])<1e-6 for k in ['sales','cfo','capex','net','da','sbc'])}
checks.update({'terminal_fcff_identity':all(abs(r['terminal_fcff']-(r['terminal_nopat']-r['terminal_reinvestment']))<1e-8 for r in results.values()),'capex_floor':all(x['capex']>=.03*x['sales']-1e-8 for r in results.values() for x in r['rows']),'terminal_capex_floor':all(r['terminal_capex']>=.03*r['terminal_sales']-1e-8 for r in results.values()),'scenario_order':results['adverso']['value']<results['central']['value']<results['favorable']['value'],'inverse_tie':all(abs(model(dict(CASES['central'],**({p:v,'terminal_margin':v} if p=='margin' else {p:v})))['value']-price)<1e-7 for p,v in inverse.items())})
assert all(checks.values()), checks
out=dict(price=price,price_at='2026-11-06T16:00:00-05:00',annual=annual,quarters=quarters,ttm=ttm,prior_ttm=prior,normalized_ebit=base_ebit,normalized_growth_vs_prior_operating=base_ebit/prior['operating_ebit']-1,capital=dict(rf=rf,erp=erp,beta=beta,kd=kd,ke=ke,wacc=wacc,market_debt=market_debt),bridge=dict(debt=debt,cash=cash,operating_cash_floor=cash_floor,pension=pension_claim,nci=nci,earnout=earnout,net_claim=bridge,shares=shares),assumptions=CASES,scenarios=results,inverse=inverse,sensitivity=sensitivity,checks=checks)
(P/'results.json').write_text(json.dumps(out,indent=2));(P/'run_log.json').write_text(json.dumps({'artifact':'deterministic_research_support','checks':checks,'status':'screen-grade','no_trade':True},indent=2))
print(json.dumps({k:{j:v for j,v in r.items() if j!='rows'} for k,r in results.items()},indent=2));print('WACC',wacc,'Inverse',inverse,'NormEBIT',base_ebit,'checks',checks)
