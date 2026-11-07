# CXT, BLKB y YOU: revisión del escáner del 6 de noviembre de 2026

Precios facilitados por el escáner: CXT 57,57; BLKB 54,12; YOU 55,81 USD. Son referencias del escáner, no cotizaciones ejecutables. Horizonte de la tesis: 6–12 meses. Corte informativo: 6 de noviembre de 2026. Sin operaciones ni modificación de aprobaciones.

## Conclusión

**BLKB es la candidata relativa más interesante y su precio de 54,12 USD puede ser razonable bajo un coste de capital próximo al 8%.** Su negocio recurrente, mejora de costes y menor presión de renovaciones en 2027 ofrecen una tesis comprobable. SBC, software, impuestos y deuda reducen la aparente baratura del múltiplo ajustado, pero no la invalidan automáticamente. La prueba con operaciones centrales da 55,72 USD al 8% de WACC y 56,84 USD con una calibración ilustrativa de 7,918%. Falta cerrar esa calibración antes de recomendar una entrada. No hay una ganga demostrada ni un rechazo económico.

CXT sigue en observación: el trimestre confirma que la adquisición tapa debilidad orgánica en DTT. YOU tiene el crecimiento más fuerte, pero no el mejor precio frente a caja económica atribuible a A. Ninguna recibe aprobación nueva de Stage 3 ni Stage 3.5. Esta conclusión no exige una espera técnica universal de 15 minutos ni cambia el plan.

Orden útil: **BLKB como candidata condicional a precio razonable; CXT para vigilar recuperación orgánica; YOU para esperar reconciliación y mejor relación precio/valor.** Es orden de investigación, no ranking de compras aprobadas.

## BLKB: la apariencia de ganga necesita normalización

Q3: ventas 292,641 M USD, EBIT GAAP 59,951 M, EPS GAAP 1,02 frente a ajustado 1,36. La compañía mantiene guía 2026 de ventas 1.173–1.179 M, EBITDA ajustado 430–438 M, EPS ajustado 5,15–5,25 y FCF 280–290 M, esperando la mitad alta. El capex previsto de 60–70 M incluye 52–62 M de software. A 54,12, el PER ajustado de unas 10,4 veces es sólo un contraste, no beneficio económico normalizado. [Release Q3](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000029/blkbq32026exhibit991.htm).

### Caja reproducible

TTM = FY2025 − 9M2025 + 9M2026. USD millones:

| Concepto | FY2025 | 9M2025 | 9M2026 | TTM sep26 |
|---|---:|---:|---:|---:|
| Ventas | 1.128,365 | 833,109 | 864,378 | 1.159,634 |
| EBIT GAAP | 190,754 | 131,612 | 173,412 | 232,554 |
| CFO | 265,550 | 207,540 | 284,244 | 342,254 |
| Capex PPE | 7,767 | 4,805 | 7,320 | 10,282 |
| Software capitalizado de caja | 54,236 | 40,268 | 38,635 | 52,603 |
| FCF después de ambos capex | 203,547 | 162,467 | 238,289 | **279,369** |
| SBC añadida en cash flow | 92,910 | 71,079 | 67,682 | 89,513 |
| FCF menos esa SBC, diagnóstico | 110,637 | 91,388 | 170,607 | **189,856** |

El diagnóstico no es FCFF ni FCFE plenamente normalizado: faltan impuestos económicos, circulante sostenible y conciliación completa de premios. No se resta SBC de nuevo en el DCF, porque ya permanece dentro del EBIT. 9M2026 tiene 68,686 M de SBC en la conciliación de resultados frente a 67,682 M añadidos en CFO; no se fuerzan a coincidir. [10-K 2025](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm), [10-Q Q3](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm).

La caja corporativa es 35,734 M; los 428,166 M restringidos son caja de clientes, no excedente para accionistas. Deuda principal 1.046,494 M; deuda neta de toda la caja corporativa 1.010,760 M. La mejora de CFO incluye 18,6 M de mejor circulante interanual. El gross dollar retention ronda 90%; la empresa espera menos renovaciones expuestas en 2027. No se presume recuperación consumada. [10-Q Q3](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm).

Los impuestos de caja recientes se benefician de OBBBA y pérdidas fiscales; no son tasa perpetua. El 10-K prevé beneficios hasta 2027 y advierte que consumir créditos/pérdidas aumenta impuestos futuros. En 2025 FCF fue 203,5 M frente a 228,8 M en 2024; el salto actual necesita separar mejora real de calendario. [10-K 2025](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm).

### FCFF preliminar y revisión del coste de capital, sin aprobación

Modelo reproducible: value_blkb_model.py y value_blkb_model.json, en la misma carpeta de trabajo. Es una comprobación independiente, no un modelo histórico completo ni un precio objetivo certificado.

- Diez años: cinco detallados y cinco de transición. Ventas iniciales TTM 1.159,634 M.
- SBC y amortización permanecen en EBIT. D&A se añade una sola vez en caja.
- Central: crecimiento 4% los primeros cinco años, convergiendo a 2,5%; margen EBIT 20,5%→22%; impuesto 24,5%; capex 5,5% de ventas incluyendo software; D&A 7,2%→5,8%; circulante incremental cero. El crecimiento se supone principalmente de precio/productividad: si exige mayor inversión, el valor baja.
- D&A decrece para no perpetuar íntegramente amortización adquirida. El capex central del primer año es unos 66,3 M, dentro del orden de magnitud de la guía. La suficiencia del mantenimiento intangible necesita revisión.
- Terminal: reinversión = NOPAT × g / ROIC, ROIC central 15%. No se regala crecimiento terminal.
- Deuda 1.046,494 M; cero caja excedentaria por prudencia, reservando los 35,734 M operativos. Acciones 45,7 M: 44,979 M básicas de portada más aproximadamente 0,7 M de dilución de premios, aproximación por verificar. Sin recompras futuras gratuitas.
- El caso inicialmente llamado central usa WACC 9,5%; debe leerse como **operaciones centrales con descuento conservador**, no como coste de capital demostrado. No se impone una prima adicional por «prudencia» para rechazar la acción. El Treasury 10 años del 6 de noviembre fue 4,86%; beta observada 1,03 y una prima de mercado seleccionada de 4,5% implican coste propio 9,495%. Con deuda al coste medio publicado 5,63%, impuesto 24,5% y peso de deuda aproximadamente 30,1%, el WACC ilustrativo resulta 7,918%. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve), [beta observada](https://stockanalysis.com/stocks/blkb/), [deuda y acciones](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm).
- Esta calibración es preliminar: prima de mercado supuesta, coste medio de deuda distinto de coste marginal, beta dependiente de la ventana y pesos actuales distintos de pesos sostenibles tras desapalancamiento. Los pesos se calculan con 54,12 × 44,979 M de acciones básicas y deuda principal contable; por tanto, dependen del precio de referencia. No es correcto presentar ni 7,918% ni 9,5% como una verdad exacta; se muestra el impacto de ambos.

| Caso | Supuestos distintivos | Residuo por acción | Terminal/EV |
|---|---|---:|---:|
| Adverso | crecimiento 2%, margen 19%, WACC 10,5%, g 2%, ROIC 12% | 18,42 | 39,3% |
| Operaciones centrales, descuento conservador | crecimiento 4%, margen 22% final, WACC 9,5%, g 2,5%, ROIC 15% | 39,74 | 47,0% |
| Favorable | crecimiento 5,5%, margen 24% final, WACC 8,5%, g 3%, ROIC 18% | 67,63 | 55,7% |

### Sensibilidad decisiva: mismas operaciones, distinto WACC

No cambian crecimiento, márgenes, impuestos, reinversión, deuda ni acciones. g terminal permanece 2,5%. Son sensibilidades del valor presente, no objetivos de cotización futura a 6–12 meses.

| WACC | Valor por acción |
|---|---:|
| 7,0% | 72,15 |
| 7,5% | 63,12 |
| 8,0% | 55,72 |
| 8,5% | 49,53 |
| 9,0% | 44,27 |
| 9,5% | 39,74 |

**Tasa implícita aritmética para 54,12: aproximadamente 8,12% de WACC.** Es la raíz del modelo, no un umbral económico validado ni una condición automática de compra. El cálculo conserva las operaciones centrales; no exige el escenario favorable de crecimiento o margen. La calibración ilustrativa 7,918% da **56,84 USD**, aproximadamente 5,0% sobre el precio de referencia. No es un margen amplio, pero sí demuestra que el precio puede ser razonable sin hipótesis operativas extremas. El 7,5–8,0% da 55,72–63,12; no se afirma que cualquier tasa de esa zona esté ya validada.

La anterior sensibilidad acotada a WACC 8,5–10,5% y g 2–3% daba 31,33–52,17; era insuficiente para concluir rechazo, porque omitía costes de capital plausibles menores. Se conserva como escenario conservador, no como el rango total defendible. Dar crédito a toda la caja añade unos 0,78 por acción. Los escenarios no son probabilidades ni cotizaciones garantizadas. **Resultado: BLKB merece consideración condicional a precio razonable, pendiente de calibración y cierre del Stage 3; no aprobación automática ni rechazo económico.**

Catalizadores 6–12 meses: guía 2027 y evidencia de recuperación de retención, eficiencia de costes y monetización real de IA. Invalidación: retención que no mejora, más concesiones comerciales, ahorro de costes a costa de servicio, software/SBC crecientes, o caja sin reducción de deuda. No se ha verificado una fecha exacta para próximos resultados.

## CXT: Q3 no resuelve la objeción anterior

El expediente más reciente previo (A123, 30 de octubre) decía Stage 3 iniciado, no terminado. La antigua tabla A064 contenía 21/40/71 USD, pero su informe advertía que era un screening incompleto de cinco años. **No reutilizo 40 como valor vigente ni la etiqueta antigua de “Stage 3 completo” como aprobación.** [Decisiones públicas](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/data/dec.js).

Q3 ventas +11,7%, orgánicas +1,1%; SAT +7,2% orgánico, DTT −5,3%. EBIT GAAP 65,7 M frente a 81,9 M; ajustado EPS 1,28, sin crecimiento interanual. La guía de ventas baja de +15–17% a aproximadamente +14%, mientras EPS ajustado pasa a 4,32–4,42. No es un “beat and raise” operativo homogéneo. [Release Q3 del emisor](https://www.globenewswire.com/news-release/2026/11/04/3395864/0/en/crane-nxt-reports-third-quarter-2026-results.html).

Puente TTM: ventas 1.854,9 M, EBIT 236,4 M, CFO 290,3 M, capex 54,8 M y FCF 235,5 M. SBC añadida en CFO 26,5 M; diagnóstico FCF menos SBC 209,0 M. El salto trimestral de caja incluye 39,4 M de liberación de circulante. No extrapolar Q3 como cuatro trimestres iguales. [10-K 2025](https://www.sec.gov/Archives/edgar/data/25445/000002544526000009/cxt-20251231.htm), [10-Q Q3](https://www.sec.gov/Archives/edgar/data/25445/000002544526000049/cxt-20260930.htm).

Deuda contable 1.382,5 M y caja 251,1 M: neta 1.131,4 M, antes de 20,6 M de minoritarios rescatables y otras obligaciones. Antares añadió 50 M de ventas Q3, pero su EBIT fue −18,8 M, afectado por amortización/costes de adquisición. Hay además 36,1 M de valor razonable de premios Class B de ITT, sujetos a conversión y derechos de compra/venta. Deben conciliarse gasto, pasivo y pago sin deducción duplicada; no desaparecer bajo “ajustes de adquisición”. [10-Q Q3](https://www.sec.gov/Archives/edgar/data/25445/000002544526000049/cxt-20260930.htm).

A 57,57, unas 13,2 veces EPS ajustado no prueban infravaloración. Hace falta un modelo actualizado de Antares con inversión de mantenimiento, compensación, minoritarios y deuda; no se calcula un techo artificial para aprobarla. Catalizadores: recuperación de hardware/vending en CPI, sinergias reales y desapalancamiento. Invalidación: persiste caída orgánica, integración consume caja o compras nuevas impiden reducir riesgo.

## YOU: buen crecimiento, derechos económicos complejos

El dossier del 4 de noviembre sigue siendo investigación parcial sin valor total certificado. Sus casos condicionados fueron 14,90/33,12/63,95 USD; el 33,12 no es valor razonable aprobado. A 55,81, la caída desde el cierre del 4 de noviembre no resuelve el desfase con el central ni el puente de propiedad. [Dossier público](https://fundamentalpullback.github.io/research/2026-11-04/stocks/YOU.html).

Q3 ventas +27,8%, bookings +24,4% y CLEAR+ activos +14,5%. FCF trimestral −103,8 M incluye unos 315 M pagados por obligaciones de partnership ya devengadas contra ingresos. No se suman como “extraordinario” al TTM FCF de 458,037 M. El crecimiento de miembros totales no equivale a crecimiento de pagadores. [Release Q3](https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000053/clearq32026pressreleaseear.htm).

Caja y valores 632,969 M, sin deuda financiera dispuesta, pero no toda esa caja pertenece económicamente a A. Hay unas 131,298 M de unidades económicas básicas entre A y Alclear; TRA de matriz 267,786 M y RSU no vestidas 4,214 M. No dividir el FCF consolidado por sólo 102,719 M de acciones diluidas ponderadas A/B. Tampoco sumar DTA y ahorro fiscal futuro dos veces. El saldo de partnership de 83,639 M y el circulante de cobros anticipados requieren tratamiento económico. [10-Q Q3](https://ir.clearme.com/sec-filings/all-sec-filings/content/0001856314-26-000055/you-20260930.htm).

Catalizadores: retención pagadora, eGates y nuevos usos que aporten margen después de socios y SBC. Riesgos: economía de American Express/aeropuertos, TSA, costes comerciales, dilución y reparto matriz/Alclear. El dividendo de diciembre no sustituye esos catalizadores. Mantener observación.

## Alcance y controles

Fuentes recuperadas: repositorio público, 10-K/10-Q y resultados oficiales actuales. No se localizó un expediente previo específico de BLKB en los ficheros públicos examinados; no se hereda ninguna aprobación. CXT y YOU sí conservan sus antecedentes y límites.

Queda pendiente para un Stage 3 integral: historia trimestral completa conciliada, pares homogéneos, calibración de descuento y auditoría final del capital/inversión. El modelo BLKB muestra cuánto depende la conclusión de las obligaciones económicas y de un coste de capital correctamente calibrado. La revisión corrige la conclusión inicial demasiado dependiente del 9,5% discrecional. No certifica un precio objetivo ni añade un descuento de seguridad universal. Una mejora de cotización no sustituye resolver los pendientes.

