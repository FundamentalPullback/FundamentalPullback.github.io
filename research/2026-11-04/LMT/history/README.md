# Lockheed Martin: historia primaria, corte 4 noviembre 2026

USD millones salvo EPS (USD/acción) y margen (decimal). No valoración ni recomendación. Incluye FY2023–25, cuatro trimestres recientes Q4 2025–Q3 2026, comparativos 2025, períodos acumulados y TTM actual/anterior.

Ejecutar `python build_history.py` con Python estándar. Lee únicamente `numerical_inputs.json` y `input_lineage.json`; regenera CSV, JSON, lineage final y QA, sin conexión ni filings completos. 109 comprobaciones pasan: puente segmento–EBIT GAAP, NI, períodos acumulados, comparativo entre fuentes y TTM contra suma de cuatro trimestres. Los pequeños extractos de tablas permiten auditar cada input; índices de tablas/columnas son base cero. `sources.json` identifica las URL originales. Archivos enteros SEC/IR no se incluyen.

## Hallazgos y definiciones

- TTM Q3 2026: ingresos 79.116; EBIT consolidado GAAP 9.316; beneficio neto 6.513; CFO 10.112; capex 1.731; CFO−capex 8.381; SBC 358; D&A 1.686. TTM comparable Q3 2025: 73.349; 6.096; 4.200; 6.361; 1.768; 4.593; 263; 1.683, respectivamente.
- EBIT es operating profit consolidado GAAP. Incluye el FAS/CAS operativo y las partidas corporativas. Segment profit es otra métrica, no GAAP. El archivo separa sus componentes con signo para reproducir el puente.
- `fas_cas_operating_adjustment` es el beneficio de CAS menos el coste FAS de servicio. `nonservice_pension_income_signed` está por debajo del EBIT. Su suma es `fas_cas_total_adjustment`; no restar ambos al EBIT. FY25 contiene un cargo de settlement no operativo de 479 (377 después de impuestos), separado en `program_and_pension_items.json`.
- CFO−capex es FCF mecánico/definición del emisor, NO owner earnings. Capex incluye compra/desarrollo de software de uso interno. No sumar otra vez software. La reclasificación de software al PP&E en balances 2026 no implica un nuevo desembolso. No se establece mantenimiento frente a crecimiento.
- D&A proviene del ajuste agregado del estado de flujos. Ya incorpora amortización intangible; no agregar la amortización intangible por segunda vez. SBC proviene del estado de flujos, no del movimiento total de equity.
- Los add-backs de pérdidas anticipadas sobre programas son 45/1.965/1.615 en FY23/24/25. Los cargos de 1.615 de Q2 2025 se separan entre programa clasificado (950), CMHP (570) y TUHP (95). El efecto contable inmediato no es equivalente a caja libre: la ejecución futura consume caja. `program_and_pension_items.json` no pretende ser inventario exhaustivo de costes.
- CFO FY25 refleja aportación de pensiones de 860 en Q4. No se añade automáticamente al FCF, ni se confunde con el settlement contable de 479. El TTM actual conserva esa aportación y ese cargo no operativo.
- EPS trimestral y anual es el publicado directamente. EPS TTM se deja null: no se suman EPS ni se impone un denominador sintético.
- Null significa no establecido para ese campo/período. No significa cero. Algunas partidas especiales tienen importes conocidos en el fichero separado, pero no una serie trimestral/acumulada completa; por prudencia no se fuerza una resta parcial.

## Períodos y construcción

FY termina el 31 de diciembre. Q1 2026 termina 29 marzo; H1 el 28 junio; 9M/Q3 el 27 septiembre. Comparativos 2025: 30 marzo, 29 junio, 28 septiembre. 9M2024 termina 29 septiembre. Q1 2026 tiene 12 semanas frente a 13 en Q1 2025; no se ajusta la cifra publicada.

Ingresos, EBIT, NI y EPS de cada trimestre se toman directamente de estados/release. Cash flow, D&A y SBC de Q2 = H1−Q1; Q3 = 9M−H1; Q4 = FY−9M, conservando CFO/capex publicados directamente cuando están disponibles y comprobando la resta. TTM26 = FY25+9M26−9M25; TTM25 = FY24+9M25−9M24. Campos con signo conservan su presentación original; capex es salida positiva. `ebitda_mechanical` = EBIT GAAP+D&A, sin normalización.

## Entregables

`PUBLIC_FILES.txt` lista exactamente los archivos que pueden entregarse. No incluye HTML completos, cachés ni scripts de descarga. Todos los inputs para reconstruir resultados están incluidos.
