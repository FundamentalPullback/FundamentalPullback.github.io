# MAT y JAKK: comparables de HAS al 4 de noviembre de 2026

## Conclusión y límite temporal
- MAT aún NO había publicado Q3/9M26. IR confirmó publicación para 5 noviembre 2026, 16:05 ET. Se usa TTM junio 2026, no septiembre. JAKK sí publicó Q3 el 22 octubre y 10-Q el 27 octubre.
- Mismos criterios contables y fecha de precio, pero diferentes fechas de estados. No describir como panel plenamente homogéneo por fecha ni usar los dos múltiplos como precio objetivo de HAS/Magic.
- MAT: ventas TTM $5.489,929m, EBIT GAAP $429,097m, CFO $666,389m, capex $231,782m, SBC $74,002m; owner cash $360,605m. EV/EBIT 14,55x y owner cash yield 8,16%.
- JAKK: ventas TTM $627,250m, EBIT GAAP $23,052m, CFO $50,675m, capex $14,939m, SBC $11,903m; owner cash $23,833m. EV/EBIT 14,64x y owner cash yield 6,25% reportado. Sensibilidad conservadora ex cobro federal arancelario bruto + intereses: owner cash $12,733m, yield 3,34%. No es normalización fiscal exacta.

## Definiciones reproducibles
- Todas las magnitudes monetarias en USD millones salvo precio por acción. Acciones en millones.
- TTM = FY2025 + YTD2026 - YTD2025. YTD significa 6M para MAT, 9M para JAKK.
- EBIT = operating income GAAP, no EBITDA ni pretax+interés. Conserva SBC, amortización, reestructuración y costes de adquisición. No elimina cargos recurrentes por decisión discrecional.
- Owner cash = CFO - capex - SBC. CFO conserva impuestos, intereses y capital de trabajo. No es UFCF ni earnings normalizados. Restar SBC del CFO carga el coste económico de compensación que fue añadido de vuelta al CFO.
- Equity proxy = precio cierre 3 noviembre × media ponderada diluida del último trimestre disponible. NO es capitalización exacta de acciones en circulación al cierre ni fully diluted share count pro forma. La proxy cumple la convención solicitada. Para MAT es Q2, pues Q3 no existe al corte. En pérdida Q2, acciones potenciales antidilutivas quedan excluidas; evitar interpretar 288,930m como dilución plena económica. Recompras posteriores pueden cambiar la cifra.
- EV proxy = equity proxy + deuda financiera nominal - efectivo libre. No se suma pasivo de arrendamiento operativo (consistencia con EBIT después de alquiler), ni mínimos de royalties. JAKK restricted cash $1,133m se excluye del efectivo deducido. MAT deuda nominal $2.350m, no carrying value $2.333,9m.
- Yield sobre equity proxy, NO sobre EV. Usar EV en este denominador mezclaría flujo a equity con valor de empresa.
- MAT capex incluye compras de tools/dies/molds y other PP&E; software está en PP&E nota 5. No sumar otra vez software. Content assets spend ya está en CFO. Compra Mattel163 no se trata como mantenimiento/capex orgánico y no se descuenta en owner cash; adquisición crea cambio de perímetro y limita extrapolar TTM.
- JAKK capex es purchases of property and equipment ($13,226m 9M26; $7,850m 9M25). No confundir inversión total con capex: también incluye trust de remuneración diferida. No hay desembolso software separado en el estado de cash flows revisado.

## Aranceles: no confundir P&L con cash
JAKK reporta refunded tariff expenditure de $6,801m en reconciliación 9M26; está en other income, fuera de EBIT. No restarlo de operating income GAAP. El 10-Q describe $11,1m cobrados del gobierno federal por IEEPA e intereses, y una parte del reembolso aplicada al coste de inventario aún en mano a junio. El beneficio futuro al vender ese inventario no está separado; por eso NO se publica EBIT normalizado preciso. Para cash se muestra una sensibilidad restando los $11,1m completos, sin atribuir todos a beneficio económico ni aplicar tasa impositiva arbitraria. El flujo recurrente exacto requiere distinguir impuesto de caja, intereses, recuperaciones por cuenta de clientes e inventario. CFO también recibió devolución de income taxes, sin cuantía incremental separada en la discusión revisada.

MAT 10-Q Q2 dice que recibió devoluciones IEEPA no materiales y no reconoció receivable por adicionales no realizadas/realizables. No inventar un ajuste cuantitativo ni poner cero económico definitivo; el próximo Q3 puede alterar esto.

## Diferencias económicas relevantes frente a Magic (interpretación)
MAT es un propietario de marcas de juguetes con combinación de fabricación, licencias, retail y cada vez más gaming: Mattel163 se consolidó en 2026. JAKK es mucho más dependiente de licencias ajenas/productos físicos, taquilla, calendario de lanzamientos y disfraces Halloween. En 9M26 pagó royalties reconocidos por $81,272m (16,25% ventas); los mínimos futuros contractuales eran $170,0m, de ellos $57,4m próximos 12 meses, fuera de deuda financiera. El margen EBIT TTM JAKK 3,68% y MAT 7,82% no representa economía de una franquicia de cartas con base instalada/coleccionismo/lanzamientos como Magic. Son contraste del negocio juguetero y disciplina de valoración, no peers puros de Wizards. Evitar inferir una prima concreta sin evidencia del segmento HAS.

JAKK tiene estacionalidad fuerte: ventas altas Q2/Q3 y cobro Q4/Q1; no anualizar Q3. Su 9M26 crece 12,8% contra 2025 pero queda 10,7% debajo de 9M24 ($560,301m), señal de comparación deprimida. El crecimiento de Action Play se atribuye a Super Mario Movie en el 10-Q.

## Fuente de precios y discrepancia resuelta
MAT $15,29: cierre 3 nov en StockAnalysis, corroborado por ChartExchange/FinanceCharts. JAKK $31,65: tabla HTML descargada de ChartExchange y cierre Marketbeat/YCharts. El primer resultado indexado ChartExchange devolvió $31,62 y hora 15:59:58; la página actual descargada indica $31,65. Se usa el cierre actualizado, no snapshot previo. Conservar la advertencia de dependencia de proveedor, sin precisión espuria por variaciones menores de volumen.

## Archivos
`reproduce.py` genera offline `inputs.json`, `bridge.csv`, `results.json` y `results.csv`, sin red ni librerías externas. Los HTML/PDF y TXT son snapshots públicos descargados el 4 noviembre 2026. `sources.csv` documenta URL y uso; `sha256.txt` verifica integridad. Valores transcritos de estados, no estimaciones de consenso. Nada se ha publicado ni editado en modelo HAS.
