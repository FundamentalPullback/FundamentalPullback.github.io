from pathlib import Path
import json
p=Path(__file__).parent;r=json.loads((p/'model/results.json').read_text());c=json.loads((p/'capital/bridge_verified.json').read_text());notes=(p/'research_notes.md').read_text();f=lambda x:f'{x:,.2f}'
s='''# YOU — crecimiento tras Q3, pero la caja y el capital Up-C requieren separar derechos

Corte: 4 noviembre 2026, después del cierre regular. USD millones salvo acciones en millones y USD/acción. Investigación parcial revisada independientemente. No valoración total ni entrada.

## Conclusión

Clear Secure crece y mejora el beneficio operativo. Su negocio requiere acuerdos con aeropuertos, socios de tarjetas y regulación de identidad; el número total de miembros no equivale a suscriptores pagadores. El salto de hoy no sustituye valoración ni disciplina de entrada. Los flujos consolidados no pertenecen íntegramente a las acciones A: la estructura Up-C y el acuerdo fiscal TRA obligan a separar matriz y Alclear.

El nuevo CSV muestra59,25, QP90, Opportunity90 y RSI86,4. El cierre regular independiente4nov a16:00EST es59,06, +23,65%; la cotización posterior no se usa. No se reconcilia por invención la pequeña diferencia del CSV. No se hereda aprobación técnica de otra fecha ni se interpreta RSI alto como aprobación. Fuente: https://stockanalysis.com/stocks/you/history/ .

Q3 se publicó hoy antes de apertura y la llamada fue a08:00ET: ya ocurrió. No se ha confirmado la próxima fecha trimestral exacta. El calendario consultado aún etiqueta como próximo el evento ya pasado; no se confunde con2027. El próximo evento de caja documentado es dividendo0,15, registro10dic/pago24dic, no resultados. Fuente: https://ir.clearme.com/news-events/ir-calendar ; https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000053/clearq32026pressreleaseear.htm .

## Ventaja competitiva y condiciones que pueden romperla

La red aeroportuaria, relaciones comerciales, personal y plataforma de identidad permiten distribución de suscripciones, servicios premium y nuevos usos empresariales. Q3ingresos292,850 crecen27,8%, bookings323,5 crecen24,4%, CLEAR+ activos8,474M crecen14,5%; miembros totales46,741M crecen30,7%. Los miembros totales incluyen usos gratuitos y acumulación histórica; los activos incluyen pruebas, familiares y períodos de gracia. Los históricos activos fueron recast por cuentas caducadas durante un proyecto de facturación. No se infiere retención pagada ni ARPU homogéneo dividiendo ingresos por todos los miembros.

El despliegue de eGates en53 aeropuertos y Concierge en42 es progreso de producto, no ingresos adicionales garantizados. La compañía informa63 aeropuertos CLEAR+ tras Tampa a comienzos de noviembre, frente62 al30septiembre; distinguir fechas. GuíaQ4ventas299–302 y bookings335–340; FCF anual al menos490 es guía, no caja libre para A ni perpetuidad. Fuente: https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000053/clearq32026pressreleaseear.htm .

El10-K describe renovación multianual de American Express en febrero2026, pero no permite certificar una renta perpetua con términos invariables. Los acuerdos de aeropuertos pueden no renovarse o terminar por conveniencia; en algunos casos la contraparte es una aerolínea. TSA y tecnologías de identidad alternativas pueden cambiar propuesta de valor y requisitos. Son riesgos divulgados por el emisor, no afirmación de que un contrato haya terminado. No se declara una brecha de privacidad o infracción sin prueba. Fuente: https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000006/you-20251231.htm .

'''
s+=notes.replace('# CLEAR Secure (YOU): historia y perímetro de capital','## Historia y perímetro: evidencia verificable')
s+='''
## Modelo condicionado: alcance y método

El modelo de diez años valora una operación consolidada hipotética después de un impuesto económico normalizado25% sobre el100% del beneficio, no la tasa contable consolidada de una partnership. Mantiene SBC y costes de socios ya reflejados en ingresos; no añade315 a beneficio ni FCF. Ancla ventas1064,361 y EBIT281,785. No se suma toda amortización intangible7,831 como si necesariamente fuera adquisición: incluye patentes y no se ha explicado la concentraciónQ4FY25. Tampoco se elimina gasto de personal o adquisición de clientes por llamarlo crecimiento.

Los márgenes previstos son después de todos los costes operativos y SBC. El D&A físico/software futuro seleccionado2,5% de ventas se aproxima al PPE TTM26,374; no se pretende reconstruir todo el gasto intangible futuro a partir de una cifra agregada. Capex de caja3,5% de ventas, nunca inferior a125% de D&A, incluye software y equipos; SBC capitalizada adicional0,1% financia la parte no monetaria. Son hipótesis, no guía del emisor. No se añade otra vez el software completo encima del capex reportado que ya lo contiene.

Circulante neto central0% del incremento de ventas no perpetúa el beneficio de cobros anticipados: se prueban−10/0/5/10%. El saldo diferido603,646 obliga a prestar servicio; no se resta como deuda financiera completa después de incluir sus costes futuros, ni se suma como caja libre otra vez. La liquidación anual de socios se trata mediante costes netos de ingresos y financiación estable; no se concede un addback315 recurrente. El saldo heredado83,639 puede solaparse con pagos implícitos; sensibilidad adicional0/83,639/163,391 sin afirmar deuda incremental exacta.

La reinversión anual es el máximo entre capex−D&A +SBCcapitalizada +circulante y aumento positivo de NOPAT/ROIC. Esto financia también una recuperación del margen, no supone que todo el beneficio adicional llegue gratis. En terminal persisten ambos suelos: físico y NOPAT×g/ROIC. No se resta nuevamente pasivo por alquiler porque renta continúa en EBIT. Los compromisos aeroportuarios y de marketing se atienden en márgenes/caja operativa, no como deuda adicional automática.

Escenarios adverso/base/favorable: crecimientos primeros5años10/8/6/5/4%,20/18/15/12/10% y26/24/20/18/15%; márgenes24% constante,28/29/30/30/30%,30/32/34/35/35%. Años6–10 crecimiento converge linealmente a2,5/3/3%; margen se mantiene. ROIC15/20/25%, descuento12/10/9%, impuesto25%. No son probabilidades ni previsiones certificadas. Los años son períodos móviles desde4nov2026; no se presentan como ejercicios fiscales exactos.

Referencia de capital: Treasury10años4,90%, ERP4,41% y beta0,92 producen coste propio8,9572% sin deuda dispuesta;10% central incorpora prima seleccionada, no redondeo ni WACC del emisor. El reducido acceso residual al revolver14,4 no se suma como caja. Fuentes: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve ; https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm ; https://stockanalysis.com/stocks/you/statistics/ .

## Puente por derecho económico, no por EPS

Se utiliza portada30oct:99,618115M A y31,679772M unidades de terceros. Se agregan4,213967M RSU de septiembre como dilución bruta seleccionada, sin añadir los antiguos FounderPSUs ni las0,893234M performance por segunda vez. Resultan103,832082M A con premios y135,511854M unidades económicas. Se conservan SBC futuras en márgenes; premios existentes y gasto futuro representan períodos distintos. No hay una afirmación de capital final noviembre ni de emisión neta futura.

Caja/valores632,969 menos200 operativos seleccionados y0,15 por unidad básica de octubre como proxy del dividendo anunciado deja413,274317. La fecha de registro y las unidades pueden cambiar: no es desembolso certificado. Las nuevas recompras autorizadas175 y saldo254,4 no están ejecutados ni se deducen anticipadamente. El modelo no usa ingresos de préstamos no contratados.

Como caso de asignación, todo el excedente líquido se sitúa en Alclear y se reparte por unidades; **no es un hecho demostrado**. La fórmula por A es (EVoperativo +cajaOpCo)/unidades económicas + (caja propia matriz +activo fiscal seleccionado −TRA matriz)/acciones A con premios. El TRA267,786 se descuenta sólo de la matriz, no se reparte entre NCI como si ellos lo debieran. Se prueba asignación de0/50/100% del excedente a matriz; el10-K advierte expresamente que la matriz puede acumular exceso de distribuciones fiscales.

DTA central no tasada: cero crédito económico seleccionado, junto con descuento íntegro del TRAcontable267,786. Es un stress prudente, no mejor estimación de la pareja fiscal ni demostración de que el DTA valga cero. Sensibilidades con crédito bruto267,786 o315,042 mantienen la restaTRA una sola vez. La diferencia contable47,256 no se añade y vuelve a restar por segunda vez. No se usan a la vez impuestos reducidos por esos mismos ahorros y un activo fiscal agregado. Futuros intercambios, nuevos TRA/DTA, plazos y restricciones fiscales siguen pendientes: no hay valor total certificado.

El10-K añade que cambio de control o incumplimiento material puede acelerar pagos del TRA utilizando supuestos contractuales y una tasa de descuento distinta del coste de capital. Los pagos pueden exceder el ahorro fiscal real; beneficios posteriormente rechazados no originan reembolso inmediato, sino posible compensación contra pagos futuros, que podría no bastar. Por ello267,786 contables no son valor presente exacto ni techo de exposición. No se afirma que haya ocurrido ninguno de esos desencadenantes. Fuente: https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000006/you-20251231.htm .

| Caso condicionado | EV operativo100% | Residuo por A con hipótesis | PVterminal/EV | Déficit acumulado máximo |
|---|---:|---:|---:|---:|
'''
for n,o in r['cases'].items():s+=f"|{n}|{f(o['ev'])}|{f(o['conditionalClassAResidual'])}|{f(o['pvTerminalShare']*100)}%|{f(o['peakFunding'])}|\n"
s+='''
Los déficit centrales se cubren aritméticamente con el excedente líquido seleccionado, antes de necesidades no conciliadas. Los flujos negativos ya restan EV: deducir además ese déficit del puente duplicaría el coste. Esto no prueba que toda la caja sea transferible entre entidades ni que una obligaciónTRA contingente sea exigible inmediatamente.

### Diez períodos del caso base

| Año | Ventas | EBIT | NOPAT económico | Reinversión | FCFF |
|---|---:|---:|---:|---:|---:|
'''
for q in r['cases']['base']['rows']:s+=f"|{q['year']}|{f(q['revenue'])}|{f(q['ebit'])}|{f(q['nopat'])}|{f(q['reinvestment'])}|{f(q['fcff'])}|\n"
a=r['inverseFinanced'];b=r['inverseEfficiency']
s+=f'''\n## Qué exige59,06\n\nCon crecimiento base y toda mejora de NOPAT financiada aROIC20%, exige añadir{f(a['shiftPp'])} puntos de margen, hasta{f(a['terminalMargin']*100)}% terminal. El primer FCFF sería{f(a['firstFcff'])}, fuera de la caja líquida seleccionada y del revolver disponible. **No es escenario de entrada financiado**. La alternativa que atribuye el incremento de margen a eficiencia sin capital adicional exige{f(b['shiftPp'])} puntos y{f(b['terminalMargin']*100)}% terminal: tampoco es promesa. Ambas raíces verifican bracket, residual y1000 intervalos estrictamente monótonos.\n\n'''
for k,vs in r['sensitivities'].items():s+='- '+k+': '+'; '.join(f"{x['input']:g} → {f(x['value'])}" for x in vs)+'.\n'
s+='''
## Contraste de precio y límites relativos

No se ha construido una cesta homogénea de aeropuertos/identidad con capital Up-C y contratos comparables. No se sustituye ese requisito con una mediana de software, aerolíneas o múltiplo del proveedor. La capitalización sólo de A y NI atribuible a A son un perímetro diferente al EV100%/EBIT100%; cruzarlos produce un múltiplo falso. Los múltiplos publicados del proveedor usan denominadores que no concilian con las cifras primarias actualizadas. No se adoptan como valoración ni se certifica Stage3 integral.

El precio59,06 es bastante superior al caso base condicionado33,12, pero éste tampoco es valor total porque no tasa la parejaDTA/TRA ni asigna caja real por entidad. La conclusión práctica es esperar conciliación, no una recomendación de venta ni una aprobación automática del caso favorable.

## Seguimiento de tesis

A favor: crecimiento de suscripciones activas y bookings, margen después de SBC, despliegue de producto y caja TTM aun después del pago de socios. Exigir seguimiento de crecimiento neto pagador, coste/retención por canal, gasto credit-card reconocido contra ingresos, capitalización de software, cumplimientoTSA y renovación de contratos. La valoración no depende de suponer que cada miembro gratuito monetiza al mismo precio.

Invalidación: pérdida de condiciones comerciales clave, desaceleración con mayores pagos a socios, deterioro de margen, nueva inversión/compensación desproporcionada, deterioro de experiencia/seguridad, cambios regulatorios que reduzcan la ventaja y caja matriz no disponible para Alclear. Próximo dividendo no resuelve estos riesgos ni sustituye fecha de resultados.

## Evidencia publicable ES/EN

YOU crece22,86% en ingresos TTM y69,09% en EBIT, con margen26,47%. La mejora operativa no equivale a que todo el flujo consolidado corresponda a las acciones A.

YOU grows trailing revenue22.86% and operating profit69.09%, reaching a26.47% operating margin. This does not mean all consolidated cash flow belongs to Class A shares.

El pago de315 millones liquida pasivos por beneficios de tarjetas ya reconocidos contra ingresos. No es una pérdida excepcional ni se suma al FCF TTM458,037.

The315million payment settles card-benefit liabilities already recognized against revenue. It is not an exceptional loss and must not be added to trailing FCF458.037.

Caja por entidad, TRA, activos fiscales y dilución siguen condicionados. Los casos del dossier no certifican valor total ni entrada después del salto de precio.

Cash allocation, TRA, tax assets and dilution remain conditional. Dossier scenarios do not certify total value or an entry after the price jump.

## Reproducción

Ejecutar python reproduce.py: historia y perímetro desde hechos mínimos, modelo, puente, informe, resumen y QA. CSV históricos en USDmiles; modelo en USDmillones. Las diferencias de redondeo de1.000USD quedan identificadas; no se ocultan con ajustes inventados. Fuentes completas no se redistribuyen. Ninguna operación de cartera ha sido ejecutada.
'''
(p/'report.md').write_text(s)
