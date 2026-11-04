# Quanta Services (PWR): historial financiero reproducible

Fecha de corte: 4 de noviembre de 2026. Moneda: USD millones; EPS en USD/acción; acciones medias en millones; ratios y porcentajes según el nombre de la columna.

## Uso

Ejecutar `python rebuild_history.py` con Python 3, sin paquetes externos ni conexión a Internet. Solo necesita `numeric_inputs.json`, situado en esta misma carpeta. No depende de companyfacts, HTML, documentos SEC, otras carpetas ni del proceso de extracción. `python verify_offline.py` repite la ejecución en un directorio temporal que contiene únicamente esos dos archivos, bloquea la red y las lecturas fuera de dicho directorio y compara los resultados byte a byte.

Archivos de salida: `history.json`, `history.csv`, `ledger.csv`, `source_index.csv`, `validation_checks.csv`, `qa_flags.csv`, `conflicts.csv`, `qa.txt` y `checksums.txt`. Los hechos numéricos conservan URL, fecha de presentación, etiqueta original, periodo, escala, precisión y evidencia. El ledger registra cada dato o fórmula y sus dependencias; las etiquetas de hechos directos enlazan a los registros de `numeric_inputs.json`.

## Cobertura y método

- FY2023, FY2024 y FY2025.
- Q4 2024 y los cuatro trimestres de 2025; Q1–Q3 2026. Incluye los últimos cuatro trimestres y los cuatro comparables interanuales.
- 9M2025/2026 y TTM terminado en septiembre de 2025/2026.
- Los balances son fotografías a cierre, nunca sumas de trimestres. Todos los periodos mostrados tienen efectivo, deuda, activos, pasivos, patrimonio y minoritarios.
- Flujos trimestrales no publicados directamente: acumulado actual menos acumulado anterior. TTM: año anterior + nueve meses actuales − nueve meses anteriores.
- Q4 EPS básico/diluido y acciones medias son datos directos del comunicado de 19 de febrero de 2026, incluidos los comparativos de 2024. No se resta EPS anual y acumulado. EPS TTM queda nulo; la columna separada `eps_diluted_sum_quarters_calculated` suma cuatro EPS trimestrales directos y no representa un EPS TTM GAAP publicado. TTM septiembre de 2026 es 11,04 mediante esa suma, no 11,05 por restar EPS acumulados.
- Cuando una nota ofrece un flujo trimestral redondeado, se prefiere la diferencia exacta de acumulados si existe. Por ejemplo, recompras Q2 2025: 15,987 millones, frente a 16,0 millones redondeados en la nota.

## Bases que no deben mezclarse

**Beneficio y minoritarios.** En estos filings PWR, `ProfitLoss` es NI consolidado y `NetIncomeLoss` es NI atribuible a las acciones comunes. Se conserva también NI atribuible a minoritarios. CFO es consolidado; su conversión se compara con NI consolidado. Las distribuciones a minoritarios se muestran por separado. Los minoritarios permanentes son 86,186 millones al 30 de septiembre de 2026. No se encontró una línea separada de minoritarios redimibles o capital preferente: ambos campos quedan nulos, no se inventa cero. La identidad activos − pasivos − patrimonio total da cero en todos los balances cubiertos, pero no sustituye la revisión de términos contractuales de cada participación.

**Adquisiciones y perímetro.** Se adquirieron cinco negocios en 2023, ocho en 2024, ocho en 2025 y cinco en los primeros nueve meses de 2026. Los resultados se consolidan desde la adquisición. Cupertino Electric (2024), Dynamic Systems (2025), Tri-City, Wilson y Billings (Q4 2025) afectan la comparabilidad. El crecimiento total no es orgánico. Las cifras pro forma del note de adquisiciones son ilustrativas y se mantienen en notas separadas, no se combinan con el historial GAAP. La presentación por segmentos cambió a Electric y Underground and Infrastructure desde Q1 2025; aquí solo se normaliza el consolidado.

**FCF y reinversión.** FCF de la compañía resta capex PP&E neto de ventas de equipos y cobros de seguros. `fcf_gross_ppe` resta capex bruto y no suma esas ventas/cobros. Los proxies después de SBC no son owner earnings. FY2025 incluye además 103,370 millones de compra de activos (Billings), separados del capex PP&E y de adquisiciones de negocios. `asset_acquisitions_cash_separate` conserva ese gasto. En los estados interinos sin esa línea, cero significa que no se presenta un gasto separado y que todas las líneas de inversión concilian, no que se conozca el contenido de cada partida «Other, net». No se ha determinado capex de mantenimiento, capital circulante normalizado ni coste económico de dilución. Capex de software separado queda nulo y no debe contarse dos veces.

**Capital circulante.** CFO9M2026 de 2.940,929 millones incluye una aportación de 1.983,686 millones de pasivos de contratos, frente a 124,823 millones en 9M2025. Los usos de caja de cuentas por cobrar y activos de contrato también aumentaron. Se muestra el puente completo y la contribución neta de capital circulante; aislar solo los anticipos como sensibilidad no produce una estimación normalizada. No se debe anualizar mecánicamente el salto de CFO.

**Reclasificación de cash flow.** Estados anteriores separaban impuestos diferidos y ajustes de participadas dentro de las conciliaciones operativas; los nuevos los agrupan en «Other non-cash adjustments». La serie normalizada incluye todos esos componentes, conservando valor original y componentes en los inputs. 9M2024 ajustado a esta presentación es 1,725 millones, frente a −2,430 millones de la línea antigua más estrecha. No es un addback económico ni cambia el CFO reportado.

**Deuda y obligaciones.** La deuda corriente del balance incluye deuda a corto plazo cuando existe (8,710 millones a junio de 2026). El total de deuda a largo plazo de la nota no incluye esa deuda corta. La deuda corriente + no corriente incluye finance leases y operaciones de financiación de arrendamientos, y excluye arrendamientos operativos y contraprestaciones contingentes de adquisiciones. Estos compromisos quedan separados para no ocultarlos ni duplicarlos. Contraprestación contingente a septiembre de 2026: 837,380 millones. No se intenta valorar ni deducir otra vez minoritarios, earnouts u obligaciones en un puente de equity definitivo.

## Control de calidad y límites

Se verifican beneficio consolidado/atribuible/minoritarios, impuestos, balances, desglose de deuda, puente completo de CFO, cambio de efectivo, TTM contra cuatro trimestres y datos Q4 directos contra FY menos 9M cuando son aditivos. `validation_checks.csv` conserva cada comprobación; `qa.txt` da el recuento real. Las diferencias de presentación antiguas se armonizan explícitamente, no se suprimen como conflictos.

Los estados interinos y releases no están auditados. `qa_flags.csv` conserva las limitaciones y campos opcionales sin fuente. D&A, SBC, capex, CFO, ingresos, EBIT, ambos NI y EPS publicados tienen cobertura completa para los periodos requeridos. Las pruebas contables acreditan reproducibilidad y consistencia, no calidad económica del beneficio ni una valoración lista para invertir.

Scope clarification: working_capital_cash_contribution is an arithmetic grouping of changes in operating assets and liabilities in the cash-flow statement. It includes insurance and other non-current liabilities and other assets/liabilities; it is not pure current operating working capital.
