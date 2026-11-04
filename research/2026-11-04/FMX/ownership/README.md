# FEMSA: propiedad y puente KOF / ex-KOF

Fecha de corte: 4 de noviembre de 2026. Estados más recientes: 30 de septiembre de 2026. Importes en millones de MXN salvo acciones, porcentajes y denominadores explícitos. Este paquete contiene inputs y controles; no es una valoración terminada.

## Archivos y reproducibilidad

- `ownership_minimal_inputs.json`: capital, clases, participaciones, convenciones y campos pendientes explícitamente nulos.
- `kof_ttm_inputs.csv`: FY 2025 + 9M 2026 − 9M 2025, separando datos IFRS/BMV y métricas de gestión.
- `kof_source_facts.csv`: hechos XBRL originales utilizados, con concepto, contexto y enlace.
- `capital_bridge.csv`: balances comparables. La diferencia simple de minoritarios o patrimonio atribuible **no** equivale a patrimonio ex-KOF.
- `QA_Flags.csv`: discrepancias y tratamiento requerido.
- `Validation_Checks.csv`: 15 comprobaciones aritméticas, todas satisfactorias.
- `source_index.json`: enlaces primarios. Los documentos íntegros y las imágenes originales quedan fuera de este paquete.
- `reproduce_offline.py`: reproducción pública autónoma con Python 3.9 o posterior y su biblioteca estándar. Ejecutar `python reproduce_offline.py` desde esta carpeta, o invocar el archivo desde cualquier directorio. Por defecto escribe en `reproduced/`; acepta `--input CARPETA` y `--output CARPETA`.
- Requiere únicamente estos diez archivos incluidos: `ownership_minimal_inputs.json`, `kof_source_facts.csv`, `kof_history_source_facts.csv`, `kof_ttm_inputs.csv`, `kof_history_3fy_quarters.csv`, `capital_bridge.csv`, `additional_equity_bridge.csv`, `kof_normalization_adjustments.csv`, `october_dividends_bridge.csv` y `QA_Flags.csv`.
- No descarga documentos, no accede a la red, no requiere los filings completos ni rutas de trabajo originales y no modifica los inputs. Recalcula TTM, cuatro trimestres por diferencia de acumulados, equivalencias de propiedad, diferencias de capital, dividendos y ajuste de seguros. Genera `Reproduction_Checks.csv` y `reproduction_report.json`, con hashes de los inputs y un código de salida no nulo ante inconsistencias.
- La reproducción comprueba aritmética y consistencia entre archivos; no revalida por sí misma fuentes, interpretaciones legales o hipótesis. Los riesgos cualitativos se conservan y los datos no verificados permanecen nulos. Los trimestres reportados y derivados siguen siendo series distintas.
- `public_files.json` enumera los archivos permitidos en la distribución pública. Las herramientas originales de extracción desde XBRL son un flujo separado y opcional, dependiente de los documentos fuente; no forman parte del paquete público ni son necesarias para reproducir los cálculos.

## 1. KOF: propiedad y equivalencia bursátil

FEMSA posee 7.936.628.152 acciones A sobre 16.806.658.096 acciones KOF: **47,2231189964% económico**, presentado como 47,2%. El voto publicado es 55,97%, aproximadamente 56%. Una unidad UBL contiene 3 B + 5 L; un ADS contiene 10 unidades, u 80 acciones. La participación equivale a **99.207.851,9 ADS** sobre 210.083.226,2 equivalentes totales. La fuente de cantidades es la nota 21 del [auditado KOF 2025](https://investors.coca-colafemsa.com/assets/files/reportes_resultados_en/2025/eeff-kof-2025-eng-1.pdf), pp. 80–83.

El [Exhibit 2.9 del 20-F KOF](https://www.sec.gov/Archives/edgar/data/910631/000162828026025313/exhibit29-descriptionofsec.htm), apartados Dividend Rights, Liquidation y ADS, establece igualdad de dividendos y distribuciones por acción plenamente pagada, sin preferencia por serie, e igualdad en liquidación. Por tanto, la conversión de la participación A al equivalente cotizado no necesita ponderación de dividendo. Los derechos de voto y transferencia difieren; no se añade una prima de control o descuento arbitrario. Si se utiliza valor bursátil de la participación, **no se vuelve a deducir la deuda KOF**.

## 2. FEMSA: denominador BD, no sólo unidades nominales

Al 30 de septiembre hay 1.417.048.500 unidades B y 1.968.615.615 BD en circulación: 3.385.664.115 en total. Emitidas 3.412.732.415 menos tesorería 27.068.300. Fuente: BMV Q3, nota de capital emitido, y [resultados FEMSA Q3](https://femsa.gcs-web.com/static-files/e56d3a69-ab40-4db7-ba22-8af9a2602dd7), p. 16.

Cada B contiene 5 acciones B; cada BD contiene 1 B + 4 D. Un ADS son 10 BD. Las D perciben el 125% del dividendo B en todos los dividendos mientras estén vigentes, sin acumulación. Así, BD representa 6 derechos B frente a 5 de una unidad B:

**ADS equivalentes para distribuciones = [BD + B × (5/6)] / 10 = 314.948.936,5.**

El denominador nominal es **338.566.411,5**. Mismo patrimonio dividido por el primero arroja un valor por ADS 7,50% mayor. No se trata del número real de ADR emitidos ni de acciones diluidas exactas. El [20-F FEMSA 2025](https://www.sec.gov/Archives/edgar/data/1061736/000162828026027231/fmx-20251231.htm), Dividend Rights y Liquidation, distingue el dividendo preferente de la igualdad de derechos por acción en liquidación. Para DCF de distribuciones continuas, usar la convención económica con sensibilidad nominal. Para una hipótesis de liquidación, conservar derechos nominales. No suponer que cualquier realización de activos se distribuirá mediante dividendos preferentes.

## 3. Capital: separación operativa y deuda de arrendamientos

Al 30 de septiembre, KOF tiene caja **46.772,350**, deuda de arrendamientos **3.978,038**, activos ROU **3.678,435**, patrimonio atribuible **151.080,058** y minoritarios propios **9.255,132**. La deuda financiera de gestión es 84.370; la nota BMV suma 84.368, diferencia de 2 que se conserva. La deuda neta publicada después de coberturas, 39.892, no equivale a deuda menos caja, 37.597,650. Fuente: [KOF Q3 2026](https://investors.coca-colafemsa.com/assets/files/reportes_trimestrales_esp/2026/coca-cola-femsa-results-3q26.pdf) y BMV, enlazado en el JSON.

FEMSA menos KOF da caja **64.290,710**, antes de las inversiones financieras separadas, y leases **110.839,547**. El emisor presenta ex-KOF caja más inversiones de aproximadamente **70.403**, deuda incluyendo leases **165.605** y deuda neta **95.203**. Si todas las rentas se consideran operativas, el puente aproximado es deuda financiera ex-KOF **54.765** y caja financiera neta **15.638**. Se deriva de cifras de gestión redondeadas y requiere respetar coberturas y perímetro de inversiones. Véase FEMSA Q3, pp. 3 y 14–15.

Reglas de modelo:

1. En convención de rentas operativas, deducir renta completa en el flujo, excluir D&A ROU del add-back y no volver a deducir deuda de leases.
2. En convención financiera IFRS 16, tratar leases de forma coherente en flujo y puente a equity.
3. Excluir dividendos KOF de la operación ex-KOF cuando se añade separadamente la participación bursátil.
4. Ajustar por separado eventos posteriores al trimestre. Estos balances no incorporan recompras y financiación posteriores.

## 4. KOF TTM: datos utilizables y límites

TTM calculado sobre periodos homogéneos:

| Métrica | TTM a septiembre 2026 |
|---|---:|
| Ingresos | 304.951,352 |
| EBIT calculado con serie BMV consistente | 44.706,809 |
| EBIT de gestión, redondeado | 45.277 |
| CFO | 45.077,937 |
| Capex bruto de caja PP&E + intangibles | 19.535,973 |
| Cobros por ventas/seguros de PP&E | 1.969,975 |
| D&A standalone | 14.847,269 |
| D&A ROU, redondeada | 1.130 |
| Principal de leases | 1.070,193 |
| Intereses pagados, incluyendo leases | 6.095,877 |
| Interés lease de gasto, no caja verificada | 465 |

**No mezclar el tag directo TTM de EBIT 45.276,689 con la serie FY + 9M − 9M:** aquel coincide con el perímetro de gestión, no con el mismo cálculo de los periodos IFRS/BMV. La serie de gestión procede de los [resultados KOF 4Q25](https://investors.coca-colafemsa.com/assets/files/reportes_trimestrales_en/2025/coca-cola-femsa-results-4q25.pdf) y Q3 2026.

**D&A de distinto perímetro:** FEMSA incluye rotura de botellas en D&A de su segmento KOF. FY 2025 registra 15.895 frente a 13.837,995 standalone. El ex-KOF FY 2025 correcto sobre esa base es 44.138 − 15.895 − (15.945 − 1.009) = **13.307 de D&A no ROU**. No quedó identificado el equivalente 9M de roturas, por lo que el TTM de D&A KOF dentro de FEMSA permanece nulo. Fuente: [auditado FEMSA 2025](https://annualreport.femsa.com/descargables/eng/Femsa_Estados_financieros_2025_eng.pdf), nota 28, p. 97.

**Caja de leases:** la línea BMV de FEMSA suma principal e interés; la de KOF sólo principal. KOF FY 2025 paga interés lease 375, frente a gasto 381. No llamar caja exacta al total TTM de nota 1.535; falta el desglose cash de los nueve meses. La aproximación debe declararse.

**Capex:** KOF 9M 2026 bruto 11.647,167 menos ventas/seguros 1.744,670 = 9.902,497, coherente con los 9.902 de caja neta publicada. No es una discrepancia inexplicable.

## 5. ImperialBrady y nuevos socios

La fusión cerró el 12 de marzo de 2026. La participación retenida es aproximadamente **18,75%** en el 20-F, redondeada a 19% en resultados. La nota BMV Q3 señala pérdida de influencia significativa y abandono del método de participación. No describirla como asociada equity-accounted actual.

El antiguo 37,08% de IFS TopCo valía en libros **14.192** al cierre de 2025. La ganancia extraordinaria no monetaria de fusión de 2026 es **11.952**. Ninguno de esos datos demuestra el valor actual de la nueva participación; **14.192 + 11.952 = 26.144 no es un carrying value actual verificado**. Los activos financieros no corrientes ex-KOF 30.899,215 están agrupados y no son una cotización de ImperialBrady. La valoración individual actual se conserva como **null**, no como cero económico. Fuentes: nota 10 del auditado FEMSA; 20-F 2025; nota de eventos significativos BMV Q3 y resultados Q3.

Las divisiones ex-KOF figuran al 100% en la tabla de filiales principales de 2025, pero esto no garantiza que todas sus subsidiarias lo estén. La JV Grupo Nós era 50%; tras la separación de febrero de 2026 FEMSA retuvo el 100% del negocio OXXO Brasil acordado. Además, [QED invirtió en el negocio de préstamos](https://www.femsa.com/en/press-room/press-release/qed-to-invest-in-femsas-lending-venture/) en junio de 2026: FEMSA conserva mayoría y consolidación, sin porcentaje minoritario o importe público verificado.

El residual contable aproximado de NCI fuera de KOF es:

88.993 − [9.255,132 + 151.080,058 × (1 − 47,2231189964%)] = **2,526**.

Es una conciliación de libros con redondeo y posibles ajustes de consolidación, **no** valor de mercado de minoritarios ni prueba de que QED tenga valor cero. No restar automáticamente 88.993 ni la diferencia simple FEMSA menos KOF standalone en una SOTP que ya valore por separado la participación KOF.

## 6. Revisión adicional del puente: beneficios, fiscalidad y ASR

`additional_equity_bridge.csv` conserva los tags y fuentes de estos ajustes. Estos cálculos también se verifican con `reproduce_offline.py`.

- **Beneficios postempleo y otros beneficios no corrientes netos:** 11.265,440 FEMSA − 5.719,002 KOF = **5.546,438 ex-KOF** a septiembre de 2026. Es candidato a pasivo similar a deuda si el DCF no incorpora financiación del déficit. Los activos de los planes ya se descuentan en la medición: no sumar otra vez los fondos suplementarios del XBRL como exceso de caja. Los auditados FEMSA, nota 17.2, y KOF, nota 15.2, establecen el tratamiento neto. Mantener el coste normal de servicio dentro de operaciones. No se asigna un beneficio fiscal adicional sin conciliarlo con el DCF.
- **Impuesto corriente pagadero a largo plazo:** **2.618,794 ex-KOF**, por diferencia de tags BMV. No está identificado separadamente como posición fiscal incierta. Se puede mostrar como sensibilidad de pasivo histórico si no se paga ya en los impuestos modelados. No tratar todos los impuestos corrientes o diferidos como deuda adicional.
- **Contingencias:** al cierre de 2025, litigios de pérdida posible, incluyendo posiciones fiscales inciertas, son 190.305 FEMSA y 186.532 KOF, diferencia 3.773. Son importes brutos de riesgo posible, no una provisión cierta y pagadera. No se verificó un pasivo incierto ex-KOF actual aislado. Fuentes: nota 26.7 FEMSA y 24.7 KOF. No convertir la diferencia en una deducción automática ni declarar que no hay riesgo fiscal.
- **ASR de septiembre:** el [6-K del 14 de septiembre de 2026](https://www.sec.gov/Archives/edgar/data/1061736/000162828026061700/a6kasrprsept2026.htm) anuncia hasta 280 millones USD, entrega al vencimiento y liquidación final prevista antes de finalizar 2026. No especifica un prepago o entrega inicial ya realizada. El estado de caja registra recompras totales de todos los programas de 10.431 en nueve meses frente a 5.369 en seis meses: **5.062 en Q3 ya descontados de la caja reportada**. Las notas muestran un incremento Q3 de 105.159.300 acciones constituyentes, equivalente a 21.031.860 BD; el perímetro es todas las recompras, no específicamente el nuevo ASR. La proximidad entre esos 5.062 y 280 millones USD no prueba asignación al ASR. No deducir automáticamente otros 280 millones USD ni reducir nuevamente acciones. Si se exige una sensibilidad de liquidación futura, ajustar conjuntamente caja y títulos con una hipótesis explícita. No confundir este contrato con el ASR de diciembre de 2025, que sí anunció una entrega inicial distinta.

## 7. Octubre: dividendos posteriores al balance

El [pago KOF del 13 de octubre](https://www.femsa.com/en/press-room/press-release/coca-cola-femsa-third-quarter-2026-results/) está confirmado: 0,241875 MXN por acción y 4.065,1 millones MXN de distribución total. Con las acciones publicadas, la salida calculada es **4.065,110427**, de la que FEMSA recibe **1.919,671934**.

Las [resoluciones FEMSA de marzo](https://femsa.gcs-web.com/static-files/5cb60cd8-228c-40a1-9a90-b083002aa66a) establecen para el 15 de octubre: 1,188 ordinario + 2,014925 extraordinario por BD, y 0,99 + 1,679125 por B. Total: **3,202925 por BD y 2,669125 por B**. Aplicado a las unidades en circulación de septiembre, la salida estimada es **10.087,607746**. El importe real depende de las unidades en la fecha de pago, todavía no conciliadas. La errata abreviada de 0,41975 por D en el comunicado Q1 no sustituye el 0,419775 de las resoluciones y el 20-F.

El puente parcial ex-KOF recibe 1.919,672 y paga aproximadamente 10.087,608: **−8.167,936 de caja**. No incluye generación operativa de octubre, nuevas recompras ni otros cambios desconocidos. La caja KOF de septiembre en un DCF independiente requiere descontar la salida completa, salvo que ya se haya deducido su dividendo a pagar. La cotización KOF de noviembre ya refleja el estado posterior al dividendo: no volver a descontarlo de una participación valorada a mercado. `october_dividends_bridge.csv` y el JSON separan hechos, cálculos y estimaciones.

## 8. Historial KOF de tres años y cuatro trimestres

`kof_history_3fy_quarters.csv` contiene FY 2023–2025, 9M comparables, 3M/6M de 2026 y los cuatro trimestres reconstruidos. `kof_history_source_facts.csv` conserva cada hecho, concepto, contexto y enlace BMV. Los estados Q1/Q2 fueron recuperados del índice primario BMV, completando el historial de caja trimestral.

Los ingresos/EBIT directamente reportados por trimestre pueden no coincidir con diferencias de acumulados de distintos informes. Por ejemplo, ingresos Q3 2026 directos son 79.718,215 frente a 80.037,127 por 9M menos 6M; EBIT es 11.739,930 frente a 11.761,749. Se conservan ambos, sin atribuir a una causa no verificada ni forzar el residuo a cero. La serie TTM del modelo usa uniformemente FY + 9M − 9M; los flujos trimestrales se reconstruyen por diferencia de acumulados.

La reproducción pública de este historial utiliza los hechos mínimos incluidos y `reproduce_offline.py`. Los extractores originales dependientes de filings no son una dependencia del paquete público.

## 9. Normalización de seguros KOF

`kof_normalization_adjustments.csv` conserva perímetros y diferencias. El EBIT IFRS-style incluye otros ingresos y gastos, donde el auditado clasifica recuperaciones de seguros. La identidad de 9M 2026 concilia: ingresos 227.189,853 − coste de ventas 120.815,396 − administración 11.941,770 − distribución 64.161,581 + otros ingresos 5.410,561 − otros gastos 4.436,301 = 31.245,366. Por tanto, elegir EBIT IFRS no elimina por sí mismo los seguros.

El [comunicado Q4 2025](https://investors.coca-colafemsa.com/assets/files/reportes_trimestrales_en/2025/coca-cola-femsa-results-4q25.pdf), p. 4, cifra el beneficio operativo neto de seguros del trimestre en **1.149**; el [Q3 2026](https://investors.coca-colafemsa.com/assets/files/reportes_trimestrales_esp/2026/coca-cola-femsa-results-3q26.pdf), p. 6, publica **1.313** para nueve meses. La deducción operativa TTM aproximada es **2.462**, no sólo los 1.055 del tercer trimestre. Aplicada al EBIT IFRS-style, deja **42.244,809**, o **41.839,809** tras añadir D&A ROU 1.130 y deducir renta aproximada 1.535.

La deducción es una **proxy explícita**, no una conciliación exacta de todos los extraordinarios IFRS: FY 2025 presenta beneficio de seguros de gestión 1.432 frente a 1.460 de la nota auditada de desastres, diferencia 28; 6M 2026 de 360 más Q3 de 1.055 suma 1.415, frente a 1.313 acumulado publicado, diferencia 102. Se conserva la cifra acumulada más reciente sin inventar una explicación.

La nota auditada 2.5 distingue recuperación reconocida 1.625, costes/bajas 165 y caja cobrada 814 en FY 2025. La nota 18 utiliza un perímetro más amplio de recuperación 1.882 y gastos de seguros 186. No intercambiar esos importes ni la línea de cobros por ventas/seguros de activos con beneficio neto. Las contingencias de FY 2025 tienen cancelaciones 684 y nuevas provisiones 921, gasto neto 237: no se añade automáticamente como extraordinario, pues existen cargos y liberaciones repetidos.

La reproducción pública del ajuste de seguros está integrada en `reproduce_offline.py`; no requiere ejecutar herramientas de extracción.
