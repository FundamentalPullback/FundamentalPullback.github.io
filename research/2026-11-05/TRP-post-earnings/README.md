# TC Energy TRP: paquete público V2.1

Fecha de análisis: 5 de noviembre de 2026. **En observación; sin entrada aprobada.** Los cálculos son reproducibles, pero la valoración y el puente financiero a noviembre siguen siendo provisionales.

## Leer primero

1. dossier_es.md: informe completo y limitaciones.
2. audit_certificate_v2_1.json y verdict_v2_1.md: alcance limitado de la revisión independiente.
3. model_output.json y los CSV: historia, hipótesis, proyecciones y sensibilidades.
4. sources.json: enlaces oficiales y procedencia. No se redistribuyen PDFs ni textos completos de terceros.

El precio de referencia es **US$64,38, observado el 5 de noviembre de 2026 a las 15:34:29 UTC**. Es una referencia analítica histórica, no una cotización en vivo. El muestreo de datos de mercado posterior incluido tiene su propio sello horario. Esta entrega no actualiza la cotización.

## Reproducir cálculos

Requiere Python 3 y únicamente la biblioteca estándar. Desde una copia extraída del paquete:

- python model.py
- python independent_recalculation_v2_1.py

El primer comando vuelve a generar el JSON/CSV del modelo. El segundo recalcula independientemente los escenarios, históricos, sensibilidades, inversas y controles técnicos. La revisión original realizó 539 comprobaciones aritméticas sin fallos; la reproducción pública conserva esas comprobaciones. No vuelve a descargar documentos ni afirma repetir la verificación documental de los PDFs excluidos.

Los comandos escriben resultados junto a los scripts; conviene ejecutar sobre una copia si se desea conservar intactos los hashes de entrega. No hacen operaciones de mercado ni publicaciones.

## Integridad y cambios de entrega

PUBLIC_MANIFEST.json contiene los hashes actuales. EDITORIAL_DELTA.json documenta cambios exclusivamente editoriales/de portabilidad respecto de la entrega V2.1 y del certificado original. Los hashes históricos del certificado identifican el conjunto analítico original, no necesariamente las copias públicas con etiquetas editadas.

No se han cambiado datos, hipótesis económicas, fórmulas, escenarios, clasificación de caja ni conclusión de inversión. Las correcciones V1→V2 ya estaban incorporadas antes de esta entrega pública.
