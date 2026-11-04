# FEMSA / FMX: historial financiero y normalización de caja
Corte: 4 de noviembre de 2026. **MXN millones**, excepto EPS y número de acciones/unidades. Sin DCF ni recomendación de compra.

## Resultado útil
- Hay estados primarios suficientes: auditados 2025 con 2023–25 y XBRL BMV de Q1/Q2/Q3 2026, Q3 2025 y FY2024/FY2025. No existe la antigua brecha documental de CFO.
- El CFO BMV de 9M2026, 88.749,884, aumenta 77,6%. La reversión de cinco movimientos de circulante (21.655,897) y menores impuestos pagados (7.839) explican **76,07% de la mejora**. El diagnóstico antes de ambos crece 11,09%, no 77,6%.
- Consolidado TTM por FY2025 + 9M2026 − 9M2025: ingresos 894.726,716; EBIT de gestión 77.894; D&A de flujos 46.031; CFO BMV 109.852,734; compras PPE+intangibles 37.033; cash rent 24.458; impuestos pagados 19.235. EBIT + D&A − cash rent = **99.467**, una medida previa a impuestos, circulante y capex, no FCFF ni flujo atribuible a FEMSA.
- CFO menos compras PPE/intangibles, cash rent e interés financiero separado =39.657,734 TTM. Es un residuo consolidado histórico; no caja sostenible, no FCFF y no valor disponible íntegramente para FMX.

## Archivos y reconstrucción
Ejecutar `python build_history.py` con Python estándar. No requiere internet, paquetes, PDF, ZIP ni filings completos. Usa `selected_primary_bmv_facts.json` y `manual_primary_inputs.json`. `make_manual_inputs.py` permite regenerar el segundo a partir de su transcripción revisada.

- `history_wide.csv/json`: 3 FY, periodos interinos, cuatro trimestres individuales según emisor, trimestres residuales por diferencia, TTM actual/anterior.
- `history_long.csv/json`: cifras, unidades, fuente, localizador y etiqueta de evidencia.
- `analytics.json`: puentes y cálculos del diagnóstico.
- `validation_checks.csv/json`: comprobaciones numéricas reproducibles; resultados no reemplazan las salvedades materiales.
- `source_index.csv/json`: enlaces y fechas de las fuentes primarias.
- `normalization_issues.csv/json`: excepciones que condicionan uso de cifras.
- `ex_kof_da_bridge.json`: puente comparable anual con KOF dentro de FEMSA. Los datos standalone KOF no son intercambiables sin reconciliación.

Las copias completas descargadas permanecen en la carpeta de investigación `sources`; **no forman parte del paquete offline entregable**. `extract_bmv_facts.py` es opcional para una reextracción de esos originales.

## Convención y perímetro
**Rentas operativas:** cash rent se descuenta del flujo; la deuda por leases no vuelve a restarse del equity bridge. EBIT IFRS contiene depreciación ROU; se puede sumar ROU y restar cash rent para formar EBIT después de rentas, añadiendo después sólo D&A no-ROU. La identidad equivalente de caja es EBIT + D&A total − cash rent. Impuestos deben aplicarse a una base operativa apropiada; no se aplica un porcentaje arbitrario a EBITDA.

En FEMSA, BMV `PaymentsOfLeaseLiabilitiesClassifiedAsFinancingActivities` **incluye principal e interés**. Lo prueba FY2025: 24.061 =15.791+8.270, igual a nota12. FY2024: 19.675 =12.122+7.553. 9M2026:17.795 y9M2025:17.398 son el agregado, no principal puro. El interés financiero separado de6.487/6.570 no se debe confundir con interés lease. El split interino FEMSA no está desglosado, queda null.

**La convención KOF es distinta:** su tag de pagos lease es principal, y su interés financiero incluye interés lease. Usar la conciliación KOF del trabajo de ownership; no restar tags homónimos automáticamente.

FEMSA consolida100% KOF con47,2% de propiedad económica nominal y56% de voto. Hay que quitar KOF del flujo antes de añadir su participación accionaria, o deducir adecuadamente minoritarios en una valoración consolidada. Los dividendos KOF incluidos en el EBITDA de apalancamiento exKOF del emisor no se capitalizan otra vez al añadir el valor de la participación.

## Puentes materiales
1. **EBIT:** XBRL YTD `ProfitLossFromOperatingActivities` incluye otros ingresos/gastos amplios, incluida la ganancia ImperialBrady. 9M2026 es63.894,770 contra EBIT de gestión53.365. No se carga ese tag como EBIT operativo limpio. Además, el tag TTM cambia de base; la serie operativa se deriva de los EBIT de gestión con sus fuentes.
2. **D&A y otras partidas no caja:** IR9M2026 presenta31.979 depreciación +10.998 amortización/otros =42.977; el ajuste D&A de CFO es34.915. Los8.062 restantes no se tratan como depreciación recurrente ni se capitalizan como FCF. SBC auditado2023/24/25:943/947/1.100. El cero del tag de addback de SBC no demuestra gasto cero; el gasto interino queda desconocido.
3. **Bottle breakage:** nota28 FEMSAFY2025 D&A KOF15.895 incluye rotura de botellas, frente a D&A standaloneKOF13.838. Restar el segundo de FEMSA sobrestima D&A exKOF en2.057. D&A exKOF comparableFY2025=28.243, menos ROUexKOF14.936, produce **D&A noROU exKOF13.307**, 2,423% de ventas exKOF549.208. TTM requiere puente equivalente de rotura; no interpolar sin etiquetarlo.
4. **CFO anual comparativo:** auditFY2025 CFO2024=71.510 y2023=49.679; BMV=65.130,551 y54.377,685. El puente algebraico coincide dentro de1 M MXN: 2024 auditCFO −6.080 CFI discontinuadas −1.276 CFF discontinuadas +977 caja de discontinuadas ≈65.131; 2023 auditCFO +25.426 CFI discontinuadas −20.727 CFF discontinuadas ≈54.378. Esto respalda una reclasificación de presentación, no crecimiento de CFO. Mantener ambas series; no mezclar bases sin ese puente. El origen de la reclasificación es una inferencia de la conciliación, no una afirmación textual del emisor.
5. **Capex completo:** PPE+intangibles es el mínimo de inversión de caja, sin netear ventas de activos ni seguros. En TTM suma37.033; el tag de compras de otros activos a largo plazo añade733,769 y da37.766,769. No se ha determinado cuánto es capex económico versus otra inversión. Capex gerencialTTM38.676 usa otra definición/timing. Adquisiciones y JV están aparte. La diferencia de cash acquisitions FY−9M+9M es−118, no una adquisición negativa económica: se bloquea su uso sin aclarar reclasificaciones.
6. **Ganancia ImperialBrady:** 37.456−11.952=25.504 consolidado9M2026. No tuvo impuesto corriente. Tasa del emisor exganancia:13.656/(51.167−11.952)=34,82%. No equivale a flujo de caja, ni beneficio atribuible normalizado, ni tasa fiscal exKOF. El crecimiento declarado12,1% no concilia con25.504/20.359−1=25,27%; no se reproduce como comparación verificada.
7. **Períodos y revisiones:** los cuatro trimestres individuales publicados no suman exactamente los acumulados posteriores por revisiones/presentación. Se preservan los dos. Por ejemplo EBITQ4FY2025 publicado24.546 contra residuoFY2025−9M2025 de24.529. Las diferencias no se esconden como redondeo.
8. **NI y EPS:** para NI atribuible TTM usar la pareja directamente reportada en Q3BMV2026:35.709,642 y17.717,532. El TTM previo derivado conFY2024 auditado y9M2024 de versión anterior da16.286,724 y no es comparable. No utilizar esa deriva para crecimiento. EPS genérico XBRL cambia entre entregas; se preservan EPS anuales por B/D y EPS proforma del emisor por total unidades, sin llamarlo GAAP diluted ADS EPS.
9. **ADS:** 1ADS=10unidadesBD, cadaBD=1B+2DB+2DL. UnaunidadB contiene5B. Derechos D125% frente aB100%; totalunidadesB+BD dividido10 es un proxy, no el denominador económico exacto. Para equityvaluation consultar el puente de clases en ownership: (BD + B×5/6)/10; no confundir con ADS cotizados ni convertir acciones constituyentes÷10.

## Alcance cargable
Ingresos, estados auditados, caja BMV con convención documentada, circulante, impuestos, compras PPE/intangibles y cash rent son trazables. Las líneas con `null` están ausentes, no valen cero. Los EBIT de gestión son cifras reportadas del emisor, no garantía de recurrencia. La normalización deja fuera ganancias extraordinarias y evita anualizar la mejora de circulante, pero **no impone una hipótesis de FCF sostenible**: eso corresponde al modelo posterior, con supuestos explícitos.

## Actualización Spin: fondos de clientes
Los estados regulatorios de Compropago al30sep2026, autorizados el31oct2026, identifican4.781,191 M MXN de fondos electrónicos exigibles de clientes y92,017 de cuenta global inactiva: **4.873,208 M MXN en total**. Activos:293,529 de efectivo y4.485,744 de reportos. La política exige separar fondos de clientes de recursos propios. Estos activos de respaldo no son caja excedente distribuible a FMX. El mapeo con la caja/inversiones IFRS de FEMSA todavía no se concilió: no deducir mecánicamente el pasivo si los activos ya fueron excluidos. Fuente, unidades, fechas y localizadores en `spin_customer_funds.json`.

## Ancla exKOF comparable
`ex_kof_operating_comparison.json`: TTMseptiembre2026 frente aTTMseptiembre2025, por sustracción consistente de KOF de FEMSA:
- Ingresos589.775,364 frente a539.664,863, +9,29%.
- EBIT de gestión32.617 frente a30.781, +5,96%.
- PPE de caja16.659,428 frente a18.137,221; más intangibles837,599 frente a2.357,073.
- PPE+intangibles de caja17.497,027 frente a20.494,294, −14,62%. Bruto antes de seguros/ventas; sin compras de negocios ni leases.
La resta conserva el residual de eliminaciones de consolidación; no se presenta como un estado legal independiente de Retail.
