from pathlib import Path
import json
P=Path(__file__).parent;r=json.loads((P/'model/results.json').read_text());h=json.loads((P/'history/normalized.json').read_text());s=json.loads((P/'model/sensitivities.json').read_text());rates=json.loads((P/'model/rates_results.json').read_text())
q='https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm';fy='https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm'
text=f'''# FORM — investigación parcial: expansión industrial y financiación pendiente

Corte informativo: 4 de noviembre de 2026. Precios: cierre del 3 de noviembre. USD millones salvo precio/acción; acciones en millones. Investigación revisada; no aprobación de entrada. No es valoración total de FormFactor ni Stage 3 integral.

## Conclusión

FormFactor acelera en tarjetas de prueba para memoria y lógica avanzada, pero la rentabilidad del trimestre no equivale a un margen de ciclo. El DCF industrial conserva SBC, financia fábrica y crecimiento y excluye una valoración independiente de la participación privada FICT. Con financiación Teradyne supuesta, los casos parciales son 17,20 / 52,82 / 113,93 dólares por acción; sin cierre, 13,95 / 50,57 / 113,40. Ninguno es valor total, cota inferior ni rango íntegro de FORM. No se asignan probabilidades al cierre. El precio de referencia es 96,79, no el scanner histórico 123,84.

La tesis exige convertir la demanda de HBM, lógica avanzada y encapsulado en caja después de una expansión intensiva en capital. El caso favorable exige ingresos de 4.153 M en el año diez, margen operativo antes de amortización adquirida de 34% y descuento de 9,5%; no constituye previsión corporativa. El caso central no acredita margen de seguridad frente al precio, pero tampoco permite concluir una sobrevaloración total certificada porque FICT, premios y capital actual siguen incompletamente conciliados.

## Negocio y calidad

El Q3 facturó 280,547 M: tarjetas 221,095 M y sistemas 59,452 M. Las tarjetas sirven foundry/lógica y DRAM/HBM, mientras sistemas incluyen pruebas avanzadas y ópticas. La cualificación técnica, complejidad de contactos y relación con fabricantes favorecen continuidad comercial; no eliminan concentración, competencia ni ciclos de capacidad. SK hynix representó 20,7% y TSMC 12,8% del trimestre: 33,5% combinado. Son porcentajes de un mismo período, no se suman clientes de trimestres diferentes. Los destinos de entrega no prueban el país del consumidor final.

Los ingresos TTM subieron de 759,313 a 980,096 M y el EBIT reportado de 41,430 a 179,534 M. La mejora tiene respaldo contable, pero la expansión fabril, la concentración de clientes y la ciclicidad de memoria impiden perpetuar mecánicamente el margen Q3. Fuente: {q}

## Historia normalizada y caja

Los anexos history contienen tres ejercicios, cuatro trimestres y TTM comparable, con EPS, acciones, SBC, D&A, capital circulante y segmentos cuando disponibles. Todos son períodos de 52/13 semanas; Q4 es FY menos nueve meses. EPS y acciones ponderadas Q4/TTM derivados se etiquetan calculados, no reportados. La ponderación temporal no reconstruye necesariamente treasury-stock ni antidilución; son proxies analíticos, no denominadores GAAP certificados ni EPS reportados.

| Período | Ingresos | EBIT GAAP | CFO | Capex caja | SBC CF | FCF bruto |
|---|---:|---:|---:|---:|---:|---:|
'''
for a in h['periods']:
 text+='| '+a['period']+' | '+' | '.join(f"{a[k]:,.3f}" if a.get(k) is not None else 'no separado' for k in ['revenue','operating_income','cfo','gross_capex','sbc_cf_addback'])+' | '+f"{a['cfo']-a['gross_capex']:,.3f}"+' |\n'
text+=f'''
El EBIT FY2023 incluye ganancia por venta de negocio de 72,953 M: retirarla reduce 82,756 a 9,803 M. FY2024 incluye 20,581 M: 64,780 pasa a 44,199 M. Son puentes analíticos, no otra cifra GAAP. Reestructuración y arranque permanecen en el historial y no se añaden automáticamente al DCF. La cifra de EBIT TTM de 213,4 M mostrada por un agregador no sustituye los 179,534 M reconciliados con estados primarios. Fuente anual: {fy}

FCF bruto significa CFO menos compras brutas de PP&E: TTM 257,009 − 75,752 = 181,257 M; menos SBC CF 35,429 resulta un proxy de 145,828 M, no FCFF ni capacidad distribuible certificada. El TTM previo fue 105,336 − 100,008 = 5,328 M, y después de SBC −33,588 M. Parte del salto obedece a calendario de inversión: el período previo incluía compra inmobiliaria Farmers Branch de 55 M en junio de 2025; no prueba capex de mantenimiento permanentemente menor.

El FCF ajustado del emisor no es el mismo: Q3 64,778 M añade a 64,622 M de CFO menos capex 0,081 de intereses y 0,075 de costes de adquisición. FY2025 13,574 frente a 11,740 añade 0,362 y 1,472. No se toma ese ajuste como caja gratis. D&A CF incluye amortización adquirida; el modelo antes de ésta usa sólo D&A física/software seleccionada, evitando doble addback.

SBC gasto Q3 fue 8,835 M y nueve meses 25,556 M, distinto del ajuste no GAAP 8,802/25,395. Los 0,161 M de SBC en reestructuración explican la diferencia de nueve meses; no se inventa su distribución trimestral. Capitalización de SBC y amortización de software no separadas quedan desconocidas. El modelo conserva SBC como coste, además de mostrar sensibilidad de premios netos ya existentes; no resta automáticamente todas las RSU sin consolidar y todo el gasto futuro dos veces.

Los reembolsos IEEPA aumentaron el beneficio bruto Q3 en 8,6 M y nueve meses en 9,4 M; corresponden a tarifas de períodos anteriores y el emisor no espera repetición similar. La caja recibida 9,9 M no equivale al beneficio reconocido. Se preserva el GAAP histórico, se retiran 8,6 M del ancla trimestral del DCF y 9,4 M de la alternativa TTM. No se vuelve a restar la caja ya recibida, ni se añade como activo nuevo la expectativa de otros 1,8 M en Q4. Los márgenes futuros elegidos excluyen ese beneficio extraordinario; la base inicial de 27% es ligeramente superior al margen Q3 sin reembolso (aproximadamente 26%), por lo que presupone mejora operativa pese a la rampa. El adverso/base no cambian al corregir el ancla porque el suelo físico domina la inversión inicial; el favorable exige más inversión y sí cambia. Fuente: {q}

## Farmers Branch y sostenibilidad

La nueva planta comenzó producción al final de Q3 y la rampa continuará durante 2027. El 10-Q advierte costes sustanciales de infrautilización: al producir, parte del gasto de arranque pasa de G&A a coste de ventas, no desaparece. Q3 soportó 6,375 M de arranque y el TTM 20,012 M. PP&E neto fue 300,369 M y obra en curso 117,845 M. No se usa el margen no GAAP del trimestre como margen libre de costes futuros. Fuente: {q}

El capex TTM de 75,752 M no se extrapola: FY2025 103,658 menos 9M2025 92,345 más 9M2026 64,439. La guía histórica de expansión no es una confirmación de gasto actual; no se presenta como vigente sin verificar actualizaciones. El modelo selecciona capex inicial de 14% de ingresos en base, 173,6 M, y un suelo recurrente de 6% al estabilizarse. Son supuestos propios, no guía. El stress +2/+4 puntos de capex continúa también en terminal. La evidencia primaria basta para exigir financiación explícita, no para certificar el calendario definitivo del proyecto.

## Capital, financiación y FICT

Caja y valores líquidos al 26 de septiembre: 138,179 + 257,233 = 395,412 M; caja restringida 3,590 excluida. Se reserva caja operativa 150 y se deduce deuda principal 11,403, no deuda contable 11,358 más principal. Se añade swap 1,697 y descuenta derivado FX 0,693. El revolver de 150 no dispuesto no es caja. Arrendamientos operativos 16,402 permanecen en costes, sin segunda deducción de deuda. Pagaré de 1,5 se incorpora por 0,75 seleccionado, con sensibilidad 0–1,5. DTA 87,682 no es efectivo.

Se reserva 56,397 por exposición fiscal histórica: UTB bruto septiembre 55,4 más intereses/penalizaciones FY2025 0,997 como último dato conocido. No es pago futuro exacto, puede haber compensaciones y el interés actual no está conciliado. La tasa recurrente de 24% no liquida esa exposición. Se deducen 4,948 de reestructuración devengada y 18 del grant California Competes potencialmente reembolsable, como reserva prudencial completa, no declaración de incumplimiento. Sus condiciones de empleo/inversión y el traslado de actividades exigen seguimiento. No se deduce por segunda vez toda deuda fiscal corriente que pudiera solaparse. Fuente: {q}

El acuerdo Teradyne prevé 300 M por 2,234887 millones de nuevas acciones y cierre esperado en Q4 sujeto a condiciones. El 10-Q del 3 de noviembre aún lo describe pendiente. Form D identifica el compromiso, no demuestra liquidación. En el caso de cierre se añaden 297 M netos de una comisión seleccionada de 3 M y simultáneamente las acciones nuevas. Sin cierre se eliminan ambos, no se conserva el dinero sin dilución. La marca bursátil de las acciones que podría recibir Teradyne no reduce el efectivo contractual recibido por FORM. Fuentes: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000037/form-20261006.htm y {q}

Las acciones reales son 78,403115 M al 28 de octubre, no las ponderadas Q3. Se añade un proxy de premios netos de 1,160 M, diferencia entre diluidas y básicas ponderadas Q3: no es un cap table actual certificado. El denominador seleccionado con emisión es 81,798002 M; sin emisión 79,563115 M. Hay 1,406487 M de RSU sin consolidar y 74,680 M de compensación no reconocida, con PRSU potencialmente al 200%; no se convierten todas en pasivo corriente ni se presume que todas vestirán. La autorización de recompra 70,9 M no es activo y no se observaron recompras nueve meses.

Los derechos de registro de la emisión incluyen registro vinculado al cierre y suspensiones limitadas; no garantizan liquidez inmediata ni prueban cierre. El texto completo de compra no se ha conciliado aquí, y no se infieren derechos de cancelación sin coste. Fuente: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/ex41-teradyneformfactorreg.htm . Definición Form D: https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice

La inversión privada FICT es 20% de la holding, con valor contable de 70,467 M y resultados por puesta en equivalencia rezagados. No existe un DCF independiente conciliado del negocio. Su ingreso TTM 6,193 M está fuera del EBIT industrial y no se capitaliza dos veces. Las compras relacionadas, 12,3 M en nueve meses, siguen dentro del coste operativo. Excluir la participación del componente calculado no significa que valga cero ni que el resultado sea una cota inferior. Añadir mecánicamente su book value llevaría el caso base parcial de 52,82 a 53,68; es sensibilidad, no tasación. Fuente: {q}

## DCF explícito y supuestos

Horizonte diez años, períodos anuales al 3 de noviembre de 2027–2036, no ejercicios fiscales inventados. No se omite arbitrariamente un stub y luego se llaman fiscales los descuentos. Ancla: cuatro veces Q3, ingresos 1.122,188 y EBIT antes de amortización adquirida y excluyendo reembolsos arancelarios 295,168 = (81,597 + 0,795 − 8,6) × 4. Es run-rate elevado, no previsión anual. La alternativa ancla TTM 980,096/173,012, manteniendo los mismos futuros, produce base 49,18: requiere más inversión inicial para llegar al mismo objetivo.

NOPAT = EBIT después de SBC y antes de amortización adquirida × (1−24%). No se introduce escudo fiscal de amortización no demostrado. D&A física/software se selecciona en 3% de ventas, sin añadir de nuevo la amortización adquirida. Capex menos D&A más circulante es el suelo físico; se toma el máximo con incremento positivo de NOPAT dividido por ROIC. La caída de NOPAT no genera liberación ficticia de capital; tampoco se libera circulante cuando caen ventas. El terminal financia el máximo entre suelo físico persistente y NOPAT × g / ROIC. No se añade adquisición futura ni FICT a ingresos industriales.

| Supuesto | Adverso | Base | Favorable |
|---|---:|---:|---:|
| Ingresos primer año | 1.050 | 1.240 | 1.400 |
| Margen inicial/final | 18%/20% | 27%/30% | 31%/34% |
| WACC seleccionado | 12,5% | 10,75% | 9,5% |
| g terminal | 2,5% | 3% | 3,5% |
| ROIC incremental | 15% | 25% | 30% |
| Capex inicial/final (%ventas) | 14%/6% | 14%/6% | 16%/6% |

La base crece 20%,14%,10%,8%,6%,5%,4,5%,4%,3,5% en años dos a diez; el favorable 30%,22%,17%,13%,10%,8%,7%,6%,5%; el adverso −5%,3%,5%,5%,4%,3,5%,3%,2,5%,2,5%. El margen base inicial inferior al Q3 incorpora fricción de rampa, pero sigue siendo una selección exigente frente a la historia. El objetivo empresarial de 1.600 M de ingresos/5 dólares de EPS no GAAP carece aquí de fecha comprometida y no valida estas trayectorias.

El CAPM con Treasury 10 años 4,95%, ERP 4,41% y beta proveedor 1,28 da coste de equity 10,5948%. Con deuda nominal pequeña y tipo cubierto 2,75%, el WACC proxy es {rates['calculatedWaccProxy']*100:.4f}%. El 10,75% base añade {rates['selectedPremiumBp']:.1f} pb discrecionales: no es redondeo. ERP y Treasury tienen fechas distintas; beta no es regresión propia y tipo de deuda vigente no es rendimiento de refinanciación. Fuentes: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve ; https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm ; https://stockanalysis.com/stocks/form/statistics/

| Resultado parcial con cierre | Adverso | Base | Favorable |
|---|---:|---:|---:|
'''
for label,key in [('EV industrial','enterpriseValue'),('PV explícito','pvExplicit'),('PV terminal','pvTerminal'),('Puente seleccionado','capitalBridge'),('Acciones seleccionadas','sharesSelected'),('Componente por acción','conditionalIndustrialPerShare')]:text+='| '+label+' | '+' | '.join(f"{r[n][key]:,.3f}" for n in ['bear','base','bull'])+' |\n'
text+='\n### Diez años base: cifras conciliables\n\n| Año al 3nov | Ventas | EBIT preamort/SBC retenida | NOPAT | Capex suelo | D&A física | ΔWC | Inversión neta máxima | FCFF |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for z in r['base']['rows']:text+='| '+str(z['year'])+' | '+' | '.join(f"{z[k]:,.2f}" for k in ['revenue','ebitAfterSbcBeforeAcquiredAmort','nopat','grossCapexFloor','physicalDA','wcInvestment','netReinvestment','fcff'])+' |\n'
text+='''
La inversión neta es el máximo, no la suma de dos presupuestos. FCFF = NOPAT − inversión neta. El terminal representa aproximadamente 51%/60%/71% del EV, por lo que los extremos dependen mucho de persistencia y descuento.

## Sensibilidades, inversos y lectura de precio

El capex persistente +2/+4 puntos reduce base 52,82 a 48,41/43,32; se mantiene el suelo también en terminal. Margen −5 puntos reduce base a 43,20; +5 puntos sube a 60,65. Las matrices ejecutables incluyen WACC/g, impuesto 20–28%, ROIC 15–35%, circulante 15–35%, caja reservada 100–250 M, UTB 27–70 M, grant 0–18 M, premios netos 0–2 M, comisiones 0–5 M y ajustes de caja ±100 M. No todos son independientes ni deben acumularse como rango estadístico.

El inverso industrial manteniendo financiación y demás supuestos necesitaría añadir 12,35 puntos de crecimiento en cada uno de los años dos a diez para alcanzar 96,79. Es un requisito matemático, no crecimiento estimado. En el barrido de margen de −10 a +30 puntos, el precio llega como máximo a 94,32: no se inventa solución fuera del intervalo probado. Ambos barridos verifican monotonía. Como FICT no está tasada, no son un inverso del valor total de FORM.

## Pares y disciplina relativa

La comparación contemporánea usa EBIT reportado, no el ajuste de agregador. FORM tiene EV convencional aproximado 7.205 M, 7,35× ventas TTM y 40,13× EBIT, margen 18,32%. TER tiene 8,28× ventas pero 25,80× EBIT con margen 32,11%; COHU 3,81× ventas y EBIT negativo. Un descuento en ventas no prueba menor valoración. Los activos no operativos, minoritarios, convertibles, geografías y mezcla de pruebas difieren; el anexo comps conserva fuentes y ajustes, sin aplicar mediana como objetivo.

TER y COHU son referencias de ecosistema, no sustitutos exactos de tarjetas. Technoprobe compite más directamente, pero no se fuerza una comparación Q3 antes de sus resultados ni se inventa margen o valor de su inversión. La participación de TER en Technoprobe y su compromiso FORM no deben confundirse con actividad industrial pura. Los múltiplos convencionales no certifican el puente completo del DCF.

## Calendario, seguimiento y puerta de entrada

Q3 se publicó el 28 de octubre y el 10-Q el 3 de noviembre. El calendario oficial no anuncia una fecha exacta siguiente: queda null/no confirmada. Una estimación de agregador no libera el requisito de calendario. Vigilar cierre de la emisión y registro de acciones, evolución de Farmers Branch/capex/infrautilización, concentración y memoria, condiciones del grant, exposición fiscal y resultados/caja propios de FICT. Fuente: https://investors.formfactor.com/events-and-presentations

La observación original del scanner del 14 de octubre fue 123,84, QP80, Opportunity90, RSI45,2 y Stage2Sí histórico. El cierre verificable de esa sesión 119,71 es distinto y no sustituye el dato exportado. El precio usado de 96,79 corresponde al 3 de noviembre. No se hereda aprobación técnica de octubre ni se afirma reconciliado su desfase. Fuente de cierres: https://stockanalysis.com/stocks/form/history/

**Clasificación: investigación parcial condicionada.** Valor total, rango agregado y Stage3 completo no certificados. No latestCompleted, no Stage3.5, no orden ni aprobación de entrada. Próximas verificaciones: cierre efectivo y cap table, caja y dilución posterior, valoración independiente de FICT, inversión y márgenes normalizados, fecha oficial siguiente y filtro técnico vigente.

## English conclusion

FormFactor's industrial DCF is partial and conditional: $17.20/$52.82/$113.93 per selected share assuming the pending Teradyne financing closes, versus $13.95/$50.57/$113.40 without closing. It excludes an independently unvalued private FICT interest and uses selected award/tax/cash reserves. These are not total-company fair values, lower bounds, or an entry approval. Current growth is strong, but factory investment, customer concentration and cycle margins require further proof.

## Reproducibilidad y límites

Scripts offline y ledgers factuales reproducen historia, capital, diez años, sensibilidades e inversos; no contienen filings completos. Los resultados son análisis propio, no recomendación personalizada ni precio certificado. Comisiones, reserva de caja, UTB, grant, valor del pagaré, dilución, margen, capex y coste de capital son selecciones visibles. Datos faltantes permanecen null y no se convierten en ceros económicos.
'''
(P/'report.md').write_text(text)
print('report',len(text))
