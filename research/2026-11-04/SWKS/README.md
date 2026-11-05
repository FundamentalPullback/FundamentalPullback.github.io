# Skyworks (SWKS): resultados, Qorvo y caja combinada

Abrir primero `report.html`. `report.md` contiene el mismo análisis en texto. Corte: 4 de noviembre de 2026.

**Resultado: investigación parcial condicionada.** La revisión independiente aprueba compartir el trabajo con sus límites, no una valoración total de la acción ni una entrada. Las cifras del DCF y los residuos de capital son ejercicios ilustrativos; no utilizarlos como precios objetivo. `summary.json` mantiene nulos los valores accionarios y falsos los campos de aprobación.

## Reproducción

Ejecutar `python reproduce.py` con Python 3 y su biblioteca estándar. Recalcula historia, diez años FCFF, terminal, inversa, sensibilidades, informe y auditoría. No necesita conexión de red ni paquetes externos.

**Supuestos editables:** `model/model.py` es la fuente canónica de las hipótesis. `model/inputs.json` es una instantánea regenerada para inspección y auditoría; editar sólo ese JSON no cambia una nueva ejecución. Cualquier cambio del modelo requiere nueva revisión antes de uso.

`history/source_inputs.json` conserva únicamente registros factuales seleccionados de SEC companyfacts, con sus períodos, fechas y accession numbers. Los resultados del cuarto trimestre se transcriben del comunicado oficial en `build_history.py`. El historial mantiene diferencias pequeñas de redondeo.

`capital/combined_capital.json` separa capital independiente, pro forma de julio, canje y principal reconstruido. Los estados consolidados reales de cierre permanecen desconocidos. `capital/sources.json` identifica documentos primarios; no se incluyen copias completas de documentos externos ni transcripciones.

`audit_independent.md` y `audit_independent_checks.json` explican alcance, correcciones y107 verificaciones. `manifest.json` registra huellas de los archivos entregados.
