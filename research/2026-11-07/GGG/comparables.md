# Comparables cuantitativos GGG · revisión 8 noviembre 2026
Cierres regulares del 6 noviembre: GGG $67,86; Nordson/NDSN $309,86; IDEX/IEX $226,99. Precios secundarios archivados, no multiplicadores de agregador heredados. Estados financieros primarios SEC completos y cálculos en comparables.py/json/csv.

## Definiciones comunes
Capitalización = precio × acciones básicas de la portada más reciente disponible: GGG160,375132m al7oct; NDSN55,699366m al18ago; IEX73,452801m al23oct. No se presentan como número exacto al6nov. EV simple = capitalización + deuda financiera contable corriente/no corriente − efectivo. Deuda/caja GGG104,479/139,818m al25sep; NDSN1.731,005/113,431m al31jul; IEX1.751,5/602,1m al30sep.

En los tres se excluyen del EV simple arrendamientos operativos, déficits pensionarios, caja mínima y contingente de adquisiciones. No hay ajuste positivo por NCI con valor de mercado desconocido; el NCI contable IEX es negativo$1,5m y no se convierte en caja. Esta es una métrica de comparación homogénea y limitada, no EV transaccional completo ni el puente DCF de GGG. Por eso GGG aquí no coincide con su DCF, que utiliza acciones diluidas y otras reclamaciones. Tampoco se resta nuevamente efectivo de adquisiciones ya cerradas.

TTM = FY2025 +9M2026 −9M2025, sin anualizar nueve meses. NDSN termina31jul2026; IEX30sep y GGG25sep. EBITDA comparable = EBIT GAAP + D&A reportada, conservando SBC y todos los costes restantes; no mezclar EBITDA ajustado distinto de cada compañía. CFO−capex es flujo después de intereses/impuestos y antes de adquisiciones, no FCFF. Se muestra además CFO−capex−SBC añadido en el estado de flujos como diagnóstico económico, no otra medida GAAP.

| Métrica, USDm salvo ratios | GGG | NDSN | IEX |
|---|---:|---:|---:|
| Capitalización |10.883,06|17.259,01|16.673,05|
| EV simple |10.847,72|18.876,58|17.822,45|
| Ventas TTM |2.310,24|2.979,80|3.658,30|
| EBIT GAAP TTM |619,57|800,96|763,90|
| Margen EBIT GAAP |26,82%|26,88%|20,88%|
| CFO menos capex |600,10|724,01|667,10|
| EV/EBIT |17,51x|23,57x|23,33x|
| EV/EBITDA GAAP |14,88x|19,90x|18,23x|
| Rendimiento sobre equity, caja menos capex y SBC |5,21%|4,06%|3,81%|

## Normalización operativa comparable
Para no ocultar distinto peso de adquisiciones, el cálculo incluye un segundo puente limitado a9M2026, conservando amortización adquirida, SBC y reestructuración:
- GGG: EBIT460,986 +8,9 de costes de adquisición/inventario −9 de devoluciones arancelarias =460,886; margen26,84%.
- NDSN: EBIT586,700 +1,110 de costes de compra +3,404 de ajuste de inventario =591,214; margen26,54%. La pérdida de inversión minoritaria es no operativa, no se elimina otra vez de EBIT.
- IEX: EBIT580,3 −3,0 de beneficio de contingencias/acuerdos legales =577,3; margen20,92%. No se eliminan los14,9m de reestructuración y cargos relacionados como si nunca se repitieran.

Estos puentes no equivalen a beneficios plenamente normalizados: licencias iniciales GGG no están desglosadas; la cobertura se somete a sensibilidad en su DCF. EBITDA elimina D&A de los tres, pero no demuestra reposición gratuita. La inversión física y la renovación intangible permanecen en la valoración principal. La carga de compra de clientes, patentes y marcas es distinta, por lo que la comparación EBIT/EBITDA se muestra conjuntamente, sin elegir sólo el múltiplo favorable.

## Adecuación y límites económicos de los pares
Nordson es el referente industrial más directo por adhesivos, dosificación y precisión, especialmente frente a Valco. No es un competidor puro: contiene Medical and Fluid Solutions y Advanced Technology Solutions, con exposición médica/electrónica que modifica crecimiento y valoración. IDEX combina fluidos, bombas, dosificación y nichos industriales con Health & Science Technologies; ese segmento no equivale íntegramente a salud y también incluye óptica/semiconductores. Se usan sólo como comparables, no se proponen como candidatas elegibles ni se modifica ninguna exclusión sectorial del usuario.

Perímetros: Nordson incorpora Atrion y otras compras previas; CapstanAG de marzo2026 se declara no material. IDEX incorpora Mott y Micro-LAM, esta última comprada29jul2025 por aproximadamente$80,7m netos de efectivo; su aportación anualiza en elTTM. Graco sólo incorpora Valco desde31ago2026. No sustituir el TTM histórico de Graco por EBITDA de año completo inventado: su pro forma ofrece beneficio neto, no EBIT/CFO, y el PPA sigue provisional. IEX reporta crecimiento orgánico9M6% y Q3 8%, frente GGG9M−1% y Q3 4%; el descuento de múltiplo no demuestra igual expectativa de crecimiento. Nordson cierra su trimestre fiscal dos meses antes, otra diferencia que no debe esconderse.

El descuento de GGG frente a estos pares existe en métricas comunes, pero es sólo contraste, no aprobación de $67,86. Aplicar mecánicamente la mediana de pares importaría mezcla médica/electrónica, crecimiento, calendario y amortización de adquisiciones distintos. El DCF financiado continúa en$32,10/$48,70/$78,29 y approved_values=null. Se cierra la obtención cuantitativa pendiente; permanecen incertidumbres económicas declaradas; la auditoría mecánica no las resuelve.
