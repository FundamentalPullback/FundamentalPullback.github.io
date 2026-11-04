import json,pathlib,html
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());h={r['period']:r for r in json.loads((P/'history/shop_financial_history.json').read_text())['records']}
t='''# SHOP: la caja del crecimiento, después de financiar a los comercios

Corte: 4 noviembre 2026, 19:31 UTC. Investigación y valoración FCFF condicionadas, con auditoría independiente cerrada el 4 noviembre a las 19:37 UTC exclusivamente para este alcance condicionado. USD, acción estadounidense, no cotización canadiense. Referencia: cierre 3 noviembre, 142,57 USD, posterior al resultado de esa mañana. Se preservan A123/A128 y la observación real del escáner 2 noviembre, 156,70 USD (QP 80, Opportunity 95); no se transforma esa observación en un cierre certificado ni se reescribe su fecha.

## Dictamen

La mejora operativa es real, pero el FCF anunciado sobrestima el efectivo remanente después de financiar el negocio de crédito y otros desembolsos de inversión. Un FCFF explícito condicionado, con SBC retenido, financiación de crecimiento y expansión de margen y un puente prudente, produce escenarios muy inferiores al precio de referencia. Eso no certifica valor integral ni habilita entrada: pares homogéneos, realizabilidad de inversiones, fiscalidad y calendario permanecen abiertos. No se modifica cartera, gestión ni operaciones; no latestCompleted ni Stage 3.5.

Los ingresos TTM aumentan de 10.696 a 14.167 millones USD y el EBIT GAAP de 1.302 a 2.069 millones, sin sumar SBC al beneficio operativo.

El FCF Q3 anunciado de 816 millones USD se reduce a 587 después de financiación neta de préstamos, a 488 tras intangibles y a 348 al restar SBC como sensibilidad económica.

## Historia verificable

Tres ejercicios, últimos cuatro trimestres y TTM, en millones USD. CFO es el publicado bajo la presentación de cada fecha; se ofrece después una conciliación comparable. NI conserva inversiones no operativas y efectos fiscales, no se confunde con EBIT normalizado.

| Periodo | Ingresos | EBIT | NI | CFO | PPE caja | SBC | Caja tras PPE, financiación, intangibles y SBC |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for k,r in h.items():
 if r['kind']=='FY' or k in ['2025Q4','2026Q1','2026Q2','2026Q3'] or 'TTM' in k:
  t+='| '+k+' | '+' | '.join(f'{r[x]:,.0f}' for x in ['revenue','gaap_ebit','gaap_net_income','cfo','ppe_cash_spend','sbc','cash_after_ppe_lending_intangibles_sbc'])+' |\n'
t+='''
El soporte conserva ocho trimestres y EPS directo, incluido Q4. La suma de EPS trimestrales TTM es 1,64 frente a 1,35, no un EPS GAAP TTM con denominador certificado. Q4 aditivo de cashflow se deriva de anual menos nueve meses, no se restan EPS. FY2023 incluye deterioro de 1.340 millones por la salida de logística; no se finge comparabilidad orgánica eliminándolo selectivamente. La venta de logística y el negocio actual requieren distinguir historia y perímetro.

## La diferencia entre FCF y financiación real

CFO TTM 2.682 menos PPE 21 = 2.661 millones. El comparativo es 1.903. Desde abril de 2026, los anticipos a comerciantes pasan de operación a inversión, coincidiendo con el cambio regulatorio canadiense y la transición del producto a préstamos. Los efectos identificados son 37 en Q2 y 30 en Q3: 67 en el TTM actual. Bajo la presentación anterior, el indicador actual sería 2.594, no 2.661. Los comparables de 2025 no fueron reformulados: 513 CFO Q3 y 1.308 nueve meses coinciden con el filing original. No se estableció una explicación adicional para esa ausencia de reformulación.

Para atravesar ambas presentaciones se calcula CFO menos PPE y menos financiación neta que esté en inversión. Antes de abril, los anticipos ya estaban en CFO; no se restan de nuevo. La financiación neta de inversión TTM es 789 frente a 594: quedan 1.872 frente a 1.309. Tras 99 de intangibles quedan 1.773 frente a 1.309; tras SBC 515/443, 1.258 frente a 866. El último ajuste es una sensibilidad económica, no otra salida de caja ni owner earnings certificado.

Q3: CFO 818 − PPE 2 = 816. Compras/originaciones 1.700 menos cobros/ventas 1.471 consumen 229: quedan 587. La compra de intangibles 99 lleva a 488 y SBC 140 a 348. Restar también los 30 de reclasificación después de los 229 sería doble cómputo. No se ha identificado finalidad, vida útil o parte de mantenimiento de los 99: se muestran aparte, sin llamarlos gratuitos ni íntegramente mantenimiento.

Los préstamos y anticipos netos crecen a 2.350 millones USD frente a 1.784 en diciembre; el crecimiento comercial exige capital adicional y riesgo de crédito.

El bruto es 2.596 (2.226 préstamos y 370 anticipos), menos provisión 246. Nueve meses: provisión específica de crédito 217, bajas netas 166; Q3 provisión 63 y bajas 59. Esas cifras no son la misma medida que los 120 de pérdidas de transacciones/préstamos en resultados Q3 ni los 67 de provisión ajustada en el cashflow. No se sustituyen unas por otras. Ingresos por intereses/comisiones de préstamos 96 Q3 y 271 nueve meses; no todo el crecimiento de Merchant Solutions es un ingreso sin financiación.

## Beneficio, negocio y riesgos

Q3 ingresos 3.742, beneficio bruto 1.781, EBIT 568 y NI 462. Otros gastos netos −69 incluyen intereses ganados 65, ganancia realizada 10, pérdida no realizada −127, pérdida Flexport −21 y divisas +4. Están fuera del EBIT: no se vuelven a deducir al proyectar beneficio operativo. El impuesto 37 sobre beneficio antes de impuestos 499 está favorecido por liberar 63 de provisión de valoración de activos fiscales. No se perpetúa la tasa efectiva del 7,4 %.

Subscription Solutions Q3 836 y Merchant Solutions 2.906: la mezcla favorece volumen de pagos y servicios, con márgenes distintos. GMV 119.145 millones, MRR 230 millones; no se equiparan GMV, MRR e ingresos. El producto integrado, checkout, pagos, canales y ecosistema de aplicaciones crean fricción de cambio y distribución. Compite con marketplaces, otras herramientas SaaS, soluciones empresariales y canales AI; no basta el crecimiento para demostrar poder de precio estable.

La guía Q4 apunta a crecimiento de ingresos en la parte baja de los treinta por ciento y beneficio bruto en la parte alta de los veinte; son expectativas de dirección, no crecimiento terminal. Los costes de hosting, software y uso de modelos AI aumentan; tampoco se supone que la productividad AI reduzca gastos sin coste. Founder Share y acciones de voto restringen el control económico ordinario: el modelo no atribuye al accionista minoritario capacidad de extraer toda la cartera estratégica.

## Modelo FCFF condicionado: financiación antes de valoración

Método principal FCFF, horizonte 10 años (cinco iniciales y cinco de maduración), terminal perpetuo con crecimiento financiado. No se usa CFO−PPE como FCFF inicial. Ancla TTM ingresos 14.167 y EBIT GAAP 2.069, margen 14,60 %. SBC permanece en los márgenes; no se añade al EBIT ni al FCFF.

Se resta del EBIT proyectado una conversión no monetaria equivalente a 38/10.495 de ingresos (0,3621 %), basada en contraprestación estratégica no monetaria de nueve meses. Es supuesto prudente, no promesa de que su ritmo sea constante. Los impuestos normalizados son 25 % en los tres casos, estimación explícita distinta de tasas trimestrales extraordinarias.

Reinversión explícita anual = máximo entre:

1. Suelo físico/financiero: capex 0,8 % de ventas − D&A 0,3 % + 5 % del incremento de ventas en capital de trabajo no crediticio + incremento del libro neto de préstamos manteniendo su ratio inicial 2.350/14.167 (16,59 %).
2. Incremento de NOPAT dividido por retorno incremental supuesto (15/20/25 % según escenario), con suelo cero. Se financia la mejora de margen además del crecimiento de ventas, no solo NOPAT × crecimiento de ingresos.

Estos ratios son hipótesis del analista, no ROIC demostrado, desglose de mantenimiento ni guidance. El capex de 0,8 % incorpora reinversión intangible estimada, no solo los 21 de PPE históricos; no capitaliza gratis desarrollo/adquisiciones. Las pérdidas esperadas de crédito se mantienen en el margen operativo, y se financia el crecimiento del activo neto; no se añade todo el libro al puente patrimonial. FCFF = NOPAT + D&A − capex − ΔNWC − Δpréstamos netos − reserva adicional hasta alcanzar el mayor suelo. Cada campo está en model.json.

En terminal se repite máximo entre suelo físico/financiero y NOPAT terminal × g / retorno incremental. No se relaja el suelo al acabar el año diez. El criterio económico domina los casos base actuales; duplicar el ratio de préstamos, subir capex a 1,5 % o NWC a 10 % no cambia el central mientras no superen ese suelo. No significa que tales inversiones sean irrelevantes: ya están financiadas por la reserva más exigente.

Los primeros tres FCFF centrales son negativos por financiar crecimiento y expansión de margen; no se eliminan ni se difieren para mejorar la valoración. Arrendamientos siguen como coste operativo en EBIT y no se resta además su pasivo como deuda: es una convención de rentas operativas, no un ajuste IFRS16 simulado.

| Supuesto | Bajista | Central | Favorable |
|---|---|---|---|
| Crecimientos años 1–5 | 18/15/12/10/8 % | 28/24/20/17/15 % | 35/30/26/23/20 % |
| Crecimientos años 6–10 | 7/6/5/4/3 % | 13/10/8/6/4 % | 17/14/11/8/5 % |
| Márgenes EBIT años 1–5 | 14 % constante | 16/17/18/19/20 % | 18/20/22/24/25 % |
| Margen años 6–10 y terminal | 14 % | 20 % | 25 % |
| Descuento / g terminal | 11 % / 2 % | 10 % / 3 % | 9 % / 3,5 % |
| Retorno incremental supuesto | 15 % | 20 % | 25 % |

La tasa central 10 % es una elección de riesgo: referencia Treasury 10 años 4,91 % observada el 2 noviembre en H.15 previamente recuperado y prima conjunta supuesta 5,09 puntos. No es un WACC beta-CAPM calculado ni una tasa libre de riesgo actualizada en tiempo real. El intento de recaptura del 4 noviembre no produjo dato legible; se conserva fecha y fuente del registro anterior. Se muestra sensibilidad 9–12 %.

## Puente patrimonial y acciones

Se añaden caja 1.868, títulos cortos 2.859 y títulos largos 524. Se reserva caja operativa del 5 % de ventas TTM (708,35) y estrés fiscal 24: puente 4.518,65 millones. No hay deuda financiera dispuesta en balance; la línea RBC de 100 está sin disponer y no se suma a caja. El pasivo de leases 188 no se resta por segunda vez al mantener rentas en EBIT.

El estrés 24 refleja la propuesta de CRA para 2020, antes de intereses. La empresa no reconoce pasivo y disputa la propuesta; los ejercicios 2021–26 siguen abiertos y el importe adicional puede ser material. No se afirma que 24 sea la pérdida probable ni máxima, y se muestra estrés adicional 100.

Inversiones estratégicas 4.911 más Flexport por puesta en equivalencia 538 se excluyen del puente central. No se declara que carezcan de valor: incluyen 2.596 de acciones/warrants con fair value observable o modelado, 1.706 de privadas, 599 de convertibles y opción Klaviyo 10. No son todas efectivo libre; Flexport tiene además convertible 351 ya dentro de 599, que no se vuelve a sumar. Concesiones por servicios producen contraprestación no monetaria, incluidas en esa estrategia. Una sensibilidad añade 75 % de los 5.449 de libro (descuento conjunto ilustrativo por liquidez/fiscalidad, no tasa fiscal factual).

Denominador conservador de investigación: 1.286,382910 millones de acciones A+B al 30 septiembre, más todas las opciones 11,821761, RSU 4,344951 y DSU 0,006168, sin reconocer proceeds = 1.302,555790 millones. No es EPS diluido contable ni máximo de toda emisión futura. Q3 diluido medio publicado 1.290,726742. La portada del 10-Q informa al 30 octubre 1.208,456928 millones A y 78,065084 millones B: 1.286,522012, incremento de 0,139102 millones sobre septiembre. No se mezcla esa fecha con el inventario de premios de septiembre ni se certifica un denominador al 3 noviembre; el modelo conserva explícitamente el ancla de septiembre. No se añaden las 531,8 millones reservadas para planes como si fueran premios emitidos, ni las acciones restringidas ya incluidas en acciones existentes. SBC futuro sigue en gasto; no se proyecta encima otra dilución anual idéntica. Puede quedar solapamiento conservador con premios actuales y no es una valoración exacta de opciones.

## Resultados y sensibilidad

'''
for k,label in [('bear','Bajista'),('base','Central'),('bull','Favorable')]:
 v=m['cases'][k];t+=f"- {label}: {v['value']:.2f} USD por acción; EV operativo {v['ev']:,.2f} millones; terminal {v['terminal_share']*100:.2f} % del EV.\n"
t+='''
El escenario central condicionado es 39,84 USD y el favorable 91,97 USD, frente al cierre de referencia de 142,57 USD; ninguno acredita margen de seguridad para una entrada.

El favorable no es techo ni probabilidad. El central depende en un 80,54 % del valor presente terminal, por lo que pequeñas hipótesis cambian mucho el resultado. No es una certificación integral del patrimonio: se han excluido inversiones y quedan contingencias y reconciliaciones pendientes.

'''
for k in ['strategic_book_after_25pct_haircut','additional_tax_stress_100','cash_revenue_no_adjustment','w0.09_g0.02','w0.09_g0.035','w0.12_g0.02']:
 t+=f"- Sensibilidad {k}: {m['sensitivities'][k]:.2f} USD.\n"
t+='''
Inverso acotado: se desplazan conjuntamente los diez márgenes centrales entre 0 y +60 puntos, dejando crecimiento, financiación y descuento constantes. No se obtiene raíz dentro del barrido de 0,5 puntos: el extremo +60 puntos (margen terminal 80 %) alcanza 136,60, aún bajo referencia. No se afirma imposibilidad universal ni se usa ese margen absurdo como pronóstico. El precio podría reflejar otras combinaciones de crecimiento, retornos, reinversión y riesgo; aquí no se fuerza una solución ni un “crecimiento implícito” sin unicidad.

## Comparables y criterios abiertos

WIX Q2, no Q3 todavía: ingresos 563,058, EBIT GAAP −58,799, CFO 55,562, PPE/software 2,920, FCF 52,642; menos SBC 53,372 queda −0,730. Su FCF ajustado 61,176 suma 8,534 de reestructuración pagada. Q3 está anunciado para el 10 noviembre: no se anticipan resultados.

EBAY Q3: ingresos 3.206, EBIT 616, CFO continuado 875, PPE 126, FCF 749, SBC 173. Su adquisición Depop cerró el 30 julio y consumió 1.321 fuera de FCF; software cambió de normativa con reformulación retrospectiva desde enero. La combinación de marketplace, publicidad, pagos y perímetro no es Shopify puro. No se homogeneizan múltiplos sin puentes de capital y préstamos equivalentes. Pares operativos ayudan a juzgar la escala, no convierten el DCF en un ranking de valor certificado.

El negocio de préstamos requiere cumplimiento por jurisdicción, y el cambio canadiense está documentado por el emisor; no se presenta como revisión legal independiente de todas sus licencias. También quedan riesgos de pagos, privacidad, impuestos, protección del consumidor, fraude y AI. Se mantiene pendiente el cierre normativo integral.

Próximos resultados exactos no identificados en el calendario IR al corte. El evento del 3 noviembre ya ocurrió. Antes de una eventual entrada se necesitan nueva lectura técnica/temporal, perímetro/capital y costes de crédito, evidencias de retornos incrementales y comparación homogénea. No se altera la gestión existente ni se registra operación.

## Fuentes y reproducción

[10-Q Q3 del 3 noviembre](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000068/shop-20260930.htm), [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm), [comunicado Q3](https://www.shopify.com/investors/press-releases/shopify-sustains-rapid-growth-revenue-32-and-free-cash-flow), [eventos](https://www.shopify.com/investors/events), [precio histórico estadounidense](https://stockanalysis.com/stocks/shop/history/), [H.15](https://www.federalreserve.gov/releases/H15/Current/). Subconjuntos numéricos, historia, fuentes de pares y supuestos identificados en el soporte portable; no se redistribuyen filings completos. Reproducir historia, pares, model.py, report.py, prepare.py y qa.py según README. Cifras monetarias de valoración son escenarios condicionados, no oferta ni recomendación de ejecución.
'''
(P/'report.md').write_text(t);(P/'report.html').write_text('<!doctype html><meta charset="utf-8"><title>SHOP · FCFF condicionado</title><style>body{max-width:1000px;margin:40px auto;font:16px/1.6 system-ui;padding:20px}pre{white-space:pre-wrap}</style><pre>'+html.escape(t)+'</pre>')
