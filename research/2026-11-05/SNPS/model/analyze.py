from value import *
O=json.loads((P/'results.json').read_text());B=O['cases']['base'];w=B['wacc'];man={'constant_growth':.15,'margin':[.353,.38,.405,.425,.43]};tests={'management':calc(overrides=man),'management_wacc_minus50bp':calc(overrides={**man,'wacc':w-.005}),'management_moderate_stress':calc(overrides={'constant_growth':.13,'margin':[.333,.36,.385,.405,.41],'wacc':w+.005,'g':.025}),'no_strategic_investment':calc(overrides={'strategic':0}),'no_cash_reserve':B['value']+500/B['shares'],'q4_cash_rollforward_error500':500/B['shares'],'one_extra_diluted_million':(B['ev']+B['bridge'])/(B['shares']+1),'tax18':calc(overrides={'tax':.18}),'terminal_roic20':calc(overrides={'roic':.20}),'terminal_roic30':calc(overrides={'roic':.30})}
# A104 disclosed inputs replay. Historical value is conditional, not controlling.
def old(rate=.095,gr=[.12,.115,.10,.09,.08],marg=[.29,.30,.31,.315,.32],bridge=-6429.691,shares=193):
 rev=9715;pv=0
 for i in range(10):
  gg=gr[i] if i<5 else gr[-1]+(.03-gr[-1])*(i-4)/5;prior=rev;rev*=1+gg;mm=marg[min(i,4)];nop=rev*mm*.8;raw=rev*.01+(rev-prior)*.05;weight=0 if i<5 else (i-4)/5;net=raw*(1-weight)+nop*.03/.22*weight;fc=nop-net;pv+=fc/(1+rate)**(i+1)
 return (pv+fc*1.03/(rate-.03)/(1+rate)**10+bridge)/shares
migration=[('A104 replay (may differ timing)',old()),('WACC only',old(rate=w)),('Current bridge/shares',old(rate=w,bridge=B['bridge'],shares=B['shares'])),('New segment growth, old margins/reinvestment',old(rate=w,gr=[x['growth'] for x in B['rows'][:5]],bridge=B['bridge'],shares=B['shares'])),('New economic margin path, old reinvestment',old(rate=w,gr=[x['growth'] for x in B['rows'][:5]],marg=A['cases']['base']['margin'],bridge=B['bridge'],shares=B['shares'])),('Current full economic model',B['value'])]
out={'tests':{k:(v['value'] if isinstance(v,dict) else v) for k,v in tests.items()},'migration':migration,'forecast_year5_revenue':B['rows'][4]['revenue'],'forecast_year10_revenue':B['rows'][9]['revenue'],'base_cash_yield':B['rows'][0]['fcff']/(A['price']*B['shares']-B['bridge'])}
(P/'analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
