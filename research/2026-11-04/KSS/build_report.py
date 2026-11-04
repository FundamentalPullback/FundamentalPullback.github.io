from pathlib import Path
import json
p=Path(__file__).resolve().parent
h=json.loads((p/'history/normalized_history.json').read_text())['periods'];r=json.loads((p/'model/results.json').read_text());i=json.loads((p/'model/inputs.json').read_text());sens=json.loads((p/'model/sensitivities.json').read_text());comps=json.loads((p/'comparables/results.json').read_text())
def f(x,n=1):return 'n/d' if x is None else f'{x:,.{n}f}'.replace(',','X').replace('.',',').replace('X','.')
lines=['| Período | Ventas totales | EBIT | NI | CFO | Capex | FCF | EPS diluido |','|---|---:|---:|---:|---:|---:|---:|---:|']
for period,a in h.items():
 if period.startswith('FY') or period.startswith('Q') or period.startswith('TTM'):
  lines.append('| '+period+' | '+' | '.join(f(a.get(k),2 if k=='eps_diluted' else 0) for k in ['revenue','ebit','net_income','cfo','capex','fcf_cfo_less_capex','eps_diluted'])+' |')
sc=['| Caso | Ventas año1 | Margen renta año1/final | ROIC marginal | Descuento / g | EV operativo | Residuo equity | Lectura por acción proxy |','|---|---:|---:|---:|---:|---:|---:|---|']
for name,a in r.items():
 c=i['cases'][name];sc.append(f'| {name} | {f(c["firstRevenue"],0)} | {f(c["margins"][0]*100)}/{f(c["margins"][-1]*100)}% | {f(c["marginalRoic"]*100)}% | {f(c["wacc"]*100)}/{f(c["terminalGrowth"]*100)}% | {f(a["operatingEvAfterFullRent"])} | {f(a["equityResidual"])} | '+('Déficit '+f(-a['equityResidualPerShare'],2)+'; no precio negativo' if a['equityResidual']<0 else f(a['equityResidualPerShare'],2)+' USD condicionado')+' |')
b=['| Año | Ventas | EBIT después renta | Impuesto | D&A residual | Capex bruto implícito | ΔWC | FCFF |','|---|---:|---:|---:|---:|---:|---:|---:|']
for a in r['base']['rows']:b.append('| '+str(a['year'])+' | '+' | '.join(f(a[k]) for k in ['revenue','ebitAfterRent','tax','residualDda','impliedGrossCapex','incrementalWc','fcff'])+' |')
st=['| Sensibilidad de base | Entradas | Resultados económicos por acción proxy |','|---|---|---|']
for a in sens:st.append('| '+a['parameter']+' | '+' / '.join(str(v['input']) for v in a['rows'])+' | '+' / '.join(f(v['equityResidualPerShare'],2) for v in a['rows'])+' |')
cp=['Contraste Q2 operativo, con IEEPA y partidas identificadas retiradas; no márgenes después de renta cash homogéneos:','| Compañía | Crecimiento ventas | EBIT ajustado parcial | EBIT previo comparable parcial | Margen actual parcial |','|---|---:|---:|---:|---:|']
for a in comps['operating']:cp.append('| '+a['ticker']+' | '+f(a['revenueGrowthPct'],2)+'% | '+f(a['normalizedEbitPartial'])+' | '+f(a['priorNormalizedEbitPartial'])+' | '+f(a['normalizedMarginPct'],2)+'% |')
cp+=['','URBN/Nuuly y ANF tienen modelos y mezcla distintos; no se traslada su margen a KSS. Las compras de ropa de alquiler Nuuly ya están en CFO y no se vuelven a deducir. Este contraste no cambia gestión de posiciones.','']
for a in comps['operating']:cp.append(a['ticker']+': '+a['source'])
cp+=['','Macy’s ofrece un contraste de departamento más cercano, también imperfecto. TTM al1 de agosto: ingresos22.781 M, operating income1.144 M; quitando ganancias de activos39 y acuerdo interchange328, y añadiendo cargos199, quedan976 M. Retirar95 M de IEEPA bruto da881 M, conservando gasto de reinversión financiado por ese reembolso: es sensibilidad, no normalización neta certificada. Cierres y perímetro tampoco son constantes.','',"Cierre Macy’s4nov25,69; acciones261,176646 millones de agosto, deuda financiera contable2.433 y caja1.294 dan EV sin leases7.848,6 M. Ratio indicativo frente881 M≈8,91x. No se homogeneizó renta cash TTM: no entra en mediana objetivo. KSS con la misma convención básica exleases y notas contables daEV "+f(comps['kssRelative']['evExAllLeasesBookNotes'])+' M; frenteEBIT496 da'+f(comps['kssRelative']['multipleBeforeFullCashRent'],2)+'x, pero frente347 después de toda renta da'+f(comps['kssRelative']['multipleAfterFullCashRent'],2)+'x. Cambiar la definición cambia la aparente baratura. No se concluye valor relativo con métricas desiguales.','', 'Macy’s fuentes: https://www.sec.gov/Archives/edgar/data/794367/000162828026061320/m-20260801.htm y https://s202.q4cdn.com/285121676/files/doc_financials/2025/ar/Macy-s-Inc-2025-Annual-Report.pdf y https://stockanalysis.com/stocks/m/history/ .','', 'No hay mediana de múltiplos aplicada como precio objetivo. La conciliación completa de rentas, capital y ajustes de pares sigue pendiente antes de certificar Stage3 integral.']
s=(p/'report_body.md').read_text()
for k,v in {'HISTORY_TABLE':lines,'SCENARIO_TABLE':sc,'BASE_TABLE':b,'SENSITIVITY_TABLE':st,'COMPARABLES':cp}.items():s=s.replace('{{'+k+'}}','\n'.join(v))
(p/'report.md').write_text(s)
