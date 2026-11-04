# VFC — control del modelo y datos

4 de noviembre de 2026. Revisión analítica reproducible, no auditoría estatutaria.

- Historia: 845 filas con origen; 137 comprobaciones de cifras y puentes, con un redondeo expresamente identificado de $0.001m.
- Modelo: 256 comprobaciones de una segunda implementación de fórmulas, sin importar ni ejecutar model.py. Pasan escenarios, años, terminal, valoración inversa y sensibilidad fiscal.
- Central $10.648646; favorable $22.083215; constructivo $22.081529. Inversa constructiva: crecimiento 2.920027%, condicionado al resto de sus supuestos.
- SBC permanece dentro de EBIT. No hay doble deducción ni devolución de SBC en FCFF. Capex de expansión se calcula después de separar la inversión en circulante.
- Se corrigió el impairment de LEVI: $2.5m se cancela entre FY y 9M anterior; no se añade al TTM actual.
- Se incorporaron caminos fiscales consistentes con la aspiración de dirección, sin equiparar automáticamente ETR contable e impuesto cash.
- Se corrigió la comparación con FCF de dirección: debe retirarse SBC antes de compararlo con FCFF económico. El presupuesto NTM de circulante no se presenta como guía de la empresa.
- Para comparar EV/EBIT se usa EV financiero estándar consistente, separado de los claims adicionales del DCF.

Eliminar conjuntamente la reserva fiscal analítica, el claim de reestructuración y la proxy de premios eleva central a $11.135921. Descontar los flujos explícitos a mitad de año da $11.171976. Estas alternativas no explican toda la diferencia con el cierre $20.04; tampoco hacen imposible el escenario constructivo.

La ausencia del carve-out exacto de caja Dickies y del timing completo de tarifas/proveedores sigue declarada. No hay una cifra ficticia de caja retenida normalizada. Incertidumbre de datos y supuestos no equivalen a error aritmético ni a aprobación de compra.

Reproducir: ejecutar model.py y después verify_model_independent.py. Los dos archivos operan localmente sin transacciones ni escrituras externas. Comparar independent_checks.json y los SHA-256 del manifiesto.
