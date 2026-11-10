# Stage 4 · revisión al cierre del 9 de noviembre de 2026

**A494 · Publicada el 10 de noviembre. Aplicación prospectiva para la sesión del 10 de noviembre de 2026.**

Esta revisión actualiza la gestión de las seis posiciones PAPER abiertas. Distingue las operaciones ya registradas, los indicadores calculados y las órdenes del bróker. **No añade operaciones ni cambia cantidades, efectivo o la serie de resultados. No acredita ninguna orden de protección.** El stop S de JXN a 124,80 USD queda adoptado manualmente en esta revisión; su M de 126,14 USD queda revalidado ahora, sin validación retroactiva de la compra.

## Conclusión operativa

- ASO: trailing de referencia por cierre calculado sube de 60,57 a **63,45 USD**. Es una estimación específica del proveedor; no rebaja ningún nivel confirmado superior.
- ULTA: trailing por cierre calculado sube de 606,31 a **607,61 USD**. Revisión fundamental prioritaria **abierta**, sin ampliación.
- EXLS: conserva trailing **39,98 USD**; usar A196 como actualización fundamental posterior a A148.
- DOCU: conserva trailing **76,97 USD**. Cierre regular 77,75, solo 0,78 USD por encima; revisión fundamental prioritaria **abierta**, sin ampliación.
- CTSH: conserva S manual **61,20 USD**, M **61,55 USD** y R original **5,49 USD**. Umbral +2R **77,67 USD**; trailing inactivo.
- JXN: S manual **124,80 USD** confirmado en esta revisión del 10 de noviembre UTC (9 de noviembre EST), efectivo para la sesión del 10; M **126,14 USD** revalidado ahora. R **11,15 USD**, umbral +2R **158,25 USD**; trailing inactivo.

En las posiciones abiertas no se identifica toque de S, ruptura por cierre del trailing previo ni salida combinada EMA50 + M en las sesiones del 6 y 9 de noviembre. Esta comprobación no convierte un nivel adoptado ahora en protección acreditada durante la compra. Una salida válida sigue teniendo prioridad sobre cualquier parcial o revisión fundamental pendiente.

## Posiciones y niveles vigentes

Cantidades reconciliadas con las operaciones PAPER ya publicadas. Los cierres de la columna siguiente son los de sesión regular del 9 de noviembre, 16:00 EST, publicados por StockAnalysis. No son cotizaciones extendidas ni precios ejecutables garantizados.

| Ticker | Acciones abiertas | Cierre regular · USD | S manual · USD | M · USD | Trailing por cierre para 10 nov · USD |
|---|---:|---:|---:|---:|---:|
| ASO | 155 | 71,18 | 50,30 | 51,21 | 63,45 calculado |
| ULTA | 16 | 665,13 | 522,00 | 529,01 | 607,61 calculado |
| DOCU | 134 | 77,75 | 62,50 | 63,60 | 76,97 |
| EXLS | 160,699 | 43,33 | 33,50 | 34,05 | 39,98 |
| CTSH | 82 | 63,60 | 61,20 | 61,55 | Inactivo |
| JXN | 60 | 135,51 | 124,80 | 126,14 | Inactivo |

**S manual:** si el precio toca el nivel, corresponde gestionar la salida manual conforme al plan; no implica que haya una orden enviada al bróker. **Trailing por cierre:** se contrasta el cierre con el nivel vigente antes de esa sesión. Un mínimo intradía por debajo del trailing no activa por sí solo esa regla. El nivel nuevo calculado al cierre se aplica a la sesión siguiente, nunca hacia atrás. Un hueco o deslizamiento puede producir una ejecución peor que la referencia.

## Continuidad del trailing: A290 → 6 y 9 de noviembre

Se continúa la semilla exacta de ATR14 Wilder y el mayor cierre desde la entrada que quedaron documentados en [A290](https://fundamentalpullback.github.io/research/2026-11-05/trailing-reconciliation/report.html). No se reinicia el ATR y no se mezcla la serie de ChartExchange con los cierres de StockAnalysis. Se conserva toda la precisión interna; se muestran dos decimales.

TR = máximo de H−L, |H−cierre previo| y |L−cierre previo|. ATR14 nuevo = (13 × ATR14 previo + TR) / 14. Candidato = mayor cierre desde entrada − 3 × ATR14. Referencia siguiente = máximo de S, referencia previa y candidato: **nunca baja**.

| Ticker | ATR14 al 9 nov | Mayor cierre de la serie · USD | Candidato · USD | Referencia previa · USD | Referencia 10 nov · USD |
|---|---:|---:|---:|---:|---:|
| ASO | 2,587112021819 | 71,21 | 63,448663934544 | 60,566971190359 | 63,45 |
| ULTA | 19,138333547668 | 665,03 | 607,614999356996 | 606,308515355301 | 607,61 |
| EXLS | 1,220556813819 | 43,61 | 39,948329558543 | 39,983743156654 | 39,98 |
| DOCU | 2,866329630873 | 85,27 | 76,671011107382 | 76,970000000000 | 76,97 |

**Límite de la fuente:** la fila del 9 de noviembre de ChartExchange recogía últimos cruces de 15:59:xx, antes de la subasta de cierre. Sus campos de cierre eran ASO 71,21, ULTA 665,03, EXLS 43,34 y DOCU 77,73 USD, distintos de los cierres de las 16:00 de StockAnalysis. Son cálculos prospectivos específicos de ese proveedor, no cierres certificados por la bolsa ni órdenes. No se sustituye el cierre contable ya publicado por esos cruces. Una revisión posterior de la fuente no reescribe este snapshot.

Las dos sesiones se comparan primero contra su trailing previo. DOCU tuvo mínimo de 76,70 el 9 de noviembre, por debajo de 76,97, pero cierre regular de 77,75 y campo de cierre ChartExchange de 77,73: ninguno rompe la referencia por cierre. Se conserva 76,97 porque el nuevo candidato es inferior. El mínimo del 6 de noviembre tampoco activa por sí solo un trailing por cierre.

[Continuación de cálculo y barras del 6 y 9 de noviembre](https://fundamentalpullback.github.io/research/2026-11-09/stage4-review/trailing-calculations.json) · [Semilla exacta de A290](https://fundamentalpullback.github.io/research/2026-11-05/trailing-reconciliation/calculations.json)

## EMA50 y regla combinada con M

EMA50 calculada en la revisión original con 251 sesiones de ChartExchange, del 10 de noviembre de 2025 al 9 de noviembre de 2026. Semilla: media aritmética de los primeros 50 cierres, el 22 de enero de 2026; alpha = 2/51. El contador se pone a cero cuando el cierre es igual o superior a la EMA50 de esa sesión. No se mezcla el cierre de otro proveedor. Se publican la metodología y los resultados revisados; este resumen no contiene las 251 barras originales.

| Ticker | EMA50 al 9 nov · USD | Cierres consecutivos bajo EMA50 |
|---|---:|---:|
| ASO | 56,2083 | 0 |
| ULTA | 588,2930 | 0 |
| DOCU | 73,2040 | 0 |
| EXLS | 38,5610 | 0 |
| CTSH | 62,4508 | 0 |
| JXN | 132,1529 | 0 |

JXN tuvo el 6 de noviembre cierre ChartExchange 131,69 frente a EMA50 132,0199, contador 1. El 9 de noviembre, 135,41 frente a EMA50 132,1529 lo devuelve a 0. La recuperación de 133,94 se observa al cierre, después del fill, y **no valida retroactivamente la entrada**. Ninguna de las seis posiciones reúne ahora la regla combinada de dos cierres consecutivos bajo EMA50 y cierre bajo M.

[Metodología y resultados de EMA50](https://fundamentalpullback.github.io/research/2026-11-09/stage4-review/ema50-method-results.json)

## JXN: adopción de S y revalidación de M

Compra PAPER ya registrada: **60 acciones a 135,95 USD el 9 de noviembre a las 15:57:24 EST**. El fill ocurrió antes del cierre regular. La revisión del cierre y la aprobación manual posterior no eliminan esa excepción de timing ni prueban una orden de protección preexistente.

- **S = 124,80 USD:** confirmado como stop manual en esta revisión del 10 de noviembre UTC (9 de noviembre EST), efectivo para la sesión del 10 de noviembre. No se modifica el registro histórico de compra para aparentar que el stop estaba adoptado antes.
- **M = 126,14 USD:** mínimo exacto del 1 de octubre, contrastado en StockAnalysis y ChartExchange. Después aparecen mínimos superiores: 126,88 el 15 de octubre, 127,34 el 20 de octubre, 127,91 el 23 de octubre y 130,59 el 6 de noviembre. Se revalida ahora como referencia estructural amplia.
- **130,59 USD** es soporte táctico reciente, no un reemplazo automático de M ni un nuevo S.
- Coste de las 60 acciones: **8.157,00 USD**. Diferencia nominal coste–S: **669,00 USD**, antes de deslizamiento y nuevas comisiones. R = 135,95−124,80 = **11,15 USD**; +2R = **158,25 USD**.
- Trailing inactivo; ninguna parcial ejecutada ni nueva ampliación autorizada en esta revisión.

La valoración A293 sigue siendo investigación condicionada. Los resultados publicados el 3 de noviembre y comentados el 4 incluyen EPS ajustado de 7,55 USD, generación de capital de 281 millones, RBC de 524% y ampliación de recompra en 1.000 millones. La ganancia GAAP de 337 millones ligada al negocio reasegurado no se extrapola como caja recurrente. Reservas, remesas y capital regulatorio siguen siendo riesgos de la tesis.

## CTSH: añadido registrado, R original conservado

Dos compras PAPER ya publicadas: 41 acciones a 66,69 y 41 a 63,68 USD; **82 acciones**, coste **5.345,17 USD**, media **65,185 USD**. S manual 61,20 y M 61,55 se conservan. Diferencia nominal coste–S: **326,77 USD**, antes de deslizamiento y nuevas comisiones.

La primera compra es compatible con señal, precio y tamaño documentados, pero la ejecución a mercado en vez de limitada queda como excepción. El añadido del 9 de noviembre es discrecional, sin señal verificada. No se reescribe como ejecución automática del plan. R original = 66,69−61,20 = **5,49 USD** y +2R original = **77,67 USD**. El promedio menor, un añadido o una parcial **no reinician R**. Trailing inactivo, sin parcial ni nuevo añadido autorizado.

La adquisición de Wizeline se completó el 6 de noviembre, con términos no divulgados. Puede ampliar capacidades, pero no se asignan sinergias ni aportación financiera gratuitas al modelo.

## Revisión fundamental: trabajo abierto y referencias fechadas

Esta es una revisión de gestión y noticias, **no una nueva valoración completa**. No se certifican como valores aprobados los diagnósticos de A148. Una revisión abierta no suspende salidas válidas y tampoco constituye una venta automática.

- **ULTA:** revisión fundamental prioritaria abierta. A148 confrontaba diagnóstico de 389,36 USD con contraste de 676 USD; falta resolver duración del crecimiento, reinversión, recompras y coste de capital. La colaboración con Oura anunciada el 9 de noviembre prevé venta online el 10 y en 1.000 tiendas el 22; no ofrece impacto financiero cuantificado. Próximos resultados: **3 de diciembre**, calendario corporativo. Compras acumuladas de campaña **26.319,36 USD**; ampliación bloqueada y las ventas no restauran ese presupuesto.
- **DOCU:** revisión fundamental prioritaria abierta. Diagnóstico A148 **56,10 USD**, no decisión ejecutable. Revisar coste económico de SBC, reinversión y retorno; no afirmar tesis operativa rota por ese número. Suplari, anunciada el 3 de noviembre, carece de aportación cuantificada: no inventar sinergias. Compras acumuladas **13.775,84 USD**, sin reinicio tras parcial. No se certifica aquí una próxima fecha de resultados no verificada en fuente primaria.
- **EXLS:** la actualización posterior **A196** ofrece escenarios condicionales **17,20 / 31,25 / 57,16 USD**. No usar el diagnóstico antiguo de aproximadamente 36,69 como valoración actual. Vigilar conversión de caja y obligaciones por adquisiciones. Aimpoint, anunciada el 5 de noviembre, incorpora alrededor de 250 especialistas; términos no divulgados, sin aportación inventada al valor.
- **ASO:** diagnóstico A148 **61,52 USD**, no nueva aprobación. Persisten comprobaciones de reinversión, deuda y comparables. El anuncio de ofertas navideñas del 9 de noviembre no es un resultado trimestral ni una actualización de guidance. Compras acumuladas de campaña **12.470,00 USD**, no restauradas por la parcial.

## Parciales, cierres y disciplina del plan

Se conservan las parciales históricas: ASO 77, EXLS 80, DOCU 67 y la historia de ULTA. **No hay segunda parcial automática** por una nueva subida. El 25% restante descrito como opcional en el plan v2.1 del 9 de noviembre no es una compra automática ni una ampliación aprobada. El capital de campaña no se repone al vender.

**ANF está cerrada:** venta de las 30,8615 acciones restantes a 152,03 USD el 9 de noviembre a las 09:31:32 EST, ya registrada. Resuelve la ruptura del cierre del 6 de noviembre, 149,54, frente al trailing previo 151,69. La señal de salida queda resuelta y no quedan acciones abiertas.

**HRB está cerrada:** parcial de 18 a 55,29 USD el 5 de noviembre y venta de las 36 restantes a 52,44 el 9 de noviembre a las 12:35:29 EST, ya registradas. El cierre antes de resultados fue discrecional; **no fue un disparo del trailing**. Los niveles históricos de ambas posiciones se preservan solo como historia.

[Plan vigente v2.1 · 9 noviembre](https://fundamentalpullback.github.io/data/plan/Plan_Completo_2026-11-09.pdf)

## Dos medidas nominales distintas

Tras adoptar S de JXN, la suma nominal desde los costes restantes a los S de las seis posiciones es **2.631,44 USD**. Desde los precios de cierre regular del 9 de noviembre hasta esos mismos S es **9.989,05 USD**. Son bases distintas: la segunda incluye beneficios no realizados que podrían ceder antes de S. No son reservas de efectivo, pérdidas garantizadas ni un máximo de pérdida. No incluyen deslizamiento o nuevas comisiones; los huecos pueden superar esos importes. La vista de cartera calcula la segunda medida con los precios de la fuente que muestra en cada momento. El control presupuestario del plan requiere cálculo por lote, pérdidas realizadas y reservas; esta diferencia agregada no lo sustituye.

## Fuentes y límites

Precios de sesión regular: [ASO](https://stockanalysis.com/stocks/aso/history/), [ULTA](https://stockanalysis.com/stocks/ulta/history/), [DOCU](https://stockanalysis.com/stocks/docu/history/), [EXLS](https://stockanalysis.com/stocks/exls/history/), [CTSH](https://stockanalysis.com/stocks/ctsh/history/), [JXN](https://stockanalysis.com/stocks/jxn/history/). Series técnicas: [ASO](https://chartexchange.com/symbol/nasdaq-aso/historical/), [ULTA](https://chartexchange.com/symbol/nasdaq-ulta/historical/), [DOCU](https://chartexchange.com/symbol/nasdaq-docu/historical/), [EXLS](https://chartexchange.com/symbol/nasdaq-exls/historical/), [CTSH](https://chartexchange.com/symbol/nasdaq-ctsh/historical/), [JXN](https://chartexchange.com/symbol/nyse-jxn/historical/).

Noticias primarias: [Cognizant / Wizeline](https://investors.cognizant.com/news-and-events/news/news-details/2026/Cognizant-Completes-Acquisition-of-Wizeline/default.aspx), [EXL / Aimpoint](https://ir.exlservice.com/news-releases/news-release-details/exl-acquires-data-and-ai-consulting-market-leader-aimpoint), [Docusign / Suplari](https://www.docusign.com/company/news-center/docusign-acquires-suplari-to-accelerate-aipowered-contract-management-for-procurement), [Oura / Ulta Beauty](https://ouraring.com/blog/sv/oura-ring-ulta-beauty/), [calendario de ULTA](https://www.ulta.com/investor/news-events/ir-calendar), [campaña navideña de ASO](https://investors.academy.com/news-releases/news-release-details/academy-sports-outdoors-unwraps-top-holiday-gifts-great-value), [JXN · resultados Q3 en SEC](https://www.sec.gov/Archives/edgar/data/1822993/000182299326000170/exhibit991-3q26.htm).

Publicación web de gestión PAPER. No afirma sincronización con otros documentos maestros, nueva aprobación fundamental, señal de compra ni ejecución. A148, A196, A247, A290 y A293 permanecen accesibles con sus fechas y límites originales. El escáner posterior A495 conserva su propio alcance y sus limitaciones.
