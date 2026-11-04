# GPC: historia financiera reproducible al 4 noviembre 2026

Importes en millones USD, salvo EPS diluido en USD/acción y acciones diluidas en millones. Fuentes primarias SEC, extraídas de 10-K FY2025/FY2024 y 10-Q Q1/Q2/Q3 2026 y Q3 2025. URLs exactas, concepto XBRL, periodo y fact_id están en los extractos numéricos y evidence.json. No se incluyen filings completos. La separación Automotive/Motion prevista para Q1 2027 aún no está cerrada: todos estos datos son consolidados históricos de GPC, no pro forma de dos negocios independientes.

## Reproducción offline

Ejecutar `python3 reproduce_history.py` (solo biblioteca estándar; no red). Regenera history.json, history.csv y evidence.json. Los tests comprueban ambos TTM: Q4 2024 + Q1/Q2/Q3 2025 = FY2024 + 9M2025 − 9M2024 y Q4 2025 + Q1/Q2/Q3 2026 = FY2025 + 9M2026 − 9M2025, en ventas, EBIT operativo, EBT+interés, CFO, capex, SBC, FCF y pagos de reestructuración. extract_facts.py es el extractor opcional para originales SEC descargados por separado; no hace falta para reproducir las cifras. manual_numeric_facts.json cubre celdas de interés neto visibles en tablas pero no etiquetadas iXBRL.

## Resultados principales

| Periodo | Ventas | EBIT operativo | CFO | Capex | FCF | SBC |
|---|---:|---:|---:|---:|---:|---:|
| FY2023 | 23,090.610 | 1,747.053 | 1,435.610 | 512.675 | 922.935 | 57.226 |
| FY2024 | 23,486.569 | 1,229.216 | 1,251.251 | 567.339 | 683.912 | 40.693 |
| FY2025 | 24,300.141 | 960.651 | 890.762 | 469.838 | 420.924 | 48.847 |
| TTM septiembre 2025 | 24,060.899 | 1,188.357 | 665.715 | 532.192 | 133.523 | 40.596 |
| TTM septiembre 2026 | 25,332.614 | 912.666 | 1,196.720 | 433.871 | 762.849 | 56.759 |

Los ocho trimestres comparables en CSV/JSON son Q4 2024–Q3 2025 frente Q4 2025–Q3 2026. El campo eps_diluted utiliza exclusivamente hechos directos EarningsPerShareDiluted para FY2023–2025 y Q1–Q3 de2025 y2026, con fact_id y URL en evidence.json. Q4 de ambos años queda null porque no se retuvo un hecho directo; ambos TTM quedan null al faltar ese cuarto trimestre directo. Por tanto la historia EPS es parcial, no completa. No se resta EPS anual menos 9M. Las acciones diluidas Q4 son una aproximación 4×FY−3×9M, explícitamente marcada, no peso diario exacto ni acciones spot para valoración. Los dos TTM no suman acciones medias y dejan diluted_shares null. No se calcula EPS TTM mediante resta de EPS ni se inventa un denominador. Los campos sin desgloses comparables continúan null, incluida amortización adquirida TTM.

## Definiciones y límites de normalización

- **EBIT operativo = gross profit − operating expenses**. No confundir con EBT+interés neto: FY2025 ambos son 960.651 y 215.674, respectivamente. El segundo incluye un cargo no operativo de liquidación de pensiones de 741.967 y otros gastos netos de 3.010. El EBIT operativo ya excluye ese cargo: añadirlo otra vez sería doble conteo. TTM EBIT operativo 912.666 versus EBT+interés 169.612.
- **FCF = CFO − capex**, antes de adquisiciones y después de intereses e impuestos pagados. No equivale a FCFF. FCF después de SBC = 706.090 TTM; es una sensibilidad conservadora del coste económico de compensación, no medida GAAP.
- **Factoring/A/R vendido:** 9M2026 ventas 7,201.058 menos cobros 6,951.071 = 249.987 de financiación neta dentro de CFO. 9M2025 equivalente 0.013; FY2025 0.005. TTM aporte 249.979. FCF TTM menos este incremento = **512.870**; menos SBC adicional = **456.111**. Mantener enfoque de flujos coherente con cualquier tratamiento de deuda del stock vendido. No restar todo el turnover anual. La financiación no debe contarse como mejora económica de conversión.
- **Supply-chain finance:** revisar con el análisis del balance; el aumento de obligaciones se refleja en AP. No añadir todo el stock como deuda y además restarlo del capital circulante sin reconciliación. Esta historia no hace ajuste arbitrario de CFO por todo el stock.
- **Reestructuración:** FY2024 213.520; FY2025 253.961; 9M2026 193.426 y TTM280.070. Es recurrente en varios periodos, por lo que no se añade automáticamente al beneficio sostenible. Pagos de reestructuración: FY2024 170.172; FY2025 235.804; 9M2026 176.256; TTM262.066. Están extraídos del total de la conciliación de reservas, no se confunde cargo contable con caja. Ausencia es null, no cero.
- **Separación:** Q3 2026 21.204; 9M2026 54.912 de costes antes de impuestos. No son adquisiciones. No convertir calendario objetivo en cierre realizado ni excluir des-sinergias futuras no publicadas.
- **Adquisiciones:** caja FY2023 306.881; FY2024 1,080.238; FY2025 318.291; TTM205.754. Está fuera del FCF definido arriba. No se mezcla caja de compra con gastos de integración. Q3 2026 disclose gastos de integración 0.803 y 9M6.092 mientras 6M publica cero: conservar los reportados sin fabricar asignación de los 5.289 restantes a un trimestre.
- **D&A:** FY2023 350.529; FY2024 407.978; FY2025 538.023; TTM575.329. Amortización de intangibles anual identificada: 147.000 (2023, fuente reciente redondeada),142.994 (2024),152.431 (2025). El nombre de campo acquired_intangible_amortization recoge la línea AmortizationOfIntangibleAssets, no demuestra que cada dólar corresponda exclusivamente a adquisiciones. No se encontró desglose trimestral/9M en estos 10-Q; null TTM, sin asignación proporcional ni adición de todo D&A como si fuera amortización adquirida.
- **SBC:** se usa el add-back exacto de estados de flujo, no el gasto redondeado de la nota; FY2025 48.847 versus nota allocated SBC47. No mezclarlos.
- **First Brands y pensiones:** el FY2025 incorpora una reserva First Brands de150.500 y el cargo de pensiones741.967. El cargo de pensiones se revierte en CFO; no es una salida equivalente de efectivo ni se debe sumar de nuevo al FCF. Separar reserva, efectos de cuentas por cobrar, amortización y caja antes de ajustar.

## Control de calidad

Los hechos repetidos se deduplican dentro de cada filing y se prioriza mayor precisión. Para cifras comparativas se utiliza el filing más reciente disponible. Los nulos identifican falta de cifra adecuada, no cero. Los resultados son historia financiera y puentes aritméticos, no DCF ni recomendación final de compra.
