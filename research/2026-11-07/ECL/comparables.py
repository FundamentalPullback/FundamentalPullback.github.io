import json,pathlib,csv
p=pathlib.Path(__file__).parent
xs=[dict(ticker='ECL',price=300.68,shares=280.467785,debt=13192,cash=722.3,nci=30.6,sales=17372.3,ebit=2902.4,normalization=77.2,cfo=3029.2,capex=1234.1),dict(ticker='XYL',price=97.83,shares=229.334592,debt=2895,cash=708,nci=242,sales=9035+6662-6638,ebit=1223+1019-870,normalization=-49,cfo=1241+729-698,capex=331+268-248),dict(ticker='WTS',price=346.14,shares=27.462713+5.912640,debt=98.2,cash=444.8,nci=0,sales=2438.5+2168.4-1813.4,ebit=448.1+477.8-334.4,normalization=-39.3,cfo=402+278.9-247.3,capex=45.7+48.8-31.3)]
for x in xs:
 x['equity']=x['price']*x['shares'];x['ev_simple']=x['equity']+x['debt']+x['nci']-x['cash'];x['normalized_ebit']=x['ebit']+x['normalization'];x['ev_ebit']=x['ev_simple']/x['ebit'];x['ev_normalized_ebit']=x['ev_simple']/x['normalized_ebit'];x['normalized_margin']=x['normalized_ebit']/x['sales'];x['cash_yield_reported']=(x['cfo']-x['capex'])/x['equity']
json.dump({'asof':'2026-11-08','prices':'November 6 regular session secondary quotes','definition':'Simple EV=dated basic equity+book debt+NCI-cash; no pension, operating cash or operating lease adjustments. Not the DCF bridge. Normalization retains SBC, amortization and ongoing restructuring, removes tariff windfalls, adds only ECL identified acquisition/integration costs.','rows':xs},open(p/'comparables.json','w'),indent=2)
with open(p/'comparables.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(xs[0]));w.writeheader();w.writerows(xs)
print([(x['ticker'],x['ev_normalized_ebit'],x['normalized_margin']) for x in xs])
