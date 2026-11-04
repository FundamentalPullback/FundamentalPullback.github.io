# Bloom Energy: historia contable reproducible

Corte: 4 de noviembre de 2026. Importes en USD millones; EPS USD/acción; acciones en millones. Sin valoración. Fuentes primarias: formularios SEC 10-K/10-Q y comunicado Q4 2025, enlaces exactos en source_index.csv y cada input.

## Reproducir desde cualquier directorio

`python /ruta/history/rebuild_history.py`

Solo necesita numeric_inputs.json y el script, biblioteca estándar Python. No usa internet, pandas, companyfacts, filings completos ni archivos de otro directorio. `python /ruta/history/verify_offline.py` copia únicamente esos dos archivos a un temporal y comprueba igualdad binaria de nueve salidas; offline_reproduction.json registra resultado. Los documentos íntegros están fuera de esta carpeta y NO forman parte del paquete de historia.

## Cobertura y auditoría

- Tres ejercicios 2023–2025, trimestres 2024Q1–2026Q3, 9M2024–2026 y TTM a septiembre 2025/2026.
- Últimos cuatro trimestres: Q4 2025 y Q1–Q3 2026. Flujos trimestrales de CFO/capex/D&A se obtienen por resta YTD; TTM = FY anterior + 9M actual − 9M anterior. Cada derivación deja IDs y fórmula en ledger.csv.
- EPS y acciones no se restan ni suman. Q4 2025 y Q4 2024 son directos del comunicado; demás trimestres del 10-Q. EPS/shares TTM quedan nulos. NI diluido puede incorporar interés de convertibles, no usar NI común/acciones diluidas para reproducirlo automáticamente.
- CFO completo se reconstruye desde las filas firmadas de su estado, incluyendo capital circulante, otros activos a largo plazo y ajustes no monetarios. Cada componente `cf_bridge_` usa el signo mostrado, no el signo semántico XBRL. Categorías ausentes en un estado completo tienen cero explícitamente clasificado para evitar mezclar etiquetas antiguas/nuevas; la selección más reciente por periodo concilia exactamente. 95 comprobaciones contables pasan.
- La utilidad consolidada se mantiene separada de utilidad común y NCI. No confundir tax-equity/HLBV o pérdidas de afiliadas con resultado operativo. Beneficios de failed sale-and-leaseback y amortización de costes de deuda están identificados aparte.
- Deuda = recourse + nonrecourse al valor contable. Financing obligations se añade en columna distinta; no se confunde con VP de pagos contractuales ni con operating leases. Caja restringida separada, no neteada en net debt. NCI patrimonial no se trata como deuda.
- D&A de cash flow está rotulada “Depreciation and amortization”, aunque XBRL use “Depreciation”. Amortización de intangibles separada y software capitalizado separado: no divulgados por separado, nulos, nunca ceros inventados. PPE capex se resta una sola vez.
- SBC cashflow y SBC de resultados difieren por capitalización/reconocimiento. Warrants concedidos a cliente/cliente del cliente son contraprestación comercial separada, no SBC empleado ni capex efectivo. El proxy FCF post-SBC no equivale a owner earnings; no deduce automáticamente inversiones en afiliadas, distribuciones NCI o repagos de financing obligations.

## Alertas materiales

1. Q3 2026: CFO -27.147 y capex PPE 153.487; FCF PPE -180.634, frente EBIT GAAP 225.449 y NI común 250.271. La rentabilidad contable trimestral no se convierte en efectivo en ese trimestre.
2. TTM septiembre 2026: ingresos 3829.939; EBIT 567.405; CFO 690.968; capex 254.264; FCF PPE 436.704; SBC cashflow 200.454; proxy FCF post-SBC 236.250. Q4 2025 concentra CFO 418.073.
3. 9M2026: aumento contract assets consume 618.002; deferred revenue/customer deposits aportan 610.565. Otros activos no corrientes consumen 274.668. No igualar automáticamente variación de vendor advances en balance con consumo CFO: hay diferencias de clasificación y componentes de inversión.
4. MD&A Q3 2026 contiene descripciones de variaciones que no cuadran directamente con el estado de cash flow (deferred revenue/deposits y deferred costs). Se prioriza el estado contable y su conciliación; no se inventa ajuste y no se certifica explicación narrativa completa.
5. Comparativos EPS Q3/9M2024 en 10-Q Q3 2025 tienen escala iXBRL 3 errónea: valores mostrados -0.06/-0.59, corroborados en original 2024. Inputs usan EPS mostrado en USD/acción, no -60/-590. No es cambio económico.
6. Conflicts.csv conserva 17 comparaciones materiales: casi todas reclasificaciones de filas CFO/etiquetas (otros ajustes, venta-leaseback, extinción deuda y provisiones) que no cambian CFO total; una señal de signo del tag de sale-leaseback Q1 2025 se resuelve con comparativo posterior. El puente firmado es la referencia para impacto CFO.
7. Diferencias de redondeo de hasta USD 0.001m entre Q4 directo y FY−9M: NI común Q4 comunicado 1.091 frente resta 1.092, NI consolidado 1.425 frente 1.426; no se fuerza falsa exactitud. EPS Q4 directo es 0.00, no resta de EPS anuales.

Archivos: numeric_inputs.json (inputs numéricos reducidos con procedencia), history.json/csv, ledger.csv, source_index.csv, conflicts.csv, validation_checks.csv, qa_flags.csv, qa.txt, checksums.txt, script y verificador offline. El paquete no contiene recomendaciones de inversión ni series de precios.
