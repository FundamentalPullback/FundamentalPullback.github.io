from pathlib import Path
import json
P=Path(__file__).parent;F=json.load(open(P/'financials.json'));M=json.load(open(P/'model.json'));U=json.load(open(P/'sources/urls.json'));U.update(price='https://stockanalysis.com/stocks/alle/history/',price_check='https://www.financecharts.com/stocks/ALLE',rf='https://www.federalreserve.gov/releases/h15/',assa='https://www.assaabloy.com/group/en/news-media/press-releases/id.30333d833dbf65af',assa_report='https://attachment.news.eu.nasdaq.com/a9743fcc69444ffddcd5a4e09100fe70b',assa_price='https://stockanalysis.com/quote/sto/ASSA.B/history/',calendar='https://investor.allegion.com/financial-information/results-center/2026')
json.dump(U,open(P/'sources.json','w'),indent=2)
def cite(*keys):return '\n\nFuentes: '+', '.join(f'[{k}]({U[k]})' for k in keys)+'.\n\n'
def tab(h,rows):return '| '+' | '.join(h)+' |\n| '+' | '.join(['---']*len(h))+' |\n'+''.join('| '+' | '.join(str(x) for x in r)+' |\n' for r in rows)+'\n'
def hist(k):return tab(['Periodo','Ventas','EBIT','Neto','EPS','CFO','Capex','FCF','SBC','FCF−SBC'],[[d['period']]+[f'{d[x]:,.2f}' for x in ['revenue','ebit','net_income','eps','cfo','capex','fcf','sbc','fcf_less_sbc']] for d in F[k]])
s='''# ALLE: recuperación confirmada, valoración todavía condicionada

**Allegion plc · NYSE · USD · 4 noviembre 2026. Cierre evaluado: 189,35 USD del 3 noviembre, 16:00 EST. Corte de investigación: 4 noviembre, 15:43 UTC.** No se usa una cotización intradía como cierre.

## Decisión

**Esperar precio o evidencia que sostenga una valoración superior.** La recuperación operativa continúa después de excluir la devolución arancelaria. El nuevo FCFF de diez años da **136,09 USD central**, **80,29 adverso** y **238,52 favorable**. El cierre no queda respaldado por el central. Que esté dentro del abanico total no convierte el favorable en base ni autoriza comprar.

Este trabajo cierra la espera antigua de resultados del 22 octubre y reconstruye historia, caja y una valoración canónica. Se presenta como **investigación completa sobre la información disponible, con reservas explícitas de claims y proyección**. No equivale a una certificación transaccional del balance de noviembre ni a Stage3.5. No hay techo de compra, stop, cantidad ni orden. No se conserva como regla el antiguo descuento obligatorio de15%.

La discrepancia antigua se preserva: A004 valoraba con EPS/PER a177 USD; A064 comprobaba FCFF de cinco años con central112. Se reproduce A064 a112,20349 antes de modificar método/datos. No se promedian ambas cifras ni se atribuye todo el cambio a mejora del negocio.
'''+cite('q3','q10','price','price_check')+'''## 1. Calidad del negocio y recuperación

Allegion vende cerraduras, controles de acceso, puertas y dispositivos de salida, con marcas como Schlage, LCN y Von Duprin. Instalación existente, especificación técnica y distribución apoyan repetición y sustitución. No se cuantifica aquí una cuota de mercado ni se confunde seguridad física con demanda inmune al ciclo.

Q3 crecimiento orgánico7,2%, separado del2,6% de adquisiciones/divestitures y−0,2% de divisas. Americas crece orgánico9,1%; no residencial sube a ritmo de doble dígito bajo, residencial de dígito medio principalmente por precio. International cae orgánico0,2%. La mejora no es uniformemente global. La dirección elevó guía FY2026: ingresos+9,5–10,5%, orgánico+5–6%, EPS GAAP8,35–8,40 y ajustado9,05–9,10.

El precio avanzó de159,00 al cierre previo a resultados a176,52 el22oct y189,35 el3nov (+19,09% desde21oct). No es la misma oportunidad de precio del expediente anterior. El calendario de publicación y el movimiento coinciden, pero no prueban que cada cambio bursátil tenga una única causa.
'''+cite('q3','price')+'''## 2. Historia reconciliada: 3FY, 4Q y TTM

Millones de USD excepto EPS. Años naturales. TTM al30septiembre. Q4=FY−9M; flujosQ2/Q3=acumulado−anterior. EPS por suma/diferencia es aproximación al periodo entero; no se fuerza una identidad con un único promedio de acciones. FY2023 neto atribuible540,4 frente a neto total540,6 por minoritarios; los periodos siguientes no tienen una diferencia material.

### Tres ejercicios
'''+hist('annual')+'''### Cuatro trimestres más recientes
'''+hist('quarters')+'''### TTM comparable
'''+hist('ttm')+'''
Ventas TTM+10,33%; EBIT+13,15%; beneficio neto+7,92%; FCF+8,79%; FCF−SBC+9,07%. El margen EBIT contable pasa de20,97% a21,50%. La caja confirma progreso, aunque crece menos que las ventas y el beneficio operativo.

Las cifras se extraen del emisor, no del margen de un screener. FY2025 EBIT859,5 M$, no873,1 de una serie estandarizada histórica; CFO783,8 y capex98,1. El TTM actual es FY2025 +9M2026−9M2025. Los archivos de soporte conservan los datos y el procedimiento.
'''+cite('k25','priorq3','q1','q2','q10')+'''## 3. Qué parte del beneficio es sostenible

**Devolución arancelaria.** Q3/9M2026 EBIT incluye19,9 M$ de IEEPA y otros ingresos incluyen0,9 M$ de intereses relacionados. El comunicado distingue importe recibido y esperado, sin desglosar cuánto estaba ya cobrado. No se capitaliza repetidamente ni se presume que todo fuera caja. Al excluir19,9 del EBIT, Q3 pasa a264,7 M$, margen22,57% y crecimiento13,22% frente a233,8. TTM EBIT pasa a924,3, margen21,05% y crecimiento10,76%. La recuperación sigue siendo real, pero menor que el+21,7% de EBITQ3 reportado.

**Otros ingresos e impuestos.** Q3 incluye ganancia no operativa de4,1 M$. La tasaGAAP17,5% compara con9,8%, no con una tasa sostenible igual. Para un chequeo de neto se resta de691,1 M$ TTM el beneficio de19,9+0,9+4,1 al82,5%: neto ilustrativo670,56 M$. No es un estado auditado ni normalización completa de todos los impuestos. El DCF evita este problema partiendo deEBIT, con20% de impuesto normalizado frente a guía ajustada18–19%; no perpetúa una tasa mínima histórica.

**Costes recurrentes.** SBC TTM30,4 M$ sigue dentro de EBIT; no se añade de vuelta en el DCF ni se descuenta una segunda vez. El proxy FCF−SBC709,5 M$ no es FCFF. Se mantienen adquisición/integración/restructuración dentro del margen, salvo la sensibilidad que se indique, en lugar de borrar todos los costes por llamarse “ajustados”. La guía ajustada excluye0,60 USD de amortización adquirida y0,28 de otros ajustes; el GAAP incluye0,18 de devolución. No se usa EPS9,075 como si fuera GAAP sostenible.

**Caja.** FCF739,9 M$ y proxy trasSBC709,5 no excluyen por sí mismos devoluciones cobradas. Si se hubiera cobrado íntegramente el beneficio bruto20,8, la resta conservadora máxima al proxy sería20,8, hasta688,7 M$, antes de conciliar efectos fiscales; si no, no procede restarlo todo. Es una sensibilidad, no una afirmación de cobro. No se vuelve a restar del saldo de caja un beneficio ya incluido: la normalización de flujo y el puente de balance tienen propósitos distintos.
'''+cite('q3','q10')+'''## 4. Overly y capital: una incógnita antigua ahora resuelta

El informe anterior solo conocía el anuncio de Overly. La nota3 del10-Q confirma compra el2octubre por **88,7 M$**, financiada con caja y revolver; el1octubre se tomaron **40 M$** adicionales. El precio ya no es desconocido. Aún faltan la asignación final de compra y contribución separada; no se añaden ventas ni sinergias especulativas sobre la guía actual.

A septiembre: caja388,1; deuda nominal2041,2 frente a contable2032,0 (9,2 son descuentos/costes, no deuda extinguida). Se incorpora el desembolso88,7 y ambos lados del préstamo40: caja proforma339,4, deuda2081,2, neto−1741,8 M$. El préstamo no genera valor neto. Este es un puente de eventos conocidos, **no un balance verificado de4nov**: operaciones, recompras, intereses, divisas y pagos posteriores pueden cambiarlo.

Se reserva200 M$ de caja operativa como hipótesis, no como restricción declarada. Otros ajustes prudenciales:
- Pensiones:31,8 M$ de pasivos brutos de planes deficitarios a cierre2025, sin añadir46,4 M$ de superávits de otros planes como caja disponible. El neto global de pensiones era activo14,6 M$; no se llama déficit a ese neto. La transacción de mayo2026 en un planUSA dejó activos207,1 y obligación195,9, pero no actualiza todos los planes.31,8 es proxy conservadora antigua, revisable, no medición actual.
- Earnouts: reserva supuesta30,3 M$, anclada al valor de adquisición de2025. La nota indica pagos parciales y vencimientos condicionados hasta2028, pero no ofrece aquí saldo remanente completo. No se presenta30,3 como deuda exacta. Los earnouts2024 se estimaron inicialmente10,5 M$; sensibilidad adicional+10,5, y+50 para otros riesgos de puente. Eliminar la reserva completa aumenta valor solo0,36 USD/acción.
- Compensación diferida:17,1 M$ de pasivos frente a16,9 M$ de inversiones valoradas con precios observables, ajuste económico neto0,2. No se afirma afectación jurídica de esos fondos al plan ni se suman otra vez a caja libre.

La nota11 también revela130,6 M$ en inversiones sin valor razonable fácilmente determinable, incluyendo40 M$ adicionales enAmbient.ai duranteQ3. No se añaden a nominal como efectivo. El valor principal no asigna recuperación a esta cartera estratégica: es una elección conservadora explícita, no prueba de valor cero. Si se recuperara50% o100% del importe contable, antes de impuestos/costes, el valor subiría aproximadamente0,77 o1,53 USD por acción.

Puente total usado: **−2004,1 M$**. Los costes ordinarios de pensiones permanecen operativos; no se proyecta además el pago íntegro de déficit dentro delFCFF. Arrendamientos permanecen coste operativo y no se resta su pasivo otra vez. No se añade goodwill al equity.

Bonos:400 M$ vencen1oct2027 al3,55%;400 en2029 al3,5%;600 en2032 al5,411%;400 en2034 al5,6%. Revolver a2030. No se presupone refinanciación gratis. La reserva del modelo no es una alarma de insolvencia.
'''+cite('q10','k25')+'''## 5. FCFF de diez años: operación y reinversión

Base de ingresos4474,03 M$=FY2025×1,10, centro de guíaFY2026. No se confunde conTTM4390,9. Año1≈FY2027, con6% de crecimiento; los cinco primeros años crecen6/5/5/4/4%. Años6–10 convergen a3%. Es proyección propia, no guidanceFY2027. Se descuenta a fin de año; un desplazamiento adicional de dos meses se conserva como sensibilidad de calendario.

MárgenesEBIT21,5/22/22,5/23/23%, y transición hasta23,5% en año10, después deSBC y costes recurrentes. Se excluye la devolución excepcional del anclaje económico. NOPAT=EBIT×80%. D&A3,2% de ventas (TTM3,23%), capex2,5% (TTM2,37%), ΔNWC15% de ventas incrementales. Los tres son supuestos normalizados.

Los primeros años usan la capacidad existente: D&A puede superar capex, dejando inversión neta muy pequeña o ligeramente negativa. No se extrapola ese beneficio a perpetuidad. En años6–10, la reinversión explícita se mezcla progresivamente al20/40/60/80/100% con NOPAT×g/ROIC. Año10 ya reinvierte15% delNOPAT; terminal también. D&A=capex2,5% durante la senda explícita reduce central de136,09 a133,91, mostrando sensibilidad al mantenimiento y reposición de intangibles, pero sin demostrar que el crecimiento esté financiado.

**Límite económico material:** el central proyecta ventas +26,4% en cinco años con reinversión neta acumulada de −5,1 M$. Supone crecimiento del perímetro existente y uso de capacidad instalada; no incorpora M&A futura gratuita. La evidencia disponible no prueba que esa intensidad de inversión baste. Un stress alternativo que reinvierte NOPAT × crecimiento anual / ROIC desde el año 1 reduce el valor a **122,94 USD**. Es una prueba del coste de financiar el crecimiento, no una nueva estimación canónica ni una corrección aritmética. **136,09 permanece como central condicionado**, pendiente de demostrar capacidad e inversión necesarias.

Terminalg3%, ROICincremental20%, FCFF=NOPAT×(1−3/20). Contraste histórico aproximado: NOPATTTM sin devolución a20% de impuesto739,44 M$, capital invertido medio3763,85 M$ calculado con equity+deuda nominal−caja de dic2025/sept2026, incluyendo goodwill. Retorno19,65%. Es una proxy de dos balances, no prueba deROIC incremental futuro ni una medición exacta ajustada por adquisiciones.

WACC9,2%: Treasury10y4,91% del2nov, publicado3nov; beta supuesto1,1 y primaequity supuesta4,5%=Ke9,86%. Pesos objetivo88% equity/12% deuda, coste marginal supuesto5%, impuesto20% →9,1568%, redondeado9,2%. Se aproxima a apalancamiento actual, pero no es calibración certificada de beta/spread. Terminalg<WACC en todos los casos.

85,2 M$ de acciones no: **85,2 millones de acciones diluidas mediasQ3**. Se mantiene fijo sin atribuir recompras gratuitas.0,2 millones de premios antidilutivos excluidos se revelan, no se añaden mecánicamente sin términos/proceeds. Si cambia el capital, se actualiza la valoración.
'''+cite('q10','k25','q3','rf')+'''### Proyección central
'''+tab(['Año','Ventas M$','EBIT %','NOPAT M$','Reinversión M$','FCFF M$'],[[d['year'],f"{d['revenue']:,.1f}",f"{d['ebit_margin']*100:.2f}%",f"{d['nopat']:,.1f}",f"{d['reinvestment']:,.1f}",f"{d['fcff']:,.1f}"] for d in M['cases']['base']['rows']])+'''## 6. Escenarios y prueba inversa
'''+tab(['Escenario','Valor USD','Peso terminal EV','Hipótesis'],[[k,f"{v['value']:.2f}",f"{v['terminal_weight']*100:.1f}%",f"crecimiento primeros5 {'−3pp' if k=='bear' else '+3pp' if k=='bull' else 'central'} y transición; márgenes {'−2pp' if k=='bear' else '+2pp' if k=='bull' else 'central'} todos10años/terminal; WACC{v['assumptions']['wacc']*100:.1f}%; g{v['assumptions']['g']*100:.1f}%; ROIC{v['assumptions']['roic']*100:.0f}%"] for k,v in M['cases'].items()])+'''
El54,12% delEVcentral viene del terminal. No se asignan probabilidades estadísticas ni se elige el favorable para hacer coincidir el precio.

Con el resto central,189,35 exige crecimiento inicial superior en5,39 puntos: **11,39/10,39/10,39/9,39/9,39%** durante cinco años y transición posterior. Alternativamente exige+7,73 puntos de margen en toda la senda:29,23% año1 y31,23% terminal. Ambas son pruebas del precio, no previsiones oficiales; exceden significativamente crecimiento orgánico y margen consolidados actuales.

### Sensibilidad descuento / terminal
'''+tab(['WACC','g','Valor USD'],[[f"{d['wacc']*100:.1f}%",f"{d['g']*100:.1f}%",f"{d['value']:.2f}"] for d in M['sensitivity']])+'''## 7. Conciliación histórica sin reescribir el expediente

A004 (2oct) usaba un ejercicio deEPS modelado8,86×PER22/1,10≈177 USD, con escenario117/177/220. Era valoración por múltiplo, no DCF. Su techo150 resultaba de un descuento general15%; **ese automatismo no se mantiene**. El historial conserva lo que se pensó entonces.

A064 (17oct, publicado después) usaba FCFF de cinco años. La reconstrucción reproduce69,24/112,20/186,63, coherente a redondeo con69/112/187. Esta es la referencia de migración a diez años. Precio histórico156,54 y actual189,35 se mantienen separados delvalor.
'''+tab(['Paso de conciliación','Central USD'],[[a,f'{v:.5f}'] for a,v in M['bridge']])+'''
El puente distingue horizonte/reinversión, nueva guía de ventas, acciones, capital, margen, D&A, ROIC yWACC. La mejora de136,09 frente112,20 no se atribuye enteramente alQ3: parte es método y parte hipótesis. Ninguna diferencia queda disfrazada de “nuevo resultado”.

## 8. Comparable industrial: ASSA ABLOY

Contraste con mismo cierre3nov y beneficio atribuibleTTMseptiembre, cada empresa en su moneda, sin mezclarEPSforward conTTM:

| Métrica | Allegion | ASSA ABLOY B, Estocolmo |
|---|---:|---:|
| Precio |189,35 USD|392,60 SEK|
| Acciones medias usadas, millones |85,2|1110,776|
| Beneficio atribuibleTTM, millones locales |691,1|16959|
| Precio×acciones / beneficioTTM |23,34x|25,71x|
| Aproximación ALLE sin devolución/gananciaQ3, tasa17,5% |24,06x|No se sustituye porEPSajustado|
| OrgánicoQ3, definición emisor |7,2%|4%|
| MargenEBITQ3 informado |24,3%|17,4%|
| MargenALLE sin devolución |22,57%|No equivalente a un ajuste completo entre normas|

ASSA Q3 tiene crecimientoEBIT11%; ALLE normalizado13,22%. Ambos mejoran y tienen mayor fuerza enAmericas queChina/International. No es prueba de que uno tenga idéntico riesgo o mezcla. La comparaciónP/E conserva amortización ySBC en el beneficio contable; ASSA aplicaIFRS yALLEUSGAAP, con distintos impuestos, arrendamientos, apalancamiento, adquisiciones ydivisas. Acciones medias son proxy, no capitalización exacta a3nov. No se comparan como iguales sus métricas propias de “operating cash flow” y “available cash flow”.

La lectura relativa **no demuestra una sobrevaloración extrema deALLE**: cotiza aPER algo menor que un par industrial fuerte. Sin embargo, multiplicarEPSALLE por el múltiplo delpar transferiría también la prima de mercado sin justificar reinversión ni rendimiento requerido. Por eso este chequeo no sustituye elFCFF ni autoriza seguir al precio con el valor.
'''+cite('q10','price','assa','assa_report','assa_price')+'''## 9. Riesgos, calidad de evidencia y siguientes condiciones

La tesis positiva requiere sostener crecimiento orgánico, productividad y conversión de caja, con retorno adecuado sobre las adquisiciones. La invalidan deterioro persistente de volumen no residencial, márgenes recurrentes retrocediendo pese precios, retorno de compras por debajo de su coste y caja consumida por circulante o financiación. Interés/refinanciación, divisas, materiales y política comercial pueden alterar flujos.

Evidencia alta:3FY4QTTM, origen de devolución, cierre/precio deOverly, nominal de deuda ycalendarioQ3. Supuestos explícitos: reserva operativa, claims pendientes, márgenes/growth/WACC/ROIC, aproximación delbalanceposterior y accionesfuturas. No se afirma queearnout30,3 o pensión31,8 sean saldosnoviembre.

Último resultado confirmado22oct, ya incorporado. No se usa “pendiente deQ3” como bloqueo desactualizado. Antes de una eventual entrada, confirmar anuncio de próximo resultado y aplicación de exclusión semanal; este informe no ofrece por sí mismo una liberación delcalendario. Tampoco revalida la elegibilidad delescáner tras la fuerte subida.

Conclusión: **buena recuperación operativa; esperar precio o evidencia más firme para elvalor.** Mantener expediente actualizado, no una orden condicionada alviejo150. La siguiente revisión debe conciliar cierre deOverly, earnouts/pensiones, caja/acciones actuales y nueva guía, y solo después evaluar Stage3.5 con estructura técnica, tendencia, stop y exposición.
'''+cite('q10','calendar')
s=s.replace('85,2 M$ de acciones no: **85,2 millones de acciones diluidas mediasQ3**.','Se utilizan **85,2 millones de acciones diluidas mediasQ3**.')
pros_es=['Ventas TTM +10,33% y FCF menos SBC +9,07%; la caja confirma una recuperación operativa real.','Sin devolución arancelaria, EBIT Q3 crece 13,22% y EBIT TTM 10,76%, sin convertir el extraordinario en recurrente.','La nueva nota oficial revela Overly por 88,7 M$ y permite incorporar su financiación sin contar deuda como caja gratis.']
cons_es=['El central de 136,09 depende de una reinversión inicial muy baja; financiar el crecimiento al ROIC supuesto reduce el stress a 122,94.', 'El cierre de 189,35 USD excede el central de 136,09; el favorable de 238,52 necesita mejores hipótesis y no aprueba entrada.','Caja y claims posteriores a septiembre requieren conciliación; earnout y pensión son reservas explícitas, no saldos actuales certificados.','International cae 0,2% orgánico y el crecimiento residencial depende del precio; la recuperación no es uniforme.','El comparable industrial no confirma sobrevaloración extrema, pero tampoco sustituye el rendimiento y reinversión exigidos por el FCFF.']
pros_en=['TTM revenue grew 10.33% and FCF less SBC 9.07%; cash confirms real operating recovery.','Excluding tariff refunds, Q3 EBIT grew 13.22% and TTM EBIT 10.76%, without capitalizing a one-off gain.','New official disclosure prices Overly at $88.7m and allows its funding bridge without treating debt as free cash.']
cons_en=['The $136.09 central case depends on very low initial reinvestment; funding growth at the assumed ROIC reduces the stress value to $122.94.', 'The $189.35 close exceeds the $136.09 central case; the $238.52 favorable case requires stronger assumptions and does not approve entry.','Post-September cash and claims need reconciliation; earnout and pension adjustments are explicit reserves, not certified current balances.','International organic revenue fell 0.2% and residential growth relies on pricing; recovery is not uniform.','The industrial peer does not prove extreme overvaluation, but cannot replace FCFF reinvestment and required-return analysis.']
s+='\n## Evidencia exacta para pros y contras\n'
for title,xs in [('A favor',pros_es),('En contra',cons_es),('Pros',pros_en),('Cons',cons_en)]:s+='\n### '+title+'\n\n'+'\n'.join('- '+x for x in xs)+'\n'
# Normalize prose spacing without touching verified URLs or exact appendix strings.
import re
head,appendix=s.split('\n## Evidencia exacta para pros y contras',1)
links_saved=[]
def shield(m):
 links_saved.append(m.group(0));return '@LINKTOKEN'+str(len(links_saved)-1)+'@'
head=re.sub(r'https?://[^)\s]+',shield,head)
head=re.sub(r'(?<=[a-záéíóúñ])(?=[0-9])',' ',head)
head=re.sub(r'(?<=[0-9])(?=[a-záéíóúñ])',' ',head)
head=re.sub(r'(?<=[0-9])(?=(?:M\$|USD|SEK))',' ',head)
head=re.sub(r'(?<=[a-záéíóúñ])(?=(?:TTM|EPS|GAAP|FCFF|FCF|EBIT|SBC|DCF|ROIC|WACC|Q[1-4]|FY20|USD|PER|ALLE|Overly|Ambient))',' ',head)
head=re.sub(r'(?<=[%])(?=[a-záéíóúñ])',' ',head)
for i,url in enumerate(links_saved):head=head.replace('@LINKTOKEN'+str(i)+'@',url)
for a,b in [('delbalanceposterior','del balance posterior'),('accionesfuturas','acciones futuras'),('delcalendario','del calendario'),('delscreener','del screener'),('delescáner','del escáner'),('alviejo','al viejo'),('delvalor','del valor'),('delpar','del par'),('costesordinarios','costes ordinarios')]:head=head.replace(a,b)
s=head+'\n## Evidencia exacta para pros y contras'+appendix
(P/'report.md').write_text(s)
meta=dict(ticker='ALLE',as_of='2026-11-04',research_cutoff='2026-11-04 15:43 UTC',price=189.35,price_timestamp='2026-11-03 16:00 America/New_York',bear=80.29,base=136.09,bull=238.52,research_status='Stage3 reconstructed; research-grade conditional on growth funding and balance/claim assumptions',decision_es='Buena recuperación; esperar precio o evidencia. Central136,09 frente189,35. Sin entrada Stage3.5.',decision_en='Good recovery; wait for price or evidence. Central136.09 versus189.35. No Stage3.5 entry.',buy_ceiling=None,approved_entry=False,stage35_approved=False,pros_es=pros_es,cons_es=cons_es,pros_en=pros_en,cons_en=cons_en,pros_cons_evidence={'pros':['Section2; SEC history','Section3; q3/q10','Section4; q10 notes3/8'],'cons':['Section5; model.json growth_funding_stress','Section6; model.json,price','Section4; q10,k25','Section1; q3','Section8; assa_report,assa_price']},growth_funding_stress=round(M['growth_funding_stress']['value'],2),publication_note='Central conditioned on growth funding; stress122.94 is separate, not a new canonical estimate. Preserve historical A004177 multiple valuation and A064112 five-year FCFF, with bridge. Remove obsolete awaiting-Q3 label only; do not imply current November balance is certified or permit Stage3.5.')
json.dump(meta,open(P/'publication.json','w'),indent=2,ensure_ascii=False);print(len(s))
