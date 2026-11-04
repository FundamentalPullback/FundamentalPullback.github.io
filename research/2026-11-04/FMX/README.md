# FMX: investigación parcial y valoración de activos identificados

Corte4 nov 2026; precios cierre3 nov 2026. Estado: investigación parcial revisada de forma independiente; sin aprobación de entrada.

No contiene un fair value total de FEMSA ni aprobación de entrada. ImperialBrady y otros activos no valorados quedan fuera de los escenarios parciales, no se consideran sin valor. Mantener visibles los límites de caja Spin, D&A/botellas, seguros, leases, minoritarios, derechosBD y capital posterior a septiembre. No habilita Stage 3 completo, calendario ni filtro técnico.

Leer report.md y summary.json. Las cifras bear/base/bull de valor total son null deliberadamente. partialIdentifiedAssetValuation es otra métrica y no debe poblar una tarjeta de precio justo total o una orden.

## Reproducción offline

Python3 estándar, sin red, paquetes adicionales ni filings completos:

    python reproduce.py

Reconstruye historia, contraste exKOF, comprobación de propiedad y KOF, inputs/modelos, sensibilidades, tasas, comparables, informe, resumen y QA. Los archivos fuente mínimos y las hipótesis se incluyen; no se requiere la carpeta privada sources. Los extractores originales de filings no forman parte del paquete público.

- history/: 3FY,4Q,TTM y comparaciones, múltiples bases conservadas, 52 comprobaciones.
- ownership/: derechos económicos, capital, dividendos, KOF3FY/4Q y seguros; reproducción propia273 comprobaciones.
- model/: dos DCF de 10 años y sensibilidad/inverso,429 identidades.
- comps/: ATD,WALMEX y contraste implícito exKOF con cierres3nov.
- report.md,summary.json,pros_cons.json: síntesis y evidencias literales propias.
- qa_results.json:148 controles generales, además de las comprobaciones del modelo.

Los supuestos no se retroescriben como historia observada. DCF en MXN nominal con conversión coherente aUSD, rentas operativas y reinversión financiada. La capitalización por derechosBD es una asignación económica, no el flotanteADR ni dilución exacta. No se entregan documentos de terceros completos, sólo datos mínimos derivados y enlaces.
