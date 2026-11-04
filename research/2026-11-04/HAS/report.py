from pathlib import Path
import json,subprocess
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));peers=json.load(open(P/'peers.json'))
def num(x):return f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
def table(rows):
 out='| Periodo | Ventas | EBIT GAAP | Beneficio atribuible | EPS diluido | CFO | PPE + software | SBC | FCF menos SBC |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
 for r in rows:out+='| '+r['period']+' | '+' | '.join(num(r[k]) if k in r and r[k] is not None else '—' for k in ['revenue','operating_income','net_income','eps','cfo','capex','sbc','owner_cash_proxy'])+' |\n'
 return out
pros_es=['La mejora operativa persiste sin el beneficio arancelario: el EBIT TTM conservador alcanza 1.283,1 M$, frente a 820,3 M$ comparables.','Magic aporta crecimiento y una base de aficionados; Wizards registra 1.993,0 M$ de ventas en nueve meses, un 28,0 % más.','La caja y los bonos del Tesoro suman 1.426,9 M$; los vencimientos de 2026 están prefinanciados parcialmente.']
cons_es=[f'El central FCFF de {num(m["cases"]["base"]["value"])} USD no respalda el cierre de 117,97 USD; el favorable no es un techo garantizado.','El desarrollo de videojuegos mantiene 406,0 M$ capitalizados después de un deterioro de 56,4 M$; la rentabilidad futura aún debe demostrarse.','La devolución arancelaria, la fiscalidad, la concentración en Magic y el desfase de comparables impiden extrapolar toda la caja reciente.']
pros_en=['Operating improvement persists without the tariff benefit: conservative TTM EBIT is $1,283.1m versus a comparable $820.3m.','Magic provides growth and an established fan base; Wizards generated $1,993.0m of nine-month revenue, up 28.0%.','Cash and Treasury securities total $1,426.9m; 2026 maturities are partly prefunded.']
cons_en=[f'The ${m["cases"]["base"]["value"]:.2f} central FCFF case does not support the $117.97 close; the favorable case is not a guaranteed ceiling.','Capitalized game development remains $406.0m after a $56.4m impairment; future returns still need to be demonstrated.','Tariff refunds, tax effects, Magic concentration and mismatched peer periods prevent extrapolating all recent cash generation.']
s=f'''# HAS: crecimiento real, caja que exige normalización y reconstrucción FCFF

Fecha de investigación: 4 de noviembre de 2026. Referencia de valoración: cierre del 3 de noviembre, 117,97 USD. No se usa la cotización intradía. Escáner conservado: registro de la sesión del 15 de octubre, con referencia 95,46 USD que coincide con el cierre del 14 de octubre según el histórico. No es el cierre del 15 de octubre (98,41 USD). A057 del 19 de octubre contenía seguimiento técnico con referencia 98,76 USD, no una nueva valoración. Las fechas y precios no son intercambiables.

## 1. Conclusión y alcance

La mejora de Hasbro no se explica solo por un deterioro contable en la comparación: Wizards sigue creciendo y Consumer Products mejora. Sin embargo, el precio ha cambiado sustancialmente desde A026. La generación de caja reciente contiene devoluciones arancelarias, diferencias fiscales y un perfil de inversión en videojuegos que todavía no ha producido todos sus ingresos.

Esta es una reconstrucción nueva desde fuentes primarias, con FCFF de diez años y capital financiado. No es una réplica del archivo ejecutable de A026, que no se ha recuperado. La reconstrucción de sus hipótesis divulgadas sí reproduce los valores redondeados históricos. Investigación condicionada: no hay entrada ni aprobación de Stage 3.5, no se modifica gestión, cantidad, stops u operaciones. La próxima fecha de resultados de HAS no está confirmada con fuente primaria al corte. El panel de pares también conserva un desfase importante en MAT.

Valores por acción: conservador {num(m['cases']['bear']['value'])}, central {num(m['cases']['base']['value'])}, favorable {num(m['cases']['bull']['value'])} USD. No son órdenes, probabilidades ni precios máximos autorizados. La diferencia del central con el precio es una consecuencia de supuestos explícitos, no un descuento adicional fijo del 15 %.

## 2. Historia conciliada: tres ejercicios, cuatro trimestres y TTM

Millones de USD excepto EPS. FCF = CFO menos PPE y software capitalizado; el coste de producción de entretenimiento ya está en CFO y no se resta dos veces. FCF menos SBC es un indicador de control, no FCFF ni dividendo distribuible. Q4 se obtiene por diferencia de importes anuales y nueve meses; el EPS Q4 de 1,41 procede directamente del comunicado, no de restar EPS anuales. La suma de EPS de los cuatro trimestres es un dato distinto de dividir beneficio anual por acciones actuales.

{table(f['annual'])}
{table(f['quarters'])}
{table(f['ttm'])}

FY2023 tuvo 53 semanas e incluía eOne Film & TV hasta su venta de diciembre; FY2024 y FY2025 tuvieron 52 semanas. No se presentan como un perímetro orgánico constante. Los ejercicios contienen deterioros de goodwill, pérdidas de venta y variaciones fiscales que invalidan una tasa de crecimiento mecánica del beneficio publicado. El TTM nuevo se calcula como FY2025 + 9M2026 − 9M2025; el anterior como FY2024 + 9M2025 − 9M2024. Los scripts conservan los importes de origen y prueban la suma de los cuatro trimestres.

Fuentes: [10-K 2025](https://www.sec.gov/Archives/edgar/data/46080/000004608026000011/has-20251228.htm), [10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/46080/000004608026000065/has-20260927.htm), [Q3 2025](https://www.sec.gov/Archives/edgar/data/46080/000004608025000164/has-20250928.htm), [Q2 2026](https://www.sec.gov/Archives/edgar/data/46080/000004608026000050/has-20260628.htm), [Q1 2026](https://www.sec.gov/Archives/edgar/data/46080/000004608026000026/has-20260329.htm), [Q4 2025](https://www.sec.gov/Archives/edgar/data/46080/000004608026000006/exhibit991q42025.htm).

## 3. Calidad del beneficio y de la caja

El EBIT TTM de 1.337,6 M$ contiene 54,5 M$ de recuperación de aranceles; sin ella queda 1.283,1 M$, margen 24,77 %. El TTM anterior de −226,6 M$ pasa a 820,3 M$ al retirar el deterioro de goodwill de 1.021,9 M$ y la pérdida final de eOne de 25,0 M$. El aumento comparable es 56,42 %. No se vuelve a añadir goodwill al TTM actual, del que ya salió. SBC, amortización ordinaria, reestructuración y deterioro de videojuegos se conservan como costes en esta comparación conservadora.

En Q3, 517,3 M$ de EBIT menos 54,5 M$ de aranceles son 462,8 M$, frente a 341,1 M$: crecimiento del 35,68 %. El coste económico de los videojuegos no desaparece porque una baja de activos no sea un pago del trimestre. Los 56,4 M$ deteriorados corresponden a cancelaciones de títulos previstos para 2028 y después. Se conserva esa pérdida en el punto de partida; tampoco se resta otra vez como salida de caja futura. El saldo capitalizado de software es 406,0 M$, frente a 385,6 M$ en diciembre. Nuevos lanzamientos pueden elevar amortización y gasto comercial: un margen futuro mayor no está garantizado.

Los cobros arancelarios fueron 43,4 M$: principal 41,5 e intereses 1,9. De la recuperación contable de 54,5 quedan 13,0 M$ por cobrar (2,7 de fase 2 y 10,3 de fase 3). No se incorpora esa cuenta por cobrar como caja actual adicional. Los 1,9 de intereses están fuera de EBIT y no se retiran de él. El cobro restante depende de trámites y litigios; el plazo de seis meses es expectativa del emisor, no resolución administrativa certificada por este análisis.

El FCF TTM menos SBC de 1.018,5 M$ baja a 975,1 M$ si se retiran los 43,4 cobrados, antes de conciliar sus impuestos. Esa cifra no se perpetúa. En nueve meses CFO sube 417,3 M$; 43,4 corresponden a ese cobro y 57,4 a que el año anterior tuvo un pago de repatriación no repetido. Además, impuestos pagados son 82,5 frente a 175,6 M$, mientras el gasto fiscal de 2026 asciende a 186,1 M$. El puente de caja no convierte diferencias temporales fiscales en crecimiento permanente.

El beneficio fiscal discreto de nueve meses fue 26,6 M$; en Q3 fueron 16,8 M$, ligados principalmente al cierre de una auditoría IRS. Se usa un impuesto normalizado del 24 % en el central, no la tasa efectiva publicada de 19,8 %. No se resta SBC dos veces: se conserva en margen EBIT futuro, y la resta explícita de SBC solo pertenece al indicador histórico de caja.

El incidente de red de marzo costó 11,8 M$ en nueve meses, 1,0 M$ en Q3; no se habían reconocido recuperaciones de seguro. La dirección indica que los procesos normales se habían restaurado y operaron todo Q3. El gasto queda conservado, sin inventar un cobro de seguro. Las reestructuraciones son recurrentes en la historia y tampoco se eliminan de forma automática.

## 4. Negocio, ventajas y riesgos

Wizards facturó 1.993,0 M$ en nueve meses frente a 1.556,5; su beneficio operativo de 935,1 M$ concentra alrededor del 86 % del resultado de segmentos antes de costes corporativos. Incluye 6,6 M$ de devolución arancelaria y soporta el deterioro de videojuegos. Consumer Products facturó 1.688,8 M$ frente a 1.637,6, con EBIT de 111,8 M$ que incluye 47,9 de devolución. Sin esa devolución son 63,9 M$; la comparación de 2025, retirando solo goodwill, es 28,5 M$. No equivale a una recuperación homogénea en todas las marcas y geografías.

Magic superó 600 M$ trimestrales según la dirección, con ventas +34 %. Aproximadamente 40 M$ de ventas previstas para Q4 se adelantaron a Q3; este desfase debe retirarse de la expectativa de Q4, no sumarse de nuevo. No se transforma el crecimiento trimestral en una tasa anual sostenible. La combinación de juego, coleccionismo, tiendas y propiedad intelectual favorece recurrencia y precio; no demuestra demanda ilimitada. El ritmo de lanzamientos y colaboraciones puede saturar al cliente, elevar regalías y crear dependencia de éxitos. Los ingresos de licencias consolidados de Q3 fueron 144,3 M$, inferiores a los 152,6 previos: el crecimiento de Magic no debe confundirse con crecimiento de toda licencia. La mayor parte del crecimiento operativo proviene de Wizards. El 27 de octubre se anunció el nombramiento de Dan Ayoub al frente de Wizards, efectivo el 2 de noviembre; es un cambio de ejecución que debe seguirse, no prueba de que los próximos juegos cumplirán. [Anuncio oficial](https://investor.hasbro.com/news-releases/news-release-details/hasbro-names-dan-ayoub-president-wizards-coast-hasbro-digital).

La dirección elevó su guía anual a ventas +7–9 % en moneda constante y margen operativo ajustado 27–28 %. Son medidas prospectivas y ajustadas, distintas del margen GAAP sin devolución usado aquí. El modelo no trata el 28 % como un hecho ganado. Los lanzamientos de videojuegos de 2027 y la producción de nuevos sets son catalizadores y riesgos de ejecución; su contribución no está aislada en una valoración por producto. La dirección señaló específicamente que Wizards podría pasar de margen 44–45 % previsto para 2026 al tramo alto del 30 % en 2027, por amortización de Exodus y Warlock. No es una guía consolidada de 2027. El modelo conserva margen inicial inferior al TTM, pero no dispone de una proyección por título que pruebe su suficiencia. Q4 también lleva unos 15 M$ adicionales de marketing para los juegos. El objetivo de recompras se elevó a 400 M$; no se descuentan futuras recompras y a la vez se mantiene su caja como si no se pagasen.

Se mantienen litigios sobre declaraciones históricas de Magic y acciones derivadas. El emisor no puede estimar un intervalo de pérdida. No se presume culpabilidad, ni se asigna pérdida cero porque falte estimación. La obligación ambiental identificada de 30 M$ proviene principalmente de una instalación heredada de una adquisición histórica; es una obligación existente revisada, no una nueva adquisición de este trimestre.

Fuentes: [resultados Q3](https://investor.hasbro.com/news-releases/news-release-details/hasbro-reports-third-quarter-2026-financial-results), [comentarios preparados de dirección](https://investor.hasbro.com/static-files/ffa2f41b-ceec-4112-ae29-af274c452d63), y notas 1, 2, 14, 15, 16 y litigios de la 10-Q.

## 5. Puente empresa a accionista

| Concepto | M$ | Tratamiento |
|---|---:|---|
| Efectivo | 850,7 | Saldo de septiembre |
| Bonos del Tesoro a corto plazo | 576,2 | Saldo líquido; parte prefinancia deuda |
| Reserva operativa propia | −350,0 | Hipótesis, no efectivo legalmente restringido |
| Deuda nominal | −3.527,8 | No el saldo neto de costes de emisión de 3.510,3 |
| Intereses minoritarios | −24,6 | Valor contable como aproximación |
| Pensiones y prestaciones | −52,6 | Proxy de déficit FY2025, no medición actuarial de septiembre |
| Reserva fiscal histórica | −52,1 | Proxy conservador FY2025, no pasivo actual certificado |
| Obligación ambiental histórica | −30,0 | Remediación identificada en Q3 |
| Puente neto | {num(m['capital_bridge']['net'])} | Restado una sola vez al valor empresa |

La reserva de pensiones suma 27,9 de pensión estadounidense, 19,4 de prestaciones y 5,3 de déficit internacional (79,2 menos 73,9). No agrega los activos de pensiones a caja corporativa. No se dispone de una actualización actuarial trimestral completa. El gasto de los planes definidos se informa fuera de EBIT en la historia, evitando añadirlo otra vez al margen operativo; permanecen posibles diferencias de servicio normalizado internacional y medición.

La reserva fiscal suma 37,7 de beneficios no reconocidos, 9,1 de intereses/penalizaciones y 5,3 de repatriación del cierre FY2025. Es deliberadamente un proxy prudente: el acuerdo IRS y beneficios fiscales de 2026 pueden haber reducido esa exposición. No se puede restar automáticamente el beneficio discreto de 16,8 al pasivo sin una conciliación. Las cuentas fiscales del cierre anterior incluyen posiciones en activos, de modo que tampoco se afirma que toda esa suma sea una obligación exigible de septiembre. Suprimir por completo esta reserva elevaría el central solo a {num(m['capital_sensitivity']['remove_prior_tax_proxy'])} USD. Suprimir toda la reserva de prestaciones lo elevaría a {num(m['capital_sensitivity']['remove_prior_pension_proxy'])}.

Los 497,0 M$ con vencimiento en noviembre de 2026 y 396,9 M$ en septiembre de 2027 ya están incluidos en deuda nominal. Los fondos obtenidos para prefinanciarlos están en bonos del Tesoro. No se restan los vencimientos por segunda vez y no se suma el efectivo una segunda vez al amortizar deuda. No se ha confirmado que la amortización de noviembre ya haya ocurrido al corte.

El arrendamiento operativo de 339,6 M$ no se capitaliza de nuevo como deuda en este modelo con rentas conservadas como coste operativo. Las altas de derecho de uso de 227,5 M$ no son capex de caja; explican buena parte del cambio en activos, no un pago omitido. Los 118,8 M$ de financiación de proveedores están en cuentas a pagar y CFO: no se duplican como deuda, pero su crecimiento puede ayudar temporalmente a caja. La deuda revolvente no estaba dispuesta; la capacidad disponible no es efectivo. Impuestos operativos, regalías y reestructuraciones ordinarias siguen en circulante/costes y no se restan indiscriminadamente de nuevo.

Se usan 142,5 millones de acciones diluidas Q3. Es un promedio, no una garantía contra dilución futura: 0,2 millones de premios antidilutivos quedan excluidos y no se suman íntegros sin considerar sus condiciones. Las recompras previstas no se cuentan a la vez como caja conservada y menor denominador.

## 6. Modelo: ventas, margen, impuestos y reinversión

Modelo nominal USD, diez años: cinco explícitos y cinco de transición, más perpetuidad financiada. Punto de partida: ventas TTM de 5.181,0 M$. El primer año representa los siguientes doce meses hipotéticos, no una predicción exacta del calendario FY2027.

Central: crecimiento 8 / 7 / 6 / 5 / 4 % los primeros cinco años, después convergencia a 2,5 % en el año diez. Margen EBIT 23 / 24 / 25 / 25,5 / 26 %, después 26 %. El primer año baja frente al 24,77 % TTM sin devolución para reconocer el inicio de amortización de videojuegos y un mix de Wizards menos favorable. La recuperación posterior sigue siendo una hipótesis propia, no guía de 2027. Impuesto 24 %. D&A 2,9 % de ventas; inversión de caja agregada en PPE, software y producción 4,0 %; incremento de circulante 10 % del aumento de ventas. La inversión incluye producción futura, mientras la reconstrucción histórica no duplica su gasto en CFO.

La reinversión aplicada es el máximo entre capex menos D&A más incremento de circulante, y NOPAT × crecimiento de ventas / 20 %. La reserva adicional aparece en cada fila, y FCFF = NOPAT + D&A − capex − incremento de circulante − reserva adicional. El 20 % es una hipótesis de rendimiento económico de financiación, no un ROIC incremental contable demostrado. La mejora de margen se supone sobre la capacidad financiada; no se confunde crecimiento de ventas con crecimiento de NOPAT. Hay sensibilidad a este supuesto. La misma regla se mantiene en terminal, sin regalar crecimiento ni cambiar bruscamente de método al finalizar el año diez.

Año uno central: ventas {num(m["cases"]["base"]["rows"][0]["revenue"])}; NOPAT {num(m["cases"]["base"]["rows"][0]["nopat"])}; D&A {num(m["cases"]["base"]["rows"][0]["da"])}; inversión {num(m["cases"]["base"]["rows"][0]["capex"])}; incremento de circulante {num(m["cases"]["base"]["rows"][0]["delta_nwc"])}; reserva adicional {num(m["cases"]["base"]["rows"][0]["additional_reinvestment_reserve"])}; FCFF {num(m["cases"]["base"]["rows"][0]["fcff"])} M$. Por eso el indicador histórico de 1.018,5 M$ después de SBC no es el flujo proyectado. No se vuelve a añadir SBC en ninguna proyección. El crecimiento de videojuegos debe financiarse aunque su coste se capitalice contablemente.

Tasa central 10 %. Referencia libre de riesgo: Treasury a diez años 4,91 % del 2 de noviembre, publicación H.15. Una ilustración con beta supuesta 1,30, prima 4,5 %, peso de deuda 15 % y coste de deuda prospectivo 6 % da aproximadamente 9,83 % después del escudo al 24 %; se redondea a 10 % por incertidumbre de mezcla, ejecución y capital. Beta, prima y pesos son supuestos, no estimaciones empíricas certificadas. No se usa el cupón histórico como coste marginal universal. [H.15](https://www.federalreserve.gov/releases/h15/).

Conservador: crecimiento inicial cuatro puntos menor, margen cuatro puntos menor durante diez años y terminal, WACC 11 %, g 1,5 %, rendimiento de reinversión 15 % e impuesto 26 %. Favorable: crecimiento inicial cuatro puntos mayor, margen 3,5 puntos mayor durante diez años y terminal, WACC 9 %, g 3 %, rendimiento 25 % e impuesto 23 %. Los años seis a diez convergen al g de cada escenario. No son desviaciones estadísticas ni escenarios equiprobables.

| Caso | Valor USD | Peso del terminal en EV |
|---|---:|---:|
'''
for k,label in [('bear','Conservador'),('base','Central'),('bull','Favorable')]:s+=f'| {label} | {num(m["cases"][k]["value"])} | {num(m["cases"][k]["terminal_weight"]*100)} % |\n'
s+='\nSensibilidad central a WACC y crecimiento perpetuo:\n\n| WACC | g | Valor USD |\n|---:|---:|---:|\n'
for r in m['sensitivity']:s+=f'| {num(r["wacc"]*100)} % | {num(r["g"]*100)} % | {num(r["value"])} |\n'
s+='\nSensibilidad al rendimiento económico de reinversión:\n\n| Rendimiento | Valor USD |\n|---:|---:|\n'
for r in m['roic_sensitivity']:s+=f'| {num(r["roic"]*100)} % | {num(r["value"])} |\n'
s+=f'''
Con un 3 % más de acciones, central {num(m['dilution_sensitivity'])} USD. Reservar 250 / 450 M$ de caja, en lugar de 350, da {num(m['capital_sensitivity']['cash_reserve250'])} / {num(m['capital_sensitivity']['cash_reserve450'])} USD. Son sensibilidades aisladas, no certezas de acceso a efectivo. Retirar 40 M$ de ventas del punto de partida como sensibilidad al adelanto de envíos da {num(m["pullforward_sensitivity"])} USD, sin afirmar que ese sea el ajuste correcto de todos los periodos. Un coste adicional de 80 M$ anual escalado con ventas, aproximado por menor margen en todos los años, reduce el central a {num(m["amortization_sensitivity"])} USD; es un estrés de rentabilidad, no una previsión de amortización publicada.

## 7. Inversa y puente con A026

Para alcanzar 117,97 USD manteniendo el resto del central, la inversa de margen requiere {num(m['reverse']['margin_extra_all_years']*100)} puntos porcentuales adicionales en todos los diez años y terminal. No es el margen implícito de un solo trimestre. En el intervalo comprobado se encuentra una raíz de crecimiento de {num(m["reverse"]["growth_roots"][0]*100)} puntos adicionales en cada uno de los cinco primeros años, manteniendo la posterior convergencia. Es una exigencia alta sobre una base que ya creció, no una previsión. La inversa de crecimiento se barre explícitamente entre 0 y 40 puntos adicionales en los cinco primeros años; se conservan las reinversiones exigidas, por lo que no se presupone monotonicidad fuera de los intervalos comprobados. El soporte contiene todos los puntos y los intervalos con cambio de signo, no una raíz forzada. Directa e inversa comparten hipótesis y no son pruebas independientes.

A026 usaba FCFE simplificado de cinco años: caja inicial 800 / 900 / 1.000 M$, crecimiento 3 / 7 / 10 %, descuento 10 %, perpetuidad 2,5 % y 143,2 millones de acciones. Su reconstrucción arroja {num(m['historical_A026']['cases']['bear']['value'])} / {num(m['historical_A026']['cases']['base']['value'])} / {num(m['historical_A026']['cases']['bull']['value'])}, coherente con 78 / 104 / 130 históricos. No se le resta deuda retroactivamente: su caja era para accionistas. La nueva valoración FCFF reconstruye operaciones, financiación del crecimiento y puente de capital, con cifras Q3 nuevas. El cambio no puede atribuirse solo a deterioro del negocio ni presentarse como réplica exacta del archivo antiguo.

## 8. Comparables y calendario

El panel se ha calculado con el mismo cierre de precios y fórmulas de TTM, pero no con el mismo cierre contable. EV de comparación = precio × acciones diluidas medias del último trimestre + deuda nominal − efectivo e inversiones líquidas; no aplica la reserva operativa del DCF. Es una aproximación, no capitalización exacta. Se conserva SBC y amortización en EBIT.

| Empresa | Cierre TTM | EV/EBIT GAAP | CFO menos capex y SBC / equity |
|---|---|---:|---:|
| HAS | septiembre 2026 | 14,14x | 6,06 % |
| MAT | junio 2026 | 14,55x | 8,16 % |
| JAKK | septiembre 2026 | 14,64x | 6,25 % |

HAS sin los 54,5 M$ arancelarios da EV/EBIT de 14,74x; el rendimiento de caja, retirando el cobro bruto de 43,4 M$, es 5,80 %, antes de conciliar impuestos. No hay una prima obvia por múltiplo simple, pero los riesgos y horizontes distintos impiden concluir que el precio sea barato. JAKK reconoce 6,801 M$ de devolución en Other income, fuera de EBIT; no se restan de EBIT. Cobró 11,1 M$ con intereses y parte de la devolución afecta inventario: el posterior paso a coste de ventas no está aislado. Retirar todo ese cobro bruto baja el rendimiento de caja a 3,34 %, como sensibilidad, no normalización fiscal exacta. MAT excluye premios antidilutivos por la pérdida Q2, de modo que su denominador no es dilución futura plena.

Fuentes: [MAT 10-Q](https://www.sec.gov/Archives/edgar/data/63276/000162828026054347/mat-20260630.htm), [fecha MAT](https://investors.mattel.com/news/news-details/2026/Mattel-Announces-Third-Quarter-2026-Financial-Results-and-Conference-Call-Date/default.aspx), [JAKK 10-Q](https://www.sec.gov/Archives/edgar/data/1009829/000143774926033558/jakk20260930_10q.htm). El soporte contiene puente FY + YTD − YTD anterior y fuentes de precios 15,29 / 31,65 para MAT / JAKK.

 Mattel tiene anunciado Q3 para el 5 de noviembre a las 16:05 ET: antes de ese evento solo puede usarse su TTM de junio, claramente fechado, sin inventar nueve meses de septiembre. JAKKS ya publicó Q3. La exposición a juguetes físicos, propiedad intelectual ajena y estacionalidad difiere de Magic; una diferencia de múltiplos no demuestra por sí sola una prima injustificada. No se deriva un objetivo automático de la media de pares.

HAS ya presentó Q3 el 20 de octubre y 10-Q el 29 de octubre. Es incorrecto mantener ese resultado como un catalizador futuro. La página oficial revisada no confirma el próximo anuncio anual; estimaciones de agregadores no liberan el filtro. La actualización de pares tras Mattel, los nuevos sets, la ejecución de videojuegos, capital fiscal actualizado y el cobro arancelario son las siguientes evidencias útiles. [Calendario HAS](https://investor.hasbro.com/events). El dividendo previsto de 0,70 USD se paga el 2 de diciembre a titulares del 18 de noviembre; no cambia la valoración por sí solo.

## 9. Qué apoyaría o invalidaría la tesis

A favor: crecimiento de Magic que no dependa exclusivamente de adelantar envíos, recuperación de juguetes sin devoluciones extraordinarias, y software que convierta inversión en rentabilidad después de amortización. En contra: caída persistente de demanda por exceso de lanzamientos, margen de Consumer Products que no se sostenga sin reembolsos, más bajas de juegos capitalizados, o caja sostenida por proveedores y menor pago de impuestos. No se atribuye una caída histórica a una causa única no demostrada; actualmente el precio está por encima de las referencias antiguas de selección.

Faltan para certificar integralmente: puente fiscal y actuarial actualizado, comparable MAT después de resultados, próxima fecha HAS confirmada y cierre de incertidumbres regulatorias/materiales. Ninguna de estas reservas se transforma en un valor cero ni en una orden. Auditoría independiente completada: liberado únicamente como investigación condicionada, sin certificación integral ni entrada.

## 10. Evidencia breve ES / EN

'''
for label,key in [('A favor','pros_es'),('En contra','cons_es'),('Pros','pros_en'),('Cons','cons_en')]:
 s+=f'### {label}\n\n'+'\n'.join('- '+x for x in locals()[key])+'\n\n'
(P/'report.md').write_text(s)
meta=dict(ticker='HAS',as_of='2026-11-04',research_cutoff='2026-11-04 17:38 UTC',price=117.97,price_timestamp='2026-11-03 16:00 America/New_York',base=round(m['cases']['base']['value'],2),bear=round(m['cases']['bear']['value'],2),bull=round(m['cases']['bull']['value'],2),research_status='New FCFF reconstruction; capital, peers and calendar qualified. Independently audited for conditional research only.',decision_es='Esperar precio o evidencia; investigación condicionada, sin entrada.',decision_en='Wait for price or evidence; conditional research, no entry.',approved_entry=False,stage35_approved=False,buy_ceiling=None,pros_es=pros_es,cons_es=cons_es,pros_en=pros_en,cons_en=cons_en,publication_note='Preserve A026 historical FCFE and A057 technical follow-up. Scanner session Oct15 carries 95.46, matching Oct14 close; not Oct15 close 98.41. Nov3 close 117.97 is separate. No portfolio/operations changes, no next earnings date invented, no integral certification.')
json.dump(meta,open(P/'publication.json','w'),indent=2,ensure_ascii=False)
subprocess.run(['pandoc',str(P/'report.md'),'-s','-o',str(P/'report.html'),'--metadata','title=HAS — 4 noviembre 2026'],check=True)
