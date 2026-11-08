# Auditoría independiente de TFC v2

Fecha: 8 de noviembre de 2026. Resultado: revisión parcial, no aprobada. Solo fuentes públicas y archivos locales. No se publicaron archivos, no se enviaron órdenes y no se realizaron operaciones.

## Hallazgos resueltos

1. El motor conservaba una escritura de financials.json con texto v1 obsoleto. Corregido: las cifras verificadas son entradas y el motor comprueba el TTM continuado sin sobrescribirlas. 
2. El TTM anterior de 4.915 era un subtotal válido, pero no el continuado final de 4.928. Ambos quedan diferenciados y el campo canónico actual es 5.608.
3. El ajuste RAC de 739 se desglosa mecánicamente en pérdidas de valores +1.447, retirada de liberación de reservas -581, costes de venta +106 e impuestos -346 +139 -26. No se añade solo la pérdida manteniendo la ganancia de reservas.
4. La sensibilidad del motor incorpora CAPM exacto 8,6967% y Ke 9,5%, antes presentes en la narrativa pero ausentes de la matriz ejecutable.
5. El informe explica la identidad valor = patrimonio cuando ROE = Ke y la ausencia de puente de OCI/AOCI y acciones futuras. No se presenta la igualdad de $46,78 como calibración empírica.

## Resultado de las comprobaciones

- Series 2023–2025: beneficio común menos discontinuadas más minoritarios discontinuados; preferentes ya deducidas. Continuadas -1.864 / -394 / 4.974. Ajustes definidos: +6.078 -204 en 2023; +5.089 en 2024; +15 en 2025. Resultado 4.010 / 4.695 / 4.989. La pérdida de valores residual 2024 de un millón permanece, según política explícita.
- TTM: 4.901 +13 +14 = 4.928; 4.869 +739 = 5.608. Crecimiento 13,7987%. No equivale a crecimiento orgánico de perímetro constante.
- Preferentes, SBC y amortización no se añaden indebidamente. Patrimonio común 56.061, preferentes 5.411, BVPS 46,78. Capital CET1 46.315 y RWA 431.752 son consistentes con 10,7% redondeado.
- La SCB 2,5% de octubre de 2025 rige hasta diciembre de 2027; el 10-Q actual explicita enero de 2028 y enero de 2029 para el cambio de calendario y promedio. No confundir esta cronología con una garantía de distribución.
- LightStream: préstamos 7.700, ingreso de venta previsto 7.200, capital estimado 850 = 70 +820 -40. La mayor parte es liberación por RWA, no efectivo libre; cierre esperado 4T26 condicionado y potencial reposicionamiento AFS. El informe trata correctamente el uso previsto para amortizar financiación mayorista.
- RI y DDM coinciden: $31,1866667 / $46,78 / $64,7723077. No hay deducción duplicada de deuda ni suma de caja regulatoria. Payout 75% en todos los escenarios es una hipótesis que no supera una prueba de estrés por el hecho de cuadrar.
- CAPM 4,86% +0,87 ×4,41% = 8,6967%. RF y ERP se verificaron directamente; beta 0,87 se corroboró en resultado indexado Yahoo, sin reconstrucción de retornos. Las primas prudenciales no son observables y pueden duplicar el estrés de ROE.

21 comprobaciones automáticas superadas mediante independent_audit.py, incluidos hashes de los 19 archivos originales y persistencia de financials.json tras ejecutar el modelo. Esto verifica aritmética y trazabilidad, no calidad económica suficiente para invertir.

## Verificación web independiente

Consultado el 8 de noviembre de 2026:

- https://stockanalysis.com/stocks/tfc/history/ : cierre regular del 6 de noviembre a las 16:00 EST $49,38; after-hours distinto $49,29. No se mezclan sesiones.
- https://ir.truist.com/events-and-presentation?item=92 : evento oficial de resultados 4T26, miércoles 20 de enero de 2027, 08:00 EST.
- https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve : fila 6 de noviembre, columna diez años 4,86%.
- https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm : ERP de noviembre 4,41%, TTM con payout ajustado. La propia página usa Treasury 5,29% para su cálculo mensual; combinarla con 4,86% diario es explícitamente una aproximación temporal, no una recalibración diaria de ERP.
- https://sg.finance.yahoo.com/quote/TFC/ : beta 5 años mensual 0,87 en índice de búsqueda; no se afirma haber reconstruido la serie.

## Bloqueos restantes

Capacidad de distribución y remesas al holding ligada a RWA, pérdidas, financiación y buffers de estrés; cierre y beneficios proforma de LightStream y cartera ex-RAC; OCI/AOCI y evolución de acciones; ausencia de guía numérica escrita posterior a BAAB y de guía anual 2027. No se elimina ninguno mediante una prima de descuento elegida por el analista.

La revisión documental y las correcciones mecánicas permiten conservar los diagnósticos, pero no aprobar Stage 3 ni precio de entrada. Estado final: partial, approved=false.