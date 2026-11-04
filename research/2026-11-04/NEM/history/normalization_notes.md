# NEM: historia financiera y límites de normalización
Fecha de corte: 4 noviembre 2026. USD millones; filings hasta Q3 2026. Fuentes y hechos mínimos: `financial_inputs.json`. Reproducir sin red con `python rebuild_history.py`; Los inputs mínimos permiten la reproducción offline; los originales y la herramienta de extracción no forman parte del paquete público. No hay filings completos en esta carpeta.

## Resultado
TTM Sep26: ventas 26.606; EBIT operativo reconstruido 13.793; NI consolidado 9.440; NI Newmont 9.240; CFO 13.098; capex efectivo 3.024; FCF CFO-capex 10.074. TTM Sep25: ventas 21.503; EBIT operativo 9.853; NI Newmont 7.187; CFO 9.224; capex 3.102; FCF 6.122. Son períodos reportados, no estimaciones prospectivas ni rentabilidad normalizada al precio de oro de ciclo medio.

EBIT operativo = ventas menos todos los costos y gastos que figuran antes de Other income (expense). Incluye D&A, reclamation, exploración, advanced projects/R&D, G&A, impairment, ganancias/pérdidas de venta y Other expense. Excluye intereses, rendimientos de inversiones y otros resultados no operativos; también excluye equity income of affiliates, presentado después de impuestos. Se reconcilia para cada período al pretax antes de afiliadas mediante Nonoperating income/expense. NI+tax+interest no es sustituto adecuado.

Normalización PARCIAL de EBIT = EBIT operativo + línea separada de impairments + pérdida/(ganancia) de activos held-for-sale. TTM Sep26: 14.638; Sep25: 9.125. No se presenta como EBIT recurrente definitivo. Los pequeños write-downs contenidos en Other expense, reclamation revisions, reestructuración, proyectos, impuestos, mix de minas, grados y precios no están íntegramente normalizados. Se mantienen exploración, G&A y D&A: minería consume reservas y requiere reinversión. No se inventan impuestos normalizados ni NI ajustado.

## Caja y SBC
FCF = CFO menos capex efectivo, no EBITDA menos sustaining capex. Las ventas de minas/otros activos están en inversión (FY25 2.811; 9M26 99; 9M25 2.789), no se añaden al CFO ni al FCF recurrente. Una ganancia contable se elimina en la reconciliación de CFO; no volver a sustraerla del CFO. Impairments son no monetarios: su reversión en EBIT no genera nueva caja ni permite sumarlos otra vez al CFO.

FY23/FY24 CFO total incluye 9/45 de operaciones discontinuadas. FCF de operaciones continuas es 88/2.916 frente al FCF simple 97/2.961. FY25 y períodos 2025/2026 sin ese diferencial. Las ventas de activos held-for-sale no equivalen automáticamente a operaciones discontinuadas.

SBC FY23/FY24/FY25: 80/89/99, corroborado por nota 12 y cash flow, incluye proporción NGM. Q4 FY25 = 28 por diferencia con 9M25 de 71. SBC 2026 no se aísla de Other non-cash adjustments: null para Q1/Q2/Q3 y TTM. No se usa emisión de acciones, APIC o retenciones fiscales como proxy de gasto. SBC capitalizada no separada: null, nunca cero. No hay FCF ajustado por SBC 2026 por falta de dato fiable.

## Capex y reclamation
Desglose sustaining/development es DEVENGADO, mientras capex del cash flow es EFECTIVO. FY25: desarrollo 1.312 + sustaining 1.755 = 3.067 devengado; ajuste -32 => caja 3.035. 9M26: 967 + 1.383 = 2.350; ajuste -134 => caja 2.216. TTM: desarrollo devengado 1.278 + sustaining devengado 1.906 = 3.184, frente a 3.024 caja. No imputar el ajuste completo a sustaining ni development. Ambos desgloses de caja permanecen null. Los componentes AISC incluyen arrendamientos y otra definición: no sustituyen este puente.

Reclamation/ARO no es mero impairment. Incluye actualización de obligaciones, acreción y gasto real de cierre/remediación. 9M26 registra gasto reclamation/remediation 358, ajuste no monetario CFO 339 y cambio negativo de obligaciones en CFO de 714. Nota 6 identifica 667 pagados para ARO y 47 de remediación, que suman 714. No eliminar estos pagos para inflar caja recurrente. Tampoco descontar íntegramente ARO en equity bridge si el DCF ya incorpora los mismos pagos sin una reconciliación explícita.

## Perímetro
- NGM 38,5% se consolida proporcionalmente, no al 100%. Su producción/costos ya están en las partidas consolidadas. No sumar otra vez un valor completo o multiplicar todo Newmont por 38,5%.
- Pueblo Viejo 40% es equity method: aporta beneficio de afiliadas, no ventas/EBIT consolidados de mina. Sus onzas sí figuran en producción atribuible. Compras y reventas de su oro/plata se presentan netas, inmateriales, en Other income. No añadir ingresos teóricos por producción atribuible a las ventas consolidadas.
- Merian 75% es consolidado y genera NCI. La relación NI consolidado menos NCI igual NI Newmont se verifica para todos los períodos. CFO-capex consolidado no equivale exactamente a caja atribuible al accionista: distribuciones/aportaciones de NCI y afiliadas precisan puente separado. Fruta del Norte también explica diferencia entre producción atribuible y consolidada.
- Newcrest se incluye desde 6 noviembre 2023, pero todo 2024 y 2025. FY23→FY24 no es crecimiento orgánico comparable; tampoco se reconstruye un pro forma de mina constante sin suficientes estados.
- Telfer/Havieron sale en diciembre 2024. CC&V, Musselwhite, Éléonore, Porcupine y Akyem se venden en 2025. Porcupine/Akyem cierran 15 abril; Musselwhite/Éléonore 28 febrero. FY25/9M25 incluyen operaciones anteriores a esas ventas, 2026 no. FY25→TTM26 mezcla desapalancamiento del perímetro, oro y desempeño operativo; no aplicar un crecimiento bruto como runway normalizado.
- Ahafo North comienza producción comercial en octubre 2025; el split previo entre desarrollo y operación difiere. No tratar reducción del capex de desarrollo como ahorro permanente sin calendario de proyectos.

## Controles y limitaciones
Las cifras trimestrales de cash flow se obtienen por diferencias acumuladas: Q4=FY−9M, Q2=H1−Q1, Q3=9M−H1. TTM=FY previo+9M actual−9M previo. Últimos cuatro trimestres concilian exactamente con TTM para todos los campos no nulos. El archivo checks.txt registra controles de NCI, EBIT y TTM.

No se ha probado un EBITDA/FCF económico de ciclo medio, un perímetro same-mine, impuestos normalizados, SBC capitalizada o sustaining capex de caja. Esos campos no deben presentarse como hechos. Los hechos de estados históricos son auditados a nivel anual y no auditados a nivel interino; el cálculo de EBIT/normalización es analítico, no un subtotal GAAP publicado ni la métrica ajustada oficial.
