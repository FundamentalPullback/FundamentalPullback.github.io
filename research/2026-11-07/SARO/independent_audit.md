# SARO: comprobación final de versión corregida

Fecha: 8 de noviembre de 2026.

Versión revisada: SHA-256 del manifiesto `66d92da52c5f85d57dbb4c770e3ff207ba41c067b0fd13e670aa66147357ed03`.

**Dictamen: apta como investigación parcial corregida; no apta para valoración aprobada, entrada, tamaño o stop.** Ninguna operación queda autorizada por este dictamen.

Se han incorporado las correcciones materiales de la auditoría: alcance del FCF y adquisición neta, sesión no verificada del precio scanner, controles TI y distinción entre deficiencias abiertas/remediadas, acciones puntuales y dilución, contraprestación contingente, licencia OEM ya pagada, ASR como intención y vencimiento de cobertura de intereses. No quedan contradicciones materiales pendientes entre esas correcciones y el informe v2.

Comprobaciones:
- 138 pruebas independientes satisfactorias, incluidos todos los hashes del manifiesto actual.
- El modelo ejecutado en directorio temporal reproduce byte por byte `results.json`, sin escribir en la versión congelada.
- Las cinco comprobaciones del modelo son satisfactorias.
- Valoración y entrada siguen sin aprobar: valores de valoración nulos; entrada deshabilitada.
- Archivo original completo conservado: manifiesto `d66ddc43632cd19b385f9e8b40b19ced9831b0d54102b0cac9cf444aa00a845e`, con todos sus archivos comprobados sin diferencias.

Persisten los huecos expresamente declarados, que no se resuelven con esta corrección editorial: economía y renovación de licencias; inversión de mantenimiento/expansión y capital circulante; puente de capital y covenant pro forma ASR; margen y crecimiento comparable por segmento; WACC, comparables y escenarios numéricos; revisión técnica. Tampoco está verificada la sesión de los 27,52 del scanner. No se han creado cifras artificiales para cerrar esos huecos.

Pruebas reproducibles: `checks_v2.py`, salida `checks_v2.json` y comprobación adicional `final_v2.json`. La auditoría original se conserva y este documento la complementa únicamente para la nueva versión.