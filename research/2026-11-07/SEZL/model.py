"""Auditable historical cash bridge, USD millions. No approved valuation."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
# Annual statements and company releases archived alongside source register.
rows=[
['FY2023',159.356772,22.200401,7.098022,1.25/6,-25.690433,1.365592,None,6.933718,'10k24; CFO original includes notes receivable; not comparable to recast CFO'],
['FY2024',271.128,82.246,78.522,2.19,130.648,1.464,89.749,5.193,'10k25 recast; capex includes software'],
['FY2025',450.279,176.789,133.130,3.72,209.907,2.695,178.874,6.520,'10k25'],
['Q42024',98.223,30.871,25.367,.70,130.648-73.247,1.464-1.058,89.749-33.319,None,'fy25 release; CFO and credit cash derived FY24 minus 9M24 recast 10k25'],
['9M2025',320.410,121.542,90.439,2.55,139.274,2.103,83.656,5.180,'10q326 recast'],
['Q42025',129.869,55.247,42.691,1.21,209.907-139.274,2.695-2.103,178.874-83.656,6.520-5.180,'fy25 release; CF derived FY25 minus 9M25'],
['Q12026',135.539,69.036,51.303,1.47,88.978,1.089,21.404,1.321,'q126'],
['Q22026',149.683,54.961,40.765,1.17,141.226-88.978,2.329-1.089,77.931-21.404,3.434-1.321,'q226 CF minus Q1'],
['Q32026',166.503,64.251,47.825,1.38,227.930-141.226,3.259-2.329,142.332-77.931,6.355-3.434,'10q326 CF minus 6M26'],
['9M2026',451.725,188.248,139.893,4.02,227.930,3.259,142.332,6.355,'10q326']]
h={r[0]:dict(zip(['revenue','operating_income','net_income','diluted_eps','cfo','capex_and_software','net_loan_purchases','sbc','source'],r[1:])) for r in rows}
for label,parts in [('TTM2025',['Q42024','9M2025']),('TTM2026',['Q42025','9M2026'])]:
 h[label]={k:sum(h[p][k] for p in parts) if all(h[p][k] is not None for p in parts) else None for k in list(h['FY2025'])[:-1]};h[label]['source']=' + '.join(parts)+'; EPS sum is approximation, not pooled-share EPS'
for r in h.values():
 r['naive_cfo_minus_capex']=r['cfo']-r['capex_and_software'];r['cash_after_credit_before_financing']=None if r['net_loan_purchases'] is None else r['cfo']-r['capex_and_software']-r['net_loan_purchases']
price=149.43
results={'ticker':'SEZL','asOf':'2026-11-08','price':price,'priceSession':'2026-11-06 16:00 America/New_York regular close','history':h,'method':'FCFE financiero con balance crediticio explícito; diseño sin valoración aprobada','valuationApproved':False,'approvedValue':None,'entryApproved':False,'q3_normalized_net_income_illustrative':47.825-1.999-3.7*(1-.249),'normalization_note':'Retira beneficio fiscal discreto e incentivo de red; conserva SBC y proyectos estratégicos como costes. No es FCFE.','credit':{'amortized_notes':355.529,'allowance':39.611,'net_notes':315.918,'begin_allowance_9m':28.505,'provision_9m':81.949,'gross_chargeoffs_9m':78.441,'recoveries_9m':7.598,'net_chargeoffs_9m':78.441-7.598,'reserve_rollforward_residual':28.505+81.949-78.441+7.598-39.611,'past_due_29_to_90_pct':(14.749+14.986)/355.529*100,'past_due_29_to_90_fy25_pct':(8.274+9.841)/283.4*100,'delinquency_definition':'Saldo de cuentas a cobrar a coste amortizado con mora de 29–90 días dividido entre saldo total a coste amortizado; no incidencia por prestatario','allowance_pct':39.611/355.529*100},'capital':{'cash_unrestricted_accounting':70.142,'cash_in_vie':19.610,'cash_outside_vie_before_other_needs':70.142-19.610,'restricted_cash':37.722,'facility_principal':104,'facility_limit':300,'minimum_draw':50,'book_equity':277.679,'shares_outstanding_m':33.783402,'q3_diluted_shares_m':34.753,'purchase_commitments_carrying':27.8,'purchase_commitments_order_value':36.1,'market_cap':price*33.783402,'cash_bridge_9m_after_credit_capex_debt_fees':227.930-142.332-3.259+135-172.260-1.163},'valuation_context':{'pe_ttm_quarterly_eps':price/(1.21+4.02),'pe_company_2027_adjusted_eps':price/7.2,'note':'Múltiplos de contexto. Guidance no es flujo distribuible ni valor intrínseco.'},'scenario_design':{'adverso':'Más pérdidas maduras, menor anticipo de garantía, presión sobre comisiones y mayores necesidades de capital.','central':'Separar cartera propia y retenida por WebBank, sin asumir desaparecen riesgos ni costes.','favorable':'Crecimiento rentable y financiación más barata; no anticipar licencia bancaria ni capital gratuito.'},'blocked_model_outputs':['FCFE normalizado prospectivo','valor central y rango','sensibilidad de valoración','valoración inversa','entrada y tamaño']}
assert abs(results['credit']['reserve_rollforward_residual'])<1e-9
assert abs(sum(h[p]['revenue'] for p in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026']['revenue'])<1e-9
(P/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2025']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(json.dumps({k:results[k] for k in ['credit','capital','valuation_context']},indent=2));print('TTM',h['TTM2025'],h['TTM2026'])
