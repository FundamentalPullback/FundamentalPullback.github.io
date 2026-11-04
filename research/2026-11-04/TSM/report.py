import json,pathlib
P=pathlib.Path(__file__).parent;h=json.loads((P/'history/history.json').read_text());d=json.loads((P/'analysis.json').read_text());v=d['diagnostics']
def f(x,dec=0):return 'No desglosado' if x is None else f'{x:,.{dec}f}'.replace(',','X').replace('.',',').replace('X','.')
rows=[]
for k in ['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025Q3','TTM2026Q3']:
 a=h['periods'][k];rows.append('|'+ '|'.join([k]+[f(a[z]) for z in ['revenue','ebit','net_income_parent','cfo','capex_ppe','capex_intangibles','sbc']])+ '|')
text='''# TSM — crecimiento excepcional, caja aún sin conciliación integral

**Actualización fundamental parcial. Sin valoración intrínseca, sin aprobación de entrada y sin cierre integral de Stage 3.** Corte: 4 de noviembre de 2026, 18:22 UTC. Auditoría independiente completada: investigación parcial, sin certificación de valoración ni de Stage 3 integral. No altera cartera, operaciones ni A105.

## 1. Conclusión y precio

TSMC combina escala, liderazgo tecnológico y expansión de beneficios operativos. Sin embargo, el crecimiento de caja exige separar inversión industrial, cobros fiscales, intereses y obligaciones consolidadas. El dossier cierra la historia disponible y explica sus límites; no rellena las partidas omitidas con cero ni transforma un diferencial de caja en owner earnings.

Referencia bursátil: cierre del 3 de noviembre de 2026, **404,80 USD por ADR**, fuente secundaria Stockanalysis contrastada con Yahoo. A105 conserva su referencia del 27 de octubre de 436,63 USD; la última observación real del escáner es 28 de octubre, 431 USD. No se ha fabricado una nueva sesión de escáner ni señal técnica.

Cada ADR representa cinco acciones ordinarias. La conversión contextual utiliza **32,760 NTD por USD**, cierre interbancario publicado por CBC el 3 de noviembre; no confundirlo con 31,983 medio Q3, 31,880 del balance ni 31,8 supuesto en la guía. Los 25.932 millones de acciones diluidas medias Q3 equivalen a 5.186,4 millones de ADR: sirven como aproximación, no como recuento real vigente. A ese denominador, la capitalización indicativa es 2.099.455 millones USD. No constituye un enterprise value certificado.

## 2. Historia financiera reproducible

NTD millones, salvo indicación expresa. NI es atribuible a la matriz, distinto del beneficio consolidado. EBIT es resultado de operaciones, sin ganancias financieras. Las cifras del resumen Q3 están redondeadas a millones; las derivaciones desde estados completos mantienen decimales solo para reproducción, no por precisión económica.

|Periodo|Ingresos|EBIT|NI matriz|CFO IFRS|PPE caja|Intangibles caja|SBC|
|---|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(rows)+f'''

El TTM aumenta ingresos un **{f(v['ttm_revenue_growth']*100,2)} %**, EBIT un **{f(v['ttm_ebit_growth']*100,2)} %** y CFO un **{f(v['ttm_cfo_growth']*100,2)} %**. El margen operativo pasa del **{f(v['prior_ttm_margin']*100,2)} % al {f(v['ttm_margin']*100,2)} %**. Existe progreso operativo además de factores no operativos. D&A TTM es 746.304 millones NTD; EPS diluido ordinario TTM aproximado 97,47 NTD por roll-forward FY2025 menos 9M2025 más 9M2026 (65,47 − 46,75 + 78,75). La suma de los cuatro trimestres con Q2 publicado directamente resulta 97,48 (18,72 + 22,08 + 27,25 + 29,43). La diferencia de 0,01 refleja redondeo y medias ponderadas; ninguno es un EPS TTM certificado por el emisor.

Q4 2025 se obtiene restando nueve meses de FY2025. Q2 caja se obtiene restando Q1 de H1. Q2 EPS publicado 27,25 se conserva, sin inferirlo de EPS acumulados que emplean medias ponderadas diferentes. Los inputs, fórmulas y propagación de valores desconocidos se entregan en history/.

## 3. Calidad del beneficio y de la caja

**Los ingresos TTM crecen un 36,17 % y el EBIT un 59,55 %, hasta 4.944.817 y 2.866.916 millones NTD, respectivamente.**

La venta parcial de VIS en mayo reduce la participación al 19 % y elimina la influencia significativa. La ganancia de 63.202,285 millones NTD incluye revalorización no monetaria del remanente, mientras los cobros de venta son 24.301,349 millones. Está fuera de EBIT; el CFO ya revierte la ganancia. No restarla de nuevo del EBIT ni llamar orgánico a todo el crecimiento de beneficio neto. No se presume un ajuste fiscal exacto sin desglose.

**CFO menos PPE asciende a 1.480.749 millones NTD en el TTM, pero faltan intangibles, SBC y arrendamientos Q3 para certificar owner FCF.** La cifra es un diferencial bruto, no FCF integral. En IFRS, los intereses pagados se clasifican en financiación y los cobrados en inversión. Restar los 20.054 millones de intereses pagados reduce ese diferencial a 1.460.695 millones, todavía sin cerrar los demás ajustes. Tampoco constituye FCFF: el coste de financiación no es un flujo operativo no apalancado.

A la capitalización y FX indicativos, el diferencial CFO-PPE equivale al 2,15 % del equity. **Ese porcentaje no es owner FCF yield** y no es una valoración ni un techo de compra. No se añaden automáticamente intereses cobrados o dividendos de participadas si luego se valoran sus activos por separado.

H1 muestra pagos de intangibles de 3.876,352 millones, adquisición de derechos de uso de 9.441,034 millones y principal de arrendamientos de 2.249,689 millones. La ausencia de sus filas en el resumen Q3 no significa ausencia de gastos. El interés capitalizado H1, 5.096,044 millones, está excluido del cash PPE y forma parte de la conciliación de costes financieros; exige un tratamiento coherente de capex y financiación.

El informe de gestión Q3 atribuye principalmente a créditos fiscales de inversión estadounidenses el agregado de otros cobros de inversión de 198.740 millones NTD. Incluye conceptos como intereses y dividendos y no coincide con la fila resumida de otros flujos de inversión de 159.868 millones. **No se dispone del importe separado exacto del crédito fiscal en esos documentos.** No se añade al CFO, no se perpetúa como margen recurrente y no se vuelve a sumar al balance si ya está cobrado.

## 4. Capital: partidas observadas y pendientes

|Concepto septiembre, NTD millones|Importe|Tratamiento|
|---|---:|---|
|Caja|3.621.894|No equivale a caja excedente certificada|
|Instrumentos financieros corrientes|395.085|Clasificación/liquidez y reservas por conciliar|
|Inversiones de largo plazo|224.633|No son caja libre; excluir de una suma automática|
|Dividendos por pagar|363.053|Conciliar obligaciones, ex-dividend y derechos del accionista|
|Acreedores de equipo y contratistas|298.826|Conciliar altas económicas y pagos de capex; evitar doble cuenta|
|Bonos y préstamos bancarios corrientes|213.198|Incluyen deuda corriente, no duplicarla|
|Bonos no corrientes contables|770.315|No certifican principal ni toda deuda financiera|
|Otros pasivos no corrientes agregados|271.600|No asumir que son íntegramente operativos o cero deuda|
|Intereses no controladores|45.326|Book value, no valor económico independiente|

**Los 4.016.979 millones NTD de caja e instrumentos corrientes no son caja distribuible certificada; hay dividendos pendientes y deuda bancaria no corriente por conciliar.** La suma de 983.513 millones de bonos contables y deuda corriente identificada no es toda la deuda financiera. H1 contiene préstamos bancarios no corrientes de 49.226,958 millones que podrían seguir dentro del agregado septiembre; no se asume que desaparecieron. Los bonos necesitan reconciliación a principal y divisa.

H1 también informa de arrendamientos no corrientes de 33.276,056 millones, prestación definida neta de 5.893,691 millones y pasivos derivados de 2.452,333 millones más coberturas de 2,563 millones. Son referencias históricas, no saldos certificados a septiembre. No se construye un puente actual sumándolos como si todas las fechas y categorías coincidiesen.

Un DCF futuro deberá elegir un tratamiento coherente de arrendamientos y mantenerlo en EBIT, reinversión y deuda. Para PPE, el desfase entre pagos y altas, incluidos acreedores, no permite identificar gasto de mantenimiento únicamente con la amortización. Deben separarse créditos y subvenciones, obligaciones de devolución, capital minoritario y caja operativa mínima. Tampoco se descuenta todo acreedor de equipo como deuda si su efecto ya queda financiado en reinversión.

El 6-K del 22 de octubre describe actividades de septiembre, no octubre: no registra emisión de bonos ni cancelación de acciones en septiembre. No prueba que no existan cambios posteriores.

## 5. Ventajas, riesgos y guía

**Los nodos de 7 nm y más avanzados representan el 79 % de los ingresos Q3; HPC aporta el 68 %.** La combinación indica exposición a computación avanzada y capacidad tecnológica, no una garantía de crecimiento perpetuo. Smartphones aporta el 21 %. El 79 % de ingresos de clientes de Norteamérica refleja domicilio del cliente, no ubicación de fabricación.

El 20-F muestra concentración FY2025: diez mayores clientes 78 % de ventas, primero 19 % y segundo 17 %, sin identificar aquí nombres no publicados. El riesgo combina demanda de pocos grandes compradores, inversión adelantada, competencia, suministro de energía/agua, desastres y concentración productiva en Taiwán. Diversificación comercial no elimina riesgo geopolítico o de interrupción.

La guía Q4 sitúa ventas en 52,3–54,3 mil millones USD, margen bruto en 65–67 % y operativo en 56,5–58,5 %, bajo supuesto FX 31,8. No es resultado conseguido. La dirección mantiene capex FY2026 de 60–64 mil millones USD y anticipa gasto elevado en 2026–28. En la llamada aclaró que la dilución de margen de fábricas internacionales de 3–4 puntos corresponde a la segunda mitad del horizonte de cinco años; no se fija automáticamente a 2027. Los nuevos nodos y las plantas exteriores pueden limitar el margen pese al crecimiento.

**El presupuesto de capex FY2026 de 60–64 mil millones USD y el coste de plantas internacionales exigen financiar crecimiento antes de valorar beneficios futuros.** El supuesto de reinversión de un futuro DCF debe cubrir expansión, mantenimiento y capital circulante; un terminal con crecimiento y reinversión nula no sería admisible.

## 6. Normativa y calendario

El 20-F confirma que la autorización VEU de Nanjing expiró en diciembre de 2025 y que existe una licencia anual de exportación. No garantiza su renovación ni constituye una autorización permanente. Las subvenciones tienen condiciones que pueden conllevar devolución o pérdida de financiación. No se ha certificado integralmente al corte la aplicación de cada norma, licencia, arancel o contrato de subsidio. No se asigna pérdida cero ni una probabilidad inventada a riesgos geopolíticos.

**Los resultados Q3 ya se publicaron el 15 de octubre; el anuncio del 10 de noviembre es de ventas mensuales, no de resultados trimestrales.** Calendario oficial: 10 noviembre, 13:30 Asia/Taipei, ventas de octubre. No se ha encontrado confirmación de la siguiente fecha trimestral. La página oficial de estados completos consultada contiene H1 2026, sin notas Q3 completas; no se inventa su fecha de publicación.

## 7. Comparables y valoración

UMC y GlobalFoundries son referencias industriales, no clones de TSMC. Sus nodos, clientes, subvenciones y utilización difieren. El resultado Q3 de GFS publicado el 4 de noviembre es posterior al cierre bursátil de referencia del 3 de noviembre; no se presenta ese precio como una reacción al anuncio. Los archivos comps/ distinguen cifras IFRS de ajustadas y documentan límites de caja.

UMC publica margen operativo Q3 del 25,1 %, frente al 58,7 % de TSMC. GFS publica 12,1 % IFRS y 17,9 % ajustado: no mezclarlos. GFS CFO de 341 millones USD menos inversión bruta de 301 deja 40, mientras su FCF ajustado de 136 incluye 96 de subvenciones de inversión. UMC muestra una diferencia de aproximadamente 120 millones NTD entre capex narrativo y las filas de compras PPE más intangibles, aún sin conciliar. Estas diferencias son precisamente por qué no se aplican múltiplos cruzados automáticamente.

La comparación operativa ayuda a interpretar calidad; **no cierra múltiplos homogéneos TTM ni una valoración relativa certificada**. No se ha ejecutado DCF, reverse DCF, rango de valor ni precio de entrada con inputs incompletos. Bear/base/bull se mantienen nulos, no en cero. No reutilizar un modelo de otro ticker ni asumir que A105 contenía valoración.

## 8. Próximos pasos concretos

1. Incorporar notas completas septiembre: intangibles, SBC, arrendamientos, préstamos, principal de bonos, derivados, obligaciones fiscales y prestaciones.
2. Conciliar inversión bruta/económica, pagos por equipo, créditos fiscales cobrados y subvenciones futuras sin duplicación.
3. Separar beneficio recurrente y ganancia VIS, con fiscalidad verificable; conciliar participadas y minoritarios.
4. Rehacer pares TTM en la misma base y fecha. En GFS incorporar el anuncio del 4 de noviembre y separar subvenciones del cashflow operativo.
5. Solo después, DCF explícito de diez años con reinversión, moneda/tasa coherentes, escenarios y análisis inverso. Verificar normativa, calendario y filtros técnicos antes de cualquier eventual Stage 3.5.

## 9. Fuentes y reproducción

history/SOURCES.md enlaza los estados anuales, Q1, H1 y nueve meses usados. build_history.py reproduce la historia; build_analysis.py calcula diagnósticos sin rellenar desconocidos. analysis.json conserva las partidas actuales y proxies históricos por separado. Los extractos de cifras y enlaces permiten revisión sin redistribuir documentos completos.

'''
for name,u in d['primary_sources'].items():text+=f'- {name}: {u}\n'
text+='- FS Q3: https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-10/3a94d1034b9e6b22446b674f7aaf3d088a12a193/FS.pdf\n- Management report Q3: https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-10/f83780000ddc0c3b48e57a87eab6814c4ab35058/3Q26%20ManagementReport.pdf\n- Llamada alojada por IR: https://investor.tsmc.com/schinese/encrypt/files/encrypt_file/reports/2026-10/eba4fac72873bf546b669bd2b5d973df5c93215d/TSMC%203Q26%20Transcript.pdf\n'
(P/'report.md').write_text(text)
