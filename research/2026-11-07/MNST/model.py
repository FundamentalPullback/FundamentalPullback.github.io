"""MNST FCFF, USD millions, post-Aug2026 split. Analyst scenarios, not guidance.
Run: python model.py. Standard library only.
"""
import json, pathlib
OUT=pathlib.Path(__file__).parent
history={
 '2023':dict(revenue=7140.027,ebit=1953.355,net=1630.988,cfo=1717.753,capex=221.428,intangibles=13.296,da=68.898,sbc=68.836,diluted=2115.962),
 '2024':dict(revenue=7492.709,ebit=1930.294,net=1509.048,cfo=1928.533,capex=264.074,intangibles=42.360,da=80.434,sbc=90.985,diluted=2026.214),
 '2025':dict(revenue=8294.343,ebit=2419.354,net=1905.432,cfo=2098.177,capex=132.275,intangibles=25.254,da=114.441,sbc=125.687,diluted=1968.902),
 '9M2025':dict(revenue=6163.290,ebit=1876.720,net=1456.242,cfo=1718.762,capex=104.101,intangibles=19.681,da=82.023,sbc=86.664,diluted=1967.064),
 '9M2026':dict(revenue=7453.817,ebit=2189.118,net=1722.452,cfo=1670.835,capex=100.642,intangibles=9.342,da=89.887,sbc=94.284,diluted=1978.204)}
history['TTM2026']={k:history['2025'][k]-history['9M2025'][k]+history['9M2026'][k] for k in history['2025'] if k!='diluted'}
for k,adjustment in {'2023':43.036,'2024':135.282,'2025':50.440,'9M2025':2.279,'9M2026':19.904,'TTM2026':68.065}.items():
 history[k]['impairment_adjustment']=adjustment
 history[k]['ebit_ex_impairment']=history[k]['ebit']+adjustment
 history[k]['nopat_ex_impairment_25pct']=(history[k]['ebit']+adjustment)*.75
for h in history.values():
 h['fcf_cfo_less_ppe_intangibles']=h['cfo']-h['capex']-h['intangibles'];h['ebit_margin']=h['ebit']/h['revenue'];h['nopat_25pct']=h['ebit']*.75
R0=history['TTM2026']['revenue'];PRICE=45.72;SHARES=1980.113
# Current diluted shares retain vested option dilution; SBC remains in EBIT. No free future buybacks.
BRIDGE=dict(cash=2148.401,short_investments=1555.851,long_investments=927.011,operating_cash_reserve=500,financial_debt_proxy=5,other_claims=0)
EXCESS=sum(BRIDGE[k] for k in ['cash','short_investments','long_investments'])-BRIDGE['operating_cash_reserve']-BRIDGE['financial_debt_proxy']
CASES={
 'adverso':dict(growth=[.06,.05,.04,.035,.03],margins=[.27,.265,.26,.26,.26],terminal_margin=.25,wacc=.105,g=.025,roic=.15,capex=.025,da=.013,nwc=.22),
 'central':dict(growth=[.12,.10,.09,.08,.07],margins=[.29,.295,.30,.30,.30],terminal_margin=.29,wacc=.095,g=.03,roic=.20,capex=.023,da=.013,nwc=.20),
 'favorable':dict(growth=[.16,.14,.12,.10,.09],margins=[.30,.31,.32,.32,.32],terminal_margin=.31,wacc=.085,g=.035,roic=.25,capex=.023,da=.013,nwc=.18)}
def value(case='central',wacc=None,g=None,growth=None,margin_shift=0):
 p=dict(CASES[case]); w=p['wacc'] if wacc is None else wacc; g=p['g'] if g is None else g
 assert w>g and p['roic']>g
 gs=p['growth'] if growth is None else [growth]*5
 r=R0;rows=[];pv=0
 for t in range(1,11):
  a=max(0,(t-5)/5)
  gr=gs[t-1] if t<=5 else gs[-1]*(1-a)+g*a
  margin=(p['margins'][t-1] if t<=5 else p['margins'][-1]*(1-a)+p['terminal_margin']*a)+margin_shift
  prev=r;r*=1+gr;nopat=r*margin*.75;da=r*p['da'];dnwc=(r-prev)*p['nwc'];raw_reinv=r*(p['capex']-p['da'])+dnwc
  # Transition to coherent incremental terminal ROIC; residual net capex includes maturation reinvestment.
  reinv=raw_reinv if t<=5 else raw_reinv*(1-a)+nopat*g/p['roic']*a
  capex=da+reinv-dnwc;fcff=nopat-reinv;disc=fcff/(1+w)**t;pv+=disc
  rows.append(dict(year=t,growth=gr,revenue=r,ebit_margin=margin,ebit=r*margin,nopat=nopat,da=da,capex_and_intangibles=capex,delta_nwc=dnwc,reinvestment=reinv,fcff=fcff,pv=disc))
 n11=r*(1+g)*(p['terminal_margin']+margin_shift)*.75;tvfcff=n11*(1-g/p['roic']);tv=tvfcff/(w-g);pvt=tv/(1+w)**10;ev=pv+pvt
 return dict(price=(ev+EXCESS)/SHARES,ev=ev,equity=ev+EXCESS,bridge=EXCESS,pv_explicit=pv,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_fcff=tvfcff,terminal_reinvestment=n11*g/p['roic'],wacc=w,g=g,roic=p['roic'],rows=rows)
def solve(fn,target,lo,hi,increasing=True):
 for _ in range(100):
  mid=(lo+hi)/2
  if (fn(mid)<target)==increasing:lo=mid
  else:hi=mid
 return (lo+hi)/2
results={'as_of':'2026-11-07','price':PRICE,'price_timestamp':'2026-11-06T16:00:00-05:00','scanner_last':45.50,'shares':SHARES,'history':history,'bridge':BRIDGE,'assumptions':CASES,'scenarios':{k:value(k) for k in CASES},'sensitivity':[{'wacc':w,'g':g,'value':value(wacc=w,g=g)['price']} for w in [.085,.095,.105] for g in [.025,.03,.035]],'reverse':{'five_year_constant_growth':solve(lambda x:value(growth=x)['price'],PRICE,0,.5),'parallel_margin_shift':solve(lambda x:value(margin_shift=x)['price'],PRICE,-.1,.5),'implied_wacc':solve(lambda x:value(wacc=x)['price'],PRICE,.031,.20,False)}}
results['checks']={'fcff_identity':all(abs(r['fcff']-(r['nopat']+r['da']-r['capex_and_intangibles']-r['delta_nwc']))<1e-8 for x in results['scenarios'].values() for r in x['rows']),'terminal_reinvestment_positive':all(x['terminal_reinvestment']>0 for x in results['scenarios'].values()),'price_range_cent_immaterial':.01/PRICE,'approval':False}
# Audit supplementation: discrete quarters and previous TTM, SEC cash-flow definitions.
prior_9m=dict(revenue=5680.668,ebit=1549.070,net=1238.337,cfo=1466.832,capex=172.795,intangibles=21.473,da=59.822,sbc=68.793)
prior_ttm={k:history['2024'][k]-v+history['9M2025'][k] for k,v in prior_9m.items()}
prior_ttm['impairment_adjustment']=135.282-6.067+2.279
prior_ttm['ebit_ex_impairment']=prior_ttm['ebit']+prior_ttm['impairment_adjustment']
q1=dict(revenue=2353.291,ebit=729.958,net=569.485,cfo=604.986,capex=20.604,intangibles=3.531)
h1=dict(revenue=4890.764,ebit=1470.401,net=1154.025,cfo=1114.201,capex=69.031,intangibles=6.567)
quarters={'Q4_2025':{k:history['2025'][k]-history['9M2025'][k] for k in q1},'Q1_2026':q1,'Q2_2026':{k:h1[k]-q1[k] for k in q1},'Q3_2026':{k:history['9M2026'][k]-h1[k] for k in q1}}
for h in [prior_ttm,*quarters.values()]:
 h['fcf_cfo_less_ppe_intangibles']=h['cfo']-h['capex']-h['intangibles'];h['ebit_margin']=h['ebit']/h['revenue']
results['supplemental_history']={'prior_9m2024':prior_9m,'TTM2025':prior_ttm,'quarters':quarters,'note':'Q2 EBIT derived from 6M minus Q1 differs from release standalone by USD0.001m rounding; no valuation effect.'}
results['checks']['four_quarters_tie_to_ttm']=all(abs(sum(q[k] for q in quarters.values())-history['TTM2026'][k])<1e-8 for k in ['revenue','ebit','net','cfo','capex','intangibles'])
(OUT/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps({k:{s:round(v[s],4) for s in ['price','terminal_weight']} for k,v in results['scenarios'].items()},indent=2));print(results['reverse']);print(history['TTM2026']);print(results['checks'])
