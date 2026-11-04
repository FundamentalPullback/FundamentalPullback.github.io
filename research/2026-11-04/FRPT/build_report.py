from pathlib import Path
import json,datetime
P=Path(__file__).parent
h=json.load(open(P/'history.json'));m=json.load(open(P/'model_results.json'));peers=json.load(open(P/'comps.json'))['rows']
fmt=lambda v,d=2: 'n/d' if v is None else f'{v:,.{d}f}'
pct=lambda x:f'{100*x:.2f}%'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n'
periods=['FY2023','FY2024','FY2025','Q4 2025','Q1 2026','Q2 2026','Q3 2026','TTM Sep2025','TTM Sep2026']
hist=table(['Periodo','Ventas','Beneficio bruto','EBIT GAAP','Beneficio neto','EPS básico / diluido','CFO','Capex caja','FCF caja'],[[k]+[fmt(h[k].get(v),3) for v in ['revenue','gross_profit','ebit','net_income']]+[fmt(h[k].get('eps_basic'))+' / '+fmt(h[k].get('eps_diluted'))]+[fmt(h[k].get(v),3) for v in ['cfo','capex','cash_fcf']] for k in periods])
norm=table(['Periodo','SBC publicada','SBC analista 3%','Cargos retirados EBIT','EBIT normalizado','FCF − SBC normalizada','D&A CFO','Δ circulante: entrada +'],[[k]+[fmt(h[k].get(v),3) for v in ['sbc_total','analyst_sbc_3pct','nonrec_operating_charges','ebit_standardized_sbc_3pct','cash_fcf_after_standardized_sbc_3pct','da_cf','operating_wc_cash_change']] for k in periods])
sc=table(['Escenario','CAGR ventas 10 años','Ventas año 10','EBIT año 10','WACC / g / ROIC','Valor hoy','Vs $69.60','Peso terminal','TIR negocio / accionista*'],[[k,pct(z['revenue_cagr']),fmt(z['years'][-1]['net_revenue']),pct(z['years'][-1]['ebit_margin']),' / '.join(pct(z['params'][v]) for v in ['wacc','g','roic']),fmt(z['per_share']),pct(z['upside']),pct(z['terminal_share']),pct(z['enterprise_fixed_exit_irr'])+' / '+pct(z['equity_distribution_proxy_irr'])] for k,z in m['scenarios'].items()])
years=table(['Año rodante','Ventas','EBIT económico','SBC ya incluida','Impuesto caja','D&A total','Capex total','Δ WC inversión','FCFF'],[[str(q['year'])]+[fmt(q[k]) for k in ['net_revenue','ebit','sbc','cash_tax','da','capex_total','change_operating_wc','fcff']] for q in m['scenarios']['central']['years']])
reverse=table(['WACC','EBIT maduro','CAGR ventas requerido','Ventas año 10','Hogares año 10, M','Compra anual retail'],[[pct(x['wacc']),pct(x['year10_ebit_margin']),pct(x['cagr']),fmt(x['year10_revenue']),fmt(x['year10_households']),fmt(x['year10_buy_rate'])] for x in m['reverse_joint']])
comps=table(['Par / cierre 3 nov','TTM hasta','EV proxy con NCI libro','EBIT normalizado','EV/EBIT','EV/ventas','FCF − SBC','Rend. caja − SBC'],[[r['ticker']+' / $'+fmt(r['price']),r['period'],fmt(r['ev_nci_book_proxy']),fmt(r['ebit_norm_low'])+'–'+fmt(r['ebit_norm_high']),fmt(r['ev_ebit_low'])+'–'+fmt(r['ev_ebit_high']),fmt(r['ev_sales']),fmt(r['cash_fcf_less_sbc']),pct(r['yield_after_sbc'])] for r in peers])
discount=table(['WACC \\ g','2.0%','2.5%','3.0%','3.5%'],[[pct(w)]+[fmt(next(x['value'] for x in m['discount_terminal_sensitivity'] if x['wacc']==w and x['terminal_growth']==g)) for g in [.02,.025,.03,.035]] for w in [.09,.095,.1025,.11,.115]])
pricegrid=table(['Precio','TIR anual del negocio, salida fija'],[[fmt(x['price']),pct(x['enterprise_fixed_exit_irr'])] for x in m['central_price_return_grid']])
joint=table(['Desplazamiento anual conjunto de motores','EBIT final −2pp','EBIT final igual','EBIT final +2pp','EBIT final +4pp'],[[pct(g)]+[fmt(next(x['price'] for x in m['joint_growth_margin_sensitivity'] if x['annual_growth_component_shift']==g and x['ebitda_margin_shift']==v)) for v in [-.02,0,.02,.04]] for g in [-.02,0,.02,.04]])
sens=table(['Cambio aislado central','Valor por acción'],[[x['case'],fmt(x['value'])] for x in m['operating_sensitivities']])
s='''# FRPT — Stage 3 completo tras resultados Q3 2026

**Fecha de revisión: 4 de noviembre de 2026, después del comunicado de las 06:30:34 EST y antes de la conferencia de las 08:00 EST. Versión FRPT-S3-20261104-v1.**

**Resultado: buena empresa; esperar precio o evidencia que respalde un escenario más exigente. Investigación fundamental completa con la información publicada al corte; no aprobada una compra ni una entrada Stage 3.5.** No se descarta permanentemente. No se exige un descuento universal del 15%, un crecimiento mínimo mecánico ni una rentabilidad arbitraria.

Precio de referencia **$69.60**, cierre regular del 3 de noviembre, no cotización posterior al resultado. Nasdaq, acción ordinaria estadounidense, USD; no ADR ni conversión de divisas. Verificado con [historial de FT/Markit](https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=FRPT%3ANMQ) y la observación del [escáner del usuario](https://fundamentalpullback.github.io/data/scan-3960.js). No se mezclan precios intradía/after-hours con el cierre. Cantidades en millones de USD, salvo acciones, EPS, hogares y porcentajes especificados.

## 1. Qué decide la revisión

- El trimestre confirma progreso operativo real: ventas +10.0%, volumen +10.0%, margen bruto GAAP 44.5% y EBIT $35.130m. El EBIT TTM normalizado después de SBC económica crece **20.6%**, no el crecimiento aparente del beneficio neto contaminado por impuestos/venta de inversión.
- La calidad de crecimiento merece vigilancia: consumo medido +12.7%, pero hogares compradores apenas +1%, frente a +9% de gasto por hogar. Parte de la brecha entre consumo y envíos tiene explicación de calendario/inventario; no prueba deterioro estructural ni garantiza recuperación.
- La mejora de caja existe, pero Q3 CFO cae $6.0m; el FCF sube $6.3m porque capex cae $12.3m. El recorte de capex es en parte aplazamiento por productividad, no prueba de inversión recurrente mínima.
- DCF central **$44.38**, alternativa operativa plausible a coste de capital central **$58.92**, y alternativa conjunta con WACC 9.5%/ROIC 20% **$68.34**. Escenario favorable más exigente **$84.79**. Por tanto, $69.60 puede tener explicación económica razonable, pero requiere mejoras de demanda, margen y/o coste de capital simultáneamente; no queda respaldado por el centro de la evidencia actual.
- Rango de trabajo de escenarios centrales plausibles: **aproximadamente $44–59**. El entorno de $68 no es absurdo, pero supone adoptar la alternativa conjunta favorable de demanda/márgenes/capital. No se denomina “valor razonable” a todo el intervalo adverso–favorable $11–85.
- Confianza **media en la dirección operativa y baja-media en el valor puntual**. La amplitud es incertidumbre de hipótesis, no probabilidades ni límites de pérdida.

## 2. Resultados nuevos, guía y acontecimientos

El [comunicado oficial de 4 nov](https://investors.freshpet.com/news-releases/news-release-details/freshpet-inc-reports-third-quarter-2026-financial-results), los [comentarios preparados](https://investors.freshpet.com/static-files/c7c74ec5-1ed3-410b-8411-deca2f2f769e) y la [presentación Q3](https://investors.freshpet.com/static-files/f82d5c97-c5cc-4996-bcf7-5114ee716771) ya están publicados. La conferencia y sus preguntas todavía no habían ocurrido al corte. La consulta SEC final a las 11:59 UTC no mostraba aún el 10-Q/8-K de resultados; no se inventan sus notas.

Q3 ventas $317.840m frente a $288.848m; beneficio bruto $141.307m frente a $114.192m; EBIT $35.130m frente a $24.901m; beneficio neto $29.712m frente a $101.663m; EPS básico/diluido $0.61/$0.58. El desplome del beneficio neto interanual no es una caída comparable del negocio: el anterior trimestre tenía una fuerte liberación fiscal. Margen bruto ajustado 50.0% y EBITDA ajustado $64.542m/20.3% no equivalen a márgenes GAAP.

9M ventas $921.070m (+12.8%): volumen +13.3%, precio/mix −0.5%. EBIT $61.170m, beneficio neto $97.708m; éste incluye ganancia de inversión $66.552m. CFO $145.516m y capex $80.259m. La venta de inversión aportó $99.998m a **inversión**, ya excluida del CFO; no se resta otra vez del CFO.

Guía FY2026: ventas +12–13% frente a +10–12%, equivalente a **$1,234.257–1,245.277m**, centro $1,239.767m. EBITDA ajustado $215–220m frente a $210–220m. Capex $125–150m frente a aproximadamente $150m. Esto implica capex Q4 **$44.741–69.741m**, muy superior a los $22.935m de Q3. No extrapolar el último trimestre bajo.

Objetivos 2027: ventas por encima de categoría, margen bruto ajustado al menos 49%, EBITDA ajustado 20–22%. Los comentarios nuevos sitúan el margen en la **mitad inferior** sin alivio importante de inflación. Se planean aumentos selectivos de precio en algunos artículos. Logística supone $10–12m sobre el plan inicial FY26, frente a $8m previsto en Q2. Q4 espera menor margen bruto secuencial por paradas planificadas y personal de Homestyle. No se presenta consenso como si fuera guía: este informe no usa una serie verificable de estimaciones sell-side.

## 3. Negocio, crecimiento y motivo del retroceso

Freshpet fabrica comida refrigerada para mascotas y opera infraestructura de producción, cadena fría y refrigeradores propios en minoristas. No es software recurrente ni una marca de alimentación sin activos. Sus posibles ventajas son distribución, densidad logística, fabricación, calidad y repetición de compra. Aún debe demostrar que esas ventajas generan retornos sostenibles después de publicidad, capex y SBC. Walmart representó 25% de ventas FY25, Costco 10% y los diez principales clientes 68%: poder de negociación concentrado. Fuente: [10-K FY2025, negocio/riesgos](https://www.sec.gov/Archives/edgar/data/1611647/000161164726000006/frpt-20251231.htm).

Q3 red: 31,164 tiendas, 40,523 refrigeradores; 25% de tiendas EE.UU./Canadá tienen más de uno. Tiendas +5%, refrigeradores +4%, capacidad cúbica +5%, puntos de distribución +14%. Ecommerce +35% y 16.9% de negocio, pero 82% se sirve mediante la red minorista; no sumar digital y fridges como mercados excluyentes. Homestyle supera $100m de ventas **retail**, no ventas netas de FRPT.

Panel 52 semanas: 15.5m hogares frente a 15.3m; gasto $122 frente a $112; MVP 2.6m frente a 2.4m, con $522 por año y 72% de ventas. Los 15.9m hogares del panel Q2 usan otra ventana: no inferir una tasa de churn de la diferencia. Consumo medido Q3 +12.7% y volumen retail +14%; canales no medidos añadirían 1–2 puntos según dirección. Envios +10% soportan >2 puntos de comparación de club/4 de julio y 1–2 puntos adicionales por inventario del cliente creciendo menos que sus ventas. Son explicaciones de dirección, no auditoría de sell-through.

Hill’s lanzó refrigerado en especialidad en julio 2026; Blue Buffalo Love Made Fresh se lanzó nacionalmente en octubre 2025. Purina y Nom Nom también ofrecen formatos frescos/congelados. Las relaciones de veterinarios, marcas y capital de estos grupos son riesgos reales. Sus ventas comparables por producto y retorno incremental no están revelados. No asignar letras anónimas de competidores del deck a nombres sin evidencia. [Hill’s](https://www.hillspet.com/about-us/press-releases/hills-rolls-out-science-diet-refrigerated-dog-food), [Blue Buffalo](https://privacy.generalmills.com/news/press-releases/blue-buffalo-launches-love-made-fresh-nationwide-making-every-meal-a-fresh-act-of-love-for-your-dog), [Purina](https://www.purina.com/purina-one/fresh-entrees-dog-food), [Nom Nom](https://support.nomnomnow.com/hc/en-us/articles/360024602113-Where-to-Buy-Nom-Nom).

**Causa de caída:** no se ha demostrado una causa única de mercado. El cierre del 3 nov está por encima de $64.12 del 23 oct y FT muestra avance anual; estar en un escáner de pullback no prueba un nuevo desplome. Desaceleración de hogares, competencia, logística y necesidad de inversión son preocupaciones verificables del negocio, no causalidad demostrada de cada movimiento bursátil. La noticia del 4 nov no pudo causar el cierre del 3 nov. Tampoco se atribuye el movimiento a una supuesta salida del CEO: Billy Cyr sigue; el cambio es President/COO/advisor.

## 4. Historia completa y normalización comparable

Fuentes: [10-K FY25, publicado 23 feb 2026](https://www.sec.gov/Archives/edgar/data/1611647/000161164726000006/frpt-20251231.htm), [Q1 2026, 6 may](https://www.sec.gov/Archives/edgar/data/1611647/000161164726000012/frpt-20260331.htm), [Q2 2026, 5 ago](https://www.sec.gov/Archives/edgar/data/1611647/000161164726000018/frpt-20260630.htm), [Q3 2025, 3 nov 2025](https://www.sec.gov/Archives/edgar/data/1611647/000161164725000030/frpt-20250930.htm), [Q3 2024, 4 nov 2024](https://www.sec.gov/Archives/edgar/data/1611647/000161164724000019/frpt-20240930.htm), y comunicado Q3 2026 arriba. Los tres ejercicios son 2023–25; cuatro trimestres Q4’25–Q3’26. TTM = FY anterior + 9M actual − 9M anterior. CFO/capex/SBC trimestrales se calculan por diferencias acumuladas; EPS Q4 se obtiene del comunicado, **no** restando EPS anual menos 9M. Diferencias de $0.001m pueden surgir de redondeo.

'''+hist+'''
No se inventa EPS TTM multiplicando o sumando denominadores distintos. La suma indicativa de EPS trimestrales actuales es $2.69 básico/$2.52 diluido, no un EPS GAAP TTM recalculado con reglas de convertibles. La pérdida FY23 aún no permite tasas porcentuales estables desde base negativa. Crecimiento de ventas FY24 27.16%, FY25 13.01%, TTM actual 11.75%: el modelo reconoce desaceleración, no extrapola el pasado excepcional.

### Puente homogéneo de beneficio y caja

EBIT normalizado = EBIT GAAP + cargos específicos excluidos + SBC publicada − **3% de ventas** como SBC económica analítica constante. No se añade la SBC de nuevo al FCFF proyectado. El 3% no es guidance: se utiliza para evitar perpetuar las reversiones de 2025 y se tensiona en escenarios al 2.5%/4%.

Cargos FY25 retirados de EBIT: crédito de distribuidor $10.680m, asuntos legales $5.703m e internacional $1.273m = $17.656m. Son cargos concretos; no se retira toda SG&A. No se vuelve a cobrar ficticiamente la cuenta incobrable ni se añade $17.656m al CFO. FY23 otros gastos se conservan por prudencia. El cash FCF es CFO menos **todo** capex de caja; el diagnóstico propietario resta SBC económica, sin sustituirlo por FCFF operativo.

'''+norm+'''
TTM normalizado: EBIT $84.473m frente a $70.057m, +20.6%. Beneficio después de intereses netos y un impuesto estándar del 25%, retirando inversión y efectos fiscales extraordinarios: $60.993m frente a $49.070m, +24.3%; es métrica del analista, no EPS ajustado del emisor. Margen EBIT GAAP actual **8.76%**, normalizado 7.00%. El 17.283% que arrastra el escáner coincide aproximadamente con margen **neto** del viejo TTM junio ($203.474/$1,177.308), no margen operativo actual.

TTM CFO $200.622m frente a $155.824m (+28.8%); capex $133.309m frente a $153.398m; FCF caja $67.313m frente a $2.426m. Después de SBC económica constante, $31.124m frente a −$29.959m. Usando el mismo denominador económico actual de 48.8685m para aislar negocio, FCF caja por acción $1.38 frente a $0.05; después de SBC $0.64 frente a −$0.61. No son cifras históricas GAAP por acción.

El CFO incluye un **uso** de circulante TTM de $15.989m, frente a $28.384m anterior: parte de mejora de caja es menor absorción, no una liberación perpetua. Inventarios a septiembre $95.151m frente a $76.766m de diciembre; cuentas a cobrar $68.561m frente a $63.762m. En Q3 inventario usa $7.680m frente a liberación de $19.225m en Q3 anterior. Esto explica por qué margen mejor no implica CFO trimestral mejor.

Como puente FCFF histórico adicional: NOPAT normalizado + D&A − capex de caja − altas no monetarias de finance leases + variación de circulante publicada. FY23 −$222.190m, FY24 −$80.275m, FY25 −$40.645m; TTM anterior −$48.311m. TTM actual es **$10.725m menos L**, donde L son altas de finance leases no monetarias Q3 aún no desglosadas. No se sustituye L por cero. El diagnóstico de CFO/FCF de caja anterior sí es observado y completo. Una inversión económica adicional de $10m reduce un flujo cercano en aproximadamente $0.19 por acción a WACC central; no constituye una cota auditada de L. No se usa esta incertidumbre menor para simular una falta de historia o bloquear toda valoración.

SBC FY24 incluye $2.027m de warrants a proveedor y FY23 $5.160m; fueron servicios y terminaron de amortizarse en FY24. FY25 SBC $13.883m incluye Q4 negativo de $6.373m por reversiones de probabilidad de premios, no remuneración recurrente normal. En el modelo futuro SBC sí es coste económico y las compras futuras de acciones no son gratuitas.

## 5. Balance, reclamaciones y dilución sin doble cómputo

A 30 septiembre: caja $345.860m; convertible contable $399.007m, pero obligación principal **$402.5m**, cupón 3%, vence 1 abril 2028. Finance leases $28.539m. Operating leases $65.651m permanecen como alquiler en márgenes; no se restan otra vez como deuda. Reserva de caja operativa **$30m es hipótesis**, deja $315.860m excedentarios. No se añaden otra vez los $100m de venta de inversión ni las recompras ya ejecutadas. Recompras de caja 9M $102.304m, unas 1.8m acciones; sólo se reconocen las ya reflejadas en caja/acciones a septiembre.

La caja y futura generación reducen riesgo de vencimiento, pero no equivalen a capacidad ilimitada de recompras: principal excede caja total en $56.64m antes de reservas/leases. El modelo mantiene la obligación y supone refinanciación para la TIR ilustrativa, no presume que ésta esté contratada. El riesgo reside en coste y capacidad de financiar crecimiento/deuda si el negocio decepciona, no en insolvencia inmediata demostrada.

Acciones actuales publicadas: **48.329m**. Promedio básico Q3 48.426m, diluido GAAP 54.742m. Conversión bruta 5.776519m = $402.5m × 14.3516 acciones/$1,000. Una proxy de dilución ordinaria es 54.742 − 48.426 − 5.776519 = **0.539481m**; denominador económico 48.868481m. No se trata ese promedio como inventario exacto de premios al día.

Los capped calls comprados compensan la opción desde el strike inicial ~$69.68 hasta cap **$120.23** si se mantienen las condiciones y se liquida principal en caja. Modelo coherente: resta deuda principal, no añade simultáneamente las 5.7765m acciones brutas; valora sólo el residual por encima del cap como call de 5.7765m acciones. Black–Scholes simplificado, 513/365.25 años, Rf4.91%, volatilidad **asumida**45%, sin dividendos. Valor residual al precio de mercado $26.967m; a valor central $3.513m. Se resuelve implícitamente precio × acciones + opción residual = EV + caja excedentaria − deuda − finance leases. La volatilidad no es una observación de mercado y la operación supone contrapartes cumplidoras/hedge intacto; no valora en detalle cláusulas de make-whole ni terminación anticipada. La proxy de premios ordinarios puede solaparse parcialmente con gasto futuro de antiguos premios no consolidados; no hay inventario Q3 para cuantificarlo exactamente y la sensibilidad de acciones muestra su escala. No se añade una capa de dilución anual por los mismos pagos futuros.

Prueba de volatilidad30–60% y acciones ordinarias ±0.3m: central **$43.93–44.72**. La diferencia de liquidación física puede alterar acciones, pero deuda/valor de cobertura deben cambiar de forma consistente. No se resta principal y toda conversión a la vez. Se mantiene historial de opciones/RSU FY25/H1 y nueva retención de Baty 58,245 RSU (21 oct, vest junio2029) sin convertirla automáticamente en duplicado de gasto futuro; dilución máxima aislada alrededor de0.12%. Fuente [8-K 23 oct](https://investors.freshpet.com/node/14466/html). No es un cambio de CEO.

DTA neto actual $42.924m no se suma al equity. NOL federal FY25 $391.1m, de ellos $146.5m vencen2028–37 y $244.6m son indefinidos con límites; la venta de inversión ha consumido atributos. Límites Section382 y NOL actual no están cuantificados. Modelo beneficio fiscal futuro limitado **$25/35/40m** según escenario, impuesto normal25% y máximo80% de ahorro anual hasta agotarlo. Es reserva analítica, no declaración fiscal disponible. Sin ahorro fiscal, central $43.75. No confundir DTA contable con efectivo.

## 6. FCFF explícito a diez años

**FCFF = EBIT económico − impuesto de caja + D&A − inversión total − aumento de circulante.** EBIT ya descuenta SBC. No se vuelve a restar SBC después ni se añade como caja. Año1–10 son **años rodantes NTM1–NTM10**, anclados en TTM septiembre2026, no FY2027–2036. Primera venta central $1,342.370m equivale a +11.28% sobre TTM y +8.28% sobre centro de guía FY26; es una aproximación rodante, no previsión calendario precisa. Rebasar proporcionalmente al centro FY26 eleva central a $45.45, cambio pequeño.

Demanda se descompone como hogares × compra anual retail × factor de realización neta constante0.6379. Es una identidad de modelización calibrada a $1,206.299m/15.5m/$122, no precio contractual, medición de ingresos de todos los canales ni retorno de cohortes. El gasto mezcla volumen/participación de cartera/precio. No se suma MVP por separado. Central hogares +4% reduciéndose a1%; gasto +7% reduciéndose a2.5%. Esto ya exige recuperación de hogares desde el1% actual; no es un caso de inmovilidad.

EBITDA tipo guía central20.5% en año1,22% en2,23.5% en3,24.5% en4 y25% desde5. A ese margen se añade un puente **0.23634 puntos**: D&A total CFO TTM $96.668m menos D&A de conciliación EBITDA $93.817m = $2.851m. Permite restar luego D&A total sin duplicar su gasto. El puente se mantiene por ventas como hipótesis; no se asegura que todos los $2.851m sean un tipo de lease. Diferencias residuales de otras rentas/intereses significan que no se denomina conciliación exacta al EBITDA GAAP futuro. SBC central3%; D&A7.8% de ventas converge a6%; EBIT maduro16.236%. Adverso SBC4%, EBIT8.736%; favorable SBC2.5%, EBIT20.236%.

Capacidad: 16 líneas actuales y potencial24+ documentadas, mejoras desbloquean >$100m de capacidad de ingresos según dirección. **Capacidad inicial $1,500/1,600/1,650m, utilización82/85/88%, productividad de expansión2/3/3.5x y crecimiento nominal de capacidad1.5/2/2% son hipótesis, no datos revelados.** Q2 afirmaba capacidad para2026 y buena parte2027; justifica no comprar una planta nueva cada año, no capex cero. Expansión = déficit de capacidad para ventas/utilización dividido por productividad. Capex mayor que mantenimiento amplía capacidad; el modelo no paga expansión sin reconocer capacidad.

Mantenimiento central85/90/95% de D&A primeros tres años y100% después: hipótesis transitoria de base joven. Capex mínimo $140m/$130m en primeros dos años; favorable140/140; adverso150/140. Se incluyen fridges, tecnología, producción y reposición, sin un desglose GAAP inexistente. Δ WC =5% de incremento de ventas, no se perpetúa la liberación de caja. Desde años8–10 la reinversión converge al retorno sostenible, evitando que la expansión final sea gratuita. Terminal: NOPAT11 × (1 − g/ROIC), WACC > g. Con central, NOPAT11 $293.330m, reinversión$48.888m, FCFF11 $244.442m.

WACC central10.25%: [Fed H.15, edición3nov/observación2nov](https://www.federalreserve.gov/releases/h15/) Treasury10años4.91%; ERP4.5% y beta1.35 **supuestas** dan Ke10.985%; deuda12%, coste marginal6%, impuesto25% dan aproximadamente10.21%, redondeado10.25%. No usar el cupón viejo3% como coste de deuda perpetuo. Beta de proveedor cercana1.70 implicaría WACC~11.6%; se muestra11.5%. Beta1.35 no es estimación estadística validada y es una elección relativamente benigna frente al dato de proveedor. La tasa no se aumenta a escondidas por cada riesgo ya modelado en caja.

Terminal central g3%, ROIC18%; adverso2%/10%; favorable3.5%/22%. g nominalUSD está por debajo del coste de capital; retornos requieren marca/red/productividad y no están garantizados. Como control de exigencia, NOPAT TTM normalizado $63.355m sobre PP&E neto más circulante operativo corriente al cierre de aproximadamente $1,234.049m da sólo ~5.1%; es una proxy con saldo final, no ROIC auditado sobre capital medio. El objetivo terminal18% exige una mejora sustancial de utilización/márgenes, no una prolongación del retorno actual. El caso central invierte $1,513.960m en diez años y su NOPAT final sobre PP&E más circulante modelados se aproxima al retorno terminal. No se asume adquisición gratuita ni venta de negocio extraordinaria.

'''+years+'''
Central: EV **$2,287.453m** + caja345.860 − reserva30 − principal402.5 − finance leases28.539 − opción3.513 = equity común **$2,168.761m** /48.868481m = **$44.3795**. Cifras no redondeadas en código/JSON; todos los años de los tres escenarios en CSV.

## 7. Escenarios, retorno y expectativas del precio

'''+sc+'''
*La TIR del negocio descuenta FCFF y un valor de salida del año10 fijado con los parámetros de cada escenario contra el EV exigido hoy. No es CAGR garantizada de cotización. La TIR de accionista es una **proxy de distribución**: paga caja excedentaria al inicio, distribuye flujos menos intereses después de impuestos, refinancia deuda hasta el final y satisface opción residual estimada. Esa política no está anunciada y la prima de opción no equivale a un pago esperado determinista. Se muestra para ilustrar sensibilidad financiera; la principal lectura es caja del negocio. Resolver un WACC que también cambie el múltiplo terminal da ~7.82% en central, distinto del4.52% de salida fija; no confundir ambos conceptos de rentabilidad implícita.

### Alternativa que evita convertir el central en dogma

Añadir1.5 puntos anuales a cada motor hogares/gasto, mantener EBITDA inicial20.5% y llevarlo a27% al final, con SBC3% y D&A6%, produce crecimiento de ventas **9.97%**, $3,119.762m de ventas y EBIT18.236% en año10. A coste de capital10.25%/ROIC18%, vale **$58.92**. Con WACC9.5%/ROIC20%, vale **$68.34**, sólo1.81% bajo$69.60, TIR negocio9.27% y proxy accionista9.86%.

Esta trayectoria es plausible en una categoría que gana participación y no requiere crecimiento imposible; también exige recuperación y persistencia de hogares, mayor participación de cartera y ejecución de margen. Es evidencia de **precio casi razonable bajo un conjunto concreto de supuestos**, no permiso para promover retrospectivamente esos supuestos a centrales. El actual1% de hogares y advertencia de inflación limitan la confianza. Una entrada parcial puede ser válida bajo el plan cuando esa combinación esté respaldada; el tamaño pequeño por sí solo no crea valor.

### Inversa conjunta con el mismo modelo

Se desplaza crecimiento de hogares/gasto y se aumenta margen gradualmente desde cero en año1 hasta el cambio completo en año10. No se obliga a saltar de inmediato por encima de la guía2027. Capex, circulante, impuestos, claims y reinversión siguen idéntica lógica. Todas las filas igualan$69.60.

'''+reverse+'''
Con WACC10.25%, el precio pide14.60% CAGR si EBIT final16.24%,12.76% si18.24% o11.16% si20.24%. Con9.5%/20.24% basta9.03%. No hay una expectativa implícita única. Comparar estos crecimientos con10% envíos/12.7% consumo recientes y una década completa, no sólo con el mejor trimestre.

### Sensibilidades conjuntas

En la siguiente matriz, +2 puntos significa +1 punto en hogares y +1 en compra cada año; no equivale exactamente a+2 puntos de CAGR por composición. Los cambios de margen se implementan gradualmente.

'''+joint+'''
Sensibilidad WACC y crecimiento terminal, operación central:

'''+discount+'''
Otros cambios aislados:

'''+sens+'''
Retorno del negocio central según precio, **sin** un recorte universal adicional:

'''+pricegrid+'''
A$45 el caso central aproxima10.07% anual; a$55,7.47%; a$60,6.37%; a$69.60,4.52%. El resultado refleja supuestos y salida fija, no un umbral obligatorio. Margen de seguridad frente al central = (44.38 − 69.60)/44.38 = −56.8%; no confundirlo con el potencial frente al precio de −36.2%. Frente a la alternativa de $68.34, el margen es aproximadamente −1.85%. El máximo fundamental no se calcula como “central×0.85” por defecto. Zona de **revisión**, no orden: alrededor de$44–45 si se mantiene el caso central; hasta~$59 si nueva evidencia permite adoptar la alternativa operativa a coste de capital central. Cerca de$68–70 requiere además el conjunto más favorable de coste/retornos o márgenes. No elevar esos límites porque suba la cotización.

## 8. Comparables actuales y límites de homogeneidad

Precios cierre3nov2026; estados últimos publicados. CL incluye Hill’s pero también higiene/consumo; GIS incluye Blue Buffalo pero gran negocio humano; CHWY es minorista. Son **contrastes**, no pares puros fresh. Rentas operativas permanecen en EBIT y se excluyen pasivos operativos del EV; equity común de fechas indicadas, sin fingir inventario de opciones al cierre.

'''+comps+'''
Los EV de esta tabla son la aproximación explícita market cap + deuda financiera − caja + NCI de libro ($352m CL y $13.4m GIS). Los NCI son proxies contables, no valores de mercado. CL/GIS ya incluyen finance leases en deuda; no se añaden otra vez $72m/$0.4m antiguos. CHWY no presenta NCI ni preferentes, pero su finance lease actual no está cuantificado; históricamente inmaterial no significa cero. Se conserva esta limitación y la de premios ordinarios. No se promedian para fabricar un valor. CL acciones794.920513m de30sep; GIS534.687144m de16sep; CHWY401.927249m de2sep. Deuda/caja se fecha con el periodo financiero, no con el precio.

CL: EBIT GAAP3,161 incluye919 de impairment. Extremo conservador de normalización4,080 retira sólo ese deterioro;4,503 adopta además los ajustes del emisor, incluidos reestructuración/ERISA con consecuencias reales. GIS: GAAP−206.4 no sirve como múltiplo significativo. Retirar impairments1,802.9, valoración held-for-sale1,055.5, neto de desinversión5.0 y retirar MTM86.4/inversión7.4 da2,563.2 conservando reestructuración137.4 y transacción/integración33.6; endpoint emisor2,734.3, con redondeo0.1. Su TTM tiene53semanas y no se inventa ajuste proforma para venta futura de Brasil. CHWY EBIT328.2 retiene SBC297.9 y es margen de retail, no fabricante.

Fuentes CL [10-Q30sep](https://www.sec.gov/Archives/edgar/data/21665/000002166526000048/cl-20260930.htm)/[10-K25](https://www.sec.gov/Archives/edgar/data/21665/000002166526000006/cl-20251231.htm)/[release30oct](https://investor.colgatepalmolive.com/news-releases/news-release-details/colgate-palmolive-announces-3rd-quarter-2026-results); GIS [10-K26,1jul](https://www.sec.gov/Archives/edgar/data/40704/000162828026046466/gis-20260531.htm)/[10-Q30ago,23sep](https://www.sec.gov/Archives/edgar/data/40704/000162828026063201/gis-20260830.htm); CHWY [10-Q2ago,9sep](https://www.sec.gov/Archives/edgar/data/1766502/000162828026061018/chwy-20260802.htm)/[10-K,25mar](https://www.sec.gov/Archives/edgar/data/1766502/000176650226000034/chwy-20260201.htm). Precios [CL](https://stockanalysis.com/stocks/cl/history/), [GIS](https://stockanalysis.com/stocks/gis/history/), [CHWY](https://stockanalysis.com/stocks/chwy/history/).

FRPT a$69.60 con claims económicos: EV~$3,543.39m, ventas2.94x, EBIT normalizadoTTM41.95x; beneficio normalizado~$60.99m implica P/E~55.8x usando acciones económicas, no el PE del scanner basado en beneficio extraordinario viejo. Cash FCF después de SBC normalizada rinde~0.92%. La prima frente a fabricantes maduros puede justificarse por crecimiento, pero requiere convertirlo en caja. CHWY~27x EBIT tiene economía distinta y tampoco valida automáticamente40x.

Como contraste de múltiplos **no sustitutivo**, un intervalo12–27x EBIT NTM central$133.38m abarca aproximadamente$30–71 por acción tras los mismos claims. El extremo27x requiere prima de crecimiento y no se adopta como valor central. Aplicarlo al EBIT TTM más bajo daría valores menores; esa diferencia demuestra cuánto depende el argumento de mejora futura. No se selecciona el mayor método porque se acerque al precio ni se ofrece un múltiplo histórico inventado sobre EPS contaminados.

## 9. Riesgos, falsación y Stage 3.5 separado

**Riesgos con impacto en modelo:** hogares no recuperan, gasto por hogar se enfría, rivales reducen velocidad/precio, logística/medios capturan el ahorro fabril, tecnología exige más capex o llega tarde, grandes clientes reajustan inventario, seguridad alimentaria/recall, márgenes no sostienen inflación, deuda2028 y cobertura dilutiva, compensación normal superior3%. El adverso no es pérdida máxima; una crisis de producto/financiación puede ser peor.

**Qué mejora tesis/precio:** consumo y nuevos hogares se sostienen de manera comparable; evidencia de márgenes2027 hacia20–21% pese a costes, ahorros tecnológicos netos de inversión, capacidad operativa y rentabilidad incremental medibles, cash conversion tras capex normal, no sólo deferral. **Qué la invalida:** varios periodos de deterioro de volumen/retención sin explicación temporal verificable, incremento persistente de inventario/impagados, retorno sobre nueva capacidad insuficiente o necesidad financiera/dilución no resuelta.

Próximo evento: conferencia4nov08:00EST/13:00UTC, futura al corte; después notas del10-Q. Preguntas prioritarias: panelhogares1%; calendario de inventario del cliente; alcance/coste de100bp tecnológicos; capex2027 y mantenimiento; inflación/precios/elasticidad; lease del nuevo DC Bethlehem; inventario de premios y cash taxes/NOL. No se afirma haber oído respuestas que todavía no existen.

**Stage3 está investigado; Stage3.5 no está aprobado.** Faltan precio posterior al evento, estructura/EMA50 vigente, señal numérica y temporalidad elegidas antes de ejecutarla, soporteM y stopS, patrimonio/riesgo/capital de campaña, cantidad, vigencia y cancelaciones. No son huecos del DCF ni excusa para llamar “incompleto” a todo el análisis. No se inventan niveles técnicos con cierres desfasados. Ninguna compra, venta, orden ni cambio de stop deriva de este informe.

## 10. Controles, diferencias de fuente y trazabilidad

1. Comentarios preparados p6 dicen beneficio neto$27.9m; estado financiero$29.712m y deck$29.7m. Se utiliza estado, no promedio.
2. Logística anterior5.5% en comentarios vs subida170bp del deck hacia7.1% (implica5.4%): diferencia de redondeo/fuente preservada.
3. Tres líneas tecnológicas ya instaladas en comentarios vs nota del deck “instaladas a final2027”: alcance/tiempo sin aclaración. No se presupone todo100bp adicional a35bp ya previstos2026.
4. CFO D&A distinto de conciliación EBITDA; corregido puente2.851m en modelo. Auditoría independiente reproduce cifras. Antes de corrección central43.63, después44.38; cambio+$0.75 no cambia decisión. No se conserva cifra antigua como valor vigente.
5. No hay aún notas Q3 de nuevos leases, premios completos, NOL o impuesto de caja. Se conservan fechas, proxy de claims y sensibilidades en lugar de números inventados. Los estados publicados permiten cerrar investigación y valoración a este corte; revisión posterior no equivale a tener conclusiones futuras.
6. No se utiliza la guía del emisor como consenso ni un consenso no verificado. Las estimaciones de capacidad, gasto, SBC, WACC, ROIC y fiscalidad se identifican como propias.

Paquete reproducible: `model.py` y `model_results.json`, tres CSV de10años, `history.json/csv`, reconstrucción `build_post_history.py` y base de51comprobaciones históricas, fuentes brutas SEC/IR, archivos de hechos operativos, peer bridges y auditoría independiente. `python model.py`, `python build_comps.py` y `python build_report.py` regeneran valoración, contraste y este informe usando datos preservados. Los escenarios no son probabilidades, objetivos garantizados ni autorización para operar.
'''
# Standard human-readable spacing for common compact draft tokens.
replacements={'a$':'a $','A$':'A $','cerca de$':'cerca de $','de$':'de $','hasta~$':'hasta ~$','margen~':'margen ~','EV~':'EV ~','TTM41':'TTM 41','TTM$':'TTM $','P/E~':'P/E ~','rinde~':'rinde ~','CHWY~':'CHWY ~','Stage3':'Stage 3','Stage 3.5':'Stage 3.5','10años':'10 años','51comprobaciones':'51 comprobaciones','panelhogares':'panel hogares'}
for a,b in replacements.items():s=s.replace(a,b)
import re
# Separate numbers from units/nearby prose; leave URLs and code-file names unchanged.
lines=[]
for line in s.splitlines():
 if 'https://' not in line and '`' not in line:
  line=re.sub(r'(?<=\d)(?=(?:puntos|punto|años|año|semanas|meses|acciones|hogares|líneas|comparaciones|comprobaciones|EST|UTC|bp)\b)', ' ', line)
  line=re.sub(r'(?<=[a-záéíóúñ])(?=(?:20[2-3][0-9])\b)', ' ', line)
  line=re.sub(r'(?<=[a-záéíóúñ])(?=\$)', ' ', line)
 lines.append(line)
s='\n'.join(lines)+'\n'
# Protect URLs and code identifiers, then ensure ordinary prose has normal spacing.
protected=[]
def keep(match):
 protected.append(match.group(0));return 'ZZPROTECTED'+str(len(protected)-1)+'ZZ'
s=re.sub(r'https?://[^\s)]+|`[^`]+`',keep,s)
s=re.sub(r'(?<=[a-záéíóúñ])(?=\d)', ' ', s)
s=re.sub(r'(?<=\d)(?=[a-záéíóúñ])', ' ', s)
s=s.replace('soporteM','soporte M').replace('stopS','stop S').replace('Section382','Section 382').replace('80%de','80% de')
s=s.replace('$55,7.47%', '$55, 7.47%').replace('$60,6.37%', '$60, 6.37%').replace('$69.60,4.52%', '$69.60, 4.52%')
for i,v in enumerate(protected):s=s.replace('ZZPROTECTED'+str(i)+'ZZ',v)

(P/'FRPT_full_stage3_2026-11-04.md').write_text(s)
print('report',len(s.split()),'words')
