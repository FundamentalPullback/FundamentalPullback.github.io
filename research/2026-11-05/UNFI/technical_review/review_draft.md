# UNFI: revisión técnica al cierre del 4 de noviembre de 2026

Corte de fuentes: 5 noviembre, 03:19 UTC. Valoración fundamental concluida y auditada como investigación condicional en observación; no Stage 3 aprobado para invertir ni Stage 3.5 aprobado, ninguna orden ni cantidad. Esta revisión no equivale a una señal retroactiva.

## Precio y datos

El histórico regular de StockAnalysis confirma O 46,41 / H 48,44 / L 46,14 / C 48,29, volumen 783.406. Yahoo también muestra cierre 48,2900009 y metadata regular 48,29 con sello de las 21:00:03 UTC. Una respuesta web anterior mostraba 48,32 tanto en encabezado como en barra; no se atribuye automáticamente esa diferencia a fuera de horario. Se adopta la barra histórica coincidente de dos fuentes, preservando la observación anterior.

Los volúmenes difieren ligeramente: Yahoo barra 783.300 y metadata 783.346, frente a 783.406 del histórico StockAnalysis. No se construye un gatillo de volumen con esa precisión aparente. La serie conserva cinco años de Yahoo hasta el 3 de noviembre y reemplaza la barra final por la barra redondeada y documentada de StockAnalysis. No hay ajustes por dividendos en esta serie; bruto y ajustado coinciden.

Fuentes: https://stockanalysis.com/stocks/unfi/history/ y https://query1.finance.yahoo.com/v8/finance/chart/UNFI?interval=1d&range=5y&events=div%2Csplits . Archivos fuente y SHA en technicals.json.

## Indicadores reproducibles

- EMA 20: 46,588319.
- EMA 50: 46,447016.
- EMA 200: 44,574793; sube 1,0409% en veinte sesiones.
- ATR de Wilder 14: 1,712362. RSI de Wilder 14: 57,1878.
- Volumen medio de veinte sesiones, incluida la última: 562.140.
- Máximo de 252 sesiones: 57,02; retroceso del cierre: 15,3104%.

Precio por encima de EMA 50 y EMA 20 por encima de EMA 50: los filtros básicos se cumplen. También se sitúa sobre EMA 200, con pendiente positiva, pero eso no garantiza una estructura de mínimos crecientes. RSI no es veto ni autorización independiente. El incremento diario de 7,07% no es prueba de que haya cambiado el valor económico.

## Estructura y límites

El máximo confirmado del 15 de octubre es 48,87 y el del 28 de octubre 48,71. El cierre actual sigue por debajo de ambos. El mínimo confirmado del 30 de octubre, 44,84, es menor que el del 21 de octubre, 45,32. Por ello no se describe una secuencia completa de máximos y mínimos ascendentes. La recuperación de medias merece seguimiento, pero no se convierte en ruptura que aún no ocurrió.

48,71–48,87 son referencias observadas, no órdenes stop de compra. El mínimo 44,84 tampoco es un stop aprobado: falta elegir configuración prospectiva, punto de entrada, margen técnico, riesgo y plazo dentro del máximo fundamental que resulte de la revisión. No se elige un stop sólo para conseguir un ratio de beneficio/riesgo deseado.

## Estado Stage 3.5

- Stage 3: análisis terminado en observación condicional; no aprobación para invertir ni autorización heredada de A104 o del score 100.
- Configuración A/B/C: no aprobada.
- Máximo fundamental y técnico: nulos.
- Señal y marco temporal de ejecución: nulos.
- M, S, capital y riesgo fijo de campaña, reservas, tamaño y caducidad: no aprobados.
- Cantidad: cero. Entrada: no aprobada.

La próxima fecha exacta de resultados sigue por confirmar; eso no prueba por sí solo que estemos dentro de la semana excluida. Antes de ejecutar habría que verificar evento, valor y ficha vigente, además de cartera, efectivo y órdenes existentes. Un precio diferente obliga a actualizar estos datos; no activa automáticamente ninguna referencia de este documento.

Método: EMA con semilla de primera observación, ATR y RSI con media inicial de catorce observaciones y suavizado de Wilder; pivotes requieren dos sesiones a cada lado. El motor y CSV conservados permiten reconstruir la revisión. La reconstrucción técnica independiente desde Yahoo coincide con los indicadores y documenta el efecto inmaterial de usar una barra final ligeramente distinta; technical_independent_check.json conserva sus resultados. La auditoría de valoración y libro está disponible en el expediente.
