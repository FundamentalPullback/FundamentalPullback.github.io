from pathlib import Path
import json,html,re
p=Path(__file__).parent;x=json.loads((p/'facts/inputs.json').read_text());r=json.loads((p/'model/results.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text());comp=json.loads((p/'comparables/results.json').read_text());q=x['sources']['q3'];T=h['periods']['TTM_2026_09'];old=h['periods']['TTM_2025_09']
def n(v,dec=2):
 if v is None:return 'No calculado'
 return f'{v:,.{dec}f}'.replace(',','@').replace('.',',').replace('@','.')
def tab(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |'for row in rows)+'\n'
text=f'''# Scorpio Tankers (STNG): beneficios del ciclo, renovación de flota y capital

Corte de información y precio: 4 de noviembre de 2026, después del cierre de EE. UU. Preparación terminada el 5 de noviembre UTC. Investigación parcial condicionada. Revisión independiente completada para este alcance parcial. USD millones salvo precios, fletes diarios y acciones. Sin valoración total, Stage 3 completo ni entrada.

## Conclusión

La mejora operativa de STNG es real, pero el beneficio publicado exagera su magnitud: el EBIT TTM de 1.020,0 incluye 418,1 de ganancias por ventas de buques. Sin esas ganancias, el EBIT es 601,9 frente a 264,4 del TTM anterior. Es una recuperación de un negocio cíclico y una flota menor, no un crecimiento orgánico estable que pueda perpetuarse.

Los 1.396,9 de caja neta de octubre no son íntegramente distribuibles: quedan 1.295,9 de pagos de nuevos buques y de la JV de VLCC. Esos compromisos compran activos y no deben restarse otra vez si ya están en un DCF. El dividendo, la renovación futura, las inversiones minoritarias y el convertible obligan a separar liquidez de valor para el accionista.

Los fletes LR2 de 181.000 dólares diarios cubren sólo el 44% de los días spot previstos para Q4. No son una tarifa de toda la flota ni una hipótesis sostenible a diez años. Este expediente deja el valor total y los precios de entrada vacíos hasta cerrar el modelo de flota, reinversión, fiscalidad y dilución.

Escáner: Last 85,1297, QP 80, Opportunity 85 y RSI 48,6. Cierre regular verificado: 85,05 a las 16:00 EST; volumen 894.555. Se conservan separados. No hay Stage 2 actual, medias móviles ni filtro completo certificados en el CSV. [Precio](https://stockanalysis.com/stocks/stng/history/).

## Negocio y fuentes

Transporte marítimo de productos petrolíferos, con exposición creciente a crudo mediante VLCC propios y participaciones minoritarias. Los ingresos dependen de demanda de transporte, distancias, disponibilidad de flota, fletes, contratos y días operativos. TCE resta gastos de viaje a ingresos, pero no resta tripulación, mantenimiento, G&A ni renovación del activo.

Fuentes principales: [20-F 2025]({x['sources']['fy2025']}), [20-F 2022 y comparativos 2020–2021]({x['sources']['fy2022']}), [resultado Q3 2026]({q}), [Q3 2025](https://www.scorpiotankers.com/scorpio-tankers-inc-announces-financial-results-for-the-third-quarter-of-2025-and-an-increase-to-its-quarterly-dividend/), [Q4 2025](https://www.sec.gov/Archives/edgar/data/1483934/000148393426000012/q42025earnings-exhibit991.htm). Las entradas y fórmulas reproducibles distinguen el dato publicado de diferencias de acumulados. No se usa consenso verificado ni una sorpresa frente a consenso.

## Historia: ciclo completo y comparación reciente

Se muestran seis ejercicios para incluir la contracción de 2021. El perímetro y los arrendamientos cambian: no se comparan niveles de beneficio como si la flota fuera constante. Q4 se contrasta con el resultado publicado; caja trimestral procede de diferencias de acumulados. TTM = FY anterior + 9M actual − 9M anterior. El beneficio sin ventas de buques no elimina otros riesgos o costes económicos.

'''
periods=['FY2020','FY2021','FY2022','FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM_2025_09','TTM_2026_09']
text+=tab(['Periodo','Ingresos','TCE','EBIT publicado','Ganancia buques','EBIT sin ventas','CFO','Capex seco/otros','Buques/construcción','SBC'],[[k]+[n(h['periods'][k][v])for v in ['revenue','tce_revenue','ebit_reported','vessel_sale_gain','ebit_ex_vessel_gains','cfo','drydock_other_capex','vessel_acquisition_capex','sbc']]for k in periods])
text+=f'''
La pérdida por ventas de 66,486 en 2022 se retira con signo negativo: aumenta el EBIT sin ventas. El saneamiento de depósitos de scrubbers de 10,508 en 2023 permanece en el EBIT de esta tabla; no se borra automáticamente. La depreciación de activos arrendados de años anteriores no significa que su principal fuera capex cero: los diagnósticos de caja no homogeneizan arrendamientos ni compras de opciones de buques.

TTM: ingresos +{n((T['revenue']/old['revenue']-1)*100,1)}%, EBIT sin ganancias de ventas +{n((T['ebit_ex_vessel_gains']/old['ebit_ex_vessel_gains']-1)*100,1)}% y CFO +{n((T['cfo']/old['cfo']-1)*100,1)}%. Q3, sin embargo, baja a 116,550 de EBIT sin ventas desde 244,179 en Q2. Los fletes y la menor flota explican por qué una buena variación TTM no certifica un ritmo anual repetible.

## Calidad del EPS y caja

Q3: EBIT publicado 269,100 − ganancia por buques 152,550 = 116,550. Al añadir depreciación 35,208, el EBITDA operativo después de SBC es 151,758. El EBITDA ajustado del emisor, 172,240, excluye SBC y contiene diferencias no operativas; no se usa directamente como caja del propietario.

Beneficio neto Q3: 224,316 − ganancia de ventas 152,550 + pérdida de valoración del pasivo convertible 55,593 = 127,359 ajustado. El EPS diluido IFRS 4,60 y el ajustado 2,49 no se reconcilian sólo restando ganancias por acción: el ajustado usa numerador 136,398 tras añadir 9,039 de gasto financiero convertible y denominador 54,862882 millones. En IFRS Q3 el convertible era antidilutivo, mientras en 9M no lo era. No se suman EPS diluidos trimestrales para fabricar un TTM comparable.

CFO TTM 833,298 − drydock/otros 27,436 − compras/construcción 182,188 = 623,674. Restar además SBC TTM 75,592 deja 548,082 como diagnóstico económico, todavía NO owner FCF: faltan reposición de buques, separación de intereses/impuestos, reinversión y participaciones. Los 1.025,010 cobrados por ventas de buques en 9M están en inversión, no en CFO recurrente. La caja de 9M consume 18,733 por circulante frente a 49,419 en 2025; no extrapolar esa menor salida.

La caída del desembolso de drydock a 27,436 TTM, frente a 104,206 anterior, no demuestra que el negocio necesite permanentemente menos mantenimiento. Menor flota y calendario de inspecciones importan. El capex de 182,188 ya incluye la nueva unidad entregada y anticipos. Los 185,7 pagados hasta octubre son otra fecha y perímetro, incluyendo JV: no sumarlos nuevamente a 182,188.

## Flota, calendario de renovación y contratos

A 26 de octubre había 74 buques: 25 LR2, 35 MR y 14 Handymax, con edad media 10,3 años. Elysees y Veneto permanecían pendientes de venta por 70 y 73. Si cierran, la flota baja a 72. Los 17 nuevos buques propios llevarían el total a 89 antes de otras ventas: cinco MR, ocho LR2 y cuatro VLCC. Los ocho VLCC de la JV NO son ocho buques consolidados de STNG. [Flota y compromisos]({q}).

Entregas previstas: tres MR y dos LR2 en 2027; cuatro VLCC en 2028; seis LR2 en 2029; dos MR en 2030. Son previsiones, no entregas realizadas. El programa conocido de 18 buques, incluyendo Moxie ya entregado, suma aproximadamente 1.368,46 a precios contractuales. La diferencia de unos 113,14 frente a pagos realizados más pendientes no identifica con precisión la participación en JV: redondeos, equipos y perímetro requieren conciliación.

Existen charters de varios años que amortiguan el ciclo, pero sus tarifas nominales no pueden reemplazarse por spot al valorar los años contratados. Ejemplos: Orchard 28.350/día durante cinco años desde agosto de 2025; Rambla 30.500 durante ocho años desde marzo de 2026; Jermyn 42.500 durante tres años desde octubre de 2026. Los MR Bronx y Pontiac tenían contratos de tres años a 23.900 pendientes de comienzo en Q4. Bosphorus está cedido bareboat: el fletador paga sus costes operativos y la participación en el programa estadounidense depende de renovación anual. No extender todos esos contratos automáticamente hasta perpetuidad.

Una vida de 25 años situaría muchas renovaciones de los buques de 2014–2017 después del horizonte explícito de diez años. Una terminal que sólo añada crecimiento y omita esa ola de reposición sobrevaloraría la flota. Hace falta un calendario por cohortes, scrap, costes, off-hire y nueva financiación. La vida de 25 años es una hipótesis económica por evaluar, no una fecha obligatoria de retiro.

## Capital: principal, opción convertible y participaciones

Caja de septiembre 2.042,088; caja no restringida al 26 de octubre 2.051,865. Principal 655 = convertible 605 + crédito bancario 50. El pasivo contable de 718,621 incluye deuda registrada 522,534 y derivado 196,087; no se suman ambos al principal. Revolver no dispuesto 483,2 y facilidad no dispuesta 90 son liquidez potencial, no caja ni patrimonio.

El convertible vence el 15 de abril de 2031, cupón 1,75%. La segunda emisión a prima es financiación ya recibida, no principal adicional. Conversión vigente: 10,0791 acciones por cada 1.000, equivalente a 99,2152 por acción y 6,0978555 millones de acciones. Las condiciones y ajustes futuros importan. El método por defecto combina efectivo para principal y liquidación del exceso, pero el emisor puede elegir efectivo, acciones o combinación conforme al contrato. No es efectivo obligatorio en todos los casos. [Indenture, sección 5.03]({x['sources']['indenture']}).

Acciones emitidas y en circulación al 26 de octubre: 51,078851 millones, incluidas restringidas emitidas. No añadir encima la dilución de restringidas del cálculo EPS. Las RSU no emitidas y otros derechos futuros no están conciliados. Una conversión física completa elimina el derecho de 605 y lleva el denominador a 57,1767065; no restar además el derivado. Para la combinación, una aproximación a precio P es añadir máximo(6,0978555 − 605/P, 0) millones de acciones y mantener principal, pero el contrato usa un periodo de observación de VWAP y condiciones reales. Esto no valora la opción ni certifica conversión actual.

Ejemplos exclusivamente algebraicos con un activo bruto hipotético, sin estimar EV de STNG:

'''
text+=tab(['Activo bruto supuesto','Sólo principal / acción','Conversión física / acción','Combinación aproximada / acción'],[[n(e['hypotheticalGrossAssetValue']),n(e['parOnlyPerShare']),n(e['fullConversionPerShare']),n(e['defaultCombinationPerShare'])]for e in r['convertible']['examples']])
text+='''
Bajo el precio de conversión, la conversión física voluntaria por menos del principal no es el comportamiento económico esperado. Los ejemplos no incorporan valor temporal de la opción, vencimiento, cupón, make-whole ni dilución no emitida. No son escenarios de valoración ni objetivos.

Volare: 38,4 invertidos en octubre, 2,4 millones de acciones y aproximadamente 3,4% del capital. Ampera: 12,004 invertidos a septiembre, no sólo los 10 iniciales. JV VLCC: 7,381 invertidos y aportaciones futuras ya dentro del total de compromisos. JV dual-fuel: valor contable inferido 11,323 desde 13,023 + resultado 2,113 − distribución 3,813, sin asegurar ausencia de otros movimientos. No se valoran por coste automáticamente.

«Otros activos» 65,516 incluye partidas de distinta naturaleza. Los depósitos de pools son circulante operativo, no caja libre. No añadir el total y después cada inversión separada. El valor de las participaciones, su financiación y el cobro de pools posterior a octubre necesitan conciliación. Los 143 de ventas pendientes sólo se añaden al retirar los dos buques del valor operativo, con gastos/tributos de venta; nunca junto a los mismos buques o su valor contable de 72,804.

## Liquidez y pagos pendientes

'''
text+=tab(['Periodo','Pagos de buques/JV pendientes'],[[v['period'],n(v['amount'])]for v in x['commitments']['schedule']]+[['Total',n(1295.9)]])
text+='''
Caja 2.051,865 − principal 655 − todos los compromisos 1.295,9 = 100,965. Es un ejercicio de reserva de liquidez, NO NAV ni valoración: descuenta anticipadamente obligaciones con fechas distintas y omite la caja futura y el valor de los activos adquiridos. Dividendo anunciado de 0,75, pagadero el 4 de diciembre con registro el 13 de noviembre, equivale a 38,309 con el número de acciones de octubre, que puede cambiar. Reservar además 250 operativos, selección analítica, deja −187,344 antes de caja futura o ventas. Esto no implica insolvencia ni déficit de financiación inmediato: no hay principal programado antes de 2028 y existen ingresos operativos y facilidades.

No se deduce este total de compromisos del puente si luego se introduce otra vez como capex en un DCF. Drydock previsto: 11,3 en Q4 y 19,6 en 2027, con fechas sujetas a cambios. Un dividendo anualizado de 3,00 no es una promesa de distribución constante. Recompras autorizadas restantes de 445 no equivalen a ejecución ni a incremento de valor gratis.

## Sensibilidad económica, sin sustituir al DCF

El siguiente ejercicio NO calcula flujo de caja futuro, valor intrínseco ni owner FCF. Aísla cuánto cambia un excedente anual indicativo según fletes y carga de reposición. Usa flota hipotética después de las dos ventas, 72, o después de todos los nuevos buques propios, 89; no mezcla ambas con el balance actual como si hubieran ocurrido.

Supuestos en dólares de 2026: 350 días de ingreso y 365 de opex por buque; un MR bareboat con ingreso 12.986/día y sin opex a cargo de STNG. Opex por día: Handy 8.058, MR 8.383, LR2 9.433, observados Q3; VLCC 12.000, hipótesis. G&A 160 incluye SBC. Drydock 0,4 por buque/año, hipótesis suavizada. Reposición: (precio de nuevo buque × 90%)/25 años, con precios MR 45, LR2 72,8, VLCC 135 y Handy 35. Los tres primeros tienen referencias contractuales; Handy, residuo 10% y vida de 25 años son supuestos, no tasaciones. Se aplica un estrés fiscal del 2% sólo al excedente positivo, no un tipo estatutario certificado.

Esta reserva económica suavizada NO es capex real. No puede deducirse además del mismo gasto de reposición en un DCF; tampoco resuelve la ola de renovaciones ni las tarifas contratadas. No incluye nuevo gasto de expansión ni financiación, y no atribuye retorno a las participaciones. Sirve para mostrar por qué el cash break-even declarado por la empresa no mide el coste económico completo.

'''
text+=tab(['Caso de fletes','Handy/día','MR/día','LR2/día','VLCC/día','Excedente 72 buques','Excedente 89 buques'],[[k]+[n(a,0)for a in rates.values()]+[n(r['economicBreakEvenCases'][k][scope]['economicSurplusAfterSelectedTax'])for scope in ['postSale72','afterAllDirectNewbuild89']]for k,rates in x['economicBreakEvenAssumptions']['selectedClassRates'].items()])
text+=f'''
En el ejercicio de 72 buques, opex anual {n(r['economicBreakEvenCases']['base']['postSale72']['operatingCost'])}, G&A 160, drydock 28,8 y reposición {n(r['economicBreakEvenCases']['base']['postSale72']['annualEconomicReplacementCharge'])} exigen un TCE uniforme aproximado de {n(r['economicBreakEvenCases']['base']['postSale72']['uniformDailyTCEBreakEven'],0)} al día para los buques no bareboat. No es el break-even de caja reportado por STNG y no lo contradice: contiene otras cargas, otro perímetro y supuestos propios.

'''
text+=tab(['G&A supuesto','Vida económica supuesta','TCE uniforme de equilibrio','Excedente con tarifas base'],[[n(e['GNA'],0),e['lifeYears'],n(e['breakEvenDailyTCE'],0),n(e['surplus'])]for e in r['breakEvenSensitivity']])
text+='''
El soporte añade sensibilidad a días de ingreso, coste de nuevos buques, opex, valor residual y estrés fiscal. No se interpretan los extremos como probabilidades. Se conserva nulo el valor total: falta el FCFF de diez años con cinco años detallados y cinco de transición, coste de capital, terminal con reinversión, valoración inversa y comparables homogéneos exigidos por el plan. Un DCF de vida finita por buques puede ser un contraste útil, pero no sustituir sin explicar el marco principal acordado.

## Q4: qué cubren realmente las reservas

Las tarifas comunicadas corresponden a reservas sobre parte de los días spot esperados. LR2: 181.000 y 44% de 1.025 días; MR: 56.000 y 47% de 2.919; Handy: 40.000 y 37% de 1.183. El resto queda por fijar. Se añaden los días y tarifas de time charter y bareboat del mismo cuadro, no se aplica spot a toda la flota.

'''
text+=tab(['Tarifa supuesta para días sin fijar','TCE Q4 aritmético'],[[e['case'],n(e['TCERevenue'])]for e in r['q4BookingArithmetic']])
text+='''
La referencia Q3 usa spot de 72.283 LR2, 31.183 MR y 24.253 Handy para los días sin fijar; no el TCE total mezclado. Estos cálculos no son guía del emisor. Incluso el caso de cero en días no fijados no constituye un mínimo garantizado: pueden cambiar off-hire, disponibilidad, calendario, costes de viaje y cumplimiento de contrapartes. No se convierte este trimestre en terminal.

## Comparación sectorial, debate y precio

'''
text+=tab(['Empresa','TCE diario Q3','TCE diario año anterior','Variación','Fuente'],[[v['ticker'],n(v['dailyTCE'],0),n(v['priorDailyTCE'],0),n(v['dailyTCEGrowth']*100,1)+'%',f"[Resultado]({v['source']})"]for v in comp['comparisons']])
text+='''
TORM permite contrastar la fuerza del ciclo, no importar un múltiplo. Mezcla de buques, cobertura, edades, deuda y pagos de nuevas JV difieren. TORM tenía 704,1 de deuda neta calculada sin caja restringida a septiembre, frente a caja neta de STNG a octubre. Sus 615,3 de capex comprometido no incluyen una nueva JV cuantificada; los 1.295,9 de STNG sí incluyen su JV VLCC. Comparar esos totales sin ajustar induciría a error. No hay mediana de EV/EBIT homogénea ni precio objetivo derivado del NAV de TORM.

La acción cerró a 95,07 el 29 de octubre y 85,05 el 4 de noviembre: caída de aproximadamente 10,5% después de una reacción inicial favorable a resultados. Esa secuencia no identifica por sí sola la causa. El efecto de normalización de fletes, toma de beneficios o percepciones macro es una hipótesis, no una noticia causal demostrada. No se atribuye el retroceso únicamente a una empresa deteriorada ni únicamente al mercado.

La llamada del 28 de octubre aporta contexto, no sustituye las cuentas. En Q&A, Stephanie Moore (Jefferies) preguntó por demanda y cobertura: James Doyle defendió exportaciones y reposición de inventarios; Robert Bugbee y Lars Nielsen describieron contratación oportunista. Liam Burke (B. Riley) preguntó por LR2 en crudo; Nielsen indicó que permanecerían mientras los diferenciales lo justificaran. Lectura favorable: flexibilidad y demanda. Objeción: spot y mezcla pueden revertir. Pruebas futuras: fletes fijados, días productivos, nuevas coberturas y caja cobrada. [Transcripción](https://stockanalysis.com/stocks/stng/transcripts/719821-q3-2026/).

El contexto comunicado por el emisor incluye alteraciones de rutas por Oriente Medio, recuperación de exportaciones y buques LR2 dedicados a crudo. Son factores para vigilar, no una garantía de escasez permanente. Reapertura de rutas, menor demanda de productos, retorno de LR2 al mercado limpio, entregas del sector y costes regulatorios pueden reducir márgenes. Los pools y gestores relacionados requieren vigilar comisiones, saldos por cobrar y conflictos. La exención fiscal del transporte internacional depende de requisitos; no se certifica tributación nula permanente.

## Calendario, pruebas pendientes y decisión

El calendario primario consultado muestra la llamada de Q3 del 28 de octubre, sin fecha exacta del siguiente resultado confirmada. Registro del dividendo el 13 de noviembre y pago el 4 de diciembre no son resultados. No se libera el filtro de calendario con una estimación de terceros. [Eventos](https://www.scorpiotankers.com/investor-center/events/).

Para completar Stage 3:
1. Conciliar flota por cohortes y calendario de reemplazo, contratos y off-hire; separar capex de JV y de buques propios sin doble cargo.
2. Construir FCFF a diez años con fletes normalizados, G&A con SBC, fiscalidad, capital circulante y reinversión terminal; contrastar con vida finita y fletes exigidos por el precio.
3. Cerrar acciones, RSU no emitidas, opción convertible, caja posterior, ventas pendientes y valor de participaciones; verificar fuente de fondos y vencimientos.
4. Homogeneizar comparables e historia de múltiplos y verificar próxima convocatoria. La técnica se revisa aparte antes de Stage 3.5.

Decisión: investigación parcial en observación. No hay valor conservador, central o favorable de la acción, máximo de compra, stop, entrada aprobada ni cantidad nueva autorizada. Los ejercicios de fletes y de liquidación convertible son diagnósticos, no sustitutos de una valoración completa.
'''
(p/'report.md').write_text(text)
# HTML is deliberately self-contained; source tables remain readable on narrow screens.
parts=[];lines=text.splitlines();i=0
while i<len(lines):
 line=lines[i]
 if line.startswith('|'):
  group=[]
  while i<len(lines) and lines[i].startswith('|'):group.append(lines[i]);i+=1
  heads=[v.strip() for v in group[0].strip('|').split('|')];body=[]
  for row in group[2:]:body.append('<tr>'+''.join('<td>'+html.escape(v.strip())+'</td>'for v in row.strip('|').split('|'))+'</tr>')
  parts.append('<div class="table"><table><thead><tr>'+''.join('<th>'+html.escape(v)+'</th>'for v in heads)+'</tr></thead><tbody>'+''.join(body)+'</tbody></table></div>');continue
 if line.startswith('# '):parts.append('<h1>'+html.escape(line[2:])+'</h1>')
 elif line.startswith('## '):parts.append('<h2>'+html.escape(line[3:])+'</h2>')
 elif line:parts.append('<p>'+re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',html.escape(line))+'</p>')
 i+=1
(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>STNG · Investigación parcial</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#15302f;background:#f5f4ee;margin:0;padding:32px}main{max-width:1080px;margin:auto}h1{font-size:40px;line-height:1.15;color:#103d3b}h2{margin-top:48px;border-top:2px solid #b7c7bf;padding-top:20px}p{max-width:920px}.table{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;background:#fff;font-size:13px;width:100%}td,th{text-align:right;padding:9px;border-bottom:1px solid #d9e0dc;white-space:nowrap}th{background:#153d3a;color:#fff}td:first-child,th:first-child{text-align:left}a{color:#006c67}@media(max-width:600px){body{padding:18px}h1{font-size:29px}}</style><main>'+''.join(parts)+'</main></html>')
print('Report and self-contained HTML generated')
