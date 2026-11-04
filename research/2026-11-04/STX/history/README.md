# STX: historia financiera normalizada, 4 noviembre 2026

Importes USD millones; EPS USD/acción; acciones millones. Estados GAAP consolidados de Seagate Technology Holdings plc. Sin previsión, DCF ni publicación.

## Entregables y reproducción
- `financial_history.csv` y `financial_history.json`: FY2024–FY2026; ocho trimestres Q2FY2025–Q1FY2027; Q1FY2025 auxiliar para conciliaciones; dos TTM hasta Q1FY2026/Q1FY2027.
- JSON incluye procedencia por métrica y operandos de cálculos. `source_numeric_extracts.json`, `additional_numeric_extracts.json` y `manual_release_extracts.json` son extractos numéricos compactos con URL primaria. `source_index.json` indexa 10-K/10-Q.
- Ejecutar `python rebuild_history.py` y `python validate_history.py`. Solo biblioteca estándar, sin red ni dependencias externas. Los scripts no necesitan filings completos.
- Base de ingresos/EBIT/NI/EPS/CFO/capex/SBC/D&A cargable. Campos complementarios nulos siguen siendo no disponibles, nunca cero supuesto. EPS de cada trimestre y FY son reportados directamente; EPS TTM es suma de cuatro EPS trimestrales, no un EPS TTM reportado ni NI dividido por acciones actuales. No sumar EPS trimestral para sustituir EPS anual.

## Calendario y comparabilidad
FY termina el viernes más próximo al 30 junio. FY2024 final28jun2024 y FY2025 final27jun2025 tienen52 semanas. FY2026 final3jul2026 tiene53; Q1FY2026 tuvo14 semanas. Q1FY2027 terminó2oct2026 y tuvo13. TTM comparativo tiene53 semanas, actual52. No ajustar mecánicamente la semana extra ni anualizar Q1 récord.

FY2024/2025/2026: ingresos6551/9097/12195, EBIT452/1890/4094, NI335/1469/3184, EPS1.58/6.77/13.90, FCF664/818/3105. TTM actual: ingresos13799, EBIT5464, NI4396, EPS suma19.04, CFO4832, capex675, FCF4157, SBC224, D&A280. TTM previo: ingresos9558, EBIT2181, NI1713, EPS suma7.79, CFO1520, capex302, FCF1218, SBC214, D&A259.

## Normalización y advertencias
1. FCF=CFO-capex; FCF después de SBC resta la compensación no monetaria del flujo de caja y es una sensibilidad económica, no GAAP ni FCF oficial. El TTM actual es3933 frente1004 previo. D&A ya figura en CFO: no volver a añadirlo.
2. Q1FY2027: SBC en CFO63, pero reconciliación no-GAAP excluye77 de compensación y cargos relacionados. Su definición incluye impuestos patronales sobre nómina. Diferencia14, no asumir que toda es SBC no monetaria. TTM:224 versus238. Conservar coste económico de la compensación; no usar automáticamente EBIT no-GAAP.
3. D&A FY2026=276 incluye amortización adquirida8, depreciación268. Intangibles adquiridos FY2025: amortización inmaterial, no cero exacto; FY2024 ninguna. Amortización adquirida Q1/Q2/Q3/Q4FY26=3/2/2/1; Q1FY27=2; TTM actual7. Ya está dentro de D&A, no sumar dos veces.
4. FY2024 NI incluye313 de ganancia por venta SoC y104 por terminación de swap. Su EBIT incluye beneficio neto30 en restructuring, ligado a sale-leaseback; cargos de cancelación de pedidos87. No tomar NI335 como run-rate limpio ni sumar indiscriminadamente un beneficio como cargo.
5. FY2025 restructuring de estado25 difiere del ajuste total no-GAAP38 por13 en coste de ventas; FY2026 estado y ajuste27. Q3FY2025 estado10 versus ajuste20; Q4FY2025 estado13 versus ajuste16. Mantener bases separadas. FY2025 cancelación de pedidos es beneficio9. Reconciliación EBIT no-GAAP menos SBC (solo puente descriptivo, no beneficio sostenible): FY24 550; FY25 1927; FY26 4237.
6. FY2026 incluye gasto legal105. Q3FY2026 contiene el cargo; en Q1FY2027 se transfieren105 a escrow/restricted cash. No tratar automáticamente el movimiento a efectivo restringido como gasto nuevo ni como deuda financiera. BIS: obligación original300, pagos trimestrales15 durante cinco años desde31oct2023. Comprobar los pagos en CFO; no sumar de nuevo como provisión íntegra.
7. Impuesto FY24/FY25/FY26=110/44/506; tipos efectivos24.72%/2.91%/13.71%. Cash taxes30/42/40. FY2026 CFO se beneficia de diferimientos y +528 en accrued expenses/income taxes/warranty. Pillar Two aumenta impuesto y hay beneficios discretos/OBBBA/compensación; no extrapolar2.91% ni caja fiscal40. Q1FY27 gasto221/pretax1982=11.15%; deferred taxes en CFO -57 y variación accrued expenses/income taxes/warranty +272.
8. Intevac adquirido31mar2025: consideración119, net cash used88;47 neto de liquidar inversiones adquiridas. Intangible19, goodwill2. Pro forma no presentado por inmaterialidad. No confundir cash acquisition con capex ordinario. FY2024 SoC vendido a Broadcom altera perímetro aunque no se ofrece historia pro forma comparable.
9. Pérdidas de transacciones de deuda FY24/25/26=29/7/151; TTM actual189. Van por debajo de EBIT. La emisión/conversión de exchangeables afecta denominador EPS y equity; no calcular EPS con acciones actuales ni mezclar número diluido GAAP con ajustes capped-call del no-GAAP. Q1FY27 termina sin principal exchangeable2028; el principal era186 al cierreFY26. Deuda se paga parcialmente en efectivo y exceso de conversión en acciones; la reconciliación patrimonial no es recompras inversas.
10. Reservas de inventario no extraídas como serie independiente: `inventory_provision=null`. Warranty issued FY24/25/26=53/68/114; TTM actual128, no equivale a gasto total de garantía ni a saldo de provisión. No liberar reservas hipotéticas como ajuste.

## Fuentes y calidad
10-K FY2026 (auditado, incluye FY24/25 comparativos): https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm
10-Q Q1FY2027 (no auditado): https://www.sec.gov/Archives/edgar/data/1137789/000113778926000309/stx-20261002.htm
Release Q4FY2026, cifras directas Q4FY25 y Q4FY26: https://www.sec.gov/Archives/edgar/data/1137789/000113778926000153/stxq42026pressreleasefinan.htm
Release Q4FY2025, ajustes FY24/25: https://www.sec.gov/Archives/edgar/data/1137789/000113778925000148/stxq42025pressreleasefinan.htm
Release Q1FY2027: https://www.sec.gov/Archives/edgar/data/1137789/000113778926000300/stxq12027pressreleasefinan.htm
Resto de 10-Q, URLs en cada extracto. Se detectaron cero conflictos numéricos entre períodos/contextos sin segmentos. La fecha IR es27oct2026; dateline EX99.1 dice28oct2026. Mantener discrepancia de fecha, no mover trimestre. Los estados de flujo de caja trimestrales Q2/Q3 se derivan de acumulados cuando no hay dato individual; Q4 CFO/capex son explícitos en release. Hay datos redondeados al millón, y no se debe atribuir exactitud superior.
