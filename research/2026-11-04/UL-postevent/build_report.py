from pathlib import Path
import json,html,re
P=Path(__file__).parent;R=json.loads((P/'model/results.json').read_text());E=json.loads((P/'inputs/event_inputs.json').read_text())
L=R['legacy'];C=R['cash_cost_capex_sensitivities'];M=R['margin_sensitivities'];rev=R['reverse_margin_diagnostic'];status=json.loads((P/'publication_state.json').read_text())
def f(v):return f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
body=f'''# Unilever: qué cambia después del Investor Event

**UL | Evento del 4 de noviembre de 2026 | Fuentes observadas el 5 de noviembre de 2026 hasta las 00:17 UTC; suplemento preparado posteriormente.**
**Estado: suplemento de evento condicionado. {status['audit_text']}** No es una nueva valoración integral, ni autorización de entrada. El expediente fundamental y la auditoría anteriores se conservan con su fecha y supuestos preevento.

## 1. Dictamen y precio actualizado

El evento da más detalle útil sobre la ejecución del negocio de hogar, belleza y cuidado personal. También hace explícitas necesidades de caja que deben conciliarse con el modelo anterior: capex del 3,6% en 2027–29, un agregado de 5.000 M€ de impuestos, reestructuración, separación y otros costes, y 1.200 M€ de reestructuración durante esos tres años. **No es correcto anunciar que el evento ratifica sin cambios el valor calculado antes de conocer esas cifras.** [1,2]

UL cerró el 4 de noviembre a **66,92 USD por ADR**, frente a 64,81 el día anterior: +{f(R['price_change']['return']*100)}%. Es cierre bursátil verificado, no precio ejecutable ni cotización en tiempo real. El avance de la cotización no demuestra por sí solo que haya aumentado el valor intrínseco. [4]

La lectura sigue siendo seguimiento condicionado, sin entrada aprobada. Las cifras antiguas de 67,26 sin operación Foods y 62,49 para el paquete económico con operación son referencias **preevento**. La auditoría había mostrado 66,52 y 61,67 al hacer converger gradualmente la reinversión al ROIC terminal. No presentamos ninguno de esos números como un nuevo objetivo vigente.

## 2. Qué evidencia se revisó

Se descargaron cinco presentaciones oficiales: CEO, CFO, marketing, Estados Unidos e India. Las páginas CFO 15, 22, 29, 33 y 41 se comprobaron visualmente, además de extraer el texto. La página oficial confirma que el evento ya se celebró y anunciaba la repetición próximamente al consultar. No puede certificarse la hora exacta en que se publicó cada archivo. [1,2,3]

Se leyó además la transcripción completa disponible en StockAnalysis/Quartr, incluidas preguntas y respuestas. Es una fuente de terceros, no cotejada con audio ni transcripción oficial. Para cifras y perímetros prevalecen las presentaciones oficiales. El índice SEC recuperado seguía mostrando como último 6-K el anuncio del 3 de noviembre; eso no descarta una presentación posterior. El enlace al comunicado del evento devolvió un error de acceso y no se afirma haberlo leído. [5,6,7]

Este evento no entrega nuevas cuentas trimestrales completas de beneficio, balance o caja. No se inventan datos Q3 de esas líneas, ni se vuelve a etiquetar una estimación semestral como un trimestre auditado. Los tres ejercicios, ingresos trimestrales y limitaciones de TTM del expediente anterior conservan sus cortes.

## 3. Cambios materiales de caja y perímetro

**Capex.** CFO página 22 muestra 3,6% para 2027–29, frente a 3,3% en 2024–26, y más del 50% de capex destinado a productividad. El pie identifica el perímetro HPC más India Foods, pro forma sobre información de 2025. No se aplica automáticamente al futuro Foods/McCormick ni a todo el antiguo grupo. El modelo llevaba 3,2% de capex más 0,8% de reposición de activos arrendados. Las fuentes revisadas no explican si el 3,6% incluye o excluye estos últimos. Comparar 3,6% con 3,2% sin resolverlo puede crear un gasto duplicado. [2, p22]

El cambio de gestión de 3,3% a 3,6% son 30 puntos básicos; la comparación con el input analítico de 3,2% son 40. Como simple escala, manteniendo las ventas HPC iniciales de 40.300 M€ y crecimiento del 5% del modelo anterior, cuatro décimas de ventas equivalen a unos 169, 178 y 187 M€ en tres periodos ilustrativos. Las etiquetas 2027–29 de esta escala no equivalen a previsiones de calendario o carve-out auditado. No son previsiones publicadas de capex ni un cálculo neto después de contratos de arrendamiento.

**Costes y reestructuración.** CFO página 33 asigna 5.000 M€ del efectivo Foods a impuestos, reestructuración, separación y otros costes. El modelo anterior reservaba 4.000 M€, incluidos 500 M€ de reestructuración extraordinaria. La nueva presentación también confirma 1.200 M€ de reestructuración 2027–29 y 500–600 M€ en 2027. No se ha publicado aquí una conciliación que permita sumar esas tres cifras. El nuevo agregado es la referencia primaria, pero su diferencia de 1.000 M€ respecto a la reserva analítica **no prueba un incremento neto de costes de igual importe**. [2, pp29,33,41]

La sensibilidad conserva la deducción recurrente anterior del 0,6% de ventas y los costes residuales HPC de 120/60 M€ en los dos primeros periodos. Su posible solapamiento con los 5.000 M€ sigue abierto. No se agregan 1.200 M€ ni 500–600 M€ otra vez. La transcripción de terceros menciona 400–500 M€ de costes varados iniciales y servicios transitorios de dos o tres años, lo que exige justificar la trayectoria de eliminación en vez de darla por hecha. [5]

**Inflación e inversión.** Para 2027 la compañía anticipa 550–750 M€ de impacto inflacionario en COGS, impuesto subyacente cercano al 26% y mejora modesta del margen. La inflación debe reflejarse junto con precios, mezcla y productividad; no se resta además íntegramente a un margen que ya recoge esos efectos. El impuesto del modelo resulta compatible con la guía. [2, p41]

## 4. Crecimiento, ventaja competitiva y margen

La dirección mantiene el algoritmo de 4–6% de crecimiento subyacente de ventas. La presentación muestra crecimiento de volumen superior al 2% y expansión modesta de margen para 2027. El anuncio del 3 de noviembre ya contenía la parte esencial del algoritmo y el programa de 1.000 M€ de ahorro hacia 2029. No se cuentan esos titulares como descubrimientos nuevos del evento. Tampoco se equipara crecimiento orgánico con crecimiento nominal en euros garantizado: divisas, cartera y adquisiciones alteran el puente. [2,6]

Las prioridades de marcas, distribución, investigación y productividad refuerzan la lógica comercial: concentrar inversión en categorías y mercados con capacidad de crecer, sostener el atractivo de las marcas y financiar inversión con eficiencia. La prueba económica sigue siendo crecimiento de volumen con margen y caja después de invertir. Prometer ahorro sin mantener publicidad, I+D y capex no demuestra una ventaja duradera.

El 19,1% de margen pro forma frente a pares cercanos al 22–23% es una comparación, no un compromiso de alcanzar esa banda en 2029. El modelo heredado parte de 19,4%; no se reetiqueta como exactamente el mismo perímetro/base temporal. En preguntas y respuestas, el CFO describe una trayectoria plurianual sin cierre de la brecha en cuatro, ocho o doce trimestres. El CEO apunta a diferencias estructurales en parte de la brecha. El múltiplo o margen de un competidor no se transfiere automáticamente a UL. [2, p15;5]

Por eso no elevamos el margen central ni añadimos 1.000 M€ de ahorro sobre un margen que ya presupone mejora. Las sensibilidades de margen de abajo son decisiones del analista para probar la importancia de ejecución y tiempo, no guía de la empresa.

## 5. Deuda, participaciones y asignación de capital

Los 15.700 MUSD, aproximadamente 14.000 M€, de efectivo Foods están sujetos a ajustes al cierre. De ellos, 6.000 M€ se destinan a deuda y el remanente, tras costes, a deuda o recompras. La compañía apunta a aproximadamente 1,8 veces deuda neta/EBITDA subyacente a fin de 2027 y a no refinanciar hasta 2028 dentro del plan actual. El coste financiero neto inferior al 3% de deuda neta media no es el coste marginal de deuda ni justifica sustituir el WACC del DCF por el 3%. [2, pp33,41]

No se suman como valor tres representaciones del mismo efectivo: ingreso de la operación, reducción de deuda y recompras. El paquete económico heredado cuenta una sola vez el 65% del combinado Foods/MKC que corresponde a titulares de UL: 55,1% distribuido directamente más 9,9% retenido. Es valor del conjunto recibido, **no precio futuro de UL una vez separada la distribución**. Tampoco se vuelve a añadir el 80,15% de Ice Cream ya distribuido en 2025.

La estimación de gestión de aproximadamente 6.000 M€ para las participaciones MICC, futura MKC y Pepsi Lipton no se añade al activo ya valorado ni al 65% Foods. Los dividendos de esas inversiones y su valor son dos formas de representar la misma propiedad; deben ser consistentes en un modelo de retorno. [2, p34]

La guía incluye compras pequeñas por unos 1.500 M€ anuales, recompra de 4.500 M€ durante 2027–29 y payout cercano al 60%. Un caso orgánico sin adquisiciones es legítimo como supuesto analítico, pero no representa toda la caja del plan de gestión. Si se añade crecimiento adquirido, habrá que pagar por él. Las recompras no se suman al valor de la empresa ni se convierten en crecimiento de BPA gratis. [2, p31]

También se plantea liberar 350 M€ de inventario en tres años. Es una liberación finita: no se perpetúa, ni se suma aquí al modelo antes de conciliar el capital circulante existente. La conversión de caja cercana al 100% no equivale automáticamente al FCFF disponible para el accionista. [2, p32]

## 6. Atribución numérica reproducible, no valoración actualizada

El cálculo independiente reproduce exactamente el modelo original y la corrección de reinversión auditada. Mantiene divisa EUR/USD 1,1179, 2,162429285 mil millones de acciones diluidas analíticas, deuda, pensiones, minoritarios, participaciones y escenario Foods previos. No se han actualizado esas magnitudes a un nuevo balance pro forma. La divisa congelada permite aislar cambios operativos, no afirmar que sea un fixing nuevo.

El punto de comparación es **{f(L['deal_fade'])} USD por ADR**, paquete preevento con transición de reinversión a ROIC terminal. Sustituir solamente la reserva de 4.000 por 5.000 M€ resta **{f(-C[3]['delta_vs_frozen_fade'])} USD/ADR**. Aplicar 3,6% más el 0,8% de leases durante tres periodos resta otros **{f(-C[1]['delta_vs_frozen_fade'])} USD/ADR**. Ambos cambios mecánicos producen {f(C[4]['mechanical_package_per_adr_usd'])}. Si 3,6% ya incluyese leases, el mismo ejercicio da {f(C[5]['mechanical_package_per_adr_usd'])}. **Estos resultados no son una banda de valor razonable, un suelo ni precios de compra.**

El modelo heredado combina un tramo de 0,67 años antes del cierre con diez años completos después. Sus tres primeros periodos postcierre no equivalen exactamente a los años naturales 2027–29. Se conservan para atribución comparable, no como implementación exacta del calendario de gestión. Después de tres periodos el ejercicio vuelve al capex anterior: no se inventa guía para 2030 en adelante. El agregado de costes podría solapar gastos retenidos, por lo que la aritmética no certifica una bajada neta de valoración.

La reinversión de años 6–10 converge hacia NOPAT × crecimiento / ROIC, con ROIC terminal del 19%, crecimiento terminal del 2,5% y WACC HPC del 7,5%. Se evita presentar todo el crecimiento tardío como gratis. No se cambia WACC para conseguir un precio atractivo.

## 7. Qué ejecución exige aproximadamente el precio

Con reserva de 5.000 M€, capex de 3,6% más leases en los tres periodos iniciales y todos los demás inputs congelados, elevar gradualmente el margen al 22%, 22,5% o 23% en el **año 10 del modelo** produce paquetes mecánicos de {f(M[1]['mechanical_package_per_adr_usd'])}, {f(M[3]['mechanical_package_per_adr_usd'])} y {f(M[5]['mechanical_package_per_adr_usd'])} USD. Alcanzarlos en el año 5 daría {f(M[0]['mechanical_package_per_adr_usd'])}, {f(M[2]['mechanical_package_per_adr_usd'])} y {f(M[4]['mechanical_package_per_adr_usd'])}. La diferencia muestra por qué no basta leer un margen lejano sin especificar cuándo y a qué coste llega.

En esa parametrización, 66,92 USD se iguala con un margen de aproximadamente **{f(rev['analyst_margin_endpoint_year10']*100)}% en el año 10**. No es “lo que el mercado exige” de forma única: otra trayectoria de ventas, divisa, WACC, ROIC, capital, precio de adquisición o costes cambiaría el resultado. La comparación tampoco demuestra que ese margen sea alcanzable ni asigna probabilidades. No se publica un retorno esperado nuevo apoyado en este ejercicio.

## 8. Qué falta para cerrar la actualización integral

1. Conciliar capex del 3,6% con reposición de leases, perímetro y años naturales 2027–29.
2. Distribuir los 5.000 M€ por concepto y fecha, cruzándolos con reestructuración recurrente, 1.200 M€, costes varados y pagos ya incluidos, sin doble conteo.
3. Incorporar carve-outs y documentación de cierre Foods/MKC cuando estén disponibles, deuda y ajustes efectivos, minoritarios, participaciones, número de acciones y posible nueva consolidación al cierre.
4. Construir un calendario único de FCFF, caja del accionista y distribuciones. El retorno preevento original de 8,14% no se reutiliza como cifra actual: la auditoría de fechas lo situaba en 7,67–7,83%, también con precio y supuestos antiguos.
5. Rehacer escenarios bajista, central y alcista, valoración inversa y comparables homogéneos después de esa conciliación. La sensibilidad de seis márgenes aquí no sustituye esos escenarios.
6. Actualizar por separado Stage 3.5: cotización, medias, estructura, liquidez, stop, riesgo y proximidad de resultados. No se usa RSI como veto automático ni se aplica un descuento universal del 15%.

El evento ya no debe aparecer como pendiente. Sí quedan pendientes los documentos definitivos y la conciliación financiera. La presentación sitúa S-4, regulación y voto de MKC en Q4 2026/Q1 2027, y cierre a mediados de 2027 como máximo, con intención de acelerarlo. Son ventanas y expectativas, no aprobaciones ya obtenidas ni fechas de resultados. Este suplemento no vuelve a certificar una próxima fecha de resultados. [2, p33]

**Conclusión:** el caso operativo gana detalle, pero el precio también ha subido y la caja exige más precisión. Conservamos el trabajo histórico como investigación fechada. Dejamos vacíos el valor integral vigente y el precio de entrada hasta terminar la conciliación; no se declara Stage 3/3.5 actual completo a partir de este suplemento.

## Fuentes y reproducibilidad

[1] [Página oficial del Investor Event](https://www.unilever.com/investors/unilever-investor-event-2026/).
[2] [CFO: Leading Performance](https://www.unilever.com/files/leading-performance-srinivas-phatak.pdf), especialmente páginas 15, 22, 29, 31–34 y 41.
[3] [CEO: HPC Pureplay](https://www.unilever.com/files/hpc-pureplay-fernando-fernandez.pdf).
[4] [UL: histórico de cotización](https://stockanalysis.com/stocks/ul/history/), cierre del 4 de noviembre.
[5] [Transcripción StockAnalysis/Quartr](https://stockanalysis.com/quote/lon/ULVR/transcripts/665870-cmd-2026/), fuente de terceros no cotejada con audio.
[6] [6-K del 3 de noviembre](https://www.sec.gov/Archives/edgar/data/217410/000165495426009451/a6665b.htm), noticia conocida antes del evento.
[7] [Índice de presentaciones SEC](https://data.sec.gov/submissions/CIK0000217410.json), consultado el 5 de noviembre.

El soporte conserva inputs numéricos, fuentes, cálculos, comprobaciones y este informe. Python 3 y su biblioteca estándar bastan para recalcularlo sin conexión. No redistribuye los PDF oficiales ni el texto íntegro de terceros. Las sensibilidades se distinguen de cualquier valor certificado mediante etiquetas y campos vacíos en el resumen de publicación.
'''
(P/'report.md').write_text(body)
# Minimal standalone HTML; source text preserved, no external scripts/fonts.
def inline(x):
 x=html.escape(x);x=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',x);x=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',x);return x
parts=[]
for para in body.split('\n\n'):
 if para.startswith('# '):parts.append('<h1>'+inline(para[2:])+'</h1>')
 elif para.startswith('## '):parts.append('<h2>'+inline(para[3:])+'</h2>')
 else:parts.append('<p>'+inline(para).replace('\n','<br>')+'</p>')
(P/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>UL · Investor Event 2026</title><style>body{font:17px/1.6 system-ui,sans-serif;max-width:940px;margin:45px auto;padding:0 24px;color:#182635;background:#fff}h1{font-size:2.1rem;line-height:1.15}h2{margin-top:2em;font-size:1.35rem;color:#174e68}a{color:#075a91}strong{font-weight:650}@media print{body{font-size:11pt;margin:0}h2{break-after:avoid}p{orphans:3;widows:3}}</style><main>'+''.join(parts)+'</main></html>')
print('report words',len(body.split()))
