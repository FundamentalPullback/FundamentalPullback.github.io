# GXO Logistics | Stage 3 parcial
**Fecha de investigación: 8 de noviembre de 2026. Cierre regular: 6 de noviembre de 2026. USD; estados en millones salvo acción.**

**Conclusión: vigilancia; no decisión de valoración ni entrada aprobada.** La aceleración comercial es real según la compañía, pero no demuestra mayor caja económica. El cambio hacia inversión financiada con arrendamientos hace inadecuado proyectar el FCF publicado sin conciliación. No se calcula precio objetivo, precio máximo, margen de seguridad, escenario inverso ni sensibilidades con una base sin cerrar.

## Cobertura y precio
Último escáner: 6/11/2026, Opportunity 80, QP 80, RSI 72,7, Last 55,18. La autorización de investigar desde 65 no transforma ese score en aprobación Stage 3.5.

El cierre **55,18 dólares** se verificó separadamente en [IR/LSEG](https://investors.gxo.com/stock-information/historical-price-lookup) y [StockAnalysis](https://stockanalysis.com/stocks/gxo/history/), este último con hora **16:00 EST, 21:00 UTC**. Volumen 1.269.273. El Last coincide, pero no fue usado como prueba del cierre. Tras resultados, el cierre pasó de 52,03 el 3/11 a 56,96 el 4/11 (+9,48%); ello no constituye prueba de infravaloración. No se validaron EMA200, pendiente ni estructura para entrada.

## Fechas y negocio
Resultados 3T26 publicados **3/11/2026**, llamada **4/11/2026** y 10-Q presentado **4/11/2026**. Ya son hechos conocidos, no catalizadores futuros. **Investor Day: 16/11/2026 a las 09:00 ET**, todavía futuro al corte. Fuente: [resultados oficiales](https://investors.gxo.com/news-releases/news-release-details/gxo-reports-third-quarter-2026-results).

Logística contractual: almacenes, distribución, fulfillment y devoluciones. El [anual 2025](https://investors.gxo.com/static-files/df5b7f88-7dff-4738-a600-60a6e1107a9d) sitúa cinco clientes en aproximadamente 20% de ingresos y ninguno por encima de 6%. Esto reduce concentración individual, no elimina concentración sectorial: omnicanal representó 49% en 2025. Crecer en tecnología, industria y defensa puede diversificar, pero requiere inversión y ejecución.

## Historia publicada y calculada
Fuentes S1/S3/S4/S5/S6 del registro. `history.csv` y `actuals.json` conservan cifras y `build_research.py` reproduce diferencias. Beneficio neto es consolidado, no siempre atribuible a GXO.

| Periodo | Ventas | EBIT GAAP | Neto | CFO | Capex caja | Ventas PP&E | FCF compañía |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 9.778 | 318 | 233 | 558 | 274 | 18 | 302 |
| 2024 | 11.709 | 218 | 138 | 549 | 359 | 61 | 251 |
| 2025 | 13.178 | 245 | 36 | 434 | 324 | 149 | 259 |
| 4T25 | 3.507 | 94 | 43 | 170 | 55 | 48 | 163 |
| 1T26 | 3.298 | 39 | 5 | 31 | 65 | 3 | -31 |
| 2T26 | 3.441 | 77 | 27 | 76 | 65 | 1 | 12 |
| 3T26 | 3.590 | 96 | 65 | 156 | 74 | 3 | 85 |
| TTM sep25 | 12.921 | 252 | 93 | 450 | 373 | 146 | 223 |
| TTM sep26 | 13.836 | 306 | 140 | 433 | 259 | 55 | 229 |

TTM = ejercicio previo + nueve meses actuales − nueve meses previos. 1T26 = semestre − 2T26. FCF = CFO − capex caja + ventas PP&E; **no es FCFF**. Capex y ventas PP&E de 2T26 proceden de la conciliación oficial de FCF; 1T26 se obtiene restando ese trimestre al semestre. SBC trimestral1T/2T no se distribuye sin fuente. El TTM de ingresos aumenta 7,1%, mientras CFO cae 3,8%. Caja después de capex antes de ventas de activos: 174 TTM actual frente a 77 previo; esa mejora todavía omite inversión no monetaria por leasing.

## Qué cambia tras el 3T26
Crecimiento orgánico comunicado 6,4% y ventas +5,7%; EBITDA ajustado 251, igual al año previo; margen ajustado 7,0% frente a 7,4%. El EBIT GAAP cae de 118 a 96. El EPS se beneficia de impuesto trimestral bajo y no debe extrapolarse sin normalizarlo. Guidance 2026 reiterado: orgánico 4%-5%, EBITDA ajustado 945-965, EPS ajustado 2,95-3,15 y FCF/EBITDA 30%-40%. Es guidance de la empresa, no FCFF del analista. [Fuente](https://investors.gxo.com/news-releases/news-release-details/gxo-reports-third-quarter-2026-results).

## Caja, inversión y normalización
El [10-Q, notas 4/6/7/9/10](https://investors.gxo.com/static-files/0aa63e58-d87a-458c-8475-d220c2fe9451) y el anual permiten identificar los siguientes controles, aún sin aprobar un FCFF normalizado:

| Control | 9M26 | 9M25 |
|---|---:|---:|
| CFO | 263 | 264 |
| Capex de caja | 204 | 269 |
| Ventas PP&E | 7 | 101 |
| FCF publicado calculado | 66 | 96 |
| Altas de activos finance-lease | 207 | 83 |
| Capex caja + altas finance-lease | **411** | **352** |
| SBC | 35 | 34 |
| D&A | 347 | 337 |
| Amortización de intangibles adquiridos | 84 | 90 |
| Costes transacción/integración | 54 | 50 |
| Reestructuración | 11 | 22 |

La inversión conjunta sube **16,8%**, frente al descenso **24,2%** del capex de caja. Esta suma combina capex de caja con activos ROU obtenidos a cambio de pasivos de arrendamiento. No prueba inversión física bruta comparable, gasto de mantenimiento ni reinversión normalizada.

**Bloqueo concreto:** anual FY25, nota 9, presenta 74 de altas finance-lease; el comparativo 9M25 muestra 83, confirmado también en el 10-Q original de 2025. Restarlos produce -9 en 4T25. Se revisaron las tablas de leasing y notas adyacentes: la nota de adquisición del anual (83) corresponde a 2024, frente a 36 de adquisición en el comparativo 9M24 original; no explica por sí sola FY25 frente a 9M25. No se encontró allí un puente cuantificado de modificaciones/reclasificaciones que cierre la diferencia. No se afirma error contable ni que ambos importes sean inversión física bruta comparable. Antes de usar 198 como alta TTM mecánica (74+207−83), debe reconciliarse su significado económico. No convertir ese -9 en inversión negativa recurrente.

Software interno forma parte de PP&E: saldo bruto 436 al cierre de 2025 frente a 398 en 2024. El aumento de saldo no es gasto de inversión anual: incluye otros movimientos. Incluirlo dentro del capex, no sumarlo dos veces. SBC permanece como coste económico. Los 21 de ingreso de pensiones de 9M26 ya están fuera del EBIT GAAP; no deben restarse de nuevo al normalizar ese EBIT.

Normalizaciones pendientes: beneficio inmobiliario de 30 en 9M26 por terminación anticipada; recurrencia de integración y reestructuración; impuesto operativo sostenible; cobros/factoring y coste de puesta en marcha de nuevos contratos. No se elimina automáticamente todo coste que la compañía ajusta. Tampoco se anualiza nueve meses de caja estacional.

## Adquisiciones y perímetro
Wincanton se adquirió en abril 2024; parte del salto 2024/25 no es orgánico. La integración empezó tras aprobación condicionada y la desinversión de contratos de alimentación se completó en septiembre 2026: pago de caja 38 y pérdidas adicionales 24 en 9M26. El pago de 38 figura como salida de inversión y queda fuera del FCF de compañía; la pérdida contable de 24 no equivale a otro pago. No se vuelve a descontar el desembolso histórico del puente de caja/deuda actual. El crecimiento denominado orgánico en la conciliación de 2026 excluye FX; no aporta aquí una eliminación separada del perímetro desinvertido. Falta cuantificar su efecto futuro en ventas/EBIT.

Clipper es anterior a esta ventana: el 10-K2024 atribuye 20 de integración de 2023 a Clipper y 12 a PFS. No asumir sinergias nuevas gratis por Clipper. La [llamada FY2025](https://investors.gxo.com/static-files/16196f3a-f852-4288-8ec0-b7148d2b448f) comunicó objetivo de Wincanton de 60 de run-rate al entrar en 2027. Es objetivo, no prueba de ahorro incremental pendiente al 8/11: requiere conciliar lo ya realizado y lo ya incorporado al guidance.

## Balance y puente hacia la acción
30/9/2026: deuda contable 2.818 **incluye 487 finance leases**; no restarlos de nuevo. Caja 340, restringida 3 excluida. Deuda neta contable antes de sobregiros: 2.478; añadiendo sobregiros2, deuda neta publicada2.480. Costes/descuentos de emisión identificados 21 permiten aproximar 2.839 de principal/obligación, sujeto a revisión. Operating leases: 777 corriente +2.225 largo =3.002; permanecerán como gasto operativo en FCFF y no se restarán otra vez como deuda.

NCI contable31 no equivale automáticamente a valor económico. Acciones al cierre113,026 millones versus promedio diluido3T114,636: no son intercambiables. Ninguna recompra futura gratuita. Superávit pensiones UK160 a diciembre2025: no añadirlo como efectivo disponible; no se ha probado distribuibilidad. El 10-Q mantiene planes UK como activos y otros planes no materiales. Se pagaron400 de bonos en julio2026; siguiente préstamo275 vence mayo2027. Fuente: [10-Q](https://investors.gxo.com/static-files/0aa63e58-d87a-458c-8475-d220c2fe9451).

## Método y coste de capital
Se mantiene FCFF10años, 5 explícitos+5 transición y terminal con reinversión=NΟPAT×g/ROIC. `model.py` implementa las fórmulas y exige confirmación de puentes cerrados; **no es un DCF calibrado, ni workbook de valoración**. El beneficio financiero del leasing no sustituye su inversión física. La reposición, crecimiento y margen deben pertenecer al mismo perímetro.

Insumos encontrados, no WACC aprobado:
- Treasury10Y **4,86%**, 6/11/2026, [fuente primaria](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve).
- ERP **4,41%**, 1/11/2026, trailing12m adjusted payout, [Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm). Su página muestra Treasury5,29% para su propio cálculo mensual; difiere del Treasury diario actual. No confundir ambas fechas/bases.
- Beta5Y mensual **1,54**, resultado indexado [Yahoo](https://finance.yahoo.com/quote/GXO/); apertura directa429. Falta verificación robusta de ventana y benchmark.
- Bono GXO6,50%2034: YTM indicativo **6,10% al5/11**, [CUSIP36262GAG6](https://www.atlantisdatasolutions.com/bond/36262GAG6). No sustituir cupón por coste de deuda ni presentar ese YTM como ejecución; es callable.

Rf+beta×ERP produce 11,6514% aritmético, no coste de equity definitivamente adoptado. Faltan impuesto sostenible, mezcla de capital y verificación de inputs para aprobar WACC. No se añaden primas discrecionales. El ROIC operativo publicado45,6% usa capital seleccionado sin goodwill ni intangibles adquiridos; no se adopta como ROIC incremental terminal. Sin cerrar la caja recurrente y el perímetro, producir tres precios, un inverso o un múltiplo histórico sería precisión ficticia.

## Pros · GXO
- Aceleración orgánica publicada y oportunidades comerciales en nuevos verticales; clientes individuales poco concentrados.
- Sinergias de Wincanton ofrecen palanca si se realizan sin duplicar objetivos ya incluidos en guidance.
- Cierre y calendario verificados con información posterior al 3T26, evitando una valoración anterior al evento.

## Cons · GXO
- EBITDA trimestral plano pese al crecimiento; margen GAAP y caja necesitan normalización de extraordinarios y perímetro.
- Inversión financiada por leasing material, con diferencia FY25/9M25 todavía sin reconciliar.
- Deuda, necesidad de efectivo operativo y futuras inversiones impiden equiparar FCF publicado con caja distribuible.

## Próximo paso preciso
Conciliar FY25/9M25 de finance leases y la reinversión por contrato; validar impuestos y perímetro vendido; actualizar sinergias realizadas. Solo entonces calibrar escenarios10años, terminal/ROIC, inverso y sensibilidades y someterlos a auditoría independiente. Investor Day16/11 puede aportar evidencia, pero no se anticipan sus resultados. No se han enviado preguntas a IR, cursado operaciones ni publicado cambios.

## Revisión independiente de esta entrega parcial
Historia, diferencias trimestrales, TTM, cierre y controles principales contrastados. Sin DCF calibrado, coste de capital aprobado, valor canónico ni entrada. Las cifras -9 y 198 se conservan solo como diagnósticos aritméticos rechazados, no como altas aceptadas. La revisión no cierra los bloqueos económicos ni autoriza publicación.