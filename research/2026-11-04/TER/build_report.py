from pathlib import Path
import json
P=Path(__file__).parent
H=json.loads((P/'history/normalized_history.json').read_text())['periods'];R=json.loads((P/'model/results.json').read_text());V=json.loads((P/'model/checks.json').read_text());C=json.loads((P/'capital/facts.json').read_text())
f=lambda n:f'{n:,.2f}'
def hv(period,key):return H[period].get(key,{}).get('value')
S=C['sources'];pro='Teradyne registra TTM de 5.000,8 millones de ingresos y 1.606,0 de EBIT. El crecimiento de test de memoria y centros de datos es real, pero no elimina el ciclo ni garantiza repetir el margen del pico.'
con='El margen pretax de Semiconductor Test cayó de 42,14% a 38,09% y 34,23% entre Q1 y Q3 FY26. Anticipos a proveedores de 539,7 millones y compromisos de compra de 2.252,9 millones amplifican la exposición si se modera la demanda.'
con2='El híbrido suma DCF industrial, Technoprobe a mercado y el caso de compra financiada de FormFactor. La salida fiscal y el precio futuro del minoritario MLTP no están conciliados; no es valor intrínseco total certificado ni aprobación de entrada.'
t=f'''# TER | Teradyne | Ciclo de test y valoración híbrida condicionada

Investigación al 4 noviembre 2026. Precios congelados al cierre del 3 noviembre; USD millones salvo datos por acción y excepciones indicadas. Investigación parcial revisada; sin aprobación de entrada. Valor intrínseco total actual no certificado; escenarios del dossier son un DCF industrial más activos cotizados y obligaciones seleccionadas, no un precio objetivo íntegro validado. Sin entrada ni Stage 3 integral.

## 1. Decisión, escáner y calendario

La última observación del registro es del **12 octubre**: precio 386,55, QP 90, Opportunity 95, RSI 47,7 y Stage 2 Sí histórico. El cierre de mercado de esa fecha fue 383,85; no se reescribe el escáner para hacerlo coincidir. El cierre **3 noviembre, 269,35**, se usa para valoración. Un filtro positivo antiguo no demuestra una entrada vigente después del movimiento de precio y de resultados. [Historial de precios]({S['terPrice']}).

{pro}

{con}

{con2}

Los tres casos centrales condicionados son {f(R['bear']['hybridConditionalPerShare'])}, {f(R['base']['hybridConditionalPerShare'])} y {f(R['bull']['hybridConditionalPerShare'])} por acción, frente a 269,35. No bastan para respaldar el precio bajo estos supuestos. Sin embargo, un estrés conjunto de demanda/margen excepcional y menor descuento sí puede superarlo; por tanto no se declara que el precio sea matemáticamente imposible ni se convierte el resultado en una recomendación de venta corta.

Q3 terminó el 27 septiembre; el comunicado se publicó **27 octubre**, seguido de llamada 28 octubre y 10-Q el 30 octubre. El calendario oficial de TER no anuncia todavía el próximo resultado. No se usa la estimación de febrero 2027 como fecha confirmada. **Technoprobe**, participada, sí tiene revisión del consejo de ingresos/EBITDA/posición financiera Q3 el **11 noviembre**: no es el resultado de Teradyne. [Calendario TER]({S['calendar']}) y [calendario Technoprobe]({S['stakeCalendar']}).

## 2. Negocio y cambios que importan

Semiconductor Test prueba chips de sistema, memoria y sistemas integrados; Product Test incluye pruebas de almacenamiento y conexiones, mientras Robotics agrupa brazos colaborativos y robots móviles. La complejidad de los chips y el volumen de dispositivos AI pueden elevar contenido de test por unidad y ampliar la cartera. Pero la posición competitiva depende de instrumentos, software y rendimiento técnico; Advantest, Cohu y otros disputan gasto de clientes concentrados. No se supone monopolio ni un retorno garantizado por la etiqueta AI.

Q3 ingresos 1.305,950: Semiconductor Test 1.072,011, Product Test 138,111 y Robotics 95,828. El grupo creció aproximadamente 70% interanual, con récord en memoria y test de sistemas. Guía Q4 de ingresos **1.250–1.350** y EPS GAAP **1,88–2,18**, frente a no GAAP 1,95–2,25. El punto medio de ingresos daría FY26 aproximadamente 5.217,4, cálculo propio, no una nueva guía anual. El Q3 es fuerte, pero la guía no afirma que 70% de crecimiento continúe diez años. [Comunicado primario](https://www.sec.gov/Archives/edgar/data/97210/000119312526434981/ter-ex99_1.htm).

La concentración geográfica refleja lugar de entrega, no nacionalidad del cliente: Corea 32%, China 21% y Taiwán 14% en Q3. El ejercicio 2025 tuvo clientes especificadores de 12% y 10% de ingresos y un directo de 19%, con solapamiento: no deben sumarse como tres riesgos independientes. La fabricación del negocio de test está principalmente externalizada con operaciones relevantes en Malasia; robótica tiene fábricas en Dinamarca y Estados Unidos. Exposición a controles de exportación, aranceles y restricciones de componentes permanece. [10-K FY25]({S['fy25']}).

La tesis favorable exige que el mayor contenido de test y venta cruzada compensen normalización de gasto, sin degradar precio ni exigir inventario improductivo. La refutan caída persistente de márgenes, retrasos/cancelaciones, crecimiento de circulante superior a ventas o robótica que no sostenga rentabilidad. Los riesgos no son solo demanda final de AI: incluyen cuota, transición tecnológica, capacidad contratada y capital necesario para servirla.

## 3. Historia, SBC y normalización

El paquete contiene tres ejercicios, ocho trimestres disponibles y TTM contra TTM anterior, con 446 hechos fuente y fórmulas. Las magnitudes se convierten de miles a millones. EBIT industrial excluye el resultado por puesta en equivalencia de Technoprobe. El beneficio neto atribuible no debe confundirse con consolidado tras la compra MLTP.

| Periodo | Ventas | EBIT GAAP | CFO | Capex caja | SBC CFO | CFO−capex−SBC CFO |
|---|---:|---:|---:|---:|---:|---:|
'''
for n in ['FY2023','FY2024','FY2025','Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026','TTM2025Q3','TTM2026Q3']:
 vals=[hv(n,k) for k in ['revenue','ebit','cfo','capex','sbc_cf']];last=vals[2]-vals[3]-vals[4];t+='| '+n+' | '+' | '.join('ND' if v is None else f(v) for v in vals+[last])+' |\n'
t+=f'''
TTM ingresos 5.000,771 frente a 2.859,571; EBIT 1.605,983 frente a 510,435. FCF bruto 1.024,864 frente a 456,827; tras SBC del estado de flujos 944,777 frente a 394,411. El crecimiento es extraordinario, pero la base previa estaba deprimida. Los márgenes EBIT FY23/FY24/FY25 fueron aproximadamente 18,72%/21,06%/20,38%, frente al 32,11% del TTM. Usar este último como margen perpetuo sin contrastar ciclo sobrevalora certeza.

SBC CFO TTM 80,087 no es automáticamente idéntico a gasto SBC ni a movimiento APIC. El gasto anual de remuneración se conserva en el histórico cuando se divulga, mientras que gasto trimestral completo y capitalizado no se fuerzan a cero ni se deducen dos veces. El DCF retiene el SBC incluido en EBIT. FCF menos SBC es una aproximación adicional de coste económico, no FCFF ni caja distribuible por acción.

Amortización adquirida TTM 15,897 se separa de D&A total 138,955. EBIT anterior a amortización adquirida = **1.621,880**, sin añadir SBC. Reestructuración/otros TTM 23,537 permanece como coste: no se borra automáticamente una familia recurrente de ajustes. No se transforma el tag XBRL de 42,6 millones en deterioro extraordinario: el texto dice activos completamente amortizados retirados de coste/amortización acumulada y ausencia de deterioro de intangibles en nueve meses. Eliminar gastos que nunca existieron falsearía el resultado.

Technoprobe aporta pérdida TTM −6,482 por puesta en equivalencia, que incluye amortización de diferencias de compra y un retraso de tres meses. Está **fuera del EBIT industrial**. No se suma su beneficio y su cotización a la vez. FY24 también incluye venta de DIS; por ello ingresos y composición de Product Test no son idénticos a años previos. Los registros documentan la diferencia, sin atribuir todo el crecimiento a cuota orgánica.

Los márgenes de segmento divulgados son **beneficio antes de impuestos**, no EBIT. Semiconductor Test pasó de 42,14% a 38,09% y 34,23% en Q1/Q2/Q3 FY26. Robotics llegó a beneficio pretax 0,345 en Q3, pero margen TTM sigue aproximadamente −7,78%. No se capitaliza una rentabilidad ya consolidada de robótica que aún no existe. [10-Q Q3]({S['q3']}).

## 4. Caja, ciclo y compromisos

Nueve meses CFO 1.047,875 y capex 241,762, frente a 392,776 y 161,121. CFO incorpora aumento de impuestos por pagar 81,144 y entradas de anticipos de clientes 64,045. En contra, cuentas a cobrar consumen 302,733, inventarios 178,794 y anticipos/otros activos 224,940. No es coherente extrapolar la recuperación de beneficio y excluir toda financiación del circulante.

Anticipos a fabricantes/proveedores son 539,686; inventario 574,992 y cuentas a cobrar 1.110,798. Restando proveedores 516,967 y anticipos/deferred revenue 270,025, el diagnóstico de capital operativo es **1.438,484**, aproximadamente 28,8% del TTM. Omite otras cuentas y no es un balance normalizado certificado. El modelo selecciona 27% de incremento de ingresos como inversión en circulante, con sensibilidad 15–40%.

Compromisos de compra de **2.252,9**, de ellos 1.906,4 a menos de un año, no son todos deuda adicional: gran parte abastece ventas futuras ya cargadas en margen/capex. Pero podrían provocar excedentes o costes de cancelación si se reduce la demanda. El estrés deduce 225/450 adicionales del capital sin afirmar que sean pasivos existentes. En el escenario adverso no se inventa liberación automática de todo inventario/anticipo cuando caen ventas; una variante permite recuperación proporcional y muestra el efecto.

El modelo reconoce mantenimiento y expansión físicos: D&A no adquirido seleccionado 2,5% de ventas; capex bruto comienza 6% base y termina 4,5%, por encima de depreciación. Los porcentajes se apoyan en intensidad histórica aproximadamente 6–7% de capex, pero no hay desglose exacto de mantenimiento. La rebaja a 4,5% es supuesto de normalización, no guía. El suelo sigue financiado en terminal.

## 5. Capital y minoritarios: no usar libro como valor económico

| Puente industrial seleccionado | USD millones |
|---|---:|
| Caja y valores corto/largo | 624,865 |
| Reserva operativa discrecional | −250,000 |
| Deuda financiera | 0,000 |
| Pasivos de pensiones | −152,910 |
| Reserva por impuestos históricos | −188,105 |
| Derivados netos | −1,008 |
| Capex histórico pendiente de pago | −12,292 |
| Obligación económica MLTP seleccionada | −250,000 |
| Compromiso FormFactor, caso de cierre | −300,000 |
| Puente industrial antes de activos cotizados | −529,450 |

Caja 460,742 y valores 164,123 están fechados 27 septiembre; la cartera incluye fondos y bonos con riesgo de mercado. No equivalen a efectivo libre observado en noviembre. La línea de crédito renovada en agosto, **1.000 hasta agosto 2031**, no está dispuesta: no se suma como caja. Se mantienen covenants y garantías; deuda financiera cero no elimina riesgo de liquidez. Arrendamientos operativos 137,115 permanecen en gasto, no se añaden a deuda sin ajustar también EBIT.

Pensiones 152,910 se deducen sin compensar activo 12,240 de otros planes, cuya transferibilidad no se demuestra. Reserva fiscal 188,105 corresponde a impuestos por pagar, distinta del impuesto recurrente proyectado. UTB 6,9 más intereses/penalizaciones 0,3 podrían solaparse y **no se deducen otros 7,2 mecánicamente**. Reserva operativa, circulante y calendario de pagos pueden solaparse parcialmente; las sensibilidades muestran la aproximación. No se suman DTA 311,092, goodwill o anticipos operativos como activos libres.

MLTP se constituyó/adquirió el 8 abril: 75% por 157,839 y 25% minoritario consolidado. Valor inicial minoritario 35,799 + beneficio 5,684 + acreción 7,582 = **49,065** de equity temporal. El socio puede vender y TER comprar desde 2029 bajo condiciones y precio por fórmula. No se ha establecido la fórmula cuantitativa completa ni un valor actual independiente del derecho. El saldo contable no representa automáticamente el valor de toda la participación futura.

Por prudencia analítica se seleccionan **250** como obligación económica, no pago contractual: sensibilidad 49,065/100/250/500. Anualizar beneficio minoritario Q3 5,332 produciría 21,328, lo que muestra que un saldo inicial pequeño podría ser insuficiente, pero no convierte un trimestre en FCF sostenible. No se usa esa anualización como valoración independiente. Los flujos industriales se modelan consolidados; no se restan además dividendos minoritarios anuales. La ausencia de contribución standalone separada y fórmula futura mantiene el análisis condicionado.

Acciones efectivas **156,124751 millones al 26 octubre**, no las 157,502 medias diluidas del trimestre. Se añade un proxy de **1,24 millones** de dilución neta existente, inspirado en la diferencia trimestral diluida−básica, para llegar a 157,364751. No es puente exacto de premios en circulación. SBC futuro sigue como coste de margen; no se añaden todos los premios brutos ni se asumen recompras gratis. Se prueban 0/1,24/3 millones adicionales. El no reconocido FY25 97,3, amortizable en unos 2,6 años, confirma que una fracción de los premios aún depende de servicio futuro.

### Compromiso posterior con FormFactor: cierre no confirmado

El 6 octubre TER firmó la compra de **2.234.887 acciones de FormFactor por aproximadamente 300 millones USD**. El 8-K de FORM del 13 octubre y su 10-Q presentado el 3 noviembre todavía describen un cierre esperado en Q4, sujeto a condiciones y autorizaciones. No se ha confirmado el cierre al corte de este informe. Es un acuerdo posterior al balance del 27 septiembre, distinto de los compromisos operativos de compra de 2.252,9. [FORM 8-K]({S['formfactor8K']}), [FORM 10-Q]({S['formfactorQ3']}) y [TER Note V]({S['q3']}).

Los tres casos centrales son **condicionados al cierre**: restan 300 de la caja y añaden solo el valor ilustrativo de las acciones que se recibirían. A cierre 3 noviembre de FORM **96,79 USD**, la marca es **{f(R['base']['formfactorConditionalMarkedAsset'])} millones**. El efecto neto es negativo, no se conserva simultáneamente el efectivo gastado y el activo. Tampoco se reconoce beneficio fiscal por la diferencia frente al coste. [Precio FORM]({S['formfactorPrice']}). Son acciones de colocación privada no registrada: usar la cotización del título público es una aproximación, no valor razonable certificado del bloque ni efectivo realizable. Se prueban descuentos de liquidez 25/50/100%; no se presumen derechos de venta inmediata. No se inventan sinergias, dividendos ni ganancias de la participada en el EBIT industrial.

El acuerdo de derechos de registro exige presentar un S-3 de reventa al cierre; la eficacia automática depende de elegibilidad. Permite suspensiones de hasta 60 días por ocasión y 90 al año, por lo que registro contractual no equivale a liquidez incondicional. No se ha localizado un S-3 de reventa ni confirmación posterior del cierre en los filings consultados. [Derechos de registro]({S['formfactorRights']}). El Form D del 20 octubre declara 300.000.056 USD vendidos y fecha de primera venta 6 octubre; la definición SEC de primera venta es compromiso contractual irrevocable, no necesariamente liquidación del efectivo. No desplaza la descripción posterior de cierre pendiente del 10-Q. La diferencia de 56 USD frente a 300 millones no es material al modelo. [Form D]({S['formfactorD']}) y [definición SEC]({S['formDDefinition']}).

El caso alternativo **sin cierre** retiene caja y no incorpora acciones FORM: base **{f(V['sensitivity']['formfactorClosing'][0]['conditionalHybridValue'])}**, frente a **{f(R['base']['hybridConditionalPerShare'])}** con cierre. No representa un derecho demostrado a cancelar gratis: costes de terminación, restricciones y desenlace no están conciliados. No se asignan probabilidades. Tras desembolsar 300, caja y valores históricos serían 324,865 antes de operaciones, impuestos y otras salidas; frente a reserva operativa 250, el margen bruto es estrecho. No es una previsión de liquidez actual: no se conoce generación de caja posterior ni se añade la línea no dispuesta como efectivo.

## 6. Technoprobe: participación cotizada, no segundo DCF implícito

La página de accionistas, actualizada 22 septiembre, identifica **65,326087 millones de acciones** de Teradyne, 10% del capital emitido. No se toma 10% del número de acciones de un proveedor neto de autocartera. [Accionistas oficiales]({S['ownership']}).

Cierre 3 noviembre **24,34 EUR**, FX ECB **1,1179 USD/EUR**: valor bruto seleccionado **{f(R['base']['technoprobeGrossMarkedValue'])}**. El valor razonable de 2.242,4 del 10-Q era al 27 septiembre; el contable 518,559 es otra base. No se suman los tres. La reserva de salida, 20% de ganancia sobre coste histórico USD 524,1, es supuesto y deja **{f(R['base']['technoprobeNetSelectedMark'])}**. Coste original no es base fiscal verificada; no se certifica tratamiento tributario de la sociedad holandesa tenedora. Se prueban tasas 0/20/30% y descuento de liquidez 0/10/25%. [Cotización]({S['stakePrice']}) y [corroboración]({S['stakePriceCorroboration']}) y [ECB]({S['fx']}).

**El bloqueo financiero original de 36 meses no sigue vigente:** Teradyne anunció su terminación el 8 enero de 2025 tras ampliar la relación de Technoprobe con Advantest. Se mantiene inversor estratégico. Eso elimina una restricción histórica concreta, pero no garantiza realización inmediata íntegra ni determina todos los términos de una venta en bloque. [Comunicado primario]({S['lockupTermination']}).

Este trabajo no valora por DCF el negocio completo de Technoprobe. La suma es un **híbrido DCF industrial + marca de mercado**. Si la cotización de la participada sobrevalora su negocio, también podría sobrevalorar esta parte del híbrido; el estrés lleva la participación a cero. No se agrega una cuota de su caja o beneficio además de sus acciones.

## 7. Modelo de diez periodos, ciclo y terminal financiado

Periodos anuales analíticos del 3 noviembre 2026 al 3 noviembre 2036, no ejercicios fiscales declarados ni un stub reconstruido de caja octubre. Ancla ingresos TTM 5.000,771 y EBIT preamortización adquirida 1.621,880; SBC retenido. La trayectoria base introduce un descenso de ventas del 10% en el segundo periodo como prueba de ciclo, **no como previsión empresarial de caída en un año concreto**. El caso favorable no contiene esa caída.

NOPAT = EBIT después de SBC/pre-amortización adquirida × (1−impuesto). Impuesto elegido 20% hasta el noveno periodo, 22% en el décimo y terminal. El actual beneficio fiscal de Singapur exige empleo/inversión y vence 31 diciembre 2035: no se perpetúa sin más la tasa efectiva cercana a 14%. El salto anual es aproximación temporal, no cálculo jurisdiccional exacto. No hay escudo automático por amortización contable adquirida.

Inversión neta = máximo entre (capex físico − D&A + inversión de circulante) y (incremento positivo de NOPAT / ROIC). De este modo crecimiento de ingresos **y** mejora de margen reciben financiación; R&D y SBC ya son gastos, no addbacks. Los ROIC son supuestos de productividad incremental, no el ratio contable observado aplicado sin crítica. Caídas de NOPAT no generan desinversión artificial. Capex y circulante mínimos siguen vigentes en terminal, donde reinversión ≥ NOPAT×g/ROIC.

Referencia de descuento: Treasury 10 años 4,95% (3 noviembre), ERP 4,41% (1 noviembre, calculado originalmente con Treasury 5,29%) y beta de proveedor 1,75. CAPM = 12,6675%; sin deuda financiera, base **12,75%** es una selección próxima, no una medición exacta. Los inputs tienen fechas/métodos distintos; el descuento refleja volatilidad y ciclo, no solo tipo libre de riesgo. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve), [ERP](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), [beta](https://stockanalysis.com/stocks/ter/statistics/).

| Hipótesis | Adverso | Base | Favorable |
|---|---:|---:|---:|
| Ventas primer periodo | 4.600 | 5.600 | 6.200 |
| Crecimiento periodos 2–5 | −17/3/5/5% | −10/8/10/8% | 18/15/12/10% |
| Crecimiento periodos 6–10 | 4/3,5/3/2,5/2,5% | 6/5,5/5/4,5/4% | 9/8/7/6/5% |
| Margen años 1/2/5/10 | 22/15/18/18% | 27/22/25/25% | 34/34/32/32% |
| ROIC | 18% | 30% | 40% |
| Descuento | 14,5% | 12,75% | 11% |
| Crecimiento terminal | 2% | 3% | 3,5% |
| Capex bruto/ventas 1→10 | 6,5→4,5% | 6→4,5% | 6,5→4,5% |

| Periodo base | Ventas | EBIT preamortización adquirida/después SBC | Impuesto | NOPAT | Inversión neta | FCFF |
|---|---:|---:|---:|---:|---:|---:|
'''
for a in R['base']['rows']:t+=f"| {a['year']} | {f(a['revenue'])} | {f(a['ebitAfterSbcBeforeAcquiredAmort'])} | {a['taxRate']:.0%} | {f(a['nopat'])} | {f(a['netReinvestment'])} | {f(a['fcff'])} |\n"
t+='\n| Caso | EV industrial | Residuo tras financiar FORM, antes de marcas/acción | Marcas netas participadas/acción | Híbrido condicionado/acción | Terminal/EV industrial |\n|---|---:|---:|---:|---:|---:|\n'
for n,a in R.items():t+=f"| {n} | {f(a['enterpriseValueIndustrial'])} | {f(a['industrialConditionalPerShare'])} | {f((a['technoprobeNetSelectedMark']+a['formfactorConditionalMarkedAsset'])/a['sharesMillions'])} | {f(a['hybridConditionalPerShare'])} | {a['terminalShareOfIndustrialEV']:.1%} |\n"
t+='''
No se asignan probabilidades, media ponderada ni confianza estadística a los extremos. Todos comparten una marca contemporánea de la participada; su cotización también puede caer en un escenario industrial adverso, de ahí la sensibilidad independiente.

## 8. Sensibilidad e inverso

| Variación aislada del caso base | Híbrido condicionado |
|---|---:|
'''
for key,label in [('nciClaim','Obligación MLTP'),('stakePriceEur','Precio Technoprobe EUR'),('cashReserve','Reserva de caja'),('incrementalWC','Circulante/incremento ventas'),('formfactorLiquidityHaircut','Descuento liquidez FORM')]:
 for a in V['sensitivity'][key]:t+=f"| {label} {a['input']} | {f(a['conditionalHybridValue'])} |\n"
t+='\n| WACC / g base | 2% | 3% | 4% |\n|---|---:|---:|---:|\n'
for w in [.10,.11,.1275,.14]:t+='| '+f'{w:.2%}'+' | '+' | '.join(f(next(a['value'] for a in V['sensitivity']['wacc_g'] if a['wacc']==w and a['g']==g)) for g in [.02,.03,.04])+' |\n'
t+=f'''
Permitir recuperar circulante al caer ventas eleva base a {f(V['sensitivity']['wcReleaseOnDecline']['value'])}; es recuperación supuesta, no cobro comprobado. Sin valor de Technoprobe, pero con FORM financiado y marcado, híbrido base {f(V['sensitivity']['stakeZero']['value'])}. Subir capex bruto en 2,5 puntos de ventas reduce base a {f(V['sensitivity']['capexFloor'][-1]['value'])}; no se omite ese suelo extra en terminal. Más sensibilidades de impuestos, ROIC, premios y capital están en model/checks.json.

Inverso a 269,35: con margen/ROIC/descuento base y primer ingreso fijo, requiere sumar **{V['inverse']['uniformGrowthShiftYears2to10']['root']*100:.2f} puntos porcentuales** a cada crecimiento de años 2–10. El segundo periodo pasa de −10% a {(V['inverse']['uniformGrowthShiftYears2to10']['root']-.10)*100:.2f}% y el décimo de 4% a {(V['inverse']['uniformGrowthShiftYears2to10']['root']+.04)*100:.2f}%, antes del salto a 3% perpetuo. Es combinación matemática exigente, no lectura literal del consenso. Solo elevar márgenes hasta +60 puntos no encuentra raíz dentro del intervalo, aun con margen final 85%; valor en ese límite {f(V['inverse']['uniformMarginShift']['valueAtUpperBound'])}. El modelo financia los aumentos de NOPAT y no extrapola raíces inexistentes.

La otra cara: combinando trayectoria favorable con **margen 40%, WACC 10%** y sus crecimientos originales, el estrés arroja **{f(V['sensitivity']['jointHighDemandStress'][0]['value'])}**. Si además se suman 3 puntos de crecimiento a años 2–10, asciende a **{f(V['sensitivity']['jointHighDemandStress'][1]['value'])}**; con +5 puntos, **{f(V['sensitivity']['jointHighDemandStress'][2]['value'])}**. No son escenarios centrales ni probabilidades. Indican que el precio puede justificarse con un conjunto más ambicioso, especialmente si el mercado de test se expande y captura rentabilidad extraordinaria. El contraste con Advantest hace improcedente declarar que un margen alto sea imposible; tampoco demuestra que TER lo logrará. La decisión exige evidencia sobre ejecución y duración, no solo una hoja de cálculo adversa.

## 9. Comparables

| Pantalla TTM | TER | Advantest | Cohu |
|---|---:|---:|---:|
| Margen EBIT | 32,11% | 50,00% | −2,38% |
| EV/ventas convencional | 8,28x | 17,64x | 3,81x |
| EV/EBIT convencional | 25,80x | 35,28x | No significativo |
| FCF/capitalización básica | 2,44% | 1,79% | 2,36% |

El paquete comps/ incorpora el contraste contemporáneo de Teradyne, Advantest y Cohu, sus fuentes y límites. La pantalla de pares usa capital de septiembre y no incorpora el cierre pendiente de FORM; el puente DCF sí presenta ese desembolso y activo como caso condicionado. La variante industrial TER resta la marca de Technoprobe y añade pensiones/minoritario contable, resultando EV/EBIT 24,81x; no es idéntica al puente DCF con minoritario económico seleccionado. Advantest tiene 432.586 millones de yenes en inversiones no tratadas todas como caja; restar su libro solo como sensibilidad baja EV/EBIT a 34,68x. Su FCF de 463.173 millones de yenes baja a 458.437 después de principal de arrendamientos y a 453.469 tras SBC, sin confundir clasificación IFRS con US GAAP.

Cohu tiene EBIT TTM −13,552 millones y FCF 55,854, o 32,882 tras SBC. No se sustituye EBIT GAAP por ajustado para fabricar un múltiplo positivo. Su convertible dentro del dinero requiere sensibilidad: EV/ventas pasa de 3,81x a 3,98x al añadir intrínseco de conversión neto de capped call; el cap 41,02 es inferior al precio 50,03. Esto no captura valor temporal ni certifica valor razonable. No se añaden a la vez deuda íntegra y todas las acciones de conversión. [Advantest H1](https://www.advantest.com/document/en/investors/ir-library/result/E_FR_FY2026_2Q.pdf), [Advantest anual](https://www.advantest.com/en/news/2026/a81o6o0000000hgw-att/E_FR_FY2025_FN.pdf) y [Cohu Q3](https://ir.cohu.com/news-releases/news-release-details/cohu-reports-third-quarter-2026-results). Los ratios de valoración no sustituyen ciclo normalizado ni se aplica una mediana como precio objetivo. Advantest usa IFRS, periodos fiscales distintos y grandes inversiones financieras; Cohu tiene diferente mezcla de sistemas/consumibles y pérdidas operativas TTM aunque Q3 sea positivo. No se compara EPS de equity-income/valoración financiera con EBIT industrial sin separar ambos.

La diferencia de margen sectorial es una prueba útil contra conclusiones demasiado absolutas: Advantest presenta rentabilidad muy superior, mientras Cohu muestra sensibilidad al ciclo. TER no debe recibir automáticamente ni el margen de su competidor mejor situado ni un múltiplo de beneficio cíclico deprimido. El calendario bursátil japonés también importa: 3 noviembre fue festivo, por lo que la observación pertinente es última sesión disponible y se rotula, no se inventa un cierre japonés de ese día.

## 10. Qué falta para una conclusión operable

Verificar cierre, restricciones y financiación efectiva de FormFactor; reconciliar capital posterior al trimestre, puente de premios netos y fórmula/valor de la salida MLTP; confirmar condiciones y fiscalidad de una eventual venta de Technoprobe; actualizar resultados de la participada tras su evento; verificar la próxima fecha de resultados de TER y renovar filtro técnico. El modelo de ciclo y el precio marcado de la participada no certifican el valor intrínseco total del grupo.

Conclusión ES: **Esperar; análisis híbrido condicionado.** Demanda y caja han mejorado mucho, pero márgenes secuenciales, circulante y compromisos exigen normalización. Los casos centrales no respaldan 269,35; un conjunto más optimista sí puede hacerlo. No existe margen de seguridad demostrado con este paquete, no se certifica valor total y no se autoriza entrada.

Conclusion EN: **Wait; conditional hybrid analysis.** Demand and cash generation improved materially, but sequential margins, working capital and purchase commitments require cycle normalization. Central cases do not support $269.35; a stronger joint operating scenario can. This package does not establish a margin of safety, certify total intrinsic value or approve an entry.

## Fuentes y reproducción

[10-K FY25]({S['fy25']}), [10-Q Q3]({S['q3']}), [Q2](https://www.sec.gov/Archives/edgar/data/97210/000119312526327715/ter-20260628.htm), [Q1](https://www.sec.gov/Archives/edgar/data/97210/000119312526201058/ter-20260329.htm). Todos los hechos tienen fecha/unidad/procedencia; estimaciones propias se identifican. Ejecutar reproduce.py sin red regenera historia, capital, modelo y pruebas. Se publican datos factuales seleccionados y cálculos propios, no filings íntegros. Reproducir aritmética no certifica supuestos económicos ni constituye una recomendación personal de inversión.
'''
(P/'report.md').write_text(t)
s={'ticker':'TER','company':'Teradyne','researchDate':'2026-11-04','valuationDate':'2026-11-03','status':'partial_hybrid_conditioned_audited','readyForPublication':True,'fairValue':None,'fairValueTotal':None,'bear':None,'base':None,'bull':None,'conditionalHybridScenarios':{n:a['hybridConditionalPerShare'] for n,a in R.items()},'conditionalIndustrialScenarios':{n:a['industrialConditionalPerShare'] for n,a in R.items()},'scanDate':'2026-10-12','scanPrice':386.55,'scanQuality':90,'scanOpportunity':95,'scanRsi':47.7,'scanStage2Historical':True,'scanStage2Current':None,'scanComparisonClose':383.85,'latestClose':269.35,'latestCloseDate':'2026-11-03','nextEvent':{'date':None,'confirmed':False,'type':'Next Teradyne earnings date not announced in reviewed issuer calendar','sourceUrl':S['calendar']},'investeeNextEvent':{'date':'2026-11-11','confirmed':True,'company':'Technoprobe','type':'Board review of Q3 turnover/EBITDA/net financial position, unaudited','sourceUrl':S['stakeCalendar']},'formfactorEvent':C['formfactor'],'sources':S,'entryApproved':False,'stage3Complete':False,'stage35Approved':False,'confidence':'Moderate on filed history/arithmetic; conditional on FormFactor closing/mark/restrictions, cycle, MLTP economic claim, award bridge and investee exit tax/market mark.','conclusionEs':'Esperar. DCF industrial más marca Technoprobe condicionado; sin valor intrínseco total certificado ni entrada.','conclusionEn':'Wait. Conditional industrial DCF plus Technoprobe market mark; no certified total intrinsic value or entry.','pros':[{'textEs':'Ingresos y EBIT TTM han crecido con test de memoria y centros de datos; el avance no elimina la ciclicidad.','textEn':'TTM revenue and EBIT rose with memory and data-center testing; the improvement does not eliminate cyclicality.','evidence':pro,'sourceUrl':S['q3']}],'cons':[{'textEs':'Margen pretax del segmento principal cae secuencialmente; anticipos y compromisos de compra amplifican riesgo de ciclo.','textEn':'The main segment’s pretax margin falls sequentially; supplier prepayments and purchase commitments amplify cycle risk.','evidence':con,'sourceUrl':S['q3']},{'textEs':'Híbrido con participadas a mercado y compra FORM pendiente; fiscalidad y obligación MLTP no conciliadas. No valor total certificado.','textEn':'Hybrid includes market-marked stakes and pending FORM investment; exit taxation and MLTP claim remain unresolved. No certified total value.','evidence':con2,'sourceUrl':S['q3']}]}
(P/'summary.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n');print('report',len(t.split()),'words')
