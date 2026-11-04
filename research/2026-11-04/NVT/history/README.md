# NVT: historia financiera normalizada

Fecha de corte: 4 de noviembre de 2026. USD millones, salvo EPS en USD/acción y ratios. No contiene valoración, recomendación ni publicación.

## Entrega y reproducción

Ejecutar `python reproduce.py` dentro de esta carpeta. Solo usa la biblioteca estándar de Python y `numeric_ledger.json`; no requiere red, companyfacts completo ni documentos originales. Genera `history.json`, `history.csv`, `numeric_ledger.csv`, `derivation_audit.json` y `qa.json`.

- 3 ejercicios: 2023, 2024, 2025.
- Últimos 4 trimestres: Q4 2025 a Q3 2026; incluye los 4 comparables previos.
- TTM a 30 de septiembre de 2025 y 2026.
- Cada entrada numérica lleva período, unidad, tag, fecha de presentación, URL, ámbito y método. El registro de derivación identifica los componentes usados.
- Las cifras originales completas de SEC y el script inicial de selección quedan fuera de esta carpeta. No son dependencias de reproducción.

## Reglas contables

1. Ingresos, EBIT operativo, beneficio, impuesto y caja denominados `continuing` excluyen Thermal Management. Los ejercicios proceden de los comparativos recast del 10-K 2025. CFO y beneficio consolidados y discontinuados tienen columnas separadas. No se divide CFO consolidado por beneficio continuado como medida homogénea.
2. Los trimestres monetarios de caja se obtienen por diferencias de acumulados del mismo ámbito; Q4 por ejercicio menos nueve meses. Los EPS trimestrales son directos, incluyendo Q4 de la nota de resultados. TTM EPS queda nulo: no se calcula restando EPS anuales y acumulados.
3. FCF estricto = CFO continuado menos capex PPE continuado. La definición de FCF de la empresa añade cobros por venta de PPE. FCF después de SBC = FCF estricto menos SBC, una sensibilidad no GAAP, no otro flujo efectivo. Adquisiciones no son capex de mantenimiento.
4. D&A = depreciación más amortización de intangibles. Esta última no se añade otra vez a D&A. La separación adicional de amortización exclusivamente adquirida queda nula; no se presume que toda amortización sea eliminable. Capex de intangibles separado queda nulo, no cero: no está identificado como línea independiente en los estados seleccionados.
5. Balances son saldos de cierre consolidados, no sumas TTM. El perímetro de activos mantenidos para venta varía históricamente. Cash usa el tag actual que incluye restricted cash, cuya línea visible se denomina cash and cash equivalents; no suma efectivo dentro de activos mantenidos para venta. Por ello cash FY2023 recast es 179,6, frente a 185,1 de la presentación antigua. No aplicar indiscriminadamente retornos sobre activos a esta base histórica cambiante.
6. Deuda es valor contable de deuda corriente más no corriente, después de costes/descuentos. No equivale al nominal, no incluye todas las obligaciones tipo deuda y no constituye puente EV.
7. Selección más reciente por fecha exacta de período hasta el corte. La combinación de distintos documentos puede producir diferencias de redondeo de 0,1 M$. QA admite 0,11 M$, no exige precisión falsa. No se presenta esta tolerancia como una auditoría externa.

## Resultados principales

FY2023 / FY2024 / FY2025: ventas continuadas 2.668,9 / 3.006,1 / 3.893,1; EBIT 462,7 / 527,1 / 616,8; CFO continuado 422,2 / 501,0 / 649,0; FCF estricto 356,6 / 427,0 / 555,7.

TTM septiembre 2026: ventas 5.294,9; EBIT 942,5; beneficio continuado 674,4; CFO continuado 804,3; capex 131,3; FCF estricto 673,0; FCF de definición empresa 678,3; SBC 37,6; D&A 227,4. TTM previo: ventas 3.578,6; EBIT 570,1; beneficio continuado 296,2; CFO continuado 603,5; FCF estricto 520,4.

La comparabilidad es de clasificación continuada, no de perímetro constante ni beneficio recurrente: adquisiciones, impuestos y reembolsos arancelarios siguen importando. Ver `comparability.json`.

## QA

Se comprueban CFO y NI continuados + discontinuados frente a consolidados, beneficio antes de impuestos menos impuestos, activos contra pasivo + patrimonio, TTM contra suma de cuatro trimestres y presencia de EPS trimestrales directos. `qa.json` enumera cada control y todos los campos nulos. El archivo portable puede copiarse a una carpeta vacía con reproduce.py y regenerarse sin las fuentes completas.
