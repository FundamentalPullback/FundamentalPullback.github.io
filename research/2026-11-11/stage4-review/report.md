# Stage 4 · cierre del 11 de noviembre de 2026

Revisión de seis posiciones PAPER. Referencias para el 12 de noviembre. Sin operaciones ni cambios en cantidades o efectivo. Los niveles son manuales, no órdenes acreditadas del bróker.

## Decisión de gestión

**Sin salida detectada en la sesión regular:** ningún mínimo toca S y ningún cierre rompe el trailing previamente vigente. Los seis cierres superan M; no se cumple la salida combinada de dos cierres bajo EMA50 y cierre bajo M. No se afirma una EMA50 nueva sin reconstrucción verificada.

**Actualizar mañana:** ASO 63,45 → **63,56**; ULTA 609,58 → **610,40**; EXLS 40,61 → **40,72**. DOCU mantiene **76,97**. CTSH y JXN continúan sin trailing activado.

**DOCU gana margen, pero sigue siendo la más cercana al trailing:** cierre 80,15, un margen del 3,97% del cierre hasta 76,97. CTSH queda un margen del 5,01% del cierre hasta S. Esto no activa una compra ni una segunda venta parcial.

## Niveles y proximidad

Precios StockAnalysis/S&P Global: cierre regular del 11 de noviembre, 16:00 EST, comprobados después del cierre. No son precios en vivo ni after-hours. Distancia = (cierre − protección próxima sesión) / cierre; no es pérdida máxima garantizada.

| Posición | Acciones PAPER ya registradas | Cierre regular USD | Mínimo regular USD | S manual USD | M USD | Protección próxima sesión USD | Distancia desde cierre |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCU | 134 | 80,15 | 77,27 | 62,50 | 63,60 | Trailing 76,97 | 3,18 / 3,97% |
| CTSH | 82 | 64,43 | 63,46 | 61,20 | 61,55 | S 61,20; trailing inactivo | 3,23 / 5,01% |
| EXLS | 160,699 | 43,92 | 43,56 | 33,50 | 34,05 | Trailing 40,72 | 3,20 / 7,29% |
| ULTA | 16 | 659,08 | 649,52 | 522,00 | 529,01 | Trailing 610,40 | 48,68 / 7,39% |
| ASO | 155 | 69,32 | 68,93 | 50,30 | 51,21 | Trailing 63,56 | 5,76 / 8,31% |
| JXN | 60 | 139,44 | 137,37 | 124,80 | 126,14 | S 124,80; trailing inactivo | 14,64 / 10,50% |

## Qué vigilar

- **DOCU:** Vigilar cierre frente a 76,97; no repetir parcial. Revisión fundamental pendiente.
- **CTSH:** Vigilar toque de S 61,20. Trailing inactivo; activación por cierre 77,67. Sin nueva ampliación.
- **EXLS:** Subir trailing a 40,72 para mañana; vigilar cierre. A196 sigue condicionado.
- **ULTA:** Subir trailing a 610,40; vigilar cierre. Revisión fundamental prioritaria; ampliación bloqueada por campaña.
- **ASO:** Subir trailing a 63,56; vigilar cierre. No es una nueva aprobación fundamental.
- **JXN:** Vigilar toque de S 124,80. Trailing inactivo; activación por cierre 158,25; revisar capital y reservas.

## Reglas y cálculo auditable

Primero se comprueba el cierre de hoy contra el trailing que ya estaba vigente. Solo después se calcula el nivel de mañana. S funciona por toque intradía; trailing por cierre, con salida manual en la siguiente apertura si se activa. No confundir ambos. Huecos y deslizamiento pueden superar el riesgo nominal.

Continuidad con la semilla exacta congelada de A547 al 10 de noviembre, sin recalcular retrospectivamente señales ni bajar protección. TR = max(H−L, |H−cierre previo|, |L−cierre previo|); ATR14 Wilder = (13×ATR previo+TR)/14. Candidato = mayor cierre desde entrada−3×ATR14. Nueva referencia = max(S, referencia previa, candidato). Precisión interna conservada, presentación a dos decimales.

Para ATR se utiliza únicamente la serie ChartExchange de la sesión 11: ASO H70,36/L68,93/C69,31; ULTA H663,68/L650,00/C659,16; DOCU H80,24/L77,57/C80,14; EXLS H44,22/L43,63/C43,91. Sus marcas «At Close» son 15:59:xx; se conservan como continuación del mismo proveedor, no como sustituto del cierre regular mostrado. Sus OHLC difieren de StockAnalysis. No mezclamos proveedores ni promediamos. Son niveles calculados dependientes del proveedor, no certificación de bolsa.

| Ticker | ATR14 | Mayor cierre | Candidato | Referencia próxima sesión |
|---|---:|---:|---:|---:|
| ASO | 2.541438426976 | 71,18 | 63.555684719071 | 63,56 |
| ULTA | 18.243472002107 | 665,13 | 610.399583993678 | 610,40 |
| DOCU | 2.816069936824 | 85,27 | 76.821790189528 | 76,97 |
| EXLS | 1.195126611332 | 44,31 | 40.724620166003 | 40,72 |


CTSH conserva R original 5,49 y activación +2R 77,67, no R recalculado desde su promedio. JXN R11,15 y activación158,25. Ninguno alcanza su activación. S/M no cambian. ANF y HRB permanecen cerradas. Se mantienen las cantidades previamente publicadas, compatibles con la captura aportada; esta revisión no audita todos los movimientos del bróker.

## Fundamentos y ampliaciones

No hay nueva ampliación aprobada. Se mantienen las reservas fundamentales anteriores de ULTA (valoración y reinversión), DOCU (SBC y valoración), EXLS (A196 condicionado), CTSH (integración/IA) y JXN (capital/reservas). Esta revisión técnica no reemplaza una actualización financiera completa ni certifica ausencia de noticias. El 25% opcional no es orden, las ventas no reponen presupuesto acumulado de campaña y no se repiten parciales ya realizadas. Una cotización mejor no valida retrospectivamente excepciones de ejecución previas.

## Fuentes y evidencia

- [DOCU: cierre regular y OHLC](https://stockanalysis.com/stocks/docu/history/)
- [CTSH: cierre regular y OHLC](https://stockanalysis.com/stocks/ctsh/history/)
- [EXLS: cierre regular y OHLC](https://stockanalysis.com/stocks/exls/history/)
- [ULTA: cierre regular y OHLC](https://stockanalysis.com/stocks/ulta/history/)
- [ASO: cierre regular y OHLC](https://stockanalysis.com/stocks/aso/history/)
- [JXN: cierre regular y OHLC](https://stockanalysis.com/stocks/jxn/history/)
- [ASO: serie técnica homogénea](https://chartexchange.com/symbol/nasdaq-aso/historical/)
- [ULTA: serie técnica homogénea](https://chartexchange.com/symbol/nasdaq-ulta/historical/)
- [DOCU: serie técnica homogénea](https://chartexchange.com/symbol/nasdaq-docu/historical/)
- [EXLS: serie técnica homogénea](https://chartexchange.com/symbol/nasdaq-exls/historical/)

[Semilla A547](../../2026-11-10/stage4-review/calculations.json) · [Cálculos de hoy](calculations.json). Valores y fuentes fechados; informes anteriores conservados.
