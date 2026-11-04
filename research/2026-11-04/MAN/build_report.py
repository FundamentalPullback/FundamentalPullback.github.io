from pathlib import Path
import json
P=Path(__file__).parent
r=json.loads((P/'model/results.json').read_text());s=json.loads((P/'model/sensitivities.json').read_text());h=json.loads((P/'history/annual_3fy.json').read_text());q=json.loads((P/'history/latest_4q.json').read_text());t=json.loads((P/'history/ttm_comparison.json').read_text());c=json.loads((P/'comparables/outputs.json').read_text())
def n(v):return 'no divulgado' if v is None else f'{v:,.2f}'
def tab(rows,cols):
 out='| '+' | '.join(b for a,b in cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'
 for x in rows:out+='| '+' | '.join((f'{x[a]:.2%}' if a in ['discount','growth'] else n(x.get(a))) if isinstance(x.get(a),(float,int)) or x.get(a) is None else str(x.get(a)) for a,b in cols)+' |\n'
 return out+'\n'
a='\n## Tablas reproducibles\n\n### Historia 3FY, 4Q y TTM\n\n'
cols=[('period','Período'),('revenue','Ventas'),('ebit','EBIT GAAP'),('cfo','CFO'),('capex_including_software','Capex'),('fcf_cfo_less_total_capex','FCF calculado')]
a+=tab(h+q+t,cols)
a+='### Casos condicionados, no rango de valor total\n\n'
for k,v in r.items():
 p=v['assumptions'];a+=f"**{k}**: ingresos iniciales {p['firstRevenue']:,.0f}; margen antes de amortización adquirida {p['margins'][0]:.2%}→{p['margins'][-1]:.2%}; impuesto {p['tax']:.0%}; descuento {p['discount']:.1%}; crecimiento terminal {p['terminalGrowth']:.1%}; ROIC {p['roic']:.0%}. EV operativo {v['operatingEV']:,.2f}; puente seleccionado {v['selectedBridge']:,.2f}; residuo económico por acción-proxy {v['economicResidualPerShareProxy']:.2f}. "
 a+=('El residuo negativo expresa déficit del ejercicio; NO precio negativo ni acción valorada en cero.\n\n' if v['economicResidualPerShareProxy']<0 else 'No constituye valor total certificado.\n\n')
 a+=tab(v['rows'],[('year','Año'),('revenue','Ventas'),('ebitBeforeAcquiredAmort','EBIT sin amort. adquirida'),('selectedCashTax','Impuesto'),('physicalSoftwareDa','D&A residual'),('impliedGrossCapex','Capex financiado'),('workingCapitalGrowth','ΔWC'),('legacyWcFunding','WC heredado'),('fcff','FCFF')])
 a+=f"Terminal FCFF {v['terminal']['fcff']:,.2f}; reinversión {v['terminal']['netInvestment']:,.2f}; PV terminal {v['terminal']['pv']:,.2f}.\n\n"
a+='### Sensibilidades base\n\n'
for key,rows in s.items():
 if isinstance(rows,list):a+=f'**{key}**\n\n'+tab(rows,[(z,z) for z in rows[0]])
a+='### Inverso: exigencia económica, no plan financiado\n\n'
x=s['inverse'];y=s['inverseEfficiencyAlternative']
a+=f"Con el puente y ROIC central, justificar 46,94 exige elevar todos los márgenes {x['marginUplift']*100:.3f} puntos: {x['firstMargin']:.2%} inicial y {x['terminalMargin']:.2%} final; ventas año10 {x['year10Revenue']:,.0f}. El primer FCFF sería {x['firstFcff']:,.2f}, porque se financia la recuperación de beneficio a ROIC12%. Esa necesidad de fondos y su dilución no están certificadas: no es una recomendación ni trayectoria ejecutable.\n\n"
a+=f"La alternativa que atribuye recuperación de margen a eficiencia sin capital adicional exige {y['marginUplift']*100:.3f} puntos, márgenes {y['firstMargin']:.2%}/{y['terminalMargin']:.2%} y FCFF inicial {y['firstFcff']:,.2f}. Mantiene capex y circulante mínimos. La diferencia identifica dependencia del supuesto de financiación, no dos precios observados. Ambas raíces tienen bracket, residuo numérico y barrido monótono comprobados.\n\n"
a+='### Contraste relativo indicativo\n\n'+tab([dict(ticker=k,**v) for k,v in c.items()],[('ticker','Ticker'),('revenueTTM','Ventas TTM'),('ebitSelected','EBIT seleccionado'),('simpleEVExLeasesAndOtherClaims','EV simple'),('simpleEVtoEBIT','EV/EBIT')])
(P/'report.md').write_text((P/'report_body.md').read_text()+a)
