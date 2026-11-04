import json,csv,pathlib
P=pathlib.Path(__file__).parent
I=json.load(open(P/'model/inputs.json'));R=json.load(open(P/'model/results.json'));S=json.load(open(P/'model/sensitivities.json'));H=json.load(open(P/'history/history_wide.json'));A=json.load(open(P/'history/analytics.json'));rates=json.load(open(P/'model/rates_results.json'));C=json.load(open(P/'comps/fmx_results.json'));atd=json.load(open(P/'comps/atd_results.json'));wal=json.load(open(P/'comps/walmex_results.json'))
f=lambda x:f'{x:,.2f}'
paras={
'pro_network':'OXXO México mantiene una red difícil de replicar: 24.759 tiendas y ventas mismas tiendas +9,2% en el tercer trimestre. Esa escala ayuda a distribuir productos, captar tráfico y extender servicios, pero el margen operativo bajó de 9,7% a 9,3% y el crecimiento no es enteramente volumen.',
'pro_cash':'El antiguo bloqueo de caja documental se ha cerrado: existen estados BMV para reconstruir tres ejercicios, cuatro trimestres y TTM. El CFO antes de los cinco movimientos de circulante e impuestos pagados crece 11,09% en nueve meses; es una señal mejor que la ausencia de caja, aunque no equivale a FCFF.',
'pro_kof':'La participación de FEMSA en Coca-Cola FEMSA es 47,2231% económica y equivale a 99,2079 millones de ADS de KOF. Los derechos económicos por acción KOF son iguales. La participación permite separar el embotellador del retail, sin sumar de nuevo dividendos ni descontar dos veces la deuda.',
'con_cash':'El 76,07% del aumento de CFO de nueve meses se explica por circulante y menores impuestos pagados. Spin mantiene 4.873,208 millones de MXN de obligaciones con clientes y cuentas inactivas; sus activos de respaldo no son caja excedente. Su mapeo exacto al balance consolidado sigue pendiente.',
'con_scope':'ImperialBrady no tiene un valor individual actual verificado en las fuentes revisadas. La rotura de botellas incorporada a D&A de KOF dentro de FEMSA y el interés de leases interino requieren aproximaciones explícitas. Las cifras de este modelo son una valoración parcial de activos identificados, no un precio justo completo de FMX.',
'con_gate':'La última fila real del escáner es del 3 de noviembre a 127,03 USD: QP 100 y Opportunity 75, por debajo de 85. La próxima fecha exacta de resultados no está confirmada. Esta revisión de un pendiente no habilita el filtro técnico, Stage 3.5 ni una entrada.'}
text=f'''# FEMSA / FMX: caja reconstruida, valoración parcial y atribución económica

Fecha de investigación: 4 de noviembre de 2026. Precios: cierre regular del 3 de noviembre. Estados: septiembre de 2026; eventos posteriores expresamente identificados. MXN millones salvo indicación contraria; valores por ADS en USD. Estado: **Investigación parcial revisada de forma independiente, sin aprobación de entrada.**

## 1. Decisión y alcance

El bloqueo antiguo de CFO ya no justifica dejar el expediente vacío. Hay evidencia suficiente para reconstruir caja, separar obligaciones de clientes y valorar explícitamente los negocios identificados. Pero no hay base para afirmar que el valor de ImperialBrady sea cero o que un balance de septiembre sea una conciliación exacta de noviembre. Por ello **no se publica un fair value total de FEMSA ni se etiqueta Stage 3 completo**.

Los escenarios propios de activos identificados arrojan {f(R['bear']['partial_value_per_fmx_ads_usd'])} / {f(R['base']['partial_value_per_fmx_ads_usd'])} / {f(R['bull']['partial_value_per_fmx_ads_usd'])} USD por ADS, frente a 127,03. Son dos DCF de diez años, ex-KOF y KOF, sin valor asignado a inversiones no verificadas. No son un intervalo estadístico ni una cota inferior demostrada: algunas reservas, márgenes y asignaciones pueden variar en ambas direcciones. Con KOF al precio bursátil observado, en lugar de su DCF propio, el caso central parcial asciende a {f(R['base']['hybrid_kof_market_mark_usd_per_fmx_ads'])}. La conclusión útil es que **no está demostrado un descuento de compra** bajo los supuestos explicitados, no que se haya tasado todo el grupo.

{paras['con_gate']}

La fila original A102 del 26 de octubre era 124,98 USD; A127 utilizó cierre 30 de octubre 126,10. Se conservan como antecedentes, separados de la observación actual. El negocio es consumo/retail diversificado con farmacia dentro del grupo; no se reclasifica toda FEMSA como empresa sanitaria. No se actualiza puntuación técnica con datos intradía.

## 2. Negocio, calidad y riesgos que importan

{paras['pro_network']}

La densidad de locales, logística, relación con proveedores y conveniencia favorecen frecuencia de visita. La expansión aporta ventas, pero 191 aperturas y 140 cierres en el trimestre producen sólo 51 tiendas netas. Costes laborales, cierres y menor ingreso comercial comparativo presionan rentabilidad. No se añade al EBIT un supuesto coste temporal de cierres ni se transforma todo aumento del ticket en crecimiento real. [S1]

Europa muestra +4,0% de ventas comparables mientras los ingresos convertidos a MXN caen 5,2%; Salud crece ventas 7,0% pero no confirma mejora proporcional del beneficio. Brasil OXXO se consolida desde febrero tras la separación de Grupo Nós, de modo que no todo crecimiento es orgánico a perímetro constante. El ex-KOF agregado incluye retail, movilidad, Europa, Salud, Spin, otros y eliminaciones; no es un estado legal independiente de OXXO. [S1,S3]

Spin tiene 11,7 millones de usuarios activos y 30 millones en lealtad, pero usuarios y transacciones no son utilidad distribuible. Compropago registra pérdida de nueve meses de 906,607 y aportación de capital de 340. No se suma una valoración fintech opcional ni se elimina su pérdida del beneficio del retail. QED entró en el negocio de crédito conservando FEMSA mayoría y consolidación; el porcentaje minoritario y precio no se divulgaron en el comunicado revisado. [S4,S9]

{paras['pro_kof']}

KOF aumenta volumen 5,3% e ingresos 10,9% en Q3, pero parte de la mejora de EBIT incluye recuperaciones de seguros. La estructura de franquicias, rutas y marcas ayuda, pero no elimina impuestos a bebidas, elasticidad de demanda, agua, costes de envases, divisas y dependencia comercial del sistema Coca-Cola. Se distingue crecimiento operativo de seguros no recurrentes; la normalización final figura en los inputs del modelo y el apéndice de propiedad. [S5]

Los contratos de embotellado se renuevan automáticamente por periodos de diez años salvo los avisos previstos y pueden terminar por incumplimiento. El BMV KOF al 30 de septiembre actualiza Nicaragua a mayo2036 y Brasil a octubre2034; las fechas antiguas de 2026/2027 no se tratan como vigentes. Costa Rica sigue septiembre2027, Uruguay/parte de Guatemala2028 y México2033/2035. La nota interina más reciente se prioriza sobre fechas diferentes del anual. El terminal presupone continuidad renovada, no un derecho legal perpetuo; se entrega estrés de reducción20%/50% de FCFF KOF desde2028 y ausencia de terminal posterior a2036, sin atribuir probabilidades o participación territorial no documentadas. [S23,S30]

## 3. Historia y calidad de beneficios

{paras['pro_cash']}

### 3.1 Tres ejercicios: bases conservadas, no mezcladas

| Periodo BMV | Ingresos | EBIT gestión | CFO BMV | Capex PPE+intangibles | Renta pagada |
|---|---:|---:|---:|---:|---:|
'''
for yr in ['FY2023_BMV','FY2024_BMV','FY2025_BMV']:
 z=H[yr];text+='| '+yr.replace('_BMV','')+' | '+' | '.join(f(z[k]) for k in ['revenue','ebit_management','cfo_bmv','cash_capex_ppe_intangibles','cash_lease_total'])+' |\n'
text+='''
El auditado FY2025 presenta CFO comparativo 2024 de 71.510 y 2023 de 49.679, frente a BMV 65.130,551 y 54.377,685. Los flujos de negocios discontinuados concilian algebraicamente la diferencia casi por completo; es una inferencia de presentación, no un crecimiento económico ni una cita del emisor explicando la reclasificación. El historial mantiene ambas versiones y no usa su mezcla para proyectar caja. EBIT de gestión tampoco equivale al tag bruto IFRS que incluye otras ganancias. [S2,S3]

### 3.2 Cuatro trimestres: flujo residual acumulado

| Periodo residual | Ingresos | EBIT gestión | CFO | Capex bruto | Renta pagada |
|---|---:|---:|---:|---:|---:|
'''
for yr in ['Q42025_residual','Q12026_BMV','Q22026_residual','Q32026_residual']:
 z=H[yr];text+='| '+yr+' | '+' | '.join(f(z[k]) for k in ['revenue','ebit_management','cfo_bmv','cash_capex_ppe_intangibles','cash_lease_total'])+' |\n'
text+='''
Los trimestres por diferencia no se hacen pasar por las publicaciones originales individuales. Q4 2025 publicó EBIT 24.546 frente a residual 24.529; Q2 2026 ingresos publicados 231.002 frente a residual 230.911; Q3 ingresos publicados 235.609 frente a residual 235.928. Se preservan revisiones/perímetros y se emplea FY+9M−9M consistente para el TTM. El CSV detalla cada concepto, periodo, contexto y procedencia. [S1–S3]

### 3.3 TTM y caja recurrente

Consolidado TTM: ingresos 894.726,716; EBIT de gestión 77.894; D&A de CFO 46.031; CFO BMV 109.852,734; compras de PPE/intangibles 37.033; cash rent 24.458. CFO menos inversión bruta, rentas e interés financiero separado deja 39.657,734, pero ese residuo no es FCFF ni corresponde íntegro a los accionistas FMX. Incluye KOF, sus minoritarios, impuestos de caja y movimientos de circulante. No se netean ventas de activos o seguros contra el capex del DCF.

{con_cash}

El puente de nueve meses es 88.749,884 frente a 49.977,733 de CFO: mejora 38.772,151, de la que 21.655,897 es circulante y 7.839 impuestos. La tasa fiscal contable 26,7% está deprimida por la ganancia ImperialBrady sin impuesto corriente. Excluyendo esa ganancia, 13.656/(51.167−11.952)=34,82%; no es automáticamente la tasa marginal de todos los segmentos. NI 37.456−11.952=25.504 frente a 20.359 implica +25,27%, no el +12,1% normalizado descrito por el emisor; no se certifica ese porcentaje sin otro puente. [S1–S3]

NI atribuible TTM directamente reportado en el BMV Q3 es 35.709,642 frente a 17.717,532. Una construcción del TTM previo con versiones históricas distintas no concilia y no se usa. No se publica un P/E ajustado basado en EPS inventado. SBC anual 2023/24/25 es 943/947/1.100; el tag interino de addback cero no demuestra que no exista gasto. Se conserva el gasto dentro del EBIT y no se agrega SBC a FCFF.

Ex-KOF TTM consistente: ingresos 589.775,364 frente a 539.664,863 (+9,29%); EBIT de gestión 32.617 frente a 30.781 (+5,96%); capex bruto 17.497,027 frente a 20.494,294 (−14,62%). Es crecimiento con presión de margen, no evidencia de desaparición del negocio. El menor capex no se extrapola automáticamente como nueva rentabilidad permanente.

## 4. Atribución económica y capital

Un ADS FEMSA son diez unidades BD, cada una con una B y cuatro D; una unidad B contiene cinco B. Las D reciben 125% del dividendo B mientras estén vigentes. Así, 1.968.615.615 BD + 1.417.048.500 B×5/6, dividido por diez, da **314.948.936,5 ADS equivalentes de distribución**. El denominador nominal es 338.566.411,5; no son ADS flotantes ni dilución exacta. Liquidación tiene igualdad por acción, de modo que se muestra sensibilidad nominal. KOF no presenta esa preferencia económica de series. [S3,S6,S7]

ImperialBrady cerró su fusión el 12 de marzo; FEMSA retiene aproximadamente 18,75%, ya sin influencia significativa y sin método de participación. Los 14.192 del antiguo 37,08% de IFS TopCo más ganancia de 11.952 **no certifican** un carrying value actual de 26.144. Los activos financieros no corrientes ex-KOF 30.899,215 están agrupados. Se dejan inversiones no valoradas fuera del total parcial y se muestra sensibilidad separada, sin denominarlas cero económico o techo de valor. [S2,S3,S6]

### Puente a equity, sin sumar dos veces caja o restar dos veces leases

- Caja ex-KOF 64.290,710 e inversiones separadas 6.112 al 30 de septiembre. Deuda financiera ex-KOF aproximada {debt}; la tabla del emisor está redondeada, no es deuda legal exacta a noviembre.
- Reservas ex-KOF: operación 15.000 (supuesto), fondos cliente Spin 4.873,208 (reserva prudencial por mapeo no resuelto), déficit neto de planes 5.546,438, impuesto pagadero no corriente 2.618,794. Este último no está identificado como impuesto incierto y no se etiqueta así. Minoritarios residuales 2,526 son proxy contable, no valor de mercado; sensibilidad 0–3.000. Los activos de pensión ya están neteados en la obligación y no se suman otra vez.
- La reserva Spin puede ser excesiva si parte de los respaldos ya queda fuera de caja/inversiones consolidadas; se muestra escenario de reserva cero. No se declara que el pasivo completo esté exactamente embebido en la caja del holding. Hay 293,529 de efectivo y 4.485,744 de reportos en la entidad regulada, bajo NIF/CNBV, no el mismo perímetro IFRS. [S4]
- KOF: caja 46.772,350, deuda financiera 84.370, reserva derivada de diferencia de deuda neta cubierta 2.294,350, déficit neto de planes 5.719,002 y caja operativa 10.000. Minoritarios de subsidiarias KOF se reservan a 15.000 como hipótesis, frente a libro 9.255,132 y beneficio minoritario TTM 1.431,172; no son los minoritarios de FEMSA. Sensibilidad 9.255–25.000.
- Las rentas completas ya se descuentan operativamente: **no se restan otra vez leases ex-KOF 110.839,547 ni KOF 3.978,038**. Dividendo KOF no forma parte del FCFF ex-KOF; la participación se añade una sola vez después de valorar equity KOF.
- El pago KOF del 13 de octubre fue 4.065,110, de los que FEMSA recibe 1.919,672. El dividendo FEMSA del 15 de octubre, aplicado a acciones de septiembre, implica salida estimada 10.087,608; ex-KOF neto −8.167,936. El DCF KOF resta su salida; al usar KOF a precio de noviembre no se descuenta de nuevo. El importe FEMSA exacto depende de acciones elegibles en octubre.
- El bono CHF300m liquidado el 14 de octubre suma deuda y caja si no se gastó: no crea equity gratis. No se conoce su uso neto completo ni el saldo noviembre; residual central cero con sensibilidad ±10.000, no afirmación de ausencia de movimientos. ASR hasta USD280m sigue sin liquidación final verificada; recompras ya reflejadas en septiembre no se deducen otra vez ni se anticipan acciones finales. [S1,S8]

El puente ex-KOF central es {xb}; el puente KOF es {kb}. Se conserva separación entre hechos, estimaciones y reservas. El conjunto no es una conciliación observada de caja al 3 de noviembre.

## 5. Dos DCF: convención y financiación del crecimiento

Se eligió antes de valorar una suma de partes porque FMX consolida 100% de KOF pero posee sólo 47,2231%. Un FCFF consolidado dividido por ADS sin minoritarios sobrevaloraría FEMSA; restar patrimonio minoritario contable completo tampoco valora adecuadamente esa participación.

Rentas operativas: EBIT económico = EBIT IFRS + D&A ROU − renta completa; después se añade sólo depreciación física/no-ROU. Para ex-KOF, sin D&A ROU interina segmentada, se parte de EBIT + D&A de CFO − renta y se resta depreciación física estimada. FY2025 demuestra diferencia de 2.057,005 entre D&A KOF dentro de FEMSA (incluye roturas) y standalone; se usa **únicamente como proxy TTM**, con sensibilidad 0–4.000. D&A física ex-KOF se ancla a 13.307/549.208=2,423%; no se afirma exactitud de ese recast.

El EBIT económico ex-KOF inicial estimado es {exebit}; margen {exmargin}%. KOF utiliza EBIT IFRS consistente FY+9M−9M de44.706,809, menos recuperación neta de seguros TTM aproximada2.462 (Q4251.149+9M261.313), másROU1.130 menosrenta1.535: EBIT económico41.839,809. Se reduce también cada margen proyectado en2.462/304.951,352, no sólo la cifra inicial. El ajuste de seguros conserva diferencias de28 entre FY25PR y nota auditada y102 entre sumas trimestrales y9M26; es proxy, no puente IFRS exacto. Esas diferencias quedan en sensibilidad, sin borrar datos originales. El interés de lease de nota es gasto, no pago exacto: FY2025 difiere en 6; se conserva como límite y se prueba sensibilidad. No se añaden los 8.062 de otros cargos no monetarios que el comunicado mezcla con D&A de nueve meses.

Años 2027–2036: cinco años explícitos y cinco de transición. El TTM es proxy de salida 2026, sin crecimiento inventado en el stub. Se incluye stub de 58 días al 31 de diciembre y descuento de FY2027 a 1,159 años desde el 3 de noviembre. El stub usa caja normalizada prorrateada y no pretende captar estacionalidad Q4. La omisión aislada del stub y el acortamiento del calendario son efectos distintos.

FCFF = NOPAT − reinversión neta. Reinversión elegida = máximo entre ΔNOPAT positivo/ROIC marginal y el suelo de capex físico bruto menos depreciación física más 2% del incremento positivo de ventas como circulante. Por tanto, también se financia la subida de márgenes; no se trata como beneficio gratis. El método no suma ambas medidas y duplica inversión. No libera capital en contracciones. En terminal se financia NOPAT×g/ROIC y se respeta el suelo físico/circulante, con WACC > g.

| Segmento/escenario | Crecimiento inicial / final | Margen inicial / final | Impuesto | ROIC marginal | Capex bruto/ventas | WACC USD | g MXN |
|---|---|---|---:|---:|---:|---:|---:|
'''.format(con_cash=paras['con_cash'],debt=f(I['capital']['ex_kof_financial_debt_estimated']),xb=f(R['base']['ex_kof_capital_bridge']),kb=f(R['base']['kof_capital_bridge']),exebit=f(I['anchors']['ex_kof']['economic_ebit_after_rent_estimated']),exmargin=f(100*I['anchors']['ex_kof']['economic_ebit_after_rent_estimated']/I['anchors']['ex_kof']['revenue']))
sc=json.load(open(P/'model/scenarios.json'))
for name,v in sc.items():
 for seg,s in v.items():text+=f"| {seg} {name} | {s['growth'][0]*100:.1f}% / {s['growth'][-1]*100:.1f}% | {s['margin'][0]*100:.2f}% / {s['margin'][-1]*100:.2f}% | {s['tax']*100:.0f}% | {s['roic']*100:.0f}% | {s['capex_ratio']*100:.1f}% | {s['wacc_usd']*100:.1f}% | {s['g']*100:.1f}% |\n"
text+='''
Son hipótesis del analista. La base ex-KOF crece menos que el último TTM, recupera margen gradualmente y exige capex 3,2% frente a 2,97% de caja reciente. KOF mantiene inversión física superior a depreciación y no capitaliza seguros. Bear recoge menor crecimiento, presión laboral/comercial y mayor inversión; bull necesita ejecución sostenida y capital más barato. No se aplican probabilidades inventadas.

### Coste de capital y moneda

Treasury del 3 de noviembre 4,95%; ERP NYU del 1 de noviembre 4,41%, calculada originalmente con Treasury5,29%. Es una combinación de fechas, no una ERP implícita recalculada al día. Para reflejar la convención de default estadounidense 0,22%, se usa rf ajustado4,73% y ERP4,63%; se añade prima México julio2026 de2,7202% como proxy geográfico, no promedio exacto multinacional. Brasil3,0984%, Chile1,0473% y Suiza0 muestran sus limitaciones. [S10–S12]

Betas seleccionadas1,00 retail y0,70 KOF se contrastan con referencias sectoriales desapalancadas sin caja0,78 retail general/0,85 alimentación/0,58 bebidas. No son estimaciones estadísticas de FMX. Beta proveedor0,18 se declara, pero no determina por sí sola todo el riesgo económico. Deuda financiera objetivo20%/16%, coste USD6,5%, impuestos33%/30% producen WACC mecánicos10,5351%/9,7086%. Los11%/10,5% elegidos añaden46,5/79,1pb por juicio, **no redondeo**. Se muestra sensibilidad amplia de descuentos. [S10–S13]

Flujos nominales MXN se descuentan a WACC MXN=(1+WACC USD)×1,02−1: base13,22% y12,71%. El2% es depreciación cambiaria anual supuesta, no forward observado. g terminalMXN4,5% equivale a2,451% USD bajo esa misma convención. La equivalencia con traducir cada flujo a USD año por año se prueba numéricamente. Sólo después se divide a spot ECB3nov18,597012MXN/USD; no se usa el18,0609 de presentación de septiembre. [S14]

### Proyección central: ex-KOF

| Año | Ventas | EBIT tras rentas | NOPAT | D&A física | Suelo capex bruto | Reinversión neta | FCFF |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for row in R['base']['ex_kof']['rows']:text+='| '+str(row['year'])+' | '+' | '.join(f(row[k]) for k in ['revenue','ebit_after_rent','nopat','physical_da','gross_physical_capex_floor','net_reinvestment_selected','fcff'])+' |\n'
text+='''
### Proyección central: KOF

| Año | Ventas | EBIT tras rentas | NOPAT | D&A física | Suelo capex bruto | Reinversión neta | FCFF |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for row in R['base']['kof']['rows']:text+='| '+str(row['year'])+' | '+' | '.join(f(row[k]) for k in ['revenue','ebit_after_rent','nopat','physical_da','gross_physical_capex_floor','net_reinvestment_selected','fcff'])+' |\n'
text+='''
## 6. Resultados parciales e inverso

| Escenario | EV ex-KOF MXN | Equity KOF MXN | 47,2231% KOF MXN | FMX parcial USD/ADS | Denominador nominal | KOF a mercado, híbrido |
|---|---:|---:|---:|---:|---:|---:|
'''
for name,z in R.items():text+='| '+name+' | '+' | '.join(f(x) for x in [z['ex_kof']['enterprise_value'],z['kof_equity_common'],z['femsa_owned_kof_value'],z['partial_value_per_fmx_ads_usd'],z['nominal_equal_shares_sensitivity'],z['hybrid_kof_market_mark_usd_per_fmx_ads']])+' |\n'
text+=f'''
Terminal representa {R['base']['ex_kof']['terminal_share']*100:.1f}% del EV ex-KOF y {R['base']['kof']['terminal_share']*100:.1f}% del EV KOF. El modelo propio KOF central implica {f(R['base']['kof_standalone_value_per_ads_usd'])} USD/ADS frente a116,42 cotizados; esta diferencia importante explica parte del bajo SOTP, y por eso se incluye contraste manteniendo KOF a mercado. No se afirma que el mercado pruebe el DCF.

Incluso fijando KOF al cierre observado, resolver127,03 con sólo un incremento paralelo de margen ex-KOF, financiando ΔNOPAT/ROIC, exige margen inicial {S['inverse']['required_year1_margin']*100:.2f}% y terminal {S['inverse']['required_terminal_margin']*100:.2f}%. Es un ejercicio mecánico deliberadamente restrictivo, **no una previsión viable ni la única combinación de precio**: el salto inicial de margen exige fuerte reinversión. El residual de activos no valorados necesario sería {f(S['inverse']['unpriced_asset_value_required_mxnm_kof_market_mark'])} M MXN con KOF a mercado. No se identifica ese residual con ImperialBrady ni se afirma que la cuenta contable agrupada limite su valor.

{paras['con_scope']}

### Sensibilidades seleccionadas

| Cambio aislado | Valor parcial USD | Híbrido KOF a mercado USD |
|---|---:|---:|
'''
for row in S['one_way']:
 if any(x in row['case'] for x in ['Unpriced','Spin','bottle','physical capex','spot MXN','tax 0.']):text+=f"| {row['case']} | {f(row['partial_value_usd'])} | {f(row['hybrid_kof_mark_usd'])} |\n"
text+='''
También se entregan rejilla WACC/g, ROIC12–25%, minoritarios, impuestos históricos, caja operativa, saldo post-septiembre ±10.000 y denominador nominal. Las sensibilidades de inversiones no verificadas son escenarios, no estimaciones de un activo. No se calcula un MOS de compra a partir de la cifra parcial.

## 7. Contraste relativo actual

Cierres3nov: ATD81,77CAD, WALMEX50,04MXN, KOF116,42USD. ATD se convierte con ECBUSD/CAD0,71554759. No se usan precios intradía de4nov. Las cuentas de ATD son Q1FY27 al19jul y TTM52semanas; Walmex y FEMSA hasta septiembre. [S15–S20]

| Comparación | EV/EBIT | Convención |
|---|---:|---|
'''
text+=f"| ATD | {atd['ev_normalized_ebit']:.2f}x | EBIT TTM4.727,8 menos recuperación legal260,9; deuda y leases, pensión y put minoritario280 |\n| WALMEX | {wal['ev_ebit_reported']:.2f}x | EBIT reportado77.491,705; leases y pensión; sin normalización inventada de beneficio puntual |\n| FMX ex-KOF implícito | {C['rows'][0]['ev_management_ebit']:.2f}x | KOF a mercado, derechos de distribución, no inversiones no verificadas |\n| FMX ex-KOF sensibilidad | {C['rows'][1]['ev_management_ebit']:.2f}x | deducción hipotética30.899,215 de activos no core, no valor validado |\n"
text+='''
ATD usa EV66.290,839 M USD, caja3.198,3 excluyendo10,6 restringida; deuda financiera10.329,3 y leases5.049,9; 918,9macciones diluidas. El pasivo de put280 sustituye al NCI de libro128,1 relacionado con Bélgica; añadir todo ese NCI es sensibilidad, no doble deducción central. La adquisición Żabka está pendiente de condiciones/aprobación en la evidencia revisada, sin proforma. Fuel bruto, tiendas propias y mezcla geográfica impiden equivalencia perfecta con OXXO. [S15,S16]

WALMEX usa acciones17.137,424m, caja27.064,984, leases84.019,971 y pensiones3.953,525; no se identifica deuda financiera adicional en el balance. EV918.465,225; al añadir impuesto no corriente y otras provisiones,11,96x. El beneficio SG&A puntual deQ4FY25 no está cuantificado en el release; el múltiplo reportado no se llama plenamente normalizado. P/E17,53x usa suma de EPS2,855, no la división por acciones actuales. [S17,S18]

Para FEMSA el market cap agregado deducido del ADR es una asignación por derechos económicos, no capitalización observada de cada serie. Con unidades nominales, el múltiplo ex-KOF sube a21,03x. La comparación incluye leases en EV para mantener EBIT IFRS; el DCF opera con rentas y no mezcla esa deuda. El mayor múltiplo exige justificar superioridad de crecimiento/rentabilidad, no aplicar automáticamente una mediana o comprar porque una marca sea buena.

## 8. Qué falta y qué cambiaría la conclusión

1. Valor individual actual y condiciones de monetización de ImperialBrady, con impuestos/costes de realización si proceden. Sin ello no existe total completo del holding.
2. Reconciliar D&A KOF/botellas de los interinos, efectivo de intereses de leases y recursos de clientes Spin contra consolidado. Los proxies son visibles y no completan la contabilidad por decreto.
3. Capital exacto tras dividendos, ASR, bonoCHF y otros movimientos; acciones elegibles/dividendo reales. El puente mínimo conocido no certifica noviembre.
4. Próxima fecha oficial exacta y evidencia técnica actual. La página oficial mantiene todavía la llamada28oct como upcoming; ese evento ya ocurrió. No se traslada a un día inventado de febrero2027. [S21]
5. Para mejora fundamental: crecimiento que se convierta en margen después de salarios/rentas, caja antes de circulante e impuestos, disciplina de capex, evolución de pérdida Spin y seguros KOF fuera de beneficios recurrentes. La tesis se debilita si expansión no recupera márgenes o fondos cliente se usan como argumento de caja disponible.

No se emite orden, precio de entrada, tamaño, stop ni aprobación. Se cierra la búsqueda de caja primaria, no todas las puertas del plan.

## 9. English summary

FEMSA's historical cash-flow evidence is now available and reproducible. However, most of the nine-month CFO improvement comes from working capital and lower cash taxes, and Spin customer funds are not distributable surplus cash. The analysis separates ex-KOF retail from FEMSA's47.2231% economic KOF stake, expenses full lease rent, funds growth and translates nominal MXN cash flows consistently.

The scenario outputs cover identified assets only. ImperialBrady has no independently verified current standalone value in the reviewed material; interim bottle-breakage/lease allocation and the post-quarter capital bridge retain disclosed assumptions. No complete FEMSA fair value or entry approval is issued. An alternative marks KOF at its observed closing price rather than relying on the standalone DCF. Current peer multiples do not establish a buying discount. Earnings timing remains unconfirmed and the last scanner Opportunity score75 is below85.

## 10. Fuentes y reproducción

El paquete público contiene cálculos propios, transcripciones mínimas de hechos y enlaces, no PDFs/filings completos. Python estándar reproduce historia, modelos, sensibilidades, comparables, informe y QA. Los datos históricos nulos no se sustituyen por cero. Las aproximaciones del modelo no se retroescriben como cifras observadas.

'''
sources={
'S1':'https://femsa.gcs-web.com/static-files/e56d3a69-ab40-4db7-ba22-8af9a2602dd7','S2':'https://annualreport.femsa.com/descargables/eng/Femsa_Estados_financieros_2025_eng.pdf','S3':'https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1598706_2026-03_1.zip','S4':'https://spinbyoxxowebsite.cdn.prismic.io/spinbyoxxowebsite/Hrw7b8KtckGMxOaU_COPAEstadosfinancierosQ3_26.pdf','S5':'https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1597622_1.pdf','S6':'https://www.sec.gov/Archives/edgar/data/1061736/000162828026027231/fmx-20251231.htm','S7':'https://www.sec.gov/Archives/edgar/data/910631/000162828026025313/exhibit29-descriptionofsec.htm','S8':'https://femsa.gcs-web.com/static-files/5cb60cd8-228c-40a1-9a90-b083002aa66a','S9':'https://www.femsa.com/wp-content/uploads/2026/06/ENG-PR-QED-vFinal-07.06.26-Closing.pdf','S10':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','S11':'https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','S12':'https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctrypremJuly26.xlsx','S13':'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html','S14':'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html','S15':'https://corporate.couche-tard.com/image/2027_Q1_Quarterly_Report_EN.pdf','S16':'https://corporate.couche-tard.com/2026-06-22-ALIMENTATION-COUCHE-TARD-ANNOUNCES-ITS-RESULTS-FOR-ITS-FOURTH-QUARTER-AND-FISCAL-YEAR-2026','S17':'https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1598123_1.pdf','S18':'https://files.walmex.mx/upload/files/2025/EN/Quarterly/4Q25/Walmex_Earnings_Release_4Q25.pdf','S19':'https://stockanalysis.com/stocks/fmx/history/','S20':'https://stockanalysis.com/stocks/kof/history/','S21':'https://femsa.gcs-web.com/news-events/events','S22':'https://investors.coca-colafemsa.com/assets/files/reportes_resultados_en/2025/eeff-kof-2025-eng-1.pdf','S23':'https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1597620_2026-03_1.zip','S24':'https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1598127_2026-03_1.zip','S25':'https://stockanalysis.com/quote/tsx/ATD/history/','S26':'https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=WALMEX%2A%3AMEX','S27':'https://corporate.couche-tard.com/image/COTA78_ACT_Annual-Report_WEB_EN_20240626.pdf','S28':'https://zabkagroup.com/zabka-group-delivers-continued-growth-in-9m-2026-surpassing-13000stores-and-further-improving-profitability/','S29':'https://stockanalysis.com/stocks/fmx/','S30':'https://www.sec.gov/Archives/edgar/data/910631/000162828026025313/kof-20251231.htm'}
text+='\n\n'.join(f'[{k}] {u}' for k,u in sources.items())+'\n';(P/'report.md').write_text(text);(P/'report_evidence_paragraphs.json').write_text(json.dumps(paras,ensure_ascii=False,indent=2)+'\n');(P/'source_urls.json').write_text(json.dumps(sources,indent=2)+'\n');print('report words',len(text.split()))
