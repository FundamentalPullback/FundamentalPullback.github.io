import json,html,re
from pathlib import Path
P=Path(__file__).resolve().parent
j=json.loads((P/'model.json').read_text());h=j['historical'];c=j['cases'];cap=j['capital']
sources=[
('AOS FY2025 Form 10-K','2026-02-10','https://www.sec.gov/Archives/edgar/data/91142/000009114226000008/aos-20251231.htm','Three annual periods, business mix, accounting, capital and share classes.'),
('AOS Q3 2026 Form 10-Q','2026-10-29','https://www.sec.gov/Archives/edgar/data/91142/000009114226000104/aos-20260930.htm','Current statements, acquisition, restructuring, debt and dilution.'),
('AOS Q2 2026 Form 10-Q','2026-07-30','https://www.sec.gov/Archives/edgar/data/91142/000009114226000098/aos-20260630.htm','Derive standalone second and third quarter flows.'),
('AOS Q1 2026 Form 10-Q','2026-04-30','https://www.sec.gov/Archives/edgar/data/91142/000009114226000084/aos-20260331.htm','First-quarter statements and cash flows.'),
('AOS Q3 2025 Form 10-Q','2025-10-28','https://www.sec.gov/Archives/edgar/data/91142/000009114225000150/aos-20250930.htm','Prior TTM comparator and quarterly year-over-year context.'),
('AOS third-quarter 2026 results','2026-10-29','https://investor.aosmith.com/news-releases/news-release-details/o-smith-reports-third-quarter-2026-results','Ex-China guidance and FY2025 reconciliation, pension balance.'),
('AOS China majority sale announcement','2026-10-27','https://investor.aosmith.com/news-releases/news-release-details/o-smith-announces-majority-interest-china-business-acquired-cpe','81% disposal, 19% retained stake, licensing and closing conditions.'),
('AOS fourth-quarter 2025 results','2026-01-29','https://investor.aosmith.com/news-releases/news-release-details/o-smith-reports-record-2025-diluted-earnings-share-eps-385-and','Standalone Q4 EPS and full-year comparison.'),
('AOS Events and Presentations','accessed 2026-11-07','https://investor.aosmith.com/news-events/events-and-presentations','Calendar: October 29 call archived, next results not announced.'),
('AOS price history','2026-11-06','https://stockanalysis.com/stocks/aos/history/','Verified regular-session close, distinct from scanner observation.'),
('U.S. Treasury daily yield curve','2026-11-06','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve','USD 10-year risk-free calibration of 4.86%.'),
('ZWS Q3 2026 Form 10-Q','period ended 2026-09-30; accessed 2026-11-07','https://www.sec.gov/Archives/edgar/data/1439288/000162828026067577/zws-20260930.htm','Peer TTM earnings, cash, acquisition and tariff qualifications.'),
('ZWS FY2025 Form 10-K','2026-02-09','https://www.sec.gov/Archives/edgar/data/1439288/000162828026006372/zws-20251231.htm','Peer annual cash and earnings bridge.'),
('ZWS price history','2026-11-06','https://stockanalysis.com/stocks/zws/history/','Peer matched regular-session price $43.47.')]
# Dates are published dates where verified; otherwise period/access dates are labeled.
(P/'sources.json').write_text(json.dumps([dict(title=t,date=d,url=u,purpose=p) for t,d,u,p in sources],indent=2))
def table(periods):
 s='|Periodo|Ventas|EBIT operativo|Neto|CFO|Capex|SBC|FCF menos SBC|\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
 for p in periods:s+='|'+p+'|'+ '|'.join(f'{h[p][k]:,.1f}' for k in ['sales','ebit','net','cfo','capex','sbc','cash_after_sbc'])+'|\n'
 return s
case_table='|Caso|Ventas años 1–5|Margen inicial / año 5 / año 10|WACC|g|ROIC incremental|USD/acción|Peso terminal|\n|---|---:|---|---:|---:|---:|---:|---:|\n'
for name,v in c.items():
 p=v['inputs'];case_table+=f"|{name}|{p['growth']:.1%}|{p['margin_start']:.1%} / {p['margin5']:.1%} / {p['margin10']:.1%}|{p['wacc']:.2%}|{p['g']:.1%}|{p['roic']:.0%}|{v['per_share']:.2f}|{v['terminal_weight']:.1%}|\n"
pros=[('La franquicia de reposición y distribución sostiene un margen norteamericano de 23,6%, aunque ha cedido 60 puntos básicos.','Replacement demand and distribution support a 23.6% North American margin, although it fell 60 basis points.'),('La caja operativa TTM de 612,5 millones cubre inversión física y SBC, sin depender de nuevo capital para la operación ordinaria.','TTM operating cash of $612.5 million covers physical investment and SBC without relying on new capital for ordinary operations.'),('La venta acordada de China puede reducir exposición a un mercado débil; conserva 19% y una licencia, pero sigue pendiente de cierre.','The agreed China sale can reduce exposure to a weak market; a 19% stake and license remain, but closing is pending.')]
cons=[(f"El FCFF central de {c['base']['per_share']:.2f} USD queda por debajo del cierre de 64,55; el favorable de {c['bull']['per_share']:.2f} apenas lo respalda.",f"Central FCFF of ${c['base']['per_share']:.2f} is below the $64.55 close; the ${c['bull']['per_share']:.2f} favorable case only just supports it."),('El beneficio neto TTM cae 6,77% y la caja después de capex y SBC cae 2,11%; las recompras no sustituyen crecimiento.','TTM net income fell 6.77% and cash after capex and SBC fell 2.11%; buybacks do not replace growth.'),('Faltan caja e impuestos finales de la venta, economía de royalties y flujos del perímetro retenido; el beneficio arancelario no está cuantificado.','Final sale cash and taxes, royalty economics and retained-perimeter cash flows remain unresolved; the tariff benefit is unquantified.')]
summary=f"AOS: observar y esperar precio o recuperación. FCFF condicionado {c['bear']['per_share']:.2f} / {c['base']['per_share']:.2f} / {c['bull']['per_share']:.2f} USD frente a 64,55. Beneficio TTM decreciente y China pendiente de cierre; sin entrada aprobada."
summaryen=f"AOS: watch for a better price or operating recovery. Conditional FCFF ${c['bear']['per_share']:.2f} / ${c['base']['per_share']:.2f} / ${c['bull']['per_share']:.2f} versus $64.55. TTM earnings are declining and China closing remains pending; no approved entry."
text=f'''# A. O. Smith: reposición resistente, recuperación todavía no demostrada

Investigación: 7 noviembre 2026. Datos financieros hasta septiembre 2026. USD millones, salvo precio, EPS y porcentajes. **Estado: investigación condicionada, screen-grade; no Stage 3 aprobado ni Stage 3.5.**

{summary}

{summaryen}

## Qué tendría que ser verdad

AOS conserva marcas, canales profesionales y una base de equipos que requieren sustitución. Eso amortigua la vivienda, pero no elimina menores volúmenes, acero, fletes ni competencia. Para justificar 64,55 sin hipótesis favorables simultáneas, el negocio retenido tendría que crecer y convertir mejor de lo que demuestra hoy. La venta de China ayuda al foco, pero no convierte automáticamente una caída del beneficio en crecimiento orgánico. Esperar menor precio o evidencia; no hay techo, stop, cantidad ni orden autorizados.

El escáner del 6 noviembre muestra Opportunity 80, QP 80 y 64,54. Es elegible para esta exploración autorizada desde 65; no cambia el filtro general del plan ni sus reglas de compra. El precio 64,54 es una observación del escáner sin hora verificada. El cierre regular comprobado fue **64,55 a las 16:00 EST del 6 noviembre**. No reemplazamos uno por otro silenciosamente. La biblioteca y el perfil completos no mostraron investigación directa anterior de AOS; existía como comparable de ZWS.

## Negocio, mezcla y cambios de perímetro

En FY2025 Norteamérica vendió 2.460,1 en calentadores, 281,0 en calderas/componentes y 243,1 en tratamiento de agua. China, antes de eliminaciones, vendió 689,5 frente a 791,9 en 2024 y 835,1 en 2023. No sumar cifras de segmentos con intercompañía al consolidado sin eliminar duplicidades. En Q3 2026 las ventas norteamericanas crecen 3%, pero solo 1% orgánico: Leonard Valve aporta 14,8. Calderas crecen 13% según el emisor; caen volúmenes residenciales. El margen del segmento baja de 24,2% a 23,6%. Tratamiento de agua implica optimización de fábricas y marcas, no crecimiento gratuito.

China Q3 cae 17% en moneda local según el emisor. El desglose geográfico muestra 139,8 frente a 151,7 (−7,84% reportado), mientras la dirección comunica −17% local. El puente exacto entre ambas bases no está conciliado; no se inventa una explicación por divisas/eliminaciones ni se deriva crecimiento orgánico de esa fila. Esta discrepancia permanece abierta. Rest of World incluye también India y Europa: no se elimina todo el segmento al valorar la venta. Ventas ROW 192,8, beneficio 10,5, margen 5,4% frente a 7,4%; traducción de moneda aporta aproximadamente 5 a ventas. Los flujos del modelo son nominales USD, sin convertir otra vez ventas ya traducidas.

El 27 octubre se acordó vender 81% de China, manteniendo 19% y licencia de marca. Valor empresarial anunciado cercano a 400, libre de deuda/caja; el valor total incluyendo licencia supera 500 según la compañía. Cierre esperado H1 2027, sujeto a condiciones y aprobaciones. No es una venta cerrada ni 500 de efectivo. El emisor espera presentar China discontinuada desde Q4 y reexpresar la historia; Q3 y el TTM publicados todavía la incluyen.

## Historia homogénea: tres ejercicios, cuatro trimestres, dos TTM

{table(['FY2023','FY2024','FY2025'])}

{table(['Q4 2025','Q1 2026','Q2 2026','Q3 2026'])}

{table(['TTM2025','TTM2026'])}

TTM = ejercicio anterior + nueve meses actuales − nueve meses anteriores. Flujos trimestrales obtenidos por diferencias de acumulados; Q4 = FY − 9M. EBIT operativo = beneficio bruto − SG&A − reestructuración, antes de otras partidas no operativas e intereses. No confundirlo con EBIT del emisor, que puede incluir otros ingresos: FY2025 son 728,0 operativos frente a 728,6 por neto + impuestos + intereses.

EPS diluido FY2023/2024/2025: 3,69 / 3,63 / 3,85. Los cuatro trimestres Q4 2025 a Q3 2026: 0,90 / 0,85 / 0,91 / 0,93. Q4 0,90 está publicado directamente, no es resta de EPS redondeados. Q3 neto cae 4,32% y EPS 1,06%; acciones diluidas medias caen de 140,895 a 136,098 millones. Esta diferencia muestra el apoyo de recompras, no mayor beneficio total. No construimos un EPS TTM exacto sumando importes redondeados o mezclando ponderaciones.

En TTM ventas caen 0,71%, EBIT operativo 4,90%, neto 6,77% y CFO 6,57%. El margen operativo baja de 18,35% a 17,57%. La caja después de capex y SBC cae solo 2,11% porque capex desciende 39,38%. La conversión FCF/neto de 113,6% no demuestra mejora estructural: el capex TTM 50,8 está por debajo de D&A 94,8. No perpetuamos esa brecha como caja gratuita.

## Normalización: qué se retira y qué se conserva

- Reestructuración 2026: 22,6 antes de impuestos, incluidos 12,4 de deterioro y 10,2 de costes potencialmente monetarios; beneficio fiscal 5,5. Se distingue rentabilidad recurrente de caja: se pueden mostrar resultados sin el cargo, pero los pagos siguen siendo reales. Quedan 9,3 de provisión a septiembre, reservados en el puente para no prometer caja libre. Históricamente hubo 17,6 en 2024 y 18,8 en 2023; no son accidentes imposibles de repetir.
- Leonard Valve costó 469,5 en efectivo y se financió con préstamo de 470. Aporta 46,6 de ventas y 15,2 de beneficio antes de impuestos en nueve meses; su PPA aún es preliminar. Los costes de adquisición son 6,8. No eliminar amortización de clientes de forma automática ni sumar otra vez el precio de compra a deuda ya reflejada. No se modelan adquisiciones futuras sin financiación.
- Como prueba favorable a la compañía, EBIT TTM más reestructuración y los 6,8 de transacción = 697,7; el TTM previo más reestructuración = 720,3. Aun antes de retirar cualquier devolución arancelaria, cae 3,14%. Tampoco es crecimiento orgánico: incorpora el negocio comprado. La comparación no certifica todo el EBIT normalizado.
- Hay beneficio de devoluciones IEEPA compensando costes. El importe no está cuantificado en los textos primarios revisados. No declaramos cero ni inventamos una conciliación. Una reducción hipotética de 10 o 20 en beneficio operativo recurrente equivale aproximadamente a 0,3 o 0,6 puntos de margen sobre 3.280; es incertidumbre de hipótesis, no un ajuste publicado.
- SBC TTM 15,2 se conserva como coste económico en márgenes; el FCF histórico menos SBC hace visible su coste. No restarla de nuevo del FCFF después de mantenerla en EBIT. La dilución incremental del denominador cubre derechos ya existentes, sin proyectar recompras gratuitas.
- El tipo efectivo 9M baja a 23,0% frente a 24,1% por una elección fiscal transfronteriza; Q3 sube a 24,2% frente a 23,2% por mezcla. Usamos 25% normalizado, sensibilidad 23–28%, sin perpetuar el beneficio discreto. FY2023 contiene 0,9 de ingreso por liquidación de pensión; no se proyecta.
- A septiembre cuentas por cobrar 612,9 frente a 582,3 al cierre anterior, inventario 509,3 frente a 479,3 y proveedores 516,6 frente a 504,1. Depósitos de clientes China bajan de 34,2 a 18,6. No es liberación gratuita de circulante. CFO 9M incluye 26,0 de impuestos diferidos frente a 9,7 y 12,4 de deterioro no monetario; capex menor explica la mejora aparente del FCF.

## Capital, liquidez y puente de equity

Deuda 673,1 = 41,0 corriente + 632,1 larga; caja 234,5. Préstamo Leonard de 470 vence enero 2029 con pago final, tipo Q3 4,56%. Dos préstamos chinos suman 74,5 y vencen junio 2027, aunque clasificados largos por intención/capacidad de refinanciar. Revolvente 500 no dispuesto vence agosto 2029; la compañía declara cumplimiento de covenants. TTM EBIT operativo/intereses es 26,4 veces aproximadamente, pero no sustituye el cálculo contractual.

Puente del modelo: sumar 134,5 de caja excedentaria (reserva operativa propia 100), restar deuda total 673,1, pensión publicada 7,5 y pagos de reestructuración pendientes 9,3. Los arrendamientos operativos permanecen como gasto dentro de margen; no se resta deuda de leasing adicional con la renta ya cargada. Garantías de producto 213,9 se tratan como pasivo operativo y gasto recurrente, no se restan nuevamente todas las garantías de equity. La provisión de reestructuración se separa del circulante normal para evitar doble cómputo.

Acciones a 27 octubre: 25,860239 millones Clase A más 108,468717 ordinarias = 134,328956. Añadimos 0,734055 millones de dilución incremental Q3 como aproximación, total **135,063011**. No confundir acciones emitidas con circulantes netas de autocartera. Las clases comparten economía de EPS, pero no voto: la familia Smith controlaba 67,8% del voto al cierre 2025. Se valora el derecho económico, no una prima de control. Sensibilidad usar 136,098 millones medias Q3 reduciría la valoración central aproximadamente 0,34 por acción.

Para China añadimos por separado valor de negocio bruto 240 / 320 / 400, no ingresos de China dentro del FCFF retenido. 320 aplica un descuento propio de 20% al valor empresarial anunciado: recoge impuestos, costes y riesgo, **no es estimación certificada de efectivo neto de venta**. Incluye conjuntamente lo realizado y el 19% retenido sobre base empresarial; se conserva la deuda completa en el puente. No convertir 324 (81% de 400) en equity neta sin asignar deuda, caja e impuestos; no sumar además 76, 80 repatriables o una licencia de 100. La caja china que se repatría ya forma parte del efectivo consolidado. Royalty NPV se deja en cero por prudencia, no porque la licencia no valga. Cambios de deuda/caja transferida, impuestos, cierre y valoración del 19% exigen un puente definitivo futuro.

## FCFF del perímetro retenido: diez años, crecimiento financiado

Ventas iniciales 3.280: punto medio de guía ex-China 3.270–3.290. Guía EPS ajustado ex-China 3,42–3,52 frente a 3,42 en 2025: no promete recuperación fuerte. El emisor concilia FY2025 ex-China ventas 3.155,3 y EBIT 668,2, margen 21,18%; el modelo comienza 19–20,5%, incorporando presión actual, costes ordinarios y SBC. La historia permanece publicada con China; el futuro es una hipótesis ex-China separada, no un TTM recast inventado.

{case_table}

Ancla temporal: valoración al cierre del 6 noviembre 2026; la guía FY2026 ex-China es una aproximación al nivel inicial de ventas. Año 1 representa un año futuro completo descontado a t=1 desde esa fecha, seguido de otros nueve años completos. No se incorpora flujo parcial de 2026, ajuste por fracción de año ni descuento separado por demora del cierre de China. Los valores son aproximaciones anuales condicionadas, no una valoración con calendario exacto de la transacción.

Años 1–5: crecimiento de ventas constante por caso y margen convergiendo gradualmente al año 5; años 6–10: crecimiento y margen convergen linealmente a g y margen final. Crecimiento central 4% está cerca de guía agregada ex-China, no se llama orgánico demostrado; favorable 6% exige expansión de calderas/agua/India y recuperación residencial. No se presupone todo el crecimiento de China dentro del retenido. Margen favorable 23% exige mejoras operativas, mezcla y precio; no es la guía de la dirección.

FCFF = EBIT × (1 − impuesto) + D&A − inversión − Δcirculante. D&A supuesta 2,5% de ventas, circulante incremental 12% de incremento de ventas. Reinversión neta = mayor entre incremento positivo de NOPAT/ROIC incremental y suelo físico de 0,5% de ventas más circulante. Así se financian tanto crecimiento como mejora de margen. Inversión bruta = D&A + reinversión neta − circulante. Es presupuesto económico amplio de reinversión, no previsión publicada de capex fabril: central año 1 implica 224,5 frente a 50,8 de capex consolidado TTM. Esta prudencia es material y explica menor valor; no se oculta como dato observado.

En terminal: reinversión = mayor de NOPAT × g/ROIC y suelo físico más circulante. D&A no desaparece y el crecimiento terminal no es gratis. ROIC incremental 12/16/20% es hipótesis prudente frente a negocio maduro con márgenes altos; el precio pagado por Leonard y la caída actual impiden asumir retornos extraordinarios perpetuos. El suelo no liga en el central porque la financiación por NOPAT ya exige más; sí limita escenarios de crecimiento bajo. Evita inversión negativa cuando se estrechan márgenes.

WACC nominal USD central 9,75%: Treasury 10 años 4,86% a 6 noviembre; ERP supuesto 4,75%, beta de riesgo supuesta 1,10, no regresión estimada. Coste de equity 10,085%; deuda marginal supuesta 5,5%, después de 25% de impuesto 4,125%, ponderación objetivo de deuda supuesta de 6% da 9,73%, redondeado 9,75%. El 6% es una hipótesis objetivo del analista, no una ponderación observada: deuda bruta / (deuda bruta + capitalización con las dos clases actuales) es aproximadamente 7,20%. No usar la deuda/valor contable 27% como peso de mercado. Rango 9–10,75% recoge defensividad de reposición frente a demanda, ejecución y venta; g 2–3% nominal a largo plazo y siempre inferior a WACC. No se presenta ERP/beta como datos de mercado observados.

Base: EV retenido {c['base']['ev']:.1f}, puente neto {c['base']['equity_bridge']:.1f}, equity {c['base']['equity']:.1f}, dividido entre 135,063011 millones. China no se añade al EV retenido y vuelve a sumarse: está una sola vez en el puente. No hay probabilidades asignadas ni promedio mecánico.

## Expectativas implícitas y sensibilidades

Comparación condicional con el central: margen de seguridad aritmético = (valor − precio) / valor = **−43,81%**; variación desde precio hasta valor = (valor − precio) / precio = **−30,47%**. Son denominadores distintos. No hay margen de seguridad certificado, umbral de revisión aprobado ni techo de compra: 44,88 es una referencia analítica condicionada y no una autorización operativa. No se aplica automáticamente un descuento universal del 15%.

Manteniendo margen central 21%, WACC 9,75%, g 2,5% y ROIC 16%, el cierre 64,55 exige crecimiento años 1–5 de **{j['inverse']['first_five_year_growth']:.2%}**, seguido de transición a 2,5%. Es una inversa condicional, no consenso. Se buscó en −5% a 30%, se verificó el precio reconstruido y monotonía de crecimiento entre 0% y 20%. No extrapolar fuera de esos supuestos; la inversa exige crecimiento muy superior al 4% central. Los valores favorables no son límites de seguridad.

|WACC / g|1,5%|2,0%|2,5%|3,0%|
|---|---:|---:|---:|---:|
'''
for w in [.0875,.0925,.0975,.1025,.1075]:text+='|'+f'{w:.2%}'+'|'+'|'.join(f"{r['value']:.2f}" for r in j['sensitivity'] if r['wacc']==w)+'|\n'
text+='''
En central, impuesto 23/25/28% da 46,13 / 44,88 / 43,02; ROIC 12/16/20% da 40,94 / 44,88 / 47,25. Cambiar caja operativa reservada de 50 a 150 mueve aproximadamente ±0,37 por acción. Llevar el activo China de cero a 500 da aproximadamente 42,52–46,22: la incertidumbre de la venta no explica por sí sola toda la brecha a 64,55. Suelo neto 0%, 0,5% o 1% no cambia el central, porque el retorno incremental ya impone mayor inversión. El archivo calculado contiene precisión completa y las diez filas de cada escenario.

## Comparable: menos caro que ZWS no significa barato

Precio regular 6 noviembre, USD, US GAAP, TTM septiembre; para comparabilidad usamos acciones medias diluidas Q3 en ambos (AOS 136,097723; ZWS 168,105), no la aproximación de acciones actuales del DCF. P/E AOS 17,76x frente a ZWS 25,27x; precio/FCF 15,64x frente a 18,88x; precio/(FCF−SBC) 16,08x frente a 21,24x. AOS neto TTM 494,6, FCF 561,7, SBC 15,2; ZWS neto continuo 289,2, FCF 387,0, SBC 43,0. ZWS tiene mayor crecimiento de ingresos, mezcla comercial/institucional y distinta exposición a construcción y China; no se traslada su prima automáticamente.

Los ratios todavía contienen devoluciones arancelarias. En ZWS se conoce efecto neto 40,4: FCF−SBC−reembolso = 303,6, múltiplo 24,07x. En AOS falta el importe: comparar 16,08x reportado con 24,07x ajustado no sería homogéneo. ZWS CFO también incorpora flujos discontinuados no separados, y AOS cambiará perímetro. Es contraste delimitado, no muestra estadística ni mediana de sector. No se certifica una banda histórica homogénea de múltiplos: no se dispone de capitalización y ajustes históricos con el nuevo perímetro, y usar precios pasados contra beneficio actual sería engañoso. Esta limitación mantiene la investigación condicionada.

## Catalizadores, riesgos y prueba de recuperación

La fecha primaria Q3 fue 29 octubre 2026 y ya ocurrió; no existe fecha futura anunciada en el calendario consultado. No diferir AOS como si reportara entre 2 y 6 noviembre. Hitos: resultados Q4 con historia ex-China recast, detalle del acuerdo y cierre H1 2027, caja neta después de impuestos, costes centrales retenidos, gasto de separación, licencia y valoración del 19%. Son expectativas, no fechas confirmadas salvo la llamada ya realizada.

Mejoraría la tesis: recuperación de volumen residencial, crecimiento orgánico sin compra, margen después de aranceles y costes, capex/retorno que sostengan expansión, China cerrada con puente verificable. La invalidarían más debilidad de demanda, problemas de calidad/garantías, pérdida de distribución, costes sin precio, integración débil, retraso de China o retorno insuficiente de adquisiciones. Reposición no elimina exposición macro ni transición tecnológica hacia mayor eficiencia/heat pumps. La recuperación del precio desde octubre no prueba recuperación fundamental; no atribuimos todo el drawdown a una única noticia sin estudio causal.

No se ejecutaron operaciones ni se cambió gestión. El resultado aporta investigación y una valoración condicionada; solo una revisión posterior con rentabilidad sostenible, perímetro y precio satisfactorios podría reabrir Stage 3. Stage 3.5 exigiría análisis técnico/riesgo separado.

## Evidencia exacta para pros y contras / Exact pros and cons

'''
for title,arr in [('A favor / Pros',pros),('En contra / Cons',cons)]:
 text+='### '+title+'\n\n'
 for es,en in arr:text+='- '+es+'\n- '+en+'\n'
text+='\n## Fuentes públicas\n\n'
for title,date,url,purpose in sources:text+=f'- [{title}]({url}) · {date} · {purpose}\n'
text+='\n## Reproducción y control\n\nModelo propio en Python estándar, resultados JSON y pruebas QA acompañan este informe. No contiene documentos originales del emisor. La historia concilia cuatro trimestres con TTM; se revisaron FCFF, inversión, WACC > g, orden de casos e inversa. Los límites de datos se conservan; aprobación fundamental y publicación final requieren revisión humana.\n'
(P/'report.md').write_text(text)
(P/'summary.json').write_text(json.dumps(dict(ticker='AOS',company='A. O. Smith Corporation',asOf='2026-11-07',summary=summary,summaryEn=summaryen,status='conditional',stage3Complete=False,entryApproved=False,approvedValuation=None,valuationScope='conditional_research_only',approvedReviewThreshold=None,certifiedMarginOfSafety=None,conditionalMarginOfSafety=(c['base']['per_share']-cap['price'])/c['base']['per_share'],priceToValueReturn=(c['base']['per_share']-cap['price'])/cap['price'],decision='En observación',decisionEn='Watchlist',currency='USD',close=64.55,closeDate='2026-11-06',valuation={k:round(v['per_share'],2) for k,v in c.items()},pros=[dict(text=a,textEn=b,evidence=a,sourceUrl=sources[k][2],evidenceOrigin='authored_report_summary',evidenceArtifact='report.html') for (a,b),k in zip(pros,[5,1,6])],cons=[dict(text=a,textEn=b,evidence=a,sourceUrl=sources[k][2],sourceUrls=[sources[z][2] for z in ks],evidenceOrigin=origin,evidenceArtifact='report.html') for (a,b),k,ks,origin in zip(cons,[5,1,6],[[5,10,6],[0,1,4],[1,5,6]],['analyst_model_derived_from_public_inputs','analyst_calculation_from_reported_financials','authored_source_gap_assessment'])],next='Q4 y reexpresión ex-China; fecha no anunciada. Cierre China esperado H1 2027, condicionado.',nextEn='Q4 and ex-China recast; date unannounced. China closing expected H1 2027, conditional.'),indent=2))
# Minimal static publication rendering; all text and tables are authored above.
lines=text.splitlines();parts=[];inlist=False;intable=False
for line in lines:
 if line.startswith('|'):
  if not intable:parts.append('<div class="table"><table>');intable=True
  if re.match(r'^\|[-:| ]+\|$',line):continue
  parts.append('<tr>'+''.join('<td>'+html.escape(x.strip())+'</td>' for x in line.strip('|').split('|'))+'</tr>');continue
 if intable:parts.append('</table></div>');intable=False
 def fmt(s):
  s=html.escape(s);s=re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s);return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
 if line.startswith('#'):
  n=len(line)-len(line.lstrip('#'));parts.append(f'<h{n}>'+fmt(line[n:].strip())+f'</h{n}>')
 elif line.startswith('- '):parts.append('<p class="bullet">• '+fmt(line[2:])+'</p>')
 elif line.strip():parts.append('<p>'+fmt(line)+'</p>')
(P/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AOS · Investigación condicionada</title><style>body{font:17px/1.6 system-ui,sans-serif;color:#172b3a;background:#f7f8f7;margin:0}main{max-width:1000px;margin:0 auto;padding:48px 28px;background:white}h1{font-size:38px;line-height:1.15;color:#123c43}h2{margin-top:2.2em;border-top:2px solid #b1c8ca;padding-top:22px;color:#123c43}h3{font-size:20px}a{color:#126770;overflow-wrap:anywhere}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}td{padding:8px;border-bottom:1px solid #dde5e5;text-align:right}td:first-child{text-align:left}tr:first-child{font-weight:700;background:#e9f1f1}.bullet{padding-left:16px}strong{color:#103e48}</style><main>'+''.join(parts)+'</main></html>')
print('Report and source ledger generated.')
