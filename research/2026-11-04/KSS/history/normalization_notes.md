# KSS: historia normalizada, corte financiero 1 agosto 2026

Importes en USD millones salvo EPS y acciones (millones). FY2025 acaba el 31 enero 2026; no confundir FY con año calendario. FY2023 tiene 53 semanas. La información del corte fue publicada posteriormente, hasta el 3 septiembre 2026: no es una simulación de información disponible el 1 agosto.

## Reproducibilidad y fuentes

Ejecutar `python rebuild.py` desde cualquier directorio. Sólo usa `inputs.json`, biblioteca estándar y archivos locales. Genera `normalized_history.json`, `normalized_history.csv`, `ttm_comparison.csv` y `qa.json`. No contiene filings completos ni requiere red. Cada input tiene URL HTTPS a filing primario o índice de accession y, para datos estructurados, tag y fecha de filing. Los inputs son extractos revisados de los documentos descargados por el equipo.

- [10-K FY2025](https://www.sec.gov/Archives/edgar/data/885639/000119312526115982/kss-20260131.htm): tres años, estado de flujos, PPE, leases.
- [10-Q Q3FY2025](https://www.sec.gov/Archives/edgar/data/885639/000119312525306677/kss-20251101.htm): Q3 y 9M, comparativos FY2024.
- [10-Q Q1FY2026](https://www.sec.gov/Archives/edgar/data/885639/000119312526257402/kss-20260502.htm).
- [10-Q Q2FY2026](https://www.sec.gov/Archives/edgar/data/885639/000119312526381893/kss-20260801.htm): Q2/H1, IEEPA, balance y flujos.
- [Release FY2025, 10 marzo 2026](https://www.sec.gov/Archives/edgar/data/885639/000119312526099319/d65722dex991.htm): EPS y acciones Q4 directamente publicados.
- [SEC companyfacts](https://data.sec.gov/api/xbrl/companyfacts/CIK0000885639.json): extractos históricos, incluido H1FY2024; URLs por accession en inputs.

## Convenciones

Revenue significa ingresos totales: net sales + other revenue; tag RevenueFromContractWithCustomerExcludingAssessedTax. Capex es PaymentsToAcquireProductiveAssets, sin netear ventas de activos. Los gastos de intereses están separados del interés pagado. CFO ya deduce intereses pagados y cash rent operativo; restarlos de nuevo duplicaría costes.

Q3 cash flow=9M−H1; Q4=FY−9M; Q2 cash flow=H1−Q1. TTM FY2026Q2=FY2025−H1FY2025+H1FY2026. TTM previo=FY2024−H1FY2024+H1FY2025. EPS y acciones ponderadas no se restan ni se suman para crear una supuesta cifra GAAP. Q4 NI 125 se confirma directamente en el release FY2025 del 10 marzo 2026 y coincide con 272−147. Ese release publica EPS diluido 1,07, EPS básico 1,11, acciones diluidas medias 117 millones y básicas 112 millones; se incorporan directamente, nunca por resta de promedios. El redondeo de los reportes puede producir diferencias de1 millón; por ejemplo, Q1FY2025+Q2FY2025 NI=-15+153=138 frente a H1 reportado139.

Se detectó que companyfacts asignaba a fechas de Q3 los cash flows de leases207 y principal57. La tabla del filing dice expresamente nueve meses: se corrigieron a9M antes de diferenciar. OtherNoncashIncomeExpense usa signo positivo para ingresos; se invirtió para reconciliar CFO. QA verifica identidades, sumas de cuatro trimestres y reconstrucción CFO (tolerancia1 millón).

## Resultados

| Periodo | Revenue | EBIT | NI | CFO | Capex | FCF simple | SBC |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2023 | 17.476 | 717 | 317 | 1.168 | 577 | 591 | 42 |
| FY2024 | 16.221 | 433 | 109 | 648 | 466 | 182 | 30 |
| FY2025 | 15.527 | 624 | 272 | 1.380 | 372 | 1.008 | 34 |
| Q3FY2025 | 3.575 | 73 | 8 | 124 | 108 | 16 | 9 |
| Q4FY2025 | 5.173 | 212 | 125 | 750 | 64 | 686 | 8 |
| Q1FY2026 | 3.167 | 46 | −14 | −74 | 84 | −158 | 9 |
| Q2FY2026 | 3.515 | 261 | 151 | 552 | 62 | 490 | 10 |
| TTM previo | 15.886 | 563 | 209 | 907 | 427 | 480 | 31 |
| TTM actual | 15.430 | 592 | 270 | 1.352 | 318 | 1.034 | 36 |

Revenue TTM cae2,87%. El aumento de FCF554 se divide en CFO+445 y menor capex109. La contribución de circulante (inventario, otros activos operativos, proveedores y accrued/otras liabilities; excluye variación de lease liability) pasa de−41 a357: mejora398. CFO antes de esa contribución pasa948→995, sólo+47. No concluir que los1.034 sean capacidad anual recurrente.

## Ajustes parciales de resultados y caja

Q2FY2026 EBIT261−beneficio IEEPA aproximado100=161. Q2FY2025 EBIT279−legal settlement129+charges11=161. Esto sólo normaliza esas partidas identificadas; no resuelve promociones, mix, vendor allowances ni otras diferencias de coste.

TTM EBIT592−100+charges4=496; el gain legal129 ya queda fuera del TTM actual porque se cancela al restar H1 previo. TTM previo EBIT563−legal gain129+charges87=521. Esta normalización parcial indica deterioro aproximado4,8%, frente a mejora GAAP5,2%. SBC sigue siendo coste: nunca se añade al EBIT normalizado.

El reembolso IEEPA recibido es aproximadamente150, mientras el beneficio de resultados es aproximadamente100. No convertir los50 restantes en inventario íntegramente: el filing describe también reparto con vendors e inversión en valor para clientes, sin desglose de cantidades. Los claims restantes son gain contingencies sin reconocimiento adicional. Restar150 de FCF reportado produce884 sólo como sensibilidad a cobros brutos, no FCF recurrente exacto; puede ignorar pagos asociados, impuestos y timing. No sumar mecánicamente ajustes de WC y refunds porque pueden solaparse.

## Puente FCF y tratamiento de leases/SBC

TTM: CFO1.352−capex318=FCF simple1.034. SBC36 se mantiene explícita: aproximación económica tras SBC998. Principal de finance leases y financing obligations81 (73+8) reduce FCF a953; proceeds de financing obligations son0 en TTM. Este es el equivalente TTM del adjusted FCF de la compañía. Interés pagado294, cash operating leases269, cash finance lease interest115 y cash financing obligation interest72 ya están en CFO. Las categorías de interés/lease pueden solaparse: no deben sumarse como nuevas deducciones.

Other investing es salida neta7 en H1FY2026 y15 en FY2025; TTM22. No está desagregada para poder concluir que es capex software. Si se incluye conservadoramente como inversión adicional, FCF1.012; tras SBC y principal leases/financing queda895. Es una sensibilidad separada, no métrica GAAP ni modelo de valoración.

El balance PPE incluye Information technology (coste778 al cierre FY2025,1.164 FY2024, vida3–5 años). No se publica aquí un capex software independiente. No sumar otra estimación de software sobre PPE, ni afirmar que es cero porque no tiene fila separada. La cantidad de Other investing no prueba qué parte corresponde a software.

## Escáner9,19 por acción

1.034/9,19 implica112,514 millones de acciones. Con Q2 diluidas reportadas118, la razón es8,76; con H1 diluidas117,8,84; con H1 básicas113,9,15. Sin el denominador exacto y fecha del escáner no puede certificarse9,19 como FCF por acción diluida. Todas son razones de FCF TTM contra denominadores de períodos específicos, no EPS GAAP. No se reconstruye una media diluida TTM desde medias anuales y H1.

## Límites

No es un modelo de valoración. No proyecta recuperación comercial ni convierte extraordinarios o releases de WC en perpetuidad. Las observaciones son a partir de los archivos aportados; los mínimos extractos históricos conservan trazabilidad, pero no incluyen documentos completos. Los flujos trimestrales derivados y los ajustes parcialmente normalizados están diferenciados de cifras directamente reportadas.
