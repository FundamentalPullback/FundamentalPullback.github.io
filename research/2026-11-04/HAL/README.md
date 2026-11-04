# HAL Stage 3 · 4 noviembre 2026

Cierre de referencia: 34,07 USD del 3 de noviembre. Datos financieros: septiembre 2026.

El reporte separa hechos GAAP, estimaciones de normalización y escenarios de inversión.
La investigación fundamental no constituye una entrada Stage 3.5 aprobada.

Reproducción con Python 3, sin paquetes externos:

1. python build_history.py
2. python model.py
3. python build_comps.py
4. python build_report.py
5. python validate.py

Las tablas primarias necesarias están en sources/. Los modelos no requieren consultar internet.
Los enlaces del reporte y source_manifest.json permiten volver a consultar los originales.
No se redistribuye la transcripción completa de terceros.

Todos los importes del modelo son millones de USD, excepto cotización por acción.
Las cifras españolas del reporte usan punto para miles y coma para decimales; CSV/JSON usan formato numérico estándar.
El archivo validation.json contiene comprobaciones internas, no sustituye una revisión independiente.
