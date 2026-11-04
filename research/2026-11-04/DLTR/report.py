from pathlib import Path
import json,subprocess
P=Path(__file__).parent
m=json.load(open(P/'model.json'));f=json.load(open(P/'financials.json'));peers=json.load(open(P/'peers.json'));c=m['cases'];b=c['base'];a=b['assumptions'];urls=json.load(open(P/'sources/urls.json'));pu=json.load(open(P/'sources/peer_urls.json'))
def n(v):return '—' if v is None else f'{v:,.2f}'
def pct(v):return f'{v*100:.2f}%'
pros=['La venta de Family Dollar permite evaluar un negocio continuado rentable, con EBIT TTM de 1.747,0 M$ después de retirar devoluciones y servicios transitorios.','Las ventas comparables Q2 crecen 3,7%, con tráfico positivo de 0,4%; la mejora no procede exclusivamente de aperturas.','El calendario oficial confirma resultados el 24 de noviembre antes de apertura, con llamada a las 08:00 ET.']
cons=[f'El FCFF central de {c["base"]["value"]:.2f} y favorable de {c["bull"]["value"]:.2f} no respaldan el cierre de 134,07 bajo estos supuestos.', 'El CFO TTM de 3.117,0 M$ incorpora cobros arancelarios, fiscalidad de la venta y circulante favorable; no es una anualidad recurrente.', 'Quedan por verificar resoluciones aduaneras posteriores al Q2 y contingencias de Family Dollar; las fechas antiguas de agosto y octubre ya han vencido.']
proen=['The Family Dollar sale isolates a profitable continuing business, with $1,747.0m of TTM EBIT after removing refunds and transition services.','Q2 comparable sales rose 3.7%, with positive traffic of 0.4%; growth is not solely from new stores.','The official calendar confirms earnings on November 24 before the open, with an 08:00 ET call.']
conen=[f'Central FCFF of {c["base"]["value"]:.2f} and favorable FCFF of {c["bull"]["value"]:.2f} do not support the 134.07 close under these assumptions.','TTM CFO of $3,117.0m includes tariff cash, sale-related taxes and favorable working capital; it is not a recurring annuity.','Post-Q2 customs decisions and Family Dollar contingencies remain qualified; the old August and October decision dates have already passed.']
s=f'''# DLTR: caja normalizada, reinversión y perímetro retenido

Corte de investigación: 4 noviembre 2026, 16:55 UTC. Precio de referencia: 134,07 USD, cierre regular del 3 noviembre (16:00 Nueva York). Estados: último 10-Q al 1 agosto 2026; FY2025 al 31 enero 2026. No se fabrica un balance a noviembre. Moneda: USD; importes en millones salvo precio y EPS.

## 1. Conclusión y alcance

**Esperar precio o nueva evidencia; no avanzar a Stage3.5.** Valor central {n(c['base']['value'])}; escenarios {n(c['bear']['value'])}/{n(c['bull']['value'])}. Es una valoración propia condicionada, no un precio máximo de compra. El favorable tampoco respalda el precio de referencia. Sin descuento mecánico adicional del 15%, sin órdenes, cambios de posición, stop ni tamaño.

Se cierra la reconstrucción financiera y del modelo, pero **no se certifica un cierre normativo integral**: no se ha recuperado la resolución final de dos expedientes aduaneros con fechas ya vencidas, y la indemnización de litigios de Family Dollar no tiene importe fiable. Estas limitaciones siguen visibles. La decisión de esperar es compatible con ellas; una entrada no queda autorizada por esta investigación.

A113 ya era un FCFF operativo: no se reclasifica como FCFE. La reconstrucción de sus supuestos reproduce {n(m['historical_A113']['reconstruction']['bear']['value'])}/{n(m['historical_A113']['reconstruction']['base']['value'])}/{n(m['historical_A113']['reconstruction']['bull']['value'])}, frente a los 35,55/72,78/130,27 divulgados. El archivo ejecutable original no fue recuperado; reproducir sus cifras redondeadas no acredita identidad del fichero. A113 y el escáner original se conservan como historia.

## 2. Negocio, calidad y evolución real

Dollar Tree conservada vende productos de bajo precio en Estados Unidos y Canadá. El surtido multiprecio, la red de tiendas y distribución y la compra a escala ayudan a sostener el formato, pero no constituyen por sí solos un monopolio ni una barrera tecnológica. Compite por precio, conveniencia, surtido y ejecución. Los clientes pueden cambiar de comercio; importaciones, salarios, alquileres, merma y mezcla consumible/discrecional son riesgos operativos reales. Esta valoración del negocio es una inferencia, no una declaración de moat permanente.

La mejora de Q2 tiene base operativa pero también extraordinarios: ingresos totales 4.891,2 frente a 4.570,4 (+7,02%), comparables +3,7%, tráfico +0,4% y ticket +3,3%. En H1, tráfico −0,3% y ticket +3,9% muestran que precio/mezcla han contribuido más que afluencia. El margen bruto incorpora menor merma y aranceles, además de la devolución; una menor merma estimada no garantiza repetición. El EBIT Q2 de 690,1 y EPS 2,70 no deben anualizarse.

El FY2023 contiene 53 semanas y los siguientes 52. EBIT anual 1.774,5/1.462,0/1.653,1: la recuperación no borra la compresión anterior. El EPS también se beneficia de recompras: usar crecimiento del EPS como sustituto de crecimiento operativo atribuiría a la actividad una mejora financiera. Se pagaron aproximadamente 1.200 M$ en recompras H1 y se añadió un préstamo de 500 M$; no se presume creación de valor por el mero descenso del número de acciones.

Fuente: [10-Q Q2]({urls['q2']}), [10-K FY2025]({urls['k25']}), [resultados Q2]({urls['release']}).

## 3. Tres ejercicios, cuatro trimestres y TTM comparable

Operaciones continuadas, incluyendo gastos corporativos. Family Dollar discontinuada queda fuera de beneficio y CFO. Ventas incluyen otros ingresos. FCF = CFO − capex; caja después de SBC = CFO − capex − SBC, una comprobación económica, no el FCFF descontado. Capex ya comprende las inversiones incluidas por el emisor; no se añade software otra vez. Q4 se obtiene por diferencia para partidas aditivas; EPS Q4 **2,56** y diluidas **199,8** se leen directamente del comunicado, no se restan EPS anuales.

|Periodo|Ingresos|EBIT|Neto continuado|EPS diluido|CFO|Capex|SBC|FCF|FCF−SBC|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for r in f['annual']+f['quarters']+f['ttm']:s+='|'+r['period']+'|'+'|'.join(n(r.get(k)) for k in ['revenue','ebit','net_income','eps','cfo','capex','sbc','fcf','fcf_less_sbc'])+'|\n'
s+=f'''
TTM = FY2025 + H1FY2026 − H1FY2025; previo = FY2024 + H1FY2025 − H1FY2024. Los cuatro trimestres suman el último TTM. D&A TTM 691,8: aproximadamente 3,45% de ingresos. [Fuente directa Q4](https://www.sec.gov/Archives/edgar/data/935703/000093570326000024/ex991q4-25earningspressrel.htm). Las tablas numéricas fuente, etiquetas y fórmulas se incluyen en el soporte.

## 4. Beneficio y caja recurrentes: conciliación sin dobles ajustes

EBIT TTM publicado 2.201,4 − devolución arancelaria bruta 368,7 − ingreso neto TSA 85,7 (=54,9 FY −8,0 H1 previo +38,8 H1 actual) = **1.747,0 M$**, margen 8,71%. No se añaden los 37 M$ ya gastados en reinversión (22 en coste de ventas, 15 en SG&A), ni los 13 M$ de otros derechos AD/CVD. Añadir los 37 produciría 1.784,0, pero sería una normalización menos estricta, no otra ganancia simultánea.

El TSA dura 18 meses desde el 5 julio 2025. Q2 reconoce 17,7 netos y H1 38,8; los gastos para prestar soporte permanecen en SG&A. Retirar todo el ingreso neto mientras se mantienen los costes puede ser prudente, pero no calcula exactamente el margen tras la separación. No se proyecta indefinidamente el TSA ni se eliminan gastos de soporte sin datos.

Los 14 M$ de intereses de la devolución y los 5,2 M$ de seguro en Q1 están en Other income, no en EBIT. No se restan nuevamente del EBIT ni se usan como margen recurrente. Los 368,7 de beneficio y aproximadamente 369 de cobro son distinto redondeo, no dos ingresos independientes.

CFO TTM 3.117,0 incluye unos 383 M$ cobrados por devolución más intereses, circulante favorable y menores pagos de impuestos vinculados a Family Dollar. FCF−SBC 1.910,1 menos 383 = 1.527,1 es solo un **estrés bruto antes del efecto fiscal**, no caja recurrente certificada. No se inventa una corrección fiscal o de inventarios exacta. La valoración parte de NOPAT proyectado, no de repetir ese CFO; SBC queda como coste en EBIT y no se resta otra vez del FCFF.

La empresa prevé reinvertir una parte significativa del reembolso durante el resto de FY2026, incluyendo unos 40 M$ en un fondo filantrópico. El primer año del modelo carga 40 M$ adicionales antes de impuestos como hipótesis prudente; no se afirma que sea una deuda vencida ni una estimación completa del desembolso restante. El margen base ya supone progreso operativo y costes ordinarios, sin añadir de nuevo los 37 históricos. Sensibilidades 0/40/100/200 M$ delimitan la reserva; no sustituyen la ejecución real. No se combinan este cargo y una deducción de la misma partida en el puente de caja.

## 5. Caja, deuda, acciones y obligaciones conservadas

|Puente a equity|M$|Tratamiento|
|---|---:|---|
|Caja disponible 1 agosto|1.058,1|No incluye 43,7 de efectivo restringido|
|Reserva operativa|−500,0|Hipótesis de liquidez, no gasto ni pasivo contable|
|Deuda principal|−2.950,0|2.450 en notas y 500 préstamo; no 2.933,5 contables netos|
|Impuestos a pagar a largo plazo|−23,4|Saldo actual; no añadir también 29,7 de enero|
|Recompras pendientes de liquidar|−0,5|Identificadas al cierre|
|Recompras posteriores hasta 25 agosto|−5,3|Caja conocida; no se presupone otra recompra posterior|
|**Puente neto**|**{n(m['capital_bridge']['net'])}**|Una sola aplicación después del valor operativo|

Acciones: 190,9 M diluidas medias Q2. No son las 187,673 M emitidas al cierre ni una garantía de dilución futura: se excluyeron 1,8 M instrumentos antidilutivos. No se suman automáticamente todas las opciones sin ejercicio/proceeds; se muestra +3% de dilución. La recompra posterior de 41.412 acciones no reduce el denominador diluido medio: es una cautela pequeña, explícita, no un balance proforma exacto.

Los alquileres permanecen como coste operativo en EBIT y FCFF. No se resta otra vez toda la deuda de arrendamientos operativos. La financiación de proveedores de 305,6 M$ está incluida en cuentas a pagar, sin cambio de condiciones según el emisor: no se duplica como deuda además del circulante, aunque existe riesgo de liquidez si cambia su disponibilidad. No se suma como caja el activo fiscal ni se resta íntegro el pasivo fiscal diferido de 347,9; se usa impuesto normalizado y el saldo de impuestos a largo plazo separado.

La venta de Family Dollar generó aproximadamente 793 M$ (680 de proceeds netos y liquidación de circulante, más 113 de monetización previa): ya están reflejados, no se añaden otra vez. Subsisten garantías de alquiler por 20 M$ en el segundo año y 10 M$ en el tercero; el emisor considera inmaterial su valor razonable. No se convierten 30 M$ brutos en deuda cierta: estrés de desembolso total reduce el valor a {n(m['capital_sensitivity']['lease_guarantee_full30'])}. La indemnización de determinados litigios anteriores a la venta no tiene rango de pérdida fiable; no se certifica importe cero.

## 6. FCFF financiado y supuestos

Modelo de diez años: cinco explícitos y cinco de transición. Años de proyección desde la última base disponible, **no guía fiscal FY2026 ni calendario trimestral exacto**. El año1 base 21.000 M$ es un periodo normalizado hacia delante; la guía corporativa FY2026 de ventas netas es 20.500–20.700 M$, con calendario y definición ligeramente distintos. No se ha construido un balance de noviembre ni un roll-forward trimestral inventado.

EBIT = ingresos × margen propio − cargo adicional del año1. NOPAT = EBIT × (1−25%). Reinversión explícita = capex − D&A + ΔNWC. Se financia el mayor entre esa inversión y NOPAT **operativo antes del cargo extraordinario** × crecimiento de ventas / ROIC supuesto. Así un gasto extraordinario no reduce artificialmente la financiación del crecimiento. FCFF = NOPAT − reinversión. La reserva adicional se muestra en cada fila y concilia FCFF = NOPAT + D&A − capex − ΔNWC − reserva.

Crecimiento de ventas en esta regla no equivale a crecimiento de NOPAT: la mejora de márgenes supone uso de capacidad existente. El 12% no es un ROIC incremental contable demostrado. Es una hipótesis de reposición/crecimiento madura, con sensibilidades. El retorno contable sin capitalizar alquileres sobrestimaría la comparación con capital económico total; no se usa como prueba automática de moat.

D&A 3,4% de ventas; capex 5,5% en años1–5, descenso **gradual** a 4,5% en año10; ΔNWC 10% del incremento de ingresos. No hay caída abrupta del capex solo al entrar en terminal, como en A113. Terminal: mayor entre capex4,5%−D&A3,4%+circulante y NOPAT×g/ROIC. Se conserva un coste real de activos, incluso si se eleva ROIC; no se libera toda la amortización como caja perpetua.

|Caso|Ingresos año1|Crecimientos años2–5|Margen operativo año1→5|WACC|g|ROIC|Valor/acción|Peso terminal EV|
|---|---:|---|---|---:|---:|---:|---:|---:|
'''
for key,label in [('bear','Conservador'),('base','Central'),('bull','Favorable')]:
 x=c[key];r=x['rows'];ass=x['assumptions'];s+=f'|{label}|{n(r[0]["revenue"])}|'+ '/'.join(pct(y['growth']) for y in r[1:5])+f'|{pct(r[0]["core_ebit_margin"])}→{pct(r[4]["core_ebit_margin"])}|{pct(ass["wacc"])}|{pct(ass["g"])}|{pct(ass["roic"])}|{n(x["value"])}|{pct(x["terminal_weight"])}|\n'
s+=f'''
Los márgenes anteriores son antes del cargo adicional40; el EBIT efectivo año1 central es1.892,0 M$. El favorable exige margen12% y fuerte crecimiento, no es un techo de compra ni una probabilidad. Impuesto25% y ROIC12% en los tres escenarios; D&A y capex iguales. Convergencia lineal de crecimiento años6–10 hacia g, margen del año5 mantenido después.

Tasa central10% nominal USD: anclaje ilustrativo RF4,91% (2nov, H.15 publicado3nov), ERP supuesto4,5%, beta supuesta1,28 y deuda10% del capital con coste supuesto6%, impuesto25% producen aproximadamente10,04%, redondeado10%. No se presenta beta como regresión estimada ni 10% como observación exacta. Sensibilidad9–11%; el cambio simultáneo de crecimiento/margen/tasa entre casos no es una distribución estadística.

|Año|Ingresos|EBIT|NOPAT|D&A|Capex|ΔNWC|Reserva extra|FCFF|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for r in b['rows']:s+='|'+str(r['year'])+'|'+'|'.join(n(r[k]) for k in ['revenue','ebit','nopat','da','capex','delta_nwc','additional_reinvestment_reserve','fcff'])+'|\n'
s+=f'''
Valor presente explícito {n(b['pv_explicit'])}; terminal {n(b['pv_terminal'])}; EV {n(b['ev'])}; puente {n(b['net_bridge'])}; equity {n(b['equity'])}; dividido por190,9. Reinversión año10 {n(b['rows'][-1]['reinvestment'])}, terminal {n(b['terminal_reinvestment'])}: transición financiada, sin salto gratuito a NOPAT.

## 7. Sensibilidades e inverso del precio

|WACC|g2,0%|g2,5%|g3,0%|
|---|---:|---:|---:|
'''
for w in [.09,.095,.10,.105,.11]:s+='|'+pct(w)+'|'+'|'.join(n(next(r['value'] for r in m['sensitivity'] if r['wacc']==w and r['g']==g)) for g in [.02,.025,.03])+'|\n'
s+='\nROIC: '+ '; '.join(pct(r['roic'])+' → '+n(r['value']) for r in m['roic_sensitivity'])+'. Al subir ROIC domina el suelo explícito: el valor no crece sin límite.\n'
s+='\nCargo adicional primer año: '+ '; '.join(n(r['first_year_expense'])+' M$ → '+n(r['value']) for r in m['expense_sensitivity'])+'.\n'
s+=f'''
Reserva de caja250/750 M$: {n(m['capital_sensitivity']['reserve250'])}/{n(m['capital_sensitivity']['reserve750'])}. Dilución +3%: {n(m['dilution_sensitivity'])}. Sin suelo económico en años explícitos: {n(m['no_growth_funding_floor'])}; manteniendo capex5,5% hasta año10: {n(m['no_capex_transition'])}. No se promedian las variantes para elegir un resultado cómodo.

Inverso del mismo modelo: para alcanzar134,07 manteniendo crecimiento base, el margen de **todos los diez años y terminal** aumenta {m['reverse']['margin_extra_all_years']*100:.2f} puntos, hasta aproximadamente {10+m['reverse']['margin_extra_all_years']*100:.2f}% en el año5/terminal. Es una exigencia condicionada, no pronóstico.

La alternativa de crecimiento no es monotónica porque crecer exige financiación. En un barrido de +0 a +40 puntos a los crecimientos de años2–5, pasos0,1 puntos, el máximo calculado es {n(max(m['reverse']['growth_scan'],key=lambda r:r['value'])['value'])}, cerca de +29,8 puntos; no alcanza134,07. **No se halló solución en ese dominio**, no se demuestra inexistencia universal. No se fuerza una raíz por bisección ni se recicla el +11,65 de A113, que no financiaba ese crecimiento igual. Escenarios extremos pueden requerir caja externa: no validan capacidad de financiación ni dilución futura.

## 8. Pares comparables con ajustes delimitados

Precios cierre3nov, diluidas Q2, estados TTM a1ago (DG31jul). USD y US GAAP; alquileres permanecen operativos. EV aproximado=capitalización diluida+deuda−caja/inversiones. Para DLTR se usa principal2.950; DG utiliza deuda contable reportada, una diferencia menor de base que se declara. Los múltiplos son contraste, no derivan valor justo ni mediana aplicable.

|Empresa|Precio|Ventas TTM|EBIT publicado|Ajuste devolución|TSA retirado|EBIT ajustado|EV/EBIT ajustado|PER guía parcialmente ajustada|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for name,r in peers['companies'].items():s+='|'+name+'|'+'|'.join(n(r[k]) for k in ['price','ttm_sales','ttm_ebit','refund_removed','tsa_removed','ttm_ebit_normalized','ev_ebit_normalized','guidance_pe_ex_refund'])+'|\n'
s+=f'''
DLTR y FIVE eliminan devolución **bruta** en EBIT; DG solo permite estimar beneficio **neto** de reinversión, 66pb × ventasQ2 =74,52. No son normalizaciones idénticas y no se interpreta una diferencia de múltiplos pequeña como arbitraje. FIVE tiene mayor crecimiento comparable y mezcla discrecional; DG mayor peso consumible y deuda. DLTR incluye otros ingresos en ventas, los pares ventas netas; no se confunde precisión de cálculo con equivalencia económica.

La guía DLTR7,70–8,05 menos0,60 =7,10–7,45 es referencia parcial, antes de depurar TSA y demás ajustes; no EPS GAAP recurrente. DG7,90−0,25 y FIVE10,07 tampoco constituyen beneficios plenamente homogeneizados. La comparación no prueba que DLTR sea barata.

Fuentes: [FIVE 10-K]({pu['fy25']}), [FIVE Q2]({pu['q226']}), [FIVE comunicado]({pu['q226_release_sec']}), [DG 10-K]({pu['dg_fy25']}), [DG Q2]({pu['dg_q226']}), [DG comunicado]({pu['dg_q226_release_sec']}).

## 9. Normativa, catalizadores y pendientes concretos

Q2 describía exposiciones retroactivas máximas de11 M$ en aluminio y15 M$ en platos de papel; las decisiones previstas31ago/14oct ya están vencidas. No se han recuperado aquí las resoluciones finales aplicables al emisor: **resultado actual no confirmado**, no «evento futuro» ni «sin pérdida». Búsquedas en Federal Register hasta4nov no equivalen a prueba de ausencia. El gasto13 M$ por importaciones posteriores ya permanece en EBIT; el estrés adicional de26 M$ corresponde a retroactividad distinta y lleva el valor a {n(m['capital_sensitivity']['retroactive_duties26'])}. No es obligación cierta ni estimación probabilística.

La investigación de aluminio de Indonesia/Malasia iniciada6ago es otro expediente. El Q2 citaba preliminar4ene2027, una fecha histórica sujeta a cambios, no confirmación de calendario actual. Nuevos aranceles, origen de producto y eventual repercusión al cliente pueden afectar margen mucho más que una liquidación histórica aislada. No se extrapola la devolución IEEPA a otras tarifas ni se presume refund adicional material.

Los litigios e indemnizaciones de Family Dollar siguen siendo riesgos sin pérdida estimable: no se inventa reserva ni se etiqueta riesgo cero. El marco analítico conserva el coste laboral, alquileres y suministro. No es asesoría jurídica ni una certificación de cumplimiento integral.

**Resultados24nov2026 antes de apertura; llamada08:00 ET**, anunciados oficialmente3nov. No están en la semana de exclusión2–6nov. Esto resuelve el calendario de resultados, pero no elimina los otros filtros. [Anuncio oficial](https://corporate.dollartree.com/investors/news-events/press-releases/detail/312/dollar-tree-inc-to-host-third-quarter-earnings-conference).

Para reabrir: verificar Q3 sin devolución, avance de TSA y costes de salida, gasto de reinversión realmente ejecutado, caja y recompra posteriores, resolución DOC y contingencias, margen sostenible y precio. GuíaQ3 ventas5.000–5.100, comparables3–4%, EPS ajustado0,80–0,95 con impacto negativo0,50 de reinversión: no comparar ese trimestre débil con Q2 inflado como si fueran idénticos.

No se actualizan medias técnicas ni se afirma una nueva señal de pullback. El cierre3nov es referencia de valoración, no un nuevo escáner. La causa de una caída diaria no queda demostrada solo por estos riesgos. Falta una futura validación técnica/Stage3.5 si el fundamental y precio llegan a justificarla.

## 10. Evidencia resumida para la ficha

### A favor
'''
s+='\n'.join('- '+x for x in pros)+'\n\n### En contra\n'+'\n'.join('- '+x for x in cons)
s+='\n\n### English evidence\n'+'\n'.join('- '+x for x in proen+conen)
s+='\n\n## Reproducibilidad\n\nEjecutar build_financials.py, model.py, peers.py, report.py y qa.py con Python estándar y Pandoc para HTML. El ZIP público incluye datos numéricos seleccionados y notas propias, no filings completos. Los escenarios son hipótesis propias, no recomendaciones de ejecución. Auditoría independiente completada: modelo, puente, fuentes y paquete reproducidos; se conservan las reservas normativas expresas.\n'
(P/'report.md').write_text(s)
subprocess.run(['pandoc',str(P/'report.md'),'-s','-o',str(P/'report.html'),'--metadata','title=DLTR — revisión fundamental'],check=True)
meta=dict(ticker='DLTR',as_of='2026-11-04',research_cutoff='2026-11-04 16:55 UTC',price=134.07,price_timestamp='2026-11-03 16:00 America/New_York',base=round(c['base']['value'],2),bear=round(c['bear']['value'],2),bull=round(c['bull']['value'],2),research_status='Independently audited funded FCFF; customs/legal status remains qualified',decision_es='Esperar precio/evidencia; valoración financiada y calendario 24 nov, normativa posterior al Q2 pendiente.',decision_en='Wait for price/evidence; funded valuation and Nov 24 earnings date, post-Q2 customs status qualified.',approved_entry=False,stage35_approved=False,buy_ceiling=None,pros_es=pros,cons_es=cons,pros_en=proen,cons_en=conen,publication_note='Preserve A113 original FCFF35.55/72.78/130.27 and original scanner; new reconstruction, not original executable identity. Price134.07 Nov3 distinct from scanner. No positions/stops/lots changed. Do not label normative review fully completed.')
json.dump(meta,open(P/'publication.json','w'),indent=2,ensure_ascii=False)
