# URBN: historia financiera reproducible al 4 de noviembre de 2026

## Alcance y unidades
- USD millones, salvo EPS en USD/acción. FY2026 termina el 31 de enero de 2026; Q2FY2027 termina el 31 de julio de 2026.
- Tres ejercicios FY2024/FY2025/FY2026; últimos cuatro trimestres y cada comparable; H1 actual y anterior; TTM hasta julio de 2026.
- `periods.json/csv`: ingresos, EBIT, beneficio neto, EPS básico/diluido, CFO, compras de PPE, SBC, D&A y FCF definido como CFO menos PPE.
- `balances.json/csv`: balances de enero de los tres ejercicios y julio actual/comparable.
- `numeric_inputs.json`: valores de entrada y fuente, sin copiar filings completos. `ledger.json`: trazabilidad de directos y derivados. `custom_disclosures.json`: alquiler Nuuly y partidas extraordinarias separados.
- `build_history.py` reproduce offline usando solamente `numeric_inputs.json` y `custom_numeric_inputs.json`, ambos incluidos aquí. No lee ningún directorio `sources`, companyfacts completo ni HTML, y solo usa la biblioteca estándar de Python. `source_hashes.json` es procedencia histórica de las copias originales, no una dependencia de ejecución. No publicar los filings completos.

## Resultado TTM
Ingresos 6.474,380; EBIT 731,440; beneficio neto 569,063; CFO 715,886; PPE 420,675; FCF 295,211; SBC 31,154; D&A 140,766.

El TTM monetario es FY2026 + H1FY2027 - H1FY2026. Los ocho trimestres incluyen flujos derivados por diferencias de acumulados cuando no hay cifra directa. El EPS trimestral siempre es directo. Q4FY2026 y su comparativo Q4FY2025 proceden del Exhibit 99.1 del 25 de febrero de 2026: diluido 1,05/1,28 y básico 1,07/1,30.

La suma de los cuatro EPS diluidos trimestrales es 6,41 (básicos 6,50). Se presenta en campos separados `eps_*_sum_quarters`: es una suma aritmética con denominadores de acciones diferentes, no EPS TTM publicado por la compañía. Los campos de EPS TTM directo permanecen vacíos intencionalmente. No se resta EPS anual y acumulados.

## Separación contable esencial
Las compras de producto de alquiler Nuuly fueron 150,668 / 175,697 / 232,411 en FY2024/25/26. El producto de alquiler neto fue 294,544 en julio de 2026 frente a 246,413 en enero y 230,091 en julio de 2025. Está en Other assets, no en inventario comercial. La amortización de alquiler pasa por COGS; no se publica aquí una cifra separada porque las fuentes extraídas no la cuantifican. No sumar una amortización de alquiler estimada ni restar otra vez las compras de alquiler del CFO sin un puente explícito que evite doble conteo. El FCF de este archivo es CFO - PPE, con los efectos operativos de alquiler ya dentro del CFO reportado.

Q2FY2027 incluye un beneficio IEEPA de 100,105: 95,660 de reducción de COGS y 4,445 de interés. UK tax benefit: 16,225. Un EBIT analítico sin el crédito COGS sería 193,079 en Q2 y 635,780 TTM, pero no implica beneficio neto/EPS normalizado. No tratar todo el beneficio pretax como EBIT, ni asumir que el efectivo exacto recibido es 100,105. No se inventa un impuesto marginal para normalizar.

El Q4FY2026 también tiene una donación de 46,0 incluida en Other expense, debajo del EBIT. El release presenta NI ajustado 130,5 y EPS diluido ajustado 1,43, frente a GAAP 96,267 y 1,05. Para Q4FY2025, NI ajustado 98,1 y EPS ajustado 1,04 excluyen liberación de reservas fiscales. Mantener esos ajustes de management separados de cualquier normalización propia.

## QA
`qa.json`: identidades de balance, cotejo CFO/PPE H1 con la cara de estados, suma de componentes IEEPA, y reconciliación de los cuatro trimestres al TTM para siete métricas. Todos los tests pasan. Los datos son GAAP salvo campos que dicen explícitamente adjusted, proxy o suma.

## Fuentes principales
- https://www.sec.gov/Archives/edgar/data/912615/000119312526137916/urbn-20260131.htm
- https://www.sec.gov/Archives/edgar/data/912615/000119312526386468/urbn-20260731.htm
- https://www.sec.gov/Archives/edgar/data/912615/000119312526074606/urbn-ex99_1.htm
- SEC companyfacts CIK0000912615, con accessions y enlaces específicos en cada input.

## Comparativo TTM y cautelas adicionales
TTM julio de 2025: ingresos 5.832,231; EBIT 556,619; beneficio neto 475,424; CFO 590,066; PPE 191,276; FCF 398,790. Se calcula como FY2025 + H1FY2026 - H1FY2025.

No ajustar el EBIT por la donación de FY2026: está debajo de EBIT. Tampoco añadir automáticamente 46,0 al CFO/FCF. La clasificación, desembolso y efecto fiscal exigirían un puente específico. El NI GAAP sí recoge la donación y su fiscalidad.

Variación del activo de alquiler neto: julio2025→julio2026 +64,453; enero2026→julio2026 +48,131; enero2025→enero2026 +30,287. Usar fechas comparables por estacionalidad. Son cambios contables de saldo, no prueba autónoma de flujos exactos de caja: pueden existir disposiciones, FX u otros efectos. En un FCFF construido desde EBIT puede ser necesario financiar la inversión neta de alquiler, pero solo una vez y con una reconciliación que distinga el D&A de PPE de la amortización de producto de alquiler. Ese ajuste no se debe volver a aplicar al CFO ya reportado.

Inspección de nombres de todos los hechos inline XBRL de Q2/FY26: no aparece tag de amortización de producto de alquiler separado. Aparecen D&A genérica, depreciation de PPE, amortización de inversión de créditos fiscales y amortización de deuda/valores. No asumir que la D&A de 140,766 TTM incluye alquiler ni inventar un importe de amortización Nuuly.

## Reproducción pública verificada
Ejecutar `python build_history.py`. Para la prueba de portabilidad ejecutar `python test_portable.py`: crea un directorio temporal limpio, copia únicamente constructor y extractos numéricos (más el manifiesto histórico para verificar preservación), reconstruye los outputs y compara sus SHA-256 con `portable_baseline.json`. No hay carpeta sources ni acceso de red. `portable_test_result.json` registra el resultado: los nueve archivos comprobados son idénticos byte a byte a los originales, sin cambios en cifras. El manifiesto histórico no se vuelve a calcular a partir de archivos privados.
