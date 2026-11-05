# TRMD: revisión independiente de cálculos técnicos

Se reconstruyeron los indicadores desde el JSON de Yahoo y la barra del 4 de noviembre de StockAnalysis, sin importar ni ejecutar el cálculo original. Se verificaron 7.556 controles: las EMA20/50/200 de 1.254 observaciones en dos bases, ATR y RSI Wilder, máximos, retroceso, volumen medio, pivotes y estados de entrada. Todos pasan.

El cierre 37,64 queda por encima de EMA50 sin ajustar 37,4524 y ajustada 37,0336; EMA20 supera EMA50 en ambas. El retroceso del 13,0917% desde 43,31 está en el intervalo de elegibilidad del plan. La revisión larga es constructiva, con deterioro corto. No se ha usado la variante de ajustes más favorable para inventar un aprobado. La EMA200 usa semilla inicial; cinco años reducen mucho la influencia de la semilla, sin asegurar identidad con proveedores que usen otro historial.

El mínimo 37,02 del 4 de noviembre todavía no tiene dos sesiones posteriores para ser un pivote confirmado. El cierre cumple elegibilidad, no una señal prospectiva: no están aprobados soporte, máximo técnico, stop ni tamaño. Cantidad cero y Stage 3.5 no aprobado son coherentes. El 39 USD fundamental condicionado no es una orden.

El último cierre y OHLC nulos de Yahoo fueron sustituidos de manera expresa por la barra regular archivada de StockAnalysis. Los metadatos de Yahoo corroboran el cierre, pero el volumen difiere. No se resuelve esa diferencia mediante un promedio ni se activa señal de volumen. La comprobación valida el uso coherente de la evidencia recibida, no garantiza que los proveedores no la revisen después.

El dividendo Nasdaq del 17 de noviembre exige ajustar de forma consistente serie, niveles y efectivo. La caída after-hours no sustituye el cierre regular. No se ha aprobado una entrada ni un monitor, y este documento no extiende la autorización de negociación.

Reproducción: `independent_technical_review.py`; resultados: `independent_technical_checks.json`. Requiere pandas. Fuentes públicas y plan se conservan en `review_draft.md` y los archivos originales de esta carpeta.
