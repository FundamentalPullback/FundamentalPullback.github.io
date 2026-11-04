# Macy’s (M): comparable operativo de KSS, no múltiplo objetivo
Corte: 4 noviembre 2026. Millones USD salvo precio/acciones. Fuentes primarias para fundamentales. **Excluir de mediana objetivo: no se logró homogeneizar renta cash TTM.**

## Precio y capital
Cierre regular **$25.69**, 4-nov-2026 16:00 EST, separado del after-hours $25.64. [StockAnalysis / S&P Global](https://stockanalysis.com/stocks/m/history/). La observación Stocknear $25.70 a 15:59 se descarta por anterior al cierre.

Balance 1-ago-2026: cash $1,294; deuda financiera en libros $2,433; ABL dispuesto cero. Acciones reales **261,176,646 a 29-ago-2026**, no el promedio diluido trimestral 271.9m. Capitalización con esas acciones $6,709.6m y EV **excluyendo todos los leases** $7,848.6m. No son acciones/caja de noviembre. Lease liabilities no corrientes $2,656m no equivalen a total. [10-Q, portada y pp. 5, 11, 14–15](https://www.sec.gov/Archives/edgar/data/794367/000162828026061320/m-20260801.htm).

## Puente TTM reproducible
FY25 + H1-26 − H1-25, final 1-ago-2026:

| Variable | FY25 | H1-26 | H1-25 | TTM |
|---|---:|---:|---:|---:|
| Net sales | 21,764 | 9,548 | 9,411 | 21,901 |
| Total revenue | 22,621 | 9,951 | 9,791 | 22,781 |
| Operating income | 1,030 | 356 | 242 | 1,144 |
| Ganancias inmobiliarias | 48 | 23 | 32 | 39 |
| Impairment/restructuring expense (beneficio negativo) | 230 | -1 | 30 | 199 |
| Interchange settlement gain | 328 | 0 | 0 | 328 |
| D&A | 894 | 416 | 437 | 873 |

[Annual report FY25, pp. 24–31 y estados financieros](https://s202.q4cdn.com/285121676/files/doc_financials/2025/ar/Macy-s-Inc-2025-Annual-Report.pdf), [10-Q H1, pp. 3 y 27](https://www.sec.gov/Archives/edgar/data/794367/000162828026061320/m-20260801.htm).

**No confundir operating income con EBIT obtenido de net income.** TTM net income $750 + taxes $237 + net interest $94 = $1,081. Al excluir también debt-extinguishment loss $16 llega a $1,097; diferencia con operating income $1,144 = benefit-plan income $20 menos pension settlement $67. Para comparar operaciones uso operating income y declaro la definición.

Normalización analítica: **1,144 − 39 + 199 − 328 = $976m** antes de retirar IEEPA. Retirar $95m de gross operating refunds Q2 da **$881m**, margen 3.87% sobre total revenue. Es una sensibilidad conservadora, no beneficio recurrente exacto: conserva reinversiones financiadas por refunds. No extraigo EBIT neto del EPS redondeado. Q3 $17m operativo/$1m interés no entra al TTM; Q2 $3m de interés tampoco estaba en operating income. La compañía comunica $0.23 EPS neto de reinversión y no un puente exacto de EBIT neto recuperado aquí. [Comunicado Q2, sección Tariff Refunds y guidance](https://investors.macysinc.com/newsroom/news/news-details/2026/Macys-Inc--Reports-Strong-Second-Quarter-2026-Results-With-Continued-Growth-Across-All-Nameplates/).

Add-back de cierres no significa cero coste futuro: los $199m mezclan partidas y pueden repetirse. Tampoco ajusto las ventas TTM como si tiendas cerradas siguieran abiertas. El TTM no es un perímetro pro forma.

## Renta y límite de comparabilidad
M registra rentas operativas por devengo; EBIT conserva depreciación de finance leases, pero excluye su interés. KSS solicitado trata **toda renta cash** como gasto operativo. Para homologar se requiere sumar renta operativa de devengo y depreciación finance lease, y restar pagos operativos cash completos y principal/interés cash de finance lease, conciliando variable, short-term, sublease y componentes no-lease. No duplicar pagos ni deducir leases nuevamente en EV.

Referencia anual, **no TTM**: FY25 cash de pasivos operativos $399m; principal finance lease $3m; interés finance lease expense $1m. Rent expense: mínimo inmobiliario $361m, variable $64m, sublease income $54m y personal property $5m. El $399m no es toda renta cash. Enero-2026: operating liabilities $3,122m y finance $13m. Faltan flujos H1 y desglose lease corriente agosto para puente completo. [Annual report, notas 4 y 6](https://s202.q4cdn.com/285121676/files/doc_financials/2025/ar/Macy-s-Inc-2025-Annual-Report.pdf).

## Lectura limitada, no precio objetivo
EV sin leases / operating income reportado **6.86x**; / normalizado antes de IEEPA **8.04x**; / sensibilidad sin refund bruto **8.91x**. Son ratios indicativos con renta contable, no múltiplos homogéneos con KSS. La aparente baratura GAAP depende de partidas no recurrentes; no prueba mispricing. Macy’s mezcla Bloomingdale’s/Bluemercury, distinta exposición a lujo, y no justifica trasladar múltiplo automáticamente. No se estima valor inmobiliario ni maintenance capex.

## Próximo hito
**Fecha oficial no verificada**. El calendario oficial accesible no expuso un próximo evento; no convertir ausencia en prueba de que no existe anuncio. [Calendario IR](https://www.macysinc.com/investors/events-presentations-and-investor-updates/Events/default.aspx). 2-dic-2026 aparece como **estimación externa**, no fecha confirmada, en [MarketBeat](https://www.marketbeat.com/stocks/NYSE/M/EARNINGS/). Siguiente revisión: Q3 y desglose de reversión/reinversión IEEPA, crecimiento sin cierres y actualización de leases/acciones. Hasta entonces: comparable operativo, no mediana de valoración.

## Reproducción
Ejecutar `python ratios.py`; lee `facts.json`, no usa red y verifica revenues, operating income y normalización. `ratios_output.json` conserva el resultado. Los inputs mínimos documentados permiten reproducción sin filings originales.
