from pathlib import Path
import json
P=Path(__file__).parent
R=json.loads((P/'results.json').read_text());S=json.loads((P/'sensitivity.json').read_text());F=json.loads((P/'source_review/financials.json').read_text());T=json.loads((P/'technical.json').read_text());I=json.loads((P/'model/inputs.json').read_text());b=R['base']
def n(x,d=2):return f'{x:,.{d}f}'.replace(',','X').replace('.',',').replace('X','.')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |'for r in rows)+'\n'
hist=table(['Periodo','Ventas','EBIT GAAP','Beneficio neto','EPS diluido','CFO','Capex','FCF estricto'],[[p,n(F[p]['revenue'],0),n(F[p]['ebit'],0),n(F[p]['net_income'],0),n(F[p].get('eps'),2)if F[p].get('eps')is not None else'—',n(F[p]['cfo'],0),n(F[p]['capex'],0),n(F[p]['cfo']-F[p]['capex'],0)]for p in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM_2025_09','TTM_2026_09']])
annual_fcfps='/'.join(n((F[p]['cfo']-F[p]['capex'])/F[p]['shares_diluted']) for p in ['FY2023','FY2024','FY2025'])
quarter_fcfps='/'.join(n((F[p]['cfo']-F[p]['capex'])/F[p]['shares_diluted']) for p in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])
current_fcfps=n((F['TTM_2026_09']['cfo']-F['TTM_2026_09']['capex'])/b['shares'])
forecast=table(['Año','Ventas','Margen EBIT','NOPAT','D&A','PPE/capex agregado','M&A','Δ circulante + contratos','Reinversión neta','FCFF'],[[r['year'],n(r['revenue'],0),n(r['ebit_margin']*100)+'%',n(r['nopat'],0),n(r['da'],0),n(r['ppe_or_aggregate_capex'],0),n(r['acquisition_cash'],0)if r['acquisition_cash']is not None else'En agregado',n(r['nwc_increment']+r['contract_capitalization'],0),n(r['net_reinvestment'],0),n(r['fcff'],0)]for r in b['rows']])
cases=table(['Escenario','WACC','Valor actual/acción','Frente a65,78','Peso terminal/EV'],[[{'bear':'Adverso','base':'Central','bull':'Favorable'}[c],n(R[c]['wacc']*100)+'%',n(R[c]['per_share']),n(R[c]['upside']*100)+'%',n(R[c]['terminal_pct_ev']*100)+'%']for c in ['bear','base','bull']])
bridge=table(['Paso','Valor/acción','Cambio'],[[{'Approximate A120 narrative reconstruction':'Reconstrucción aproximada de A120','Same old operating assumptions, only WACC8.51757%':'Misma operación antigua; solo WACC 8,51757%','New growth/cohorts/tax/reinvestment/terminal and timed acquisition cash, no Q4stub; old capital/share bridge':'Nueva operación, reinversión, terminal y fechas de M&A; sin stub y con puente antiguo','Add estimated economic Q4stub':'Añadir stub económico estimado de Q4','New pension/earnout/capital-return reserve and current diluted denominator':'Nuevo puente de capital y denominador diluido'}.get(r['step'],r['step']),n(r['value']),n(r['change'])if'change'in r else'—']for r in S['migration_bridge']])
text=f'''# CTSH | Candidata a precio razonable, con aprobación fundamental condicional

**Corte: 5 de noviembre de 2026. Precio:65,78 USD, cierre regular del4 de noviembre.** Los64,18 USD del scanner eran negociación posterior al cierre y no se utilizan como precio regular. Unidades financieras: millones deUSD, salvo importes por acción. Negocio: Cognizant Technology Solutions, servicios de tecnología y transformación empresarial.

## Dictamen y límites

CTSH **puede pasar Stage3 como candidata a una entrada pequeña a precio razonable**, con máximo fundamental condicionado de**66,50 USD**. No es una compra ejecutable, ni se considera una infravaloración robusta. Stage3.5 sigue pendiente: faltan patrimonio, efectivo, órdenes y presupuestos vigentes verificados, y la señal propuesta es futura. No se ha enviado una orden ni se ha supuesto una ejecución.

El FCFF financiando adquisiciones arroja**{n(b['per_share'])} USD** centrales frente a65,78: potencial{n(b['upside']*100)}%, margen de seguridad{n((1-I['price']/b['per_share'])*100)}% respecto a ese escenario. El rango central plausible es aproximadamente**64–80 USD**; no se llama justo a todo el intervalo adverso/favorable. El caso adverso completo vale**{n(R['bear']['per_share'])}**, alrededor de21% por debajo del precio, y no es una pérdida máxima. La confianza es**media, condicionada a la conversión de caja y a la disciplina de adquisiciones**.

La autorización fundamental se apoya en beneficio operativo positivo y sostenible, baja deuda financiera neta, expectativas moderadas y un descuento al escenario central. No depende de multiplicar el EPS mediante recompras gratuitas. Su debilidad es clara: la mejora de caja prevista todavía debe materializarse; crecimiento orgánico y márgenes no permiten llamar a la tesis de alta visibilidad. Combinaciones razonables más exigentes valoran la acción alrededor de64USD. Comprar cerca de65,78 supone aceptar ese riesgo, no haberlo eliminado.

El máximo66,50 deja{n((1-66.5/b['per_share'])*100)}% por debajo del valor central, algo más que la referencia inicial de15% del plan. Se redondea hacia abajo para no fingir precisión. El pequeño aumento del descuento responde al crecimiento normalizado inferior a5% y a la caja por demostrar. **No es una nueva regla universal**, ni se suma mecánicamente otra penalización al adverso. Si cotiza sobre ese máximo, se suspende la propuesta hasta revisión con evidencia nueva, no se eleva el límite para perseguirla.

## Historia: el EPS está creciendo más que el negocio

{hist}

FCF estricto = CFO menos compras de propiedad/equipo, incluido software capitalizado. Los trimestres de caja son diferencias de estados acumulados; EPS y acciones medias trimestrales son cifras publicadas, no restas de promedios anuales. El EPS TTM de5,48 usado como contraste de PER es la suma de cuatro EPS trimestrales, cuyos denominadores difieren.

El FCF estricto dividido por acciones medias diluidas publicadas fue{annual_fcfps}USD en2023/2024/2025. En los últimos cuatro trimestres fue{quarter_fcfps}USD; no se anualiza el trimestre fuerte. El TTM2.363m equivale a{current_fcfps}USD con el denominador diluido actual estimado448,83m, que no es una serie histórica perfectamente comparable de FCF por acción.

Las ventas TTM crecen4,96%. Para comparar EBIT se retiran exclusivamente la ganancia inmobiliaria de62m del periodo previo y la reversión de81m de pasivos deIndia del actual, manteniendo reestructuraciones:3.225m→3.361m,**+4,22%**. El FCF comparable cae2.651m→2.363m,**−10,86%**. Si además se excluyen reestructuraciones, el EBIT crece6,78%, pero no es prudente asumir que nunca volverán: NextGen costó229m en2023 y134m en2024, y Leap ya es un nuevo programa en2026.

El beneficio neto ajustado deQ3 es670m frente a675m,**−0,74%**, aunque el EPS ajustado sube7,2%. En nueve meses el beneficio ajustado crece2,28% frente a8,1% del EPS. La caída de acciones medias de487m a450m explica buena parte de la diferencia. La extraordinaria carga fiscal no monetaria de390m delQ3 anterior distorsiona aún más el crecimiento GAAP. Las recompras benefician a cada acción, pero no prueban aceleración operativa.

## Perspectivas y calidad del crecimiento

La guía2026 es22.050–22.140m deventas, margen ajustado aproximadamente16,1% y EPS ajustado5,72–5,79. No se dispone de guía2027 publicada. Q3 crece4,8% en moneda constante, con unos2,1puntos de adquisiciones; el crecimiento orgánico incluido resale ronda2,7%. Q4 guía3,2–4,7%CC con unos2puntos adquiridos, aproximadamente2%orgánico en su punto medio.

El resale de productos de terceros aporta aproximadamente1,9puntos enQ3. Restarlo también daría0,8%, pero **no es una serie certificada de crecimiento orgánico de servicios**: puede solaparse con negocios adquiridos y ambas contribuciones están redondeadas. No usamos esa resta como un hecho exacto.

Los motores positivos son grandes contratos, cloud/AI y servicios financieros, que crecen12,3%CC. Sin embargo, unos4puntos de este segmento corresponden a resale; HealthSciences y Products&Resources decrecen, y casi9puntos del10,7% de crecimiento en Communications/Media/Technology son adquisiciones. Los bookings TTM suben4%, book-to-bill ronda1,3, pero el valor anualizado de contratos disminuye modestamente por mayor duración. No equivale a ingresos o caja asegurados.

El margen actual también recoge divisas: INR aporta unos90pb favorables en nueve meses frente a una mejora de30pb del margen ajustado. Mantener el nivel de cambio vigente no exige restar automáticamente90pb, pero tampoco permite repetir ese beneficio cada año. Las hipótesis centrales15,6%→16% retienen SBC y un coste recurrente de transformación. No se añaden de nuevo los200m de ahorros deLeap sobre márgenes que ya los incorporan.

## Caja: se necesita mejor conversión, no una liberación gratuita

En nueve meses CFO cae189m y el uso de activos/pasivos operativos aumenta de454m a818m. Influyen incentivos pagados, activos de contratos y otros pasivos. DSO pasa de82 a89días interanuales; activos de contratos466m→690m desde diciembre; los costes capitalizados para cumplir contratos aumentan94m frente a31m, con amortización44m frente a59m. El deterioro es real, aunque no implica que cada año deban empeorar otros siete días.

TTM CFO−capex=2.363m. Después de193m deSBC quedan2.170m; tras ajustar intereses netos e impuestos al26%, un diagnóstico aproximado de caja empresarial es2.143m. No es un FCFF normalizado exacto. Restar las adquisiciones pagadas de1.313m deja1.050m deFCF estricto,857m después deSBC. No se confunde esa inversión con gasto operativo ni se omite su coste.

El modelo central **no libera circulante existente**: financia20% del incremento orgánico de ventas y otros0,2% de ventas para capitalización neta decontratos. No vuelve a financiar los activos circulantes que ya vienen dentro del precio de una compra. Aun así, el FCFF2027 antes de nuevas adquisiciones asciende a**{n(S['additional_checks']['cash_conversion_FCFF_2027_before_new_MA'],0)}m**, aproximadamente27% por encima del diagnóstico TTM. Supone que no se repite todo el deterioro reciente de compensación/cobros, además del crecimiento y margen previstos. No debe describirse simplemente como caja estable.

Como control, otro uso de caja de300m anual durante cinco años y desaparición gradual posterior reduce el valor a**{n(S['additional_checks']['extra_cash_drag_300_per_year_first5_then_fade_value'])}**. Cinco días adicionales deDSO cuestan unos308m en el adverso. La tesis exige comprobar cobros y contratos; si empeoran de forma persistente sin recuperación respaldada, se retira la aprobación fundamental.

### Puente deQ4

La empresa guía conversión deFCF del90–100% del beneficio neto para2026, no una cifra monetaria exacta. Una conciliación desdeEPS, acciones medias y ajustes sugiereFCF deQ4 de730–1.030m;880m es **estimación propia**. Menos50mSBC y más intereses netos después de impuestos da832,22m deFCFF económico. No se descuentan otra vez pagos deLeap ya contenidos en esa proyección.

Se parte del balance de septiembre y se incorpora toda esa caja deQ4 para aproximar su acumulación hasta diciembre. Los57días de descuento desdeNov4 no convierten la proyección en saldo verificado. Se reservan70m de caja por recompras posteriores a septiembre ya potencialmente reflejadas en las acciones de octubre; es una estimación, con sensibilidad0–150m. No se reduce la futura cantidad de acciones sin pagarla. Dividendos futuros son distribución del valor del accionista, no una segunda deducción del puente. Excluir íntegramente el FCFF económico delstub baja el valor a{n(S['additional_checks']['without_economic_Q4_stub'])}, por lo que esta aproximación no explica por sí sola la conclusión.

## Adquisiciones: crecimiento con factura y fechas

3Cloud cerró el1 deenero2026 y Astreya el22 dejunio. Consideración actual total1.398m, incluido un máximo25m contingente, y55m de caja adquirida. A partir del aporte aproximado de2,1puntos enQ3 se obtiene un precio cercano a3x ventas anualizadas. Es una referencia de escenario, no un múltiplo exacto de resultados independientes no divulgados.

El modelo central combina2,5% de crecimiento orgánico,1,5% anual de nuevo run-rate adquirido sobre ventas previas y0,6% de anualización2027 de compras ya pagadas. Los nuevos negocios genéricos cierran a mitad de año: se reconoce media venta el primer año, se arrastra el resto y se paga3x el run-rate completo. En2027 se presupuestan994m deM&A. El coste no desaparece al valorar la acción.

**DyFlex está acordada por aproximadamente210m en efectivo al cierre**, sujeto a ajustes, según el10-Q posterior al anuncio. La previsión de cierre esQ1 2027. El anuncio inicial del21octubre no daba el importe; el10-Q del29octubre sí lo divulga. Los210m están dentro del presupuesto994m, no se suman dos veces. Como no se conocen ventas/EBIT independientes, se usa ventas=210/3 como aproximación y reconocimiento87,5% en2027 por cierre a mitad deQ1. El resto de compras se trata a mitad de año. Los pagos se descuentan en esas fechas; los demás flujos anuales, a cierre.

El contraste de negocio ya poseído solo añade la compra comprometida deDyFlex y elimina adquisiciones hipotéticas posteriores, baja el crecimiento a2,5% y hace disminuir la amortización deintangibles existentes. Arroja**{n(R['owned_business_crosscheck']['per_share'])}**. No es la trayectoria prometida por la dirección ni un motivo para borrar M&A del caso principal conservando su crecimiento.

## FCFF de diez años y capital

SBC permanece como coste del margen. D&A inicial2,6% deventas; inversiónPPE/software1,6%; impuestos26%; capitalización neta decontratos0,2%. Los años2032–2036 son transición agregada, no una predicción literal de cada futura compra: crecimiento converge a2,5%, margen16% y reinversión neta aNOPAT×g/ROIC conROIC12%. D&A/capex se presentan de forma conciliable, sin una perpetuidad de amortización gratis. El terminal consume20,83% deNOPAT para crecer. ElROIC12% es juicio prospectivo, no rendimiento demostrado de los nuevos acuerdos.

{forecast}

En la tabla, el capex agregado de transición incluye reinversión que ya no se asigna a operaciones concretas. Los valores presentes descuentan adquisiciones en su fecha supuesta de cierre, por lo que no equivalen a descontar todo elFCFF de la fila únicamente al final del año.

WACC central**{n(R['capital']['wacc']*100)}%**: Treasury10años4,90% alNov4; ERP implícita4,41% publicadaNov1; beta propia0,8067 sobre58rendimientos mensualesCTSH/SPY, ajustada un tercio hacia1 a0,8711; coste deequity8,74%; deuda5,75% y peso de deuda aproximadamente5%, escudo fiscal26%. El coste de deuda aproxima la referencia de largo plazo más spread decrédito0,875%, no afirma ser el cupón flotante exacto.

La beta tieneSE0,290, R²0,121 e intervalo amplio;8,52% no es una tasa precisa. Se mezclan conscientemente la última tasaTreasury diaria y la últimaERP mensual; la ERP deNov1 se calculó conRf5,29%. Mantener eseRf daWACC8,888%, sensibilidad incluida. Beta1 daWACC9,0575%. No se adopta automáticamente el antiguo10% como barrera, ni se usa la baja beta como garantía de seguridad.

Puente: caja1.515m + inversiones37m − reserva operativa500m =**1.052m excedentarios estimados**. Restamos deuda1.552m, déficit de pensiones/gratuidad260m, earnout25m y estimación de recompras70m: derechos totales1.907m. Déficit de260m es el último importe exacto de diciembre2025; no existe actualización de septiembre certificada y se sensibiliza. No se vuelven a cobrar pagos del mismo déficit enFCFF. La deuda se refinancia en octubre, no se duplica; vence2031 y la amortización trimestral comienza en diciembre2027. Los leases operativos permanecen en gasto, no se suma otra deuda por ellos.

No añadimos el depósito fiscal litigioso de360m como efectivo, ni se resta otra vez el principal ya depositado; intereses/reclamaciones adicionales no cuantificados siguen como riesgo. Tampoco se valora el laudoSyntel de298m bajo apelación. Acciones:447,030425m publicadas alOct23 más1,8m de dilución estimada=448,830425m. No es la media anual de460m ni una promesa de futuras recompras.

## Escenarios, precio implícito y fragilidad

{cases}

Adverso: orgánico1%, margen14,5%, compras3,5xventas, capex1,8%, impuesto27%, otros308m deDSO, WACC+1punto y terminalg2%/ROIC10%. Favorable: orgánico4%, margen16,3%→16,8%, compras2,5x, impuesto25%, WACC−0,5punto yROIC15%. No son probabilidades ni límites garantizados.

A la misma tasa central, combinar orgánico2%, margen50pb menor, compras3,5x, impuesto27% y capex1,8% produce aproximadamente**{n(S['same_wacc_tests']['moderate_combined'])}**. ConWACC9% resulta**{n(S['combined_risk_tests']['moderate_wacc9'])}**; conbeta1 y otros5díasDSO,**{n(S['combined_risk_tests']['moderate_beta1_plus5DSO'])}**. Esta es la razón para aprobar solo como precio razonable condicionado, no como gran descuento ni apuesta de máxima convicción. Un escenario adverso por debajo del precio no veta automáticamente una inversión; sí exige reconocer pérdida posible y no confundir tamaño pequeño con mejor valor.

El precio65,78, con los demás supuestos centrales, equivale aWACC**{n(S['reverse']['wacc_at_price']*100)}%**, o aproximadamente237pb menos de margen operativo en toda la trayectoria, oROIC terminal6,34%. También puede alcanzarse con unos−1% de crecimiento orgánico en los cinco primeros años, **seguido por la transición prevista a crecimiento terminal positivo**: no significa que el mercado descuente contracción perpetua. Son soluciones alternativas del mismo modelo, no evidencias independientes ni una única expectativa observable.

## Contraste y migración desde66,47

Al cierreNov4, elPERGAAP aproximado es12,0x paraCTSH,19,5x paraAccenture y14,7x paraInfosys. Se recalculan con precios regulares65,78/264,27/12,24 yEPS5,48/13,56/0,83. Accenture usa el ejercicio cerrado enagosto; Infosys es IFRS yEPSUSDTTM redondeado deproveedor, no reconstrucción completa de sus cuatro trimestres. El contraste es orientativo: crecimiento, márgenes, impuestos y negocio no son iguales. Accenture guía3–6% en moneda local; Infosys1–2%CC con márgenes20–22%. No se aplica el múltiplo deAccenture aCTSH como objetivo.

Se rechazan ratiosEV/EBIT deproveedor cuyos campos no concilian con EBITGAAP y deuda/leases homogéneos. Por ejemplo, el campooperatingincomeCTSH3,58bn no es el EBITGAAPTTM3,442bn. No se disimula esa discrepancia para fabricar un comparable barato.

Se conservaA120. Su narrativa se reconstruye en66,4849, cercana al66,47 publicado; no se posee el ejecutable original y la diferencia de0,015 puede ser redondeo/convenio. El método sigue siendoFCFF diez años. La conciliación, con la misma información y precio de comparación, es:

{bridge}

El puente separa actualización de tasa, operación/reinversión/timing,stub ycapital. La revisión de coste de capital aumenta el valor; los nuevos supuestos operativos y de reinversión lo reducen respecto a mantener las antiguas hipótesis con la nueva tasa. El modelo nuevo al10% da62,48, de modo que no se escondió el coste deM&A para superar el antiguo techo.

## Técnica y calendario: ficha prospectiva, todavía no ejecutable

Opportunity100 delscannerNov4 habilita investigación; no aprueba compra. Cotización65,78>EMA50**{n(T['ema50'])}**, EMA20**{n(T['ema20'])}**>EMA50 yEMA50>EMA200**{n(T['ema200'])}**; EMA200 crece1,74% en20sesiones. La lectura larga es alcista, con corrección importante: máximo252sesiones87,03 del14enero, retroceso24,42%. Volumen medio6,89m, RSI53,67 yATR2,83. La serie tiene501sesiones y50observaciones recientes contrastadas, sin discrepanciasOHLC materiales. No se inventan nuevas ventanas delscanner.

La caídaOct29 fue5,79%, seguida por rebote4,14%Oct30; la conferencia de resultados deQ3 estaba convocada para las8:30 de la mañanaET delOct29, antes de la apertura. La caída de esa sesión no se clasifica como anterior a los resultados. Elretroceso desdeenero no se atribuye auna única noticia. Riesgos verificados: moderación orgánica, resale/M&A, presión deprecios porIA, contratos y caja. Nov4 subió3,05% en una sesión demercado fuerte; el anuncio propio solo programó una conferencia, no cambióguidance ni demuestra causalidad.

**Ficha propuesta registrada antes de cualquier señal posterior alNov4:**

- Vía A, retroceso y estabilización. Zona prevista 62,50–64,00; esperar esa prueba y la confirmación posterior definida, sin perseguir una ruptura fuera del límite.
- Máximo fundamental66,50; máximo técnico propuesto65,25. No se elevará tras una subida.
- Señal: una **sesión regular futura**, desde Nov5, registra un mínimo entre62,50 y64,00 y cierra por encima de64,75 pero no por encima de65,25, también sobre su apertura yEMA50. El volumen debe superar o igualar el promedio de las20sesiones **anteriores**, excluyendo la sesión de señal. Es una prueba y recuperación de soporte definida de antemano por el analista, no un patrón estadísticamente validado; no se declara señal actual ni ruptura del último máximo.
- Una ruptura genuina sobre66,77, máximo delNov4, no cabe en el máximo fundamental66,50. La víaC queda suspendida; no se sustituye ese máximo por uno antiguo para hacer encajar una compra.
- Mínimo relevanteM=61,55 delOct29; stop protector manual inicial propuestoS=61,20. No comprar siM se pierde durante la campaña pendiente, si hay invalidación fundamental o salida pendiente. No cambiar al cierre de15min después de ver el resultado.
- Tras confirmación, revisar sesión siguiente ysolo límiteDAY de sesión regular, E≤65,25. Cancelar si pierde64,75 antes del fill, se rompeM o supera el máximo permitido. Si no se ejecuta, no perseguir conmercado ni asumir unfill.
- Vigencia: la última sesión admisible de señal es el9noviembre2026, para posible ordenDAY el10noviembre. Todas las órdenes y esta ficha caducan al cierre del10noviembre; después requiere revisión. ConferenciaBMO12noviembre10:45ET confirmada. No existe fecha futura de resultados confirmada enlasfuentes revisadas; no autorizar atravesar resultados sin actualizarcalendario.
- P, efectivo, exposición, riesgo agregado, órdenes pendientes yplazas **no verificados**. No se asigna cantidad real ni se afirma disponibilidad.

Solo como fórmula pendiente: C=10%P habitual yB=1%P fijados para la campaña, Primer tramo de la víaA Ctramo≤2%P, sujeto a C. Se propone además Btramo≤25%B para esta candidatura, no como nueva regla universal. ConE=65,25 yS=61,20, acciones enteras=floor delmínimo de Ctramo/65,25, capital restante/65,25 y riesgo disponible limitado porBtramo dividido entre4,05. La reserva de costes/deslizamiento debe fijarse conla cuenta real. Los stops manuales pueden demorarse ylos huecos superarB. **No hay Stage3.5 aprobado, señal ejecutada ni posición nueva.**

## Seguimiento y condiciones que cambian la tesis

1. Q4: demostrarFCF compatible con elrango inferido730–1.030m, sin confundir ventas deactivos o menor impuesto extraordinario con recurrencia.
2. DSO/contratos: estabilización, no nuevas acumulaciones persistentes. Debe revisarse el salto de caja operativo previsto.
3. Crecimiento2027: separar orgánico, resale, anualización y nuevas compras; margen15,5–16% conSBC ysin repetirFX extraordinario.
4. M&A: DyFlex dentrodel presupuesto; validar ventas, sinergias, coste real y retorno incremental. No financiar crecimiento perpetuo a precios que destruyan valor.
5. Cotización/técnica: si supera66,50, se cancela esta propuesta; si pierde estructura o tesis, se reevalúa. El modelo no sustituye gestiónStage4 de posiciones existentes.

## Fuentes y trazabilidad

Primarias: [10-K2025](https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm), [10-Qseptiembre2026](https://www.sec.gov/Archives/edgar/data/1058290/000105829026000041/ctsh-20260930.htm), [resultadosQ3](https://investors.cognizant.com/news-and-events/news/news-details/2026/Cognizant-Reports-Third-Quarter-2026-Results/default.aspx), [transcripción alojada porlaempresa](https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q3/transcript/Transcript_CTSHQ3-2026-Earnings-Call.pdf), [conferenciaBMO](https://investors.cognizant.com/news-and-events/news/news-details/2026/Cognizant-to-Present-at-the-BMO-Technology-and-Innovation-Leaders-Conference/default.aspx). Los cierres/series se contrastan conStockAnalysis/Yahoo; Treasury yDamodaran sustentan tasas yprima. Sources/source_review distinguen datos publicados, guía, derivaciones ehipótesis. Los datos demercado son un corte, no cotizaciones en tiempo real.

Soporte reproducible: históricosCSV, modeloPython determinista, escenarios,reverseDCF,sensibilidades,serieOHLCV,comprobaciones yacta independiente. **No es un libroExcel de fórmulas ni se afirma validación enExcel nativo.** Los originales y el expediente anterior se conservan; la versión depublicación incluye datos seleccionados yenlaces, no copias completas de informes ajenos.
'''
import re
# Editorial spacing without altering verified links or machine identifiers.
parts=re.split(r'(https?://[^\s)]+)',text)
for k in range(0,len(parts),2):
 x=parts[k]
 x=re.sub(r'([a-záéíóúñ])([A-ZÁÉÍÓÚ])',r'\1 \2',x)
 x=re.sub(r'([A-Za-zÁÉÍÓÚáéíóúñ]+)(\d+)',lambda m:m[0] if m[1] in ['Q','FY','TTM','EMA','ATR','RSI'] else m[1]+' '+m[2],x)
 x=re.sub(r'(\d)([A-Za-zÁÉÍÓÚáéíóúñ]+)',lambda m:m[0] if m[2] in ['x','m','bn'] else m[1]+' '+m[2],x)
 for a,b in {'deella':'de ella','porsísolo':'por sí solo','sísolo':'sí solo','lasfuentes':'las fuentes','elcierre':'el cierre','delcierre':'del cierre','elprecio':'el precio','demercado':'de mercado','deventas':'de ventas','deuda5':'deuda 5','decontratos':'de contratos','laempresa':'la empresa','porlaempresa':'por la empresa','deguía':'de guía','depagos':'de pagos','debeneficio':'de beneficio','deenero':'de enero','dejunio':'de junio','delretroceso':'del retroceso','Elretroceso':'El retroceso','elde':'el de','todal':'toda l','dela':'de la','definidas':'definidas','delmínimo':'del mínimo','derecho':'derecho','lasacciones':'las acciones','poracción':'por acción','enlasfuentes':'en las fuentes','deesa':'de esa','las20':'las 20','detoda':'de toda','decoste':'de coste','deequity':'de equity','decrédito':'de crédito','deproveedor':'de proveedor','deprecios':'de precios','deagosto':'de agosto','enagosto':'en agosto','defuturos':'de futuros','delos':'de los','deltiming':'del timing','delespacio':'del espacio','delmodelo':'del modelo','delespejo':'del espejo','efectivoal':'efectivo al','noconfirmada':'no confirmada','antel':'ante l','dentrodel':'dentro del','diluidopor':'diluido por','datospublicados':'datos publicados','enel':'en el','noticiasverificadas':'noticias verificadas','ypresupuestos':'y presupuestos','yenlaces':'y enlaces','ehipótesis':'e hipótesis','yacta':'y acta','sinuna':'sin una','porun':'por un','conla':'con la','sinconfundir':'sin confundir','enun':'en un','señalde':'señal de','confuentes':'con fuentes','hastala':'hasta la','delscanner':'del scanner','noviembre2026':'noviembre 2026','elsector':'el sector','delflujo':'del flujo','losdemás':'los demás','Noes':'No es','elimporte':'el importe','deposiciones':'de posiciones'}.items():x=x.replace(a,b)
 parts[k]=x
text=''.join(parts)
for a,b in {'Dy Flex':'DyFlex','Stock Analysis':'StockAnalysis','3 Cloud':'3Cloud','ypresión':'y presión','ycapital':'y capital','ysolo':'y solo','ysupuestos':'y supuestos','yplazas':'y plazas','ylos':'y los','ysin':'y sin','yprima':'y prima','auna':'a una','elrango':'el rango','unfill':'un fill','conmercado':'con mercado','deactivos':'de activos','enlas fuentes':'en las fuentes','actualizarcalendario':'actualizar calendario','cambióguidance':'cambió guidance','porla empresa':'por la empresa','depublicación':'de publicación','10-Qseptiembre':'10-Q septiembre','valoractual':'valor actual','Series/source_review':'Datos de fuentes','Sources/source_review':'Los archivos de fuentes','/timing,stub':'/timing, stub',',stub':', stub',',reverse':', reverse',',sensibilidades':', sensibilidades',',serie':', serie',',comprobaciones':', comprobaciones', 'habitual y B=1%P fijados para la campaña, Primer':'habitual y B=1%P fijados para la campaña. Primer', 'PERGAAP':'PER GAAP','EPSUSDTTM':'EPS USD TTM','deltotal':'del total','elFCF':'el FCF','comoFCF':'como FCF','vs.':'frente a'}.items():text=text.replace(a,b)
text=re.sub(r'(%)(?=[A-Za-zÁÉÍÓÚáéíóúñ])',r'\1 ',text)
text=re.sub(r'(?<=[\w])(?=\*\*)',' ',text)
text=re.sub(r'(?<=\*\*)(?=[\w])',' ',text)
text=text.replace('RSI53','RSI 53').replace('ATR2','ATR 2')

text=re.sub(r'\*\*\s*(.*?)\s*\*\*',lambda m:'**'+m[1].strip()+'**',text)
text=text.replace('Precio:65','Precio: 65').replace('delstub','del stub').replace('deintangibles','de intangibles').replace('A 120','A120').replace(';880','; 880').replace('orgánico,1','orgánico, 1')
(P/'report.md').write_text(text)
print('Words',len(text.split()))
