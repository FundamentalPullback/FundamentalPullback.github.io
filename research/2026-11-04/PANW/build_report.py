from pathlib import Path
import json
P=Path(__file__).parent
x=json.loads((P/'model/inputs.json').read_text());r=json.loads((P/'model/results.json').read_text());v=json.loads((P/'model/valuation_checks.json').read_text());h=json.loads((P/'history/reported_history.json').read_text())['periods']
f=lambda n:f'{n:,.2f}'
sources={'10k':'https://www.sec.gov/Archives/edgar/data/1327567/000132756726000023/panw-20260731.htm','proxy':'https://www.sec.gov/Archives/edgar/data/1327567/000130817926000432/panw-20261027.htm','release':'https://investors.paloaltonetworks.com/news-releases/news-release-details/palo-alto-networks-reports-fiscal-fourth-quarter-and-fiscal-10','calendar':'https://www2.paloaltonetworks.com/company/press/2026/palo-alto-networks-to-announce-fiscal-first-quarter-2027-financial-results-on-wednesday--november-18--2026','price':'https://stockanalysis.com/stocks/panw/history/'}
pro='PANW combina red, nube e identidad con ingresos FY26 de 11.480 millones y RPO de 21.200 millones. La oportunidad comercial es amplia, pero el crecimiento incluye adquisiciones y no demuestra crecimiento orgánico equivalente.'
con='El FCF bruto FY26 fue 4.113 millones; al restar el SBC del estado de flujos quedan 2.339 millones, solo un 7,59% más. Esta aproximación no es FCFF ni caja distribuible: anticipos, impuestos y comisiones alteran la conversión.'
con2='La caja de julio, las compras posteriores y las obligaciones convertibles pueden modelarse, pero la dilución neta de premios y el capital actual no están conciliados. Los DCF son condicionales; no se certifica valor total ni entrada.'
text=f'''# PANW | Palo Alto Networks | Investigación parcial y DCF condicionado

Corte de investigación: 4 noviembre 2026. Precios congelados al cierre del 3 noviembre. USD millones, salvo acciones en millones, ratios y dólares por acción. Estado: investigación parcial revisada independientemente. No aprobación de entrada ni Stage 3 integral. El valor total actual permanece **no determinado**; los escenarios siguientes son resultados de supuestos explícitos, no un rango certificado de valor justo.

## 1. Decisión y origen del pendiente

La caída de cotización no basta para abrir una posición. El último escáner conservado, 29 octubre, dice 377,95, QP 80, Opportunity 85 y RSI 50,8; Stage 2 está vacío, no equivale a Sí. El informe A118 distinguía ese dato del cierre 380,57. El cierre independiente del 3 noviembre es **350,20**, sin sustituir retrospectivamente la observación del escáner. [Historial de cotización]({sources['price']}).

{pro}

{con}

{con2}

El modelo central arroja {f(r['base']['conditionalValuePerShare'])} por acción bajo sus supuestos, y los casos alternativos {f(r['bear']['conditionalValuePerShare'])}/{f(r['bull']['conditionalValuePerShare'])}. Ni siquiera el caso favorable analizado alcanza 350,20. Esto indica exigencia elevada del precio bajo esta metodología, no certeza de sobrevaloración de idéntica magnitud: el beneficio fiscal de compras y el puente de capital no están certificados, el negocio está cambiando y los márgenes futuros son supuestos. No se transforma esa distancia en señal corta o entrada.

El próximo resultado está confirmado para **18 noviembre de 2026 después del cierre estadounidense**, Q1FY27 terminado el 31 octubre. La fecha está confirmada; no hay resultados Q1 en esta investigación. [Anuncio oficial publicado el 3 noviembre]({sources['calendar']}). Hasta entonces interesa comprobar alcance adquirido, margen GAAP/SBC, caja de cierre y guía, no anticipar un resultado inexistente.

## 2. Negocio, competencia y evidencia que puede refutar la tesis

La plataforma integra seguridad de red, operaciones/nube e identidad; CyberArk amplía identidad y Chronosphere observabilidad. La integración puede reducir proveedores y aumentar venta cruzada, pero también exige migraciones, incentivos comerciales, desarrollo e integración. Los competidores no desaparecen por agrupar productos. Fortinet y Check Point ofrecen referencias de rentabilidad de seguridad, aunque difieren en hardware, suscripciones, adquisiciones y trimestre.

FY26 tuvo 9.200 de suscripción/soporte y 2.280 de producto. RPO alcanzó 21.200, de los que aproximadamente 9.300 se esperan reconocer en los siguientes doce meses. NGS ARR de 9.100 creció 63%, pero cambia de perímetro con productos/compras: no es ingreso GAAP, caja cobrada ni crecimiento orgánico. Dos distribuidores representan 15% de ingresos cada uno; ningún cliente final supera 10%. La dependencia de canal y ejecución comercial existe aunque la cartera final esté diversificada. [10-K FY26]({sources['10k']}) y [comunicado Q4]({sources['release']}).

La tesis favorable requiere retención/venta cruzada que conviertan la ampliación de plataforma en EBIT después de SBC, sin un ciclo permanente de compras financiadas con acciones. La refutan márgenes que solo mejoren excluyendo remuneración, pérdidas persistentes en las compras, mayor capex/comisiones o pérdida de competitividad. El modelo no capitaliza una etiqueta de IA: exige ingresos, márgenes y retorno sobre inversión verificables.

## 3. Historia normalizada y conversión de caja

El TTM termina el 31 julio y coincide con FY26. No se añade un trimestre octubre no publicado. El paquete incluye FY24–26 y ocho trimestres FY25–26, con observaciones, procedencia y conciliaciones. Q4 es año menos nueve meses; flujos Q2/Q3 son diferencias acumuladas. Todos los valores se ajustan al split histórico cuando así los presenta el filing.

| Periodo | Ingresos | EBIT GAAP | CFO | Capex bruto | FCF bruto | SBC CFO | FCF menos SBC CFO |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for name in ['FY2024','FY2025','FY2026','Q1FY2026','Q2FY2026','Q3FY2026','Q4FY2026']:
 a=h[name];text+='| '+name+' | '+' | '.join(f(a[k]) for k in ['revenue','ebit','cfo','capital_spend','fcf_gross','sbc_cf','fcf_less_sbc_cf'])+' |\n'
text+=f'''
Ingresos FY26 crecen 24,50%, pero el margen EBIT cae de 13,48% a 6,05%. FCF bruto sube de 3.469 a 4.113; FCF menos SBC de CFO sube de 2.174 a 2.339, con margen que baja de 23,58% a 20,37%. El SBC de CFO 1.774 no es idéntico al gasto GAAP total 1.815; usar ambos como dos deducciones sería incorrecto. La alternativa FCF menos gasto SBC es 2.298. Ninguna es beneficio disponible por acción.

Los impuestos pagados FY26 fueron 199 frente a 505; los anticipos de clientes aportaron 1.202 al CFO. No se supone que ambos favorezcan indefinidamente el flujo. Las comisiones diferidas consumieron 795 frente a amortización 590: desfase neto 205. El gasto/capex agregado 440 incluye propiedad, equipo y otros activos; no hay desglose fiable de caja de software o SBC capitalizado. Esos campos permanecen nulos. Software interno neto 266 frente a 167 y amortización 104 no demuestran 203 de adiciones de caja en un año de adquisiciones.

D&A 855 se separa en amortización adquirida 640, software interno 104 y residual físico/otro 111. El DCF retiene reposición del software interno; no añade D&A total sobre un EBIT ya anterior a amortización adquirida. FY24 beneficio neto 2.578 incluía beneficio fiscal 1.590, por lo que no constituye base de beneficio recurrente. FY26 pérdida no operativa neta 562 por valoración de notas/capped calls tampoco se convierte en coste operativo permanente.

Normalización de control: EBIT reportado 695 + amortización adquirida 640 − ganancia QRadar 117 = **1.218** después de SBC y antes de amortización adquirida. Eliminar la ganancia es correcto porque redujo G&A. CFO ya la revierte; no se descuenta otra vez del CFO. No se añade automáticamente un escudo fiscal sobre los 640: el valor contable no prueba base ni vida fiscal.

## 4. Compras, perímetro y guía: no confundir crecimiento con adquisición

CyberArk se adquirió el 11 febrero por 21.061: efectivo 2.308, 112 millones de acciones valoradas en 18.488 y premios sustitutivos 265 atribuibles a la compra. De los premios totales 945, otros 680 dependen de servicio futuro. El goodwill 14.800 es sustancialmente deducible fiscalmente, pero no hemos reconstruido el calendario fiscal. Intangibles 6.279 incluyen tecnología 2.537, renovaciones 3.500, contratos 219 y marca 23. No se añaden goodwill ni intangibles a la valoración del negocio ya descontado.

Chronosphere cerró el 29 enero por 2.951, incluidos 2.842 de caja y 109 de premios de compra. Otros 416 de premios son servicio futuro. Goodwill 2.364 no deducible e intangibles 565. Koi, 14 abril, costó 231 principalmente caja; Portkey, 29 mayo, 117. Embrace cerró 27 agosto con precio de caja anunciado 325 y Console el 1 septiembre por 500, sujetos a ajustes. Se deducen una vez 825 como puente posterior a julio, no como salida de caja exacta neta ni balance de noviembre. Las adquisiciones anteriores ya están en la caja de julio y no se vuelven a descontar.

CyberArk y Chronosphere aportaron 930 de ingresos y pérdida operativa 797 desde sus compras. El proforma combinado FY26 indica ingresos **12.312**, frente a 10.486 comparables FY25, y pérdida neta 114; no equivale a desempeño orgánico realizado ni EBITDA normalizado. La guía FY27 de ingresos 14.100–14.200 implica aproximadamente 14,93% sobre 12.312 al punto medio, no el 23–24% frente al reporte de perímetro incompleto. La guía FY27 de margen no GAAP es 29,5% y FCF ajustado 38%, sin reconciliación GAAP prospectiva por componentes inciertos. No se adopta ese margen como después de SBC. La guía Q1 3.300–3.310 y EPS no GAAP 0,96–0,98 con 837–844 millones de acciones no reemplaza una valoración GAAP después de SBC. [Comunicado]({sources['release']}).

El modelo utiliza 12.312 como ancla de ingresos y 1.218 como ancla anterior de EBIT para financiar incremento de NOPAT. **Las dos anclas tienen diferente alcance**: 1.218 procede del reporte, no es EBIT proforma. Se expone esta carencia y se prueba ancla 500–3.000; no se inventa una conciliación. La caja futura financia el crecimiento y la mejora de margen con ROIC, evitando tratarlos como gratuitos.

## 5. Puente de capital, convertibles y remuneración

| Concepto | Importe seleccionado | Naturaleza/fecha |
|---|---:|---|
| Caja e inversiones | 7.906 | Reportado 31 julio |
| Embrace + Console | −825 | Precios anunciados, sujetos a ajustes |
| Reserva operativa | −2.000 | Supuesto, no caja legalmente restringida |
| Notas convertibles | −1.774 | Valor razonable julio, no cotización noviembre |
| Capped calls | +153 | Valor razonable julio |
| QRadar contingente | −206 | Valor razonable, no pago garantizado |
| Remuneración diferida | −405 | Obligación económica, normalmente acciones |
| Riesgo fiscal histórico | −500 | Reserva discrecional, no deuda fiscal verificada |
| Reestructuración reconocida | −14 | Obligación registrada |
| Puente seleccionado | +2.335 | No certificado como capital actual |

Caja 2.514 e inversiones 5.392 totalizan 7.906; inversiones de corto 557 y largo 4.835. Tras restar 825 quedan 7.081 antes de todos los demás movimientos posteriores. No se añaden DTA, goodwill, financiación a clientes ni créditos contractuales como caja libre. Arrendamientos operativos se mantienen en gasto y no se suman como deuda con un EBIT sin ajuste paralelo. Los ingresos diferidos no se restan íntegramente como deuda ni se perpetúan sus entradas de caja.

Las notas tienen principal derivado 1.097 (1.250 menos 153), pero valor razonable 1.774. La conversión por 1.000 de principal da 4,3161 acciones más 88,263 en efectivo; el principal se liquida en efectivo y el exceso puede liquidarse en caja/acciones. Strike efectivo cerca de 211,24, caps de la cobertura entre 287,21 y 291,44. Se usa la obligación neta de valor razonable 1.621, **sin añadir también toda la conversión como dilución**. Es un proxy fechado; el precio de noviembre requiere revaloración de opción si se desea precisión. Las antiguas warrants 2025 ya se liquidaron emitiendo 27 millones de acciones incluidas en el saldo.

Las acciones efectivas del 9 octubre son **818,771631 millones** según proxy, no las 764 medias diluidas anuales. Se añaden **15 millones de dilución neta seleccionada**, denominador 833,771631. Es un supuesto analítico, no un número reconciliado. Hay 29,821161 millones de RSU/PSU al máximo rendimiento y 0,232754 millones de opciones con strike 9,84; los máximos no son expectativa de devengo. El saldo de remuneración futura no reconocido 3.300 se reconoce en unos 2,5 años y no incluye futuras concesiones. Retener el SBC futuro y sumar todos los premios brutos podría contar dos veces parte de la remuneración.

La obligación diferida 405 normalmente se paga en acciones, con caja si no hay suficientes acciones del plan. Los 405 cubren solo cuentas diversificadas clasificadas como pasivo, no todo el plan. El proxy muestra al cierre FY26 saldos diferidos de Arora 990,481487, Golechha 46,592250 y Jenkins 119,897603 millones: suma 1.156,971340. No se suman mecánicamente ni se convierten a acciones actuales, pues fecha, valoración y solapamiento con premios/acciones no están conciliados. Los 15 millones seleccionados no demuestran que todos los derechos ya ganados estén capturados. Por ello no se certifica valor total. Se muestran sensibilidades a dilución 0/15/30 millones y a retirar la deducción 405; ninguna resuelve por sí misma la coexistencia de premio ganado, servicio futuro, impuestos de liquidación y PSU. [Proxy del 27 octubre]({sources['proxy']}).

Los UTB brutos son 719 y los intereses/penalizaciones 113: exposición 832, no obligación incremental neta demostrada. Solo 393 afectarían gasto fiscal si se reconocieran, lo que **no los convierte en caja por pagar**. La reserva central 500 es discrecional, no 393+113 disfrazado de deuda cierta. La sensibilidad 0/500/719/832 deja visible la incertidumbre sin añadir también DTA como activo libre. El impuesto normalizado futuro 24% es distinto de resolver este saldo histórico.

## 6. FCFF de diez años: capital y SBC no gratuitos

Diez periodos anuales analíticos desde 3 noviembre 2026 hasta 3 noviembre 2036, no ejercicios fiscales reportados. La guía FY27 sirve como ancla económica del primer periodo, no proyección exacta agosto–julio ni un stub observado. Descuento al final de cada periodo; el flujo hasta noviembre no está certificado. La ausencia de extrapolación trimestral evita inventar Q1, pero deja una aproximación de calendario/perímetro.

EBIT se define después de SBC y antes de amortización adquirida. Impuesto normalizado 24% sobre EBIT positivo, sin escudo fiscal contable automático. D&A físico/software seleccionado 2% de ventas; gasto bruto de capital mínimo desciende del 4% al 3% en base. Inversión neta = máximo de (capex − D&A + 9% del incremento de ventas para comisiones + 2% para otros circulantes) y (incremento positivo de NOPAT / ROIC). El segundo término financia también la expansión del margen. No se suman ambos como dos proyectos independientes ni se acredita entrada perpetua de anticipos de clientes.

Estos parámetros son supuestos de reposición y crecimiento, no guía empresarial. Las bandas de capex se apoyan en 440 sobre ventas 11.480 y la necesidad de software/capital de integración, pero no afirman que todo 440 sea mantenimiento. El gasto SBC permanece dentro del margen; su ratio memo base 15%→12% no es un addback ni una segunda deducción. La alternativa con inversión ligada solo a crecimiento de ventas reconoce eficiencia de margen sin capital adicional: se muestra aparte, no se llama ROIC incremental idéntico.

Terminal: crecimiento nominal perpetuo, mismos márgenes finales, capex físico/software mínimo y comisión/circulante sobre crecimiento; reinversión al menos NOPAT×g/ROIC. No se concede amortización fiscal adquirida para siempre. La prueba de escudo fiscal 100/250/400 anuales dura solo diez periodos y no es una estimación fiscal.

| Supuesto | Adverso | Base | Favorable |
|---|---:|---:|---:|
| Ingresos primer periodo | 12.800 | 14.150 | 14.500 |
| Crecimiento periodos 2–5 | 12/10/8/7% | 18/16/14/12% | 23/21/19/17% |
| Crecimiento periodos 6–10 | 6/5/4/3/3% | 10/8/7/6/5% | 15/13/11/9/7% |
| Margen después SBC, años 1/5/10 | 10/15/17% | 15/22/24% | 18/27/30% |
| ROIC incremental seleccionado | 20% | 30% | 40% |
| Descuento | 10,5% | 9% | 8% |
| g terminal | 2% | 3% | 3,5% |
| Capex bruto/ventas 1→10 | 4,5→3,5% | 4→3% | 3,8→2,8% |

Referencia de descuento: Treasury 10 años 4,95% al 3 noviembre; ERP mensual ajustado 4,41% al 1 noviembre, originalmente calculado con Treasury 5,29%; beta de proveedor 0,93, no regresión propia. CAPM da 9,0513%. Con deuda objetivo seleccionada 2%, spread elegido 1,5% e impuesto 24%, WACC mecánico aproxima 8,97%; 9% es selección próxima, no precisión observada. La beta de otro proveedor difiere (0,97), y los inputs no están sincronizados. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve), [ERP](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), [beta](https://stockanalysis.com/stocks/panw/statistics/).

| Periodo base | Ventas | EBIT después SBC/pre-amortización | NOPAT | Inversión neta financiada | FCFF |
|---|---:|---:|---:|---:|---:|
'''
for a in r['base']['rows']:text+=f"| {a['year']} | "+' | '.join(f(a[k]) for k in ['revenue','ebitAfterSbcBeforeAcquiredAmort','nopat','netReinvestment','fcff'])+' |\n'
text+='\n| Caso | EV operativo | Puente | Acciones | Resultado condicionado/acción | Terminal/EV |\n|---|---:|---:|---:|---:|---:|\n'
for n,a in r.items():text+=f"| {n} | {f(a['enterpriseValue'])} | {f(a['capitalBridge'])} | {f(a['sharesMillions'])} | {f(a['conditionalValuePerShare'])} | {a['terminalShareOfEV']:.1%} |\n"
text+='''
El peso terminal, especialmente favorable, obliga a tratar las cifras como escenarios, no probabilidades ni una banda de confianza. El crecimiento, margen y ROIC favorable deben coexistir; no son tres regalos independientes.

## 7. Sensibilidades e inverso: qué exigiría 350,20

| Variación aislada base | Resultado condicionado |
|---|---:|
'''
for k,label in [('taxRisk','Reserva fiscal'),('netExistingDilution','Dilución neta existente'),('priorNopatAnchor','Ancla EBIT anterior'),('taxShieldAnnual10y','Escudo fiscal anual solo 10 años'),('roic','ROIC'),('capexFloor','Capex adicional/ventas')]:
 for a in v['sensitivities'][k]:text+='| '+label+' '+str(next(z for key,z in a.items() if key!='value'))+' | '+f(a['value'])+' |\n'
text+='\n| WACC / g base | g 2% | g 3% | g 4% |\n|---|---:|---:|---:|\n'
for w in [.08,.09,.10,.11]:text+='| '+f'{w:.0%}'+' | '+' | '.join(f(next(a['value'] for a in v['sensitivities']['wacc_g'] if a['wacc']==w and a['g']==g)) for g in [.02,.03,.04])+' |\n'
text+=f'''
Con solo eficiencia de margen sin inversión incremental por esa mejora, la alternativa asciende a {f(v['sensitivities']['revenueGrowthOnlyInvestment']['value'])}. Comisiones 0–15% del incremento no cambian central porque el suelo ROIC domina; no significa que las comisiones sean gratuitas. Capital desconocido ±1.000 mueve aproximadamente ±1,20 por acción. El escudo fiscal, la dilución y las reservas importan, pero estas variaciones aisladas no cierran la distancia al precio.

El inverso manteniendo primer ingreso, margen, ROIC y descuento base requiere añadir **26,31 puntos porcentuales** a cada crecimiento de los periodos 2–10: crecimiento segundo periodo alrededor de 44,31% y décimo 31,31%, seguido de desaceleración terminal a 3%. No es pronóstico ni prueba de que el mercado modele eso: es una combinación matemática, muy exigente y con salto terminal. El inverso de margen no encuentra raíz al elevar todos los márgenes hasta +60 puntos; incluso margen final 84% arroja solo {f(v['inverse']['uniformMarginShift']['valueAtUpperBound'])} porque también se financia la creación de beneficio. No se extrapola fuera del intervalo ni se presenta una raíz falsa. Los scripts verifican monotonía dentro del barrido.

## 8. Comparables y límites del contraste relativo

| Último trimestre publicado | PANW mayo–julio | FTNT julio–septiembre | CHKP julio–septiembre |
|---|---:|---:|---:|
| Ingresos | 3.410 | 2.078,4 | 669,8 |
| Margen EBIT GAAP | 5,04% | 33,89% | 26,46% |
| SBC CFO / ventas | 13,49% | 3,85% | 8,18% |
| CFO − capex agregado | 1.254 | 881,8 | 257,9 |

La comparación retiene SBC y amortización en EBIT GAAP de los tres. El EBIT ajustado de PANW no se enfrenta directamente a EBIT GAAP ajeno. PANW ajusta FCF Q4 hasta 1.289; FTNT excluye 17 de escrow y reporta 864,8; CHKP año previo incluía anticipo de arrendamiento 159,9. Se conserva el cálculo base, no una falsa clasificación de calidad por el porcentaje de CFO. Las compras, software y periodos no son homogéneos.

No se ha establecido un conjunto homogéneo contemporáneo de EV, capital/acciones y denominadores TTM para los tres. Por tanto **no hay contraste de múltiplos de valoración cerrado** ni mediana aplicada como objetivo. Este requisito pendiente, junto al puente de premios/capital, impide declarar Stage 3 integral. Los datos y enlaces reproducibles están en comps/. [FTNT Q3](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000027/ftnt-20260930.htm), [CHKP Q3](https://www.sec.gov/Archives/edgar/data/1015922/000117891326004953/zk2636310.htm).

## 9. Próximos controles y conclusión

Antes de una valoración certificable: conciliar capital de octubre y pagos de compras; separar premios ya ganados de servicio futuro y diferidos; actualizar valor de notas/cobertura; reconstruir base y vida fiscal de adquisiciones; comprobar margen/caja de perímetro completo; cerrar comparables de valoración; refrescar el filtro técnico con datos actuales. El 18 noviembre puede aportar parte de ello, no se presume que resuelva todo. No hay instrucción de operar ni seguimiento de cuenta de inversión.

Conclusión ES: **Esperar, investigación parcial.** El negocio ampliado ofrece potencial, pero el crecimiento adquirido y el FCF ajustado no sustituyen beneficio después de SBC ni capital financiado. El DCF condicionado no respalda 350,20 con los supuestos probados. Capital/dilución y contraste relativo siguen abiertos; sin valor total certificado, sin Stage 3 integral y sin entrada.

Conclusion EN: **Wait; partial research.** The enlarged platform has potential, but acquired growth and adjusted FCF do not replace profit after SBC or funded reinvestment. The conditional DCF does not support $350.20 under tested assumptions. Current capital, net award dilution and homogeneous valuation peers remain unresolved; no certified total fair value, completed Stage 3 or entry approval.

## 10. Fuentes, reproducción y alcance

Fuentes primarias enlazadas junto a los hechos; precios/beta secundarios identificados como tales. Fuentes históricas adicionales: [Q1FY26](https://www.sec.gov/Archives/edgar/data/1327567/000132756725000035/panw-20251031.htm), [Q2FY26](https://www.sec.gov/Archives/edgar/data/1327567/000132756726000005/panw-20260131.htm), [Q3FY26](https://www.sec.gov/Archives/edgar/data/1327567/000132756726000015/panw-20260430.htm). El paquete incluye selección factual, procedencia, scripts, escenarios, sensibilidades y pruebas; no copias íntegras de filings. La reproducción es determinista y offline. Recalcular prueba aritmética, no verifica por sí solo calidad económica ni fuentes en tiempo real.
'''
(P/'report.md').write_text(text)
summary={'ticker':'PANW','company':'Palo Alto Networks','researchDate':'2026-11-04','valuationDate':'2026-11-03','status':'partial_conditioned_audited','readyForPublication':True,'reviewScope':'Partial research; current capital/net awards and homogeneous valuation peers unresolved','fairValue':None,'fairValueTotal':None,'bear':None,'base':None,'bull':None,'conditionalDcfScenarios':{k:a['conditionalValuePerShare'] for k,a in r.items()},'scanPrice':377.95,'scanDate':'2026-10-29','scanQuality':80,'scanOpportunity':85,'scanRsi':50.8,'scanStage2':None,'scanComparisonClose':380.57,'latestClose':350.2,'latestCloseDate':'2026-11-03','sources':sources,'nextEvent':{'date':'2026-11-18','timing':'After US market close','type':'Q1FY2027 results','confirmed':True,'sourceUrl':sources['calendar']},'entryApproved':False,'stage3Complete':False,'stage35Approved':False,'confidence':'Moderate on historical facts and arithmetic; limited on proforma operating normalization, net dilution, tax basis and current capital.','conclusionEs':'Esperar. Investigación parcial: DCF condicionado y capital/dilución sin conciliar; no valor total certificado ni entrada.','conclusionEn':'Wait. Partial research: conditional DCF, unreconciled current capital/net awards, no certified total fair value or entry.','pros':[{'textEs':'Plataforma ampliada y RPO de 21.200 millones, con oportunidad de venta cruzada; el crecimiento incluye adquisiciones.','textEn':'Expanded platform and $21.2bn RPO support cross-selling potential; reported growth includes acquisitions.','evidence':pro,'sourceUrl':sources['10k']}],'cons':[{'textEs':'FCF menos SBC de CFO crece solo 7,59%, pese al 24,50% de ingresos; anticipos e impuestos limitan comparabilidad.','textEn':'FCF less cash-flow SBC grows only 7.59%, versus 24.50% revenue growth; prepayments and taxes limit comparability.','evidence':con,'sourceUrl':sources['10k']},{'textEs':'Capital y dilución neta no conciliados; DCF condicionado, sin valor total certificado ni entrada.','textEn':'Current capital and net dilution remain unreconciled; conditional DCF, no certified total value or entry.','evidence':con2,'sourceUrl':sources['proxy']}]}
(P/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n');print('report words',len(text.split()))
