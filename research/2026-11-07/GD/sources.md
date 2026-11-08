# Fuentes públicas — GD
Recuperación: 8 de noviembre de 2026. Importes USD millones. Enlaces a los documentos públicos utilizados se enumeran abajo.

- S1. SEC, 10-K FY2025, tres ejercicios auditados: https://www.sec.gov/Archives/edgar/data/40533/000004053326000006/gd-20251231.htm — sources/10k_2025.html y .txt. Estados financieros, notas de arrendamientos, jubilación y contratos.
- S2. SEC, Q3 2025, comparativos de nueve meses 2024/2025: https://www.sec.gov/Archives/edgar/data/40533/000004053325000045/gd-20250928.htm — 10q_2025q3.
- S3. SEC, Q1 2026: https://www.sec.gov/Archives/edgar/data/40533/000004053326000012/gd-20260405.htm — 10q_2026q1.
- S4. SEC, Q2 2026: https://www.sec.gov/Archives/edgar/data/40533/000004053326000032/gd-20260705.htm — 10q_2026q2.
- S5. SEC, Q3 2026: https://www.sec.gov/Archives/edgar/data/40533/000004053326000038/gd-20261004.htm — 10q_2026q3. Balance, resultados, flujos, compromisos y contingencias, backlog y MD&A. Nota de contingencias: investigaciones de Electric Boat; no rango estimable. El litigio histórico de contratación laboral no se presenta como nueva reclamación pendiente.
- S6. SEC, comunicado Q3 del 30 de octubre: https://www.sec.gov/Archives/edgar/data/40533/000004053326000036/gd-20261004exhibit991.htm — q3_release. Alternativa primaria al sitio IR cuya descarga directa devolvió 403; no se reintentó el recurso denegado.
- S7. GD, dividendo: https://www.gd.com/Articles/2026/08/05/general-dynamics-board-declares-dividend — anuncio primario consultado en web; registro 9 de octubre, pago 13 de noviembre, 1,59 USD. Sin captura HTML local.
- S8. Cierre: https://stockanalysis.com/stocks/gd/history/ y https://www.quiverquant.com/stock/GD/historical-prices/ — secundarios corroborados, cierre regular 6 de noviembre 354,06 USD. No equivalen a nueva ejecución del scanner.
- S9. Damodaran ERP: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm — sources/erp.html. ERP implícita 1 de noviembre, 4,41%, variante trailing-12-month adjusted payout. Fecha distinta de la tasa Treasury actualizada.
- S10. Treasury 10Y, secundarios: https://ycharts.com/indicators/10_year_treasury_rate y https://apnews.com/article/bba6f0bf9035a6e6b1c4fef3e8230b89 — 4,86% el 6 de noviembre. Archivo Fed directo devolvió 403 y URL Treasury ensayada 404; no se afirma verificación primaria de esa sesión.
- S11. Beta histórica Yahoo: https://finance.yahoo.com/quote/GD/ — 5 años mensual 0,30, consulta 8 de noviembre. La beta modelada 1 y spread de deuda 100 pb son supuestos, no datos de esta fuente.
- S12. Comparables secundarios: https://stockanalysis.com/stocks/lmt/statistics/ ; https://stockanalysis.com/stocks/noc/statistics/ ; https://stockanalysis.com/stocks/hii/statistics/ — fuentes guardadas en market_web_capture.json, cotizaciones 6 de noviembre. Ratios agregados no normalizados.

## Reproducibilidad y límites
Ejecutar python model.py desde cualquier directorio genera results.json y financial_history.csv. Identidades de cuatro trimestres/TTM, FCFF y financiación terminal se verifican mediante assertions. Las hipótesis de crecimiento, inversión, capital circulante, tasas, ROIC terminal y proxies de obligaciones son del analista y no guidance del emisor. No se ha aprobado un valor ni imputado probabilidad al pasivo desconocido. Conservación del HTML permite verificar las cifras contra el texto primario; la conciliación exacta aparece en el modelo.

- S13. Verificación primaria independiente del Treasury a diez años, 6/11/2026: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve · 4,86%; captura en sources/independent_treasury_verification.json. Cierra el hueco primario indicado anteriormente en S10; no se reintentó el archivo Fed denegado.
