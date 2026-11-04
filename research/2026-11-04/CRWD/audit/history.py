import json,pathlib
P=pathlib.Path(__file__).parent
# USDm. FY26 10-K quarterly tables contain revised earnings; cash unchanged.
def cash(cfo,ppe,software,sbc,capsbc):return dict(CFO=cfo,cash_capex=ppe+software,FCF=cfo-ppe-software,SBC=sbc,capitalized_SBC=capsbc,economic_cash_diagnostic=cfo-ppe-software-sbc-capsbc)
fy25=dict(revenue=3953.624,EBIT=-116.400,NI_attributable=-15.241,**cash(1381.727,254.852,58.969,861.391,36.959))
fy26=dict(revenue=4812.005,EBIT=-293.292,NI_attributable=-162.502,**cash(1612.349,302.108,68.751,1096.679,56.956))
h124=dict(revenue=1884.908,EBIT=12.525+4.745,NI_attributable=45.880+40.629,**cash(709.869,88.937,24.995,384.002+(20.594-17.270),19.478))
h125=dict(revenue=2272.386,EBIT=-224.170,NI_attributable=-174.417,**cash(716.939,116.248,34.726,527.292,28.431))
h126=dict(revenue=2856.526,EBIT=-63.832,NI_attributable=33.080,**cash(1121.205,222.037,49.090,674.617,36.799))
a={k:fy25[k]+h125[k]-h124[k] for k in fy25};b={k:fy26[k]+h126[k]-h125[k] for k in fy26}
a.update(incident=60.062+75.383-5.132,commission_policy_effect=0);b.update(incident=117.730+3.600-75.383,commission_policy_effect=53.4)
for v in [a,b]:v['normalized_EBIT_same_policy_incident_excluded']=v['EBIT']-v['commission_policy_effect']+v['incident']
quarters=[dict(period='Q3 FY26',revenue=1234.244,EBIT=-62.222,NI_attributable=-26.776,CFO=1114.480-716.939,cash_capex=199.643+51.496-116.248-34.726),dict(period='Q4 FY26',revenue=1305.375,EBIT=-6.900,NI_attributable=38.691,CFO=1612.349-1114.480,cash_capex=302.108+68.751-199.643-51.496),dict(period='Q1 FY27',revenue=1385.629,EBIT=-30.600,NI_attributable=27.774,CFO=590.937,cash_capex=97.624+22.571),dict(period='Q2 FY27',revenue=1470.897,EBIT=-33.232,NI_attributable=5.306,CFO=1121.205-590.937,cash_capex=222.037+49.090-97.624-22.571)]
for q in quarters:q['FCF']=q['CFO']-q['cash_capex']
assert all(abs(sum(q[k] for q in quarters)-b[k])<1e-7 for k in ['revenue','EBIT','NI_attributable','CFO','cash_capex','FCF'])
r=json.loads((P/'stress_results.json').read_text());shares=1050.118022;net=3550.309;price=244.68;marketEV=price*shares-net
for v in r.values():
 inp=v['inputs'];tv=v['terminal_FCFF']/(inp['wacc']-inp['g']);lo=-.7;hi=.7
 for _ in range(150):
  z=(lo+hi)/2;pv=sum(row['FCFF']/(1+z)**row['year'] for row in v['rows'])+tv/(1+z)**10
  if pv>marketEV:lo=z
  else:hi=z
 v['implied_enterprise_return_at_price']=z
(P/'stress_results.json').write_text(json.dumps(r,indent=2));(P/'historical_bridge.json').write_text(json.dumps(dict(prior_TTM_July2025=a,current_TTM_July2026=b,quarters=quarters,source_periods=dict(FY25=fy25,FY26=fy26,H1July2024=h124,H1July2025=h125,H1July2026=h126),notes=['Revised H1 July 2024 SBC = original 384.002 + EBIT revision 3.324; no cash effect.','Economic cash diagnostic is CFO less capex less P&L and capitalized SBC; not full normalized FCFF.','Normalized EBIT restores four-year commission amortization and removes only specifically disclosed July incident costs; other adjustments retained.']),indent=2))
print(json.dumps(dict(prior=a,current=b,quarters=quarters,returns={k:round(v['implied_enterprise_return_at_price']*100,2) for k,v in r.items()}),indent=2))
