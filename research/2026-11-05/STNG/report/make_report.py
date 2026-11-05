from build_package import *
def f(x):return f'{x:,.2f}'
def table(head,rows):return '| '+' | '.join(head)+' |\n|'+'|'.join(['---']*len(head))+'|\n'+'\n'.join('| '+' | '.join(str(x) for x in r)+' |' for r in rows)+'\n'
rev=next(x for x in A['reverse'] if x['wacc']==.10 and x['fade_years']==2)
text=f'''# STNG Valoración de flota y precio razonable

Fecha de mercado: 4 de noviembre de 2026. Preparado: 5 de noviembre de 2026. USD millones salvo tarifas diarias, acciones en millones y valor por acción. Estado: screen-grade; revisión independiente aritmética superada y conclusión de no aprobar validada. No hay entrada aprobada ni fair value certificado.

## Conclusión para la decisión

**No aprueba Stage 3 a 85,05 USD. Resultado: mantener en observación y esperar un precio que compense mejor el riesgo.** El caso base de continuidad da **{f(B['per_share'])} USD**, un potencial de **{B['upside']:.1%}** y descuento de **{1-85.05/B['per_share']:.1%}**. Las expectativas actuales son plausibles sin recurrir al bull, pero no se cumplen conjuntamente las condiciones del apartado 12: la rentabilidad esperada no compensa suficientemente esta incertidumbre cíclica. Una variación ordinaria del 5% en tarifas normalizadas borra prácticamente todo el descuento. La confianza en un valor puntual es baja a media, aunque los datos históricos y la aritmética sean sólidos.

El rango central de trabajo es aproximadamente **81–95 USD**, formado por continuidad base y sensibilidades centrales de vida, tarifa y coste de capital. No se llama razonable a todo el intervalo17,88–176,85. El precio actual está dentro de ese rango; eso no implica que ofrezca una compensación atractiva por el riesgo. No se exige automáticamente25%: el umbral se justifica con las sensibilidades de esta compañía.

**Revisar alrededor de 75 USD**, con zona indicativa **72–76 USD**, si no cambia la tesis. Ese nivel se ancla en74,99 USD de valor al reducir10% las tarifas normalizadas del mismo modelo. No se aplica otro recorte porcentual encima de ese escenario. A75, el potencial al base sería27,3% y al caso de tarifas5%menores,13,6%; el adverso sin renovación49,40 seguiría suponiendo una pérdida importante y no es un suelo. El descuento de21,4%frente al base es resultado de este razonamiento, no una regla universal. Alcanzar75 obliga a revisar información y gráfico, no autoriza una compra.

Para reconsiderar85,05 haría falta evidencia más fuerte de ingresos normales duraderos, contratos que los aseguren a costes actuales y disciplina de reposición que evite reinvertir por debajo del coste de capital. Un trimestre spot excepcional, la inversión minoritaria no valorada o un rebote técnico no bastan. La incertidumbre de JV y las acciones restringidas ya emitidas **no son bloqueos fatales artificiales**: el motivo para esperar es precio frente a riesgo económico. Un tamaño pequeño reduce dinero expuesto, no mejora la rentabilidad de la acción.

La mejora frente al dossier anterior es real: inventario de buques, diez años de FCFF, vencimiento de charters, desembolsos comprometidos, renovación de cohortes, terminal con reinversión, WACC explícito, reverse y puente de capital reproducibles. Este avance no obliga a aprobar una candidata. No procede activar Stage3.5 mientras no pase el criterio fundamental.

El dato de mercado es el cierre del 4 de noviembre, 85,05 USD a las 16:00 EST, volumen 894.555, de StockAnalysis. No se confunde con ScannerLast 85,1297. Scanner de noviembre: Opportunity85 y QP80. El paquete técnico usa una captura posterior con volumen894556: una acción más, sin impacto en la decisión. [S03]

## Tres escenarios y la limitación del bear

'''+table(['Caso','Tarifas normalizadas Handy / MR / LR2 / VLCC','WACC','Valor USD','Lectura'],[
 ['Bear continuidad','17k / 21k / 27k / 38k','11,5%',f(R['bear']['per_share']),'Fuerza renovación antieconómica; estrés de mala asignación, no suelo'],
 ['Base continuidad','21k / 27k / 35k / 45k','10,0%',f(B['per_share']),'25 años de vida y reposición a costes actuales inflados'],
 ['Bull con conversión','25k / 33k / 45k / 60k','9,0%',f(R['bull']['physical_conversion']),'Conversión coherente; no usar proxy de opción congelado'],
 ['Bear sin nuevas renovaciones','Mismas tarifas bear','11,5%',f(A['runoff']['bear']['per_share']),'Contraste finito, no una promesa de liquidación ni un mínimo']])+f'''
Los escenarios no tienen probabilidades asignadas ni se promedian. El bull sin ajustar la opcionalidad del convertible arrojaría {f(R['bull']['per_share'])}; se descarta como cifra principal porque subestima la dilución cuando el valor supera el precio de conversión. El bear de continuidad produce EV operativo negativo porque obliga a comprar buques nuevos a rentabilidades inferiores al coste de capital. No debe presentarse como escenario de gestión racional ni como estimación central de pérdidas.

El contraste sin reposición mantiene todos los buques actuales y comprometidos hasta su vida supuesta, después retira capacidad y libera capital circulante. La corrección de revisión elimina ahorros de G&A antes de que empiecen esas retiradas. Aun así, la reducción proporcional de gastos, los valores de chatarra y la ausencia de costes extraordinarios de cierre hacen que **{f(A['runoff']['bear']['per_share'])} no sea un suelo protegido**. No se reemplaza el método FCFF por NAV o un múltiplo.

## Históricos y tarifas sostenibles

El EBIT TTM a septiembre de 2026 es 1.020,0 reportado, pero incluye 418,12 de ganancias por venta de buques. El EBIT sin esas ganancias es **601,88**, frente a **264,38** en el TTM anterior. No se utilizan EPS, EBITDA ajustado o CFO menos diques como owner earnings sostenibles. Las ventas de flota reducen la capacidad que genera beneficios futuros. SBC TTM75,592 permanece como coste económico; no se suma al FCFF. [S01 y dossier histórico auditado]

'''+table(['Año','Handy spot/pool','MR spot/pool','LR2 spot/pool'],[[y,*[f(v[c]) for c in ['Handymax','MR','LR2']]] for y,v in A['historical_tce'].items()])+f'''
Son tarifas nominales, medias anuales de cada clase, no una serie homogénea ajustada por composición. Las medias simples de 2021–25 son 24.714 / 25.602 / 33.184 USD/día. Los niveles base de 21k/27k/35k en USD2026 son plausibles frente a esa historia y a contratos plurianuales existentes, pero no son una media garantizada. MR y LR2 quedan por encima de 2025 (22.349 y 32.297), y muy por encima del mercado deprimido de 2021. El VLCC45k es un supuesto explícito, no una tarifa histórica propia de STNG. [S02,S12,S13,S15]

El base empieza en 2027 con 28k/38k/65k/70k y converge a los niveles normales en 2029. Bear converge en 2028, bull en 2031. Tras esa normalización, tarifas y costes suben 2% nominal, sin crecimiento real de capacidad más allá de las entregas conocidas. La sensibilidad a tarifas cambia el nivel sostenible, no el beneficio de 2026 retrospectivamente.

Para Q4 se usan **los días completos comunicados** por canal: spot/pool LR2 1.025, MR2.919, Handy1.183; time charter1.025/154/91 y bareboat91. El 44%/47%/37% de esos días spot está contratado a181k/56k/40k. El resto usa tarifas Q3 en base, más bajas en bear. No se aplica181k a toda la flota ni a una perpetuidad. Las tarifas netas de time charter comunicadas son32.150/26.100/23.000. [S01]

## Flota y construcción del FCFF

Se reconstruyen los 74 buques por nombre, clase y año. Se excluyen ingresos después de las ventas pendientes de Elysees y Veneto (143 brutos), con entrega supuesta15 noviembre y cobro neto1%gastos aproximadamente1 diciembre. Todos los demás buques vendidos citados en Q3, incluido Dama, ya habían cerrado a más tardar en septiembre; no se suman sus cobros otra vez. Se incorporan17 nuevas unidades propias:5MR,8LR2,4VLCC. Flota madura:14Handy,40MR,31LR2,4VLCC=89. Los ocho VLCC de la JV minoritaria no se consolidan como si fueran buques propios. [S01]

Se respetan los contratos individuales y su expiración; sus tarifas brutas se convierten a netas con1,25% y comisión comercial diaria335USD para MR/Handy,285 para LR2. El bareboat Bosphorus usa12.986 netos y no carga opex ni drydock al propietario durante el contrato; su continuidad hasta2037 está sujeta a renovación anual del programa estadounidense. Las fechas trimestrales exactas no están publicadas y se aproximan, sin cambiar las ventanas oficiales. [S01,S02]

Coste operativo diario inicial:8.058 Handy,8.383 MR,9.433 LR2 y12.000 VLCC (este último supuesto). Incluye la gestión técnica; no se vuelve a añadir. G&A parte de69,936 de gasto sin SBC más78,0 de SBC anualizadoQ3; aumenta0,2 por buque neto por encima de72, e inflación2%. Se añade1% anual de opex por año de edad superior a15 en base. Cinco días de reparación por buque/año después de2027. [S01,S15]

Diques: se emplean11,3 de caja y212días totales de offhire Q4 y19,6/543días en2027, según guía. Desde2028 se infieren revisiones a edades5,10,15 y cada2,5años después, costes1,2/1,5/2,2/3,5m por clase, mayores después de15años, y25días por evento. Las fechas reales de survey por buque no están disponibles. No se confunden pagos de dique con renovación completa de flota. [S01,S02,S15]

Vida25años base/bull y20bear. Es estimación contable de vida útil, no obligación de retirada. Reposición en USD2026:35m Handy (proxy),46,33MR,72,8LR2,135VLCC; los tres últimos tienen ancla en contratos recientes. Valor residual10% del precio de referencia actual, distinto del residual contable de la compra antigua. Sensibilidades de vida20–30 y coste−15%/+30%. Las obligaciones ya contratadas no se vuelven a estimar a estos costes. La reposición discrecional futura se paga en el modelo al entregar el buque, sin anticipos. Adelantar esos pagos un año reduce el valor base3,33USD/acción, a92,12; una anticipación media de1,5años reduce5,11USD, a90,33. Es un riesgo de timing respaldado por la práctica de pagos por hitos de los contratos actuales, no un calendario futuro conocido. Las IRRs de proyectos también se benefician del supuesto de pago a la entrega. [S01,S02,S15]

Todos los **1.295,9** de pagos futuros (incluida la financiación de la participación minoritaria de la JV) se deducen una sola vez del FCFF:45,6Q4;298,2en2027;481,9en2028;379,2en2029;91,0en2030. No se restan otra vez del equity. Los185,7 pagados incluyen Moxie ya entregado; no son caja disponible. El calendario trimestral de2027 se agrega y descuenta a mitad de año, aproximación de timing. [S01]

Impuestos base0%, coherente con la exención de ingresos de transporte y ausencia de carga histórica; sensibilidad2%,5%,15%, sin afirmar que una exención nunca cambie. NWC futuro15%del TCE más reserva operativa de125m escalada por capacidad e inflación; la caja operativa se excluye del efectivo añadido al equity. Se conserva capital de pools39,644 de2025 como proxy con extremos0y65,516. D&A económica no pretende ser un rollforward IFRS exacto; se cancela en FCFF excepto en pruebas fiscales. [S02,S15]

## Diez años de proyección y reinversión

FCFF = NOPAT + D&A − diques − reposición + chatarra − pagos comprometidos − cambio en NWC. No se deducen intereses ni se añade SBC. Los años2027–31 son detalle y2032–36 transición con capacidad, edad y charters explícitos. Q4es un período adicional, no uno de los diez años.

'''+table(['Período','Flota media','TCE','EBIT','Diques','Compromisos','ΔNWC','FCFF'],[[r['year'],f(r['avg_fleet']),f(r['tce']),f(r['ebit']),f(r['drydock']),f(r['committed']),f(r['dnwc']),f(r['fcff'])] for r in B['rows'][:11]])+f'''
La aparente abundancia de caja2031–36 no se perpetúa sin coste. La concentración de buques construidos2014–17 obliga a renovar por unos1.068/1.046/990/890m brutos en2039–42 con vida25. El motor conserva esa edad y simula los flujos posteriores, en vez de sustituirlos directamente por una flota joven uniforme. El PV del ajuste por cohortes frente al Gordon homogéneo es **{f(B['age_adjustment_pv'])}m**, **{f(B['age_adjustment_pv']/P['shares'])}USD/acción**. La cola efectiva supone **{B['terminal_weight']:.1%}** del EV. La cola numérica llega hasta2196; el PV posterior a2180 es0,021m en base, una aproximación inferior a una décima de centavo por acción.

La comprobación independiente del terminal2037 reconstruye capital modelado de buques y NWC por añadas de compra y depreciación, con drydock tratado como mantenimiento. No es capital invertido estatutario total medido independientemente:2.839,44 de buques más357,87 de NWC=3.197,31. El NOPAT operativo370,32 más9,98 de diferencia normal entre chatarra corriente y residual contable histórico produce NOPAT económico380,30. No son ganancias extraordinarias de venta comercial de barcos. Reinversión=2%×3.197,31=63,95; ROIC=380,30/3.197,31=11,89%; FCFF=380,30×(1−2%/11,89%)=316,36. La identidad de capital se verifica desde las añadas, no infiriendo capital sólo como reinversión/g.

Ese ROIC **no prueba que cada compra nueva cree valor**. La revisión independiente calcula IRRs ilustrativas base con costes, diques, overhead y NWC por unidad de6,92%Handy,10,41%MR,10,18%LR2 y6,75%VLCC. Con WACC10%, renovar todas las clases no es una política óptima demostrada. El caso continuidad es una hipótesis mecánica de mantenimiento de flota, no promesa de disciplina de la dirección. Comprar usado, reducir flota o renegociar costes podría cambiar el valor, pero no se añade una prima de “gestión óptima” sin evidencia.

## Descuento en USD

Treasury10años4,90%al4nov; ERP implícitaDamodaran4,41%al1nov. Con beta1,0 elegida, prima específica1,0%, coste de equity10,31%; deuda6,4% estimada y mezcla objetivo90%equity/10%deuda, impuesto0%, WACC9,919%, redondeado10%. Bear11,5%, bull9%, sensibilidad8–12%. La beta y prima específica son juicio explícito; las betas de grupos amplios Marine/Transportation0,66/0,71 sin deuda y corregidas por caja no bastan para calibrar un tanker puro. No se usa una beta bursátil puntual negativa para justificar descuento artificialmente bajo. [S04–S06,S15]

## Puente de equity y capital

'''+table(['Concepto base','USDm'],[['EV operativo',f(B['operating_ev'])],['Caja30septiembre',f(P['cash_reported'])],['Reserva operativa excluida',f(-P['operating_cash_reserved'])],['Ventas pendientes netas PV',f(P['pending_sales_pv'])],['Volare',f(P['volare'])],['Ampera',f(P['ampera'])],['JV dualfuel',f(P['dual_jv'])],['Nueva JV valor incremental',0],['Compra Volare octubre PV',f(-P['post_balance_volare_purchase_pv'])],['Claims host más derivado',f(-P['claims'])],['Equity',f(B['equity'])],['Acciones actuales millones',f(P['shares'])],['Valor por acción',f(B['per_share'])]])+f'''
La versión revisada usa caja y circulante **ambos al30septiembre**, más una previsión de Q4completo. Así evita sumar caja26octubre con liberaciones de circulante desde30septiembre o prorratear reservas de todoQ4 a un stub restante. Los2.051,865 de caja26octubre se utilizan sólo como control: aumento9,777 más inversiónVolare38,4 requiere otros flujos netos48,177 hasta esa fecha; no se presenta como una conciliación de caja real al4noviembre. No se comunicaron pagos de nuevos buques enQ4 hasta26octubre. [S01]

Acciones:51,078851m emitidas y en circulación al26octubre, incluidas restringidas emitidas. No se suma otra vez el total no vested del20-F ni se usa el promedio diluido trimestral como capital actual. Los Form4 de septiembre muestran concesiones en acciones comunes emitidas; el Form4 de julio no demuestra por sí solo RSUs adicionales no emitidas. Una diferencia residual de0,5m o1,5m de títulos se prueba aparte. No hay recompra futura gratuita: caja y acciones bajarían juntas. [S01,S02,S08,S09]

Convertibles:605m de principal,1,75%, vencimientoabril2031,6,0978555m acciones de conversión potencial a99,215USD. El base utiliza522,534 de host contable más banco y196,087 de derivado=718,621, sólo como proxy de claims al30septiembre, no valor de mercado certificado. Par655 sin opcionalidad da{f(B['par_only'])}; principal más derivado como prueba conservadora (no definición de deuda reportada) da{f(next(x['value'] for x in A['claimscases'] if x['claims']==851.087))}. El bull elimina605m de deuda y suma6,0978555m acciones, sin deducir también el derivado. Las elecciones de settlement y la opción temporal requieren una valoración más completa para precisión, pero no justifican doble conteo. [S01,S07]

Volare2,4m acciones≈3,4% aNOK164,60/USDNOK9,2278≈42,81m; su compra38,4m enoctubre se deduce del puente de septiembre. Valorar a coste cambia menos de0,09USD/acción. Ampera12,004 de coste se valora6,002 base y0bear; JVdualfuel11,323 es una conciliación aproximada, no NAVtasado. La JVde ochoVLCC tiene participación<15%y sus aportaciones futuras están incluidas en1.295,9; no se inventan ingresos ni NAV. No se agregan otros activos65,516 encima de inversiones y poolcapital, para evitar duplicaciones. [S01,S10,S11]

El dividendo declarado0,75 con registro13nov y pago4dic está incluido económicamente en el valor cum-dividendo: restarlo de caja sin reconocer el cobro del inversor reduciría artificialmente el valor. Tampoco se trata como dinero gratis.

## Reverse y comprobación relativa

Para justificar85,05 con WACC10%, normalización en dos años y las demás hipótesis base, las tarifas terminales son aproximadamente **Handy{f(rev['rates_current_price']['Handymax'])}, MR{f(rev['rates_current_price']['MR'])}, LR2{f(rev['rates_current_price']['LR2'])}, VLCC{f(rev['rates_current_price']['VLCC'])} USD/día de2026**. Son niveles realistas, no permanencia del pico181k. No constituyen evidencia independiente porque proceden del mismo modelo.

Como control relativo, EV simple con principal y toda la caja no restringida, dividido por EBITTTM sin ganancias de venta, es4,90xSTNG frente a5,79xTORM. El cálculo usa STNG51,078851m×85,05+655−2.051,865 y TORM102,7m×37,62+704,1. Son compañías con flota, exposición, compromisos y fechas de capital diferentes; ambos EBIT son cíclicos. Este contraste no se mezcla con FCFF para crear un objetivo medio ni transforma un múltiplo bajo de pico en señal de compra. [S01,S03,S14]

## Qué puede cambiar la decisión

'''+table(['Prueba aislada sobre base','Valor USD'],[[x['variable']+'='+str(x['input']),f(x['value'])] for x in A['structural'] if (x['variable'],x['input']) in [('life',20),('life',22),('life',30),('replacement_premium',1.15),('replacement_premium',1.3),('tax',.05),('sbc',95),('repair_days',10),('additional_shares',1.5),('jv_value',100)]])+'''
1. Decisivo: aceptar o rechazar el nivel sostenible de TCE y el coste de capital. Un descenso10% de tarifas normales o una vida/coste de reposición más exigente puede borrar el pequeño descuento al base. Son incertidumbres económicas, no un dato contable que pueda certificarse por búsqueda.
2. Decisivo: política de reinversión y costes evitables de una reducción de flota. La perpetuidad de89buques no se justifica sólo con ROIC agregado. La alternativa sin renovación no tiene costes de cierre completos ni garantiza valor de venta.
3. Falta exacta para una valoración completa de capital: porcentaje económico y financiación final de la JVVLCC, waterfall, derechos y posibles garantías adicionales. El enfoque actual carga todos los compromisos divulgados y otorga cero beneficio futuro. La incertidumbre bloquea certificar ese activo, no crea una pérdida adicional conocida fuera de las aportaciones publicadas.
4. Incertidumbre acotada: valor actual del componente opcional del convertible; diferencia de claims100m equivale1,96USD/acción. No hay evidencia de que las concesiones comunes ya emitidas requieran duplicar el denominador. Los estados más completos y la cotización del bono mejorarían precisión.
5. Sensibilidades operativas acotadas: fecha de los surveys posteriores a2027, entrega dentro del trimestre, impuestos y reserva de caja. Deben conservarse visibles, no etiquetarse todas como bloqueos esenciales genéricos.

Para elevar convicción harían falta tarifas sostenibles corroboradas, disciplina visible de nuevas inversiones y un precio/entrada que soporte esos riesgos. Para deteriorar la tesis bastan menor demanda de toneladas-milla, normalización de rutas, nuevas entregas del sector, costes/regulación mayores o reinversión sin rentabilidad suficiente. El próximo control debe mirar TCE realizadoQ4 y coberturaQ1, cierre de las dos ventas, financiación/entregas nuevas y evolución de acciones/SBC. No se presume que este informe garantice rentabilidad ni que el precio tenga que converger al base.

## Reproducción y entregables

El motor de buques es build.py; analyze.py ejecuta reverse y sensibilidades. results.json y los CSV conservan todos los años de la cola. El libro Excel es una exportación personalizada con fórmulas de FCFF, descuento y puente; sus drivers operativos son salidas del motor por buque. No se presenta como banker_formula_workbook ni como un modelo que recalcule buques al editar cualquier celda. La plantilla genérica no representa cohortes, expiración de charters y reposición; no se sustituyó este análisis por una CAGR genérica. La evidencia anterior se mantiene intacta y la versión inicial no revisada se archiva separadamente.

Las pruebas independientes deben acompañar a cualquier uso de las cifras. Los cambios de revisión fueron: balance30septiembre coherente con Q4completo, días de ingresos directamente de guía, gasto de runoff sin ahorros prematuros, capital terminal por añadas y bullconversión coherente. No hay operaciones, publicaciones ni mensajes externos en este trabajo.

## Fuentes

'''
for s in D:
 text+=f"- **{s['id']}** {s['source']} ({s['date']}; {s['label']}). {s['usage']} "+(f"{s['url']}" if s['url'] else '')+'\n'
# Presentation-only spacing. Preserve URLs, source IDs and vessel-class tokens.
import re
protected = {}
def keep(m):
 key = "ZZKEEP" + chr(65 + len(protected) // 26) + chr(65 + len(protected) % 26) + "ZZ"
 protected[key] = m.group(0)
 return key
text = re.sub(r"https?://[^\s]+|\bS\d{2}\b|Q[1-4]|LR2|20-F", keep, text)
text = re.sub(r"([A-Za-zÁÉÍÓÚÑáéíóúñ])(\d)", r"\1 \2", text)
text = re.sub(r"(\d)([A-Za-zÁÉÍÓÚÑáéíóúñ])", r"\1 \2", text)
text = re.sub(r"(%)([A-Za-zÁÉÍÓÚÑáéíóúñ])", r"\1 \2", text)
text = re.sub(r"([,;:])(?=[A-Za-zÁÉÍÓÚÑáéíóúñ])", r"\1 ", text)
text = re.sub(r'([A-Za-zÁÉÍÓÚÑáéíóúñ][,:])(?=\d)', r'\1 ', text)
text = re.sub(r';(?=\S)', '; ', text)
for key, value in protected.items(): text = text.replace(key, value)
for old, new in {"Q4completo":"Q4 completo", "Q4es":"Q4 es", "todoQ4":"todo Q4", "enQ4":"en Q4", "anualizadoQ3":"anualizado Q3", "coberturaQ1":"cobertura Q1", "realizadoQ4":"realizado Q4", "JVdualfuel":"JV dual fuel", "JVde":"JV de", "JVVLCC":"JV VLCC", "ochoVLCC":"ocho VLCC", "NAVtasado":"NAV tasado", "enOCT":"en OCT", "enoctubre":"en octubre", "vencimientoabril":"vencimiento abril", "implícitaDamodaran":"implícita Damodaran", "inversiónVolare":"inversión Volare", "bullconversión":"bull con conversión", "poolcapital":"pool capital", "EBITTTM":"EBIT TTM", "Stage 3.5":"Stage 3.5"}.items(): text = text.replace(old, new)
(ROOT/'report/STNG_valoracion_flotas.md').write_text(text)
print('Report saved',len(text),'characters')
