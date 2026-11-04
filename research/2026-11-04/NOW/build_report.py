import json
from pathlib import Path
P=Path(__file__).resolve().parent
j=lambda f:json.loads((P/f).read_text())
m=j('model/results.json');s=j('model/sensitivities.json');rates=j('model/rates_results.json');h=j('history/history.json');b=m['base'];i=j('model/inputs.json')
f=lambda n:format(n,',.2f').replace(',','X').replace('.',',').replace('X','.')
get=lambda p,k:next((r['value'] for r in h if r['period']==p and r['metric']==k),None)
Q='https://www.sec.gov/Archives/edgar/data/1373715/000137371526000096/now-20260930.htm';K='https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm';E='https://www.sec.gov/Archives/edgar/data/1373715/000137371526000092/erq3fy26.htm'
r=f'''# ServiceNow (NOW): crecimiento fuerte, pero la remuneración en acciones y las compras también cuestan

Investigación propia del 4 de noviembre de 2026. Precio de referencia: **109,16 USD, cierre del 3 de noviembre**. Estados financieros: septiembre de 2026, publicados tras resultados del 28 de octubre. Cifras en USD millones, salvo acciones y porcentajes. **Investigación revisada y condicionada; sin aprobación de entrada ni Stage 3.5.**

## 1. Conclusión y observaciones del registro

El modelo de FCFF después de SBC produce **{f(m['bear']['valuePerShare'])} / {f(b['valuePerShare'])} / {f(m['bull']['valuePerShare'])} USD** por acción en escenarios adverso/base/favorable. Frente a 109,16 de cierre, el potencial calculado al central es {f(b['upsideToReferenceClose']*100)}%. El rango no tiene probabilidades asignadas ni es un intervalo estadístico. El favorable requiere crecimiento más prolongado, margen más alto después de SBC, reinversión eficiente y menor descuento; no basta con que el negocio siga creciendo cerca del 20% durante un trimestre.

El atractivo comercial de la plataforma no demuestra que la acción esté barata después de una caída. Esperar mejor relación precio/valor o evidencia que sostenga una trayectoria más favorable. No se propone compra, venta, tamaño de posición ni stop. La valoración refleja supuestos explícitos sobre integración, capital y márgenes, no un consenso o una predicción puntual.

A098 registró el 23 de octubre 158,87, QP 90, Opportunity 100, RSI 70 y s2 «Sí». La última fila real es del 28 de octubre: Last 123,73, QP 100, Opportunity 100, RSI 56,5 y **s2 vacío**, no «Sí» ni «No». A112 ya documentó el contraste entre ese Last CSV 123,73 y cierre 150,13. La discrepancia no tiene conciliación primaria de fecha/ajuste: se conserva el registro literalmente, sin llamarlo cierre de esa sesión ni heredar el s2 anterior. El cierre separado del 3 de noviembre es 109,16. [Precios históricos](https://stockanalysis.com/stocks/now/history/). El split 5:1 de diciembre de 2025 no explica por sí solo una diferencia entre dos cotizaciones de octubre de 2026.

## 2. Franquicia, visibilidad y lo que no demuestra el backlog

ServiceNow integra workflows, datos y controles de acceso en una plataforma empresarial. La implantación en procesos críticos, costes de migración, ecosistema de integradores y contratos recurrentes respaldan continuidad comercial. El Q3 registró ingresos 4.106 (+20,5%), suscripción 3.988 (+21%), cRPO 13.650 (+20,5%) y RPO 29.700 (+22%). Hubo 19 operaciones con más de 5 de nuevo ACV y 680 clientes con ACV superior a 5, aproximadamente 23% más. La empresa elevó su objetivo de ACV de IA de 2026 a 1.700. **ACV no es ingreso reconocido ni caja del año**. [Resultados Q3]({E}).

La renovación del 98% es una medida basada en ACV de cuentas perdidas frente a renovadas, no retención neta de dólares ni porcentaje de clientes. Generalmente no refleja aumentos o reducciones de compra si la cuenta sigue activa. Por tanto, una reducción de asientos o consumo puede deteriorar la economía sin aparecer inmediatamente como churn en ese 98%. Los contratos cloud se reconocen durante el plazo; self-hosted puede reconocer una parte sustancial al entregar el software. No todos los ingresos de suscripción tienen idéntica cadencia. [Definiciones y reconocimiento]({Q}).

cRPO es la parte de obligaciones a reconocer en 12 meses, no ARR, cobro garantizado ni cartera íntegramente no cancelable en todo escenario. Los contratos federales de 12 meses, con mayor contratación en Q3, generan variabilidad de cRPO posterior hasta renovarse. La guía de Q4 es crecimiento cRPO 18,5%, frente al 20,5% observado en Q3; no se etiqueta toda diferencia como pérdida de demanda sin separar moneda, duración y renovación federal. La guía de suscripción Q4 es 4.245–4.255, +22,5–23% reportado y 21,5% en moneda constante. No se ha verificado una previsión primaria de crecimiento para 2027.

La IA puede ampliar monetización y gobierno de procesos, pero también cambiar precios por asiento, interfaces, competencia y costes de inferencia. Las alianzas anunciadas con OpenAI, Google y NVIDIA son hechos comerciales, no garantías de ingresos incrementales. El modelo no capitaliza por separado una cartera de IA además de los ingresos consolidados, ni convierte declaraciones promocionales en una ventaja permanente.

## 3. Historia: crecimiento de ventas no equivale a crecimiento de caja económica

|Periodo|Ingresos|EBIT GAAP|NI|CFO|Capex PP&E|SBC en P&L|FCF simple menos SBC|
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for per in ['FY2023','FY2024','FY2025','Q4-2025','Q1-2026','Q2-2026','Q3-2026','TTM-September-2025','TTM-September-2026']:
 r+='|'+per+'|'+'|'.join(f(get(per,k)) if get(per,k) is not None else 'no separado' for k in ['revenue','ebit_gaap','net_income','cfo','capex_ppe','sbc_pnl','fcf_less_sbc_pnl'])+'|\n'
r+=f'''
La historia incluye 436 observaciones con fuente primaria y 457 filas derivadas, tres ejercicios, cuatro trimestres, TTM frente al anterior y balances. TTM = FY2025 + 9M2026 − 9M2025. EBIT GAAP se reconcilia como 1.824 + 1.050 − 1.381 = 1.493; no se sustituye por el operating income estandarizado de un proveedor. Ingresos TTM 15.431 frente a 12.667; EBIT 1.493 frente a 1.755: crecimiento no implica apalancamiento operativo favorable en este corte. [10-K]({K}); [10-Q]({Q}).

SBC de P&L TTM 2.340 frente a 1.915. El ajuste de SBC en CFO es 2.323, no exactamente 2.340; se preservan ambos sin forzarlos a coincidir. CFO 5.334 − capex 584 = 4.750; restar el coste económico P&L de SBC deja 2.410, frente a 2.043 anterior. **Este último es una aproximación de propietario, no FCFF exacto**: conserva interés, impuestos y circulante reportados. El cash withholding 456 sobre liquidaciones netas de equity en 9M no se resta otra vez si se reconoce el coste completo de remuneración; tampoco convierte SBC en coste nulo.

En 9M26, CFO 3.096 cayó frente a 3.206, mientras capex 346 bajó frente a 630. El FCF ajustado del emisor 3.121 añade 371 de cash costs de combinaciones/otros relacionados a CFO menos capex 2.750. En Q3, FCF simple 839 − 91 = 748 frente FCF ajustado 822, por un addback 74. La guía anual 36% de margen FCF utiliza esa definición ajustada, no caja económica después de remunerar empleados con acciones. [Conciliación del emisor]({E}).

FY2023 NI 1.731 incluye gasto fiscal negativo 723 y liberación de valuation allowance aproximadamente 1.050; no perpetuar ese margen neto. En 9M26 hubo beneficio discreto 51 por liberar una allowance de California y ganancias no realizadas 367 en inversiones estratégicas. Los shortfalls fiscales de SBC también afectan al tipo efectivo. El DCF usa 25% normalizado, sensibilidad 20–30%, sin convertir activos fiscales 804 en caja adicional automática.

### D&A, software y comisiones

D&A total en CFO TTM 1.267; amortización adquirida 535; depreciación PP&E 608. El residuo 124 **no está clasificado de forma concluyente**, y no se añade a FCFF como si fuera depreciación física. PP&E incluye software: gross software 170 en septiembre frente a 126 en diciembre. Los 584 de capex son compras totales PP&E; no se inventa una partida separada de internal-use software. Software vendido/arrendado/comercializado se lleva a R&D porque la ventana de capitalización fue inmaterial, según política anual.

Comisiones capitalizadas pagadas 885 frente amortización 686: diferencia 199, no un beneficio gratis. El margen operativo mantiene la amortización de comisiones; el DCF resta solo la inversión neta adicional necesaria, sin volver a restar toda la comisión en efectivo y su amortización. El modelo selecciona 10% del incremento de ventas como inversión neta en comisiones, frente al 199/2.764 ≈ 7,2% observado, cuya base mezcla adquisiciones y calendarios. Es una hipótesis, no un ratio contractual fijo.

## 4. Adquisiciones: no mezclar crecimiento, gastos y contraprestación

Moveworks cerró el 15 de diciembre de 2025 por 2.407: equity 1.467, efectivo 905, préstamo preexistente 31 y awards precombinación 4. Casi todo FY25 excluye su actividad. Armis cerró el 20 de abril de 2026 por 7.637 en efectivo y Veza el 2 de marzo de 2026 por 1.237 sustancialmente en efectivo; otras cinco compras de 2026 sumaron 612. El desembolso neto por adquisiciones 9M fue 9.167. Es capital consumido, no gasto operativo ajustable ni un pago futuro que restar de nuevo a la caja de septiembre.

La empresa no presenta proforma operativo 2026 porque considera inmateriales los efectos sobre resultados consolidados, pero esa afirmación no hace inmateriales deuda, goodwill o amortización: goodwill subió de 3.578 a 10.012 y activos intangibles netos de 1.121 a 3.594. No se inventa crecimiento orgánico exacto a partir de esa frase. El retorno de estas compras debe probarse con beneficios/caja, no con el importe del goodwill.

Los gastos de adquisición 9M de 118 se registraron en G&A. Además, 211 de compensación diferida para empleados clave se reconocieron en activos y se amortizan a R&D durante el servicio: **es un prepago, no deuda adicional de 211**. No se eliminan automáticamente todos los 371 de cash costs ajustados ni toda la retención por ser «no recurrentes». Severance 9M de 167, pagos 153 y pasivo 34 se distinguen; el programa esperado hasta 2026 no asegura que nunca vuelva a haber reestructuración. [Note 5 y Note 15]({Q}).

El modelo normaliza gradualmente el margen después de SBC y de gastos operativos de integración, pero antes de amortización adquirida. No pronostica compras nuevas de 9.167 cada año ni supone que nuevas adquisiciones sean gratis: cualquier deal material futuro obliga a rehacer crecimiento, capital y dilución. La reinversión genérica para crecimiento no equivale a un presupuesto detallado de M&A.

## 5. Construcción del DCF: beneficio después de SBC y crecimiento financiado

Ancla 2026 de ingresos 16.233 = 9M reportado 11.863 + punto medio de la guía de suscripción Q4 de 4.250 + 120 seleccionados para otros servicios. **No es guía de ingresos totales de la compañía**. Margen normalizado inicial = (1.493 EBIT GAAP + 535 amortización adquirida)/15.431 = 13,14%; no incorpora addback de SBC, severance o todos los costes de compra.

Se proyectan diez años 2027–2036: cinco de expansión y cinco de desaceleración. Margen aquí significa beneficio operativo **después de SBC, R&D y amortización de comisiones, antes de amortización adquirida**. El margen 2027 base del 15% sube al 20% en 2031 y al 23% en 2036. Como lectura de sus exigencias, SBC económico memo parte del 15% de ventas y termina en el 12%; el margen antes de SBC implícito termina en el 35%, no en el 23%. Estos porcentajes futuros son selección analítica, no guidance ni una reclasificación de SBC como caja.

Los nuevos Leadership Awards del 26 de octubre suman 126,55 de valor objetivo para cinco directivos nombrados; el total de todos los receptores y el número exacto de shares no se divulgaron aquí. Vesting 25%/35%/40% en 2027/28/29, condicionado al empleo. Se carga económicamente 126,55 en tres importes iguales en 2027–2029 **adicionales** al margen operativo seleccionado, sin afirmar que sea el calendario GAAP de reconocimiento. No se deduce a la vez 126,55 del puente de equity ni se estima un número de acciones con un precio de concesión supuesto. [10-Q, Item 5]({Q}).

La amortización adquirida se presenta como memo GAAP: 783/730/702/649 en 2027–2030 según el calendario reportado; los 533 restantes se distribuyen 300/150/83 únicamente para presentación. **Cambiar ese memo a cero no cambia el valor**. Se grava el beneficio antes de amortización al 25% y no se atribuye un tax shield desconocido a activos adquiridos. Eso no prueba que todas las deducciones fiscales sean cero; evita inventarlas. R&D y sustitución del producto siguen como coste operativo, no se asume que una tecnología dure para siempre gratis.

FCFF = NOPAT + depreciación PP&E − capex PP&E − inversión neta en comisiones − ΔWC − otra reinversión para crecimiento. Depreciación PP&E del 4% de ventas y capex en efectivo mínimo del 4,5%; comisiones netas del 10% del incremento de ventas y otro WC del 2% del incremento. El capex en efectivo nunca cae por debajo de la depreciación PP&E: la sensibilidad del 3,5% queda limitada por el suelo de reposición del 4%, sin liberación perpetua de activos. No se asume liberación cuando ventas caen, ni financiación perpetua adicional gratis por deferred revenue. La reinversión neta es el máximo entre ese suelo físico/comisiones/WC y **aumento positivo de NOPAT/ROIC**; se financia también la expansión de margen, no solo las ventas. El excedente es otra inversión de crecimiento explícita, no un capex anunciado por la empresa.

ROIC incremental del 35% en el caso base es una exigencia optimista de inversión orgánica ligera, no el retorno histórico incluyendo Armis/Moveworks ni una prueba de que esas compras ya rentan un 35%. R&D y comercialización ya están en el margen; ROIC modela capital adicional no expensado. Sensibilidad 15–100% permite evaluar esta selección. El crecimiento no queda gratis por llamar al negocio «capital-efficient».

|Hipótesis|Adverso|Base|Favorable|
|---|---:|---:|---:|
|Crecimiento 2027|12%|18%|22%|
|Crecimiento 2031|6%|11%|15%|
|Crecimiento 2036|2%|3%|5%|
|Margen 2027 después de SBC, antes de nuevos Awards|12%|15%|17%|
|Margen 2031|15%|20%|24%|
|Margen 2036|18%|23%|28%|
|WACC|10,5%|9,5%|8,5%|
|g terminal|2%|3%|3,5%|
|ROIC incremental|20%|35%|50%|

Treasury 10Y del 3 de noviembre al 4,95%, ERP del 1 de noviembre al 4,41% y beta 5Y de 0,99 dan Ke del 9,3159%. El ERP mensual usó Treasury al 5,29%, por lo que no es una prima implícita sincronizada con el 3 de noviembre. Peso de deuda seleccionado del 7%, spread de 120 pb, Kd del 6,15% e impuestos del 25% producen un WACC mecánico del {f(rates['mechanicalWacc']*100)}%; se elige el 9,5%, colchón discrecional de {f(rates['discretionaryBufferBp'])} pb, no redondeo. No se presenta el 4,05% del commercial paper de septiembre como coste de deuda fijo para siempre. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve); [ERP](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm); [beta](https://stockanalysis.com/stocks/now/statistics/).

FY2027 se descuenta 423/365 años desde el 3 de noviembre. Stub de 58 días usa flujo anual normalizado del ancla 2026, no el Q4 estacional de cobros; base {f(b['valuePerShare'])} con él frente a {f(s['calendar']['withoutStub'])} sin él. Descontar incorrectamente la primera anualidad a un año daría {f(s['calendar']['incorrectOneYearDiscountIllustration'])}. Es estimación temporal, no caja verificada de octubre/noviembre.

Terminal: NOPAT crece a g y reinversión = max(g × NOPAT/ROIC, capex neto físico + comisiones + WC de la expansión). Da FCFF terminal base de {f(b['terminalFcff'])}. Su valor actual supone {f(b['terminalFractionEnterprise']*100)}% del EV, de modo que duración del crecimiento, margen y descuento dominan. No se usa un múltiplo de salida para ocultar el supuesto.

|Año|Ingresos|EBIT antes de amortización adquirida, después de SBC|NOPAT|Depreciación PP&E|Capex PP&E|Comisiones netas|WC|Otra reinversión|FCFF|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for row in b['rows']:
 r+='|'+str(row['year'])+'|'+'|'.join(f(row[k]) for k in ['revenue','ebitBeforeAcquiredAmortAfterSbc','nopat','ppeDepreciation','cashPpeCapexFloor','netCommissionInvestment','otherWcInvestment','additionalGrowthInvestment','fcff'])+'|\n'
r+=f'''
## 6. Capital, compromisos y denominador

Caja 2.393 + valores corrientes 2.214 + valores no corrientes 2.354 = 6.961; efectivo restringido 12 excluido. Inversiones estratégicas 2.050 son principalmente privadas, no caja: se aplica recuperación seleccionada del 50% neta de liquidez/impuestos = 1.025, sensibilidad 0/50/100%; no una tasación ni probabilidad demostrada. Ganancias contables 367 no entran de nuevo en operación ni se suman aparte. Deuda principal 7.600 frente a valor contable de 7.524: diferencias de descuento y costes no hacen desaparecer el principal.

|Puente base|USD millones|
|---|---:|
|EV por DCF|{f(b['enterpriseValue'])}|
|Caja y valores negociables|6.961,00|
|Valor seleccionado inversiones privadas|1.025,00|
|Deuda principal|−7.600,00|
|Reserva operativa de caja|−1.500,00|
|UTB registrado|−197,00|
|Severance pendiente|−34,00|
|Capital posterior desconocido|0,00|
|Equity|{f(b['equityValue'])}|
|Acciones seleccionadas, millones|1.050,00|
|Valor por acción|{f(b['valuePerShare'])}|

La reserva de 1.500 es prudencia analítica, no caja legalmente restringida identificada. El pasivo de deferred revenue de 7.733 no se resta íntegro como deuda: el coste de prestar el servicio permanece en FCFF y no se añade financiación futura gratis por crecimiento del pasivo. Arrendamientos operativos de 891 permanecen como gasto operativo, no como deuda añadida además del gasto. Financiación de proveedores de 18 sigue en cuentas por pagar, no nueva financiación financiera sumada otra vez. UTB 197 está registrado; DTA 804 no se suma como caja. Otros pasivos amplios no permiten certificar un puente actuarial/fiscal completo de cada jurisdicción.

El préstamo Armis de 4.000 de abril se repagó en mayo con notas: no contar préstamo y notas simultáneamente. Notas de 5.500 y commercial paper de 2.100, con 62 días de vencimiento ponderado en septiembre, requieren gestión de liquidez; revolver de 3.000 no utilizado no es activo. ASR de 2.000 de enero se liquidó en Q1 con 18,5 millones de acciones a 107,97 de media; las 1,6 millones adicionales por 225 y la reserva de recompra de 4.200 ya están reflejadas o son autorización, no nuevas acciones retiradas a imputar al modelo.

Las 1.037,917 millones de acciones son las emitidas menos tesorería del 30 de septiembre; media ponderada diluida Q3 de 1.043,011. Base usa 1.050 millones, guía diluida Q4, no tabla de capitalización exacta del 3 de noviembre. Sensibilidades 1.037,917/1.043,011/1.050/1.070/1.090. Los 41,808 millones de RSU y 6,9 de opciones no se agregan indiscriminadamente encima de un denominador diluido que ya captura parte. La remuneración futura se mantiene como coste económico; no se supone que buybacks eliminen ese coste sin consumir capital. Todos los datos históricos de acciones/EPS se ajustan al split 5:1 del 18 de diciembre de 2025.

Compromisos cloud: 262 para el resto de 2026, 432 en 2027, 606 en 2028, 737 en 2029 y 2.800 en 2030; equipamiento IT de 1.600 hasta 2030. Los pagos no coinciden necesariamente con consumo de servicios. Leases no iniciados 355. No se resta todo como deuda además de costes/capex, pero la caída de capex actual no demuestra ausencia de necesidades de compute. Se estresa capex hasta el 6% de ventas y capital adicional. Las cifras son obligaciones contractuales, no gasto añadido automáticamente al margen ya modelado. [Note 18]({Q}).

La investigación del DOJ relacionada con contratación y posible conflicto en un contrato gubernamental sigue abierta, sin resultado ni importe estimable. No se afirma que haya fraude probado, cierre favorable o una multa concreta. Un impacto sobre contratos/gobierno podría exceder una reserva monetaria arbitraria; sensibilidad adicional de 250/500 solo ilustra capital, no estima ese caso.

## 7. Comparables con SBC retenida, sin target de mediana

NOW, como referencia propia: EV de 113.938,01972 millones = 109,16 × 1.037,917 + 7.600 − 6.961. Con SBC retenida, equivale a 76,3148x EBIT GAAP y 56,1825x EBIT antes de amortización adquirida. Las inversiones privadas no se deducen del EV principal; la sensibilidad de recuperación del 50%, equivalente a 1.025, reduce el EV, pero no constituye una valoración probada. El cálculo usa las acciones al cierre de septiembre, frente a los 1.050 millones de la guía usados en el DCF: la diferencia es intencional. Es un screen con balance fechado, no un EV exacto de noviembre. Cálculo exacto en comps/now_screen.json. [10-Q de NOW]({Q}); [precio histórico](https://stockanalysis.com/stocks/now/history/).

CRM y WDAY son referencias de software empresarial con diferencias de producto, crecimiento y adquisiciones. Cierres del 3 de noviembre: CRM 222,20 y WDAY 197,94. Sus últimos balances publicados son de julio de 2026 y acciones de portada de agosto, mientras NOW ya tiene septiembre. La comparación usa tasas de amortización adquirida separadas y **retiene SBC**; no mezcla EBITDA no GAAP sin remuneración con GAAP de NOW.

CRM: EBIT TTM GAAP 8.735, amortización adquirida 1.995; EV aproximado de 211.601 da 24,22x GAAP y 19,72x antes de amortización. Incluye 633 de arrendamientos financieros además del principal financiero. WDAY: EBIT 1.085, amortización 134; EV 47.301 da 43,59x/38,80x. Usar acciones diluidas trimestrales en vez de acciones de portada produce CRM 24,17x/19,68x y WDAY 44,56x/39,66x, no valores intrínsecos.

CRM cerró Contentful el 1 de septiembre y Fin el 10 de septiembre después del balance: costes acordados en efectivo aproximados de 1.500 + 3.600, pero ajustes de cierre, efectivo adquirido y beneficios no están conciliados. La sensibilidad de pago solo produce 24,81x/20,20x y **no es un EV normalizado completo**. ASR final de CRM no verificado; Braze anunciada con EV de ~5.660 sigue pendiente y no se mezcla con los cierres. WDAY tiene un puente de financiación posterior: 43,62x/38,83x, sin certificar todos los movimientos. Son screens de precio actual y balance fechado, no comparables homogéneos actuales certificados. La mediana no fija target.

Fuentes completas y cálculos en comps: [CRM 10-Q](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm), [CRM IR](https://investor.salesforce.com/stock-info/), [WDAY IR](https://investor.workday.com/home/default.aspx). Los URLs exactos de filings y cierres usados en el paquete se verifican en comps/sources.json; cualquier cambio de perímetro exige revisar la resolución de EV.

## 8. Inversos y sensibilidad: qué tendría que cambiar

Con el resto del caso base constante, 109,16 exige una subida paralela de margen de {f(s['reverse']['roots'][0]['parallelMarginIncrease']*100)} puntos: 2027 {f(s['reverse']['roots'][0]['margin2027']*100)}% y 2036 {f(s['reverse']['roots'][0]['margin2036']*100)}%, después de SBC. Alternativamente, manteniendo márgenes y descuento, exige añadir {f(s['reverseGrowth']['roots'][0]['annualGrowthShift']*100)} puntos al crecimiento de cada uno de los diez años, desde {f(s['reverseGrowth']['roots'][0]['growth2027']*100)}% en 2027 hasta {f(s['reverseGrowth']['roots'][0]['growth2036']*100)}% en 2036, manteniendo g terminal del 3%. Estas soluciones de un solo eje son mecánicas, no consenso de mercado ni escenarios recomendados; el mercado puede combinar crecimiento, margen y descuento. El salto final del segundo inverso hasta el 3% también es una simplificación explícita.

Ambos barridos verificaron monotonicidad y todas las raíces en rangos declarados; financiación del incremento de NOPAT sigue activa. No se elimina capex para alcanzar el precio. El escenario favorable 125,93 muestra que una combinación más optimista puede soportar 109,16, aunque no es el central ni tiene probabilidad asignada.

|ROIC incremental base alternativo|Valor por acción|
|---|---:|
'''
for a in s['roic']:r+=f"|{f(a['roic']*100)}%|{f(a['value'])}|\n"
r+='''
Hay matrices WACC/g, márgenes, comisiones, capex, impuestos, acciones, caja, inversiones privadas y calendario. La principal incertidumbre es la duración/calidad del crecimiento después de remunerar capital y talento, no una décima de EPS. No confundir una sensibilidad de capital con una fecha de cierre o multa confirmada.

## 9. Confirmaciones pendientes y falsadores

Q3 ya publicado el 28 de octubre; próxima fecha exacta de earnings **no confirmada en fuente primaria localizada**. El registro técnico vigente tiene s2 ausente y discrepancia de precio; Opportunity 100 histórico no libera esa puerta ni una entrada. Revisar el próximo anuncio oficial de resultados y la ejecución Q4 frente a guía, sin convertir ventanas estimadas en citas confirmadas. [Eventos IR](https://investor.servicenow.com/events-and-presentations/default.aspx).

Mejoraría la tesis: caja después de SBC y capex creciendo de forma persistente; acuerdos AI convertidos en ingresos y cash sin dilución/costes desproporcionados; retorno de Armis/Veza demostrable; márgenes después de SBC e inversión compatibles con el caso favorable. La debilitarían presión de precios/downsells oculta en renovación, menor cRPO renovado, altos pagos cloud, nuevas compras costosas o SBC persistentemente elevado. No se infiere automáticamente ninguna de esas causas de la caída del precio.

Confianza: alta en conciliaciones históricas observadas; media en normalización contable; media-baja en valor puntual y capital posterior a septiembre. No hay proforma orgánico completo, escudo fiscal de intangibles probado, final captable actual ni valoración independiente de inversiones privadas. El residuo D&A de 124 sigue sin clasificar. Los pares tienen limitaciones de perímetro. Investigación condicionada, no certificación integral del plan técnico/calendario.

## English summary

ServiceNow has strong subscription growth and a sticky workflow platform, but stock-based compensation and acquisitions consume real shareholder value. The model retains SBC, funds margin expansion and commissions, and does not invent an acquired-amortization tax shield. Reported and adjusted FCF are not interchangeable with owner cash flow. September capital, stale peer balances and the unresolved scanner-price discrepancy remain explicit. Next exact earnings date is unconfirmed and the latest s2 field is missing. This is conditional research, not entry approval or an order.

## Reproduction

Run reproduce.py with standard Python 3. Own factual extracts and HTTPS sources are included; full third-party filings and private extraction scripts are excluded. The ten-year model, terminal reinvestment, tax-shield neutrality check, inverse scans and all history/comparables regenerate offline. Arithmetic checks do not remove the stated forecasting and source limitations.
'''
(P/'report.md').write_text(r)
print('report words',len(r.split()))
