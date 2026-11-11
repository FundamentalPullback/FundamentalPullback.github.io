# NXPI: el precio exige más que una recuperación normal

11 de noviembre de 2026. Corte de valoración: 10 de noviembre. USD millones salvo precio por acción. Extensión de A529, no sustitución de sus series históricas. **Modelo de diez años con fórmulas completas, pero análisis parcial de preselección (screen-grade); no valoración plenamente sustentada ni certificación de financiación, valor razonable o entrada.** Opportunity 90; $261,56 es la referencia del scanner del 10 de noviembre, ahora corroborada como cierre regular a las 16:00 EST por Stock Analysis, con corroboración en MarketWatch. Otros feeds muestran discrepancias: no mezclar históricos ni volúmenes entre proveedores.

## Hallazgo económico

La recuperación no basta por sí sola para justificar la referencia del scanner. Con reinversión financiada y SBC mantenido como coste, los escenarios ilustrativos producen aproximadamente **$65 adverso, $143 base y $261 favorable**. El favorable combina crecimiento elevado, margen GAAP de hasta 35%, menor coste de capital y mayor productividad del capital. No son probabilidades, objetivos aprobados ni un rango estadístico. El precio ya se aproxima al escenario favorable.

La valoración inversa exige un crecimiento de ventas cercano al **18,2% anual durante los primeros cinco años**, con márgenes, impuestos, eficiencia del capital y WACC del caso base. Las ventas llegarían a ~$33.008m en 2031 frente a la base estimada de $14.313m. La inversión requerida aumenta con las ventas; no se ha obtenido ese resultado congelando el capex. La hipótesis supera ampliamente el objetivo histórico de crecimiento 6–10% de la presentación de la compañía, cuyo horizonte y base son diferentes. No prueba que tal resultado sea imposible; identifica una exigencia que necesita evidencia nueva.

## Datos frente a supuestos

Datos primarios nuevos inspeccionados: 10-Q al 27/9/2026; presentación IR que incluye guía de Q4 2026; curva nominal del Treasury al 10/11/2026. Las fuentes originales se identifican en public_sources.json. La reconstrucción de tres ejercicios, cuatro trimestres y TTM se conserva en historical_reconstruction.md, actuals.csv y computed.json.

Base de ventas = 9M real $10.463m + Q4 guía media $3.850m = $14.313m. **No es FY2026 publicado.** El EBIT GAAP TTM excluyendo únicamente la ganancia MEMS es $3.921m, 28,42% de ventas. El margen Q3 es 32,44%. No se ajusta el impuesto histórico de la venta aplicando una tasa fiscal genérica; el modelo pronostica operaciones futuras sin repetir esa venta.

La guía histórica de margen 34–40% es no-GAAP. No se copia como GAAP: SBC cercano a 3% y amortizaciones siguen incluidos en el coste de explotación del modelo. Las previsiones de margen son hipótesis del analista apoyadas en el Q3 y en el rango operativo de la compañía, no orientación GAAP de diez años.

## Arquitectura reproducible

Ejecutar `python model.py` reconstruye assumptions.json, model_results.json y tres CSV anuales 2027–2036. FCFF = EBIT × (1−impuesto) + D&A − mantenimiento − capital de crecimiento − cambio de circulante − aportaciones a JV.

- Adverso: crecimiento −5%, 2%, 3%, 3%, 3%; margen 26–28%, impuesto 23%, WACC 11,5%, terminal g 2%, margen 27%, ROIC incremental terminal 12%.
- Base: crecimiento 8%, 7%, 6%, 5%, 5%; margen 31–32%, impuesto 20%, WACC 10,313%, terminal g 2,5%, margen 30%, ROIC incremental terminal 15%.
- Favorable: crecimiento 12%, 10%, 9%, 8%, 7%; margen 33–35%, impuesto 19%, WACC 9%, terminal g 3%, margen 33%, ROIC incremental terminal 18%.

En años 6–10 se reduce linealmente crecimiento, margen y productividad del capital hacia el terminal. Los valores presentes terminales representan 41%, 49% y 59% del valor operativo, respectivamente. No se añade múltiplo de salida.

D&A y mantenimiento se fijan ambos en 5% de ventas: no se concede un beneficio perpetuo por amortizaciones de adquisiciones sin coste de sustitución. El agregado incluye PP&E, software, tecnología y renovación de acceso a capacidad. **No es una estimación verificada de mantenimiento físico.** La evidencia 9M muestra D&A $555m (PP&E $346m, software $40m y otros intangibles $169m), frente a pagos de PP&E/intangibles $314m. La igualdad de mantenimiento y D&A es un supuesto simplificador que debe contrastarse, no una revelación de la empresa.

El presupuesto total de inversión de crecimiento es incremento positivo de ventas dividido por ventas/capital incremental (0,9/1,2/1,5). Incluye circulante al 16% del incremento de ventas y JV. El capital propio adicional es el remanente, nunca negativo. Cuando circulante más JV supera el presupuesto, se financia la cantidad superior. Así las aportaciones a JV **no se suman dos veces** a un presupuesto ya global. En contracción no se concede liberación automática de capital. Los coeficientes de capital son supuestos visibles; no estimaciones privadas ni ratios históricos verificados.

Como control de plausibilidad, capital contable consolidado inicial = patrimonio $12.465m + deuda contable $10.978m − caja $3.943m = $19.500m. El ROIC contable diagnóstico base llega a ~20,9% en 2031. Este indicador usa capital al cierre, no promedio, y no es ROIC económico auditado: incluye goodwill e inversiones sin separar y no capitaliza I+D. I+D permanece en gastos, no se agrega un activo ficticio ni se elimina el coste de investigación.

El terminal financia reinversión explícita = NOPAT del año 11 × g / ROIC incremental terminal. La productividad incremental converge a ROIC / margen NOPAT, haciendo coherentes crecimiento y financiación. El ROIC terminal es el de **nuevo capital**, no el retorno medio de todo el capital histórico.

## Fábricas, caja y reclamaciones

Los $916m pendientes se cargan una sola vez: $565m VSMC en 2027 y $351m ESMC repartidos en tres años. Es un calendario supuesto de modelización basado en plazos contractuales, no un calendario revelado de pagos. El modelo no añade $1.231m de valor contable de las JV al valor del negocio; tampoco capitaliza beneficios contables ni dividendos no documentados. El beneficio económico supuesto de acceso a suministro ya está en los márgenes y su financiación en inversión. Un dividendo independiente justificable sería un ajuste posterior, no una entrada gratuita.

Los $1.200m de capacidad VSMC ya pagados no se vuelven a deducir del puente de caja. Tampoco se añaden como un activo separado. Su reposición económica futura queda en el presupuesto de mantenimiento. El CFO histórico ya deduce los $345m pagados en 9M; el modelo empieza en NOPAT, no suma el CFO y esas partidas. Las compras mínimas de capacidad se tratan mediante costes/márgenes; no se descuenta todo el compromiso de ~$14.096m como deuda además de COGS. El caso adverso representa menor utilización, pero no sustituye un modelo contractual por fábrica.

Se parte de caja $3.943m y se retiene $1.000m como caja operativa, supuesto explícito. Deuda deducida = principal $11.039m, no deuda contable $10.978m. NCI económico = $1.000m, **supuesto**, no los $377m de patrimonio contable. Se compara con beneficio NCI de $41m en 9M, sin demostrar que sea una valoración conservadora, y reconoce que el 38,8% de SSMC no pertenece a NXPI. Incluye la reclamación sobre la caja de SSMC, de modo que no se deduce otra vez 38,8% de sus $316m. No se acredita el earn-out MEMS de $44m ni un valor de inversiones financieras, conservador y explícito. Cada $100m de ajuste neto al puente cambia aproximadamente $0,39 por acción.

Las rentas operativas permanecen como gasto operativo; no se añade deuda de leases por separado. Intereses e ingresos financieros quedan fuera de EBIT/FCFF y la deuda/caja se tratan en el puente. No se infieren compromisos actuales de Qualcomm de una operación histórica: no se encontró esa partida en el 10-Q revisado.

Denominador = 253,831m acciones diluidas medias Q3 como proxy supuesto, frente a 252,053m spot básicas al 24 de octubre. No se presenta como fully diluted actual. SBC permanece en EBIT; no se vuelve a restar en FCFF ni se proyecta dilución anual por el mismo coste. El proxy incluye adjudicaciones ya existentes; no se anticipan recompras autorizadas pero no realizadas.

Reloj: se descuentan los flujos de fin de año 2027–2036 desde el 10/11/2026, añadiendo 51/365 años de stub. Se supone FCFF cero durante ese stub y se mantiene el balance de septiembre. El balance del 27/9 tiene además un desfase retrospectivo de 44 días hasta la valoración del 10/11, distinto del stub prospectivo de 51 días hasta cierre de año. La reconciliación del balance y flujos desde el 27 de septiembre hasta diciembre sigue pendiente: esta aproximación no constituye un conjunto de supuestos demostrablemente conservador y es otra razón para no publicar un valor canónico.

## Coste de capital y sensibilidad

Treasury 10 años 4,98%, 10/11/2026, confirmado en la tabla primaria. ERP 5%, beta 1,25 y coste de deuda 6% son hipótesis de riesgo, no observaciones de mercado ni una regresión verificada. Capitalización de referencia = $261,56 × 253,831m; deuda principal $11.039m. Ke = 11,23%. WACC = E/(D+E) × Ke + D/(D+E) × 6% × (1−20%) = 10,313%.

Los cupones del 10-Q incluyen emisiones antiguas al 2,5–5,55% y un tramo EIB al 4,45%; no justifican usar el cupón medio como coste marginal actual. El 6% es una prima supuesta de ~102pb sobre Treasury, a validar con cotizaciones de deuda y pares. No se denomina WACC plenamente validado.

Con economía base y g 2,5%, el valor es ~$181 a WACC 9%, $151 al 10%, $128 al 11% y $111 al 12%. La matriz completa cruza WACC 9–12% con g 1,5–3,5%; en ese rango, el máximo es ~$195. El favorable de ~$261 cambia también crecimiento, márgenes y eficiencia del capital, no sólo el descuento.

## Gates y uso autorizado

El análisis es un avance económico material frente al anterior informe sin valoración: incluso un negocio que recupera margen puede no ofrecer colchón al precio del scanner. **No se aprueba compra, precio máximo ni tamaño.** Los campos canónicos de valor y entrada permanecen null.

Antes de certificar Stage 3: revisión independiente de fórmulas y fuentes; coherencia del histórico de precios entre proveedores; acciones spot diluidas reconciliadas; caja/deuda/NCI y stub actualizados; estimación mejor sustentada de mantenimiento, capacidad y retorno incremental; calibración externa de beta/ERP/spread y contraste homogéneo de pares (TXN/ADI/STM, con distinto fab mix y amortizaciones). No se inventa una tabla de múltiplos ni se declara completado el contraste. Stage 1/2 y señales técnicas no están certificados por este modelo.

## Fuentes primarias

- https://www.sec.gov/Archives/edgar/data/1413447/000141344726000059/nxpi-20260927.htm
- https://www.sec.gov/Archives/edgar/data/1413447/000141344726000057/nxp3q26exhibit991.htm
- https://investors.nxp.com/static-files/a9321248-f1b0-4cf8-a377-03893a4d2aca
- https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve

## Contraste posterior de mercado y beta

La página abierta de Stock Analysis identifica $261,56 como cierre del 10/11/2026 a las 16:00 EST, distinto de after-hours $263,40. MarketWatch también informa $261,56; Yahoo lo corrobora en el resultado indexado, pero su página devolvió 429 y no se usa como prueba única. ChartExchange y FT mostraron cierres diferentes; la referencia usada permanece identificada por proveedor, sin promediar cotizaciones.

Stock Analysis publica beta 5Y de 1,86, también visible en Yahoo. Esto es sustancialmente mayor que el supuesto de 1,25 del escenario base ilustrativo. **Por ello, 1,25 debe leerse como hipótesis benigna de normalización del riesgo, no beta actual verificada.** Con beta publicada 1,86 y los demás supuestos constantes, WACC sería 12,93% y la economía base valdría ~$97,06. Se conserva el caso de $143 para hacer visible la sensibilidad, no para presentar 10,31% como el único coste de capital defendible. La evidencia de mercado hace menos convincente, no más, una entrada a $261,56.

No se toman ratios contables del proveedor: su EBIT TTM $4,67bn no coincide con la reconstrucción primaria y sus $3,50bn de FCF no incluyen todo el capital industrial. Esta divergencia demuestra por qué el contraste de pares requiere normalización antes de usar múltiplos. El nuevo contraste está en provider_beta_stress.json.

Fuentes de mercado: https://stockanalysis.com/stocks/nxpi/statistics/ y https://www.marketwatch.com/data-news/nxp-semiconductors-n-v-stock-outperforms-competitors-on-strong-trading-day-cef4b897-4936be3cfd01 .

## Revisión independiente

La revisión independiente reprodujo escenarios, tablas anuales, WACC, valoración inversa, sensibilidades y estrés de beta sin diferencias materiales; también contrastó los puentes históricos con nuevas descargas primarias. Ese resultado valida las fórmulas y la trazabilidad revisada, no convierte los supuestos económicos en hechos ni certifica Stage 3. La corroboración del precio de mercado queda fuera del alcance independiente. Véanse independent_audit.md y sus archivos de cálculo.


La revisión independiente verificó fórmulas y puentes de fuentes primarias. No certificó por separado la corroboración de cotizaciones, que corresponde a la evidencia del autor. Estado parcial, sin valor canónico ni entrada aprobada.

Las fuentes descargadas de nuevo no se certifican idénticas en bytes a copias anteriores; public_sources.json distingue los hashes históricos de los nuevos.
