# Auditoría independiente de JBTM, revisión 2

Fecha: 8 de noviembre de 2026. Alcance: documentación pública preservada localmente, código, resultados y manifiesto. No se hicieron publicaciones, operaciones ni escrituras remotas. Esta auditoría no aprueba valoración ni entrada.

## Resultado

Reproducción correcta y estado parcial apropiado. Los 77 archivos del manifiesto coinciden con sus SHA-256. La ejecución aislada de run_model.py reproduce exactamente la estructura de results.json, sin modificar el paquete auditado. El valor razonable permanece nulo y la entrada deshabilitada. No se detectó un error aritmético en las pruebas de caja ni el descuento.

Hay precisiones documentales que deben incorporarse antes de declarar revisada una nueva versión: distinguir coste contractual de deuda, tasa efectiva contable y coste marginal; y declarar explícitamente que los precios/sesiones y las cifras Marel 9M24 no cuentan con captura local independiente. No es necesario inventar un precio, una caja comparable ni una valoración para cerrar esas precisiones.

## Comprobaciones

- Perímetros: 2023–24 son JBT anterior a Marel y 2025 combinado. La fuente anual respalda ingresos pro forma 2024 de 3.436,6 y la trimestral 9M24 de 2.597,6. El puente 3.629,2 de ingresos TTM anteriores es aritméticamente correcto, pero no es crecimiento orgánico ni FCFF comparable. La presentación inicial 3.494/479 no sustituye el pro forma posterior. La conciliación pública indica reducción IFRS/US GAAP de EBITDA de 31,9 USD por desarrollo/arrendamientos.
- Marel anual IFRS/EUR: CFO 95,1; inversión física 20,4; intangible 27,5; principal de alquileres 16,6, corroborados en fuente pública citada. La resta con los 9M citados arroja 77,7/8,9/6,7/4,7 para 4T24. No se verificó independientemente la tabla 9M: su PDF no está preservado y se declara descarga 403. No se reintentó mediante otra ruta. No sumar euros y dólares ni sustituir conversión IFRS/GAAP por simple FX. La comparación de caja sigue abierta.
- Caja futura: cálculos independientes arrojan 319,4072 / 359,5362 / 390,8895. Pagan inversión física, reserva de software/nube, incremento de circulante y transición. Son pruebas de un año, no previsiones aprobadas, terminal ni rango de valor. Los márgenes se definen post-SBC, pero no hay conciliación que demuestre una previsión normalizada. La depreciación 93 procede de 261 menos 168 de adquisición y sigue siendo una aproximación, no mantenimiento demostrado. La reserva de software puede duplicar desarrollo ya gastado. Estos límites impiden aprobar FCFF.
- No se suma la adquisición como reinversión recurrente ni se añaden sinergias nuevamente sobre márgenes que ya las incorporan. El tratamiento de compra/amortización e inversión tecnológica no queda cerrado por eliminar D&A contable.
- Derivados: pasivos brutos 120, activos 6, financiación 90+22=112 y operativo neto 8−6=2. La convención principal da 1.719−98+112=1.733 antes de alquileres financieros no verificados. La clasificación evita sumar 2 dos veces al circulante; el propio expediente deja abierta la conciliación deuda/cobertura a valor razonable.
- Principal de líneas redondeadas 1.720 frente a total divulgado 1.719, residuo 1 identificado. Deuda contable 1.694 es distinta. Efectivo disponible 98 y restringido 19 están separados. Inversiones afectadas 37 no son caja libre adicional. Garantías 117 y 10 no se convierten automáticamente en deuda; garantías de producto 19 son operativas.
- Acciones vigentes 51,077880 millones corresponden al 27 de octubre, no al promedio diluido. Convertibles 575 de principal frente a 501 de valor razonable, precio de conversión 187,77 y warrants 283,42 requieren convención coherente en escenarios. Recompras autorizadas no se tratan como ejecutadas. La minoría comprada no se resta otra vez. Alquileres 78,2/10,2 son cierre 2025, no septiembre de 2026; con alquiler operativo en FCFF no capitalizar otra vez.
- WACC independiente 8,45793554%, beta reapalancada aproximadamente 1,070. Treasury 4,86% del 6 de noviembre, ERP 4,41% del 1 de noviembre y beta sector Machinery 0,89/105 empresas están en las capturas. ERP utiliza Treasury 5,29%; la inconsistencia se reconoce y debe resolverse. Pesos actuales, beta sectorial y país no constituyen calibración aprobada.
- Precisión pendiente sobre deuda: el 10-Q, nota 9, especifica TLB max(SOFR,0)+1,75%, vencimiento 2 de enero de 2032. El 5,44% es tasa efectiva del trimestre, no coste marginal contractual contemporáneo demostrado. Revolver: SOFR/EURIBOR o base alternativa más margen por apalancamiento. Convertible: cupón 0,375%, tasa efectiva 0,93%. Una nueva versión debe dejar explícita esa distinción en anexo y resultados sin alterar silenciosamente el cálculo diagnóstico.
- Fecha de resultados 3 de noviembre corroborada en los archivos de presentación/publicación. Los controles no efectivos y debilidades materiales no remediadas están documentados. No se confunden con prueba de errores materiales en los estados.
- Precios 128,35 regular frente a 127,36 posterior al cierre: separación coherente en el modelo, pero las URLs de mercados carecen de captura local en los 77 archivos. La auditoría no eleva esa afirmación del autor a verificación independiente. Técnicos y Stage 3.5 pendientes.

## Dictamen y versión exacta

Aceptable exclusivamente como investigación parcial, con los límites indicados y sin autorización de operación. Para nueva versión, incorporar las precisiones de deuda y evidencia ausente, conservar v2, generar manifiesto nuevo y repetir checks. El estado parcial no exime de corregir hechos mecánicos conocidos.

Manifiesto v2 auditado: a33bffe9e01e73e624f130424065edc5b32331c7c8d2f0339af52a8b6aa3a716.
Resultados v2: 58b359fccf36638a3eb219d0c197446e2dba9c1efbdce5e27334ad4fb04053c4.

Archivos complementarios: check.py (ejecutable), checks.json (resultados), reproduction_stdout.txt (salida aislada). No se modificó ningún archivo del paquete v2.

## Adenda final: revisión 3 corregida y congelada

Se aplicaron las precisiones acotadas en el informe, anexo, resultados y registro de fuentes; se preservó el manifiesto original v2 en su archivo. Una consulta pública independiente permitida a StockAnalysis corroboró ambos precios y sus sesiones del 6 de noviembre. Se conserva el extracto fechado en fuente pública citada. Esta nueva evidencia cierra la limitación de precio descrita arriba, sin afirmar que existía antes. No se reintentó el PDF Marel denegado: la limitación sigue explícita en datos, anexo e informe. Las cifras diagnósticas no cambian.

Los 79 archivos del manifiesto v3 coinciden; run_model.py reproduce exactamente results.json y los cálculos independientes. Dictamen final: documentación corregida y reproducible, solamente parcial, sin FCFF comparable aprobado, sin valor razonable, sin entrada autorizada.

Manifiesto final v3 SHA-256: 19a42569ae2a5edf15684575f886f44afe18ecd6c419b4f5fea18ae1c8726b31.
Resultados finales v3 SHA-256: 6ad1b6592b5c24a1b1d8a87a29f87c8152a9718e0675b151244cbfd647ac7a3c.