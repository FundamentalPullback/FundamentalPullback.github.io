from pathlib import Path
import json
P=Path(__file__).parent;R=json.load(open(P/'model/results.json'));H=json.load(open(P/'history/history.json'))
release='https://www.sec.gov/Archives/edgar/data/4127/000000412726000052/q426earningsreleaseformex9.htm'
remarks='https://www.skyworksinc.com/-/media/SkyWorks/Documents/Press-Releases/FY26Q4-Earnings-Call-Prepared-Remarks.pdf'
f25='https://www.sec.gov/Archives/edgar/data/4127/000000412725000085/swks-20251003.htm'
q3='https://www.sec.gov/Archives/edgar/data/4127/000000412726000049/swks-20260703.htm'
q1='https://www.sec.gov/Archives/edgar/data/4127/000000412726000008/swks-20260102.htm'
q2='https://www.sec.gov/Archives/edgar/data/4127/000000412726000015/swks-20260403.htm'
q424='https://www.sec.gov/Archives/edgar/data/4127/000000412724000100/q424earningsreleaseformex9.htm'
close='https://www.sec.gov/Archives/edgar/data/4127/000110465926113538/tm2626934d1_8k.htm'
pf='https://www.sec.gov/Archives/edgar/data/4127/000110465926089381/tm2620808d3_ex99-2.htm'
exchange='https://www.sec.gov/Archives/edgar/data/4127/000110465926114359/tm2626934d2_8k.htm'
financing='https://www.sec.gov/Archives/edgar/data/4127/000110465926093358/tm2622643d2_425.htm'
transcript='https://finance.yahoo.com/markets/stocks/articles/skyworks-swks-q4-2026-earnings-152938011.html'
qorvoq='https://www.sec.gov/Archives/edgar/data/1604778/000162828026050149/earningsrelease20260627.htm'
qorvoy='https://www.sec.gov/Archives/edgar/data/1604778/000162828026030523/earningsrelease20260328.htm'
hist='\n'.join('| '+ ' | '.join([x['period'],f"{x['revenue']:,.1f}",f"{x['ebitGAAP']:,.1f}",f"{x['epsDiluted']:.2f}",f"{x['cfo']:,.1f}",f"{x['capexPPE']+x['purchasedIntangibles']:,.1f}",f"{x['fcfAfterPurchasedIntangibles']:,.1f}",f"{x['sbc']:,.1f}"])+ ' |' for x in H)
cases='\n'.join(f"| {name} | {R['cases'][k]['operatingEV']:,.0f} | {R['cases'][k]['illustrativeEquityResidualPerShare']:.2f} | {R['cases'][k]['terminalWeight']:.1%} |" for name,k in [('Adverso','bear'),('Central','base'),('Favorable','bull')])
reverse='\n'.join(f"| {x['matureMarginAfterSBC']:.0%} | {x['growthYears2to5']:.1%} |"for x in R['reverse'])
sens='\n'.join(f"| {x['wacc']:.1%} | {x['g']:.1%} | {x['operatingEV']:,.0f} | {x['illustrativeResidualPerShare']:.2f} |"for x in R['waccGrowthSensitivity'])
text=f'''# Skyworks (SWKS): una compañía combinada que todavía no tiene caja normalizada certificada

Corte de información: 4 de noviembre de 2026, después del cierre de EE. UU. USD millones, salvo precios y EPS; acciones en millones. Investigación parcial condicionada. No es Stage 3 completo, valoración total de la acción ni aprobación de entrada.

## Conclusión

La combinación con Qorvo amplía tecnología y diversificación, pero no corrige por sí sola el deterioro del legado: FY26 de Skyworks registra ventas −3,1%, EBIT GAAP −56,7% y CFO −57,7%. Tras incluir inversión en intangibles, FCF baja de 1.075,9 a 198,8; tres de los cuatro trimestres de FY26 son negativos. La mejora de mix y las sinergias tienen que convertirse en caja, no sólo en EPS ajustado. [Resultados oficiales FY26]({release}).

La operación cerró el 5 de octubre, después del cierre contable del 2 de octubre. Por eso los resultados publicados son de Skyworks independiente, mientras que la guía de diciembre corresponde al combinado y utiliza aproximadamente 241 millones de acciones diluidas. Aplicar el beneficio o balance independiente a la acción combinada produce una conclusión falsa. [Cierre]({close}) y [explicación de la dirección]({remarks}).

Decisión: **en observación por recuperación y perímetro/capital sin cerrar**. No hay valor razonable total, descuento de seguridad ni máximo condicionado aprobados. Los ejercicios numéricos de este informe sirven para contrastar qué tendría que ocurrir; no son precios objetivo. El bloque no resuelto no se arregla con una posición pequeña.

## Scanner, precio y criterio de selección

Scanner del 4nov: Last 82,65; QP 60; Opportunity 85; RSI 49,6; máximo 52 semanas 92,7999; margen operativo LTM 7,227%; FCF/acción 2,73; PER 42,82. Se conserva la observación original, pero el margen y FCF del scanner no coinciden con las cuentas recién publicadas ni resuelven el perímetro. El margen FY26 independiente es 5,47%, y FCF tras inversión en intangibles por acción diluida es 1,32. No sustituyen métricas combinadas inexistentes.

Stock Analysis muestra cierre regular 82,96 a las 16:00 EST del 4nov, distinto del scanner y del after-hours. Otro proveedor consultado mostraba 82,92; se conserva la pequeña discrepancia sin certificar un feed de ejecución. El cierre de Stock Analysis cae 2,86% frente a 85,40 del 3nov; la caída intradía o after-hours inicial no es ese retorno. [Histórico fechado](https://stockanalysis.com/stocks/swks/history/). El modelo inverso utiliza 82,65 sólo para mantener la referencia del scanner.

QP 60 no es veto automático ni Opportunity 85 aprobación. No se ha reconstruido la serie de EMA20/EMA50 para certificar Stage 2 vigente; queda nulo. La regla canónica pide precio > EMA50 y EMA20 > EMA50, no EMA50 > EMA200. No hay Stage 3.5, ticket, tamaño, stop ni operación.

## Negocio y causa de la caída

Skyworks diseña y fabrica RF, timing y soluciones analógicas. Qorvo añade filtros, RF GaN, potencia y broadband. La integración puede mejorar contenido por dispositivo y diversificación, pero quedan competencia, concentración de compradores, presión de precios, riesgo de perder sockets y costes industriales. No debe valorarse como software recurrente ni como una exposición pura a IA.

En el último trimestre independiente, Broad Markets vendió aproximadamente 416, creció 9% y representó alrededor del 40% de ventas; el mayor cliente fue aproximadamente 62% incluyendo productos no smartphone. En el combinado FY26, la dirección presenta Smartphone aproximadamente 4.600, −11%, y Diversified Growth Markets aproximadamente 2.900, +12%. Son categorías pro forma redondeadas, no un estado financiero consolidado auditado. La nueva mezcla mejora el potencial, pero el bloque smartphone sigue pesando más. [Comentarios oficiales, pp. 2–4]({remarks}).

La caída está asociada a una guía débil y riesgos conocidos de Android/contenido, no a una mera corrección técnica sin deterioro. No se ha recuperado un consenso homogéneo previo para cuantificar una sorpresa combinada: tampoco se compara la guía combinada de 1.850 con un consenso antiguo independiente. La publicación financiera de noviembre y el cierre de octubre son hechos materiales distintos.

## Historia: cuatro años de contexto y cuatro trimestres

TTM independiente al 2oct2026 coincide con FY26; su comparativo es FY25. FY25 tiene 53 semanas y FY26 52, por lo que los porcentajes no son crecimiento orgánico ajustado por calendario. Los tres ejercicios mínimos se amplían a FY23 para evidenciar caída desde un margen operativo de 23,6% hacia 5,5%; no se presume un ciclo completo ni reversión automática.

| Período | Ventas | EBIT GAAP | EPS diluido | CFO | PPE + intangibles | FCF calculado tras intangibles | SBC |
|---|---|---|---|---|---|---|---|
{hist}

FCF de esta tabla = CFO − compras de PPE − compras de intangibles, no FCFF normalizado. El nombre económico señala que incluye inversión adicional a PPE, no que todo el flujo sea distribuible. FY26 = 549,9 − 320,6 − 30,5 = 198,8. FCF/PPE convencional sería 229,3. Restar SBC deja −19,6 como diagnóstico de compensación, **no** una segunda deducción en el DCF ni sustituto de normalización.

Q2 y Q3 de caja se obtienen restando acumulados reportados; Q4 proviene del comunicado. Las cuatro ventas/EBIT/neto/CFO/SBC concilian con el año. PPE trimestral suma 320,7 frente a 320,6 anual; intangibles 30,6 frente a 30,5 y amortización 173,3 frente a 173,4: diferencias de redondeo de 0,1, preservadas. EPS trimestral no tiene por qué sumar EPS anual por denominadores ponderados y redondeo. [10-K FY25]({f25}), [Q1 FY26]({q1}), [Q2]({q2}), [Q3]({q3}) y [Q4/FY26]({release}).

## Beneficio sostenible, impuestos y conversión de caja

El beneficio GAAP FY26 de 172,1 y EPS 1,14 no son iguales al neto ajustado 762,1 y EPS 5,05. EBIT GAAP 216,7 llega a non-GAAP 849,8 mediante SBC 218,4, gastos de adquisición 132,9, amortización adquirida 140,7, liquidaciones/ganancias/pérdidas/deterioros 67,8 y reestructuración/otros 73,3. No se acepta todo el puente como caja recurrente.

Puente de trabajo seleccionado: 216,7 + 140,7 de amortización adquirida + 132,9 de gastos de adquisición = **490,3**, antes de impuestos, reteniendo SBC, reestructuración y deterioros. El comparable FY25, 500 + 153,3 + 5,4 = **658,7**, implica caída de25,6%. CFO identifica además66,2 de deterioro no monetario, pero no se ha verificado su correspondencia exacta con categorías del puente: retirarlo sólo como sensibilidad elevaría el EBIT a556,5, todavía15,5% inferior al comparable. Esta sensibilidad no es beneficio normalizado certificado. Excluir costes históricos no recupera el dinero gastado ni implica integración futura gratuita.

Una vista más estricta, agregando solamente amortización adquirida al EBIT GAAP, da FY24 798,5, FY25 653,3 y FY26 357,4. No se etiqueta esa serie como beneficio limpio completo: conserva costes de adquisición, deterioros y reestructuración desiguales. La gran categoría de ajustes FY24 no se borra automáticamente. [Reconciliación FY24]({q424}) y [reconciliación FY26/FY25]({release}).

El trimestre tuvo beneficio fiscal 13,6 sobre beneficio antes de impuestos 9,8, elevando el neto a 23,4. No se perpetúa esa tasa. FY26 tiene impuesto contable 41,6 y cambios fiscales diferidos −90,6 en CFO; no equivalen a caja fiscal sostenible. El DCF usa20% central, cercano al19,5% contable anual independiente, y prueba18–23%, frente al10% de guía non-GAAP de un trimestre. No se certifica la futura mezcla fiscal combinada. No se añaden DTA ni beneficios fiscales de adquisición como caja extra.

La inversión en inventario consume 316,7 en FY26 frente a liberación 41,8 en FY25. Cuentas a cobrar aportan 103,5 frente a consumir 89,3; cuentas a pagar aportan 54,8, y otros activos/pasivos consumen 119,2. La suma de esas cuatro líneas es −277,6 en FY26 frente a +193,2, giro adverso de 470,8. No se recupera todo el inventario por decreto ni se anualiza Q1 CFO 395,5. Capex PPE aumenta 64,4%. Dividendos pagados 320,1 y recompras del programa 114,5 superan FCF 198,8 antes de retenciones fiscales de awards 42,9; autorizaciones futuras no se cuentan como recompra ejecutada. [Estado de caja]({release}).

## Qorvo: evidencia disponible y desfase que no debe ocultarse

Qorvo FY26 termina el 28mar2026: CFO 808,631; capex 129,070; FCF 679,561; SBC 136,070. Su trimestre al 27jun2026: CFO 139,493; capex 24,144; SBC 34,411. Frente al trimestre comparable, el TTM derivado de junio queda en CFO 765,179, capex 115,671, FCF 649,508 y SBC 128,006. [FY26 Qorvo]({qorvoy}) y [Q1 FY27 Qorvo]({qorvoq}).

Estas cifras son anteriores al trimestre de septiembre y usan un calendario distinto de Skyworks. No se suman al FY26 de Skyworks para proclamar un TTM combinado limpio. Para septiembre sólo se ha verificado ingreso Qorvo de 937, con aproximadamente 70 por una semana adicional. Faltan estados completos comparables, integración y balance real consolidado en los documentos recuperados. Las cifras redondeadas de ventas combinadas no rellenan esos huecos.

## Capital y operación: no contar dos veces financiación ni acciones

El 5oct cada acción elegible Qorvo se convirtió en 32,50 USD y 0,960 acciones SWKS. Awards no consolidados tienen conversión distinta que incorpora equivalencia de efectivo, por lo que multiplicar sólo acciones ordinarias no certifica toda la dilución. La referencia de 241 millones es guía de acciones diluidas Q1, no captable spot auditado. [8-K de cierre]({close}).

El efectivo/inversiones 2.606,1 y deuda contable 2.472,8 al 2oct son **independientes y anteriores al pago de compra**. Incluyen financiación de agosto: 800 al 5,00%, 600 al 5,75% y 600 al 6,25%; cupón anual agregado 112. Añadir otros 2.000 de caja y deuda sobre esos saldos duplicaría la emisión. [Financiación]({financing}).

El canje liquidado 7oct emite principal nuevo 1.424,901 y deja principal antiguo 123,520, total Qorvo 1.548,421. Las notas entregadas se cancelaron; no se suman otra vez. Más 500 de legado SWKS y 2.000 de agosto, el principal reconstruido es **4.048,421**, no deuda contable consolidada oficial. El cupón tampoco sustituye al coste marginal de deuda en WACC. [Canje]({exchange}).

El pro forma publicado con balances de julio mostraba caja 790 + 1.329 − 2.867 de consideración + 1.987 de financiación neta = 1.239; valores negociables 23, de ellos 14 no corrientes; deuda contable 3.931. Deuda neta incluyendo valores = 2.669. Son cifras ilustrativas de julio, no caja/deuda real del 5oct. El 8-K de cierre anuncia presentación posterior de estados adquiridos/pro forma; no se inventa la fecha exacta de esa publicación. [Pro forma oficial]({pf}).

En el ejercicio de sensibilidad se usa una **hipótesis redonda de derechos financieros netos de 3.500**, con pruebas 2.500/4.500, y 241 acciones con pruebas 238/245. No es una estimación certificada ni se construye mezclando principal de octubre y caja de julio. Debe cubrir deuda neta y reserva operativa elegida antes de emitir una valoración accionarial; contingencias, liquidez real, fees pendientes y dilución continúan sin conciliar. Los arrendamientos operativos se mantienen como gastos en márgenes/caja, sin volver a restar el pasivo de alquiler. No se infiere ausencia de otras obligaciones.

## Perspectivas y debate de la llamada

Guía Q1 FY27 combinada: ventas 1.800–1.900; central 1.850, de ellas Skyworks 1.070 y Qorvo 780. Frente a septiembre combinado 1.983 cae 6,7%; excluyendo semana adicional de 70, cae 3,3%. Es la última desagregación prometida. Gross margin non-GAAP 46–48%, OpEx non-GAAP 465–505, otros gastos aproximadamente 50, impuesto non-GAAP 10%, EPS 1,25 y 241 acciones. A centros, EBIT ajustado aritmético = 1.850 × 47% − 485 = 384,5, aproximadamente 20,8% de ventas; redondeo explica la conciliación aproximada al EPS. [Guía oficial]({remarks}).

La reconciliación prospectiva advierte SBC de 0,40–0,60 por acción e intangibles 0,45–0,65, más ajustes fiscales y otros desconocidos. No se llama a 1,25 beneficio del propietario ni se multiplica por cuatro para fijar un PER normalizado. Nuestro margen económico inicial central 14,5% retiene una carga ilustrativa SBC cercana al centro del rango, pero no es guidance GAAP.

La dirección espera sinergias OpEx de 150 en FY27, concentradas en segunda mitad, run-rate de 250–300 al salir del año y ≥500 anuales en 24–36 meses desde cierre. Aproximadamente dos tercios OpEx y un tercio COGS. No sumar 150 + 300 + 500: son medidas de período y ritmo del mismo programa. El objetivo de margen operativo 30–35% es non-GAAP, no margen después de SBC. [Preparados oficiales]({remarks}).

La transcripción secundaria aporta estos contrastes, sin sustituir las cifras oficiales:
- Craig Ellis, B. Riley, preguntó sobre crecimiento y margen. Phil Brace describió smartphones como negocio de crecimiento bajo de un dígito y mayor contribución de diversificados. Prueba: estabilidad de contenido y expansión real de DGM, no sólo mix por contracción móvil.
- Krish Sankar, TD Cowen, preguntó por adjudicaciones del mayor cliente. Brace no espera cambios en su proceso de compra ni menos competencia por el tamaño combinado. Prueba: nuevos sockets y retención, no asumir poder de fijación de precios.
- Gabriella Tulchinsky, por Morgan Stanley, preguntó por recompras/deuda tras eliminar dividendo. Philip Carter mantiene preferencia por recompras, pero también quiere reforzar caja. Prueba: reducción de deuda y FCF después de integración; una recompra no sustituye rentabilidad.
- Christopher Rolland, Susquehanna, pidió precisar calendario de ahorro. Carter confirmó concentración al final de FY27 y presión de costes que puede ocultar ahorros COGS. Prueba: margen/caja realizada y gasto de integración, no una cifra de run-rate sin coste.

[Transcripción del 3nov publicada el 4nov]({transcript}). No se repiten citas literales ni se convierte comentario sobre marzo en guía formal. La competencia incluye Broadcom, Qualcomm y Murata en partes del stack; los mercados de defensa, industria y automoción tienen ciclos y compradores distintos, de modo que no justifican transferir múltiplos sin homogeneizar.

## FCFF a diez años: contraste condicionado, no valor actual certificado

Se usa el marco canónico: cinco años detallados, cinco de transición; FCFF = EBIT después de impuestos + D&A productivo − capex necesario − Δcirculante − caja extraordinaria de integración. SBC permanece en margen; no se resta otra vez. Se excluye amortización adquirida del margen seleccionado y tampoco se añade otra vez en D&A. Se conserva amortización de intangibles operativos propios y su reposición dentro de inversión.

Ancla de ventas 7.500 procede de categorías redondeadas pro forma de la dirección. La estimación central FY27 de 7.400 es hipótesis propia, no guía anual ni simple anualización certificada de diciembre. La trayectoria no toma las sinergias como cheque adicional sobre márgenes que ya las incorporan.

| Hipótesis | Adverso | Central | Favorable |
|---|---|---|---|
| Crecimiento años 1–5 | −8%, 0%, 2%, 2%, 2% | −1,33%, 2%, 4%, 5%, 5% | 2%, 7%, 8%, 8%, 7% |
| Margen EBIT después de SBC años 1→5 | 12%→13% | 14,5%→22% | 16%→28% |
| Impuesto sostenible | 23% | 20% | 18% |
| D&A productivo / ventas | 6% | 6% | 6% |
| Capex necesario / ventas años 1–5 | 8% | 7% | 6,5% |
| Circulante / ventas incrementales positivas | 17% | 15% | 14% |
| Caja extra integración años 1/2/3 | 200/150/100 | 150/100/50 | 100/75/25 |
| WACC / crecimiento terminal / ROIC terminal | 12% / 2% / 12% | 10,5% / 2,5% / 16% | 9,5% / 3% / 20% |

Márgenes favorables requieren éxito de integración y restan una carga económica de SBC respecto a objetivos ajustados. D&A 6% y capex 6,5–8% son selecciones sobre necesidades industriales y las historias separadas, no cifras combinadas verificadas. El escenario adverso evita contar una liberación automática de circulante cuando caen ventas. Los márgenes seleccionados excluyen caja extraordinaria de integración, que se resta separadamente sin atribuir beneficio fiscal. Esos costes son hipótesis explícitas y podrían ser mayores; no se han confirmado por la compañía.

Años 6–10 interpolan crecimiento, margen y reinversión neta hacia una economía sostenible; el año 10 converge a NOPAT × g/ROIC y el terminal usa NOPAT año11 × (1−g/ROIC). No se impone capex=D&A con crecimiento gratis. La tabla de diez años completa, identidades y sensibilidad son reproducibles en el paquete.

WACC central 10,5% es selección, no estimación exacta del combinado. Como contraste: Treasury10y 4,90% el4nov, beta histórica1,48 de proveedor y prima de mercado asumida4,5% dan coste propio≈11,56%; con deuda aproximadamente17% del capital y coste marginal supuesto6% después de impuesto20%, WACC mecánico≈10,41%. Beta histórica, pesos y prima no certifican riesgo postfusión. Se redondea10,5% y prueba9,5–11,5%; adverso12%. [Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve), [beta observada](https://stockanalysis.com/stocks/swks/statistics/).

| Caso ilustrativo | EV operativo | Residuo por acción con claims3.500/acciones241 | Peso terminal |
|---|---|---|---|
{cases}

**Esos residuos no son valores razonables totales, cotas de pérdida ni umbrales de compra.** No se calcula un descuento de seguridad sobre44,55 ni se lo promueve a ficha de ejecución. Un valor bajo el caso central puede reflejar hipótesis seleccionadas y vacíos importantes de datos. Los escenarios no tienen probabilidades asignadas y el adverso no es el peor desenlace posible.

### Inversa con el mismo modelo

A 82,65 × 241 + 3.500, la exigencia ilustrativa es EV 23.418,65. Manteniendo WACC10,5%, impuesto20%, g2,5%, ROIC16%, inversión base y primer año base, se varía crecimiento constante de años2–5 junto con margen maduro alcanzado desde año3. Años6–10 desaceleran a2,5%. No es una única expectativa implícita ni una validación independiente del DCF.

| Margen maduro después de SBC | Crecimiento anual años2–5 requerido |
|---|---|
{reverse}

La combinación 22%/16,1% supera claramente el objetivo de crecimiento agregado de un dígito medio/alto de la dirección; incluso28% requiere10,1% en este ejercicio. Son exigencias condicionales a capital y reinversión seleccionados, no predicciones del mercado. El ejercicio favorable se acerca al precio mediante mejor margen, coste de capital menor y crecimiento, no demuestra descuento seguro.

### Sensibilidad central

| WACC | g terminal | EV operativo | Residuo ilustrativo por acción |
|---|---|---|---|
{sens}

Variar claims hipotéticos de2.500 a4.500 cambia cada residuo en ±4,15 por acción respecto al centro; una incertidumbre de1.000 importa aunque no explique toda la distancia al precio. Variar241 a238/245 acciones no reemplaza un captable. Ningún rango de esta tabla es un rango razonable autorizado.

## Contraste por múltiplos y límites

No se publica un peer-average ni múltiplo objetivo: los ratios de SWKS en agregadores pueden mezclar cotización combinada con beneficio, caja y acciones históricos independientes. Comparar su PER42,82 del scanner con pares daría falsa homogeneidad. Broadcom mezcla software/IA; Qualcomm incorpora licencias; NXP está más expuesta a automóvil/industria; Murata reporta enJPY y otro calendario. Son candidatos de contraste, no equivalentes validados.

La falta de comparables homogéneos y puente completo del combinado mantiene **Stage 3 parcial**. Las hipótesis FCFF no sustituyen la conciliación. A098/A102 eran cola preliminar; no se ha recuperado una valoración anterior ejecutable que permita un puente de método. No hay una migración automática de precio previo ni de aprobación.

## Qué desbloquea o invalida la tesis

1. Recuperar estados adquiridos/pro forma posteriores al cierre y primer balance combinado: caja disponible, principal/carrying, compromisos, PPA, fees y captable.
2. Conciliar historia de ambos negocios a un calendario homogéneo, incluyendo septiembre Qorvo, working capital, capex, SBC e integración. El FY26 legado sólo no basta.
3. Validar que ahorros y mejora de mix elevan beneficio después de SBC y FCF sin financiar recompras con deuda; comprobar inventarios y contratos de suministro.
4. Contrastar crecimiento y margen exigidos con retención del mayor cliente, Smartphone y DGM; pérdida adicional de contenido o ahorro absorbido por costes debilita el caso.
5. Rehacer comparables con períodos homogéneos, entonces decidir valoración total y descuento según incertidumbre; sólo después, comprobar Stage2/3.5 actual.

La dirección menciona próxima llamada de resultados en **febrero de2027**, sin día confirmado en fuente primaria recuperada. Integración IT esperada primera mitad de2027 y sinergias completas a24–36meses desde5oct2026 son ventanas, no fechas comprometidas de publicación. Cualquier recorte de guía, necesidad de refinanciación no prevista o deterioro de caja puede adelantar revisión. [Preparados oficiales]({remarks}).

## Estado y reproducibilidad

Alta confianza en los datos independientes citados y en los términos de cierre; baja confianza en un valor accionarial combinado hasta cerrar las limitaciones. El informe conserva fuentes, cifras publicadas, cálculos separados, supuestos y checks. Revisión independiente completada:107 comprobaciones de cálculo, fuentes, períodos y límites aprobadas. La publicación queda autorizada únicamente como investigación parcial condicionada, nunca como análisis completo o entrada. El registro de auditoría acompaña el informe.
'''
for old,new in {'caída de25,6%':'caída de 25,6%','además66,2':'además 66,2','a556,5':'a 556,5','todavía15,5%':'todavía 15,5%','usa20%':'usa 20%','al19,5%':'al 19,5%','prueba18–23%':'prueba 18–23%','al10%':'al 10%','claims3.500/acciones241':'claims 3.500 / acciones 241','sobre44,55':'sobre 44,55','WACC10,5%':'WACC 10,5%','impuesto20%':'impuesto 20%','g2,5%':'g 2,5%','ROIC16%':'ROIC 16%','año3':'año 3','Años6–10':'Años 6–10','a2,5%':'a 2,5%','incluso28%':'incluso 28%','requiere10,1%':'requiere 10,1%','de2.500':'de 2.500','a4.500':'a 4.500','de1.000':'de 1.000','Variar241':'Variar 241','a238/245':'a 238/245','PER42,82':'PER 42,82','enJPY':'en JPY','de2027':'de 2027','a24–36meses':'a 24–36 meses','desde5oct2026':'desde 5oct2026','completada:107':'completada: 107','y checks':'y comprobaciones','Treasury10y':'Treasury 10y','el4nov':'el 4nov','histórica1,48':'histórica 1,48','asumida4,5%':'asumida 4,5%','aproximadamente17%':'aproximadamente 17%','supuesto6%':'supuesto 6%','impuesto20%':'impuesto 20%','redondea10,5%':'redondea 10,5%','prueba9,5–11,5%':'prueba 9,5–11,5%','adverso12%':'adverso 12%'}.items(): text=text.replace(old,new)
(P/'report.md').write_text(text)
S={'ticker':'SWKS','company':'Skyworks Solutions, Inc.','asOf':'2026-11-04','status':'partial_conditioned_audited','readyForPublication':True,'researchClassification':'Investigación parcial: Qorvo integrado, capital y caja combinados pendientes','fairValue':None,'fairValueTotal':None,'bear':None,'base':None,'bull':None,'conditionalDcfCases':None,'scenarioEconomicsOnly':{k:{'operatingEV':x['operatingEV'],'illustrativeCapitalResidualPerShare':x['illustrativeEquityResidualPerShare'],'isTotalFairValue':False,'isCurrentPriceTarget':False,'capitalIsAssumed':True}for k,x in R['cases'].items()},'scanPrice':82.65,'scanDate':'2026-11-04','lastClose':82.96,'lastCloseDate':'2026-11-04','lastCloseSource':'Stock Analysis; second provider82.92 discrepancy noted, not execution certified','entryApproved':False,'stage3Complete':False,'stage35Complete':False,'latestCompletedEligible':False,'technicalGate':None,'maximumConditioned':None,'nextEarningsConfirmed':None,'nextEvent':{'date':None,'month':'2027-02','name':'Próxima llamada indicada para febrero; día no confirmado','source':remarks},'conclusionES':'Qorvo amplía diversificación, pero legado y caja se deterioran; capital combinado sin conciliar. En observación, sin valor total ni entrada.','conclusionEN':'Qorvo broadens diversification, but legacy earnings and cash weaken; combined capital is unreconciled. Watch only, no total valuation or entry.','confidence':'Alta en datos publicados; baja en valoración y capital combinados.','limitations':['Balance publicado anterior al cierre; capital real combinado y PPA pendientes.','Calendarios de Qorvo/SWKS no homogéneos; falta caja de septiembre Qorvo.','DCF y residuos sólo ilustrativos, claims y dilución supuestos.','Comparables homogéneos, fecha exacta de resultados y técnica no certificados.'],'pros':[{'es':'DGM combinado FY26 ≈ 2.900 M y +12%; mayor diversificación tras Qorvo.','en':'Combined FY26 DGM ≈ $2,900m and +12%; broader diversification after Qorvo.','evidence':'La dirección presenta Smartphone aproximadamente4.600,−11%, y DGM aproximadamente2.900,+12%; cifras pro forma redondeadas.'}],'cons':[{'es':'FCF legado tras intangibles cae de 1.075,9 a 198,8 M; tres trimestres negativos.','en':'Legacy FCF after intangibles falls from $1,075.9m to $198.8m; three negative quarters.','evidence':'FY26=549,9CFO−320,6PPE−30,5intangibles=198,8; Q2−37,5,Q3−16,9,Q4−71,8.'},{'es':'241 M acciones guiadas combinadas; no usar 151 M ni caja precompra como capital actual.','en':'241m combined guided shares; do not use 151m or pre-acquisition cash as current capital.','evidence':'Oct2 balance precedes Oct5 closing; Q1 FY27 guide uses approximately241m diluted shares.'}],'sources':[release,remarks,f25,q1,q2,q3,q424,close,pf,exchange,financing,qorvoq,qorvoy,transcript,'https://stockanalysis.com/stocks/swks/history/']}
(P/'summary.json').write_text(json.dumps(S,ensure_ascii=False,indent=2)+'\n')
print(len(text.split()),'words')
