import json,pathlib
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());h=json.loads((P/'history/portable/financial_history.json').read_text());p=json.loads((P/'peers.json').read_text())
def f(x,n=2):return 'No desglosado' if x is None else f'{x:,.{n}f}'.replace(',','X').replace('.',',').replace('X','.')
rows=[]
for k in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','prior_TTM_2025Q3','TTM_2026Q3']:
 a=h['rows'][k];rows.append('|'+ '|'.join([k]+[f(a[x],2 if x=='EPS_diluted' else 0) for x in ['revenue','EBIT','parent_NI','EPS_diluted','CFO','DA','capital_investments_gross','SBC_total']])+'|')
b=m['cases']['base'];cases='\n'.join('|'+k+'|'+f(a['value'])+'|'+f(a['assumptions']['wacc']*100)+' %|'+f(a['assumptions']['g']*100)+' %|'+f(a['assumptions']['roic']*100)+' %|' for k,a in m['cases'].items())
sens='\n'.join(f'|{k}|{f(v)}|' for k,v in m['sensitivities'].items())
s='''# VLO — el múltiplo barato depende de un margen de refino extraordinario

**Investigación y valoración condicionadas. No certifica Stage 3 integral ni Stage 3.5; ninguna entrada aprobada. Auditoría independiente completada para investigación condicionada; no certificación integral.** Corte: 4 de noviembre de 2026, 18:35 UTC. No cambia operaciones ni posiciones.

## 1. Conclusión

El beneficio actual es real y la caja ha aumentado. El riesgo consiste en capitalizar como permanente una rentabilidad por barril muy superior a su historia reciente. El DCF separa transición cíclica, capital industrial y obligaciones; mantiene visibles las estimaciones en el puente y no usa el P/E de pico para fijar valor.

'''+f'''Escenarios propios: **{f(m['cases']['bear']['value'])} / {f(b['value'])} / {f(m['cases']['bull']['value'])} USD por acción**, frente al cierre del 3 de noviembre de **387,65 USD**. No son probabilidades, límites absolutos ni recomendación de corto. El favorable no es un techo posible de mercado. La última sesión real del escáner es 30 de octubre a 399,57, distinta del cierre de ese día de 399,66. A123 era triage, sin DCF que replicar. Esta valoración es nueva.

## 2. Historia y alcance de caja

USD millones, salvo EPS diluido por acción. NI atribuible a accionistas de Valero. CFO consolidado incluye íntegramente entidades controladas, también DGD, aunque Valero posee el 50 %. Capital bruto incluye turnaround/catalizadores y otras inversiones, no solo PPE.

|Periodo|Ventas|EBIT|NI matriz|EPS|CFO|D&A|Inversión bruta|SBC total|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(rows)+'''

**El EBIT TTM aumenta a 17.575 M$ y el CFO a 15.959 M$, pero la rentabilidad de refino está muy por encima de los años 2024–25.** El EPS TTM de 44,46 es suma de los cuatro trimestres publicados. Q4 2025 usa 3,73, no FY menos nueve meses, que daría 3,68 por diferencias de denominadores. No convertir cifras de EPS en flujos de caja.

CFO menos inversión bruta TTM es 14.317 M$, antes de un ajuste completo por SBC y otras normalizaciones. El reconocimiento de capital por SBC de 102 M$ no acredita el gasto total TTM; owner FCF exacto permanece desconocido. El DCF retiene la remuneración en el EBIT, sin sumarla como efectivo gratuito.

**La inversión incluye turnaround y catalizadores: en nueve meses son 1.230 M$ brutos, no solo 654 M$ de capex fuera de VIEs.** El bruto de 1.230 incluye 661 de PPE y 569 de turnaround/catalizadores; el atribuible a Valero es 1.205. No combinar inversión atribuible con beneficio y caja consolidados al 100 %. La guía FY2026 es unos 2.000 M$, incluyendo 250 relacionados con Port Arthur, de los cuales aproximadamente 1.700 sostienen el negocio.

El aumento de impuestos por pagar aportó 1.513 M$ al circulante CFO de nueve meses, compensando parte del consumo de caja por clientes. Esa financiación fiscal no es mejora estructural del margen. El modelo no capitaliza CFO como flujo permanente y reserva el pasivo fiscal corriente en el puente.

## 3. Normalización del refino y perímetro retenido

Refining EBIT ajustado anual 2023/2024/2025: 11.528 / 3.988 / 5.273 M$. Throughput: 2.979 / 2.912 / 2.988 miles de barriles diarios. Dividiendo por días reales del año, incluido 366 en 2024, resulta **10,60 / 3,74 / 4,83 USD de EBIT ajustado por barril**. Son medidas netas de costes operativos y D&A, no crack spreads brutos.

En Q3 2026, EBIT ajustado refining 8.774 M$ y throughput 2.972 miles de barriles/día equivalen a aproximadamente 32,09 USD por barril. La explicación del emisor atribuye unos 5.500 M$ de mejora a destilados y 2.300 M$ a gasolina, mientras menor volumen resta unos 420 M$. No es crecimiento equiparable de capacidad. EIA octubre prevé relajación de mercados en 2027, pero es un pronóstico con inputs del 1 de octubre, no una garantía ni actualización del 4 de noviembre.

**Benicia terminó de detener sus unidades en abril: no se proyecta recuperar su volumen ni borrar sus obligaciones de cierre.** Sigue el suministro a clientes por vías alternativas; decommission/redevelopment pasa a gastos corporativos desde Q2. Los costes de cierre no desaparecen con el impairment. El comparativo 2025 contiene deterioro de 1.131 M$; no se interpreta su ausencia en 2026 como nueva rentabilidad recurrente.

Ajustes concretos que no se perpetúan automáticamente:
- Beneficio de liquidación LIFO de 44 M$ en 9M2026, frente a gasto de 37 M$ en Q4 2025. No asumir liberación futura continua de inventario.
- D&A incremental de Benicia de 133 M$ en nueve meses; el modelo adopta capacidad ya reducida y no añade el beneficio de recuperación de una planta cerrada.
- Seguros por cobrar de 99 M$ en nueve meses, incluidos 21 en Q3, pero sin cobro a septiembre. Existen también reparaciones de 19 M$ y gasto de inversión. No sumar el derecho al seguro de nuevo ni tratarlo como cobro recurrente.
- Devolución IEEPA de DGD de 51 M$, reconocida como menor coste y sustancialmente cobrada. No anticipar fases futuras ni añadir otra vez la caja. DGD consolidada no equivale a participación económica del 100 % de Valero.
- Créditos de combustible limpio en Ethanol: 211 M$ en nueve meses, incluidos 92 en Q3 con efecto de ventas de meses anteriores. No anualizar ese trimestre ni suponer extensión indefinida de la norma.

## 4. DCF industrial: diez años y terminal financiado

Modelización por EBIT de segmento y volumen, no por extrapolación de ventas ligadas al crudo. Año 1 representa los próximos doce meses, sin ajuste fino de un periodo inicial parcial. Primeros cinco años explícitos; años 6–10 estabilizan el ciclo y crecen nominalmente al ritmo terminal. Los supuestos son propios, no guía del emisor.

|Escenario|Valor USD|WACC|g terminal|ROIC supuesto|
|---|---:|---:|---:|---:|
'''+cases+'''

**Central:** throughput constante de 2,95 millones de barriles/día, sin reabrir Benicia. EBIT refining por barril de 14 / 10 / 8 / 6 / 6 USD en años 1–5. El 6 del quinto año es superior a 2024–25 y menor a 2023; es una hipótesis de capacidad más ajustada, no la media histórica ni consenso. Renewable Diesel EBIT consolidado de 600 / 400 / 200 / 0 / 0 M$; Ethanol 500 / 400 / 350 / 300 / 300; gasto corporativo inicial 1.150, con inflación. No se extiende automáticamente el crédito 45Z más allá del marco actual hasta 2029. Los beneficios residuales de Ethanol y, en el favorable, de DGD, son supuestos económicos, no concesiones legales futuras.

Bajista: throughput 2,80; refino 9 / 6 / 4 / 3,5 / 3,5; DGD 200 / 100 / 0 / 0 / 0; Ethanol 300 / 250 / 200 / 200 / 200; corporativo 1.200; impuesto 26 %. Favorable: throughput 3,05; refino 20 / 16 / 13 / 10 / 10; DGD 1.000 / 800 / 600 / 300 / 300; Ethanol 700 / 600 / 500 / 400 / 400; corporativo 1.100; impuesto 23 %. Central impuesto 24 %. Los perfiles de costes e inflación están íntegros en model.py.

La tasa central de 10,5 % es una rentabilidad exigida prudencial, no WACC econométrico certificado. Referencia libre de riesgo USD de 4,91 % en H.15 del 2 de noviembre; sensibilidad explícita ±1 punto. La tasa incluye riesgo del ciclo y la incertidumbre de la normalización. No se deduce mecánicamente de una beta histórica favorable. Sin prima adicional oculta o descuento genérico del 15 %.

La caja de reinversión inicial presupone 2.600 M$ anuales de capital industrial y turnaround, más 350 M$ para activos adquiridos mediante financiación de arrendamientos, frente a D&A de 2.800 M$. Es superior a la guía de inversión de 2026 y no confunde D&A con mantenimiento. Incluir activos financiados evita añadir amortización sin financiar su renovación. Los arrendamientos financieros se incluyen en deuda; los operativos conservan renta en costes y no vuelven a añadirse como deuda.

El ingreso contextual es 130.000 M$ en año 1 y 120.000 en año 2, con inflación posterior, ajustado a throughput. Se usa para necesidad de circulante, no para derivar automáticamente márgenes desde precios del crudo. El modelo financia 5 % de aumentos de ventas y **no libera caja por caídas** de precios/ventas. La mejora de beneficio unitario se supone sobre capacidad existente; no implica un ROIC incremental demostrado.

Cada año: reinversión = máximo entre capex total menos D&A más incremento de circulante y NOPAT × g / ROIC. La diferencia se presenta como reserva adicional explícita, de modo que FCFF reconcilia con NOPAT + D&A − inversión − circulante − reserva. Se impone el suelo incluso durante normalización descendente, supuesto conservador que no es desembolso observado. El terminal mantiene el máximo entre el suelo físico de inversión menos D&A más circulante y NOPAT × g / ROIC; no abandona el suelo industrial al terminar los años explícitos.

'''+f'''En el central, EBIT del quinto año es {f(b['rows'][4]['ebit'])} M$; FCFF, {f(b['rows'][4]['fcff'])} M$. El valor terminal descontado representa el {f(b['terminal_fraction_ev']*100)} % del EV. El modelo no depende de mantener los 17.575 M$ de EBIT TTM.

## 5. Puente de capital, con reservas separadas

USD millones. El puente central es **−10.387 M$**. Las partidas históricas son proxies, no balance actualizado ni pasivo transaccional exacto.

|Partida|Importe|Calidad/tratamiento|
|---|---:|---|
|Caja septiembre|+9.840|Excluye 181 de efectivo restringido|
|Caja operativa reservada|−3.000|Supuesto de liquidez, no restricción legal|
|Deuda nominal sin finance leases|−8.635|Tabla de vencimientos, frente a carrying de 8.579|
|Arrendamientos financieros|−2.422|11.001 total book menos 8.579 deuda book|
|Minorías|−3.110|Book proxy; no fair value de DGD|
|Impuestos corrientes por pagar|−1.579|Obligación del beneficio ya generado; NWC futuro excluye impuestos|
|Prestaciones brutas FY2025|−472|No netear activos de planes como caja libre|
|Pasivo contable UTB FY2025|−441|No sustituir por roll-forward fiscal bruto de 315|
|ARO proxy|−193|382 histórico menos 189 pagos Benicia; falta actualización/acreción|
|Pasivos ambientales FY2025|−275|32 corriente + 243 largo; no incluye ARO|
|Estrés adicional repatriación|−100|Supuesto, no obligación identificada|

No sumar 315 y 441 de UTB: son medidas distintas con diferencia de 126 M$ no reconciliada; intereses/penalidades se describen como inmateriales y no justifican esa diferencia por inferencia. Tampoco sumar el superávit neto de pensiones a la caja: hay activos restringidos y obligaciones brutas por planes distintos. Puede faltar separación entre amortización de obligaciones históricas y gasto laboral normalizado; las reservas no certifican ausencia de doble cómputo.

El ARO de 193 es una aproximación mecánica, no saldo septiembre verificado ni mínimo garantizado. La sensibilidad conserva los 382 de cierre de 2025. Los pasivos ambientales históricos tampoco aseguran coste final. Se mantienen expuestos los litigios de Port Arthur y posibles sanciones sin cuantía razonablemente estimable; no se asigna pérdida cero ni un techo artificial.

De la caja, 5.400 M$ están en filiales extranjeras. El emisor indica que el dividendo puede repatriarse sin impuesto federal estadounidense, pero pueden existir retenciones extranjeras, impuestos estatales y efectos fiscales de divisa. La reserva adicional de 100 es solo estrés y podría solaparse con obligaciones ya reconocidas; se muestra su retirada. No se declara caja libre transferible ni un coste fiscal exacto.

El modelo consolida todo DGD y descuenta minoría book; no usa capex atribuible con EBIT consolidado. Su valor económico puede diferir materialmente de 3.110, por eso se sensibiliza ±1.000. Los derivados operativos y créditos de mezcla se tratan dentro del negocio/circulante; no se suman como caja y no se descuentan sus nocionales. Una separación exacta de coberturas y liquidaciones sigue pendiente.

Denominador central: 285 millones, promedio diluido Q3. No garantiza dilución futura máxima. Las 278,8844 millones de acciones reales del 23 de octubre dan sensibilidad distinta y no se usan para anticipar recompras autorizadas. La autorización adicional de 10.000 M$ del 27 de octubre no prueba gasto ejecutado. Dividendo declarado 1,20 USD, registro 24 nov y pago 21 dic, posterior a la referencia de precio; no se descuenta además como si ya fuese una salida de caja observada.

## 6. Sensibilidades e inverso

|Cambio frente al central|USD/acción|
|---|---:|
'''+sens+f'''

El inverso reproduce 387,65 manteniendo los demás supuestos solo si se añaden **{f(m['reverse']['additional_refining_ebit_usd_per_barrel_all_years'])} USD de EBIT por barril a todos los años**. Implica {f(m['reverse']['year5_refining_ebit_usd_per_barrel'])} USD en el quinto año, frente a 6 central y 10,60 del año 2023. No es crecimiento de ventas ni consenso: es el margen adicional exigido bajo este modelo. La búsqueda valida el intervalo, no fuerza una raíz fuera de él.

## 7. Pares y lo que el múltiplo oculta

VLO EV indicativo con nominales y minoría book: {f(p['VLO']['ev_nominal_debt_nci_book_proxy'])} M$, equivalente a **{f(p['VLO']['ev_reported_ebit'])} veces EBIT TTM**, pero **{f(p['VLO']['ev_central_year5_ebit'])} veces** el EBIT central del quinto año. El mismo numerador produce lecturas muy distintas según el ciclo. Es contexto, no EV transaccional completo.

MPC arroja aproximadamente {f(p['MPC']['ev_reported_ebit'])} veces EBIT TTM usando principal financiero y una aproximación bursátil de la minoría pública MPLX, más minorías de sus filiales a book. Omitir MPLX minoritaria reduciría indebidamente el múltiplo. Quedan unidades redondeadas, minorías residuales y diferencias refino/midstream; no se añade una venta anunciada pendiente como caja cobrada.

PSX es un control adicional de calidad, no un múltiplo homologado: su denominador pretax+intereses de 16.930 M$ incluye 1.567 de resultados por puesta en equivalencia y 2.103 de ganancias por ventas. Retirarlos del beneficio sin ajustar simultáneamente los activos del numerador tampoco crea un comparable homogéneo. Refining margin por barril de 38 en Q3 frente a 10,88 en FY2025 evidencia el mismo riesgo cíclico, aunque no equivale al EBIT neto unitario de VLO.

**La valoración central de {f(b['value'])} USD exige normalización del ciclo; el múltiplo TTM aparentemente bajo no demuestra margen de seguridad.** No se ha certificado un conjunto homogéneo completo de EV, FCF propietario y perímetros de todos los pares. Ningún múltiplo de los pares determina el DCF o una entrada.

## 8. Calendario, límites y próximos pasos

Q3 ya publicado y 10-Q presentado el 28 de octubre. La página oficial de próximos eventos no confirma la siguiente fecha trimestral al corte; no se inventa enero. Declaraciones del 10-Q sobre créditos/aranceles no sustituyen una revisión integral de reglas vigentes y licencias. El IRS confirma elegibilidad para combustible vendido hasta el 31 de diciembre de 2029 y requisitos de materias primas norteamericanas desde 2026. Los beneficios 45Z tienen elegibilidad y horizonte legal, no perpetuidad garantizada.

Para cerrar más: actualizar capital histórico y minoría económica, conciliación UTB 441/315, seguros/cobros efectivos y contingencias, reinversión por mantenimiento/ciclo, tratamiento de créditos tras 2029 y comparables totalmente homogéneos. Mantener regulación, calendario y filtros técnicos pendientes antes de cualquier Stage 3.5. Este informe admite valorar supuestos, no ejecutar una operación.

## 9. Reproducción y fuentes

history/portable/ reconstruye 3FY/4Q/TTM desde hechos numéricos primarios sin HTML ni red. model.py, peers.py y qa.py reproducen valoración y controles. El paquete conserva extractos numéricos de las tablas, no los filings íntegros.

'''
for k,u in h['sources'].items():s+=f'- {k}: {u}\n'
s+='- Precio: https://stockanalysis.com/stocks/vlo/history/\n- Calendario: https://investorvalero.com/events-and-presentations/default.aspx\n- EIA: https://www.eia.gov/outlooks/steo/archives/Oct26.pdf\n- IRS 45Z: https://www.irs.gov/credits-deductions/clean-fuel-production-credit\n- Fed H.15: https://www.federalreserve.gov/releases/h15/\n- Pares: enlaces y fechas completos en peers.json y comps/mpc/inputs.json.\n'
(P/'report.md').write_text(s)
