# Auditoría incremental · límites de tiempo y cotización

**Delta aprobado para publicación de la ficha prospectiva. No autoriza entrada, orden ni ejecución.**

## Corrección del evaluador

Se comparó el código anterior conservado con la versión corregida. Ahora rechaza cierres fuera del cuarto de hora exacto, incluidos segundos y microsegundos no nulos. La ventana de ejecución es [cierre de señal, cierre + 15 minutos): exactamente al vencimiento y después devuelve candidato histórico caducado, con `historical_only=true` y `execution_window_current=false`. Conserva la primera señal histórica y no la sustituye por una posterior. Los candidatos nunca reciben aprobación de entrada.

Pasan los 22 tests sintéticos del autor y 229 comprobaciones independientes del delta, incluidos los 25 cierres elegibles, el instante anterior/al/posterior a cada vencimiento, segundos y microsegundos, preservación del primer candidato y hashes de fuentes. No son señales observadas, un backtest ni una auditoría integral de ingestión de datos o ejecución. El evaluador sigue siendo una ayuda de investigación sin feed, órdenes o aprobación operativa.

## Nota de precio

Se verificó la instantánea de StockAnalysis: **67,44 USD, premarket del 5 noviembre a las 06:22 EST**, consultada a las 06:30:46 EST (11:30:46 UTC). Su SHA-256 coincide con el manifiesto. Yahoo sigue mostrando 66,0103 a las 04:31:06 EST, volumen cero en ese registro: no es corroboración contemporánea.

El informe distingue correctamente esa marca indicativa del cierre regular de 65,78 y de un bid/ask ejecutable. A 67,44 no cabe una entrada bajo esta ficha. No se elevan los máximos 65,78/66,50. El premarket no activa por sí solo la suspensión definida para una negociación regular superior a 66,50; si ocurre durante sesión regular, se exige nueva revisión antes de reactivar.

Solo se añadieron a los datos la hora de revisión de mercado y la nota de cotización. Valoración, propuesta, stop, niveles, riesgo y cierre regular permanecen idénticos. Se conservan originales y ZIP anterior.

## Hashes revisados

- Informe: `f6e362172cd049fa52bae5e2b051010ef37eb5ffadb62759440f1afa65789a68`.
- Evaluador: `95c5a383dd489d31d6b80a50ca08030101379bfc02008937835758cbe6c030e7`.
- Datos: `d90555cfcdf3dc74f09adead3e89d3ce537b252878815891b8ea0105f12696ae`.
- HTML: `58df8e1fd2a3b519a5d19fce130a6bbb0f245e1cc48b3b31fc47bf67f81447fb`.

El detalle reproducible está en `delta_audit.json` y `boundary_delta_tests_independent.json`. Este dictamen complementa la auditoría original; no afirma QA visual renderizado ni elimina los requisitos operativos pendientes.
