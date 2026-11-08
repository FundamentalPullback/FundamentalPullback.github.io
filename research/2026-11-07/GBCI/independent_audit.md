# GBCI: auditoría independiente del paquete económico

Fecha: 8 de noviembre de 2026. **Apto para continuar investigación, no para decidir una operación.** Se mantiene `economic_partial`, sin valoración aprobada ni precio máximo de compra. Opportunity 70 supera el umbral de investigación autorizado de 65; no se utiliza 85 como veto automático. No se hicieron operaciones ni escrituras remotas.

## Resultado

La revisión del archivo r2 confirmó que todos los contenidos enumerados en su manifest coincidían con los archivos de trabajo antes de modificarlos. La comprobación independiente reproduce 20,02 / 33,29 / 48,83 USD por acción, la igualdad algebraica entre beneficio residual y dividendos teóricos, retención positiva y patrimonio final, y el ROE constante inverso de 13,089%. No detectó error material en estas fórmulas. No equivale a validar el capital distribuible.

Se corrigieron tres puntos del informe: ROE Q3 GAAP exacto 9,53% (antes, aproximación 9,6%); distinción entre distribución teórica y remesa regulatoriamente posible; base original del ERP mensual. No se cambiaron las hipótesis ni resultados del modelo.

Hay tres ejercicios, cuatro trimestres y dos TTM emparejados. La suma de los cuatro trimestres coincide con cada columna del TTM actual. Los gastos de adquisiciones identificados y las cifras pro forma de la nota 23 están separados de GAAP. No constituyen una normalización orgánica completa: faltan puentes de crédito, impuestos, acreción, costes recurrentes y acciones para todos los periodos.

## Fuentes y controles principales

- Patrimonio 4.339,861 millones ya incorpora AOCI negativo de 206,336 millones. No se libera AOCI automáticamente ni se agrega capital excedente. Las distribuciones del modelo retienen capital; no hay recompra gratuita ni adquisición futura gratis.
- ROE 2025 6,59% y Q3 anualizado 9,53% contrastados con documentos primarios. El 13,09% inverso supera ambos; depende de Ke y crecimiento, no es una predicción.
- FDIC: Glacier Bank, certificado 30788, junio de 2026. 8.445,984 / 24.860,896 = 33,972967%. Septiembre devuelve cero registros, no cero depósitos no asegurados. Se conservan archivos de consultas de otra entidad únicamente como evidencia rechazada; no alimentan el modelo.
- HTML primario Treasury: fila 6 de noviembre, columna 10 años, 4,86%, comprobada directamente.
- Nuevas consultas públicas de esta auditoría, no presentes en r2: Stock Analysis confirma cierre regular 48,16 USD el 6 de noviembre; Quantellect muestra beta 0,77 a cinco años mensual contra SPY. La búsqueda dirigida recuperó la beta después de un timeout de lectura. No se recalculó una regresión propia. Las diferencias de RSI y máximo entre proveedores no se utilizan para aprobar técnica.
- Damodaran: ERP del 1 de noviembre 4,41% sobre beneficios y reparto ajustado de doce meses. La página declara Treasury original 5,29%, ajustable a 5,07% con diferencial 0,22 puntos. Combinar ERP mensual con Treasury diario 4,86% es referencia híbrida 8,2557%; Ke central 10% sigue siendo juicio del analista.
- Calendario primario sin próximos eventos. No confirma la próxima fecha de resultados. Comunicado del 29 de octubre autoriza hasta 200 millones de recompras hasta el 31 de diciembre de 2027, sin obligación de ejecutar un mínimo. No se acredita recompra ejecutada.

## Bloqueos que permanecen

1. **Comparabilidad:** terminar normalización anual y TTM por adquisición y crédito, con denominadores de acciones consistentes.
2. **Hipótesis no justificadas:** conectar NIM, costes, pérdidas crediticias, ROE y retención con los escenarios, y justificar el recargo de Ke sobre referencia.
3. **Capital y liquidez:** construir estrés por entidad con RWA, CET1, AOCI, fuga de depósitos, pérdidas de valores, remesas legales y regulatorias y posibles emisiones. El estrés de beneficio de 132,30 millones no resuelve ese problema.
4. **Evidencia pendiente:** depósito no asegurado y concentración a septiembre; comparables homogéneos; causa de caída y validación técnica y de calendario antes de ejecución.

## Evidencia reproducible

`audit_checks.py` recalcula sin importar ni ejecutar el modelo original y produce `audit_checks.json`. `audit_web_evidence.json` y `audit_beta_search.json` preservan resultados nuevos de lectura pública y sus URLs. `manifest.json` identifica los archivos del cierre r3 mediante SHA-256. El archivo r2 permanece intacto. Los campos aprobados continúan nulos y no se incluye información privada de cartera o perfil.