# Bentley Systems · Resultados Q3 2026 · Paquete público V2

Abrir primero `BSY_resultados_20261105.html`. La verificación independiente está en `audit/AUDIT_PUBLICO.html`.

**Estado: investigación parcial, en observación.** No hay aprobación Stage 3/3.5, valor integral aprobado, techo de compra ni entrada. Las salidas 12,93 / 23,91 / 41,59 USD por acción son cálculos parciales y contrafactuales, no precios objetivo ni potencial de caída de la acción.

**Precio congelado:** 47,09 USD, operación del 5 de noviembre de 2026 a las 16:14:40 UTC. No es precio en vivo ni cierre. Este paquete no actualiza esa cotización.

## Reproducir

Con Python 3, ejecutar `python reproduce_public.py` desde esta carpeta. Solo requiere la biblioteca estándar. Recrea los datos y cálculos en un directorio temporal y verifica ocho archivos exactos, las identidades FCFF de las treinta filas y la referencia de cotización. Escribe `reproduction_result.json`. El HTML entregado conserva el informe auditado; la reproducción no vuelve a maquetarlo.

`model_calc.py` contiene el FCFF de diez años y sus sensibilidades. `build_metrics.py` reconstruye la historia, incluido FCF por acción básica con denominadores publicados o ponderados por días. Los CSV y JSON permiten revisar los componentes. En años 6–10 se muestran la reinversión de transición y la inversión efectiva; el 5% de ventas se aplica solo a los años 1–5.

## Fuentes y auditoría

`sources.json` enlaza los documentos públicos. `source_notes.json` recoge unos pocos hechos verificados y la procedencia de la cotización. No se incluyen documentos completos, transcripciones ni respuestas de búsqueda de terceros.

La auditoría original V2 supera 326/326 controles. `audit/source_certificate_v2.json` conserva sus hashes originales. `PUBLIC_DELTA.json` identifica las diferencias editoriales entre ese paquete y esta entrega: referencias relativas, resumen mínimo de fuentes y rotulado público. `audit/public_package_certificate.json` verifica esta conversión. No cambian supuestos, flujos, resultados ni decisiones.

`manifest.json` identifica los archivos de esta entrega. `publication_metadata.json` y `qa_log.json` describen alcance y límites. La revisión visual por la vía permitida del publicador sigue pendiente; este paquete no acredita publicación ni operación alguna.
