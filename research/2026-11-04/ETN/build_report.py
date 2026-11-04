from pathlib import Path
import json
P=Path(__file__).parent
H={a['period']:a for a in json.loads((P/'history/normalized.json').read_text())};R=json.loads((P/'model/results.json').read_text());V=json.loads((P/'model/checks.json').read_text());C=json.loads((P/'capital/facts.json').read_text());S=C['sources'];rates=json.loads((P/'model/rates_results.json').read_text());f=lambda x:f'{x:,.2f}'
pro='Eaton creció 28% en ventas Q3, con 19% orgánico y fuerte demanda eléctrica. El backlog firme de 26.200 millones ayuda a visibilidad, pero no convierte pedidos en caja ni elimina el coste de capacidad.'
con='La deuda contable alcanza 20.106 millones tras las compras y el TTM incorpora solo parte de los negocios adquiridos. El aumento de ventas no equivale a crecimiento comparable del beneficio ni a caja libre sin necesidades de inversión.'
con2='Mobility se separaría mediante un canje voluntario de acciones y combinación con Dana. El ratio y denominador final no están fijados; sumar 50,1% de SpinCo a cada acción Eaton sería incorrecto. No hay valoración total actual certificada.'
t=f'''# ETN | Eaton | Electrificación fuerte, perímetro y derechos todavía abiertos

Investigación al 4 noviembre 2026; precios al cierre 3 noviembre. USD millones salvo acciones en millones y datos por acción. Investigación parcial revisada; sin aprobación de entrada. **Investigación parcial: valor total actual y escenarios agregados nulos.** El dossier presenta un DCF contrafactual del perímetro consolidado actual sin separación Mobility ni compra COL; no es un precio objetivo del título tras las operaciones propuestas. Sin entrada ni Stage 3 integral.

## 1. Resultado y datos del escáner

Última fila real del registro: **13 octubre, 423,49; QP 90, Opportunity 85, RSI 48,1 y Stage 2 Sí histórico**. Se conserva literalmente, sin afirmar que sea un cierre de mercado ni una señal vigente. Para los cálculos se usa cierre **3 noviembre de 391,70**, con fecha y fuente separadas. La gran variación posterior del título no se incorpora a una cotización intradía mezclada con cierres. [Historial]({S['price']}).

{pro}

{con}

{con2}

Los casos de perímetro constante arrojan **{f(R['bear']['counterfactualPerShare'])}/{f(R['base']['counterfactualPerShare'])}/{f(R['bull']['counterfactualPerShare'])}**. No se promedian ni se convierten en valor actual total de ETN. El favorable se aproxima al cierre bajo supuestos exigentes; un estrés conjunto más optimista lo supera. El análisis no demuestra margen de seguridad, pero tampoco afirma que el precio sea imposible o que el mercado de electrificación carezca de crecimiento.

## 2. Negocio, demanda y calidad de resultado

Eaton suministra distribución y protección eléctrica, calidad de energía, soluciones de centros de datos, equipos y servicios aeroespaciales y componentes de movilidad. Electrificación y mayor densidad energética elevan contenido por instalación; redes, fábricas, edificios y aviación diversifican el negocio. La capacidad para entregar sistemas fiables, certificaciones y relaciones de canal ayudan, pero competidores como Schneider, ABB y Hubbell también invierten. No se presume poder de fijación ilimitado de precios ni crecimiento perpetuo de gasto AI.

Q3 ventas **8.947**, crecimiento 28%: 19% orgánico, 8% adquisiciones y 1% divisas. Segmentos publican margen de **25,3%**, pero no es margen EBIT consolidado: coste corporativo, amortización y otros conceptos importan. Beneficio pretax 1.370 más interés neto 198 da EBIT calculado **1.568**, margen 17,53%. La resta ventas−coste−SG&A−I+D da 1.589, con redondeo y otros gastos fuera de ese subtotal. EPS GAAP 2,77 frente a ajustado 3,68: ajustes incluyen 0,62 por amortización y 0,30 por adquisiciones/divestitures, parcialmente compensados por ingreso de reestructuración. No se adopta automáticamente el ajustado como beneficio económico sostenible. [Comunicado]({S['release']}) y [10-Q]({S['q3']}).

La guía FY26 de EPS GAAP 10,39–10,49 y ajustado 13,70–13,80 no es un FCFF ni una valoración. El backlog firme es aproximadamente **26.200**, con 72% dirigido a entrega en doce meses. La empresa distingue pedidos abiertos históricamente sujetos a liberaciones de cliente de compromisos firmes incluidos en backlog. Incluso estos pueden sufrir retrasos y requieren inventarios, personal y capex. La tesis favorable exige convertir pedidos en caja y rentabilidad después de corporativo y capital, no solo elevar ventas.

En Q3 la empresa atribuye 360 pb de presión de margen bruto a materias primas/salarios y 210 pb a amortización, compensados parcialmente por 200 pb de volumen. Es evidencia de que la fuerte demanda no elimina inflación de costes. La refutación de la tesis sería menor conversión de backlog, cancelaciones, competencia que comprima precio, integración deficiente, más financiación de inventario o inversión que no genere retornos suficientes.

## 3. Historia reproducible y perímetro

| Periodo | Ventas | EBIT calculado GAAP | CFO | Capex bruto caja | FCF bruto | Amortización intangible divulgada |
|---|---:|---:|---:|---:|---:|---:|
'''
for n in ['FY2023','FY2024','FY2025','Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026','TTM_2025Q3','TTM_2026Q3']:
 a=H[n];t+='| '+n+' | '+' | '.join(f(a[k]) for k in ['revenue','gaap_ebit','cfo','gross_capex','fcf_cfo_less_gross_capex','intangible_amortization'])+' |\n'
t+=f'''
TTM ventas aumentan 20,1%, pero EBIT calculado solo 9,4%; margen cae de 18,84% a 17,16%. FCF bruto aumenta 14,2%. La inversión fija crece 42,3%, más que ingresos. El consumo de circulante TTM baja de 875 a 455; esta mejora de 420 ayuda a caja y no debe extrapolarse como ingreso recurrente. El histórico contiene tres ejercicios, cuatro trimestres y TTM contra anterior, con procedencia numérica, signos y fórmulas. [10-K]({S['fy25']}).

EBIT es pretax más interés neto, no subtotal GAAP separado: conserva otros ingresos/gastos no operativos. Se ofrece también subtotal operativo. El trimestre derivado de nueve menos seis meses da EBIT Q3 **1.567**, frente a **1.568** divulgado directamente; diferencia de redondeo, no un ajuste oculto. La ancla del modelo usa el trimestre directo y la tabla histórica usa la resta documentada.

EPS diluido publicado FY23/FY24/FY25 es **8,02/9,50/10,45**; nueve meses2026 baja a **7,10** desde7,54, aunque ventas crecen. El EPS incorpora financiación, impuestos y amortización; no se suma una variación de EPS a un DCF de flujos. No se fabrica un EPS TTM exacto sumando cocientes con denominadores diferentes.

SBC anual es **97/108/126** en FY23/24/25. Gasto trimestral completo, SBC del estado de flujos y capitalizado no están aislados en las fuentes revisadas: permanecen **null**, no cero. No se inventa FCF del propietario restando una cifra trimestral desconocida ni se confunden emisiones netas de acciones con SBC. El DCF conserva remuneración en márgenes. Tampoco añade reestructuración o costes de adquisición al EBIT ancla.

La amortización divulgada es de intangibles, sin reconciliación completa de adquirido frente a otro. FY25 contiene una discrepancia documental: Note 6 muestra 461, mientras reconciliación corporativa y MD&A muestran 486. Se utiliza 486 en la serie consistente con el puente corporativo, sin inventar explicación para los 25. El modelo trabaja antes de amortización intangible divulgada, no afirma que toda sea adquirida. I+D y gasto de negocio permanecen en margen; suelo de inversión y sensibilidad de carga adicional de reposición intangible 0,5/1/2 puntos de ventas evitan asumir renovación gratuita. No se suma un escudo fiscal automático por amortización contable.

### Adquisiciones ya pagadas

Boyd Thermal cerró **12 marzo por 9.549 netos de caja**, no se vuelve a restar la compra del puente porque la caja/deuda de septiembre ya la incorpora. Ultra PCS cerró **23 enero por 1.529 netos**. Salida conjunta de adquisiciones en nueve meses, **11.079**, no es mantenimiento ordinario ni una segunda deuda. Fibrebond cerró abril de 2025 y también altera comparabilidad.

Boyd aporta desde cierre 1.058 de ventas y 257 de **beneficio de segmento**; Ultra, 166 y 47. No son beneficios GAAP consolidados ni una cuenta anual proforma. El precio asignado a Boyd incluye intangibles 7.142 y goodwill 3.771, con medición todavía provisional; goodwill no deducible según la nota. Una revisión contable del precio no genera efectivo ni justifica sumar goodwill al valor por DCF. [Adquisiciones, Note 2]({S['q3']}).

## 4. Mobility: canje y financiación, no dividendo uniforme

El acuerdo de 10 junio, modificado 16 octubre, prevé separar Mobility mediante **split-off** y combinarla con Dana por Reverse Morris Trust. Los accionistas que participen entregarán acciones Eaton a cambio de SpinCo; las acciones ETN aceptadas se amortizan. Solo si quedan acciones SpinCo sin colocar existiría distribución residual pro rata a ETN remanente. Por tanto el **50,1%** colectivo previsto para antiguos titulares Eaton no corresponde automáticamente a cada acción ETN actual. Canje plenamente suscrito puede dejar sin distribución SpinCo a quien no participe.

El prospecto preliminar no fija todavía descuento, límite superior, ratio, fechas de valoración ni vencimiento; no hay ratio mínimo. Hay prorrateo por sobresuscripción y condiciones para lotes pequeños. Los 98.079.878 títulos SpinCo estimados en proforma no permiten inventar un derecho final por acción ETN ni reducir el denominador por una cantidad arbitraria. [S-1/S-4, 19 octubre](https://www.sec.gov/Archives/edgar/data/2142558/000119312526425388/d128758ds4.htm).

El cobro anunciado aproximado de **1.100** para entidades Eaton está sujeto a caja/deuda, impuestos, true-up, ajustes por recompras Dana y rutas de venta directa. La página 153 proforma muestra 1.101+301−245−363=**794** como pago SpinCo. Los 245/363 son compras directas de Royal Precision/Specified Assets a entidades Eaton, **no ingresos perdidos del grupo**. Sustituir todo el cobro por 794 o sumar todo sin reconciliar impuestos/rutas sería erróneo.

Financiación prevista: puente original 2.600 menos 350 reemplazados por Term A 350, dando **2.250+350=2.600**, no 2.950. Revolver 1.200 no dispuesto no es caja. Proforma de junio incluye refinanciación Dana de 1.111 y otros usos; no es deuda de ETN ya desembolsada en septiembre. La ausencia de condición de financiación en el merger no garantiza fondos. No se añaden simultáneamente 1.100 de efectivo, 50,1% de equity combinado y el valor de Mobility retenida.

Fecha esperada actualizada: **primeros cuatro meses de 2027**, no fecha firme. Outside date 10 junio 2027, con extensión condicional de tres meses. Aprobación de accionistas Dana, reguladores, registro efectivo, solvencia, reservas distribuibles y opiniones fiscales siguen siendo condiciones. Una fecha de filing no certifica que estén cumplidas. Si falla el RMT, Eaton pretende spin-off independiente: ni el fracaso equivale a conservar indefinidamente el perímetro. El DCF siguiente es deliberadamente un **contrafactual analítico**, no ese desenlace pronosticado. [Actualización 3 noviembre]({S['transactionUpdate']}).

## 5. COL y capital: separar hechos de reservas elegidas

COL Group se contrató el 25 septiembre por **810 millones EUR**, 921 USD a FX de septiembre, con cierre esperado Q1 2027 y sujeto a autorizaciones. No está incorporado en el balance/EBIT modelado. La sensibilidad usa 905,499 USD a FX ECB 3 noviembre 1,1179 y valores hipotéticos del activo adquirido; no llama cero a su negocio ni suma beneficio sin pagar la compra. Hace falta un FCFF standalone y financiación para incorporar el cierre al valor total. [Note 2]({S['q3']}) y [ECB](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml).

| Puente seleccionado, antes de operaciones pendientes | USD millones |
|---|---:|
| Caja más inversión corta al 30 septiembre | 818 |
| Reserva operativa elegida | −500 |
| Deuda contable, corto más largo | −20.106 |
| Reserva elegida diferencia nominal/costes de deuda | −150 |
| Pensiones más otros beneficios postempleo | −780 |
| Reserva fiscal histórica seleccionada | −1.518 |
| Minoritarios económicos seleccionados | −100 |
| Reestructuración pendiente | −93 |
| Puente total | {f(R['base']['capitalBridge'])} |

La reserva de 150 no es conciliación exacta de nominal: FY25 tenía costes/descuentos y ajustes de cobertura, y las emisiones de marzo recibieron menos efectivo que principal. Se prueba 0/150/300, sin afirmar que deuda contable sea toda la reclamación contractual. La deuda incluye financiación de compras cerradas; no se añade otra vez el precio de Boyd. Los 8.000 de delayed-draw se cancelaron sin disposición; el revolver 4.000 no se suma a caja. Papel comercial 1.592 ya está en deuda corta. Arrendamiento financiero FY25 25 ya estaba en deuda; no se agrega duplicado. Arrendamientos operativos permanecen en gastos, sin restar pasivo y retener simultáneamente el coste completo como si fuera otra deuda.

Reserva fiscal 1.518 = UTB bruto FY25 1.300 más intereses/penalizaciones 218, último desglose disponible, **no obligación exacta actual**. El 27 octubre IRS notificó 290 de impuestos y 120 de sanciones sobre 2014–2016, pendientes de litigio; pueden solaparse con reservas. No se añaden 410 automáticamente al caso central. Se prueba 0/1.000/1.518/1.928/2.500. La tasa futura de 24% grava beneficios nuevos; no liquida por arte de fórmula disputas históricas. El recurso debe presentarse antes o el 25 enero de 2027. No se ofrece opinión jurídica sobre resultado. [Fiscalidad FY25]({S['fy25']}) y [Note 11 Q3]({S['q3']}).

Minoría contable 47 frente a beneficio atribuible de cuatro millones en nueve meses motiva una reserva económica elegida 100, con variantes 47/100/200; no es tasación de sus contratos. Pensiones 623 y otros beneficios 157 se deducen sin presumir transferibilidad de superávits de otros planes. Se conserva gasto de servicio en márgenes; algunos conceptos no operativos de pensión pueden permanecer en el EBIT calculado, por lo que no es una conciliación actuarial exacta.

SCF proveedores **763**, frente a 543 al inicio del año, forma parte de proveedores y CFO. No se resta todo como deuda adicional mientras ya financia el circulante. Una retirada de financiación se prueba como salida extra 763, sin afirmar que sea pérdida demostrada. Arrendamiento sintético de fábrica previsto 185, inicio H1 2027 y garantía residual aproximada 85%, presenta compromiso adicional: uso, valor residual y clasificación no están plenamente conciliados. La sensibilidad de capital deduce157,25 adicionales como estrés de esa garantía, sin convertirla en deuda vencida cierta ni certificar ausencia de solapamiento con capex/arrendamiento modelado.

Inversiones no cotizadas: la compra de aproximadamente7% de SPAN por75 el15enero forma parte de los92 de inversiones realizadas en nueve meses. El puente no añade su valor porque no está económicamente conciliado; **excluir no significa que valgan cero**. Se muestran adiciones hipotéticas92/250, sin tratar coste como valor razonable ni deducir otra vez efectivo ya gastado. No se añade ingreso futuro de SPAN al margen industrial ni se presume cobro inmediato de su inversión. [Note2 y cash flow]({S['q3']}).

Acciones publicadas **388,5 al 30 septiembre**, más proxy elegido de un millón de premios netos, total 389,5. El proxy se basa en diferencia Q3 diluida−básica, no es un puente exacto de premios; se prueba hasta cinco millones. No hubo recompras en nueve meses y el programa autorizado no es activo ni reducción gratuita de acciones. Dividendo declarado 1,10, registro 10 noviembre/pago 27 noviembre: no estaba pagado al cierre usado. El análisis es cum-dividend; no se resta el pago futuro olvidando el derecho económico del accionista. No se confunde la fecha de registro con una nueva fecha de resultados. [Dividendo primario]({S['dividend']}).

## 6. DCF contrafactual financiado, no valor total actual

Se mantienen los negocios hoy consolidados, incluida Mobility, y se excluye COL. No hay ingresos de separación ni deuda SpinCo añadida. Ancla: Q3 directo anualizado, ingresos **35.788** y EBIT anterior a amortización intangible **7.528** =4×(1.370+198+314). Es una aproximación de ritmo actual con negocios adquiridos presentes todo el trimestre, **no guía ni proforma anual**. Usar TTM parcial 31.984/6.320 como ancla alternativa reduce base a **{f(V['sensitivity']['reportedTTMAnchor']['value'])}**, porque cambia reinversión inicial; puede cobrar expansión adquirida ya pagada. Se muestran ambas sin declarar una exacta.

Periodos anuales 3 noviembre 2027–2036, no ejercicios fiscales exactos ni stub diciembre inventado. Márgenes después de SBC y antes de la amortización intangible seleccionada; impuesto 24%, frente a tasas históricas favorecidas por jurisdicción/beneficios fiscales. No se suma automáticamente deducción fiscal contable. D&A residual elegido 1,8% de ventas no se llama mantenimiento observado. Capex piso 4% base al inicio y 3,5% final, y circulante 25% del incremento positivo de ingresos. Se comparan reinversión física (capex−D&A+circulante) y aumento positivo de NOPAT/ROIC; se carga la mayor. El margen adicional también requiere financiación. La misma restricción física y económica sigue en terminal. El suelo económico ΔNOPAT/ROIC domina los diez años base y favorables, y seis adversos; por eso variar circulante15–35% puede no alterar el valor. No implica que el circulante sea irrelevante: está financiado dentro del mayor requisito de inversión, y un suelo físico superior sí reduce FCFF.

Rf 10Y 3 noviembre 4,95%, ERP 1 noviembre 4,41% y beta proveedor 1,14 producen coste de equity **{rates['costEquityCAPM']:.4%}**. Con deuda contable y coste elegido4,8%, WACC proxy **{rates['calculatedWaccProxy']:.4%}**. Base9,75% añade colchón discrecional, no es redondeo; ERP y rf no son sincrónicos y deuda libro no es mercado. [Treasury]({rates['sources'][0]}), [ERP]({rates['sources'][1]}) y [beta]({S['beta']}).

| Supuesto | Adverso | Base | Favorable |
|---|---:|---:|---:|
| Ingresos año1 | 34.000 | 37.000 | 40.000 |
| Crecimientos años2–5 | −3/3/4/4% | 10/8/7/6% | 15/12/10/8% |
| Crecimientos años6–10 | 3,5/3/2,5/2,5/2,5% | 5/4,5/4/3,5/3,5% | 7/6/5,5/5/4,5% |
| Margen año1→10 | 19→19% | 22,5→24% | 24→27% |
| ROIC incremental | 15% | 20% | 25% |
| WACC / g terminal | 11% / 2,5% | 9,75% / 3% | 8,75% / 3,5% |

| Año base | Ventas | EBIT preintangibles después SBC | NOPAT | Inversión neta | FCFF |
|---|---:|---:|---:|---:|---:|
'''
for a in R['base']['rows']:t+='| '+str(a['year'])+' | '+' | '.join(f(a[k]) for k in ['revenue','ebitAfterSbcBeforeDisclosedIntangibleAmort','nopat','netReinvestment','fcff'])+' |\n'
t+='\n| Caso | EV | Residuo equity contrafactual | Por acción seleccionada | Terminal/EV |\n|---|---:|---:|---:|---:|\n'
for n,a in R.items():t+=f"| {n} | {f(a['enterpriseValue'])} | {f(a['equityCounterfactual'])} | {f(a['counterfactualPerShare'])} | {a['terminalShare']:.1%} |\n"
t+=f'''
## 7. Sensibilidades y qué exige el precio

| Cambio aislado base | Valor contrafactual |
|---|---:|
'''
for key,label in [('historicTaxReserve','Reserva fiscal'),('debtFaceAdjustment','Ajuste deuda'),('awardDilution','Premios netos'),('wc','Circulante/ventas')]:
 for a in V['sensitivity'][key]:t+=f"| {label} {a['input']} | {f(a['value'])} |\n"
t+=f'''
Subir el capex en dos puntos de ventas de forma recurrente, incluido terminal, reduce base a **{f(V['sensitivity']['capex'][-1]['value'])}**. Una carga adicional permanente de reposición intangible de dos puntos de margen deja **{f(V['sensitivity']['intangibleReplacementMarginCharge'][-1]['value'])}**. El archivo de pruebas contiene malla WACC/g, ROIC, impuestos, capital y sensibilidad COL con inversión financiada. No se interpreta el activo COL hipotético cero como cota inferior garantizada ni se afirma que la compra vaya a destruir todo el efectivo.

Inverso al cierre391,70: conservando otras variables base, requiere aproximadamente **{V['inverse']['growth']['shift']*100:.2f} puntos** más de crecimiento cada año2–10, o **{V['inverse']['margin']['shift']*100:.2f} puntos** más de margen. Son experimentos separados, no consenso ni guía. Ambos barridos son monótonos y financian incremento de beneficios. Un estrés conjunto de trayectoria favorable, margen28% y WACC8% produce **{f(V['sensitivity']['jointStrongDemand'][0]['value'])}**; por ello un entorno de ejecución excepcional puede justificar más que los casos centrales. No se obliga al modelo a rechazar el precio.

## 8. Contraste operativo y de valoración

'''
cp=P/'comps/report_section.md'
t+=cp.read_text() if cp.exists() else 'Contraste contemporáneo en preparación. No se presenta una mediana ni una valoración relativa certificada mientras faltan datos de pares.\n'
t+=f'''
## 9. Calendario y cierre de investigación

Q3 se publicó efectivamente el **3 noviembre**, con 10-Q ese mismo día. La página de eventos consultada todavía no confirma siguiente resultado trimestral: queda pendiente el requisito de calendario confirmado. Registro de dividendo10 noviembre y pago27 noviembre son eventos distintos. COLQ1 y Mobilityprimeros4meses2027 son ventanas sujetas a condiciones, no días cerrados de ejecución. [Calendario del emisor]({S['calendar']}).

Para una conclusión operable faltan: ratio/cap/aceptación del canje, denominador ETN posterior, caja neta de impuestos/ventas directas, costes retenidos y standalone de negocios, financiación combinada y destino del derecho SpinCo; además cierre/FCFF de COL, capital posterior, premios netos y alcance fiscal. El dossier avanza historia, riesgos y exigencias de valoración, sin sustituir estas incógnitas por cifras aparentes.

Conclusión ES: **Esperar; investigación parcial y perímetro contrafactual.** La demanda eléctrica es fuerte y el negocio adquirido amplía capacidades, pero capital, inversión y derechos de separación impiden certificar hoy valor total por acción. Casos centrales no prueban margen de seguridad; no entrada.

Conclusion EN: **Wait; partial research with a counterfactual perimeter.** Electrical demand is strong and acquisitions expand capabilities, but capital, reinvestment and separation rights prevent a certified current total per-share valuation. Central cases do not establish a margin of safety; no entry approval.

## Fuentes y reproducción

Las tablas se basan en [10-K FY25]({S['fy25']}), [10-Q Q3]({S['q3']}) y trimestres previos identificados en history/source_manifest.json. Los documentos íntegros no forman parte de la publicación. Ejecutar reproduce.py regenera historia, DCF, sensibilidades y QA offline con Python estándar. Los hechos conservan periodo, unidad, tag y URL; supuestos y carencias se distinguen. Reproducir un cálculo no valida su desenlace económico.
'''
(P/'report.md').write_text(t)
s={'ticker':'ETN','company':'Eaton Corporation plc','researchDate':'2026-11-04','valuationDate':'2026-11-03','status':'partial_counterfactual_audited','readyForPublication':True,'fairValue':None,'fairValueTotal':None,'bear':None,'base':None,'bull':None,'counterfactualScenarios':{n:a['counterfactualPerShare'] for n,a in R.items()},'scenarioScope':'Current consolidated perimeter, no Mobility separation or COL acquisition; counterfactual, not current aggregate equity value.','scanPrice':423.49,'scanDate':'2026-10-13','scanQuality':90,'scanOpportunity':85,'scanRsi':48.1,'scanStage2Historical':True,'scanStage2Current':None,'latestClose':391.70,'latestCloseDate':'2026-11-03','nextEvent':{'date':None,'confirmed':False,'type':'Next quarterly earnings not confirmed','sourceUrl':S['calendar']},'otherEvents':[{'date':'2026-11-10','type':'Dividend record date','sourceUrl':S['dividend']},{'date':'2026-11-27','type':'Dividend payment date','sourceUrl':S['dividend']}],'sources':S,'entryApproved':False,'stage3Complete':False,'stage35Approved':False,'confidence':'Reported history reconciles, with disclosed rounding and amortization discrepancy. Actual shareholder total remains unresolved due to exchange rights, capital, tax and pending acquisitions.','conclusionEs':'Esperar. Investigación parcial; el DCF mantiene un perímetro contrafactual, no certifica valor total actual ni entrada.','conclusionEn':'Wait. Partial research; DCF retains a counterfactual perimeter and does not certify current total value or entry.','pros':[{'textEs':'Fuerte crecimiento orgánico eléctrico y backlog firme; aún requiere inversión y conversión en caja.','textEn':'Strong electrical organic growth and firm backlog; still requires investment and cash conversion.','evidence':pro,'sourceUrl':S['q3']}],'cons':[{'textEs':'Deuda elevada tras compras y TTM con perímetro parcial; no confundir crecimiento de ventas con caja libre.','textEn':'High post-acquisition debt and partial acquired TTM perimeter; revenue growth is not free cash generation.','evidence':con,'sourceUrl':S['q3']},{'textEs':'Canje Mobility pendiente sin ratio ni denominador final; no valoración total actual certificada.','textEn':'Pending Mobility exchange lacks a final ratio and denominator; no certified current total valuation.','evidence':con2,'sourceUrl':'https://www.sec.gov/Archives/edgar/data/2142558/000119312526425388/d128758ds4.htm'}]}
(P/'summary.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n');print('report',len(t.split()),'words')
