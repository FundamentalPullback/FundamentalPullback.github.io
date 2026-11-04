from pathlib import Path
import json,subprocess
P=Path(__file__).parent
f=json.load(open(P/'financials.json'));c=json.load(open(P/'capital.json'));u=json.load(open(P/'sources/urls.json'))
def n(v):return '—' if v is None else f'{v:,.2f}'
pros=['El beneficio operativo TTM aumenta a 766,4 M$ y el neto a 404,6 M$, con mejora operativa además del efecto de las recompras.','El 10-Q informa de la terminación de la orden FDIC de 2023 el 15 de octubre de 2026, tras completar las medidas requeridas.','WEX Bank mantiene clasificación de bien capitalizado; capital total de 1.007,5 M$ y ratio del 13,01 % a septiembre.']
cons=['Los 593,2 M$ de caja consolidada incluyen 463,0 M$ del banco; no son caja libre para sumar al valor del accionista.','El FCF ajustado de 502,8 M$ en nueve meses no cierra por sí solo la retención de capital, el servicio de deuda y las transferencias banco-matriz.','El crecimiento Q3 sin combustible y divisas es aproximadamente 4,37 %, frente al 12,76 % publicado; sigue sin valoración propia certificada.']
proen=['TTM operating income increased to $766.4m and net income to $404.6m, showing operating progress beyond share repurchases.','The 10-Q reports termination of the 2023 FDIC order on October 15, 2026, after the required remediation was completed.','WEX Bank remains well capitalized, with $1,007.5m of total capital and a 13.01% ratio at September.']
conen=['Consolidated cash of $593.2m includes $463.0m held by the bank; it is not freely available cash to add to shareholder value.','Nine-month adjusted FCF of $502.8m does not by itself reconcile capital retention, debt service and bank-to-parent distributions.','Q3 revenue growth excluding fuel and FX is about 4.37%, versus reported growth of 12.76%; no certified intrinsic valuation is available.']
s=f'''# WEX: actualización de capital bancario y caja distribuible

**Revisión parcial, sin valoración certificada.** Corte de investigación: 4 noviembre 2026, 17:15 UTC. Referencia: cierre regular del 3 noviembre, **181,97 USD**, no cotización intradía. Estados al 30 septiembre 2026, 10-Q presentado el 29 octubre. Importes en millones USD salvo EPS, precio y ratios; acciones en millones.

## 1. Conclusión y cambio frente a A119

Mantener en observación. Hay crecimiento y mejoras regulatorias verificables, pero aún no un flujo distribuible a accionistas suficientemente conciliado para un valor central, rango o inverso. **Valor, escenarios e inverso quedan nulos, no cero.** No se aprueba Stage 3.5 ni se modifica posición, stop, tamaño u orden.

Se añade lo que faltaba a la nota rápida A119: tres ejercicios y cuatro trimestres, capital bancario, separación de caja, financiación de cartera, costes crediticios y actualización regulatoria. A119 mostraba 502,9 M$ al sumar componentes redondeados; el emisor publica **502,8 M$** de FCF ajustado. La diferencia de 0,1 M$ es redondeo del puente, no una nueva caja encontrada.

El 10-Q informa que la orden de consentimiento FDIC de 2023 **terminó el 15 octubre 2026**, tras la subsanación. La multa de 0,65 M$ impuesta en diciembre de 2024 ya se pagó. No se mantiene esa orden como alerta vigente; tampoco se infiere que hayan desaparecido las restricciones ordinarias de un banco. [10-Q, apartado de regulación]({u['q3']}).

## 2. Negocio y calidad del resultado

WEX combina Mobility, Benefits y Corporate Payments. Las redes de aceptación, integración con clientes, datos de gasto y administración de cuentas crean relaciones recurrentes; sin embargo, una parte material de los ingresos depende de combustible, financiación, mora, tipos de interés y volumen de gasto. No se trata todo el grupo como software de caja recurrente sin balance.

Q3: ventas 780,1 frente a 691,8, +12,76 %. La conciliación del emisor identifica 57,3 M$ de efecto favorable de combustible y 0,8 M$ de divisas. Retirarlos da 722,0 y un crecimiento aproximado del **4,37 %**. Es una aproximación a combustible/divisas constantes, no prueba de crecimiento orgánico puro: no separa todos los cambios de clientes y cartera. En nueve meses, el equivalente es aproximadamente {100*c['growth']['year_to_date_ex_fuel_fx']:.2f} %.

Mobility Q3 genera 435,1 M$, frente a 360,8. El precio medio del combustible sube de 3,38 a 4,85 USD/galón, mientras los galones procesados bajan de 3.639,8 a 3.631,2 millones. Las transacciones crecen de 140,0 a 142,3 millones; la tasa neta de procesamiento baja de 1,33 % a 1,14 %. No extrapolar el aumento del gasto en combustible como crecimiento equivalente del volumen físico.

Benefits aporta 207,6 M$ y 22,1 millones de cuentas SaaS medias, frente a 198,1 y 21,5. Activos HSA de caja medios 5.349,2 frente a 4.808,5, pero rendimiento HSA 4,97 % frente a 5,13 %. Son activos de clientes que generan ingresos, no efectivo propio para repartir. Corporate Payments aporta 137,4 frente a 132,8 M$; volumen de compras 24.644,3 frente a 23.176,6, con tasa de intercambio 0,46 % frente a 0,47 %.

TTM: ingresos 2.880,4, beneficio operativo 766,4 y neto atribuible 404,6, frente a 2.624,4, 654,9 y 283,7. El crecimiento neto también refleja menor financiación neta y fiscalidad, no solo ingresos operativos. En FY2025 el neto bajó de 309,6 a 304,1 mientras EPS subió de 7,50 a 8,47 y diluidas medias cayeron de 41,3 a 35,9: ejemplo concreto del efecto de recompras.

[Resultados oficiales y conciliación macro]({u['release']}); [10-K FY2025]({u['k25']}).

## 3. Tres ejercicios, cuatro trimestres y TTM

CFO consolidado puede ser negativo por crecimiento de cartera financiada con depósitos y otras fuentes. Se presenta CFO menos inversión y SBC como **aritmética de control**, no como caja distribuible ni FCFE. Capex incluye propiedad, equipos y software capitalizado, sin doble deducción. El beneficio operativo ya incluye interés operativo y provisiones crediticias, pero no toda la financiación corporativa.

|Periodo|Ingresos|Beneficio operativo|Neto atribuible|EPS diluido|CFO|Capex/software|SBC no monetaria|CFO−capex−SBC, bruto|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for r in f['annual']+f['quarters']+f['ttm']:s+='|'+r['period']+'|'+'|'.join(n(r.get(k)) for k in ['revenue','operating_income','net_income','eps','cfo','capex','sbc','raw_cfo_less_capex_sbc'])+'|\n'
s+=f'''
TTM = FY2025 + nueve meses 2026 − nueve meses 2025; previo con FY2024 y comparativos 2025/2024. Q4 se deriva por diferencia para partidas aditivas; EPS 2,41 y diluidas 35,0 proceden directamente del [comunicado Q4](https://www.sec.gov/Archives/edgar/data/1309108/000130910826000005/q42025earningsrelease.htm). El redondeo de las fuentes puede producir diferencias de 0,1 M$ frente al trimestre publicado. No se suman EPS para inferir acciones o beneficio anual.

## 4. Conciliación de caja y beneficio ajustados

|Puente de nueve meses|M$|
|---|---:|
|CFO GAAP|−419,6|
|Compras netas de valores corrientes|−565,3|
|Capex y software|−128,0|
|Financiación neta de cartera/HSA|+1.277,9|
|Exclusión de la disminución de caja de WEX Bank|+302,0|
|Otros ajustes|+35,9|
|Suma de componentes redondeados|502,9|
|**FCF ajustado publicado**|**502,8**|

La financiación neta comprende depósitos +758,1, federal funds +195,0, participaciones +4,8 y FHLB +320,0. No es ingreso ni beneficio. El ajuste de 302,0 elimina un movimiento del saldo bancario de la métrica; **no demuestra un dividendo del banco a la matriz**. Restarlo mecánicamente como si fuese una transferencia cobrada también confundiría la conciliación.

El propio emisor advierte que el FCF ajustado no representa caja discrecional porque no descuenta todas las obligaciones, incluido servicio de deuda. Restar la SBC no monetaria de 107,0 a los 502,8 produce 395,8; retirar además otros add-backs de 35,9 deja 359,9. Son pruebas ilustrativas, **no FCFE certificado ni base de un DCF**. Los otros ajustes incluyen pagos de contraprestaciones de adquisiciones excluidos por gestión; no se asume que sean gratuitos. No se restan dos veces pagos incluidos en CFO y el flujo de financiación.

El neto ajustado Q3 de 211,9 (EPS 6,13) parte de neto GAAP 134,1 (EPS 3,88) y, entre otros ajustes, añade amortización adquirida 45,6 y SBC 45,3, compensados parcialmente por ajustes fiscales. En nueve meses el add-back SBC de la conciliación no GAAP es 112,4, frente a 107,0 en el estado de caja/nota de compensación. No son la misma serie; no se sustituye una por otra sin conciliación adicional. Los márgenes económicos conservan SBC, pérdidas crediticias y reposición de capacidades adquiridas.

La cartera bp se convirtió en Q1. El anticipo por derechos de 58,6 M$ se pagó en octubre de 2025 y pasó a intangible amortizable en diez años; otros 23,0 M$ por saldos de cuentas a cobrar se pagaron en Q2 de 2026 dentro de CFO. No se perpetúa esa salida como coste anual ni se añade el negocio sin reconocer su inversión. [10-Q, notas de adquisiciones y caja]({u['q3']}).

## 5. Balance: separar financiación bancaria y recursos de la matriz

|Dato a septiembre|M$|Qué significa|
|---|---:|---|
|Caja y equivalentes consolidados|593,2|No toda disponible para accionistas|
|Caja de WEX Bank incluida arriba|463,0|Sujeta a necesidades y regulación del banco|
|Diferencia aritmética no bancaria|130,2|No prueba que toda sea excedentaria|
|Corporate Cash del convenio|106,1|Definición contractual, no dividendo autorizado|
|Caja restringida, separada|580,9|No añadir al equity libre|
|Pasivo de caja restringida|577,5|Requiere conciliación, no activo neto libre por defecto|
|Depósitos a corto plazo|6.180,5|Pasivo de financiación/clientes, no patrimonio|
|Valores corrientes/no corrientes|4.673,6 / 102,7|No sumar sin financiación, riesgo y propiedad económica|
|Cuentas a cobrar netas/restringidas titulizadas|5.342,7 / 192,8|Activos que requieren financiación|
|Deuda contable neta corto/largo plazo|1.863,5 / 3.457,6|Mezcla financiación bancaria y corporativa|

El grupo declara principal de préstamos a plazo aproximadamente 2.600, revolver 395 y notas 550 M$. Además, FHLB aproximadamente 1.400, federal funds 195, participaciones 70 y titulización 118,8 son fuentes distintas. No se resta una suma industrial a un flujo que ya descuenta esa financiación. En un FCFE definitivo tampoco se restaría de nuevo toda la deuda al final.

Liquidez: el revolver conserva aproximadamente 1.200 M$ disponibles; FHLB solo 14,3 M$ de capacidad remanente declarada a esa fecha. No se confunden capacidades comprometidas y no comprometidas ni se concluye insolvencia de un único límite. Los pagos a comercios suelen preceder al cobro a clientes: el crecimiento de la cartera exige financiación antes de realizar el margen.

Capital consolidado 1.152,1 M$, goodwill 3.025,9 e intangibles 1.008,2. El patrimonio tangible consolidado sería negativo; no se sustituye por capital regulatorio del banco para fabricar un múltiplo patrimonial atractivo. AOCI pasa de −128,1 a −371,5: riesgo de valoración y duración de inversiones, que no equivale automáticamente a pérdidas crediticias realizadas.

## 6. Capital regulatorio: holgura no equivale a caja repartible

|Ratio bancario|Septiembre 2026|Diciembre 2025|
|---|---:|---:|
|Capital total/RWA|13,01 %|15,94 %|
|CET1/RWA|12,30 %|14,98 %|
|Tier 1/RWA|12,30 %|14,98 %|
|Tier 1/activos medios|9,26 %|9,04 %|
|Capital total, M$|1.007,5|813,1|
|Tier 1 y CET1, M$|952,4|764,3|

El emisor conserva la categoría de bien capitalizado según el último examen. A partir de los mínimos PCA publicados de 774,2 y 510,1 M$ al 10 %, se infieren RWA aproximados de 7.742 y 5.101 M$: +2.641, aproximadamente 51,8 %. Son inferencias de cifras redondeadas, no una fila exacta de RWA del call report. El capital total aumenta 194,4 y CET1 188,1, pero **no se identifica todo ese incremento como beneficio retenido**: faltan transferencias, OCI y otros componentes.

|Ratio total de referencia|Capital requerido aproximado|Diferencia con 1.007,5|
|---|---:|---:|
'''
for r in c['bank']['target_total_capital_sensitivity']:s+=f'|{r["target_ratio"]*100:.1f} %|{n(r["required_capital"])}|{n(r["arithmetical_headroom"])}|\n'
s+='''
El 10 % es el umbral PCA presentado para estar bien capitalizado; los demás son sensibilidades hipotéticas, no requisitos confirmados ni objetivos del emisor. No se elige el más bajo para extraer caja. La holgura de 233,3 sobre ese umbral no acredita autorización de dividendo, ausencia de colchones adicionales o disponibilidad de efectivo. Una referencia del 13 % deja apenas 1,0 M$ de holgura aritmética; tampoco implica que ese sea el objetivo real. El capital puede ser suficiente y, a la vez, necesitar retención para crecer.

## 7. Riesgo crediticio, financiación y perspectiva

Provisiones por crédito y fraude: 85,5 M$ en nueve meses frente a 57,9; TTM 106,0 frente a 73,5. En Mobility, las pérdidas por volumen de combustible son 11,7 pb en Q3 frente a 12,1, pero 15,3 pb acumulados frente a 12,4. La caída trimestral no elimina el deterioro del acumulado. La guía Q4 espera 17–22 pb y FY2026 16–17 pb. No se sustituye la provisión por cero para normalizar margen.

La antigüedad de cartera muestra 99 % con menos de 30 días de mora a septiembre frente a 98 % en diciembre; la métrica no es una tasa de impago nula ni elimina concentración, fraude o pérdidas futuras. Parte del aumento de provisión responde a mayor combustible y saldo financiado, y otra parte a charge-offs según la explicación del emisor.

Guía corporativa FY2026: ventas 2.970–2.990 M$ y EPS ajustado 21,28–21,48. Q4: ventas 760–780 y EPS ajustado 5,67–5,87. Supone combustible estadounidense de 4,81 USD/galón en Q4, impuesto ajustado del 25 % y acciones diluidas medias 34,1. El EPS ajustado no tiene conciliación prospectiva GAAP completa; no se usa sin más como FCFE. Los 75 M$ recomprados después de septiembre hasta 26 octubre también requieren actualizar caja y acciones, no solo reducir el denominador.

## 8. Método elegido antes de valorar y bloqueo exacto

La excepción 9b del plan se documentó antes de calcular ningún valor. La mezcla de banco, cartera financiada y pagos impide un FCFF industrial con depósitos tratados como caja/deuda libre. El método a investigar es FCFE disponible al accionista, después de crédito, financiación, inversión operativa y capital retenido; se descontaría al coste de equity, sin restar deuda otra vez. El horizonte común de diez años y terminal financiado se mantendría si pueden cerrarse esos flujos.

Faltan para hacerlo defendible:

1. Un puente banco-matriz que distinga beneficio bancario, aportaciones, dividendos, ajustes de capital y cambios de OCI. Las variaciones de caja y capital no bastan.
2. Capital incremental por crecimiento de cartera y depósitos HSA, con colchón de gestión y límites de distribución, además de mínimos regulatorios.
3. Caja de matriz después de deuda obligatoria, inversión, contraprestaciones adquiridas y recompras posteriores, sin confundir ajustes no GAAP con cobros disponibles.
4. Normalización de combustible, tipos, pérdidas de crédito y SBC coherente entre proyección y capital.
5. Comparables cuantitativos homogéneos y un próximo calendario de resultados confirmado.

Se intentó recuperar el registro financiero Q3 del banco identificado por FDIC Cert 34697/RSSD 2700984 mediante las fuentes públicas oficiales, pero la consulta no produjo una respuesta utilizable. No se afirma que no exista ni se sustituye por datos Q2 de un agregador. Los saldos de una entidad bancaria individual pueden incluir relaciones intragrupo eliminadas al consolidar; no se mezclan sin conciliación.

El PER aproximado sobre beneficio GAAP TTM es '''+n(c['price']['pe_reported_proxy'])+''' veces (precio × diluidas Q3 / neto TTM); el precio/guía ajustada central es '''+n(c['price']['forward_adjusted_pe_illustrative'])+''' veces. Son referencias de bases distintas, no dos estimaciones de valor ni prueba de descuento. La comparación pendiente debe separar pagos de flotas, custodia HSA y banco; no se aplica una mediana de software o un EV/EBITDA industrial indiscriminado.

## 9. Calendario y siguiente decisión

Q3 ya se publicó el 28 octubre y la llamada fue el 29 octubre. La página de eventos y fuentes primarias consultadas no aportaron una fecha confirmada para el próximo resultado. Se deja **no confirmada**, sin convertir estimaciones de febrero de terceros en hecho. Esto no deshace el trabajo postevento, pero tampoco aprueba un filtro futuro de calendario.

La siguiente decisión es cerrar el puente de distribución y capital, no calcular una compra con un múltiplo barato. El análisis es parcial y útil para acotar el bloqueo; no incorpora un rango de valor artificial. No se actualizan medias técnicas ni se atribuye una causa única al precio diario.

[Calendario oficial](https://ir.wexinc.com/events-and-presentations/default.aspx). [Anuncio de Q3 ya ocurrido](https://ir.wexinc.com/news/news-details/2026/WEX-Inc--to-Release-Third-Quarter-2026-Financial-Results-on-October-28-2026/default.aspx). [Identificación oficial del banco](https://www.ffiec.gov/npw/Institution/Profile/2700984).

## Evidencia para la ficha

### A favor
'''
s+='\n'.join('- '+x for x in pros)+'\n\n### En contra\n'+'\n'.join('- '+x for x in cons)+'\n\n### English evidence\n'+'\n'.join('- '+x for x in proen+conen)
s+='\n\n## Soporte reproducible\n\nLos scripts build_financials.py y capital.py generan historia, puentes y sensibilidades de capital, no una valoración. report.py genera este informe y qa.py comprueba sumas, redondeo y campos nulos. Paquete público con tablas numéricas seleccionadas y notas propias; fuentes primarias completas se enlazan. Revisión independiente completada sobre historia, fuentes, capital y reproducibilidad. Se mantiene la clasificación parcial y la valoración nula.\n'
(P/'report.md').write_text(s);subprocess.run(['pandoc',str(P/'report.md'),'-s','-o',str(P/'report.html'),'--metadata','title=WEX — capital y caja, revisión parcial'],check=True)
json.dump(dict(ticker='WEX',as_of='2026-11-04',research_cutoff='2026-11-04 17:15 UTC',price=181.97,price_timestamp='2026-11-03 16:00 America/New_York',base=None,bear=None,bull=None,research_status='Independently audited partial fundamental/capital refresh; no certified distributable FCFE',decision_es='Observación: mejora operativa y regulatoria, caja distribuible pendiente; sin valor certificado.',decision_en='Watch: operating and regulatory progress, distributable cash unresolved; no certified value.',approved_entry=False,stage35_approved=False,buy_ceiling=None,pros_es=pros,cons_es=cons,pros_en=proen,cons_en=conen,publication_note='Preserve A119 and real Oct30 scanner184.61. Nov3 close181.97 is separate valuation context. Do not set latestCompleted or insert value0. No industrial FCFF, no orders/positions/stops/lots changes.'),open(P/'publication.json','w'),indent=2,ensure_ascii=False)
