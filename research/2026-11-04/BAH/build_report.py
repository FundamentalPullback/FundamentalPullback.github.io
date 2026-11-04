import json
from pathlib import Path
p=Path(__file__).parent
j=lambda f:json.loads((p/f).read_text())
h=j('history/history.json');m=j('model/results.json');c=j('comps/outputs.json')
s='''# BAH: caja fiscal favorable, negocio en contracción y capital pendiente
Corte: 4 noviembre 2026, después del cierre regular. Investigación parcial condicionada, revisada de forma independiente, sin aprobación de entrada. Millones de USD salvo precios, porcentajes y acciones en millones. No valoración total, no Stage 3 completo ni aprobación de entrada.

El escáner del 4 noviembre muestra 89,00, QP90, Opportunity90 y RSI75,4. El cierre regular independiente es 88,28; no se sustituye por el after-hours. El escáner no certifica los filtros técnicos actuales. [Precio](https://stockanalysis.com/stocks/bah/history/).

## Conclusión
La mejora de caja no demuestra recuperación orgánica: el FCF TTM crece 165 millones mientras los impuestos pagados caen 154 millones. Los ingresos y el EBIT TTM retroceden. La compra de negocios, el capital invertido fuera del negocio y los pasivos históricos requieren reconciliación antes de atribuir un valor total por acción.

Seguridad nacional mantiene ventas trimestrales de 2.076 millones frente a 2.063 millones, mientras el negocio civil/comercial cae a 702 millones desde 827 millones. Esta resistencia relativa no elimina la contracción consolidada.

La cartera total de 40.933 millones incluye sólo 5.711 millones financiados; 10.409 millones son no financiados y 24.813 millones opciones. No equivale a ingresos garantizados ni caja disponible.

## Fuentes y calendario
[10-Q septiembre](https://www.sec.gov/Archives/edgar/data/1443646/000162828026066973/bah-20260930.htm), [10-K marzo](https://www.sec.gov/Archives/edgar/data/1443646/000162828026037521/bah-20260331.htm), [10-Q diciembre previo](https://www.sec.gov/Archives/edgar/data/1443646/000162828026003187/bah-20251231.htm), [10-Q septiembre previo](https://www.sec.gov/Archives/edgar/data/1443646/000162828025046176/bah-20250930.htm).
[Resultados Q2FY27 publicados 23 octubre](https://newsroom.boozallen.com/static-files/f4c6cabc-65a4-4d4d-9930-c16e944d236f), [resultados FY26](https://investors.boozallen.com/static-files/fc687e94-0782-4c91-ae05-c0c67a4e7d14), [resultados Q2FY26](https://investors.boozallen.com/static-files/fe57e0cb-cbcb-4a1d-a6b2-1f289215bb87).
No se localizó confirmación primaria de la próxima fecha exacta de resultados. El dividendo de 0,59 tiene registro el 12 noviembre y pago el 4 diciembre: no es un evento de resultados. Calendario de entrada pendiente.

## Historia reproducible
Tres ejercicios, últimos cuatro trimestres y TTM comparable, cifras publicadas o diferencias explícitas. CFO y capex Q2FY27 de 294 y 31 proceden del comunicado trimestral; el resto del flujo trimestral se reconstruye por diferencias de acumulados. Valores redondeados por emisor: no precisión económica de dólares individuales. TTM es cálculo propio, no tabla TTM publicada.

|Periodo|Ingresos|EBIT|NI|CFO|Capex|FCF|SBC|Impuestos pagados|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for k in ['FY2024','FY2025','FY2026','Q3FY26','Q4FY26','Q1FY27','Q2FY27','TTM20250930','TTM20260930']:
 d=h[k];s+='|'+k+'|'+'|'.join('ND' if d[v] is None else f'{d[v]:,.0f}' for v in ['revenue','ebit','netIncome','cfo','capex','fcf','sbc','cashTax'])+'|\n'
s+='''
La ilustración fiscal sustituye pagos efectivos por 26% del beneficio antes de impuestos reportado: 835,62 de FCF actual frente a 804,34 previo. No es FCFF normalizado: conserva interés, circulante y cambios de perímetro. El FCF menos SBC es diagnóstico, no otro flujo que sumar al DCF.

FY25 incluía liberación de provisión de costes reclamados de 113 en ingresos y recuperación de seguros de 115 en G&A. Una ilustración que los elimina deja ingresos 11.867 y EBIT1.142. Ambos ocurrieron en septiembre2024, fuera de los dos TTM comparados; no se vuelven a restar de ellos. FY26 tuvo 61 de indemnizaciones, no idénticos a los 33 excluidos del EBITDA ajustado: se retienen costes en el ancla. El beneficio fiscal de 86 en H1FY26 y el interés sobre reembolsos tampoco son mejora operativa. H1FY27 no repite aquella liberación de 86. Other income incluye10 de earnout por contratos vendidos enFY26, fuera de EBIT: no se resta del ancla operativa ni se presenta como EBIT recurrente.

Amortización adquirida TTM: 48 FY26 +37 H1FY27 −24 H1FY26 =61. EBIT1017+61=1078; D&A178−61=117. El ancla retiene SBC77 y costes de personal/transacción. Se grava el EBIT antes de amortización al26%, sin crear un escudo fiscal adicional por el addback. Software y SBC capitalizada no tienen conciliación completa separada; el suelo de capex y sus sensibilidades no certifican ese coste omitido.

## Negocio y adquisiciones
Ingresos Q2 caen3,9%; excluyendo gastos facturables bajan0,8%. El EPS ajustado crece18,1%, influido por impuestos y recompras: no se interpreta como crecimiento orgánico. Plantilla31.000 frente32.500, personal de cliente28.200 frente29.600. RPO11.800, con65% previsto en12meses y75% en24, no es efectivo comprometido incondicionalmente.
La guía FY27 es ventas11.300–11.600, EBITDAajustado1260–1290, EPSajustado6,50–6,70, FCF850–925 y capex aproximado200. El impuesto guiado16–19% no se perpetúa: modelo26%.
Ultra cerró24agosto por729, con goodwill501, intangibles284 y pasivos netos56. Defy cerró6abril por235, goodwill128, intangibles88 y activos netos19. La caja y deuda septiembre ya incluyen las adquisiciones: no deducir otra vez964. El flujo de compras neto934 difiere del precio bruto y no se inventa conciliación exacta. Defy incorpora cuentas por cobrar y pagar importantes; no se tratan sus cobros como crecimiento libre de inversión. Sin proforma anual homogéneo de ambos negocios, el ancla TTM es un perímetro mixto.

## Puente seleccionado, no capital certificado
Caja334 se reserva íntegra para operación. Principal deuda4441 frente carrying4410: diferencia31 de costes de emisión; no sumar ambas ni duplicar1200 de nuevas notas. Revolver1500 no dispuesto no es caja. Se mantienen rentas operativas y no se resta de nuevo toda la deuda de leases. Nuevas oficinas:240 de compromisos no descontados,61 de allowances y122 reconocidos de ROU, no una deuda adicional íntegra encima de rentas.
Reserva médica180 corresponde a marzo, no saldo de noviembre. Los233 de beneficios a largo plazo y118 corrientes incluyen otros conceptos; no sumar180+233+118. Sensibilidades de incremento53/171 reconocen la laguna. Coste de servicio7 queda en operaciones; interés10 fuera de EBIT. ECAP corriente es principalmente remuneración ordinaria, no automáticamente deuda previsional.
Se seleccionan85 de posiciones fiscales inciertas,249 por costes reclamados DCAA,187 de compromisos con fondos,6 de recompras pendientes y70,8 de dividendo sobre120 acciones proxy. Puede existir solapamiento con la reserva de caja y obligaciones operativas; no se certifica cierre exacto. El modelo prueba devolver249 o334 al puente.
Los519 de inversiones contables y182 de devolución fiscal pendiente de revisión JCT se excluyen del crédito de activos, no se declaran sin valor. Tampoco se presenta el residuo como cota inferior: deducir compromisos sin tasar activos asociados es un estrés asimétrico. Activo y pasivo de compensación diferida44 se excluyen emparejados; fondo monetario262 ya está dentro de caja334.
Acciones básicas119,096968 septiembre frente118,602638 en portada19octubre. El modelo elige120 diluidas como proxy, no tabla actual de premios. Los datos de marzo de RSU0,946327 y opciones0,513969 a73,63 no bastan para actualizar noviembre. Se prueban118,602638/120/122. Recompras posteriores y equity awards siguen sin conciliación completa. Item5 del10-Q informa una modificación del20octubre:16,67% de ciertas RSU de ejecutivos vestirá el6noviembre y83,33% en diez cuotas trimestrales desde13enero2027. No se conoce aquí la cantidad neta incremental ni su solapamiento con120M: no se vuelve a sumar automáticamente. Es un evento próximo de capital, no resultados.
Puente escogido:334−334−4441−180−85−249−187−6−70,8 = −5218,8.

## Modelo y financiación
Diez años móviles desde el corte, no FY2027 completo descontado como año exacto. No hay stub adicional ni compra gratis. Fiscal26%; reinversión es el máximo entre aumento positivo de NOPAT/ROIC y suelo físico: capex menos D&A residual más12% del aumento positivo de ventas. No se libera automáticamente circulante durante contracción. Capex mínimo200 escalado por ventas, al menos125% de D&A; el terminal conserva ese suelo. Márgenes crecientes requieren capital bajo el modelo central; alternativa de eficiencia sin inversión por toda mejora de margen queda separada.
Base: crecimiento3/4/4/3,5/3% y convergencia a2,5%; margen10/10,3/10,5/10,7/11%; ROIC20%, descuento9%. Adverso: crecimiento−4/−2/0/1/2%, margen9/8,8/8,8/9/9%, ROIC15%, descuento11%, g2%. Favorable:6/7/6/5/4%, margen11/11,5/12/12/12%, ROIC25%, descuento8%, g2,5%. Son hipótesis propias, no guía.
Treasury4,90%, ERP4,41% y beta histórica0,28 dan coste de equity mecánico6,1348%; deuda elegida5,5%, impuesto26%. El9% central incorpora prima discrecional por riesgo de financiación/perímetro y fragilidad de beta; no es redondeo del WACC. [Treasury](https://home.treasury.gov/resource-center-data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026), [ERP](https://pages.stern.nyu.edu/~adamodar/), [beta](https://stockanalysis.com/stocks/bah/statistics/). Modelo/rates.json separa cálculo y selección.

|Caso|EV operativo|Puente escogido|Residuo por acción condicionado|Peso terminal|
|---|---:|---:|---:|---:|
'''
for k,o in m['cases'].items():s+=f"|{k}|{o['ev']:.2f}|{o['bridge']:.2f}|{o['conditionalResidual']:.4f}|{o['terminalShare']:.2%}|\n"
s+='\nEstos residuos no son precios objetivo, rango de valor total ni valoración integral de BAH.\n\n### Diez años base\n|Año|Ventas|EBIT preamortización|NOPAT|D&A residual|Capex suelo|WC|Reinversión financiada|FCFF|\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in m['cases']['base']['rows']:s+='|'+str(r['year'])+'|'+'|'.join(f'{r[k]:.2f}' for k in ['revenue','ebitBeforeAcquiredAmort','nopat','physicalSoftwareDa','capex','wc','reinvestment','fcff'])+'|\n'
s+='\n### Sensibilidades base, una variable cada vez\n'
for k,vs in m['sensitivities'].items():s+=k+': '+ '; '.join(f"{v['input']}: {v['value']:.2f}" for v in vs)+'.\n\n'
s+='''Los parámetros discount/tg/wc/tax/roic se expresan como fracciones:0,09=9%. Las sensibilidades de activos son créditos brutos seleccionados, no tasaciones. Ninguna combinación valida financiación o dilución.

El inverso para88,28 exige4,5431puntos adicionales de margen, terminal15,5431% y FCFF inicial−880,26. La reserva operativa no financia ese déficit; una disposición del revolver alteraría deuda/coste y está sin certificar. No se elimina el déficit ni se denomina precio justo. Ambas raíces usan bracket, residual y barrido monótono de1000intervalos. La alternativa de eficiencia figura por separado en resultados, no sustituye el caso financiado.

## Contraste relativo limitado
'''
for k,v in c.items():s+=f"{k}: EVproxy{v['proxyEv']:.2f}, EBITGAAP TTM{v['ttmGaapEbit']:.3f}, EV/EBITproxy{v['proxyEvEbit']:.2f}x.\n"
s+='''
Ambos usan acciones diluidas medias del último trimestre y deuda carrying, no cap table exacta actual. El DCF BAH usa principal, diferencia explícita31. Se retiene amortización/SBC en EBIT y rentas en gastos; no se homogeneizan pensiones, activos, fiscalidad ni adquisiciones. No se aplica una mediana como objetivo.
CACI crece8,2% en Q1, con2,1% orgánico, frente contracción BAH. La diferencia de múltiplo no demuestra infravaloración. CACI CFO161,314 menos PPE11,359=149,955 difiere de FCF reportado133,5 por exclusión MARPA: no mezclar sin ajuste con BAH. ARKA altera su perímetro. [CACI Q1](https://investor.caci.com/2026-10-21-CACI-Reports-Results-for-Its-Fiscal-2027-First-Quarter), [FY26](https://investor.caci.com/2026-08-05-CACI-Reports-Results-for-Its-Fiscal-2026-Fourth-Quarter-and-Full-Year-and-Issues-Fiscal-Year-2027-Guidance), [cierre632,28](https://stockanalysis.com/stocks/caci/history/).

## Qué falta y qué cambiaría la tesis
Confirmar próxima fecha de resultados y filtro técnico; conciliar capital noviembre, premios, pensiones y obligaciones; tasar inversiones y fiscalidad, aislar proforma de adquisiciones y coste de software; ampliar pares homogéneos. Recuperación civil, backlog financiado que convierta a caja y EBIT sin beneficio fiscal apoyarían la tesis. Caídas de adjudicaciones, presión presupuestaria, desviaciones DCAA, costes de integración y capex estructural superior la debilitan. La información disponible no certifica entrada.

## Reproducción
Ejecutar reproduce.py sin red. Subconjunto factual XBRL, historia, normalización, capital, modelo y pares son propios y reproducibles. Se excluyen filings completos y datos privados. Datos publicados redondeados y modelos seleccionados no constituyen auditoría contable.
'''
(p/'report.md').write_text(s)
