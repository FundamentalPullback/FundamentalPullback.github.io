# Stage 4 · Trailing al cierre del 5 de noviembre

**Niveles de referencia calculados para la sesión del 6 de noviembre de 2026. No son órdenes del bróker.**

Cálculo finalizado el 6 de noviembre a las 00:04:39 UTC (5 de noviembre, 19:04:39 EST). Fuente homogénea: ChartExchange, 323 sesiones del 28 de julio de 2025 al 5 de noviembre de 2026. No es una cotización en vivo.

| Acción | Cierre 5 nov · USD | ATR14 Wilder | Trailing 6 nov · USD |
|---|---:|---:|---:|
| HRB | 55.00 | 1.690952 | **50.40** |
| ASO | 67.81 | 2.414343 | **60.57** |
| EXLS | 43.61 | 1.208752 | **39.98** |
| ANF | 157.59 | 7.056001 | **151.69** |
| ULTA | 649.68 | 18.956174 | **606.31** |
| DOCU | 78.88 | 2.959826 | **76.97** |

## Método y aplicación

Se activa tras el primer cierre regular en +2R respecto a la entrada inicial. Candidato: máximo cierre diario desde entrada menos 3 × ATR14 Wilder. Se conserva el mayor entre stop inicial, trailing previo y candidato; nunca se baja. Se calcula con precisión completa y se muestran dos decimales. Los niveles nuevos se aplican prospectivamente a la sesión siguiente: no se reinterpretan ejecuciones anteriores.

ANF y ULTA conservan el nivel generado el 4 de noviembre porque el candidato del 5 es inferior. DOCU conserva su suelo previo de 76,97 USD. Ningún cierre del 5 de noviembre quedó por debajo del correspondiente nivel previo reconstruido. Una protección por cierre no garantiza precio de salida y no evita huecos.

## Discrepancias conservadas

Estos son cálculos reproducibles de un proveedor identificado, no niveles certificados por la bolsa. No se mezclan barras entre proveedores. Contrastes con StockAnalysis o continuación de semillas anteriores: HRB 50,38–50,39; ASO 60,53; EXLS 40,01. No son bandas de ejecución ni niveles alternativos adoptados. ASO IR/LSEG confirma el cierre 67,81, pero su apertura y mínimo difieren de ChartExchange. Las demás comprobaciones primarias no proporcionaron una serie común definitiva.

## Alcance

Esta actualización completa la conciliación del trailing. No es una nueva valoración fundamental ni una autorización para ampliar. No cambia operaciones, cantidades, efectivo, stops manuales ni registros históricos. No confirma ninguna orden colocada. A247 permanece como revisión histórica del 4 de noviembre.

## English summary

Calculated close-based trailing references for November 6, using November 5 data: HRB $50.40; ASO $60.57; EXLS $39.98; ANF $151.69; ULTA $606.31; DOCU $76.97. One homogeneous ChartExchange history, Wilder ATR14, highest close since entry and never-lower rule. These are provider-specific reference calculations, not exchange-certified prices, broker orders or buy approvals. Full precision is retained. No changes to holdings, cash, manual stops or fills. Historical records are preserved.

## Fuentes y cálculos

[Cálculos completos](https://fundamentalpullback.github.io/research/2026-11-05/trailing-reconciliation/calculations.json) · [Revisión histórica A247](https://fundamentalpullback.github.io/#biblioteca/A247)
- [HRB: histórico de precios](https://chartexchange.com/symbol/nyse-hrb/historical/)
- [ASO: histórico de precios](https://chartexchange.com/symbol/nasdaq-aso/historical/)
- [EXLS: histórico de precios](https://chartexchange.com/symbol/nasdaq-exls/historical/)
- [ANF: histórico de precios](https://chartexchange.com/symbol/nyse-anf/historical/)
- [ULTA: histórico de precios](https://chartexchange.com/symbol/nasdaq-ulta/historical/)
- [DOCU: histórico de precios](https://chartexchange.com/symbol/nasdaq-docu/historical/)
