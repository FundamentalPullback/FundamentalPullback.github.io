import json
from pathlib import Path
P=Path(__file__).parent;r=json.loads((P/'model/results.json').read_text());c=json.loads((P/'capital/verified.json').read_text());h=(P/'history/normalization_report.md').read_text();comp=json.loads((P/'comparables/results.json').read_text())
f=lambda x:f'{x:,.2f}'
s='''# TOST — actualización tras Q3: mejora operativa, financiación y valoración condicionadas

Corte: 4 noviembre 2026, después del cierre regular estadounidense. USD millones, salvo USD/acción y porcentajes. Investigación parcial revisada independientemente. No certifica valor total, Stage 3 completo, Stage 3.5 ni entrada.

## Conclusión

El negocio crece y mejora el beneficio operativo, pero el crecimiento del beneficio no se convierte proporcionalmente en caja del propietario. La financiación de Toast Capital y las comisiones diferidas son reinversión real. El litigio FTC y el capital plenamente diluido no están conciliados como obligaciones/acciones finales. Por ello los casos siguientes son cálculos condicionados, no un rango certificado del valor total.

El escáner recibido el 4 de noviembre registra 35,48, QP100, Opportunity90 y RSI68,6. No contiene EMA20/50 ni aprobación Stage2 verificable; su hora17:46:27 no identifica zona. El cierre regular independiente es35,35 a16:00EST, distinto de after-hours. El resultado Q3 se publicó3nov y el10-Q se presentó4nov: ya no es un evento futuro. La próxima fecha trimestral exacta no se ha confirmado en fuente primaria; no se libera esa puerta del plan. Fuente de precio: https://stockanalysis.com/stocks/tost/history/ ; calendario: https://investors.toasttab.com/events-and-presentations/events/default.aspx .

El valor histórico19,57 deA123 y sus casos7,59/40,23 se conservan como registro anterior. Sólo se ha recuperado su descripción, no sus archivos originales ejecutables. Este modelo es nuevo y no pretende reproducir exactamente el anterior ni atribuir la diferencia únicamente al resultado trimestral. Cambian fecha, capital, descuento y financiación explícita. No se sustituye ni reescribe ese historial.

## Tesis y riesgo verificables

Toast integra software de restaurante, cobros y servicios financieros; distribución y retención pueden sostener ventas cruzadas, pero la economía depende del margen después del coste de procesamiento, de hardware subvencionado, ventas y desarrollo. No es razonable valorar todos los dólares de ingresos como suscripción de alto margen. Q3ventas1981 y EBIT165 significan8,33% de margen sobre ventas; el26% comunicado utiliza otro denominador (beneficio bruto de suscripción y fintech), no ventas.

La demanda FTC presentada29oct contiene alegaciones de cargos no autorizados/ocultos, altas y cancelación; no es una sentencia ni demuestra por sí misma todos los hechos alegados. El10-Q dice que se solicitan medidas cautelares, compensación no cuantificada y sanciones, que Toast discrepa y que no puede estimar pérdida o rango. No se inventa cuantía. Los stress de100/300/600 son elecciones analíticas, no estimaciones legales ni probabilidades. Un coste recurrente de cumplimiento o cambio comercial puede ser más importante que una multa aislada. Fuentes: https://www.ftc.gov/legal-library/browse/cases-proceedings/252-3101-toast-inc ; https://www.ftc.gov/system/files/ftc_gov/pdf/Toast-Redacted-Complaint-Filed.pdf ; https://www.sec.gov/Archives/edgar/data/1650164/000165016426000216/tost-20260930.htm .

La sucesión de CFO es otro punto a vigilar: el8-K informa salida de Elena Gomez el31dic, asesoría hasta2jul2027 y nombramiento de Michael Senno desde1ene. No se interpreta como prueba de irregularidad ni se capitaliza su salario futuro como deuda adicional. Fuente: https://www.sec.gov/Archives/edgar/data/1650164/000165016426000214/tost-20261028.htm .

'''
s+=h.replace('# TOST: historia y calidad de beneficio/caja','## Historia y calidad del beneficio')
s+='''
## Ancla del modelo y capital

El ancla operativa es512 EBIT GAAP TTM −10 devolución arancelaria Q2 +6 amortización adquirida expresamente incluida en coste de ventas =508. Los6 son5 FY25 +4 nueve meses2026 −3 nueve meses2025. No se presume haber aislado toda amortización de clientes en otras líneas: lo no identificado queda como gasto. Se mantienen SBC, desarrollo, alquileres y reestructuración. El impuesto normalizado25% grava beneficio antes de esa amortización adquirida; no se crea escudo fiscal ficticio por ella. La devolución10 aparece en el10-Q Q2 y comunicado: https://www.sec.gov/Archives/edgar/data/1650164/000165016426000164/tost-20260630.htm ; https://www.sec.gov/Archives/edgar/data/1650164/000165016426000162/tost-20260630xexhibit991.htm .

Caja corporativa1203 + valores682 =1885; se excluyen76 restringidos y154 de clientes con pasivo equivalente. Se reserva500 de operación (elección, no obligación contractual),13 por warrant a valor contable y7 como reserva fiscal histórica seleccionada. Puente seleccionado1365. El saldo fiscal7 es UTB bruto de diciembre2025, no deuda corriente exacta; puede afectar atributos fiscales y no sólo efectivo. No se suma como activo el préstamo70 ni comisiones294: sostienen el negocio modelado. No hay deuda financiera dispuesta publicada en septiembre. Mantener alquileres en EBIT implica no restar nuevamente deuda de alquiler.

El programa bancario tiene provisión contingente60 y obligación stand-ready24; no se descuentan mecánicamente ambos además de márgenes con costes crediticios y colateral restringido excluido. Falta una conciliación de pagos de obligaciones heredadas frente al gasto futuro; un stress de salida adicional84, sin duplicar costes ya financiados, equivale a0,14 por acción. No equivale a afirmar que todos84 estén fuera de los flujos. Compromisos hardware191 y nube/otros95 son costes/reinversión ordinarios del negocio; no se restan íntegros como deuda además del forecast.

El10-Q presenta519M A +62M B al30oct=581M básicas. Para los casos se suman14M RSU esperadas y19M opciones esperadas netas por treasury-stock al ejercicio medio13,98 y precio35,35: proxy606,486M. No es valoración de la opcionalidad temporal ni capital plenamente diluido actual. Se prueba595/606,486/614M. Los13 del warrant ya se deducen, por lo que no se añade otra vez su1M de acciones. Los premios existentes y el gasto futuro de SBC no son lo mismo: se conservan ambos efectos sin restar de nuevo todo el SBC histórico al DCF. Las recompras486 ya redujeron caja y acciones; los100 aún autorizados no son recompras ejecutadas.

El10-K25 documenta NOL federal928 y estatal873, créditos96 y restricciones/vencimientos. No se agrega su valor como si estuviera disponible íntegro ni se extiende la tasa efectiva4,3% para siempre. Se muestra sólo un techo aritmético histórico sin descuento de335,53 (928×21% +873×5% +96), sin certificación de uso/fecha/impuesto estatal; no es activo tasado y puede solaparse con otras reservas. Fuente: https://www.sec.gov/Archives/edgar/data/1650164/000165016426000057/tost-20251231.htm .

## Diez años y financiación

Los períodos son años móviles desde4nov2026, no ejercicios fiscales2027 certificados. Primer flujo al cabo de un año; el TTMseptiembre es el ancla histórica. No se omite un stub fiscal para llamarlo conservador. No se financian adquisiciones gratuitas.

Los escenarios adverso/base/favorable usan crecimientos primeros5años de12/10/8/6/5%,20/18/16/14/12% y24/22/20/18/16%. Márgenes correspondientes6,5/7/7,5/8/8%,8,5/9,5/10,5/11,5/12,5% y9,5/11,5/13,5/15,5/17%, sobre ingresos, después de SBC y costes operativos pero antes de la amortización adquirida identificada. No son guía del emisor. Años6–10 crecimiento converge linealmente a2,5/3/3%; margen se mantiene. ROICincremental15/20/25%, descuento14,5/12,5/10,5%, impuesto25%.

D&A físico/software residual seleccionado0,65% de ventas y capex de caja1%; el saldo software2026 no está totalmente desglosado. Se añade reinversión no monetaria de SBC capitalizada0,17% de ventas como coste de propiedad, basada sólo en la brecha inferida, no cantidad certificada de software. Comisiones netas iniciales1,6/1,2/1% y préstamos netos2/1,4/1% de ventas durante5años. No se suma una segunda vez la comisión bruta encima del neto. Circulante ordinario10% del incremento de ventas, excluyendo esos dos activos.

Desdeaño6 la nueva financiación de préstamos/comisiones mezcla el ratio inicial con el crecimiento de su saldo previo, hasta que año10 sólo aumenta el saldo al ritmo de ventas. Se evita perpetuar indefinidamente originación neta como porcentaje de ventas sin balance coherente. La financiación neta se agrega a los saldos70/294 de partida; no prueba que todos los préstamos cobrados/impagados sigan ese patrón. Márgenes incluyen pérdidas crediticias recurrentes; no se asume crédito sin riesgo. Los saldos terminales y la financiación anual son visibles enmodelo.

La reinversión de cada año es el máximo entre: capex−D&A +SBCcapitalizada +comisionesnetas +préstamosnetos +circulante, y aumento positivo de NOPAT/ROIC. No se libera caja cuando cae NOPAT por definición del segundo suelo. Esta regla financia también la mejora de margen; puede ser exigente para software de alto retorno y por eso se compara con una alternativa de eficiencia explícita. En terminal se mantiene el máximo físico (incluidos préstamos/comisiones a crecimiento estable) y NOPAT×g/ROIC; no se borra la reinversión para inflar perpetuidad.

Referencia de descuento: Treasury10años4,90% del4nov, ERP4,41% de noviembre y beta5años1,71 dan coste de capital propio12,4411%; deuda dispuesta0. Se selecciona12,5%, no WACC auditado del emisor. Beta histórica, combinación de ERP y tasa diaria, costes legales y riesgos de cartera siguen inciertos. Fuentes: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve ; https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm ; https://stockanalysis.com/stocks/tost/statistics/ .

| Caso condicionado | EV | Puente | Residuo/acción | PVterminal/EV | Primer FCFF |
|---|---:|---:|---:|---:|---:|
'''
for n,o in r['cases'].items():s+=f"|{n}|{f(o['enterpriseValue'])}|{f(o['bridge'])}|{f(o['conditionalResidualPerShare'])}|{f(o['terminalPvFraction']*100)}%|{f(o['rows'][0]['fcff'])}|\n"
s+='\nLos déficit de los primeros años consumen caja: déficits acumulados máximos aproximados43/527/939 en adverso/base/favorable. El puente líquido seleccionado1365 los cubre aritméticamente, después de apartar500 operativos. Se usan esos excedentes, no se vuelve a sumar la reserva operativa. Los flujos negativos ya reducen EV, por lo que deducir además su total del puente duplicaría el coste. Esta cobertura no certifica financiación disponible frente a pérdidas legales, restricciones o nuevos usos; stress600 deja785 y no cubre el déficit acumulado favorable939. La fuerte dependencia del terminal obliga a mantener la clasificación condicionada.\n\n### Tabla anual del caso base\n\n| Año móvil | Ventas | EBIT antes amortización identificada | NOPAT | Reinversión total | FCFF |\n|---|---:|---:|---:|---:|---:|\n'
for q in r['cases']['base']['rows']:s+=f"|{q['year']}|{f(q['revenue'])}|{f(q['ebit'])}|{f(q['nopat'])}|{f(q['reinvestment'])}|{f(q['fcff'])}|\n"
a=r['inverseFinanced'];b=r['inverseEfficiencyOnly']
s+=f'''\n## Inverso y sensibilidad\n\nCon precio35,35, manteniendo crecimiento y financiando toda mejora de NOPAT aROIC20%, la raíz exige añadir{f(a['marginShiftPp'])} puntos de margen: terminal{f(a['terminalMargin']*100)}%, ventas año10 {f(a['year10Revenue'])} y primer FCFF{f(a['firstYearFcff'])}. Esta necesidad de financiación no está cubierta por la reserva500 ni por caja total; **no es un escenario de compra factible certificado**. Expone lo extremo de esa combinación de retorno/capital, no predice una emisión concreta. El inverso alternativo atribuye la mejora de margen a eficiencia sin inversión incremental adicional y requiere{f(b['marginShiftPp'])} puntos, margen terminal{f(b['terminalMargin']*100)}%; es una hipótesis diferente y no un objetivo garantizado. Ambas raíces verifican bracket, residual y1000 intervalos de monotonía sobre el bracket completo; esto comprueba unicidad en ese dominio, no fuera de él.\n\n'''
for k,vs in r['sensitivities'].items():
 if isinstance(vs,list):s+='- '+k+': '+ '; '.join(f"{q['input']:g} → {f(q['value'])}" for q in vs)+'.\n'
s+=f"- Margen recurrente −100pb: {f(r['sensitivities']['legalMarginMinus100bp'])}; stress legal, no probabilidad.\n- Techo aritmético NOL histórico sin descuento: {f(r['sensitivities']['historicalNolUpperBound']['value'])}; no valor reconocido del activo.\n"
s+='''
## Contraste relativo limitado

SHOP es sólo un contraste de plataforma de comercio/pagos, no un comparable homogéneo de restaurante ni una segunda valoración. Ambos terminanTTMseptiembre y mantienenSBC enEBIT. TOST35,35×581−1885 produce EVindicativo18653,35;36,43×EBITGAAP512 o37,16×EBITsinrefund502. SHOP153,07×1286,382910−5251 produceEV191655,63 y92,63×EBIT2069. Las acciones/caja están fechadas; el múltiplo usa caja total por convención, distinto del puente deDCF que reservaoperación. SHOP tiene inversiones estratégicas/equity-method no valoradas en este cálculo, sin afirmar que valgan cero. No se aplica mediana a TOST ni se certifica que sea barato por tener menor múltiplo.

SHOP presentaCFO2682,capex21,préstamosnetos789,intangibles99 ySBC515: caja después de esos usos1258, aún noFCFF maduro. Su cambio de presentaciónMCA67 y perímetro impiden comparación perfecta con300 deTOST. Falta una cesta homogénea y conciliación plena de capital; el contraste no cierra Stage3 integral. Fuentes: https://www.sec.gov/Archives/edgar/data/1594805/000159480526000068/shop-20260930.htm ; https://stockanalysis.com/stocks/shop/history/ .

## Qué probaría o deterioraría la tesis

Confirmación: que crecimiento y margen trasSBC se mantengan mientras caja después de préstamos/comisiones acompaña; evolución de inventario sin pérdidas; detalle software y dilución; resolución documentada de riesgos comerciales/legales; calendario primario y filtro técnico actualizado. No basta que el beneficio neto suba por liberar valoración fiscal.

Deterioro: crecimiento sostenido de financiación y pérdidas de crédito por encima de margen; mayor coste de adquisición de clientes; mayor subsidio hardware; remediosFTC que afecten precios/retención; dilución que compense recompras; nuevos requerimientos de caja o margen estructural menor. No hay probabilidad asignada ni recomendación de operación.

## Resumen publicable ES/EN

TOST mejora su EBIT TTM de239 a512; descontando la devolución arancelaria,≈502. Mantiene crecimiento operativo, pero el cash flow exige financiar préstamos y comisiones.

TOST increases trailing operating profit from239 to512; excluding the tariff refund gives about502. Operating growth is real, but loans and deferred commissions require funding.

El FCF publicado604 baja a300 después de financiación de préstamos y SBCpatrimonio, frente306 previo. Esta sensibilidad no es FCFF: quedan impuestos, capital y contingencias por conciliar.

Reported free cash flow of604 falls to300 after loan funding and equity-recognized SBC, versus306 previously. This sensitivity is not FCFF; taxes, capital and contingencies remain unresolved.

La demanda FTC está pendiente y sin pérdida estimable. Los casos deDCF son condicionados; no certifican valor total, calendario ni entrada.

The FTC lawsuit is pending and its loss range cannot be estimated. DCF cases remain conditional and do not certify total value, an earnings-calendar gate or an entry.

## Reproducción y límites

Los scripts usan Python estándar sin red y sólo hechos mínimos derivados; las fuentes se enlazan, no se distribuyen sus documentos íntegros. Ejecutar reproduce.py. El histórico es trazable pero no una auditoría del emisor. Ausencia de fecha futura confirmada, conciliación completa de software/capital/pasivos legales y comparables homogéneos mantiene todos los valores totales ennull. No hay entrada ni alteración de cartera.
'''
(P/'report.md').write_text(s)
