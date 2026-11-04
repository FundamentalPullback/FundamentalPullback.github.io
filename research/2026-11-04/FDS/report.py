from pathlib import Path
import json
P=Path(__file__).parent;F=json.load(open(P/'financials.json'));M=json.load(open(P/'model.json'));PE=json.load(open(P/'peers.json'));U=json.load(open(P/'sources/urls.json'))
U.update(price='https://stockanalysis.com/stocks/fds/history/',bcc='https://www.factset.com/newsroom/press-release/factset-marks-a-new-era-in-enterprise-real-time-market-data-as-it-acquires-bcc-group-international',msci_q3='https://ir.msci.com/node/22986/pdf',msci_k25='https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm',msci_price='https://stockanalysis.com/stocks/msci/history/',investor_day='https://investor.factset.com/news-releases/news-release-details/factset-host-investor-day-november-10-2026',bcc_mirror='https://factset.gcs-web.com/news-releases/news-release-details/factset-marks-new-era-enterprise-real-time-market-data-it',rf='https://www.federalreserve.gov/releases/h15/')
json.dump(U,open(P/'sources.json','w'),indent=2)
def cite(*ks):return '\n\nFuentes: '+', '.join(f'[{k}]({U[k]})' for k in ks)+'.\n\n'
def tab(h,rs):return '| '+' | '.join(h)+' |\n| '+' | '.join(['---']*len(h))+' |\n'+''.join('| '+' | '.join(str(v) for v in r)+' |\n' for r in rs)+'\n'
def hist(k):return tab(['Periodo','Ventas','EBIT','Neto','EPS','CFO','Capex','SBC','FCF−SBC'],[[d['period']]+[f'{d[x]:,.3f}' for x in ['revenue','ebit','net_income','eps','cfo','capex','sbc','fcf_less_sbc']] for d in F[k]])
s='''# FDS: recuperación prevista, reinversión y capital posterior aún condicionan el valor

**FactSet Research Systems · NYSE · USD · 4 noviembre 2026. Corte: 16:10 UTC. Precio de referencia: cierre regular del 3 noviembre, 332,59 USD.** No se usa el precio intradía del 4 noviembre como cierre ni se cambia retrospectivamente el escáner.

## Decisión

**Esperar precio o evidencia más firme.** Reconstrucción independiente FCFF: **147,32 adverso, 238,53 central y 402,59 favorable**. La base utiliza el capital de agosto y la guía del negocio disponible; no certifica la compañía combinada tras BCC porque sus términos económicos y el uso del nuevo crédito no están reconstruidos. El favorable no es techo de compra ni previsión garantizada. Sin entrada Stage 3.5, sin orden, cantidad ni stop.

La caja anual mejora y la suscripción conserva buena retención. Pero el EBIT cae, normalizar solo reestructuración lo deja casi plano, y parte de la mejora de caja procede de remuneración acumulada. No se usa el PER de la guía ajustada como sustituto del análisis de caja.

Se preserva A022: valores exploratorios publicados 198/248/295. Su archivo de soporte original no está recuperado; este trabajo **no es una reproducción exacta** de aquel código. Cambios de método e hipótesis se explican, sin inventar un puente preciso entre archivos ausentes.
'''+cite('q4','k26','price','bcc')+'''## 1. Calidad y evidencia comercial

FactSet vende datos y herramientas de trabajo para profesionales financieros. Integración con procesos, cobertura y distribución generan costes de sustitución, pero compite con otros proveedores, soluciones propias de clientes e IA. La demanda de datos verificados puede crecer con IA, mientras se intensifica la presión sobre interfaces, precios y costes de tecnología. No se asume que la etiqueta IA otorgue un margen mayor sin inversión.

FY2026: ingresos +6,65%; orgánico +6,7%; ASV orgánico +7%. Retención anual de ASV superior a 95%, y de clientes 90% frente a 91%. ASV es una medida de ingresos futuros de suscripciones actualmente suministradas, no caja ya cobrada ni backlog irrevocable. Clientes 9.258 y usuarios 260.671 al cierre de agosto.

Guía FY2027: ventas 2.600–2.625 M$, ASV orgánico +5–6,5%, margen GAAP 31–32%, EPS GAAP 17–17,50; los 34,75–35,25% de margen y 19,25–19,65 de EPS son ajustados. El modelo arranca del margen GAAP, sin aplicar el ajustado al negocio completo. Se conserva SBC y remuneración recurrente.

El 10-K de octubre declara remediada a agosto la debilidad material previa de controles de TI sobre ingresos, cuentas por cobrar y diferidos; la auditoría de controles es favorable. No se arrastra como si siguiera abierta, pero la remediación no elimina riesgo de futuras deficiencias o integración.
'''+cite('k26','q4')+'''## 2. Historia reproducible: 3FY, 4Q y TTM comparable

Millones de USD salvo EPS. Capex incluye software interno capitalizado. FCF = CFO − capex; FCF−SBC es un proxy conservador para el accionista, no FCFF ni beneficio contable. Como el último corte es agosto, el TTM coincide con FY2026 y su comparable con FY2025; no se inventan meses adicionales.

'''+hist('annual')+'\n'+hist('quarters')+'''
TTM agosto 2026 frente a agosto 2025: ingresos 2.476,256 frente a 2.321,748; EBIT 699,957 frente a 748,303; neto 533,481 frente a 597,040; CFO 822,200 frente a 726,260; capex 114,720 frente a 108,806; FCF 707,480 frente a 617,454; SBC 84,099 frente a 61,229; FCF−SBC 623,381 frente a 556,225. Los importes Q4 de flujos se reconstruyen restando nueve meses al ejercicio completo. EPS Q4 procede del comunicado; los EPS trimestrales no deben sumarse para reemplazar el denominador anual ponderado.
'''+cite('k26','q1','q2','q3','q4')+'''## 3. Normalización: cuánto mejora realmente

EBIT FY2026 −6,46%, neto −10,65% y EPS −6,30%. Las recompras reducen acciones y amortiguan la caída del EPS, sin crear beneficio operativo. Los cuatro EBIT trimestrales bajan de 192,071 a 184,961, 166,301 y 156,624 M$; la estacionalidad no permite tratar esa secuencia sola como pronóstico, pero tampoco respalda una afirmación de aceleración operativa actual.

Añadir únicamente reestructuración/severance 46,2 M$ al EBIT FY2026 da 746,157, frente a 748,562 en FY2025 añadiendo su cargo comparable 0,259: −0,32%, prácticamente plano. La normalización no suma CEO onboarding 19,521, amortización adquirida 76,205, SBC ni todos los demás costes excluidos por la dirección. El ajuste completo de la compañía produce EBIT 855,308 frente a 843,432, +1,4%, y margen ajustado baja de 36,3 a 34,5%. Incluso esa métrica no equivale a gran aceleración.

FY2025 incluía ganancia de desinversión 23,238 M$ fuera de EBIT. Explica parte de la diferencia del beneficio neto, no se resta de EBIT otra vez. EBIT GAAP y neto normalizado no son intercambiables.

CFO +13,21%, FCF +14,58%, FCF−SBC +12,07%. SBC +37,35%. El aumento de remuneración acumulada aporta 62,553 M$ al CFO, frente a 35,666 el año anterior; no se perpetúa una liberación de caja de esa magnitud. Sensibilidad: quitar toda la aportación de 62,553 al proxy deja 560,828 M$, no 623,381. No significa que toda sea extraordinaria o que deba pagarse inmediatamente; muestra cuánto depende la conversión del calendario de pagos. Dividendos y recompras suman 808,145 M$, por encima de FCF 707,480, antes de otros usos.

Amortización total de intangibles en el 10-K: 155,335 M$, que incluye tecnología interna desarrollada; no toda es adquirida. D&A total 180,830. La conciliación ajustada elimina 76,205 de amortización adquirida; residual de D&A 104,625 = 4,225% de ventas. El modelo devuelve 4% y conserva como coste económico una reserva por intangibles adquiridos y prudencia adicional. No se confunde residual con depreciación física pura ni se omite software del capex.
'''+cite('k26','q4')+'''## 4. Capital de agosto y lo que todavía no sabemos de BCC

Puente desde valor de operaciones al equity, M$:
'''+tab(['Partida','Importe','Tratamiento'],[['Caja',233.339,'No incluye restringida'],['Inversiones corrientes',31.993,'Fondos de inversión; no sumar money markets otra vez'],['Reserva de caja operativa',-100,'Supuesto explícito'],['Deuda nominal',-1375,'No usar valor contable neto de costes como principal'],['Contingentes de adquisiciones',-10.201,'Saldo fair value; separado de pagos ya realizados'],['Impuestos no corrientes',-25.502,'Reserva por posiciones previas'],['Dividendo declarado pendiente',-40.901,'Obligación ya contraída a agosto'],['Reserva por litigio',-.650,'Anclada al cargo FY2026; saldo impagado no certificado'],['Puente total',M['capital_bridge']['net'],'Capital fechado, no balance de noviembre certificado']])+'''
La deuda contable es 1.370,022 M$, pero principal 1.375. Los aproximadamente 500 M$ corrientes se refieren a vencimiento próximo; no se suma ese principal otra vez sobre deuda total. Refinanciarlo puede cambiar coste e intereses. Intereses ya salen del puente FCFF a través del coste de capital y deuda, no se restan de NOPAT.

Caja restringida 6,296 M$ se excluye. Fondos monetarios 25,008 ya están dentro de caja: no se vuelven a sumar como inversión. Fondos de inversión corrientes 31,993 sí son separados y se valoran a libro/fair value publicado, sujetos a mercado. Leases operativos conservan gasto en EBIT y no se descuentan otra vez como deuda. Las cuentas ordinarias de impuestos y remuneración se tratan operativamente; la reserva fiscal no corriente y dividendo son claims separados. Los 0,650 M$ por litigio se anclan al cargo FY2026; no se ha confirmado aquí que todo siga impagado. Es una reserva conservadora, no una deuda adicional exacta. No se vuelve a restar el pago diferido de adquisición de 15,327 ya pagado en FY2026.

**BCC se adquirió después de agosto.** El anuncio del 22 septiembre no divulga términos y dice no esperar un efecto material en resultados; eso no informa el precio pagado ni certifica que el efecto en caja sea cero. El 10-K informa además 90 M$ de disposición de revolver posterior al balance. No se afirma que esos 90 sean el precio de BCC, ni se añade deuda sin mirar la caja recibida y usada.

El central utiliza el negocio y capital de referencia con limitación explícita. Nueva disposición retenida en caja aumenta efectivo y deuda por igual: efecto neto cero antes de costes. Si los 90 se gastaron y no se atribuye valor operativo adicional, sensibilidad central 236,00. Usos netos 150/300 M$ dan 234,31/230,10. Son sensibilidades sin probabilidad, no precio supuesto ni límites del acuerdo. Un uso de 100 M$ cambia valor 2,81 USD por acción. Nuevas acciones, pasivos, costes y contribución de BCC no están certificados; por tanto no hay valoración combinada actual completa.
'''+cite('k26','bcc')+'''## 5. Modelo FCFF y financiación del crecimiento

Año 1 FY2027: ingresos 2.612,5 M$, punto medio oficial. Años siguientes de crecimiento explícito: 5/5/4/4%; transición años 6–10 a 3%. Márgenes EBIT: 31,5/31,8/32/32,3/32,5%, después 32,5%; impuestos 20%. El comienzo supone recuperación hacia la guía, no reutiliza el margen ajustado. La senda no incluye futuras adquisiciones gratuitas.

D&A económica devuelta 4% de ventas, capex 4,5% incluyendo software, ΔNWC 8% del incremento de ventas. Son hipótesis normalizadas. NOPAT = EBIT×80%; FCFF = NOPAT−reinversión. En años 1–5 se usa la mayor reinversión entre capex−D&A+ΔNWC y NOPAT×crecimiento/ROIC; no se combina expansión con capital gratuito. Años 6–10 transitan al 20/40/60/80/100% hacia la regla económica. En los tres casos domina la inversión económica, de modo que esa mezcla no altera sus cifras.

La regla de reinversión usa crecimiento de ventas, no crecimiento de NOPAT: la recuperación de margen se supone sobre capacidad instalada. El 20% no es un ROIC incremental contable demostrado. ROIC de modelización 20%, supuesto apoyado solo parcialmente por proxy histórico 18,90%: EBIT normalizado 746,157×80% / capital medio (patrimonio+deuda−caja/inversiones) de dos cierres. Incluye goodwill, pero las recompras y adquisiciones pueden distorsionar el cociente; no prueba retorno incremental. Terminal g 3%, reinversión 15% de NOPAT; el año 10 ya converge a esa regla.

WACC 9,1%: Treasury 10 años 4,91% del 2 noviembre; beta **asumida** 1,05 y prima mercado **asumida** 4,5%, coste equity 9,635%. Ponderación objetivo 90/10 equity/deuda, coste deuda normalizado 5%, tax 20%: 9,0715%, redondeado 9,1%. No se presenta beta/prima como regresión o estimación contemporánea verificada. El coste de deuda es hipótesis de refinanciación, no cupón de toda la cartera vigente.

Acciones diluidas Q4 35,572 M constantes. Se mantienen SBC y costes recurrentes en margen; no se resta SBC otra vez al FCFF ni se financian recompras futuras gratis. Premios antidilutivos o aún sujetos a condiciones pueden crear dilución futura; las medias diluidas históricas no garantizan que toda esté capturada. Stress adicional de 3% de acciones, no pronóstico.

Convención temporal: el modelo valora flujos de FY2027–36 a fin de cada ejercicio con referencia de inicio FY2027; los 238,53 son esa convención, no una precisión diaria falsa del 3 noviembre. Rodar dos meses el EV manteniendo el mismo puente da 242,55, sensibilidad temporal que tampoco certifica capital post-BCC. No se añade caja de septiembre/octubre no comprobada.
'''+cite('q4','k26','rf')+tab(['Año','Ventas','Margen EBIT','NOPAT','Reinversión','FCFF'],[[d['year'],f"{d['revenue']:.2f}",f"{d['ebit_margin']*100:.2f}%",f"{d['nopat']:.2f}",f"{d['reinvestment']:.2f}",f"{d['fcff']:.2f}"] for d in M['cases']['base']['rows']])+'''## 6. Escenarios y reverse del mismo modelo

'''+tab(['Caso','USD','Cambios frente a base'],[['Adverso','147,32','Crecimiento primeros 5 años −2,5 pp; margen todos 10 años y terminal −2,5 pp; WACC10,1%, g2%, ROIC16%'],['Central','238,53','Senda descrita; WACC9,1%, g3%, ROIC20%'],['Favorable','402,59','Crecimiento primeros 5 años +2,5 pp; margen todos 10 años y terminal +2 pp; WACC8,1%, g3,5%, ROIC25%']])+f'''
Terminal descontado: {M['cases']['base']['terminal_weight']*100:.2f}% del EV. El favorable necesita mejoras simultáneas, no una mera vuelta al múltiplo histórico. Impuesto 18/20/23% da 245,40/238,53/228,23. Con 3% más acciones, {M['dilution_sensitivity']:.2f}. Relajar el guard de inversión al inicio y usar solo capex−D&A+circulante produce 258,66, no nueva base.

Para justificar 332,59 con el modelo base, el reverse exige aproximadamente **+7,50 puntos de crecimiento en cada uno de los primeros cinco años** manteniendo los demás supuestos. Alternativa separada: **+11,09 puntos de margen** en todos los años y terminal, hasta 42,59% en FY2027 y 43,59% terminal. No son forecasts; la inversión requerida sigue dentro de cada solve y las dos condiciones no se imponen juntas.

'''+tab(['WACC','g','USD'],[[f"{d['wacc']*100:.1f}%",f"{d['g']*100:.1f}%",f"{d['value']:.2f}"] for d in M['sensitivity']])+tab(['ROIC','USD'],[[f"{d['roic']*100:.0f}%",f"{d['value']:.2f}"] for d in M['roic_sensitivity']])+'''## 7. Historia, comparación y límites de continuidad

A003 usó múltiplos de EPS y descuento a un año; A022 sustituyó esa lectura por comprobaciones operativas de diez años, pero las describió expresamente como exploratorias. Sus valores 198/248/295 siguen como historia, no como certificado actual. Del A022 se recuperan margen base 31,5%, tasa de descuento 9% y criterios de reposición descritos solo parcialmente; no toda la senda numérica. No se fabrica un modelo anterior para que sus resultados coincidan.

El nuevo 238,53 frente a 248 difiere por horizonte/modelo explícitamente reconstruidos, obligación de financiar crecimiento desde año 1, hipótesis de coste de capital, software/amortización, shares Q4 y reservas de capital. Los estados FY2026 ya eran conocidos en A022: no se atribuye el cambio a resultados trimestrales nuevos. El 10-K del 20 octubre sí aporta evidencia adicional de controles y crédito posterior. El precio de mercado cambia la decisión relativa al valor, no las entradas del DCF para alcanzar una cifra deseada.

## 8. Par homogéneo: MSCI como contraste, no sustituto

Mismo dólar y US GAAP, usando precio regular del 3 noviembre y acciones diluidas del último trimestre como proxy de equity. FDS: FY/TTM agosto; MSCI: TTM septiembre. Diferencia de un mes y mezcla económica declaradas: MSCI tiene índices y royalties ligados a activos, con márgenes mucho mayores; FDS depende más de suscripciones, usuarios y workflows. No se traslada automáticamente la prima de MSCI.

MSCI neto TTM = 1.202,305 + 1.099,0 − 917,6 = 1.383,705 M$. CFO = 1.588,446 + 1.113,7 − 1.087,3 = 1.614,846. Capex físico 39,619 más software capitalizado 120,542 = 160,161. FCF 1.454,685; SBC 126,143; proxy después de SBC 1.328,542. Cifras trimestrales MSCI redondeadas a décima, por lo que los ratios son aproximados. FDS incluye software dentro de su capex 114,720; no se omite en MSCI para favorecer al par.
'''+tab(['Métrica','FDS','MSCI'],[['Precio 3 noviembre','332,59','639,78'],['Acciones proxy, M','35,572','72,3'],['PER GAAP',f"{PE[0]['p_e']:.2f}x",f"{PE[1]['p_e']:.2f}x"],['Precio/FCF',f"{PE[0]['p_fcf']:.2f}x",f"{PE[1]['p_fcf']:.2f}x"],['Precio/(FCF−SBC)',f"{PE[0]['p_owner']:.2f}x",f"{PE[1]['p_owner']:.2f}x"]])+'''
FDS tiene descuento relativo frente a MSCI, no prueba de infravaloración absoluta. Los beneficios y flujos son GAAP/efectivos, no normalizaciones idénticas de impuestos, inversión y otras ganancias. Recompras, deuda, intensidad de índice/licencias y distinta rentabilidad pueden justificar parte de la diferencia. No se usa una media de múltiplos para fijar precio objetivo; el FCFF sigue siendo la referencia propia.
'''+cite('msci_q3','msci_k25','msci_price','q4','price')+'''## 9. Qué confirma o debilita la tesis

Confirmaría recuperación: ASV orgánico dentro de guía, retención estable, margen GAAP recuperándose después de costes recurrentes, caja que no dependa permanentemente de mayores devengos y retorno razonable sobre BCC/LiquidityBook/Irwin. Debilitarían la tesis: pérdida sostenida de clientes, menor valor económico por usuario, inversión en IA sin precios o productividad que la paguen, restructuraciones repetidas y compras que consuman caja sin retorno suficiente.

Catalizador oficial: Investor Day el 10 de noviembre de 2026, 09:00 ET; materiales previstos a las 08:30 ET. No es una publicación de resultados trimestrales.

Próximo paso concreto: conciliar términos BCC, caja/uso del revolver posterior, claims actuales y margen/caja del siguiente trimestre. No se atribuye a una fecha estimada por terceros una confirmación oficial de resultados. Antes de cualquier posible operación, validar próximo anuncio, exclusión semanal, técnica, exposición y riesgo. **Research-grade condicionado; no capital combinado certificado ni Stage 3.5 aprobado.**
'''+cite('k26','bcc','bcc_mirror','investor_day')
pros_es=['Retención de ASV superior a 95% y crecimiento orgánico de ingresos de 6,7% sostienen la calidad de suscripción.','FCF menos SBC crece 12,07% y la debilidad material anterior de controles está remediada según el 10-K.','FDS cotiza a múltiplos GAAP y de caja menores que MSCI, con software incluido en ambos capex.']
cons_es=['Añadiendo solo reestructuración, EBIT queda prácticamente plano; la recuperación de margen aún es una hipótesis de guía.','La caja incluye 62,553 M$ de aportación de remuneración acumulada; no se perpetúa esa financiación.','El central de 238,53 no respalda 332,59; BCC y el uso del revolver posterior impiden certificar capital combinado actual.']
pros_en=['ASV retention above 95% and organic revenue growth of 6.7% support subscription quality.','FCF less SBC grew 12.07%, and the prior material control weakness is remediated according to the 10-K.','FDS trades at lower GAAP earnings and cash multiples than MSCI, including software in both capex figures.']
cons_en=['Adding back only restructuring leaves EBIT roughly flat; margin recovery remains a guidance-based assumption.','Cash flow includes a $62.553m benefit from accrued compensation; that funding is not perpetuated.','The $238.53 central case does not support $332.59; BCC and subsequent revolver uses prevent current combined-capital certification.']
s+='\n## Evidencia exacta para pros y contras\n'
for h,xs in [('A favor',pros_es),('En contra',cons_es),('Pros',pros_en),('Cons',cons_en)]:s+='\n### '+h+'\n\n'+'\n'.join('- '+x for x in xs)+'\n'
(P/'report.md').write_text(s)
meta=dict(ticker='FDS',as_of='2026-11-04',research_cutoff='2026-11-04 16:20 UTC',price=332.59,price_timestamp='2026-11-03 16:00 America/New_York',bear=147.32,base=238.53,bull=402.59,research_status='Independent FCFF reconstruction; research-grade conditional on BCC/post-August capital',decision_es='Esperar precio o evidencia. Base 238,53 con capital agosto; BCC/uso revolver pendientes. Sin entrada.',decision_en='Wait for price or evidence. Base238.53 with August capital; BCC/revolver uses unresolved. No entry.',buy_ceiling=None,approved_entry=False,stage35_approved=False,pros_es=pros_es,cons_es=cons_es,pros_en=pros_en,cons_en=cons_en,pros_cons_evidence={'pros':['Section1; k26/q4','Section3/1; k26','Section8; peers.json'],'cons':['Section3; q4','Section3; k26','Section4/6; model.json,k26,bcc']},publication_note='Preserve A022198/248/295 as historical exploratory numbers. Original A022 code unavailable; never label exact reproduction. Central uses August capital and annual model convention; combined BCC not certified. No15% universal rule, no Stage3.5 approval.')
json.dump(meta,open(P/'publication.json','w'),indent=2,ensure_ascii=False);print(len(s))
