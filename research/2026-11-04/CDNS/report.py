from pathlib import Path
import json
P=Path(__file__).parent;F=json.load(open(P/'financials.json'));M=json.load(open(P/'model.json'));U=json.load(open(P/'sources/urls.json'));U.update(price='https://stockanalysis.com/stocks/cdns/history/',price_check='https://www.marketbeat.com/stocks/NASDAQ/CDNS/',rf='https://www.federalreserve.gov/releases/h15/',calendar='https://investor.cadence.com/overview/',regulator='https://www.reginfo.gov/public/do/eAgendaViewRule?RIN=0694-AK34&operation=OPERATION_PRINT_RULE&pubId=202510')
json.dump(U,open(P/'sources.json','w'),indent=2)
def links(*keys):return '\n\nFuentes: '+', '.join(f'[{k}]({U[k]})' for k in keys)+'.\n\n'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(str(v) for v in r)+' |\n' for r in rows)+'\n'
def hist(group):return table(['Periodo','Ventas','EBIT','Neto','EPS diluido','CFO','Capex PPE','FCF','SBC','FCF−SBC'],[[d['period']]+[f'{d[k]:,.2f}' for k in ['revenue','ebit','net_income','diluted_eps','cfo','capex','fcf','sbc','fcf_less_sbc']] for d in F[group]])
s='''# CDNS: migración de valoración, no una señal de compra

**4 noviembre 2026 · Nasdaq · USD. Precio de referencia: 323,75 USD, cierre regular del 3 noviembre a las 16:00 EST. Corte de investigación: 4 noviembre, 15:20 UTC.**

## Decisión y alcance

**Mantener espera de precio.** El FCFF central da **140,72 USD**, el adverso **80,44** y el favorable **256,36**. El cierre excede incluso este favorable. Estos son escenarios propios, no consenso, techo de compra ni garantía. Ninguna entrada Stage 3.5 está aprobada.

Se completa una migración metodológica pendiente desde el FCFE simplificado de A106 (27 octubre) al FCFF canónico de diez años del plan de 30 octubre. No se presenta el mismo resultado del 26 octubre como novedad. Se conserva el histórico A106: 87,57 / 150,68 / 271,08. Su central se reproduce exactamente a redondeo con la fórmula publicada: 150,68386 USD.

Nivel de evidencia: alto para estados publicados, medio para proyección. **Modelo de investigación, no valoración transaccional certificada.** El perímetro incluye Hexagon D&E desde su adquisición; la contabilidad de compra aún es provisional. Falta un comparable sectorial plenamente homogéneo y no se ha aprobado elegibilidad técnica, calendario de entrada, stop o tamaño. No se sustituye esta falta por un múltiplo de un proveedor ni por un descuento fijo del 15%.
'''+links('price','price_check','q3','q10')+'''## 1. Negocio y calidad: crecimiento real, mezcla menos simple

Cadence provee software y sistemas de diseño de semiconductores, IP y simulación de sistemas. El coste de cambiar flujos de diseño y su integración con clientes y foundries apoyan la continuidad comercial, pero no constituyen una garantía de rentabilidad ni una cuota de mercado calculada en este informe.

Q3: Core EDA crece 20%, IP 24% y System Design & Analysis 30%. La distribución de ventas es aproximadamente 69% / 15% / 16%. El backlog alcanza 8.200 M$ y las obligaciones de desempeño a reconocer en doce meses 4.200 M$. Son visibilidad comercial, no caja inmediata. El 79% de ingresos trimestrales se clasifica recurrente frente al 82% un año antes; crecimiento de ingresos recurrentes de 18% no significa retención neta de clientes de 118%.

La fortaleza de IA y mayor complejidad de chips explica demanda potencial; las afirmaciones de rendimiento de nuevos agentes son de la dirección, no retornos financieros auditados. Hardware, ventas upfront y adquisiciones modifican la mezcla y el calendario de cobro.
'''+links('q3','q3cfo','q10')+'''## 2. Tres ejercicios, cuatro trimestres y TTM comparable

Millones de USD excepto EPS. Años naturales; TTM al 30 septiembre. Q4 = FY menos nueve meses, Q2/Q3 de flujos = acumulado menos anterior. EPS Q4 y TTM por diferencias/suma puede diferir de un cálculo con acciones medias de todo el periodo. Se conserva el detalle y las fórmulas de extracción, no se rellenan datos faltantes con cero.

### Tres ejercicios completos
'''+hist('annual')+'''### Últimos cuatro trimestres
'''+hist('quarters')+'''### TTM frente a TTM anterior
'''+hist('ttm')+'''
Las ventas TTM aumentan 17,64%, EBIT 19,39%, beneficio neto 30,13%, FCF 19,28% y FCF menos SBC 18,50%. El margen EBIT pasa de 28,50% a 28,92%. La mejora existe, pero no es todo orgánico ni toda recurrente.

El último trimestre es menos fuerte en beneficio que el TTM: ventas +22,0%, EBIT 428,716 frente a 425,390 M$ (+0,78%), neto 289,747 frente a 287,122 (+0,91%) y EPS 1,05 sin crecimiento. El margen GAAP cae de 31,8% a 26,2%; el no GAAP de 47,6% a 44,1%. No usar crecimiento TTM para ocultar esta compresión.
'''+links('k25','priorq3','q1','q2','q10')+'''## 3. Normalización del beneficio, SBC y perímetro

**Base de comparación regulatoria.** El TTM anterior incluye 128,545 M$ de pérdida por contingencia, que desaparece en el TTM actual. Al añadirla únicamente al EBIT anterior como sensibilidad de comparabilidad, el crecimiento EBIT baja de 19,39% a **9,89%**. No se presenta la contingencia como coste que nunca volverá: las obligaciones regulatorias siguen siendo un riesgo.

**Hexagon D&E.** La adquisición se cerró el 23 febrero 2026. El precio de compra bruto fue 3.123,931 M$, aproximadamente 3.000 M$ neto de efectivo adquirido de 154,6 M$: unos 2.200 M$ en efectivo y 3,2 millones de acciones valoradas en 902,2 M$. No volver a restar ese precio ya pagado del puente de septiembre. La emisión ya está incorporada en las acciones; no volver a cargarla como dilución adicional sin conciliación.

La nota 2 ofrece proforma combinado: Q3 ventas 1.633,311 frente a 1.397,562 M$ (+16,87%) y neto 289,747 frente a 265,519 (+9,12%). Nueve meses proforma ventas 4.755,577 frente a 4.073,228 (+16,75%). Esto aproxima el mismo perímetro, pero **no es crecimiento orgánico auditado**: incluye ajustes de financiación, intangibles, contratos, acciones y transacción. Se mantiene separado del TTM contable.

**SBC no gratis.** TTM SBC es 543 M$, 8,85% de ventas y 30,79% del FCF. El flujo tras SBC de 1.220,636 M$ es una aproximación al coste económico, no FCFF ni FCFE formal. Se retiene SBC en los márgenes proyectados y no se descuenta una segunda vez en el FCFF. Las recompras no crean valor por sí mismas: en nueve meses 800,025 M$ de recompras y 195,608 M$ de impuestos de premios consumieron efectivo. La autorización extra de 2.500 M$ no equivale a ejecución.

**No confundir addbacks.** Q3 el neto ajustado 582,187 M$ elimina SBC 144,763, amortización adquirida 79,870, adquisición/integración 25,031 y reestructuración 42,159 M$, entre otros ajustes. El modelo no sustituye el margen GAAP por el 44,1% ajustado. Reestructuración e integración reaparecen; no se eliminan todas como extraordinarias. Ganancias de inversión y divestituras TTM de 135,565 M$ tampoco se extrapolan como operación recurrente.

**Impuestos.** El 24% normalizado del modelo es un supuesto favorable, heredado de la reconstrucción para visibilizar su efecto, inferior a la tasa GAAP FY2025 de 27,1% y Q3 de 29,0%. Al imponer 27% el central baja a 134,76 USD; a 29% a 130,79. No se declara sostenible el beneficio fiscal implícito sin nuevas pruebas.
'''+links('q10','q3','k25')+'''## 4. Caja, deuda y reclamaciones

Caja septiembre: 1.452,020 M$. Deuda contractual: 2.500 M$ de bonos más 150 M$ de revolver = **2.650 M$**. Valor contable de deuda 2.633,242 M$: el descuento/costes no extingue obligación contractual de 16,758 M$. Vence un bono de 500 M$ en septiembre 2027 (4,2%); otros 1.000 en 2029 (4,3%) y 1.000 en 2034 (4,7%). El revolver vence agosto 2029, variable, y no se valora capacidad sin usar como caja.

Reserva operativa **estimada** 500 M$, no efectivo restringido informado: caja excedente 952,020 y puente a equity **−1.697,980 M$**. Reservas de 0/500/1.000 M$ cambian el valor sin alterar la operación; no se trata toda la caja como libre automáticamente. No se añaden inversiones estratégicas ni activos de compensación diferida como efectivo líquido. Los arrendamientos siguen como gasto operativo y no se resta su pasivo por segunda vez. No se ha identificado en esta revisión una reclamación adicional cuantificada que deba añadirse al puente; esta afirmación no certifica que toda contingencia futura sea cero.

CFO nueve meses 1.414,436 M$: inventarios absorben 172,927 M$, cuentas a cobrar 84,285 y cuentas a pagar/acumulaciones 263,024; anticipos/deferred revenue aportan 148,835. FCF publicado excluye 6,975 M$ de compras de intangibles y 2.143,429 M$ de adquisiciones netas de caja, además de inversión en valores. Por ello no equivale al efectivo distribuible después de adquirir crecimiento.
'''+links('q10')+'''## 5. FCFF reproducible y supuestos

FCFF = NOPAT − reinversión modelada. En años 1–5, reinversión = capex − D&A de mantenimiento + ΔNWC; en años 6–10 se aplica la transición descrita hacia NOPAT×g/ROIC. EV = suma de diez flujos descontados + terminal descontado. Equity = EV + caja excedente − deuda nominal. Precio por acción usa **275,278 M**, último promedio diluido trimestral, no garantía de dilución futura. No se supone emisión o recompra gratuita; si cambia capital, hay que rehacer el puente.

Base de ingresos de proyección: punto medio de guidance FY2026, **6.402 M$**, no el TTM de 6.132,096. Año 1 es FY2027 aproximado, 7.362,3 M$ con 15% de crecimiento. Se usa descuento de fin de año estándar, no modelo stub preciso desde noviembre; desplazar los flujos dos meses adicionales reduce central a 138,38 USD. No es la previsión oficial de 2027.

- Primeros cinco años: crecimiento 15%; margen EBIT parte de 28,7% (centro de guidance FY2026) y converge a 33% en año 5. Año 1 es 29,56%. La expansión incorpora exigencia de rentabilidad después de SBC y costes recurrentes, no añade SBC al flujo.
- Años 6–10: crecimiento cae linealmente desde 15% a 3%; margen pasa de 33% a 34%.
- D&A económica de mantenimiento 2% de ingresos, capex normalizado 3,5%, ΔNWC 5% de ventas incrementales. Los porcentajes son supuestos, no guidance. D&A total TTM es 384,718 M$ (6,27% de ingresos), pero **no se añade todo**: la diferencia incluye amortización adquirida y un ajuste prudencial adicional, conservados como reserva económica de renovación del negocio. La amortización adquirida TTM es 240,970 M$; D&A residual es 143,748 M$ (2,344% de ventas), frente al addback modelado 122,642 M$ (2%). La reserva implícita de 262,076 M$ incluye por tanto 21,106 M$ adicionales; no procede atribuirla toda a amortización adquirida. Esta retención es conservadora y puede duplicar inversión cubierta por R&D; es una decisión explícita, no una identidad contable. El 3,5% de capex se contrasta con 3,33% de PPE TTM más intangibles.
- Reinversión explícita = capex − D&A + ΔNWC. En años 6–10 se mezcla progresivamente al 20/40/60/80/100% con reinversión sostenible NOPAT×g/ROIC. Así, año 10 ya cumple la tasa terminal; no aparece inversión por primera vez en año 11.
- Terminal: g 3%, ROIC incremental 25%, reinversión 12% de NOPAT; FCFF terminal NOPAT×(1−g/ROIC). El ROIC es supuesto prospectivo, no ROIC histórico auditado.
- WACC **10,1%**: Treasury10y 4,91% observado 2 noviembre (H.15 publicado 3 noviembre); beta supuesto 1,2 y prima equity supuesta 4,5% dan Ke 10,31%. Pesos objetivo aproximados 97% equity/3% deuda, deuda marginal supuesta 5%, impuesto24%: 10,1147%, redondeado10,1%. Beta, prima y coste marginal no son observaciones de mercado certificadas.

El 15% de crecimiento durante cinco años es ambicioso frente al proforma reciente de 16,9% que ya incorpora compra. No se financian futuras adquisiciones sin coste; si crecer exigiera nuevas compras materiales, habría que restar inversión/emitir capital. No se trata el crecimiento comprado pasado como prueba de crecimiento orgánico futuro.
'''+links('q3','q10','rf')+'''### Proyección central, millones de USD
'''+table(['Año','Ingresos','EBIT %','NOPAT','Reinversión total','FCFF'],[[d['year'],f"{d['revenue']:,.1f}",f"{d['ebit_margin']*100:.2f}%",f"{d['nopat']:,.1f}",f"{d['reinvestment']:,.1f}",f"{d['fcff']:,.1f}"] for d in M['cases']['base']['rows']])+'''## 6. Escenarios y valoración inversa
'''+table(['Escenario','Valor USD','Peso terminal EV','Supuestos'],[[k,f"{v['value']:.2f}",f"{v['terminal_weight']*100:.1f}%",f"crecimiento inicial {v['assumptions']['growth']*100:.0f}%; margen año5 {v['assumptions']['margin_year5']*100:.1f}%, terminal {v['assumptions']['margin_terminal']*100:.1f}%; WACC {v['assumptions']['wacc']*100:.1f}%; g {v['assumptions']['g']*100:.1f}%; ROIC {v['assumptions']['roic']*100:.0f}%"] for k,v in M['cases'].items()])+'''
El terminal representa 58,28% del EV central. No se etiqueta el favorable como techo comprado o precio justo asegurado. Los resultados varían por supuestos, no por redondeo al centavo.

Para justificar 323,75 con el resto central, el crecimiento de los primeros cinco años tendría que ser **30,56% anual**, manteniendo después la transición a 3%. Alternativamente, el margen EBIT de año5 tendría que alcanzar **77,18%** y el terminal 78,18%, con la senda de crecimiento central. La segunda solución es una prueba algebraica económicamente extrema, **no una previsión viable**. No basta decir “IA” para validar estas exigencias.

Sensibilidad WACC/g (ROIC25%, resto central):
'''+table(['WACC','g','Valor USD'],[[f"{d['wacc']*100:.1f}%",f"{d['g']*100:.1f}%",f"{d['value']:.2f}"] for d in M['sensitivity']])+'''## 7. Puente con A106: preservar historia y separar causas

El modelo antiguo usaba ingresos6402, crecimiento15% cinco años, margen FCFE20→25% interpolado desde año1, Ke10,5%, g3% y275,278M acciones. Su valor150,68386 reproduce150,68. Su precio era343,08 (27oct); el actual323,75 es5,63% menor. Cambiar el precio modifica el margen frente al valor, **no el DCF**.

La siguiente escalera no pretende que FCFE+deuda sea intercambiable sin hipótesis: el desendeudamiento usa coste financiero neto normalizado supuesto de90 M$ antes de impuestos (130 de intereses menos40 de rendimientos),76% después de impuestos, constante. Se conserva ese supuesto para aislar el efecto; el modelo final usa EBIT, no intereses proyectados. La deducción terminal del12% sobre la caja antigua es solo un diagnóstico intermedio, no la fórmula FCFF final sobre NOPAT.
'''+table(['Paso controlado','Valor USD'],[[n,f'{v:.5f}'] for n,v in M['bridge']])+'''
Método: FCFE/Ke pasa a FCFF/WACC y puente de claims. Hipótesis: EBIT, D&A económica, capex, circulante y reinversión/ROIC terminal se hacen explícitos. Datos operativos: siguen los del trimestre septiembre publicado26oct. Precio: se actualiza por separado. No se atribuye el descenso de valor a una caída nueva del negocio ni se sobrescribe A106.

## 8. Múltiplos de control y límites de comparabilidad

A323,75, capitalización aproximada usando promedio diluido89.121,253 M$: P/FCF73? **P/FCF es50,53x y P/(FCF−SBC)73,01x**. EV ajustado con la misma reserva/deuda90.819,233 M$, EV/EBITTTM51,20x. El PER sobre guía GAAP2026media4,87 es66,48x; sobre8,40ajustado38,54x. Son métricas distintas y no se promedian. El ajustado elimina SBC y otros costes: no justifica un múltiplo reducido equivalente a “barato”.

La continuidad temporal comparable dentro de Cadence muestra que el proxy de caja tras SBC creció18,50%, mientras el precio actual todavía exige un múltiplo alto. Para históricos de PER al cierre fiscal, usar EPS anual conocido después produce sesgo retrospectivo: no se usa como múltiplo ejecutable en esa fecha.

Synopsys sería el comparable industrial natural, pero Ansys cambia radicalmente perímetro, deuda y amortización, y su año fiscal no coincide. El contraste antiguo de EPS forward ajustados de fechas distintas no se conserva como prueba homogénea. WDAY y CRM son software empresarial, no sustitutos industriales de EDA. **No se asigna valor por múltiplos sectoriales mientras no exista un puente homogéneo.** Este límite queda abierto, aunque no cambia el rechazo de entrada a un precio superior a todos los escenarios de esta migración.

## 9. Riesgos, calendario y siguiente evidencia

- Demanda: presupuestos de semiconductores, hiperescaladores y China; backlog no elimina cancelaciones, retrasos ni presión competitiva.
- Margen: hardware/upfront, amortización adquirida, integración y costes de personal; Q3 ya comprime margen.
- Capital: compra de crecimiento, capex/circulante, dilución y recompras. El valor de activos intangibles y goodwill no es caja libre.
- Regulación: exposición China16% de ventasQ3 y obligaciones DOJ/BIS de2025. El 10-Q fechado27oct indicaba que la suspensión de la regla de afiliadas llegaba hasta9nov y que una extensión política aún no estaba formalizada por BIS. La consulta actual encuentra relatos secundarios contradictorios sobre extensión, sin resolver aquí un texto primario posterior: **no se afirma cuál será su vigencia futura ni se convierte una noticia en mejora del modelo**. Confirmar publicación oficial antes de una entrada.
- Calendario: último resultado confirmado26oct. No se dispone aquí de anuncio primario de próxima fecha anual; no se deduce aprobación del veto de la semana2–6nov ni de Stage3.5 solo por haber analizadoQ3.

Prueba que reforzaría tesis: expansión persistente de EBIT después de SBC, ingresos y caja comparable del perímetro combinado, conversión del backlog sin acumulación excesiva de inventario. La debilitaría: crecimiento dependiente de adquisiciones sin retornos, margen ajustado subiendo pero económico cayendo, nueva restricción comercial material o caja inferior tras inversión necesaria.

Siguiente paso: cerrar comparables, términos finales de PPA, calendario y normativa vigente, y contrastar guidance con próximo resultado. Solo si precio y valor central fueran compatibles se revisarían estructura técnica, tendencia larga, liquidez, stop y tamaño. No se crea orden ni posición con este informe.
'''+links('q10','q3cfo','calendar','regulator')
s=s.replace('P/FCF73? **P/FCF','**P/FCF')
pros_es=['Ingresos TTM +17,64% y FCF menos SBC +18,50%, reconciliados a estados primarios.','Backlog de 8.200 M$ y 79% de ingresos trimestrales recurrentes apoyan visibilidad, no garantizan caja.','El proforma de Hexagon muestra crecimiento Q3 de ventas de 16,87% con perímetro más comparable.']
cons_es=['El cierre de 323,75 USD supera el central de 140,72 y el favorable de 256,36; no hay entrada aprobada.','Q3 EBIT crece solo 0,78% y el margen GAAP cae de 31,8% a 26,2% pese ventas +22%.','SBC TTM de 543 M$ y adquisiciones/circulante limitan la lectura del FCF como caja distribuible.','La expansión regulatoria, los comparables homogéneos y la contabilidad de compra requieren seguimiento; no se certifica Stage3.5.']
pros_en=['TTM revenue grew17.64% and FCF less SBC18.50%, reconciled to primary statements.','Backlog of$8.2bn and79% recurring quarterly revenue support visibility, not guaranteed cash.','Hexagon pro forma shows16.87% Q3 revenue growth on a more comparable perimeter.']
cons_en=['The$323.75 close exceeds the$140.72 central and$256.36 favorable cases; no entry is approved.','Q3 EBIT grew only0.78% and GAAP margin fell from31.8% to26.2% despite22% revenue growth.','TTM SBC of$543m and acquisition/working-capital needs constrain distributable-cash interpretation.','Regulatory developments, homogeneous peers and purchase accounting need follow-up; Stage3.5 is not certified.']
# Human-readable spacing for English evidence.
import re
pros_en=[re.sub(r'(?<=[a-zA-Z])(?=[0-9$])|(?<=[0-9%])(?=[a-zA-Z])',' ',x) for x in pros_en];cons_en=[re.sub(r'(?<=[a-zA-Z])(?=[0-9$])|(?<=[0-9%])(?=[a-zA-Z])',' ',x) for x in cons_en]
s+='\n## Pros y contras exactos para ficha\n'
for title,items in [('A favor',pros_es),('En contra',cons_es),('Pros',pros_en),('Cons',cons_en)]:s+='\n### '+title+'\n\n'+'\n'.join('- '+x for x in items)+'\n'
(P/'report.md').write_text(s)
meta=dict(ticker='CDNS',as_of='2026-11-04',research_cutoff='2026-11-04 15:20 UTC',price=323.75,price_timestamp='2026-11-03 16:00 America/New_York',bear=80.44,base=140.72,bull=256.36,status='FCFF methodological migration complete; research-grade; comparable and entry checks pending',decision_es='Esperar precio; FCFF central140,72 frente323,75. No entrada Stage3.5.',decision_en='Wait for price; FCFF central140.72 versus323.75. No Stage3.5 entry.',buy_ceiling=None,stage35_approved=False,approved_entry=False,pros_es=pros_es,cons_es=cons_es,pros_en=pros_en,cons_en=cons_en,publication_note='Preserve A106 historical FCFE150.68 and controlled bridge. Not new earnings. No automatic promotion to trade-ready. Regulatory status unresolved, do not assert extension or expiry as fact.',pros_cons_evidence={'pros':['Section2; k25,q10,priorq3','Section1; q3,q3cfo','Section3; q10 note2'],'cons':['Section6; model.json and price','Section2; q10','Sections3-4; q10 cashflows','Section9; q10,regulator']})
json.dump(meta,open(P/'publication.json','w'),indent=2,ensure_ascii=False)
print('Report written',len(s))
