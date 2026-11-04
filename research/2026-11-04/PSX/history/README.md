# PSX: historial y normalización de ciclo
Corte: 4 noviembre 2026. USD millones, excepto EPS y márgenes por barril. Último 10-Q: trimestre terminado 30 septiembre, presentado 28 octubre 2026. Investigación, sin DCF ni recomendación de precio.

## Archivos reproducibles
`source_facts.json` contiene únicamente hechos seleccionados con período, unidad, segmento y URL SEC. `rebuild.py` usa sólo biblioteca estándar Python y esos datos para regenerar `financial_history.json/csv` y `segment_history.json/csv`; no requiere red ni filings completos. `normalization.json` contiene ajustes adicionales del emisor y hechos de comparabilidad. Los filings completos están fuera de este paquete, en el directorio privado de fuentes.

Las filas consolidadas cubren FY2023–2025, cuatro trimestres Q42025–Q32026, 9M2025/26 y TTM septiembre2025/26. Trimestres de cash flow = diferencias acumuladas. TTM = FY anterior menos 9M anterior más 9M actual. No se restan EPS acumulados porque el promedio de acciones cambia. Blancos significan no disponible, nunca cero. Los segmentos son resultados antes de impuestos, no ganancias netas ni necesariamente EBIT comparable de filiales consolidadas.

## Lo que dicen los números
- FY2023/24/25: NI atribuible 7.015 / 2.117 / 4.403; CFO 7.029 / 4.191 / 4.962; capex e inversiones 2.155 / 1.859 / 2.233. CFO menos capex 4.874 / 2.332 / 2.729.
- TTM Sep2026 vs Sep2025: NI 12.576 vs 1.505; CFO 15.028 vs 3.408; CFO excluyendo WC 13.245 vs 5.000; capex 2.670 vs 2.057; CFO menos capex 12.358 vs 1.351. No son flujos de ciclo medio.
- Q1/Q2/Q3 2026 CFO: -2.264 / 7.259 / 7.281. Excluyendo WC: 699 / 4.317 / 6.185. Q2 y Q3 incluyen liberación de WC de 2.942 y 1.096; no extrapolar. El efecto WC 9M2026 es +1.075 frente a -1.889 en 9M2025; TTM +1.783 frente a -1.592.
- Q3 EPS 14,08 y beneficio ajustado 5.619 prácticamente iguales al GAAP no significan normalidad. Refining aporta 6.031 de 7.108 de pretax consolidado; margen realizado 38$/bbl vs 24,08 Q2 y 10,88 FY2025. Márgenes FY2023/24 =17,26/8,84. No anualizar Q3 ni usar TTM como steady-state.

## Tres capas, no una única cifra «normalizada»
1. GAAP reportado: en las tablas, conserva todos los movimientos y cambios de perímetro.
2. Ajustado emisor: FY2025 NI2.632 vs GAAP4.403; FY2024 NI2.604 vs GAAP2.117; TTM Sep2026 ajustado10.609. Se eliminan partidas especiales pero persiste el ciclo. Ajustado2025 todavía incluye964 de depreciación acelerada LA. Pretax ajustado más LA acceleratedD&A =4.543 (2025), 3.638 (2024); esta conciliación tampoco es midcycle.
3. Midcycle analítico: recalcular throughput, margen realizado, mix, costes, turnarounds y capital de mantenimiento a perímetro comparable. El promedio simple histórico mezcla cierreLA, WRB y desinversiones de marketing. No se fija aquí una falsa precisión de EPS o FCF recurrente.

## WRB y Los Ángeles
WRB pasó del50% equity method al100% consolidado el1oct2025: la compra del50% restante requirió aproximadamente1.300 de efectivo, además de450 de deuda asumida y repagada. Ventas, costes, D&A, cash flow y capex cambian de base; separar crecimiento orgánico de incremento de participación. El impairment948 de Q32025 no es gasto operativo recurrente, pero tampoco un valor económico recuperable que sumar a equity.

LA cesó combustible Q42025. D&A acelerada964 en2025 y253 en2024; Q42025 incluyó239. Eliminar de earnings comparables no crea caja: CFO ya añade D&A. No añadirlo otra vez al FCF. Quedan obligaciones reales: ARO253 a dic2025, provisión groundwater69 y posibles costes de cierre/redevelopment. El gasto de cierre excepcional no justifica borrar sus pagos futuros. Al eliminar pérdidas de LA debe retirarse también capacidad/volumen/margen y sus necesidades de capital.

## Bridge de segmentos, intereses e impuestos
Sumar seis segmentos, incluido Corporate and Other, reproduce pretax; luego restar impuesto consolidado y NCI reproduce NI de PSX. Corporate incluye financiación: no llamarlo exclusivamente gastos de HQ. El agregado `pretax_plus_interest_includes_equity_income` es PBT más interés bruto, NO EBIT operativo puro: conserva ganancias de activos, otras rentas e ingresos de afiliadas. `pretax_plus_interest_ex_equity_income` retira los ingresos por equity method, pero aún precisa limpiar no recurrentes y otros ingresos para obtener NOPAT operativo.

No gravar dos veces beneficios ya netos de impuestos de una afiliada. Tampoco suponer que todo equity income de una LLC es aftertax para PSX: distinguir impuestos soportados por la JV, impuestos passthrough a PSX y retenciones. La tasa efectiva consolidada2025 fue16,46%, influida por partidas extraordinarias. Un bridge operativo debe aislar JV del NOPAT y calcular sólo impuestos incrementales soportados por PSX sobre sus cobros; un bridge de cash flow reportado ya incorpora impuestos consolidados.

Cash taxes FY2023/24/25 =1.397 /1.186 /200 frente a tax expense2.230 /500 /892. Los pagos federales2023/24 incluyen196/551 de compras de créditos IRA. No perpetuar la baja caja fiscal2025. Cash taxes interinos no separados en los hechos seleccionados; no inferirlos sólo de tax expense o deferred tax, porque taxes/accruals y otros movimientos difieren.

## JV/CPChem: ganancia contable no es distribución
Equity earnings totales FY2023/24/25 =2.017 /1.779 /762; distribuciones incluidas en CFO =1.195 /1.368 /882. 9M2026: earnings1.448, distribuciones496, diferencia952 retirada en CFO. 9M2025: earnings643, distribuciones783. TTM2026: earnings1.567 frente a dividendos595. Las devoluciones de capital de afiliadas se clasifican en inversión (TTM91), no automáticamente en cash flow recurrente.

CPChem es50% de PSX. Equity earnings atribuibles9M2026=828; segmentoChemicals829 (no exactamente idénticos). Su capex9M2026 a100%=787, partePSX394, autofinanciado; no está dentro de capexconsolidado1.988. Los dividendos específicos de CPChem no están separados en los estados PSX revisados: NO atribuirle todos los dividendos de afiliadas. ProyectosGTP/RasLaffan prevén operación plena2027, pudiendo absorber caja aunque haya equity income.

Dos métodos coherentes, nunca mezclados: (a) consolidado ex-equity income + cobros netos de JV después de contribuciones/impuestosPSX; no deducir otra vez capex ni deudaJV si se usa flujo/value de equity; (b) look-through proporcional de operaciones, capex, WC, impuestos y deudaJV, eliminando equity income y dividendos para evitar doble cuenta. Dividendos financieros no controlados requieren escenario propio, no payout100% por defecto.

## SBC y FCF
SBC FY2023/24/25=297/210/220. Es coste económico, no partida excepcional. Interim equity compensation movement no equivale a SBC expense. No inventar un TTM. En cash flow de accionista incluir coste de dilución o un ajuste consistente por SBC, sin simultáneamente descontar el mismo coste dos veces. `cfo_minus_capex` es residual de caja consolidado antes de adquisiciones y distribución a NCI, no FCFF unlevered ni cash distribuible íntegramente al común. Capex e inversiones incluye componentes de crecimiento; separar mantenimiento cuando haya fuente y no asumir que D&A es mantenimiento.
