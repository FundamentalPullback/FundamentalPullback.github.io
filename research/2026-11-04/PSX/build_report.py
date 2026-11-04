import json
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'model/results.json').read_text());ss=json.loads((P/'model/sensitivities.json').read_text());rates=json.loads((P/'model/rates_results.json').read_text());h=json.loads((P/'history/financial_history.json').read_text());comps=json.loads((P/'comps/outputs.json').read_text());b=m['base'];inp=json.loads((P/'model/inputs.json').read_text())
f=lambda x:f'{x:,.2f}'
Q='https://www.sec.gov/Archives/edgar/data/1534701/000153470126000037/psx-20260930.htm';K='https://www.sec.gov/Archives/edgar/data/1534701/000153470126000006/psx-20251231.htm';E='https://www.sec.gov/Archives/edgar/data/1534701/000153470126000035/psx-2026930_ex991.htm'
report=f'''# Phillips 66 (PSX): valorar el ciclo, no anualizar un trimestre extraordinario

Investigación propia del 4 de noviembre de 2026. Corte de mercado: cierre del 3 de noviembre, **$271,94**. Estados: septiembre de 2026, publicados el 28 de octubre. USD millones salvo acciones, porcentajes y datos por barril. **Investigación revisada de forma independiente y condicionada; no aprobación de entrada, Stage 3.5 ni confirmación técnica.**

## 1. Conclusión y separación del registro

El DCF de dos componentes produce **${f(m['bear']['valuePerShare'])} / ${f(b['valuePerShare'])} / ${f(m['bull']['valuePerShare'])}** por acción en escenarios adverso/base/favorable. Son hipótesis de un negocio cíclico, no un intervalo estadístico ni un suelo liquidativo. El cierre de referencia supera el central en aproximadamente {f((271.94/b['valuePerShare']-1)*100)}%; el potencial calculado desde ese cierre hasta el central es {f(b['upsideToReferenceClose']*100)}%. La amplitud y el extremo adverso reflejan normalización de márgenes, gastos fijos y deuda, no una predicción de insolvencia.

La fila original A105 es del 27 de octubre: $268,25, QP 90, Opportunity 85, RSI 44,5. La última observación real del 3 de noviembre es $271,94, QP 90, Opportunity 70, RSI 47,2 y s2 «No». No se reutiliza el 85 antiguo como filtro vigente. La caída intradía observada el 4 nov no sustituye el cierre ni da señal técnica. Fuente de precio: https://stockanalysis.com/stocks/psx/history/ . El registro se conserva sin reescribir sus observaciones históricas.

El negocio genera caja considerable en condiciones favorables, pero EPS trimestral 14,08 y margen 38 $/bbl no son una renta perpetua. Esperar mejor relación precio/valor y nueva confirmación de condiciones operativas y del plan. No se plantea orden, tamaño de posición ni stop.

## 2. Negocio y ventajas con límites

PSX combina diez refinerías estadounidenses/europeas, logística y NGL, comercialización, renovables y el 50% de CPChem. Infraestructura integrada, acceso a feedstocks y capacidad comercial aportan ventajas prácticas; no eliminan exposición a cracks, transporte, energía, utilización, paradas y regulación. El 98% de utilización de crudo, producción de destilados 41% y productos limpios 86% del Q3 respaldan ejecución fuerte, no una ventaja que permita fijar precios indefinidamente. Midstream reportó fraccionamiento 1.003 MBD, wellhead 4,6 Bcf/d y Freeport 105% de utilización. [Resultados Q3]({E}).

WRB pasó de 50% equity method a 100% consolidado el 1 oct 2025. La compra restante consumió aproximadamente 1.300 más 450 de deuda asumida/repagada; el impairment 948 del Q3 previo no es caja recuperable. Los Ángeles cesó combustible en Q4 2025 y todavía estaba siendo desactivada. Lindsey se adquirió como activos e infraestructura por 115 en abril 2026: PP&E 202 incluye ARO 87; no se supone una nueva refinería operativa a plena capacidad. Por ello el crecimiento bruto de ingresos, barrels y CFO no prueba crecimiento orgánico. [10-K]({K}); [10-Q]({Q}).

La dirección comunicó más de 50 de sinergias cercanas de WRB, Coastal Bend a 350 MBD a comienzos de 2027 y operación plena esperada de Golden Triangle/Ras Laffan en 2027. Son objetivos, no fechas garantizadas ni flujos ya percibidos. Western Gateway tiene decisión final de inversión y expectativa 2029, pero no se añade valor por un proyecto completo sin presupuesto y participación detallados. El modelo financia crecimiento normalizado y muestra sensibilidad de capital, sin fingir un presupuesto proforma de cada proyecto.

## 3. Historia y normalización

|Periodo|Ingresos|NI atribuible|CFO|CFO sin WC|Capex/inversiones|Equity income|Dividendos JV en CFO|
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for r in h:
 if r['period'] in ['FY2023','FY2024','FY2025','Q4 2025','Q1 2026','Q2 2026','Q3 2026','TTM Sep2025','TTM Sep2026']:
  z=r['metrics'];report+='|'+r['period']+'|'+'|'.join(f(z.get(k,0)) if k in z else 'no separado' for k in ['revenue','net_income_parent','cfo','cfo_ex_wc','capex_investments','equity_earnings','equity_distributions_in_cfo'])+'|\n'
report+=f'''
Los archivos de historia incluyen 3 ejercicios fiscales (FY), cuatro trimestres, 9M comparativos y TTM frente al anterior, además de los seis segmentos. Q4 se obtiene restando 9M del FY; TTM = FY25 + 9M26 − 9M25. No son ajustes proforma de perímetro. La reproducción valida suma de segmentos a PBT y NI = PBT − impuestos − minorías. Fuentes y hechos mínimos están en history/source_facts.json.

NI ajustado del emisor FY25 fue 2.632, no 4.403 GAAP; FY24 fue 2.604. TTM ajustado 10.609 sigue siendo cíclico. FY25 contiene ganancias de disposición 2.984, impairments 1.060 y depreciación acelerada LA 964. Esta última persiste en el ajustado del emisor; quitarla de earnings comparables no autoriza sumarla otra vez a CFO, que ya añade D&A. FY24 LA 253 y FY25 LA 964 tampoco se convierten en capacidad futura. El corte de activos vendidos exige retirar sus beneficios, no solo sus pérdidas.

CFO TTM 15.028 menos capex 2.670 = 12.358 es residual consolidado, no FCFF ni caja íntegramente distribuible al común. Excluyendo el efecto WC 1.783, el residual baja a 10.575, aún con cracks altos. Q1/Q2/Q3 26 CFO: −2.264/7.259/7.281; sin WC: 699/4.317/6.185: prueba de volatilidad real de conversión. Los cash taxes FY25 fueron 200 frente gasto 892; no se perpetúa esa baja caja fiscal. SBC FY23/24/25 = 297/210/220 permanece como coste. No se inventa SBC trimestral a partir de movimientos de patrimonio. [Historia anual]({K}); [intermedia]({Q}).

EPS diluido de Q4 2025/Q1/Q2/Q3 2026: 7,17/0,51/9,55/14,08. La suma de los cuatro EPS publicados es 31,31, frente a 3,66 del período previo; no es un EPS TTM recalculado con un denominador único. No se utiliza para el DCF.

### Refining: puente económico y cambio de perímetro

Margen realizado FY23/FY24/FY25: 17,26/8,84/10,88 $/bbl. Q2 26: 24,08 y Q3 26: 38,00. El puente de Q3 es: 6031 PBT + 96 otros impuestos + 249 D&A/impairment + 55 SG&A + 1166 opex + 1 pérdida JV − 161 otros ingresos + 15 margen JV = 7452. Dividido entre 196,088 millones de barriles procesados resulta 38,004, redondeado a 38,00. No confundir estos inputs con crudo exclusivamente. La medida incluye participación proporcional en pequeñas afiliadas y ajustes especiales, de modo que no es GAAP EBIT por barril.

El modelo excluye ingresos JV de los segmentos consolidados. Parte de un volumen de flota retenida de 765 millones de barriles en 2027 base, frente 777,96 anualizados del Q3. Selecciona margen 25 en 2027 y 15 en 2031 en dólares reales de 2027; después solo inflación del 2%, no 38 perpetuo. Costes cash refinación 5.500 y D&A 1.000 en 2027: el gasto trimestral 96 + 55 + 1166 anualiza 5.225, pero turnarounds 79 Q3 frente 123 Q2 justifican no fijar un trimestre especialmente eficiente para siempre. Otros ingresos 161 no se perpetúan automáticamente. Estos supuestos no son guidance ni una media estadística de ciclos idénticos.

Midstream ex JV parte de 2.550 EBIT frente 2.331 TTM consolidado ex equity; marketing 650 frente 83 Q3 ex JV, afectado por trading y cambios de perímetro; corporate −550 frente a −1.602 PBT TTM que incluye 1.138 de interés consolidado. Son normalizaciones seleccionadas, no puentes exactos al resultado reportado. No se suma otra vez el ingreso financiero al FCFF. Marketing tiene sensibilidad 300–1000 y Midstream 2200–2900.

### Renewable Fuels y la fecha de los créditos

El beneficio del segmento en Q3, 191 frente a una pérdida previa de 43, depende de créditos regulatorios y condiciones del feedstock. Other income aumentó 288 Q3, principalmente por trading y Clean Fuel Production credits; no se identificó el importe 45Z individual. La IRS confirma elegibilidad del crédito para combustible vendido hasta 31 dic 2029, con restricciones de origen de feedstock. No se presume una extensión: en el escenario base, el EBIT de renovables de 250 en 2027 cae a 0 en 2030 y permanece en 0 en el terminal; favorable llega a 200 por economía operativa/otros programas, no por continuidad asumida de 45Z. Estrés de −250 adicional muestra que ni ese equilibrio está asegurado. [IRS 45Z](https://www.irs.gov/credits-deductions/clean-fuel-production-credit); [boletín actualizado](https://www.irs.gov/irb/2026-41_irb).

## 4. CPChem y afiliadas: valor de equity, no doble consolidación

Equity earnings TTM 1.567 frente dividendos 595; devoluciones de capital 91 se mantienen aparte. CPChem es 50%, con ingresos de equity 9M 828 y capex 100%: 787 (parte PSX: 394), autofinanciado. Sus estados completos no son públicos en el portal consultado y PSX no separa los dividendos específicos CPChem. No se adjudican todos los 595 a CPChem. La información seleccionada de CPChem muestra NI 2023/24/25 de 1.173/1.726/593 a 100%, ilustrando ciclo y no distribución garantizada. [CPChem](https://www.cpchem.com/who-we-are/financials).

Se usa un DCF de **equity de todas las afiliadas**: earnings normalizados menos impuesto incremental de PSX menos capital retenido. Los beneficios de una LLC no son todos netos del impuesto de PSX: las afiliadas combinadas reconocieron 111 de impuesto sobre 2.416 PBT en 2025, pero no se puede reconstruir una tasa propietaria exacta desde esos agregados. Base selecciona 20% adicional, sensibilidad 0–30%; es hipótesis, no una obligación fiscal medida. Se grava el beneficio atribuible, no solo el dividendo, porque puede existir pass-through sin caja distribuida.

Base supone equity earnings 1.300 en 2027 y 1.500 reales en 2031. Retención mínima 40% de earnings en 2027 y 25% en 2028; después se financia todo aumento positivo del beneficio después del impuesto PSX a ROE 10%. Si el requisito supera la caja, el modelo permite contribución negativa; no crea deuda JV gratis. En terminal, retención = g × beneficio después de impuesto / ROE. Ke 11%, no WACC 9,5%. No se añaden los 11.425 de inversiones equity JV registrados a diciembre de 2025 ni se resta otra vez deuda o capex JV. Con esta disciplina el valor base JV es {f(b['jvEquityValue'])}, frente a {f(m['bear']['jvEquityValue'])}/{f(m['bull']['jvEquityValue'])} en extremos. Esta aproximación no reemplaza estados individuales ni acuerdos de distribución.

## 5. DCF operativo: 5+5, reinversión y descuento

2027–2031 normalizan el ciclo; 2032–2036 son fase madura. FCFF = NOPAT + D&A − capex − ΔWC. Impuesto 24%, sin repetir cash tax 200 de FY25. D&A consolidada 2.400 en 2027 frente 591 Q3 × 4 ≈2.364 y 2.552 TTM con 239 LA en Q4 25. El mantenimiento/reemplazo mínimo es 125% de D&A, no D&A igual a capex. Capex 2027 mínimo: 3.000; aumenta con 2% de inflación. No se añade SBC a FCFF.

La reinversión neta es el máximo entre (i) 25% D&A + WC positivo, (ii) suma de aumentos positivos de NOPAT de cada segmento/ROIC y (iii) suelo de capex menos D&A + WC. Las caídas de refining no financian mágicamente la expansión de Midstream: se usan aumentos por segmento, no solo la variación consolidada. La primera anualidad parte de activos ya operando y contrasta con el run-rate Q3 actual, no con un año deprimido que exigiría inversiones ficticias por simple recuperación del precio. La sensibilidad usando un ancla de 10.000 NOPAT muestra el coste de otra lectura. No se confunde ese ancla de capacidad con pronóstico de persistencia del trimestre.

Ingresos 150.000 en 2027 y 2% de crecimiento son proxy para WC, no tesis de volumen/growth orgánico: refinado es pass-through de commodities. Se invierte 1,5% del aumento de ventas, no se supone liberación de WC cuando bajan. Un estrés de ±2.000 de capital posterior cubre parte de volatilidad del petróleo/collateral, sin pretender estimar su distribución. No existe plan proforma completo de adquisiciones, Western Gateway o nuevo cierre de instalaciones; gastos adicionales requieren revisar la valoración.

|Hipótesis|Adverso|Base|Favorable|
|---|---:|---:|---:|
|Volumen 2027, millones bbl|730|765|790|
|Cambio anual de volumen|−1%|−0,25%|0%|
|Margen 2027, $/bbl|18|25|30|
|Margen 2031 real 2027, $/bbl|10|15|20|
|Cash cost refining 2027|5.700|5.500|5.250|
|WACC|10,50%|9,50%|8,75%|
|Ke afiliadas|12%|11%|10%|
|g terminal|0%|1,5%|2%|
|ROIC operativo|10%|12%|15%|
|ROE afiliadas|8%|10%|12,5%|

Treasury 10Y, 3 nov: 4,95%; ERP mensual, 1 nov: 4,41% fue calculada con Treasury 5,29%, por tanto la combinación no es un ERP diario sincronizado. Beta 5Y del proveedor: 0,67 da Ke 7,90%; se selecciona beta 1 para reconocer riesgo cíclico, spread de deuda 150 pb, peso deuda 15% e impuesto 24%: WACC mecánico 8,6913%. El 9,5% elegido añade 80,87 pb discrecionales, no es redondeo ni coste cotizado de bonos. El Ke JV 11% refleja riesgo de distribución y dependencia de acuerdos. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve); [ERP](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm); [beta](https://stockanalysis.com/stocks/psx/statistics/).

FY2027 se descuenta 423/365 años desde 3 nov, no automáticamente un año. Stub restante 58 días usa prorrata estimada del primer flujo proyectado, sin afirmación sobre estacionalidad o caja real Oct–Nov. Con stub central: {f(b['valuePerShare'])}; sin stub: {f(ss['calendar']['withoutStub'])}; descuento erróneo de una anualidad da {f(ss['calendar']['incorrectOneYearDiscountIllustration'])}. Capital de septiembre no absorbe automáticamente caja posterior desconocida.

El terminal adopta crecimiento uniforme maduro g y exige reinversión = max(g × NOPAT / ROIC, 25% D&A + WC, suelo de capex terminal menos D&A más WC). Ya no perpetúa distintos crecimientos reales de cada segmento. Es una hipótesis de negocio en marcha con renovación de activos, no vida infinita de la misma refinería. Terminal representa {f(b['terminalShareGrossValues']*100)}% del valor operativo + JV base. Refining con declive, capital regulatorio y energía alternativa pueden hacer insuficiente este reemplazo: sensibilidad de mantenimiento 10/25/50% D&A y escenario adverso se conservan.

### Tabla base reproducible

|Año|EBIT ex JV|NOPAT|D&A|Capex|ΔWC|FCFF|Flujo equity JV|
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for r in b['rows']:
 report+='|'+str(r['year'])+'|'+'|'.join(f(r[k]) for k in ['operatingEbitExJv','nopat','da','capex','workingCapitalInvestment','fcff','jvEquityCashFlow'])+'|\n'
report+=f'''
## 6. Puente de capital y acciones

|Componente base|Efecto equity|
|---|---:|
|DCF operaciones|{f(b['operationsValue'])}|
|DCF equity JV|{f(b['jvEquityValue'])}|
|Caja de septiembre|+5.848|
|Deuda financiera carrying|−18.530|
|Reserva operativa de caja seleccionada|−3.000|
|Minorías, proxy económico|−1.200|
|Employee benefits no corrientes|−484|
|Pensión/otros beneficios corrientes, proxy FY25|−35|
|ARO/ambiental no corriente|−1.081|
|ARO/ambiental corriente, proxy FY25|−205|
|Propel accrued|−947|
|UTB/interés fiscal, último FY|−89|
|Remesas de receivables, prudencia|−269|
|Capital neto posterior desconocido|0|
|Equity calculado|{f(b['equityValue'])}|
|Acciones equivalentes, millones|{f(b['sharesMillions'])}|
|Valor por acción|{f(b['valuePerShare'])}|

La caja operativa 3.000 y minorías 1.200 son hipótesis, no saldos «restringidos» ni tasaciones. NCI book 1.172 / NI TTM 88 sirven de controles, sensibilidad 880–2.000; no sumar minority income como beneficio del común. Acciones: 390,072362 emitidas menos tesorería al 30 de septiembre de 2026 + 0,848 vested unissued proxy + 1,942 dilución incremental Q3 = 392,862362. Se conserva SBC en expense, sin proyectar nuevas recompras ni incrementar acciones arbitrariamente. Sensibilidad usando 398,953 weighted Q3: {f(ss['shares']['weightedQ3Sensitivity'])}. No es una cap table fully diluted observada el 3 nov.

Deuda 18.530 incluye 1.045 corriente + 17.485 no corriente; notas junior siguen siendo deuda, no 50% equity por tratamiento de agencias. Repagos 458 + 34 del 1 oct reducen deuda y caja por igual. Capacidad no utilizada: 6.400 no es caja. Dividendo 1,33 declarado el 16 oct, record 17 nov / pago 1 dic, no se resta como pagado. Autorización de recompra no es obligación ni acciones ya retiradas.

Propel: importe 947 acumulado está expresamente reconocido en Note 12, frente 867 dic 25. Sentencia 833 de 5 ago 25 e interés 10% están contenidos en el caso, no se suman ambos otra vez. Apelación abierta; se elimina su interés específico del beneficio normalizado de marketing y se reserva 947, con estrés 1.500/2.000. Exposición puede exceder provisión; no se afirma victoria judicial. [Note 12]({Q}).

Employee 484 abarca una categoría más amplia que el déficit actuarial individual: no se etiqueta como pensión neta exacta. Proxy corriente 35 usa FY25; no compensa automáticamente 199 de activo de pensiones extranjero. ARO/ambiental 1.081 ya incluye componente ambiental: no añadir 472 otra vez. Corriente 205 viene de FY25 y se somete a 0–400. Los pagos de pasivos existentes se reservan fuera del DCF; el modelo no inserta además un cronograma de esos mismos pagos. Nuevas obligaciones y mantenimiento siguen como riesgo económico. UTB 88 + 1 último FY no equivale a deferred tax 7.692 como deuda. Los escenarios no aplican beneficio fiscal automático a estas reservas.

Ventas de receivables 9M: 856 consisten en 592 cash + 264 repago no monetario; no son 856 de CFO extra. Remesas garantizadas 269 incluyen 244 por cobrar; reserva 269 es prudencia por capital de circulación, no clasificación probada como deuda financiera. Residual guarantees de leases 404 + 174 y cartas de crédito 2.211 son contingencias, no deuda utilizada por sumarlas todas. Leases operativos permanecen como gasto en FCFF, no se capitalizan además. No se agregan ganancias hipotéticas por redevelopment LA ni ventas no cerradas.

Los impuestos sobre renta y otros impuestos devengados aumentaron de 1.362 a 2.687 entre diciembre y septiembre. El 24% recurrente del DCF no liquida por sí solo esos devengos históricos. No se resta automáticamente todo el saldo como deuda: incluye obligaciones operativas y puede solaparse con la reserva de caja operativa 3.000, sin conciliación exacta del solapamiento. Se añade sensibilidad de reserva histórica adicional 0 / 1.325 / 2.687, que da valores base de {f(b['valuePerShare'])} / {f(b['valuePerShare']-1325/b['sharesMillions'])} / {f(b['valuePerShare']-2687/b['sharesMillions'])}. No se presenta como una deuda fiscal determinada. Separadamente, elevar el suelo anual de capex de 3.000 a 4.000 / 5.000, con inflación posterior, reduce el central a {f(next(r['value'] for r in ss['operations'] if r['name']=='common.capitalSpendingFloor2027' and r['assumption']==4000))} / {f(next(r['value'] for r in ss['operations'] if r['name']=='common.capitalSpendingFloor2027' and r['assumption']==5000))}; el suelo incrementado continúa también en el terminal, no desaparece en 2037; no se afirma que esos importes sean presupuestos publicados.

## 7. Comparables actuales: útiles para detectar trampas, no fijar target

Cierres 3 nov: PSX 271,94; VLO 387,65; MPC 427,34; MPLX 57,50. Fecha acciones/capital puede diferir y se etiqueta. No se aplica mediana a EPS/EBIT pico.

PSX EV con NCI book = 119.930,28. PBT + interés TTM 16.930 da 7,08x, pero contiene JV 1.567 y ganancias 2.103. Quitando disposiciones, denominador 14.827 y 8,09x. Si además se retira JV del denominador (13.260) y su DCF base del numerador, el múltiplo core es 8,37x: **depende del modelo JV**, no una observación pura. Tampoco elimina todo trading/credit income del ciclo.

VLO EV aproximado 112.436,54 / EBIT TTM 17.575 = 6,40x. Incluye deuda nominal 8.635 + finance leases 2.422, caja 9.840 excluyendo 181 restricted, NCI book 3.110. Minority book de DGD no es fair value y puede distorsionar comparación; no atribuir todo EBIT consolidado al común. [VLO Q3](https://www.sec.gov/Archives/edgar/data/1035002/000162828026067679/vlo-20260930.htm); [VLO FY25](https://www.sec.gov/Archives/edgar/data/1035002/000162828026011499/vlo-20251231.htm); [cierre](https://stockanalysis.com/stocks/vlo/history/).

MPC EBIT TTM 21.870 = 8.291 FY25 + 19.176 9M26 − 5.597 9M25. Market cap 116.357,11, net debt carrying 19.413 y minoría MPLX cotizada ≈21.045: EV 156.815,11 / EBIT = 7,17x. Incluyendo 224 de book NCI de subsidiarias MPLX, 7,18x; residual NCI no conciliado y unidades públicas: 366 millones redondeadas. Omitir MPLX daría 6,21x, incorrecto. Deuda principal + leases 33.492 vs 33.022 carrying implica sensibilidad 470; VLO usa nominal y PSX carrying, límite declarado. Venta anunciada 4.200 aún no cerrada no se resta. [MPC Q3](https://www.sec.gov/Archives/edgar/data/1510295/000151029526000071/mpc-20260930.htm); [MPLX Q3](https://www.sec.gov/Archives/edgar/data/1552000/000155200026000047/mplx-20260930.htm); [MPC FY25](https://ir.marathonpetroleum.com/investor/news-releases/news-details/2026/Marathon-Petroleum-Corp--Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx); [MPLX precio](https://ir.mplx.com/CorporateProfile/stock-information/stock-information/default.aspx); [MPC precio](https://www.investing.com/equities/marathon-petroleum-corp.-historical-data).

Los tres usan US GAAP y leases operativos como gasto, pero perímetro, JV/minorías, gains y mix midstream no son idénticos. Es contraste relativo con ajustes y límites, **no conjunto homogéneo plenamente normalizado** ni arbitraje. Los múltiplos bajos de trailing earnings pueden ser señal de pico, no automáticamente descuento.

## 8. Inverso, sensibilidades y falsadores

Manteniendo el resto del base, el precio 271,94 exige margen refinero 2031 de **{f(ss['reverse']['roots'][0]['margin2031Real2027'])}$/bbl en dólares 2027**, frente a 15 central y 17,26 realizado FY23. Es una solución mecánica, no consenso. El barrido 0–60 verificó monotonicidad y todas las raíces dentro del rango; no se presupone que un modelo con reinversión siempre sea monótono. El margen luego crece con inflación, no se compara directamente con un valor nominal de 2036.

|Margen maduro real 2027|Valor base con ese margen|
|---|---:|
'''
for r in ss['midcycle_margin']: report+=f"|{f(r['terminalRealMargin'])}|{f(r['value'])}|\n"
report+='''
Hay matrices completas WACC/g, costes, mantenimiento, impuestos, capital, JV tax/ROE/Ke y calendario en model/sensitivities.json. El modelo no convierte los percentiles de esas matrices en probabilidades. Las reservas de capital no eliminan la exposición a cola legal, cierre, accidentes, collateral y cambios de demanda.

Qué mejoraría la tesis: caja repetible después de mantenimiento y sin WC extraordinario; midstream creciendo con retornos y capital previsto; contratos JV/proyectos convirtiendo utilidad en cobros; margen maduro superior al central respaldado por años de oferta/demanda, no una interrupción temporal. Qué la debilita: spreads normalizados con costes fijos altos, menores beneficios de créditos desde 2030, overruns GTP/Ras Laffan/Coastal, otras obligaciones LA/Lindsey, mayor capital circulante y cobros JV insuficientes.

## 9. Calendario y próximos controles

Q3 ya publicado el 28 oct 2026 y 10-Q presentado. Dividendo: record 17 nov, pago 1 dic; no confundirlo con earnings. Próxima fecha exacta de resultados **no confirmada en una fuente primaria localizada**; la página de eventos no pudo verificarse de forma fiable durante esta consulta. No usar un calendario estimado de proveedor como confirmación final. Fuente de eventos para próxima revisión: https://investor.phillips66.com/events-and-presentations/default.aspx . Coastal Bend Q4 / early 2027 y polímeros 2027 son ventanas de proyecto, no citas exactas.

Estado: investigación con DCF revisada de forma independiente, con límites explícitos. La puerta de calendario que exija fecha oficial definitiva permanece pendiente; s2 «No» y Opportunity 70 no se convierten en aprobación. Confianza media-baja en valor central y baja en extremos; confianza mayor en historia y puentes contables que en normalización del ciclo, capacidad de distribución JV o valor económico de minorías.

## English decision summary

Phillips 66 generated exceptional Q3 cash flow, but $38/bbl refining margins and $14.08 quarterly EPS are not perpetual earnings. This analysis separates retained-fleet operating FCFF from affiliate equity cash flows, funds reinvestment, reserves disclosed liabilities, and does not double-count JV debt or capex. Current scanner Opportunity 70 and s2 “No” do not qualify an entry. The next exact earnings date remains unconfirmed. Current market multiples reflect peak-cycle earnings and materially different minority structures. The model is conditional research, not an order, entry approval or verified November cash-capital statement.

## Reproduction and limitations

All calculations run offline using the Python standard library. Original factual extracts and source URLs are included; full third-party filings are excluded. Run reproduce.py. History is reported/perimeter-aware rather than fabricated proforma. Model assumptions are deliberately visible. No proprietary consensus, plant-level cash budget, exact current JV tax split, full CPChem financials, precise NCI valuation or complete post-September capital reconciliation is claimed. These limits are not solved by running more formula checks.
'''
(P/'report.md').write_text(report)
print('report words',len(report.split()))
