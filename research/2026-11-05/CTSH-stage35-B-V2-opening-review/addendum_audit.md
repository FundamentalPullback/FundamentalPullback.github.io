# Auditoría del addendum · CTSH B V2

**Dictamen: conforme.** La aclaración no reactiva la propuesta, no cambia sus límites ni modifica A268. Se verificaron 43 comprobaciones, todas satisfactorias.

## Alcance de la regla

El plan canónico, página 13, Stage 3.5 §4, establece: «Superar el máximo autorizado suspende la compra hasta nueva evaluación. Esperar consolidación o revisar con evidencia fundamental nueva; no perseguir una subida por obligación.».

El máximo autorizado es 65,78 USD, menor que el fundamental de 66,50. La apertura y la primera vela superaron ambos. La clasificación correcta sigue siendo **suspendida, pendiente de nueva evaluación documentada**, no cancelación terminal ni deterioro demostrado del negocio.

Ese episodio de precio, por sí solo, no obliga a rehacer un DCF completo ni impone una espera fija. Una revisión futura puede ser breve, pero debe comprobar de forma sustantiva la consolidación o estructura, la vigencia de tesis y límites, una señal todavía prospectiva y el riesgo. Volver a la banda no reactiva automáticamente esta propuesta. Elevar el techo fundamental requeriría evidencia fundamental y revisión; la subida de precio no basta. Este addendum no realiza ni aprueba esa reactivación.

La ventana de quince minutos y la única oportunidad inicial son convenciones de B V2, no requisitos universales ni ventajas estadísticas demostradas.

## Reconsulta verificada

- Yahoo: **67,275 USD a las 09:51:02 EST del 5 de noviembre de 2026**, por encima de ambos límites. No es un bid/ask ejecutable certificado.
- El registro de captura sitúa el inicio de consulta a las 14:51:13 UTC y la recepción a las 14:51:31 UTC. La cronología es coherente; la hora de mercado se comprobó directamente en el raw.
- Primera vela completa 09:30–09:45 EST sin cambios: **O 67,1200 / H 67,8572 / L 66,4053 / C 66,5975 / V 401.797**. Los cinco valores coinciden exactamente con la instantánea anterior y con el registro observado.
- La vela siguiente aún estaba en formación. No se usa como una nueva señal.

La reconsulta confirma estabilidad dentro de Yahoo, no coincidencia exacta entre proveedores. Se conserva la discrepancia del mínimo diario de metadata, 66,53, frente al mínimo de la vela, 66,4053; no cambia la conclusión. La auditoría anterior ya separa la corroboración del exceso sobre 66,50 de una validación independiente del OHLC completo.

## Integridad y límites de esta auditoría

El registro de evento conserva la identidad A278 / CTSH-20261105-B-V2 y la condición de suspensión. Los dos archivos de observación y los dos de auditoría anteriores mantienen sus hashes originales y no se han modificado. No se certifican órdenes, fills, reactivación ni conciliación de cuenta. No se realizó una nueva consulta de red ni publicación.

Fuentes: [plan canónico](https://fundamentalpullback.github.io/data/plan/Plan_Completo_2026-10-30.pdf) y [consulta Yahoo](https://query1.finance.yahoo.com/v8/finance/chart/CTSH?range=1d&interval=15m&includePrePost=false). Los hashes completos de los archivos revisados y las comprobaciones reproducidas constan en `addendum_audit.json`.

Raw Yahoo de la reconsulta, SHA-256: `d190f818c7040d37e1064c31ac618b5ba176441b3d6577bccab872bebd0e0bdf`.
