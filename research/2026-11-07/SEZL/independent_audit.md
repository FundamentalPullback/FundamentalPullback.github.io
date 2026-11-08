# Auditoría independiente de SEZL v1

Resultado: puente histórico aprobado aritméticamente; investigación parcial. No se aprueba valoración, entrada ni operación. Se mantienen los bloqueos prospectivos de capital distribuible y FCFE. Se revisaron informe MD/HTML, modelo, resultados, historia, estado, QA, manifiesto y archivos primarios. No se modificó la versión congelada.

## Resultados verificables

- 54 comprobaciones pasan con `python checks.py`, incluyendo todos los hashes del manifiesto y ejecución del modelo en una carpeta temporal, sin alterar el original.
- Beneficio neto TTM septiembre 2026: 133,130 − 90,439 + 139,893 = USD182,584m. Los cuatro trimestres concilian.
- Caja TTM después de compras y originaciones netas de préstamos y capex: 298,563 − 237,550 − 3,851 = USD57,162m. TTM anterior: 196,675 − 140,086 − 2,509 = USD54,080m. Esta caja histórica antes de financiación no es FCFE distribuible: faltan financiación sostenible, liquidez y capital exigidos, garantías, covenants y capital bancario potencial.
- Flujos anuales y acumulados concilian con las tablas archivadas. CFO 2023 conserva clasificación original y no se presenta como comparable. La reformulación traslada compras/originaciones netas a inversión sin crear caja. El 10-Q mantiene la debilidad material de control de clasificación.
- Mora: (14,749 + 14,986) / 355,529 = 8,3636%; anterior (8,274 + 9,841) / 283,400 = 6,3920%. Son saldos con 29–56 y 57–90 días sobre coste amortizado bruto total, NO proporción de prestatarios ni pérdida acumulada de cohortes. Se debe explicitar el denominador en el informe. La clave del modelo `29_plus` sería más precisa como `29_to_90`.
- Reserva: 28,505 + 81,949 − 78,441 + 7,598 = USD39,611m; préstamos netos USD315,918m; castigos netos USD70,843m. Provisión no se trata como beneficio económico gratuito.
- Caja total USD107,864m = USD70,142m no restringidos contablemente + USD37,722m restringidos. Los USD19,610m de la VIE no son caja corporativa libre; tampoco se demuestra que los USD50,532m restantes sean excedentes.
- Principal USD104m frente a capacidad nominal USD300m y valor contable neto USD102,178m. Confirmados anticipo 92,5% que puede bajar al 85%, elegibilidad inferior a 30 días, SOFR 3 meses + 3,86%, suelo 2%, comisión no dispuesta 0,5% y mínimo USD50m. Cumplimiento declarado no cuantifica holgura. Restricciones del SPE y pruebas financieras corporativas no deben confundirse.
- Caja 9M antes de financiación USD82,339m; tras deuda y comisiones USD43,916m. Más opciones USD1,063m, menos recompras USD39,360m y divisas USD0,356m explican aumento total de caja de USD5,263m hasta USD107,864m.
- Compras comprometidas al originador: USD27,8m de valor contable y USD36,1m de pedidos. No se afirma transferencia total del riesgo en el acuerdo WebBank. Contratos y riesgos retenidos siguen pendientes; el 10-Q incluye referencias a contratos de marketing/servicing y venta de préstamos de agosto de 2026.
- Solicitud de licencia y seguro de depósitos, no aprobación. El 10-Q exige capital significativo si se establece el banco, además de costes; no hay monto cuantificado. No se halló afirmación fabricada de aprobación o financiación bancaria gratuita.
- Split 6:1 efectivo 28 de marzo de 2025 confirmado. EPS 2023 ajustado una vez; acciones actuales 33,783402m no se confunden con promedio diluido Q3 de 34,753m. SBC permanece como coste económico.
- USD149,43 cierre regular y USD150 posmercado coinciden con el registro de evidencia secundario archivado. No se volvió a consultar un proveedor en esta auditoría; el registro conserva valores y URLs, no respuesta íntegra del buscador. Por ello la verificación de precio es de consistencia documental, no nueva confirmación independiente de mercado.

## Correcciones antes de una revisión pública

1. CFO 2024 originalmente publicado: USD40,899m en tabla del 10-K reformulado; el informe dice USD40,900m. Diferencia de USD0,001m sin efecto en el modelo, que usa correctamente USD130,648m reformulados.
3. Explicitar el denominador y los dos intervalos de mora. Cambiar «originaciones netas» por «compras y originaciones de préstamos, netas de cobros» mejora precisión frente a la partida SEC.

## Límites

No se completó SBC TTM anterior ni homogeneización CFO 2023. Ninguna carencia se transformó en cero. No hay escenarios FCFE, valoración inversa ni capital distribuible aprobado. QA visual Chromium sigue sin realizarse según el bloqueo documentado; esta auditoría leyó el HTML sin ejecutarlo ni intentar eludir restricciones. No se hicieron escrituras remotas, publicaciones ni operaciones.

Congelación auditada: `v1_partial_frozen`, 2026-11-08T02:42:47.260207+00:00. SHA-256 del manifiesto: `153838d9b635abe2ee2b99a45a6899aa2c5025c58f12719dc677a3c3bbae8fa4`. Los 35 archivos enumerados permanecieron conformes al manifiesto al ejecutar las comprobaciones.

## Verificación posterior de v2


Verificación final: incorporada también la precisión «Compras y originaciones netas de cobros». Las 54 comprobaciones pasan sobre v2_1_partial_audit_corrections_frozen; 39 archivos conformes. SHA-256 definitivo: `48beb2b33b9d9db1e30b1ba9aa3bf7a3f9af4eeeb616e6e569e1ed32cbad98a7`.