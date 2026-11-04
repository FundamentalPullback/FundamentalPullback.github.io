from pathlib import Path
import json,re
P=Path(__file__).parent
I=json.loads((P/'model/inputs.json').read_text());R=json.loads((P/'model/results.json').read_text());S=json.loads((P/'model/sensitivities.json').read_text());V=json.loads((P/'model/inverse.json').read_text());C=json.loads((P/'capital/facts.json').read_text());H=json.loads((P/'history/history.json').read_text());CP=json.loads((P/'comps/results.json').read_text());W=json.loads((P/'model/rates_results.json').read_text());b=R['base'];bridge=b['capitalBridge']
q=I['sources']['q1'];k=I['sources']['fy26'];rel=I['sources']['release']
def f(n,d=2):return f'{n:,.{d}f}'
def table(head,rows):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)
hrows=H['annual']+[r for r in H['quarters'] if r['period'] in H['last_four_quarters']]+H['ttm']
ht=table(['Período','Ventas','EBIT','NI','CFO','Capex con intangibles','SBC gasto','CFO−capex−SBC'],[[r['period']]+[f(r[x]/1e6) for x in ['revenue','ebit','net_income','cfo','capex_including_intangibles','sbc_expense','fcf_after_sbc_expense']] for r in hrows])
labels={'operatingCashReserveSelected':'Reserva operativa seleccionada','notesPrincipal':'Bonos nominales','financeLeaseProxySelected':'Lease financiero estimado','debtExtraSelected':'Otra financiación de junio','taxReserveSelected':'Reserva fiscal histórica','additionalCurrentTaxReserveSelected':'Reserva fiscal corriente adicional','dividendPayable':'Dividendo posterior al balance','buybackPayable':'Recompras devengadas','additionalCapexReserveSelected':'Capex devengado reservado','definedBenefitOtherClaimReserveSelected':'Reserva otros reclamos'}
ct=table(['Concepto','USD M'],[['Caja septiembre',f(C['cash'])]]+[[labels[n],f(v)] for n,v in bridge['claims'].items()]+[['Puente neto seleccionado',f(bridge['netBridge'])],['Acciones millones seleccionadas',f(bridge['selectedShares'],6)]])
st=table(['Ruta','Ingresos iniciales','Margen inicial/final','WACC','g','ROIC','Resultado por acción condicionado','TV/EV'],[[s,f(d['rows'][0]['revenue']),f"{d['assumptions']['margins'][0]:.1%}/{d['assumptions']['margins'][-1]:.1%}",f"{d['assumptions']['discount']:.1%}",f"{d['assumptions']['g']:.1%}",f"{d['assumptions']['roic']:.1%}",f(d['perShareConditional']),f"{d['terminalPvShare']:.1%}"] for s,d in R.items()])
yt=table(['Fin del período','Ventas','EBIT antes amort. adquirida','Impuesto caja','D&A físico/software','Capex financiado','ΔWC','FCFF'],[[r['periodEnd']]+[f(r[x]) for x in ['revenue','ebitBeforeAcquiredAmort','cashTax','physicalSoftwareDa','fundedTotalCapexEquivalent','workingCapitalInvestment','fcff']] for r in b['rows']])
pt=table(['Empresa','EV/ventas','EV/EBIT','Margen EBIT','CFO−capex−SBC / cap. bursátil'],[[r['ticker'],f(r['evSales']),f(r['evEbit']),f"{r['margin']:.2%}",f"{r['ownerYield']:.2%}"] for r in CP['rows']])
sens='\n\n'.join('### '+key+'\n\n'+table(['Supuesto','Resultado base condicionado'],[[str(r['input']),f(r['perShare'])] for r in S[key]]) for key in ['discount','g','roic','tax','terminalTax','workingCapitalRatio','extraCapexRatio','additionalCapitalizedSbcRatio','marginShift','operatingCashReserveSelected','taxReserveSelected','additionalCurrentTaxReserveSelected','incrementalAwardsSelected','additionalCapexReserveSelected','definedBenefitOtherClaimReserveSelected'])
pro1='LRCX aumenta ventas TTM 33,36% y EBIT 49,31%. La mejora operativa es real, aunque la caja después de capex y SBC crece menos, 18,19%, y no permite confundir beneficios con efectivo disponible.'
pro2='La base instalada favorece servicios, repuestos y mejoras recurrentes. Sin embargo, los 2.486,5 M de ingresos de soporte trimestrales también incluyen equipos Reliant: no todo es suscripción ni ingreso inmune al ciclo.'
con1='El cierre de 221,43 USD supera los tres resultados condicionados del modelo. El inverso necesita aproximadamente 23,59 puntos adicionales de crecimiento anual en los años 2–10, manteniendo el resto del caso base; no es consenso ni una previsión.'
con2='China aporta 35% de las ventas trimestrales. Un cambio de inversión o restricciones de exportación puede afectar volumen, mezcla y márgenes; el récord del trimestre y la guía de diciembre no justifican extrapolar margen del 40% para siempre.'
con3='La capitalización actual, las obligaciones fiscales y la SBC capitalizada no están conciliadas íntegramente. La fecha exacta del próximo resultado tampoco está confirmada: la investigación es condicionada y no aprueba entrada.'
text=f'''# LRCX — crecimiento real, precio exigente y capital del ciclo

Corte: 4 de noviembre de 2026, después del cierre regular de Nasdaq a las 16:00 EST / 21:00 UTC. Investigación parcial condicionada revisada; sin aprobación de entrada. Todos los campos de valor total y rango agregado permanecen null. Los resultados DCF que siguen son cálculos bajo supuestos y un puente seleccionado, no un precio objetivo certificado. USD millones salvo precios/acciones; separadores de tablas en formato internacional.

## Conclusión de investigación

Lam muestra crecimiento fuerte de ventas, beneficio y soporte a la base instalada. Eso no elimina la ciclicidad del gasto de fabricantes de semiconductores, la concentración geográfica ni el coste de financiar capacidad y circulante. El caso base reduce el margen desde el récord trimestral, exige capital físico y económico, conserva SBC y eleva el impuesto terminal. El valor calculado es sensible al coste de capital, al crecimiento duradero y a los márgenes, no principalmente a pequeños ajustes de deuda.

No encuentro margen de seguridad en las rutas seleccionadas frente al cierre de 221,43 USD. Esto no afirma que el mercado deba caer hasta el central ni que el escenario favorable sea un techo: resultados más altos requieren otras hipótesis verificables. La prioridad es comprobar conversión a caja, sostenibilidad del pedido ligado a IA y normalización del ciclo. No se deriva una orden de venta ni de compra.

El último escáner real del registro es 9 de octubre: 318,84 USD, QP80, Opportunity85, RSI51,2 y Stage2 «Sí» histórico. No representa una aprobación técnica del 4 de noviembre. El cierre del 3 de noviembre fue 230,72 y el del 4 de noviembre 221,43; el after-hours no se usa. La caída desde la observación del escáner no prueba infravaloración. Fuente de cierres: https://stockanalysis.com/stocks/lrcx/history/

## Negocio, ventaja y debate verificable

La compañía vende equipos de deposición, grabado y limpieza y servicios asociados para la fabricación de chips. La complejidad de estructuras tridimensionales y la densidad de procesos pueden ampliar su contenido por oblea. La instalación, cualificación del proceso y soporte generan relaciones duraderas, pero no monopolio: los clientes pueden recortar inversión, reutilizar equipos o cambiar el ritmo de adopción tecnológica. La investigación no cuantifica una cuota o TAM nuevos sin fuente primaria.

{pro2}

Sistemas Q1 FY2027: 5.732,9 M frente a 3.547,6 M un año antes; soporte y otros 2.486,5 frente a 1.776,6. La exposición de equipos y upgrades es 46% foundry, 46% memoria y 8% lógica/IDM, distinta del mix de todos los ingresos. China genera 2.885,6 M, Corea 1.634,1 M y Taiwán 1.482,1 M. No se atribuye rentabilidad por país no divulgada. Fuente: {q}

La guía de diciembre publicada el 21 de octubre es ingresos 8.600 M ±400, margen operativo GAAP40,5% ±1 punto y acciones diluidas1.253 M. Es una estimación trimestral de dirección, no nuestros diez años ni una garantía de ejecución. El primer año base de 35.000 M se compara con 32.877,7 M de Q1 anualizado y 34.400 M de la guía anualizada; esos anualizados son referencias de escala, no años reportados. Fuente: {rel}

{con2}

## Historia financiera y calidad de beneficio

{ht}

{pro1}

El histórico conserva GAAP. FY2024 tiene53 semanas y FY2025/26 tienen52; los últimos TTM son52 semanas. Las cifras por acción usan comparativos ajustados por el split10:1 de octubre2024, sin ajustar dos veces. Q4 se obtiene por diferencia anual−9M cuando procede; Q4FY26 EPS/acciones se verifican además en el release. Las medias de acciones y EPS TTM son proxies analíticos ponderados, no una reconstrucción exacta de treasury-stock/antidilución en cada subperíodo. Las fuentes y contextos XBRL quedan en el paquete.

CFO FY26 baja a5.857,7 M desde6.173,3 M pese al aumento del NI: cuentas a cobrar absorben1.961,6 M y deferred profit disminuye286,4 M. Q1FY27 CFO3.497,7 M incorpora535,4 M positivos de cambios en activos/pasivos. Ni anualizo ese CFO sin ajustes ni elimino todo circulante histórico como si nunca se necesitara. El TTM de CFO−capex−SBC es6.133,5 M, proxy de caja del accionista antes de conciliar SBC capitalizada y otros reclamos, no FCFF industrial certificado.

Capex divulgado incluye activos intangibles, sin división completa entre físico y software. D&A FY26 es441,533 M, depreciación383,9 y residual57,633; ese residual NO es amortización adquirida exacta. Q1 D&A122,072 incluye3,016 M de amortización adquirida identificada en el release; el resto119,056 mezcla físico y otros intangibles. No se declara capitalización de software o SBC igual a cero cuando falta desglose. Fuentes: {k} ; {q} ; {rel}

### Ancla normalizada y compensación

Q1 EBIT GAAP3.283,727 + amortización adquirida3,016 + revalorización de pasivos de compensación diferida13,996 − liberación de garantía15,002 =3.285,737 M. Por cuatro da13.142,948 M antes de amortización adquirida. La corrección de garantías evita dar por permanente el beneficio de una liberación histórica. No supone que todas las liberaciones futuras sean ilegítimas.

Se neutraliza solo la revalorización financiera del pasivo EDC, cuyo activo relacionado genera12,870 M fuera del EBIT. Se conserva el coste normal de remuneración y SBC. Los activos/pasivos EDC no se suman brutos al puente; se explica su correspondencia más abajo. No se elimina otra compensación, I+D ni inversión habitual. Fuente de ajustes: {rel} y garantía Note12 del {q}

La normalización no fabrica un escudo fiscal de amortización adquirida. Se calcula impuesto sobre EBIT económico previo a esa amortización; al presentar EBIT contable y D&A total, la amortización se resta y añade una vez. Al ponerla a cero los tres valores permanecen iguales. El crecimiento sigue financiado, incluso cuando mejora el margen.

## Capital: balance fechado, reclamos y reservas seleccionadas

{ct}

La caja de7.437,384 M excluye13,506 M restringidos. Los3.750 M son principal de bonos, no los3.735,444 M de deuda y leases a valor contable combinados. Junio concilia3.722,061 M de deuda contable con12,502 M de leases financieros; septiembre no desglosa el lease. Uso15 M como proxy y0,147 M de otra financiación de junio, con sensibilidad, sin llamar exacta a la deuda actual. Los leases operativos se mantienen como coste, sin añadir su pasivo y dejar luego intacto un múltiplo incompatible. Fuentes: {q} ; {k}

El principal de bonos vence en2029,2030,2049,2050 y2060; no se confunde cupón histórico con coste de financiación marginal. Los programas de papel comercial y línea revolvente disponibles no son caja ni deuda dispuesta. La ausencia de un puente completo hasta noviembre se declara, no se rellena con transacciones supuestas.

Se reserva947,249 M por864,149 M de incertidumbre fiscal bruta de junio más83,1 M de intereses/penalizaciones. La nota contractual señala762,4 M de pasivos relacionados, de distinto perímetro. No sumo otra vez684,273 M de impuesto largo de septiembre. La reserva elegida no es un pago cierto ni una liquidación fiscal certificada. Los impuestos corrientes y otros suben263,205→800,781 M; añado300 M seleccionados y pruebo0/300/537,576/800,781. Puede solapar con la reserva operativa y el desfase corriente, por lo que no lo presento como deuda fiscal exacta. El transition tax anterior ya se liquidó en FY26; no se vuelve a deducir. Fuentes: Note7/17 del {k} y Note11 del {q}

Los412,218 M de dividendos y31,512 M de recompra devengada se restan una sola vez. El dividendo0,33 por acción se programó para14oct, después del balance; no lo trato como pago aún futuro al4nov. Fuente: https://investor.lamresearch.com/2026-08-27-Lam-Research-Corporation-Announces-a-27-Increase-in-Quarterly-Dividend El ASR de1.000 M ya estaba pagado en septiembre: no se resta de nuevo ni se acreditan acciones finales no entregadas; la liquidación se esperaba en el trimestre terminado27dic. Las1.249,171 M acciones son las informadas al20oct, no el cap table del4nov. Se añaden6,6 M seleccionadas, aproximación de5,930 M RSU más opciones netas a partir de0,916 M opciones/strike60,48 de junio. Se prueba4,885/6,6/10/15 M. La media diluida Q1 y el incremento4,885 M son contrastes, no acciones actuales exactas. Parte de los premios no vested exige servicio futuro y puede solapar con la SBC futura conservada; la aproximación6,6 no resuelve ese solapamiento y por eso no certifica el capital actual. Fuente: {q} ; {k}

El pasivo EDC de junio498,5 M tiene inversiones relacionadas511,8 M; se excluyen ambos, sin afirmar que los13,3 M netos sean efectivo distribuible hoy. Se prueba neto−100/0/+13,3. La reserva50 M para beneficios definidos u otros reclamos no conciliados es una hipótesis prudente, no un déficit de pensiones reportado. No se suma el valor contable de goodwill ni activos fiscales al valor del negocio. Fuente: Note16 del {k}

Los141,965 M de capex devengado se reservan aparte suponiendo capex futuro incremental; la sensibilidad0/141,965/283,93 muestra posible solapamiento. La transferencia de inventario a PPE37,053 M en Q1 no es equipo gratuito: parte ya pasó por caja operativa. Los compromisos de compra1.481,195 M de junio y garantías potenciales290,3 M de septiembre no se restan como deuda cierta adicional: los suministros y garantías ordinarias están en márgenes/capital, mientras cancelación y contingencias requieren seguimiento. No se afirma que su riesgo sea cero. Fuentes: {k} ; {q}

## Método DCF y financiación de crecimiento

Se modelan diez períodos anuales móviles terminados el4nov2027…4nov2036, con cobro al final del período. No son FY de junio ni se añade un año completo de caja ya cobrada. Hay sensibilidad a cobros medios0,5 años antes. El ancla de inversión es el negocio Q1 anualizado; un stress usa TTM en vez del run-rate. Ninguna de las dos bases certifica que todo el capital necesario para el crecimiento ya esté colocado.

Para cada período: NOPAT económico = ventas × margen antes de amortización adquirida ×(1−24%). Inversión neta económica = máximo(0, cambio de NOPAT)/ROIC. Piso físico = máximo(0, capex−D&A físico/software)+20% del crecimiento positivo de ventas. Se usa el mayor, no se suman ambos indiscriminadamente ni se deja crecer margen sin capital. No hay liberación automática de circulante cuando caen ventas. Capex equivalente financiado = D&A + inversión neta elegida−ΔWC.

El capex físico mínimo es5%/4%/3,5% de ventas en adverso/base/favorable; D&A físico/software1,5% en los tres, frente a119,056/8.219,418=1,45% Q1. Son hipótesis de capacidad, no solo mantenimiento reportado. SBC gasto permanece en margen. No hay dato separado de SBC capitalizada: se prueba coste extra0,25%/0,5% de ventas; el central sin cargo extra no certifica que sea cero ni que no esté en capex o margen.

En terminal se conserva el mayor de NOPAT×g/ROIC y capex mínimo−D&A+ΔWC. No desaparece el piso físico al acabar el año10. El impuesto terminal seleccionado es26%, frente a24% durante la proyección. La ventaja fiscal de Malasia tiene15 años desdeFY2022; el beneficio967,9 M enFY26 no se perpetúa sin nueva verificación. Los porcentajes seleccionados no son asesoramiento fiscal ni una predicción exacta de la mezcla por país. Fuente de incentivo y ETR: {k}

### Tasa de descuento

Treasury10Y del4nov4,90%; ERP implícita del1nov4,41%; beta5Y del proveedor2,01. CAPM de equity {W['costEquity']:.4%}. Con deuda nominal/proxy y coste marginal seleccionado6% después de impuesto24%, WACC indicativo {W['waccProxy']:.4%}. El14% base incluye un colchón discrecional de {W['selectedPremiumBasisPoints']:.1f} puntos básicos, no un redondeo obligatorio. Adverso16% y favorable12% reflejan distintos riesgos. La ERP se publicó usando otro risk-free5,29%; fechas distintas y beta histórica limitan la precisión. Se prueban10–18%; no se adopta el WACC automático del proveedor.

Fuentes: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve ; https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm ; https://stockanalysis.com/stocks/lrcx/statistics/

### Tres rutas condicionadas

{st}

Adverso: corrección de inversión con ingresos iniciales29.000 M, otra caída10% en año2, recuperación moderada y margen27–30%. Base:35.000 M, crecimiento de10% hacia3%, margen39% hacia36%, ROIC35%. Favorable:38.000 M, crecimiento15% hacia4%, margen hasta43% y40% terminal, ROIC45%. No se asignan probabilidades ni se mezclan como valor esperado. Las ventas finales son {f(R['bear']['rows'][-1]['revenue'])}/{f(b['rows'][-1]['revenue'])}/{f(R['bull']['rows'][-1]['revenue'])} M.

{yt}

La tabla usa EBIT antes de amortización adquirida y solo D&A residual físico/software, por lo que concilia directamente caja sin doble addback. El CSV adicional muestra también EBIT contable, amortización adquirida y D&A total. El piso económico domina {R['bear']['economicDominatesYears']}/10, {b['economicDominatesYears']}/10 y {R['bull']['economicDominatesYears']}/10 años; en los demás domina el físico/circulante. Una sensibilidad plana local no hace irrelevante el capital.

Terminal base: ventas{f(b['terminal']['revenue'])}, NOPAT{f(b['terminal']['nopat'])}, inversión{f(b['terminal']['netInvestment'])}, FCFF{f(b['terminal']['fcff'])}. Valor empresarial{f(b['enterpriseValue'])}, puente{f(bridge['netBridge'])}; denominador seleccionado{f(bridge['selectedShares'],6)} M. La precisión aritmética no elimina la incertidumbre económica.

## Qué exige el precio

{con1}

La solución del inverso es +{V['growthShift']['solution']:.4%} a cada crecimiento de los años2–10; el año1 y demás parámetros permanecen constantes. Se comprueba monotonicidad en0–40 puntos. El recorrido inverso lleva las ventas del año10 a aproximadamente352.163 M, una exigencia muy superior al caso base, no un pronóstico. No equivale a sumar23,59% al valor ni a una probabilidad del escenario. El inverso de margen en0–30 puntos no alcanza221,43 bajo el resto de condiciones; no extrapolo un margen imposible ni presento «sin solución» como prueba de imposibilidad del negocio.

## Comparación relativa actual, sin convertir mediana en objetivo

{pt}

Cierres regulares4nov: LRCX221,43; KLAC149,83; ASML1496,33USD. Para ASML FX ECB4nov1,1267USD/EUR, informes US GAAP y acciones medias diluidas383,5 M como proxy. KLA usa acciones1.302,962435 M al26oct y deuda principal5.950 M, sin reconciliación exhaustiva de leases en el panel; +50 M altera su EV/EBIT solo ligeramente. LRCX usa principal y15,147 M seleccionados de leases/otra financiación. Los balances siguen siendo septiembre: no son balances del cierre bursátil.

ASML tiene otra tecnología, valoración de activos estratégicos y necesidades de circulante. Su rendimiento de caja4,08% contiene7.876,9 M de cambios agregados en activos/pasivos; al retirarlos como stress baja a2,53%, sin llamarlo caja recurrente limpia. LRCX tiene menor EV/EBIT que ambos pares, pero los tres pueden incorporar expectativas exigentes. La comparación no sustituye el DCF ni demuestra compra relativa.

Fuentes pares: https://ir.kla.com/sec-filings/annual-reports/content/0000319201-26-000027/klac-20260630.htm ; https://ir.kla.com/sec-filings/all-sec-filings/content/0000319201-26-000034/klac-20260930.htm ; https://www.sec.gov/Archives/edgar/data/937966/000162828026011378/asml-20251231.htm ; https://investor.asml.com/static-files/d310262b-d037-485d-83b5-92c93cc462f0 ; https://investor.asml.com/static-files/78b1af6f-9c6e-4e5c-b229-a418251687ff ; https://investor.asml.com/static-files/8eb7be33-3fef-490d-a21c-f02161a47268

Precios y FX: https://stockanalysis.com/stocks/klac/history/ ; https://stockanalysis.com/stocks/asml/history/ ; https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml

## Sensibilidades reproducibles

No son un intervalo de confianza. Se cambia una hipótesis cada vez; combinaciones pueden producir resultados distintos.

{sens}

El stress de base de inversión TTM, sin normalizar sus ajustes, da {f(S['anchorTtmInsteadOfQuarter']['perShare'])}; usa una base menor de capital/beneficio y obliga a financiar más crecimiento inicial. Cobro a mitad de período da {f(S['midyearShift'][1]['perShare'])} frente a {f(S['midyearShift'][0]['perShare'])}. El neto EDC y leases se prueban en el JSON, sin cambiar centrales.

China: recortes persistentes10%/25%/50% de la exposición de35%, acompañados de compresión de margen0,5/1,25/2,5 puntos, generan {f(S['chinaExportStress']['0.1']['perShare'])}/{f(S['chinaExportStress']['0.25']['perShare'])}/{f(S['chinaExportStress']['0.5']['perShare'])}. No son pronóstico geográfico, elasticidad observada ni asesoramiento sobre reglas concretas de exportación.

## Catalizadores, falsadores y tareas pendientes

- Últimos resultados confirmados:21oct, trimestre terminado27sep;10-Q22oct. No hay un evento trimestral nuevo pendiente de publicar de ese corte.
- La página oficial de eventos consultada no muestra una próxima convocatoria exacta. No sustituyo esto por una estimación de enero ni marco calendario como validado: https://investor.lamresearch.com/events
- Vigilar cierre del ASR en trimestre de diciembre y conciliar caja/acciones antes de un puente actual. No reconocer de antemano acciones restantes.
- Falsador favorable: cartera y capacidad de clientes sostienen varios años de crecimiento superior, con conversión a caja y rentabilidad incremental que financian la inversión; requerir evidencia, no solo la guía de un trimestre.
- Falsador adverso: desaceleración de China o memoria, cancelaciones/diferimientos, caída de margen y nuevas cuentas a cobrar/inventarios que consumen caja.
- Revisar tasa fiscal efectiva/cash taxes e incentivo de Malasia; separar pasivos históricos de impuesto recurrente. Conciliar SBC capitalizada y premios pendientes, no extrapolar medias diluidas.
- Rehacer Stage2 con datos contemporáneos y reglas vigentes si vuelve a interesar; este informe no hace esa validación ni cambia el plan.

{con3}

Confianza alta en los estados y cálculos reproducibles, media en normalización, baja-media en diez años/ciclo y capital actual. La calidad de una fuente no es autorización de inversión. La ficha mantiene null en valor total/rango y no habilita Stage3 integral, latestCompleted, Stage3.5 ni entrada.

## Evidencia breve ES/EN

{pro1}

TTM revenue rose 33.36% and EBIT 49.31%, but cash after capex and SBC grew only 18.19%. Operating improvement is real; accounting profit is not the same as distributable cash.

{pro2}

The installed base supports services, spares and upgrades. However, quarterly support revenue of USD2,486.5m also includes Reliant equipment, so it is not all subscription revenue or immune to the cycle.

{con1}

The USD221.43 close exceeds all three conditional model outputs. The reverse model needs about23.59 additional percentage points of annual growth in years2–10 under other base assumptions; this is not consensus or a forecast.

{con2}

China represents35% of quarterly sales. Investment changes or export restrictions can affect volume, mix and margins; record results and December guidance do not justify a perpetual40% operating margin.

{con3}

Current capitalization, tax claims and capitalized SBC are not fully reconciled. The exact next earnings date is unconfirmed; this conditional research does not approve an entry.
'''
urls=[]
def keep(m):
 urls.append(m.group(0));return 'URLPLACEHOLDER'+chr(65+len(urls)-1)+'END'
text=re.sub(r'https://[^\s;]+',keep,text)
text=re.sub(r'(?<=[A-Za-zÁÉÍÓÚáéíóúñÑ])(?=[0-9])',' ',text)
text=re.sub(r'(?<=[0-9])(?=[A-Za-zÁÉÍÓÚáéíóúñÑ])',' ',text)
for n,u in enumerate(urls):text=text.replace('URLPLACEHOLDER'+chr(65+n)+'END',u)
text=text.replace('—','·')
(P/'report.md').write_text(text)
print('report',len(text))
