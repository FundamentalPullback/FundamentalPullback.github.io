# Stage 4 · cierre del 10 de noviembre de 2026

Revisión de las seis posiciones PAPER. Niveles prospectivos para el 11 de noviembre. No se ejecutan operaciones, no se cambian cantidades ni efectivo y no se acredita ninguna orden de protección.

## Decisión de gestión

**DOCU requiere la vigilancia más cercana:** cierre regular de 77,64 USD frente a trailing vigente de 76,97; margen de 0,67 USD, aproximadamente 0,86% del cierre. Su mínimo regular publicado, 76,00, quedó bajo el trailing, pero esta regla se activa por cierre, no por toque intradía. El cierre no activó salida. El stop manual inicial S es otra regla y otro nivel: 62,50 USD.

**Subir las referencias calculadas para la siguiente sesión:** ULTA de 607,61 a **609,58 USD** y EXLS de 39,98 a **40,61 USD**. ASO conserva **63,45 USD** y DOCU **76,97 USD**. Son referencias de gestión calculadas con ChartExchange, no órdenes enviadas al bróker ni precios garantizados de ejecución.

**No se identifica toque de los stops S durante la sesión regular ni ruptura por cierre del trailing previo en ninguna de las seis posiciones.** Los seis cierres están por encima de M, por lo que tampoco se cumple la salida combinada de dos cierres bajo EMA50 y cierre bajo M. No se publica una EMA50 nueva sin reconstrucción verificada.

## Niveles y proximidad

Los cierres y mínimos de esta tabla proceden de StockAnalysis para la sesión regular del 10 de noviembre, separados de la serie usada para el ATR. Porcentaje de distancia = (cierre − protección de la próxima sesión) / cierre. No representa probabilidad de salida ni pérdida máxima.

| Posición | Acciones PAPER ya registradas | Cierre regular USD | Mínimo regular USD | S manual USD | M USD | Protección próxima sesión USD | Distancia desde cierre |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCU | 134 | 77,64 | 76,00 | 62,50 | 63,60 | Trailing 76,97 | 0,67 / 0,86% |
| CTSH | 82 | 65,03 | 63,26 | 61,20 | 61,55 | S 61,20; trailing inactivo | 3,83 / 5,89% |
| ULTA | 16 | 664,57 | 656,17 | 522,00 | 529,01 | Trailing 609,58 | 54,99 / 8,27% |
| EXLS | 160,699 | 44,29 | 42,92 | 33,50 | 34,05 | Trailing 40,61 | 3,68 / 8,31% |
| JXN | 60 | 138,07 | 135,40 | 124,80 | 126,14 | S 124,80; trailing inactivo | 13,27 / 9,61% |
| ASO | 155 | 70,42 | 67,81 | 50,30 | 51,21 | Trailing 63,45 | 6,97 / 9,90% |

Fuentes de precios: [DOCU](https://stockanalysis.com/stocks/docu/history/), [CTSH](https://stockanalysis.com/stocks/ctsh/history/), [ULTA](https://stockanalysis.com/stocks/ulta/history/), [EXLS](https://stockanalysis.com/stocks/exls/history/), [JXN](https://stockanalysis.com/stocks/jxn/history/), [ASO](https://stockanalysis.com/stocks/aso/history/). Consulta después del cierre del 10 de noviembre. No certifica mínimos de todas las sesiones extendidas ni protección automática.

## Continuidad de ATR y revisiones del proveedor

Se parte de la semilla exacta congelada de [A290, al 5 de noviembre](https://fundamentalpullback.github.io/research/2026-11-05/trailing-reconciliation/calculations.json), sin reiniciar ATR ni R. Se aplican las barras refrescadas del mismo proveedor ChartExchange para el 6, 9 y 10 de noviembre. Los valores publicados en [A494](https://fundamentalpullback.github.io/research/2026-11-09/stage4-review/) se conservan como mínimo de protección; una revisión del proveedor no rebaja niveles ni reescribe señales pasadas.

TR = máximo de H−L, |H−cierre previo| y |L−cierre previo|. ATR14 Wilder = (13 × ATR anterior + TR) / 14. Candidato = mayor cierre desde entrada − 3 × ATR14. Nueva referencia = máximo de referencia previa, S y candidato. Se conserva precisión interna y se muestran dos decimales. Primero se compara el cierre del día con la referencia que ya estaba vigente; la nueva referencia se aplica después, desde la siguiente sesión.

| Ticker | ATR14 refrescado al 10 nov | Mayor cierre de la serie | Candidato | Referencia para 11 nov |
|---|---:|---:|---:|---:|
| ASO | 2,622318305975 | 71,18 | 63,313045082076 | 63,45, no baja |
| ULTA | 18,517585233039 | 665,13 | 609,577244300884 | 609,58, sube |
| EXLS | 1,234751735281 | 44,31 | 40,605744794157 | 40,61, sube |
| DOCU | 2,827306085810 | 85,27 | 76,788081742569 | 76,97, no baja |

**Puente con la revisión anterior:** ChartExchange ha revisado campos de la sesión del 9: ASO cierre 71,21 → 71,18 y mínimo 69,05 → 67,47; ULTA cierre 665,03 → 665,13, máximo 672,67 → 672,70 y mínimo 650,02 → 649,82; EXLS cierre 43,34 → 43,33 y mínimo 42,81 → 42,80; DOCU cierre 77,73 → 77,75. El máximo de DOCU del 6 se conserva en 78,50, igual que en A494. El snapshot A494 no se altera. Continuar sus barras congeladas daría ULTA 609,48 y EXLS 40,61; la conciliación explícita de barras revisadas produce 609,58 y 40,61. ASO y DOCU conservan sus suelos publicados en ambas variantes.

**Limitaciones:** los últimos de ChartExchange para el día 10 son 70,42 / 664,68 / 44,31 / 77,66 para ASO / ULTA / EXLS / DOCU. Sus timestamps son 15:59:56–16:00 EST; difieren de StockAnalysis, igual que algunos máximos y mínimos. No se promedian ni se sustituyen barras entre proveedores. DOCU se consultó inicialmente con datos intradía y se volvió a verificar cuando la fuente ya mostraba cierre; solo esa segunda lectura entra al cálculo. Los niveles siguen siendo estimaciones específicas del proveedor, no una certificación de bolsa.

[ASO técnico](https://chartexchange.com/symbol/nasdaq-aso/historical/) · [ULTA técnico](https://chartexchange.com/symbol/nasdaq-ulta/historical/) · [EXLS técnico](https://chartexchange.com/symbol/nasdaq-exls/historical/) · [DOCU técnico](https://chartexchange.com/symbol/nasdaq-docu/historical/). El archivo calculations.json adjunto a esta revisión contiene semilla, barras y cada paso de cálculo.

## Conciliación de posiciones y disciplina

Se conservan las seis posiciones reconciliadas en A494. CTSH tiene 82 acciones a media 65,185, tras las compras de 41 a 66,69 y 41 a 63,68. JXN tiene 60 a 135,95. ANF y HRB siguen cerradas; no se duplican ventas. La revisión visual del estado actual es compatible con esas seis posiciones, pero no sustituye una auditoría completa de todas las operaciones del bróker.

CTSH conserva el R original de 5,49 y la activación +2R en 77,67. JXN conserva R 11,15 y activación en 158,25. Ningún cierre actual alcanza esos umbrales; no se activa trailing ni se recalcula R a partir del promedio de CTSH. S de JXN 124,80 y M 126,14 conservan su adopción/revalidación prospectiva ya documentada en A494. No se validan retroactivamente las excepciones de ejecución de CTSH ni la compra de JXN anterior al cierre.

El toque de S exige gestionar una salida manual según el plan; el trailing por cierre exige evaluar el cierre regular y, si se activa, la salida al siguiente abierto. Ni uno ni otro demuestra un fill. Huecos y deslizamiento pueden superar la distancia nominal a la protección.

## Ampliaciones, parciales y revisión fundamental

**No hay una ampliación nueva aprobada en esta revisión.** Una sesión verde o una mayor distancia al stop no bastan: antes de añadir deben estar actualizados tesis y valoración, señal de entrada, presupuesto de campaña y riesgo por lote. El 25% restante opcional del plan no constituye una orden. Las ventas anteriores no reponen el presupuesto acumulado de campaña.

- **ULTA:** mantener abierta la revisión fundamental prioritaria. El conflicto de valoración de A148 y la reinversión/recompras deben resolverse antes de una nueva aprobación; las compras acumuladas de campaña de 26.319,36 USD mantienen bloqueada la ampliación. Subir trailing no equivale a certificar valor razonable.
- **DOCU:** mantener revisión fundamental prioritaria abierta, particularmente coste económico de SBC, reinversión y retorno esperado. El diagnóstico A148 no es una señal automática de venta. La cercanía al trailing exige seguimiento, no una segunda parcial improvisada.
- **EXLS:** usar la actualización posterior A196 y sus escenarios condicionados 17,20 / 31,25 / 57,16, no el diagnóstico antiguo. Revisar caja y obligaciones de adquisiciones antes de añadir.
- **ASO:** el diagnóstico A148 no constituye una nueva aprobación. Compras acumuladas de campaña de 12.470 USD no se restablecen por la parcial.
- **CTSH:** el añadido del 9 de noviembre conserva su carácter discrecional, sin señal verificada. La adquisición de Wizeline requiere revisión de integración y desembolso cuando haya información, sin sinergias gratuitas.
- **JXN:** A293 sigue condicionado; reservas, remesas y capital regulatorio continúan siendo controles esenciales. No se eleva S arbitrariamente al soporte táctico de 130,59.

Se preservan las parciales históricas y no se propone una segunda parcial automática. Las revisiones fundamentales abiertas no suspenden una salida válida por protección.

## Noticias y alcance de la comprobación

La búsqueda dirigida en fuentes corporativas no localizó una nueva publicación de resultados o guidance del 10 de noviembre para estas seis compañías que justificase cambiar aquí la tesis. Es una búsqueda limitada, no una garantía de ausencia de noticias ni una revaloración completa. Siguen como antecedentes de la revisión anterior Wizeline/CTSH, Aimpoint/EXLS, Suplari/DOCU, Oura/ULTA, la campaña navideña de ASO y los resultados de JXN. No se atribuye impacto financiero nuevo sin cuantificación.

Fuentes corporativas consultadas: [Cognizant](https://investors.cognizant.com/news-and-events/news/default.aspx), [EXL](https://www.exlservice.com/about/newsroom), [Docusign](https://investor.docusign.com/news-and-events/press-releases/), [Jackson](https://www.jackson.com/the-jackson-difference/who-we-are/news.html). Las búsquedas de ULTA y ASO del día no dieron un nuevo comunicado verificable. Mantener las revisiones abiertas ya descritas en A494; no presentar esta actualización técnica como Stage 3 completado.

[Plan vigente](https://fundamentalpullback.github.io/data/plan/Plan_Completo_2026-11-09.pdf). Investigación y gestión de cartera PAPER; sin órdenes, nuevas operaciones ni información de otras cuentas.
