"""Reproduce comparables primarios; USDm. Precio 2026-11-06, balances/acciones fechados."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# TTM = annual2025 +9M2026 -9M2025. NDSN fiscal Jul, IEX/GGG Sep.
inputs={
'GGG':dict(price=67.86,shares=160.375132,share_date='2026-10-07',balance_date='2026-09-25',ttm_date='2026-09-25',debt=104.479,cash=139.818,annual=[2236.604,624.797,683.591,45.669,107.433,34.333],nine_current=[1717.081,460.986,463.439,47.649,77.629,23.553],nine_prior=[1643.448,466.218,487.262,33.646,75.744,24.495]),
'NDSN':dict(price=309.86,shares=55.699366,share_date='2026-08-18',balance_date='2026-07-31',ttm_date='2026-07-31',debt=192+10+1529.005,cash=113.431,annual=[2791.687,711.725,719.175,58.060,150.523,18.944],nine_current=[2227.975,586.700,570.473,40.313,109.446,17.512],nine_prior=[2039.867,497.464,516.264,49.002,112.454,13.255]),
'IEX':dict(price=226.99,shares=73.452801,share_date='2026-10-23',balance_date='2026-09-30',ttm_date='2026-09-30',debt=1751.1+.4,cash=602.1,annual=[3457.5,699.3,680.4,63.6,75.8+130.7,27.3],nine_current=[2759.2,580.3,543.2,65.9,60.9+99.6,27.6],nine_prior=[2558.4,515.7,470.9,43.9,56.5+96.5,23.7])}
out=[]
for ticker,a in inputs.items():
 d={k:round(x+y-z,6) for k,x,y,z in zip(['sales','ebit','cfo','capex','da','cashflow_sbc_addback'],a['annual'],a['nine_current'],a['nine_prior'])}
 cap=a['price']*a['shares'];ev=cap+a['debt']-a['cash'];fcf=d['cfo']-d['capex'];ebitda=d['ebit']+d['da']
 out.append(dict(ticker=ticker,price_date='2026-11-06',**{k:v for k,v in a.items() if k not in ['annual','nine_current','nine_prior']},**d,market_cap=cap,simple_ev=ev,ebit_margin=d['ebit']/d['sales'],gaap_ebitda=ebitda,ev_sales=ev/d['sales'],ev_ebit=ev/d['ebit'],ev_gaap_ebitda=ev/ebitda,cfo_less_capex=fcf,cfo_less_capex_less_sbc=fcf-d['cashflow_sbc_addback'],equity_cash_yield=fcf/cap,equity_cash_yield_after_sbc=(fcf-d['cashflow_sbc_addback'])/cap))
normalization_9m={'GGG':{'reported_ebit':460.986,'acquisition_cost_addback':8.9,'tariff_refund_removed':9,'comparable_ebit':460.986+8.9-9,'sales':1717.081},'NDSN':{'reported_ebit':586.700,'acquisition_cost_addback':1.110,'inventory_stepup_addback':3.404,'comparable_ebit':586.700+1.110+3.404,'sales':2227.975},'IEX':{'reported_ebit':580.3,'legal_gain_removed':3.,'comparable_ebit':577.3,'sales':2759.2}}
for v in normalization_9m.values():v['margin']=v['comparable_ebit']/v['sales']
result=dict(normalization_9m=normalization_9m,asof='2026-11-08',inputs=inputs,definition='EV simple=precio Nov6 × acciones básicas del último cover + deuda contable − caja; excluye leases/pensiones/reserva operativa consistentemente. No es puenteDCF. EBITDA GAAP=EBIT+DA; SBC permanece gasto. CFO−capex es flujo tras intereses/impuestos, no FCFF. Sin normalización proforma adquisiciones.',rows=out)
(P/'comparables.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
with (P/'comparables.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for d in out:print(d['ticker'],{k:round(d[k],3) for k in ['market_cap','simple_ev','sales','ebit','ebit_margin','cfo_less_capex','ev_ebit','ev_gaap_ebitda','equity_cash_yield_after_sbc']})
