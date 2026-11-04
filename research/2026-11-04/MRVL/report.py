import json,pathlib
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());h=a['history'];rows=[]
for k in ['FY2024','FY2025','FY2026','Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027','prior_TTM','TTM']:
 r=h[k]; rows.append('| '+' | '.join([k]+[f'{r[x]:,.1f}' for x in ['revenue','gaap_ebit','net_income_parent','cfo','da_total','sbc','capex_ppe','technology_license_purchases','technology_license_obligation_payments']])+' |')
s='''# MRVL — la historia autónoma no es el combinado anunciado

Corte: 4 de noviembre de 2026, 19:02 UTC. Precio de referencia: cierre del 3 de noviembre, 171,97 USD. Se preserva el escáner histórico del 28 de octubre a 229,85 USD, QP 80 y Opportunity 95; esa observación no se presenta como cierre oficial. A112 solo contenía triage. No se reconstruye un DCF inexistente ni se publica una nueva sesión de escáner.

**Investigación parcial auditada independientemente; sin certificación integral. Valor central, rango, owner FCF certificado y valoración combinada: nulos, no cero. No hay entrada aprobada ni cierre integral Stage 3/Stage 3.5.** No se cambian cartera ni operaciones.

## 1. Resultado útil y evidencia destacada

Los ingresos TTM alcanzan 9.450,3 millones USD, un 30,62 % más, y el EBIT GAAP sube de 93,1 a 1.561,3 millones.

Data center aporta 2.171,5 millones USD en Q2, frente a 1.490,5 millones un año antes, y representa aproximadamente el 79 % del trimestre.

La estimación preliminar Q3 mantiene el punto medio de 3.150 millones USD y estrecha el intervalo a 3.087–3.213 millones; no son estados completos publicados.

El beneficio neto TTM incluye una ganancia de 1.830,4 millones USD por la venta de automoción, fuera del EBIT; no es rentabilidad operativa recurrente.

La combinación con Lumentum no está cerrada: el canje fijo es de 4,5 acciones MRVL por acción LITE y el cierre se espera en el primer semestre de 2028, sujeto a condiciones.

El flujo TTM después de PPE, pagos de tecnología y SBC es una aproximación de 763,3 millones USD, no owner FCF certificado ni caja del futuro combinado.

El avance operativo es real, pero coexisten adquisiciones ya cerradas, contraprestación contingente, preferentes y una transacción transformadora todavía pendiente. Un precio menor tras un anuncio no acredita por sí mismo descuento sobre valor intrínseco. Este expediente separa esos perímetros y evita sumar sinergias a una compañía que todavía no existe jurídicamente como grupo combinado.

## 2. Historia reproducible

Millones USD. FY2024 terminó el 3 de febrero de 2024, FY2025 el 1 de febrero de 2025 y FY2026 el 31 de enero de 2026. Último período completo: Q2FY2027, terminado el 1 de agosto de 2026. El preliminar Q3 no se añade al TTM.

| Período | Ingresos | EBIT GAAP | NI matriz | CFO | D&A total | SBC | PPE | Licencias inversión | Principal licencias |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(rows)+'''

TTM se reconstruye mediante FY2026 + H1FY2027 − H1FY2026; el comparable usa la misma ventana desplazada un año. El margen EBIT pasa del 1,29 % al 16,52 %. El crecimiento porcentual del EBIT parte de una base mínima; su expansión absoluta es más informativa que extrapolar el porcentaje. CFO crece un 19,27 %, menos que los ingresos.

D&A total incluye depreciación/amortización ordinaria y amortización de intangibles adquiridos: TTM 368,8 + 892,7 = 1.261,5. No se suma otra vez la amortización adquirida. Mantener SBC como coste económico impide convertir remuneración en acciones en caja gratis.

EPS diluido por trimestre Q3FY2026/Q4FY2026/Q1FY2027/Q2FY2027 es 2,20/0,46/0,04/0,33; suma analítica 3,03, no un EPS anual nuevo certificado. La preferente introduce método de dos clases. El beneficio de ordinarias reconstruido con anual/YTD es 2.633,4 millones; sumando asignaciones trimestrales es 2.631,3. La diferencia de 2,1 refleja el recálculo por período y no se oculta. El NI de matriz 2.639,9 sí es aditivo. No se valora el negocio mediante un PER contaminado por desinversiones.

## 3. Normalización y perímetro

La venta del negocio automotive ethernet aporta 1.830,4 millones de ganancia antes de impuestos al TTM, por debajo del EBIT. No debe sumarse o restarse de EBIT para normalizarlo. Los flujos de venta son inversión, no ventas recurrentes; tampoco se revierten una segunda vez dentro del CFO. La historia conserva el negocio vendido durante el tiempo que estuvo consolidado: no es crecimiento orgánico comparable puro.

Celestial AI se consolidó desde el 2 de febrero y XConn desde el 10 de febrero de 2026. Celestial tiene contraprestación inicial estimada de 3.533,7 millones, incluidos 1.276,0 en efectivo, 1.929,0 en acciones, 12,9 de premios por servicio anterior a la combinación y 315,8 de contingente inicial; la asignación de compra es preliminar. Costes de integración, I+D y amortización no desaparecen porque se presenten métricas ajustadas.

H1 contiene 433,7 millones de gasto por revalorizar contraprestación contingente y 131,0 de ganancia no realizada por un forward sobre la acción, neto 302,7 de gasto. Ambas partidas afectan otros resultados, no EBIT, y se revierten en la conciliación del CFO. La subida de una obligación ligada a hitos no es una nueva salida de caja inmediata, pero tampoco un coste económico que se pueda borrar sin tratar la liquidación futura.

El negocio ofrece ASIC personalizados, interconexión óptica y eléctrica, switching y otras soluciones de infraestructura. Diseño, propiedad intelectual e integración con clientes pueden favorecer permanencia de programas; no se certifica una barrera competitiva duradera por crecimiento de AI solamente. R&D H1 de 1.393,4 millones es una inversión económica necesaria, aunque se contabilice como gasto. No se capitaliza selectivamente para inflar EBIT.

## 4. Caja, licencias y reinversión

CFO TTM 2.200,3 − PPE 470,2 = 1.730,1. Restar compras de licencias 7,3 y pagos de principal de licencias 130,6 deja 1.592,2. Después del coste accionarial SBC 828,9 queda 763,3, frente a 786,0 en la ventana previa. Esta aproximación no es FCFF: contiene intereses e impuestos del período, pagos de inversión previamente financiada y capital circulante de un perímetro cambiante. Tampoco sustituye un análisis de reinversión futura o del coste de adquisiciones.

Los pagos de principal de licencias aparecen en financiación, no dentro de PPE. Ignorarlos haría parecer gratuito el acceso tecnológico. A la vez, un DCF que financiara nuevas licencias mediante capex económico y descontara sus obligaciones existentes debería evitar cargar dos veces los mismos pagos futuros. Este expediente no intenta resolverlo con una resta arbitraria de balance.

La caja aumenta de 2.638,8 a 3.932,8 millones durante H1, pero entran 2.000 millones por emisión de preferentes y aproximadamente 499 millones netos de nueva financiación antes de otros costes. El aumento no se atribuye íntegramente a generación operativa. H1 consume 1.270,9 millones de adquisiciones netas, además de recompras, dividendos y retenciones de acciones. No se proyecta la expansión como autofinanciada sin revisar esos movimientos.

## 5. Capital autónomo al 1 de agosto, no balance pro forma de noviembre

Deuda nominal 4.999,9 frente a deuda contable 4.962,9; la diferencia de 37,0 son costes/descuentos no amortizados. Restar caja da 1.067,1 de deuda neta simple, pero no un puente de valor completo. Hay obligaciones de licencias 220,0, arrendamientos 323,2, contingente Celestial 749,5, impuestos corrientes 163,7/no corrientes 85,7 y reestructuración 238,4. Los compromisos tecnológicos incluyen importes ya registrados: no se suman todos a deuda.

La contingente podría liquidarse hasta aproximadamente 233 millones de efectivo y 22,4 millones de acciones; el valor contable 749,5 es una medición de valor razonable a agosto, no el máximo contractual. El forward de 300 millones nocionales tiene activo de valor razonable 131,0 y vencimiento de doce meses desde abril. No se suma nocional como caja ni se presume que cubra toda la exposición. Si se tratara contraprestación en el puente, no se podría deducir todo su valor y contar simultáneamente las mismas acciones como dilución sin reconciliar el método.

NVIDIA aportó 2.000 millones por Series A el 31 de marzo. La conversión inicial equivale aproximadamente a 21,8 millones de acciones ordinarias; participa en dividendos y liquidación como convertida y no tiene derecho de rescate. No se trata automáticamente como deuda de 2.000 millones además de contar su dilución. Tampoco se suman esas acciones de nuevo al promedio diluido que ya asuma conversión. Derechos, futuros premios y acciones contingentes exigen un denominador coherente, no la lectura aislada de la carátula.

Las reservas de capacidad no corrientes prepagadas ascienden a 487,0 millones. Compromisos incondicionales con foundries/test/ensamblaje suman 8.518,9; servicios/licencias, 666,3; capex contratado, 351,6. Son necesidades y contratos futuros, no automáticamente deuda adicional del mismo importe. Deben entrar en escenarios operativos y de reinversión antes de decidir qué caja es excedentaria. No se certifican caja mínima, impuestos de repatriación, pensiones ni capital actual completo mediante este balance histórico.

## 6. Lumentum: términos, no sinergias realizadas

El acuerdo anunciado el 2 de noviembre prevé canje fijo de 4,500 acciones MRVL por LITE. La propiedad anunciada es aproximadamente 67 % para accionistas MRVL y 33 % para LITE, totalmente diluida. No se deriva un número exacto de acciones de porcentajes redondeados. La cifra de 115.000 millones de enterprise value de LITE utiliza precios de referencia del 28 de octubre y no es valoración propia ni obligación de pagar ese efectivo.

Al cierre de referencia MRVL de 171,97, la fórmula de canje equivale a 773,865 USD de acciones MRVL por ordinaria LITE. Es una operación aritmética fechada, no precio objetivo, valor garantizado, spread realizable ni rentabilidad de arbitraje. Sin precio LITE sincronizado y capital reconciliado no se calcula spread. El canje fijo transmite las variaciones de MRVL al valor recibido.

La dirección espera cerrar en el primer semestre de 2028, sujeto a votos de ambas compañías, autorizaciones regulatorias y otras condiciones. Más de 1.000 millones anuales de sinergias de costes y aumento de EPS no GAAP en el primer año son objetivos, no ahorro obtenido. Una valoración combinada necesitaría probabilidades justificadas, costes de integración, impuestos, plazo de realización, financiación, dilución y escenarios si la operación no cierra.

El 8-K contempla tratamiento de preferentes LITE mediante conversión o elección de Series B MRVL con derechos equivalentes ajustados. Las condiciones y fechas externas se detallan en merger/terms_note.md: fecha inicial 1 de noviembre de 2027 con extensiones regulatorias previstas hasta agosto de 2028. Hay pagos de terminación condicionados de 5.800 millones para MRVL, 2.900 para LITE y un pago regulatorio MRVL de 3.200 en circunstancias específicas. No son deuda devengada hoy ni se suman como obligación cierta; tampoco se ignora su posible consecuencia.

La presentación ilustra ingresos anualizados de trimestre de 12.600/5.100/17.700 millones para MRVL/LITE/combinado. Mezcla guía MRVL con trimestre LITE y no representa ingresos combinados reportados. No se incorpora esa cifra al TTM ni se capitalizan sinergias como si ambas entidades ya estuvieran consolidadas. El anuncio tampoco certifica la totalidad de jurisdicciones regulatorias; los anexos públicos no sustituyen las futuras resoluciones.

## 7. Comparables y riesgos de concentración

Como contraste operativo, Broadcom Q3FY2026 terminado el 2 de agosto publica ingresos de 29.591 millones, EBIT GAAP 15.955 y margen 53,92 %. CFO 14.197 menos PPE 532 da FCF publicado 13.665; SBC del trimestre es 2.019. Su software de infraestructura aporta 8.752 millones de ventas y altera sustancialmente la mezcla. No se impone ese margen a Marvell ni se compara con margen ajustado de otra empresa.

Lumentum Q1FY2027, terminado el 26 de septiembre y publicado el 2 de noviembre, aporta contexto autónomo del objetivo: ingresos 1.262,6 millones, EBIT GAAP 359,8, CFO 267,7 y PPE 229,8, dejando 37,9 por resta simple. SBC 132,5 incluye modificación de premios por 89,4; el ajuste de 146,7 de su release incluye además impuestos laborales. No se anualiza este trimestre ni se usa para certificar precio de compra o combinado. El capex absorbió gran parte de la caja operativa.

Marvell Q2 presenta EBIT GAAP 459,7 sobre 2.739,3 de ventas, margen 16,78 %. La diferencia con Broadcom no demuestra un valor objetivo: mezcla, escala, amortización, costes de desarrollo y activos difieren. No se entrega múltiplo relativo homogéneo ni descuento por pares certificado. Lumentum es objeto de adquisición pendiente, no un comparable independiente usado para justificar el precio pagado.

Un cliente directo aporta 16 % de ingresos H1 y un distribuidor 45 %; ese distribuidor sirve a diversos clientes finales, por lo que no se confunde cuota de distribuidor con un único comprador final. Cuatro clientes representan 72 % de cuentas a cobrar brutas. El 43 % de ventas H1 se envía a China, dato de destino de envío, no demanda final equivalente. TSMC es la única foundry para nodos avanzados. Exportaciones, suministro, capacidad, competencia y negociación de grandes clientes siguen siendo riesgos concretos; no se declara cierre normativo ni pérdida cero.

## 8. Calendario y decisión

Q2 completo se publicó el 27 de agosto y el 10-Q el 28. El 2 de noviembre se comunicó solo una estimación preliminar de ingresos Q3, todavía sujeta a cierre contable y revisión. El calendario oficial consultado no muestra una próxima fecha confirmada de resultados. No se sustituye con estimaciones de proveedores ni con el anuncio del año pasado.

Mantener seguimiento, sin valoración certificada y sin entrada. Para cerrar: estados Q3 completos; puentes comparables ex-automoción y adquisiciones; capital/contingentes/preferentes actualizado; reinversión económica de licencias y capacidad; pro forma y S-4 de Lumentum; condiciones regulatorias y fechas de votos. El escenario autónomo y el combinado deben mantenerse separados. No se usa el score histórico como permiso para ejecutar ni se elimina el filtro de calendario.

## 9. Fuentes y reproducción

- [10-Q MRVL agosto](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000025/mrvl-20260801.htm): estados, notas 3–11, concentración y factores de riesgo.
- [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm); history/numeric_facts.json identifica fuentes, fechas y magnitudes intermedias.
- [Anuncio MRVL/LITE](https://investor.marvell.com/news-events/press-releases/detail/1040/marvell-and-lumentum-to-combine-creating-a-category-leader-in-ai-connectivity).
- [8-K acuerdo](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001193125-26-442717/d352474d8k.htm) y [contrato público](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001193125-26-442717/d352474dex21.htm). Ver nota acotada de términos, no asesoramiento jurídico.
- [Presentación de combinación](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001193125-26-442714/d81187dex992.htm).
- [Calendario IR](https://investor.marvell.com/news-events/ir-calendar).
- [Cierre histórico MRVL](https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=MRVL%3ANSQ).
- [Lumentum Q1FY2027 10-Q](https://www.sec.gov/Archives/edgar/data/1633978/000162828026069615/lite-20260926.htm).
- [Broadcom Q3FY2026](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial).

El paquete ofrece datos numéricos y scripts offline; no redistribuye filings completos. Reproducir las cifras no convierte las incógnitas de capital, calendario o valor en hechos conocidos.
'''
(P/'report.md').write_text(s)
