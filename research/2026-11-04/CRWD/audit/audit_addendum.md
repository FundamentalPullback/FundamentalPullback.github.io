# CRWD: auditoría independiente y anexo de cobertura histórica

Corte: 3 de noviembre de 2026; comprobación: 4 de noviembre. USD millones, salvo precio por acción. Este anexo no modifica silenciosamente el modelo original ni constituye autorización de compra.

## Conclusión de la auditoría

Se reproducen **$33,86 central y $81,86 favorable original** frente a $244,68. No aparece un error de split 4:1, de moneda o de sumar dos veces la SBC que explique la distancia. La valoración económica es muy inferior a la cotización bajo la senda central; ello no demuestra que el precio deba converger en una fecha concreta. El central no parece operativamente extremo: concede una expansión desde EBIT GAAP negativo hasta margen económico después de SBC del 24%, y ventas de $20.930 millones en diez años.

**Sí se debe ampliar la exposición del caso favorable.** $81,86 es un escenario concreto, no un techo de valoración. Con crecimiento mucho más duradero y márgenes elevados se obtiene $140–239. La afirmación de que solo una aceleración inicial próxima al 39% podría sostener la cotización sería demasiado fuerte: depende de la moderación rápida impuesta en aquella familia de reverse DCF. Existe otra combinación que reproduce el precio con **30,31% de crecimiento anual durante diez años**, margen económico final del 35%, WACC 8,5%, crecimiento terminal 3,5% y ROIC terminal 35%. Esta trayectoria supone ventas cercanas a $85.000 millones en el año diez, muy superiores al objetivo empresarial documentado de ARR de $20.000 millones dentro de FY35. No es imposible, pero tampoco está demostrada por los resultados publicados. ARR e ingresos no son idénticos.

La investigación Stage3 puede darse por completa **con este anexo y sus hipótesis explícitas**, conservando la conclusión de observar por valoración. No hay una regla universal de descuento del 15%. El análisis técnico Stage3.5 y el riesgo de cartera siguen separados; no se han validado órdenes ni entradas.

## 1. TTM comparable y normalización

La fórmula es FY cerrado en enero + seis meses hasta julio − seis meses comparables del año anterior. Los resultados de julio de 2024 y 2025 se ajustan a las revisiones de SBC del 10-K FY26. El efectivo no cambió por esa revisión.

| Magnitud | TTM julio 2025 | TTM julio 2026 |
|---|---:|---:|
| Ingresos | 4.341,102 | 5.396,145 |
| EBIT GAAP revisado | −357,840 | −132,954 |
| Beneficio atribuible | −276,167 | 44,995 |
| CFO | 1.388,797 | 2.016,615 |
| Capex efectivo + software | 350,863 | 491,012 |
| FCF simple | 1.037,934 | 1.525,603 |
| SBC en resultados | 1.001,357 | 1.244,004 |
| SBC capitalizada en software/activos | 45,912 | 65,324 |
| FCF menos ambas SBC, diagnóstico económico | −9,335 | 216,275 |
| Costes netos del incidente de julio incluidos en EBIT | 130,313 | 45,947 |
| Menor amortización de comisiones por cambio de vida útil | 0 | 53,400 |
| EBIT a política constante, excluido el incidente | −227,527 | −140,407 |

Ingresos crecen **24,3%**; CFO **45,2%**; FCF simple **47,0%**. La mejora es real. Sin embargo, 137,8 de los 224,9 de mejora de EBIT reportado se explican por menor coste neto del incidente y el cambio de vida útil de comisiones. La mejora restante bajo esa normalización concreta es 87,1. La normalización conserva SBC, amortización de intangibles y otros costes recurrentes. No convierte automáticamente todo ajuste no GAAP en beneficio económico.

El diagnóstico de caja después de SBC **no es FCFF normalizado completo**: incluye intereses, impuestos efectivos, anticipos y estacionalidad. Como control adicional, restando el ingreso financiero neto de gasto financiero a un impuesto normalizado del 21%, resulta aproximadamente **−142,2 / 92,6** para ambos TTM, antes de otros ajustes de circulante y costes excepcionales. Se utiliza interés contable como aproximación, no como dato exacto de cobro. La caja sostenible se modela mediante EBIT, impuestos, reinversión y circulante explícitos, no extrapolando el FCF publicado.

Fuentes primarias: [10-K FY26, estados y revisión trimestral](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000010/crwd-20260131.htm), [10-Q julio 2025, CFO y capex comparativos 2024](https://www.sec.gov/Archives/edgar/data/1535527/000153552725000025/crwd-20250731.htm), [10-Q julio 2026](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000031/crwd-20260731.htm), [resultados FY26, costes del incidente 2025/2026](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-fourth-quarter-and-fiscal-year-2026/), [resultados Q2 FY26, incidente H1 2024/2025](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-second-quarter-fiscal-year-2026-financial/), [resultados Q2 FY27](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000029/crwd-20260826xex991.htm).

Detalle reproducible de la revisión: H1 julio 2024 EBIT revisado = 12,525 + 4,745 = 17,270; atribuible = 45,880 + 40,629 = 86,509. SBC H1 2024 revisada = 384,002 originalmente publicada + 3,324 de corrección del EBIT = 387,326. H1 julio 2025 SBC revisada = 527,292. El fichero historical_bridge.json conserva cada periodo fuente y todas las fórmulas en history.py.

## 2. Cuatro trimestres, también en caja

| Trimestre | Ingresos | EBIT | Beneficio atribuible | CFO | Capex/software | FCF simple |
|---|---:|---:|---:|---:|---:|---:|
| Q3 FY26, octubre 2025 | 1.234,244 | −62,222 | −26,776 | 397,541 | 100,165 | 297,376 |
| Q4 FY26, enero 2026 | 1.305,375 | −6,900 | 38,691 | 497,869 | 119,720 | 378,149 |
| Q1 FY27, abril 2026 | 1.385,629 | −30,600 | 27,774 | 590,937 | 120,195 | 470,742 |
| Q2 FY27, julio 2026 | 1.470,897 | −33,232 | 5,306 | 530,268 | 150,932 | 379,336 |

La suma reproduce exactamente el TTM actual. Q3 caja = nueve meses menos seis meses; Q4 = año menos nueve meses; Q2 = seis meses menos Q1. Por eso una variación secuencial de caja no se interpreta como crecimiento estructural. Complementa, no reemplaza, las tres anualidades del informe original. Fuentes: 10-K y 10-Q julio citados; [10-Q octubre 2025](https://www.sec.gov/Archives/edgar/data/1535527/000153552725000033/crwd-20251031.htm), [10-Q abril 2026](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000025/crwd-20260430.htm).

## 3. SBC, inversión, dilución y capital

- El margen proyectado ya descuenta SBC recurrente. El modelo **no impone además dilución anual por esa misma remuneración**. Utilizar acciones diluidas iniciales cubre derechos existentes; puede haber una superposición menor entre premios pendientes y coste futuro estimado, no una duplicación de todo el gasto. Pasar a acciones emitidas elevaría aproximadamente 2,3% el valor.
- La SBC capitalizada se resta porque el capex pagado en efectivo la excluye. Añadir D&A y omitir esa inversión no monetaria regalaría parte del desarrollo tecnológico. La inversión neta en comisiones se calcula aparte de D&A porque la amortización de comisiones tiene su propia línea. No se resta de nuevo todo el gasto de comisiones.
- La D&A asumida del 5% inicial es inferior a la suma D&A/amortización adquirida de H1, aproximadamente 6,4% de ingresos. Es una sensibilidad legítima; por sí sola no explica una diferencia de siete veces. El beneficio de circulante negativo, −40% del incremento de ventas en el central, **favorece** el valor y no es una hipótesis especialmente pesimista.
- Puente de capital reproducido: caja 5.013,847, reserva operativa 600, inversiones 69,263, deuda nominal 750, minoritarios 37,801, reserva máxima de efectivo XM Cyber 145; neto 3.550,309. La caja restringida no se suma. Arrendamientos operativos se mantienen en gastos, no se descuentan además como deuda. La valoración de inversiones/minoritarios a valor contable y el precio no publicado de nuevas adquisiciones son incertidumbres pequeñas frente a la prima actual, aunque no se ocultan.
- Split 4:1 confirmado por el emisor: negociación ajustada desde el 2 de julio de 2026. La base utilizada es de 1.050,118 millones de acciones diluidas aproximadas y precio posterior al split, no 262 millones de acciones a precio posterior al split. [10-Q julio, nota de capital](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000031/crwd-20260731.htm).

## 4. Sensibilidades conjuntas adicionales

Se mantienen diez ejercicios de FCFF explícito y terminal con reinversión NOPAT × g/ROIC. No se reemplaza el modelo original.

| Supuesto conjunto | Valor por acción | Ingresos año 10 | Retorno implícito de empresa al precio actual* |
|---|---:|---:|---:|
| Central original | 33,86 | 20.930 | −12,3% |
| Favorable original | 81,86 | 31.030 | −3,6% |
| Crecer 30% cinco años, después 25/20/15/10/6%; margen final 35%; WACC 8,5%, g 3,5% | 140,33 | 44.820 | 2,0% |
| Crecer 25% diez años; margen final 32%; WACC 9%, g 3% | 129,39 | 55.890 | 1,6% |
| Crecer 25% diez años; margen final 35%; WACC 8,5%, g 3,5% | 164,97 | 55.890 | 4,0% |
| Crecer 30% diez años; margen final 35%; WACC 8,5%, g 3,5% | 239,21 | 82.730 | 8,2% |
| Reverse: crecer 30,31% diez años, mismo margen/tasas | 244,68 | aproximadamente 84.700 | 8,5% |

Los márgenes iniciales de esos nuevos escenarios suben de 10% hacia 32–35% después de SBC; no se obtiene un margen terminal extraordinario desde el primer año. El caso de 30% sostenido mantiene entradas importantes de capital circulante asociadas a ventas, por lo que ya incorpora financiación favorable del cliente. En el terminal se pasa a reinversión estable; ninguna senda explosiva continúa perpetuamente.

*IRR de los FCFF y valor terminal de cada escenario frente a precio × acciones diluidas menos puente neto de capital. El valor terminal de salida conserva WACC y g de ese escenario. No es una predicción exacta de rentabilidad del accionista ni suma dividendos a un FCFF ya distribuido; sirve para mostrar qué rendimiento ofrece cada combinación al precio vigente. La caja excedente se trata en el puente inicial. No debe interpretarse como objetivo anual garantizado.

Pruebas aisladas sobre central: eliminar SBC capitalizada eleva a **34,48**; eliminar toda inversión neta de comisiones, a **34,97**; bajar capex al 5% desde el primer año, a **35,35**. Incluso un margen artificialmente generoso, como si SBC no costase, de 25% inicial a 35% final, con crecimiento central, da **51,57**. Estas pruebas no recomiendan ignorar costes: muestran que la diferencia principal es duración y escala del crecimiento exigido, no una sola línea contable.

El WACC original es un supuesto de escenario explícito, no una estimación CAPM auditada. La ampliación a 8,5% comprueba un coste inferior. La ponderación del terminal central, 61,9%, es material y se revela; el terminal no usa crecimiento mayor que descuento. El resultado puede revisarse si se prueba expansión orgánica y monetización de IA muy superiores a la senda central. No se debe presentar una cifra puntual como certeza.

## Entregables y controles

Originales preservados. stress.py recalcula sin ejecutar la escritura del modelo original; stress_results.json contiene los años, hipótesis y retornos de cada escenario. history.py/historical_bridge.json documentan la historia y comprueban la suma de los cuatro trimestres. Anexo emitido para su incorporación visible al informe publicado y para ampliar la conclusión favorable, no para alterar precios o resultados sin aviso.
