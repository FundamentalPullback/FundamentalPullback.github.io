from pathlib import Path
import json
P=Path(__file__).resolve().parent;h=json.loads((P/'history/periods.json').read_text());r=json.loads((P/'model/results.json').read_text());c=json.loads((P/'capital/inputs.json').read_text())
fmt=lambda n:f'{n:,.2f}'
s='''# PAYC — Paycom: mejora operativa, caja fiscal y recompras financiadas

**Corte informativo: 7 de noviembre de 2026; mercado: sesión del 6 de noviembre. Investigación parcial condicionada, revisada independientemente. No es Stage 3 integral ni aprobación de entrada.**

## Conclusión

Paycom merece seguimiento por crecimiento recurrente y recuperación del beneficio operativo. Sin embargo, la expansión del flujo de caja combina cambios fiscales, menor inversión y menores costes de personal/desarrollo. Las recompras han reducido fuertemente el denominador del beneficio por acción mientras la empresa ha pasado a deuda neta. Un múltiplo de FCF bruto o el crecimiento del EPS no bastan para justificar una compra.

El modelo de este dossier es un ejercicio operativo de diez años con inversión financiada y capital limitado. Sus casos no son una tasación integral certificada: siguen pendientes la conciliación actual de capital/dilución, restricciones de caja del banco fiduciario y comparables de valoración homogéneos. Los campos públicos de valor total y escenarios totales deben permanecer nulos. Opportunity90 satisface el mínimo65 solicitado, pero no demuestra elegibilidad técnica ni valor intrínseco.

## Precio y calendario: no mezclar sesiones

La fila del escáner del 6 de noviembre contiene Last223,7803, QP80, Opportunity90 y RSI41,0; Stage2 está ausente. Se conserva literalmente. El cierre regular fue237,32USD a las16:00EST, corroborado por StockAnalysis e Investing. Investing identifica223,78 como cotización posterior al cierre; StockAnalysis presenta otra observación extendida235,00 a las19:46. No se conoce el instante exacto del dato del escáner y no se presenta como cierre regular ni se certifica como última cotización extendida. Los inversos prueban ambos precios, sin atribuir las diferencias a una división de acciones.

Fuentes: https://stockanalysis.com/stocks/payc/history/ y https://www.investing.com/equities/paycom-soft-historical-data .

Los resultados Q3 se publicaron el4nov y el10-Q el5nov. El siguiente anuncio trimestral no ha quedado confirmado por una fuente primaria. El dividendo anunciado el2nov es0,375USD por acción, registro23nov y pago7dic: es un evento de capital, no fecha de resultados. No se libera el filtro de calendario ni ningún requisito técnico con estos datos.

## Negocio y evidencia reciente

La plataforma integra nómina y recursos humanos en una base de datos SaaS. El10-K informa aproximadamente39.200clientes y retención anual de ingresos91% en2025 frente90% en2024; no se interpreta como net revenue retention ni como garantía de crecimiento. La relación contractual estimada de diez años sustenta amortización de costes de adquisición/implementación y reconocimiento de ciertas tarifas diferidas. Una pérdida de clientes afecta esa recuperación y puede exigir deterioros; acelerar amortización contable no equivale por sí solo a una nueva salida de caja.

En Q3 los ingresos recurrentes y otros aumentaron de466,5M a519,3M, mientras el interés de fondos de clientes bajó de26,8M a24,5M. Ingresos totales543,8M, EBIT195,8M y neto133,2M frente493,3M/112,6M/110,7M. El aumento del EBIT es real en los estados publicados, pero incluye una base de costes reducida. Las acciones diluidas medias bajaron de56,4M a44,5M; por eso el crecimiento del EPS no es equivalente al del beneficio total.

Fuentes: https://www.sec.gov/Archives/edgar/data/1590955/000119312526449828/payc-20260930.htm y https://www.sec.gov/Archives/edgar/data/1590955/000119312526059372/payc-20251231.htm .

## Historia comparable: millones USD

TTM y Q4 se calculan con flujos aditivos, no son métricas TTM publicadas expresamente por el emisor. Los trimestres derivados pueden diferir0,1M de las columnas trimestrales por redondeo. El fichero history/history.csv conserva el detalle.

|Periodo|Ingresos|EBIT|Neto|CFO|PPE caja|CFO−PPE|SBC en CF|
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for n in ['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025','TTM2026']:
 d=h[n];s+='|'+n+'|'+'|'.join(fmt(d[k])for k in ['revenue','ebit','net_income','cfo','ppe_cash','cfo_less_ppe','sbc_expense'])+'|\n'
s+='''
El EBIT2024 de634,3M contiene una reversión de117,5M de remuneración del CEO. Sin ese beneficio aislado sería516,8M, no634,3M. No se extrapola el SBC neto negativo2024 como subvención recurrente. La reversión queda fuera de ambos TTM comparados por la combinación de períodos; no se resta nuevamente de TTM2025.

El TTM actual muestra ingresos2191,1M frente2001,3M y EBIT731,6M frente558,6M. Pero el CFO810,0M frente643,2M incluye impuestos/circulante y diferencias temporales. CFO menos PPE659,1M frente394,4M no es owner FCF normalizado: excluye compras de intangibles separadas, capitalización no monetaria, coste económico de remuneración y normalización de impuestos/circulante. Los4,5M de intangibles comprados enFY2025 no se ignoran como si fueran inexistentes; el modelo usa un suelo de recursos de capital agregado en lugar de perpetuar ese subtotal de caja.

Fuentes adicionales de historia: https://www.sec.gov/Archives/edgar/data/1590955/000119312525269543/payc-20250930.htm ; https://www.sec.gov/Archives/edgar/data/1590955/000119312526211926/payc-20260331.htm ; https://www.sec.gov/Archives/edgar/data/1590955/000119312526338010/payc-20260630.htm .

## Normalización que cambia la lectura

En nueve meses el CFO sube131,1M. La línea de variación de impuestos pasa de−65,4M a+65,6M: diferencia131,0M. Esto no significa que todo el beneficio operativo sea ficticio, sino que casi todo el incremento de CFO queda explicado aritméticamente por esa línea mientras otras variaciones se compensan. Las compras de PPE caen de197,4M a77,4M, otros120M de mejora del subtotal CFO−PPE. No se capitaliza esa combinación como crecimiento perpetuo de caja.

El gasto más desarrollo capitalizado cae de325,4M a209,5M en9M; enQ3 de117,6M a55,9M. El10-Q atribuye parte de los menores costes a empleados y plantilla. El ahorro puede ser durable, pero también exige probar capacidad de innovación/servicio. El modelo mantiene SBC en EBIT y añade sensibilidades de50M/100M de costes recurrentes adicionales, sin afirmar que esos importes sean un gasto inevitable identificado.

La vida de servidores/equipos de red aumentó de3 a6años desdejulio2025; la empresa califica de inmaterial el efecto9M2026. No se inventa un ajuste de gran tamaño. Los beneficios por cambios del contrato de naming rights,9M en2026 y35,6M en2025, están fuera del EBIT: no se descuentan otra vez del ancla operativa.

Los costes de contratos capitalizados9M suman154,2M y su amortización125,7M; activo final1045,4M. El CFO ya incorpora la inversión neta, por lo que restar154,2M otra vez sin devolver amortización duplicaría el coste. En el FCFF se conserva la amortización dentro de EBIT y se financia el aumento del activo de contratos como inversión neta adicional.

El SBC de la conciliación de caja es52M en9M, con2,6M adicional capitalizado en software; no es idéntico a48,1M en la evolución de patrimonio. El modelo no presume haber conciliado todas las capas históricas: retiene el gasto en el margen, usa inversión de reposición que incluye recursos no monetarios y declara el denominador de premios como proxy, no cifra diluida certificada.

## Fondos de clientes y puente de capital limitado

Los3891,3M de activos de clientes tienen una obligación igual y quedan fuera de caja accionista. Paycom National Trust Bank y el trust consolidado no convierten ese principal en efectivo disponible para recompras. El interés sí forma parte de ingresos operativos y se estresa por separado. El saldo medio diario9M fue aproximadamente2900M frente2700M; no se utiliza el saldo puntual3891,3M para fabricar una renta anual.

La caja corporativa publicada es193,9M y la deuda750M a30sept. Los900M de financiación y150M de amortización acompañan1390,9M de recompras9M. La facilidad no utilizada no es caja. El vencimiento del revolver es23abril2031 y la compañía reporta cumplimiento de sus covenants a30sept; no se certifica liquidez futura sin condiciones.

Se seleccionan100M de reserva operativa,5M de reserva fiscal histórica (UTB publicado3,5M a31dic2025, no saldo actualizado) y17M para el dividendo anunciado. El puente ilustrativo es193,9−100−750−5−17=−678,1M. La reserva100M no prueba cuánto capital del banco es distribuible. El DTL307,1M no se resta mecánicamente además de impuestos recurrentes; la realización fiscal de software/contratos no está conciliada completamente y se prueba un rango de tipos.

El cover informa45,034789M de acciones a27oct, incluidas0,727631M restringidas. No se vuelven a sumar estas últimas. Se añaden como proxy bruto0,1791M RSU y0,1347M PSU objetivo de septiembre:45,348589M. No es el treasury-stock method ni una conciliación de entregas, forfeitures, objetivos y retenciones hasta6nov. También se prueba2,5%/5% de dilución adicional. Los109,8M de remuneración no reconocida no se deducen como deuda y a la vez como coste futuro; siguen siendo un riesgo de margen/dilución.

Las obligaciones de arrendamientos operativos no se restan de nuevo como deuda porque se mantiene renta en costes y terminal. Ninguna de estas decisiones elimina sus compromisos reales. Fuente del dividendo: https://www.sec.gov/Archives/edgar/data/1590955/000119312526443880/payc-20261102.htm .

## FCFF ilustrativo financiado, no precio objetivo certificado

Año1=2027 y año10=2036, flujos al cierre anual descontados desde6nov2026 (primer período1+55/365años). No se agrega un stub de noviembre/diciembre2026: es un alcance incompleto, no un argumento para calificar automáticamente toda la valoración de conservadora.

Se parte de ingresos recurrentes TTM2085,6M e interés105,5M. El margen recurrente es una separación analítica: se asigna a ese negocio todo el coste operativo y se suma el interés como contribución incremental. No es un segmento publicado ni un margen neto de costes de banca auditado. Su factor0,70/0,90/1,10 cambia el nivel de interés y posteriormente crece con el volumen; no es predicción de tipos.

El impuesto de28% es seleccionado frente a28,9%9M. No se introduce amortización adquirida con escudo fiscal inventado. Se conserva el EBIT después de amortización y remuneración. El crecimiento y la mejora de margen se financian con el mayor entre: a) incremento positivo de NOPAT dividido porROIC; b) recursos brutos de capital10% de ingresos menos D&A9%, más aumento de contratos a48% de ventas recurrentes incrementales y circulante al2% de ventas incrementales. No se libera capital automáticamente cuando cae NOPAT. El suelo bruto es una proxy de reposición/software/intangibles, incluido trabajo capitalizado pagado con acciones, no una reconciliación de capex contractual. En terminal se mantienen ambos suelos y la renta; no desaparece la inversión de software por arte de una fórmula. La reinversión económica terminal usa NOPAT del año11 × g / ROIC, convención prospectiva de estado estable del plan, distinta del incremento realizado de NOPAT en los años explícitos. No se oculta ese cambio de convención ni se libera inversión para elevar el resultado.

Los descuentos11,5%/10%/9% son tasas de exigencia seleccionadas, con sensibilidad8,5–13%; no se presentan como CAPM/WACC calibrado con beta y ERP actuales. Esto deja abierto el requisito formal de coste de capital del plan. No debe confundirse un caso favorable con probabilidad de resultado.

|Caso|Crecimiento recurrente inicial→final|Margen recurrente inicial→final|ROIC|Descuento/g terminal|Residual ilustrativo USD/acción|PV terminal/EV|
|---|---|---|---:|---|---:|---:|
'''
for k,v in r['cases'].items():
 a=v['assumptions'];s+=f"|{k}|{a['growthStart']:.1%}→{a['growthEnd']:.1%}|{a['coreMarginStart']:.1%}→{a['coreMarginEnd']:.1%}|{a['roic']:.1%}|{a['discount']:.1%}/{a['terminalGrowth']:.1%}|{v['illustrativePerShare']:.2f}|{v['terminalShareOfEV']:.1%}|\n"
s+='\nLos valores anteriores son residuos condicionados del ejercicio, no valor total certificado. La banda no representa un intervalo probabilístico ni recomendación.\n\n### Senda central, millones\n\n|Año|Ingresos|EBIT|NOPAT|D&A|Recursos brutos|Δcontratos|ΔWC|Inversión neta seleccionada|FCFF|\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for z in r['cases']['base']['years']:s+='|'+str(z['year'])+'|'+'|'.join(fmt(z[k])for k in ['totalRevenue','ebit','nopat','da','grossCapitalResources','netContractInvestment','otherWCInvestment','selectedNetInvestment','fcff'])+'|\n'
s+='\n### Sensibilidades y exigencia implícita\n\n'
for key in ['reinvestment','float','rndRestoration','capital','dilution','tax','contractCapital','stub']:
 vals=r['sensitivities'][key];s+=f"- {key}: resultados entre{min(v['result']for v in vals):.2f} y{max(v['result']for v in vals):.2f}USD/acción; parámetros exactos en model/results.json.\n"
s+='''
En el inverso central,237,32 exige crecimiento recurrente inicial21,64% que desciende a3% en el año10, conservando el resto de supuestos; el precio del escáner exige19,90%. No son tasas perpetuas. Alternativamente, manteniendo el crecimiento central, el margen recurrente final tendría que acercarse a66,62% para237,32 o61,30% para223,7803. Se financia también esa mejora de NOPAT. Cada raíz comprueba bracket, residual y mil intervalos monótonos; no se presenta como previsión plausible por haber encontrado una raíz.

## Pares: contraste operativo, no valoración relativa cerrada

PAYX Q1FY2027 (31ago) publica ingresos1630,5M frente1540,0M y EBIT619,2M frente541,9M, con interés de clientes49,8M frente47,6M. PAYC tiene crecimiento de ingresos mayor y recuperación de EBIT más fuerte, pero Paychex incluye Paycor/PEO, tiene otra mezcla y distintos costes de adquisición. Su margen ajustado42% no sustituye margen GAAP.

ADP Q1FY2027 (30sept) registra ingresos5490,7M frente5175,2M e interés de clientes329,3M frente286,8M. Su beneficio antes de impuestos1454,9M no se reetiqueta EBIT comparable: tiene PEO con importes repercutidos y estrategia de financiación/inversión del float distinta. Este contraste demuestra que la sensibilidad de tipos y la mezcla importan; no permite trasplantar una mediana de múltiplos. Quedan pendientes EV, capital y denominadores normalizados contemporáneos de los pares; por ello no se declara completo el contraste relativo exigido por el plan.

Fuentes primarias: https://www.sec.gov/Archives/edgar/data/723531/000072353126000004/payx-ex99_1.htm y https://www.sec.gov/Archives/edgar/data/8670/000000867026000033/q1fy27exhibit99.htm .

## Qué confirmaría o debilitaría la tesis

Confirmaría: crecimiento de clientes/ventas recurrentes que se mantenga sin depender de recompras, margen acompañado por inversión suficiente en producto y servicio, conversión de caja después de un ciclo fiscal completo y reducción financiada de deuda. Debilitaría: deterioro de retención, necesidad de restaurar gasto que reduzca sustancialmente margen, menor ingreso de float no compensado, dilución o compromisos que absorban la caja aparente. Ninguna condición se declara ya cumplida por el Opportunity Score.

Para concluir Stage3 faltan coste de capital calibrado, pares relativos normalizados, conciliación actual de capital/SBC y recursos de inversión más detallados. Para una eventual entrada, además, faltan calendario confirmado y gates técnicos actuales. El RSI41 no es un veto autónomo del plan ni la restricción65 del usuario: esta se refiere a Opportunity Score. No se ha operado ni cambiado cartera.

## Reproducción y alcance

Ejecutar python reproduce.py regenera historia, modelo, comparables, informe y pruebas desde inputs factuales empaquetados, sin descargar filings. Los originales SEC permanecen fuera del paquete público; se entregan sólo datos derivados y enlaces. Las comprobaciones prueban aritmética y consistencia, no convierten hipótesis en hechos ni sustituyen una auditoría independiente.
'''
import re
s=re.sub(r'(\d)(M|USD|años|clientes)\b',r'\1 \2',s)
s=re.sub(r'\b(de|el|a|en|por|entre|frente|hasta|supera|son|impuesto)(?=\d)',r'\1 ',s)
s=s.replace('rndRestoration','Restauración de gasto').replace('reinvestment:','Reinversión:').replace('float:','Interés de clientes:').replace('capital:','Puente de capital:').replace('dilution:','Dilución:').replace('tax:','Impuesto:').replace('contractCapital:','Capital de contratos:').replace('stub:','Calendario de descuento:')
(P/'report.md').write_text(s)
