# CTSH · verificación independiente de apertura

**Conclusión: ficha B suspendida; no entrada.** La negociación regular superó 66,50. Volver al intervalo no reactiva la propuesta sin una nueva evaluación registrada. No se ha enviado orden ni supuesto ejecución.

- Se agregaron independientemente las **15 barras consecutivas de un minuto, 09:30–09:44 EST**, para reconstruir la vela completa **09:30–09:45 EST / 14:30–14:45 UTC**. Los timestamps de Yahoo identifican el inicio de barra.
- Resultado O/H/L/C: **67,1200 / 67,8572 / 66,4053 / 66,5975**; volumen **401.797**. Coincide exactamente con la barra de 15 minutos del mismo proveedor, sin diferencias OHLCV.
- El máximo regular supera 66,50 y el cierre 66,5975 está fuera de **(65,26; 65,78]**. No existe señal de entrada en esa primera vela.
- **StockAnalysis 66,81 a las 09:42 EST**, marcado como mercado abierto, corrobora por separado el hecho decisivo de una cotización regular >66,50. No confirma el OHLC exacto de Yahoo.
- Yahoo muestra además **67,26 a las 09:46:35 EST**. Es una marca de esa instantánea, no bid/ask ejecutable actual.

## Discrepancias conservadas

El OHLC de StockAnalysis corresponde a una instantánea anterior y difiere del de Yahoo. Además, Yahoo muestra mínimo diario 66,53 en metadatos frente a 66,4053 en sus barras de uno y quince minutos. No se mezclan ni se certifican esos OHLC entre proveedores. Estas diferencias no alteran la superación regular de 66,50 corroborada por ambos.

El campo `retrievedAt` del recolector se registra **antes** de hacer la petición: es inicio de consulta, aproximadamente 14:46:31 UTC, no final de descarga. Los archivos se guardaron entre 14:46:38 y 14:46:40 UTC, después de la marca Yahoo 14:46:35; no se presenta como una cotización obtenida antes de existir.

Pasan **23 comprobaciones** de integridad, agregación, horario y condiciones. Fuentes brutas, hashes y resultados exactos quedan en `independent_verification.json`. Sin consultas de red nuevas, publicación, modificación de reglas ni operaciones.

El registro `observed_review.json` y su resumen concilian con esta verificación. Su clasificación es **suspendida y requiere nueva evaluación**, no cancelación terminal ni invalidación de la tesis. M sigue intacto.
