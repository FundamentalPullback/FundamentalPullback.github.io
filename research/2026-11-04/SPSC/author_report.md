# SPSC · Stage 3 completo de investigación · Esperar precio

Fecha del análisis: 4 de noviembre de 2026. Corte fundamental: 10-Q del 30 de septiembre publicado el 29 de octubre; guía de la misma fecha. Moneda: USD; tablas financieras en millones salvo BPA y múltiplos. NASDAQ:SPSC es la acción ordinaria estadounidense, no un ADR. Investigación propia.

## Conclusión

La valoración propia arroja 33,64 / 52,89 / 84,61 USD por acción en escenarios adverso, central y favorable. El cierre de 85,25 USD supera el central en 61,2% y se sitúa prácticamente en el favorable. No son objetivos garantizados ni precios de compra: la decisión es esperar precio o nueva evidencia. No hay entrada aprobada.

El negocio sí mejora. La desaceleración comercial, el efecto temporal del circulante y el precio impiden confundir la recuperación de márgenes con una oportunidad barata. Se completa la investigación fundamental, no Stage 3.5: sin techo de entrada, stop, cantidad ni orden. La diferencia frente al antiguo central exploratorio de 49,73 USD no es una rentabilidad realizada ni una actualización mecánica: aquí se reconstruye un modelo propio con perímetro, impuestos y reinversión explícitos.

Precio del escáner: 85,25 USD, archivo del 3 de noviembre a las 17:27:04, zona horaria no documentada. Se mantiene separado del cierre regular de 85,25 USD del 3 de noviembre, 16:00 Eastern, contrastado en [historial de precios](https://stockanalysis.com/stocks/spsc/history/). La coincidencia de cifras no certifica que el CSV fuera un cierre. No usamos la sesión abierta del 4 de noviembre.

## Puente con el expediente anterior A119

A119 ya incorporaba el comunicado Q3 del 29 de octubre. No atribuimos a nuevas noticias la diferencia entre 49,73 y 52,89 USD. Se reconstruyen sus hipótesis publicadas y se obtiene 49,7264 USD, que redondea exactamente al valor previo. Ambos cálculos usan la misma información Q3; a igual cierre de 3 de noviembre el valor antiguo no cambia porque su tasa era una hipótesis fija, no una función de la cotización. Se conserva el informe anterior como historia, no se reescribe su decisión.

| Paso secuencial | Valor USD | Motivo |
|---|---:|---|
| A119 reproducido | 49,73 | FCFF anterior, mismos datos Q3 |
| Acciones 36,6 → 36,209 M | 50,26 | Promedio diluido Q3 identificado, en vez de guía anual |
| Nuevas tasas iniciales de crecimiento | 48,68 | Hipótesis más moderadas, no dato reportado nuevo |
| Base operativa y trayectoria de margen nuevas | 57,09 | EBIT antes de amortización adquirida, SBC conservada, margen terminal23%; cambio de normalización/hipótesis |
| ROIC terminal 25% → 20% | 56,20 | Menor eficiencia de reinversión terminal asumida |
| Reinversión detallada y transición nuevas | 52,89 | Financia crecimiento con capex/circulante y retorno incremental explícitos |

El paso de margen es un diagnóstico intermedio: no debe usarse como valoración por separado antes de completar la reinversión. El puente depende del orden de cambios y no asigna causalidad económica única. WACC10%, impuesto25%, caja excedentaria133,501M y ventas de referencia787,9M no cambian. La normalización de amortización/tecnología y el coste de reinvertir explican la mayor parte de la revisión; más detalle no prueba que la compañía valga más. El script migration_bridge.py preserva y reproduce este contraste, y el análisis de calendario/perímetro ofrece sensibilidades adicionales.

## Negocio, calidad y causa de revisión

SPS conecta proveedores y comercios mediante intercambio de datos, cumplimiento y automatización de operaciones. La integración en procesos del cliente y la red favorecen recurrencia, pero no prueban una ventaja inexpugnable. Hay exposición a gasto comercial, transacciones, plataformas de terceros, ciberseguridad, adopción de IA y ejecución de integraciones. La documentación de riesgos y las políticas de software figuran en el [10-K de 2025](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000012/spsc-20251231.htm). La caída respecto de cotizaciones históricas no se atribuye aquí a una sola noticia: la menor expansión de ingresos y la complejidad de Carbon6 son hechos; no tenemos una descomposición causal del movimiento bursátil.

El EBIT de Q3 sube de 31,191 a 39,929 M$, un 28,0%, y el margen GAAP pasa de 16,42% a 20,20%. La mejora conserva la SBC como gasto; no depende exclusivamente de recompras. El beneficio neto aumenta 20,0%, mientras el BPA crece 26,9% por la reducción adicional de acciones diluidas.

La facturación recurrente de Q3 crece 4%, pero la comparación incluye un perímetro distinto. La venta 3P elimina aproximadamente 8.050 clientes; el ARPU sube 22% en parte por esa mezcla. No interpretamos la caída de clientes del 15% como churn comparable ni el ARPU como subida pura de precios.

Datos y definición de clientes: [10-Q Q3](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000075/spsc-20260930.htm). Los ingresos recurrentes son 188,980 de 197,647 M$ en Q3, 95,6%. La proporción es favorable, pero revenue recovery depende también de resultados y del take rate. No equivale a una suscripción contractual enteramente fija. La rentabilidad de Q3 no se extrapola sola a cuatro trimestres.

## Tres ejercicios, cuatro trimestres y TTM comparable

Las columnas usan los identificadores reproducibles del archivo history.csv. EBIT y beneficio neto son GAAP. El indicador fcf_after_sbc_diagnostic = CFO menos inversión en PPE/software menos SBC; no es FCFF normalizado. Fuente: 10-K [2025](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000012/spsc-20251231.htm), [2024](https://www.sec.gov/Archives/edgar/data/1092699/000109269925000011/spsc-20241231.htm), 10-Q [Q3 2026](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000075/spsc-20260930.htm) y [Q3 2025](https://www.sec.gov/Archives/edgar/data/1092699/000109269925000064/spsc-20250930.htm), con etiquetas XBRL archivadas en la hoja de trazabilidad.

| Periodo | revenue | ebit | net_income | cfo | ppe_capex | sbc | fcf_after_sbc_diagnostic |
|---|---|---|---|---|---|---|---|
| 2023 | 536.91 | 77.25 | 65.82 | 132.30 | 19.76 | 45.51 | 67.03 |
| 2024 | 637.76 | 88.88 | 77.05 | 157.40 | 20.05 | 54.56 | 82.80 |
| 2025 | 751.50 | 118.30 | 93.34 | 178.79 | 26.52 | 53.73 | 98.54 |

| Periodo | revenue | ebit | ebit_ex_sale_loss | net_income | eps | diluted_shares | cfo | ppe_capex | sbc |
|---|---|---|---|---|---|---|---|---|---|
| 2025Q4 | 192.65 | 34.69 | 34.69 | 25.84 | 0.68 | 37.76 | 45.87 | 7.65 | 10.41 |
| 2026Q1 | 192.12 | 24.56 | 24.56 | 19.73 | 0.53 | 37.44 | 55.63 | 7.14 | 18.07 |
| 2026Q2 | 197.81 | 8.41 | 31.87 | 6.86 | 0.19 | 36.58 | 66.03 | 8.60 | 18.70 |
| 2026Q3 | 197.65 | 39.93 | 39.93 | 30.68 | 0.85 | 36.21 | 64.00 | 5.51 | 15.69 |

Q4 2025 para flujos se calcula como año menos nueve meses. Su BPA 0,68 y 37,763 millones de acciones diluidas proceden directamente del [comunicado anual](https://investors.spscommerce.com/news-releases/news-release-details/sps-commerce-reports-fourth-quarter-and-fiscal-year-2025), no de restar promedios de acciones. Los flujos de Q2 y Q3 son diferencias entre acumulados; el Q3 aislado no es nueve meses. El historial completo y las referencias por celda están en los archivos reproducibles.

| Periodo | revenue | ebit | ebit_ex_sale_loss | ebita_after_sbc_ex_sale_loss | net_income | cfo | ppe_capex | sbc | fcf_after_sbc_diagnostic |
|---|---|---|---|---|---|---|---|---|---|
| TTM September 2025 | 729.76 | 108.36 | 108.36 | 143.81 | 85.06 | 173.48 | 25.09 | 55.61 | 92.78 |
| TTM September 2026 | 780.24 | 107.59 | 131.04 | 169.09 | 83.12 | 231.53 | 28.90 | 62.87 | 139.77 |

TTM = último año completo + nueve meses actuales − nueve meses anteriores. Los BPA TTM son sumas de BPA publicados redondeados; no se utilizan como un promedio exacto de acciones ni como input del DCF. TTM ventas +6,9%; EBIT GAAP −0,7%; EBIT retirando solo la pérdida identificada por venta 3P +20,9%; EBITA después de SBC y sin esa pérdida +17,6%. El beneficio neto GAAP TTM baja 2,3%. No llamamos orgánico al crecimiento normalizado: Carbon6 y el cambio de perímetro afectan las comparaciones. Se mantienen SBC, gastos de consultoría, transición y costes operativos sin una exclusión automática por ser incómodos. La aceleración contractual de premios de ejecutivos no se elimina en este modelo. Además, la compañía revisó en septiembre la vida útil de tecnología de Carbon6 y software interno porque prevé retirar esa plataforma a mediados de 2027. El gasto adicional combinado es 1,3 M$ en Q3, 4,0 M$ previsto en Q4 y 6,9 M$ en 2027. No es un desembolso por sí mismo, pero sí evidencia de obsolescencia, integración y necesidad de inversión; no se vende el addback como beneficio económico gratuito. La mezcla exacta entre amortización adquirida e interna no está desglosada en esa advertencia, por lo que no se elimina en bloque de los costes.

## Venta 3P y normalización

La venta se cerró el 30 de junio de 2026: cobro neto 8,768 M$ y pérdida en EBIT de 23,454 M$. No cumple el criterio de operaciones discontinuadas. Retirar la pérdida contable para estudiar el beneficio recurrente no permite sumar el cobro a FCFF recurrente ni devolverlo dos veces al accionista. La guía ya descuenta aproximadamente 10,5 M$ de ingresos en el segundo semestre y el efecto indicado en EBITDA ajustado es neutro. No restamos esos ingresos otra vez al guidance publicado. El total de 2026 todavía incluye 3P en el primer semestre; no hay un carve-out completo identificado en los estados revisados. El año 2027 del modelo supone directamente 819,42 M$ de ingresos del negocio retenido: el 4% que aparece en la primera fila es crecimiento frente a la guía consolidada 2026, no una tasa orgánica certificada. Si se usa una base 2026 menor en 10,5 M$ como aproximación prudente al primer semestre vendido, el mismo crecimiento arroja un central de 52,23 USD. Esa cifra de primer semestre no es un dato reportado: la sensibilidad muestra el efecto, sin inventar una conciliación. La estimación 2027 original equivaldría a 5,4% sobre esa base menor. Véanse [10-Q](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000075/spsc-20260930.htm) y [guía oficial](https://investors.spscommerce.com/news-releases/news-release-details/sps-commerce-reports-strong-third-quarter-2026-financial-results).

Carbon6 costó 210,2 M$ netos: aproximadamente 142,5 M$ en caja y 67,7 M$ en acciones. No se da por gratis ese crecimiento pasado. Las adquisiciones en efectivo fueron 70,218 / 147,924 / 142,628 M$ en 2023–2025, adicionales al capex. El gasto recurrente en software, relaciones con clientes y reinversión futura se financia explícitamente en el modelo; no se extrapola el crecimiento adquirido de esos años como si fuera orgánico.

## Caja: qué mejora y qué no debe perpetuarse

El CFO de nueve meses aumenta 52,745 M$. La compañía atribuye aproximadamente 40,0 M$ a cambios de calendario y liquidación de activos y pasivos operativos, y 12,8 M$ al beneficio ajustado por partidas sin caja. No anualizamos los 111,956 M$ del indicador CFO menos capex menos SBC a nueve meses.

A nueve meses, CFO 185,664 menos PPE/software 21,246 da FCF de caja 164,418 M$; restar SBC 52,462 deja 111,956 M$. El indicador comparable de 2025 es 70,728 M$. En TTM, el indicador sube de 92,783 a 139,766 M$, pero no representa una nueva base perpetua. Las nuevas deducciones fiscales de I+D también reducen pagos de caja en 2026. Por ello el DCF parte de beneficio operativo y un impuesto normalizado, no del último CFO.

El software desarrollado internamente se incluye en PPE: valor bruto 107,582 M$ a septiembre; no se elimina del capex. Los costes diferidos de contrato suman 84,177 M$, frente a 87,412 M$ en diciembre. En nueve meses se incurren 65,081 M$ y se amortizan 68,316 M$; esa menor inversión/capitalización temporal no se convierte en fuente permanente de valor. El modelo mantiene costes comerciales y de I+D en márgenes, y exige inversión incremental adicional cuando crece el negocio. Fuente: notas D–F y discusión de caja del [10-Q](https://www.sec.gov/Archives/edgar/data/1092699/000109269926000075/spsc-20260930.htm).

## Balance, compromisos y acciones

A 30 de septiembre hay 153,818 M$ de caja y 29,683 M$ de inversiones a corto plazo, sin deuda financiera reportada. Reservamos 50 M$ de liquidez operativa, hipótesis propia, y añadimos únicamente 133,501 M$ al valor operativo. No añadimos otra vez el cobro de la venta 3P, ya incluido en caja.

Se usa 36,209 millones de acciones diluidas de Q3, deliberadamente por encima de las 35,585 millones ordinarias a septiembre y 35,441 millones a 22 de octubre. No se confunde promedio con cifra puntual. Es una protección frente a premios existentes; la SBC futura sigue siendo gasto económico, sin proyectar además dilución gratuita ni recompras gratuitas. La reserva de caja es propia, no efectivo legalmente restringido: añadirla entera elevaría el central solo a 54,27 USD.

Los arrendamientos se tratan como operativos, con renta en costes y sin restar otra vez el pasivo de 6,624 M$. Los compromisos de proveedores de 57,022 M$ financian infraestructura/software y se satisfacen dentro de gastos/inversión proyectados, no mediante una segunda resta indiscriminada de deuda. Los incentivos del arrendador incluyen aproximadamente 14 M$ esperados para 2027; no se añaden como caja excedentaria ni como FCFF perpetuo. Son relevantes para el seguimiento de obras y liquidez, no beneficio recurrente.

## Guía y puente operativo del DCF

La guía 2026 es ventas 786,9–788,9 M$ y EBITDA ajustado 267,4–269,4 M$. En el punto medio: 268,4 − SBC 69,5 − depreciación 24,1 = 174,8 M$ de EBIT antes de amortización adquirida, pero después de SBC. Al restar amortización adquirida 40,8, resultan 134,0 M$, aproximación operativa normalizada; no es una guía GAAP conciliada por la compañía. Su margen de caja operativo inicial es ~22,2%. La empresa advierte que no puede conciliar toda la guía no GAAP sin esfuerzo no razonable. Fuente: [comunicado Q3](https://investors.spscommerce.com/news-releases/news-release-details/sps-commerce-reports-strong-third-quarter-2026-financial-results).

La amortización adquirida se muestra por separado en el puente: no es un desembolso nuevo y la depreciación del software interno sí permanece. La continuidad de tecnología y clientes requiere mantenimiento, ventas/I+D e inversión. Estos costes siguen en margen/capex y en el requisito de reinversión. No se asume una deducción fiscal en efectivo por cada dólar de amortización contable adquirida: los impuestos se calculan sobre EBIT antes de esa amortización. El calendario contable 2027–2030 procede del 10-Q; el saldo posterior se reparte solo para mostrar el puente y no altera FCFF. Esto evita convertir amortización y ahorro fiscal hipotético en caja gratuita.

## Hipótesis propias: diez años y terminal

El modelo no cambia al método de múltiplos. Proyecta FCFF operativo durante cinco años detallados y cinco de transición. Usa convención anual: FY2027 es año 1, descontado un año, sin añadir un flujo parcial de noviembre–diciembre de 2026. Es una convención anual aproximada, no automáticamente conservadora: omitir el flujo parcial resta valor, pero descontar FY2027 a un año en lugar de aproximadamente 1,156 años lo aumenta. Una sensibilidad con 57 días adicionales de descuento da 52.16 USD sin flujo parcial; añadiendo un flujo parcial estimado proporcional al FCFF del primer año da 52.65 USD. Este flujo parcial es una hipótesis, no caja publicada de noviembre–diciembre. Ninguna variante cambia la espera por precio.

Central: crecimiento 4%, 5%, 5%, 4,5%, 4%; margen EBIT antes de amortización adquirida y después de SBC 22,2%, 22,8%, 23,4%, 24%, 24,5%. Impuesto 25%; depreciación PPE/software 3,06% de ventas; capex 4%; inversión de circulante 5% del incremento de ingresos. La aceleración modesta exige recuperar crecimiento comercial, mientras el margen terminal se reduce a 23%. No se modelan compras de empresas identificadas aún no pactadas ni se capitaliza gratuitamente su crecimiento.

La mejora de margen central supone eficiencia operativa y aprovechamiento de costes ya soportados, no crecimiento financiado sin costes. La fórmula usa crecimiento de ventas como aproximación del crecimiento de NOPAT a margen constante; el ROIC de 25% se aplica a esa expansión, no es una medición del retorno marginal de todo el aumento de beneficio cuando cambia el margen. La sensibilidad adicional financia también el aumento positivo de NOPAT asociado a margen y reduce el central a 51.79 USD. La reinversión neta de los años 1–5 es el mayor entre capex − depreciación + Δcirculante y NOPAT de caja × crecimiento / ROIC incremental. El ROIC inicial supuesto es 25%, sensible a costes de adquisición y a mantener ventajas de red. La diferencia se registra como inversión económica adicional para financiar tecnología/clientes y posibles necesidades de expansión. No se presenta como guidance de capex. Por ejemplo, 2027 exige 21,83 M$ de reinversión neta: 32,78 M$ de PPE/software, 12,55 M$ de inversión económica adicional y 1,58 M$ de circulante, menos depreciación 25,07 M$. Es mayor que simplemente extrapolar el reducido capex neto histórico.

Años 6–10: crecimiento, margen y ROIC convergen linealmente a 2,5%, 23% y 20%. El requisito de reinversión converge explícitamente a NOPAT × g / ROIC. En terminal, NOPAT 202,22, reinversión 25,28 y FCFF 176,94 M$. No hay liberación perpetua de circulante. ROIC 20% no es el ROIC observado certificado de SPS, sino una hipótesis a contrastar. Con ROIC inicial/terminal 20%/15%, el central baja a 50,44 USD.

WACC central 10% nominal USD, adverso 11%, favorable 9%. Referencia sin deuda financiera: Treasury a diez años 4,95% el 3 de noviembre, [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve), más prima de riesgo propia de 5,05 puntos en el central. No se afirma haber estimado una beta precisa ni que WACC sea la TIR futura del accionista. La recurrencia ayuda, pero desaceleración, competencia tecnológica y compras de empresas justifican no valorar como un bono. WACC supera g en todos los escenarios.

| Año | Ventas | EBIT tras amortización adquirida | Impuesto caja | D&A total | Inversión total | Δ circulante | Reinversión neta | FCFF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027 | 819.42 | 141.82 | 45.48 | 65.16 | 45.33 | 1.58 | 21.83 | 114.60 |
| 2028 | 860.39 | 166.12 | 49.04 | 56.38 | 53.70 | 2.05 | 29.43 | 117.70 |
| 2029 | 903.41 | 187.78 | 52.85 | 51.26 | 57.20 | 2.15 | 31.71 | 126.84 |
| 2030 | 944.06 | 205.15 | 56.64 | 50.32 | 57.44 | 2.03 | 30.59 | 139.34 |
| 2031 | 981.82 | 233.54 | 60.14 | 37.05 | 57.02 | 1.89 | 28.87 | 151.54 |
| 2032 | 1018.15 | 239.38 | 61.60 | 38.17 | 57.83 | 1.82 | 28.49 | 156.30 |
| 2033 | 1052.77 | 244.60 | 62.90 | 39.23 | 58.38 | 1.73 | 27.90 | 160.81 |
| 2034 | 1085.40 | 249.14 | 64.04 | 40.22 | 58.65 | 1.63 | 27.07 | 165.05 |
| 2035 | 1115.79 | 252.97 | 64.99 | 41.15 | 58.62 | 1.52 | 26.00 | 168.99 |
| 2036 | 1143.69 | 263.05 | 65.76 | 35.00 | 58.26 | 1.39 | 24.66 | 172.63 |

## Escenarios, sensibilidad e inversa

| Escenario | WACC | g terminal | ROIC terminal | Crecimiento inicial | Margen inicial a año 5 | Valor por acción | Peso terminal en EV |
|---|---:|---:|---:|---|---|---:|---:|
| Adverso | 11% | 2% | 15% | 0%, 1%, 2%, 2%, 2% | 20,5% a 20% | 33,64 | 41,2% |
| Central | 10% | 2,5% | 20% | 4%, 5%, 5%, 4,5%, 4% | 22,2% a 24,5% | 52,89 | 51,1% |
| Favorable | 9% | 3% | 25% | 7%, 8%, 8%, 7%, 6% | 24% a 28% | 84,61 | 61,2% |

Adverso incluye margen terminal 19%, impuesto 27% y capex 4,5%; favorable margen terminal 27%, impuesto 24% y capex 3,5%, con ROIC inicial 30%. Son escenarios propios sin probabilidades asignadas. El favorable necesita varias mejoras simultáneas y no debe presentarse como valor seguro.

| WACC central alternativo | g 2% | g 2,5% | g 3% |
|---|---:|---:|---:|
| 9% | 58.78 | 60.69 | 62.90 |
| 10% | 51.62 | 52.89 | 54.33 |
| 11% | 46.06 | 46.93 | 47.90 |

La banda central de sensibilidad es aproximadamente 46–63 USD al variar WACC9–11% y g2–3% con las demás hipótesis centrales. Es la referencia de rango razonable condicionado de esta investigación; no todo el intervalo adverso–favorable se considera valor justo ni existe una probabilidad estadística asociada. El margen de seguridad respecto al central es (52,89−85,25)/52,89 = −61,2%. No se crea un techo de compra con un descuento arbitrario.

Con el mismo modelo e hipótesis centrales restantes, el cierre requiere crecimiento constante de aproximadamente 17,4% en los primeros cinco años, o un margen de caja operativo constante cercano a 38,5% manteniendo crecimiento central. Son ejercicios de una variable, no pronósticos. Combinaciones alternativas: 8% de crecimiento y margen de 30% dan 76,65 USD; 12% y 27% dan 80,42; 12% y 30% dan 88,94. La comparación exige que ingresos y margen cumplan juntos, pagando la reinversión. Directa e inversa son la misma herramienta, no dos evidencias independientes.

## Contrastes y riesgos que cambian la decisión

Al precio de corte, capitalización diluida aproximada 3.086,82 M$. Con caja excedentaria de 133,50 M$, EV analítico 2.953,32 M$: 3,79 veces ventas TTM, 22,54 veces EBIT normalizado TTM y 17,47 veces EBITA normalizado después de SBC. Son múltiplos calculados con el mismo perímetro; el último no equivale a EBITDA ajustado ni elimina el coste de reinvertir. El indicador de caja TTM tras SBC rinde ~4,53% sobre capitalización, pero incluye el beneficio temporal de circulante. El DCF central equivale a un EV/EBITA TTM aproximado de 10,54 veces; no imponemos ese múltiplo desde fuera.

Como contraste operativo, [Manhattan Q3 2026](https://ir.manh.com/node/21721/html) registra ventas +11%, margen GAAP 26,5% y CFO inferior al comparable; [Descartes Q2 FY27](https://www.descartes.com/resources/news/descartes-announces-fiscal-2027-second-quarter-financial-results) registra ventas +12% y margen operativo aproximadamente 32,6%, con distinta mezcla de servicios, adquisiciones y base de reestructuración. Ambos muestran que márgenes mayores son posibles, no que SPS deba recibir su valoración. El contraste de múltiplos sí se calcula con la misma convención para las tres compañías: cierre regular del 3 de noviembre, promedio diluido del último trimestre y deuda financiera menos toda la caja/inversiones cortas reportadas. No se capitalizan arrendamientos porque los gastos siguen en EBIT; no se elimina SBC. Esta convención de caja completa difiere en 50 M$ de la reserva operativa del DCF de SPS y se declara para no mezclar los EV. Las capitalizaciones son aproximaciones diluidas, no acciones puntuales certificadas a la fecha del precio.

| Compañía | Cierre USD | Acciones diluidas M | Caja M$ | Deuda financiera M$ | Ventas TTM M$ | EBIT GAAP TTM M$ | EV/ventas | EV/EBIT GAAP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPSC | 85,25 | 36,209 | 183,501 | 0 | 780,235 | 107,587 | 3,72x | 26,99x |
| MANH | 255,14 | 58,732 | 199,449 | 0 | 1.156,585 | 279,175 | 12,78x | 52,96x |
| DSGX | 91,17 | 87,060 | 401,057 | 0 | 775,167 | 243,599 | 9,72x | 30,94x |

TTM de SPS y Manhattan termina en septiembre; Descartes en julio, dos meses antes. Todas las cifras están en USD y bajo US GAAP; DSGX es la cotización Nasdaq en USD, sin convertir el precio canadiense ni aplicar un ADR. Manhattan: [cierre](https://stockanalysis.com/stocks/manh/history/), [10-Q septiembre](https://ir.manh.com/node/21721/html) y [10-K 2025](https://ir.manh.com/node/21211/html). Descartes: [cierre](https://stockanalysis.com/stocks/dsgx/history/), [segundo trimestre fiscal](https://www.descartes.com/resources/news/descartes-announces-fiscal-2027-second-quarter-financial-results) y [FY2026](https://www.descartes.com/resources/news/descartes-announces-fiscal-2026-fourth-quarter-and-annual-financial-results). La reconstrucción TTM, numeradores y fuentes están en comps_inputs.json/comps.py, no se anualiza un trimestre.

SPS retirando la pérdida de venta 3P cotiza a 22,16x EBIT normalizado con esta convención de caja, frente a 26,99x GAAP. La tabla principal no elimina reestructuraciones o costes extraordinarios selectivamente de unos pares y no de otros. Descartes gastó después del balance 99,3 M$ en TAI y 119,9 M$ en Extensiv. Añadir únicamente ese uso de caja conocido al EV lleva EV/EBIT TTM a 31,84x; no es un balance actual ni un múltiplo pro forma completo, pues faltan los beneficios de lo comprado y los flujos posteriores. Se mantiene visible el desfase, en vez de simular equivalencia exacta.

La señal relativa favorece a SPS frente a estos dos pares, pero no invalida el DCF: la mezcla de servicios de Manhattan, el crecimiento/negocios adquiridos de Descartes y sus márgenes GAAP TTM de 24,1%/31,4%, frente al 13,8% de SPS (16,8% sin la pérdida identificada), justifican cautela. Un par caro no demuestra que el más barato tenga margen absoluto. No se aplica la mediana de estos dos múltiplos a SPS, ni se promedian valores relativos y FCFF. Es un contraste de valoración con diferencias de periodo y perímetro explícitas, no un target independiente.

Reabrir si crecimiento recurrente comparable acelera con retención y economía unitaria defendibles; si la mejora de márgenes persiste sin infra-invertir; o si el precio deja suficiente compensación frente a las sensibilidades. Vigilar normalización fiscal y de circulante, uso del efectivo en recompras/adquisiciones, 1P recovery/take rate y costes de automatización. No se fija un descuento universal ni se convierte 52,89 en techo de compra. El próximo punto de revisión es Q4/FY2026: fecha de publicación aún no verificada en la página oficial de [eventos](https://investors.spscommerce.com/events). No inventamos un día ni declaramos que el evento carece de fecha anunciada.

## Confianza y límites

Alta confianza en cifras históricas conciliadas con estados; confianza media en normalización; incertidumbre alta en crecimiento/margen/ROIC y coste de mantener relaciones adquiridas. El valor no es una cifra certificada por el emisor. El modelo no remunera ahorros fiscales por amortización adquirida ni incentivos de arrendamiento, y usa acciones diluidas históricas conservadoras. No reconstruye un DCF desglosado para cada producto o adquisición ni una valoración relativa con perímetros totalmente pro forma. No se ha validado la técnica diaria, volumen o señal actual de Stage 3.5. No hay compra, venta o modificación de cartera autorizada por este análisis.

## Archivos de auditoría

history.csv / history.json: tres ejercicios, cuatro trimestres y TTM frente al anterior. history_provenance.json: etiquetas, periodos y accesiones. model.py y model_results.json: cálculo completo y pruebas. migration_bridge.py/json: reproducción y puente con A119. comps.py y sus inputs/resultados: contraste de pares. ten_year_model.csv: tres escenarios, diez filas por escenario. Los originales de terceros se conservan solo como fuentes de trabajo; no se incluyen íntegros en el paquete público. Este informe y sus datos derivados son la investigación publicable.
