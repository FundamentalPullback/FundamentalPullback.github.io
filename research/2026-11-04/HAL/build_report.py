from pathlib import Path
import json
P=Path(__file__).parent;H=json.loads((P/'history/history.json').read_text());M=json.loads((P/'model_results.json').read_text());C=json.loads((P/'comps.json').read_text())
def f(x,n=0):return f'{x:,.{n}f}'.translate(str.maketrans(',.','.,'))
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(x) for x in r)+' |' for r in rows)+'\n'
periods=['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM_2025_09','TTM_2026_09'];names=['2023','2024','2025','Q4 2025','Q1 2026','Q2 2026','Q3 2026','TTM sep-2025','TTM sep-2026']
t1=table(['Periodo','Ventas','EBIT GAAP','Beneficio común','EPS GAAP','EBIT ajustado¹','EBIT normalizado²'],[[n,f(H[p]['revenue']),f(H[p]['ebit']),f(H[p]['net_income_common']),f(H[p]['eps_gaap_reported'],2) if H[p]['eps_gaap_reported'] is not None else 'No sumado',f(H[p]['adjusted_ebit_ex_charges']),f(H[p]['normalized_ebit_pre_sap_after_0_5pct_recurring_reserve'],1)]for p,n in zip(periods,names)])
t2=table(['Periodo','CFO','Capex bruto','Ventas PP&E','D&A','Caja circulante comercial³','FCF sin desinversiones','Caja propietario⁴','Caja propietario neutral WC⁴'],[[n]+[f(H[p][k],1) for k in ['cfo','capex','ppe_sales','da','trade_wc_cash','fcf_ex_asset_sales','owner_cash_after_sbc_and_finance_lease_mid','owner_cash_wc_neutral_after_finance_lease_mid']]for p,n in zip(periods,names)])
t3=table(['Escenario','Valor/acción','Vs.34,07','EV','FCFF año1','FCFF año10','Peso terminal','Retorno negocio⁵','Proxy retorno equity⁵'],[[name,f(v['value'],2),f(v['upside']*100,1)+'%',f(v['ev']),f(v['rows'][0]['fcff']),f(v['rows'][-1]['fcff']),f(v['pv_terminal_share']*100,1)+'%',f(v['implied_business_annual_return']*100,1)+'%',f(v['implied_equity_annual_return_proxy']*100,1)+'%']for key,name in [('adverse','Adverso'),('central','Central'),('favorable','Favorable')]for v in [M['results'][key]]])
t4=table(['Año','Ventas','Crecimiento','Margen EBIT','NOPAT neto⁶','D&A','Capex bruto⁷','ΔWC','FCFF','PV FCFF'],[[r['year'],f(r['revenue']),f(r['growth']*100,1)+'%',f(r['ebit_margin']*100,1)+'%',f(r['nopat']),f(r['da']),f(r['capex_including_finance_asset_replacement']),f(r['delta_wc']),f(r['fcff']),f(r['pv_fcff'])] for r in M['results']['central']['rows']])
t5=table(['Compañía','Precio 3nov','Ventas TTM','EBIT+D&A después SBC','EV comparable','EV/EBITDA GAAP','FCF sin ventas activos','FCF/capitalización'],[[k,f(d['price'],2),f(d['revenue']),f(d['gaap_ebitda_after_sbc']),f(d['ev']),f(d['ev_ebitda_gaap'],2)+'x',f(d['fcf_ex_sales']),f(d['fcf_yield_equity']*100,1)+'%'] for k,d in C['data'].items()])
t6=table(['WACC / g terminal','1,5%','2,0%','2,5%','3,0%'],[[f(w*100,2)+'%']+[f(M['wacc_g_sensitivity'][f'{w:.4f}/{g:.4f}'],2)for g in [.015,.02,.025,.03]]for w in [.0925,.10,.105,.11,.1175]])
t7=table(['Margen EBIT sostenible','Crecimiento ventas años1–5 que iguala34,07'],[[f(x['sustainable_ebit_margin_after_sbc_and_routine_cost']*100,1)+'%',f(x['growth_years1_5_required']*100,2)+'%']for x in M['reverse_margin_growth']])
text=f'''# HAL · Halliburton · Stage 3 completo y reproducible

**Corte de investigación: 4 de noviembre de 2026, 16:26 UTC.** Estados financieros hasta el 30 de septiembre de 2026; resultados publicados el 20 de octubre y 10-Q presentado el 23 de octubre. Cotización utilizada: **34,07 USD, cierre regular del 3 de noviembre**, no precio intradía del día 4. La última fila HAL localizada en el registro propio es del 2 de noviembre, **34,70 USD**; se conserva como observación histórica y no se sustituye silenciosamente por el cierre de mercado. Esta revisión completa la investigación acotada A137; no modifica su archivo histórico. [10-Q Q3](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm), [resultados oficiales](https://ir.halliburton.com/news-releases/news-release-details/halliburton-announces-third-quarter-2026-results), [histórico de precios](https://stockanalysis.com/stocks/hal/history/).

## Resultado de la investigación

**Candidato condicional a la recuperación, con precio razonable en un escenario constructivo, pero sin descuento claro frente al caso central.** DCF central **27,32 USD**, adverso **11,14**, favorable **49,08**. Un caso conjunto menos exigente que el favorable, crecimiento inicial del 4%, margen sostenible del 16%, WACC10%, impuesto22% y mejor eficiencia de reinversión, produce **33,59 USD**. Por tanto, 34,07 no exige una fantasía tecnológica ni permite rechazar HAL simplemente por carecer de un descuento fijo del15%. Sí requiere que la recuperación de márgenes y caja dure más que un trimestre.

El avance del beneficio GAAP oculta una comparación fácil por deterioros de2025: ventas TTM +1,5%, EBIT GAAP +15,6%, pero EBIT ajustado −8,5% y EBIT normalizado −7,6%. La caja es más matizada: parte de la caída del CFO proviene de un giro adverso de641 millones en circulante comercial. La tesis positiva necesita cobrar ese circulante sin sacrificar la renovación de equipos. El balance no presenta una refinanciación inmediata dominante, aunque hay pensiones, impuestos y adquisiciones posteriores al cierre que no deben desaparecer de la valoración.

**Stage3 fundamental: investigación completa; revisión independiente cerrada sin error material y ajustes menores incorporados. Stage3.5: sin entrada aprobada.** No se han verificado a fecha de hoy las EMA, ATR, vela de confirmación, stop, tamaño de posición ni límites de cartera. Su ausencia no convierte la investigación fundamental en incompleta ni demuestra que la señal técnica sea negativa. Una entrada parcial a valor razonable puede ser compatible con el plan si posteriormente se valida la señal y el riesgo; aquí no se ordena ninguna operación.

## 1. Negocio, calidad del crecimiento y resultados disponibles

Halliburton presta servicios y suministra tecnología de perforación, evaluación, completación y producción. La escala, la ejecución en campo, la base instalada, los equipos y los flujos digitales integrados ayudan a competir, pero no eliminan la exposición al presupuesto de sus clientes y al ciclo petrolero. Completion & Production aporta el54% de las ventas Q3; Drilling & Evaluation el46%. El componente internacional ya es62% de las ventas del trimestre. No se le asigna un múltiplo de software a todo el negocio.

Q3: ventas **5.703**, EBIT GAAP **624**, beneficio común **417**, EPS **0,50**; ajustados, EBIT **731** y beneficio **501**, EPS **0,60**. C&P registra ventas3.089 y EBIT457, −4% y −11% interanual; D&E2.614 y391, +10% y +12%. Norteamérica cae9% a2.160. Latinoamérica crece13%, Europa/África/CIS23%, mientras Oriente Medio/Asia está prácticamente plano; este último todavía cae8% en nueve meses. Son geografías y servicios distintos, no una recuperación uniforme. [Resultados Q3](https://ir.halliburton.com/news-releases/news-release-details/halliburton-announces-third-quarter-2026-results), [10-Q, segmentos y MD&A](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm).

**Guía oficial, no supuesto nuestro:** la perspectiva preliminar2027 publicada el20oct contempla crecimiento de ventas de un dígito medio y margen operativo alrededor del15%, unos200pb de mejora, con Norteamérica plana y sin exigir recuperación de fracturación norteamericana. El10-Q contempla capex2026 de aproximadamente1.100 y34 de gasto SAP enQ4, con finalización de la implantación en ese trimestre. No se añade de nuevo el ahorro SAP sobre un margen que ya lo incorpora. [Comunicado](https://ir.halliburton.com/news-releases/news-release-details/halliburton-announces-third-quarter-2026-results), [10-Q](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm).

Como contexto secundario, la transcripción publicada por StockAnalysis/Quartr atribuye a la dirección FCF2026 cercano a1.600, recuperación de cobros enQ4 y ahorro2027 combinado de250–300 por estructura/SAP. También indica que parte del coste vuelve con la actividad y que el soporte SAP continúa. No he verificado el audio: estos detalles complementan, no sustituyen, la guía primaria. Son expectativas, no caja ya ingresada. [Transcripción del20oct](https://stockanalysis.com/stocks/hal/transcripts/711265-q3-2026/).

**Consenso externo alojado en IR**, consultado4nov, sin sello temporal subyacente visible: ventas2026/27/28 de22.545/23.696/24.948 y EPS ajustado2,33/2,92/3,44; Q4 ventas5.724 y EPS0,63. La suma9M16.819+Q4consenso5.724≈22.543 reconcilia con el año. No se mezclan esos EPS ajustados con el GAAP1,50 de2025. El caso central utiliza un primer año móvil23.600, parecido al consenso2027 en magnitud, pero **no idéntico en fechas**. [Estimaciones LSEG en IR](https://ir.halliburton.com/stock-information/earnings-estimates).

**Perímetro:** se vendió parte de la cartera de químicos enQ2, con pérdida17; no existe en las fuentes examinadas un desglose retrospectivo suficiente de ventas, EBIT y CFO de esa parte para fabricar una serie orgánica constante. Las compras netas de negocios suman107 en9M2026. El2nov HAL anunció la adquisición de Keystone AS, software de planificación/ejecución que se incorpora a Landmark; el anuncio no publica precio, financiación ni EBITDA. La valoración parte del balanceSep30 y asume **NPV incremental neto cero** para Keystone hasta conocer términos, no precio de compra cero ni balance proforma exacto. Cada100 de creación/destrucción neta de valor mueve aproximadamente0,12USD/acción; la falta de términos no establece un límite real de100. [10-Q](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm), [Keystone,2nov](https://www.halliburton.com/en/about-us/press-release/halliburton-acquires-keystone-strengthen-digital-well-construction-capabilities).

## 2. Tres ejercicios, cuatro trimestres y comparación TTM

Millones de USD, excepto EPS. Años fiscales coinciden con calendario. Q4 se deriva de año menos9M; CFO/capex Q2 yQ3 son diferencias acumuladas, no resultados de nueve meses presentados como trimestrales. TTM actual=FY2025+9M2026−9M2025; anterior=FY2024+9M2025−9M2024. No se suman acciones medias ni se presenta una suma de EPS trimestrales como un EPS TTM GAAP publicado.

{t1}
¹ Ajustado=EBIT GAAP+«impairments and other charges», respetando el signo: el crédito netoQ2−95 se resta, no se añade. ² Normalizado analítico=EBIT ajustado+SAP−0,5%ventas de coste recurrente de reorganización. Es una medida de capacidad operativa comparable, no otra cifra GAAP ni caja cobrada.

{t2}
³ Cambio de caja por cuentas a cobrar+inventario+proveedores del estado de flujos; positivo libera caja. ⁴ Caja propietario=CFO−capex−SBC económico−principal de leasing financiero. La última columna elimina exclusivamente el cambio de circulante comercial. **No elimina automáticamente otros movimientos, impuestos o indemnizaciones. Tampoco deduce inversiones en adquisiciones. No es FCF plenamente normalizado.**

SBC anual real2023/24/25:219/223/213. El emisor no aísla el gasto SBC trimestral en estos10-Q; la línea de patrimonio «Stock plans» no equivale a gasto. Para cuatro trimestres y ambosTTM se usa1%ventas, con sensibilidad0,9–1,1%. Principal de leasing financiero anual real37/33/48; no aislado trimestralmente, por lo que se estima12por trimestre/48TTM, no se inventa una observación. La sensibilidad anual de principal 0/48/80/100/103 produce caja diagnóstica neutral al circulante actual de 1.585/1.537/1.505/1.485/1.482. El 10-K programa pagos financieros para 2026 de 103, incluidos intereses: 80 no es una cota superior y 103 no se presenta como principal observado. Aplicar 103 íntegro como principal es un estrés conservador que puede duplicar su parte de intereses, ya incluida en CFO. El proxy histórico de 48 no es una previsión del calendario vigente. Esta sensibilidad no cambia automáticamente el DCF, que modela los arrendamientos y la reposición de otra forma. Los archivos conservan los datos publicados separados de las estimaciones.

Fuentes: [10-K2025, tres ejercicios, notas2/7/14](https://www.sec.gov/Archives/edgar/data/45012/000004501226000015/hal-20251231.htm), [Q1](https://www.sec.gov/Archives/edgar/data/45012/000004501226000039/hal-20260331.htm), [Q2](https://www.sec.gov/Archives/edgar/data/45012/000004501226000061/hal-20260630.htm), [Q3](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm), [Q3previo, comparación2024](https://www.sec.gov/Archives/edgar/data/45012/000004501225000069/hal-20250930.htm), [Q4 oficial,EPS0,70](https://ir.halliburton.com/news-releases/news-release-details/halliburton-announces-fourth-quarter-2025-results).

## 3. Qué normalizamos y qué no

- **Deterioros y créditos:** FY2025 incluye831 de cargos netos, entre ellos299 de indemnizaciones,224 de deterioro de químicos destinados a venta,115 de activos fijos y53 de inmuebles. FY2024 incluye116netos. En9M2026 los cargos netos son12: coexisten costes de plantilla/inventario/activos y ganancias de inversiones/reembolsos. Retirar solo los costes e ignorar los créditos inflaría el beneficio. Se elimina el neto completo y se repone0,5%ventas de coste recurrente, unos112TTM, coherente en orden de magnitud con indemnizaciones medias anuales121. No es un coste cero perpetuo.
- **SAP:** se retira para comparar capacidad madura; los márgenes futuros ya incorporan costes recurrentes de soporte y un ahorro gradual. No se añade172TTM otra vez alDCF. El margen normalizado pasa de17,46%/17,20% en2023/24 a14,13% en2025 y13,27%TTM actual. Volver a15–16% es una recuperación posible, no un punto de partida ya logrado.
- **Caja y cobros:** CFO TTM cae3.217→2.630. El circulante pasa de liberación431 a consumo210; ese giro−641 es mayor que la caídaCFO−587. El resto del puente agrega+54. Esto demuestra que no debe extrapolarse el malQ3, pero no prueba que todo el consumo sea recuperable. La caja propietario neutral al circulante mejora1.174→1.537, todavía por debajo de2.270–2.334 en2023/24.
- **Venta de activos:** el FCF definido por HAL incluye ventas de PP&E. EnQ3,368−266+54=156; sin esas ventas es102. TTM,1.822frente a1.600. ElDCF no convierte los222 de ventasTTM en ingreso perpetuo. CapexTTM1.030 está por debajo deD&A1.177; un negocio de equipos no puede sostener indefinidamente esa diferencia y seguir creciendo sin coste.
- **Impuestos y otros:** la tasa9M18,6% incluye una liberación de valoración fiscal32, no caja nueva. Se usa23%central,21–25%escenarios. No se suma el activo fiscal diferido como efectivo libre. El gasto «Other,net» histórico existe fuera del EBIT: se conserva una fuga económica futura0,25%ventas antes de impuestos central,0,15–0,35%escenarios, en vez de suponer que todo desaparece. No se duplica dentro de cargos operativos.
- **Límite de la caja ajustada:** el emisor no separa el calendario de pago de cada indemnización/reembolso. No se añaden107 de cargosQ3 al CFO como si todos fueran caja ni se resta un reembolso contable como si ya se hubiera cobrado. Un FCFF sintético sin crecimiento deWC, NOPAT normalizado+D&A−capex actual−principal leasing, sería2.216previo/2.395actual; es una referencia diagnóstica condicionada a capex y circulante, no el flujo que se capitaliza. El primer FCFF central2.040 financia expansión y un colchón de cobros.

Las fórmulas y358celdas de origen constan en `history/source_rows.json`;41identidades de resultados y caja y suma de cuatro trimestres pasan. [10-K2025](https://www.sec.gov/Archives/edgar/data/45012/000004501226000015/hal-20251231.htm), [10-Q2026](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm).

## 4. Del valor del negocio a la acción

| Reclamación / activo | MillonesUSD | Tratamiento |
| --- | --- | --- |
| Deuda financiera, principal aproximado | 7.222 | BalanceSep30 contable7.162; principal aproximado desde vencimientos anuales sin amortización9M. No usar valor razonable6.598 como coste de cancelación. |
| Leasing financiero | 183 | Última separación anual31dic2025; está fuera de la deuda anterior. Sensibilidad explícita. |
| Efectivo | −1.843 | BalanceSep30; no constituye caja libre íntegra. |
| Reserva operativa de efectivo | +750 | Hipótesis, no restricción legal. Solo1.093 de exceso se descuenta. |
| Déficit pensiones internacionales | +200 | Último dato anual; obligación783 menos activos583. |
| Minoritarios | +120 | Valor económico analítico, frente a libro43; no restar además beneficio minoritario anual del FCFF. |
| Impuesto histórico susceptible de pago | +155 | Estimación publicada31dic2025, no impuesto ordinario del NOPAT. |
| NPV incremental Keystone no cuantificado | 0 | Supuesto neutral, no coste de compra cero. |
| **Reclamaciones netas DCF** | **6.787** | Distintas del EV convencional de comparables. |

Acciones reales827,126342millones a16oct, más1millón de dilución aproximada según diferencia de mediasQ3: **828,126342millones**. La aproximación no es el inventario exacto de todos los premios. No se cuentan recompras futuras gratis: se conserva SBC en márgenes. Q3 excluye unas5millones de opciones antidilutivas; a precios superiores podrían diluir. Añadir5millones más baja el valor central a27,15 y el favorable aproximadamente0,29. No se duplica anualmente SBC como gasto y expansión perpetua de acciones.

Los arrendamientos operativos siguen en costes: no se suma su pasivo1.036 para restarlo otra vez del EV. Los183 financieros sí se restan, y elDCF financia futura reposición de equipos arrendados dentro del capex, sin restar otra vez principal histórico. El déficit de pensiones no vuelve a cargarse íntegro como pago anual. La provisión fiscal155 podría solaparse parcialmente con contingencias específicas: no sumamos automáticamente todos los riesgos.

La propuesta fiscal por la cancelación Baker Hughes podría generar unos640más intereses si la empresa pierde; no es pago exigible hoy. Se ofrece estrés adicional740, con100de interés **supuesto**, que reduce central a26,42. No se presenta como estimación de la resolución ni probabilidad ponderada. La provisión reservada155 y ese estrés podrían solaparse: es una cota adversa conservadora. [10-K, impuestos/deuda/pensiones/acciones](https://www.sec.gov/Archives/edgar/data/45012/000004501226000015/hal-20251231.htm), [10-Q, balance/contingencias](https://www.sec.gov/Archives/edgar/data/45012/000004501226000074/hal-20260930.htm).

Liquidez: línea3.500 hastaagosto2030, vencimiento de deuda90enfebrero2027; la empresa indica ratingsBBB+/A3estables. Financiación de proveedores294 está enproveedores, no se duplica como deuda y circulante. LosCDS vinculados aMéxico vencieron enQ3 y su saldo es cero aSep30: no se resta el antiguo592. Un cliente mexicano representa aproximadamente8%decuentas a cobrar; la dirección espera cobrar, pero las demoras son un riesgo real. La reclamación fiscal, los cobros y el precio deKeystone hacen que este sea un puente de balance fechado, no una certificación de caja disponible al4nov.

## 5. Valoración directa: diez años deFCFF

Moneda nominalUSD. Diez periodos anuales prospectivos desde la valoración, calibrados al TTM de septiembre: cinco años explícitos y cinco de transición. No se atribuyen al año fiscal exacto. FCFF = (EBIT − fuga económica) * (1 − impuesto) + D&A − capex − ΔWC. SBC permanece como coste. Se financia crecimiento: años1–5, inversión incremental total=Δventas/ventas-capital; se divide entre circulante y equipo, no se cobra dos veces. Capex de mantenimiento≥D&Acentral, más expansión. En contracción solo se liberaWC, no se venden automáticamente activos al valor libro.

Años6–10 hacen transición gradual hacia reinversión=NOPAT*crecimiento/ROIC. Año11 FCFF=NOPAT11*(1−g/ROIC); terminal=FCFF11/(WACC−g). Crecer requiere capital incluso en perpetuidad. ElROIC terminal14%central es una hipótesis de retorno marginal, no una medición delROIC GAAP actual. D&A5,25%ventas aproxima elTTM5,24%; margen yROIC se someten a escenarios, no se extrapola el último trimestre.

| Supuesto | Adverso | Central | Favorable |
| --- | --- | --- | --- |
| Crecimiento años1–5 | −5/−4/+2/+3/+2,5% | 5/4,5/3,5/3/3% | 6,5/7/6/5/4,5% |
| Margen EBIT año1 / máximo / año10 | 11,5/13/13% | 14,5/15,5/15% | 15/17,5/17% |
| Impuesto |25%|23%|21%|
| WACC |11,75%|10,5%|9,25%|
| Crecimiento terminal / ROIC |2% /10%|2,5% /14%|3% /18%|
| Ventas/capital incremental años1–5 |1,75x|2,5x|3x|
| ΔWC porΔventas |22%|20%|18%|
| Reserva extra deWC |250+100|100 año1|0|
| Mantenimiento/D&A |105%|100%|100%|
| Fuga económica antes impuestos/ventas |0,35%|0,25%|0,15%|

El5%central sigue la perspectiva inicial2027, no un crecimiento mínimo obligatorio. Margen inicial14,5% reconoce la transición desde13,27%normalizado y alcanza15,5%si la ejecución acompaña. El favorable combina internacional fuerte, recuperación y eficiencia; no basta subir una única variable. El adverso permite caída de ventas, deterioro de margen y cobros, sin asumir quiebra.

WACC: Treasury10años **4,95% al3nov**; prima de mercado5% ybeta1,4 **supuestos**, coste equity11,95%; coste de deuda 6,45% **supuesto**, peso20%, escudo23%: WACC10,5533%, redondeado10,5%. No se atribuye a una base de datos una beta no estimada. La incertidumbre de ciclo ya se representa mediante flujos alternativos y un rango de descuento, no mediante un descuento fijo adicional al valor. [Treasury oficial](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve).

{t3}
⁵ Rentabilidades internas condicionadas al itinerario de caja y terminal del escenario desde el precio34,07. La del negocio usaEV con todas las reclamaciones. La de equity es un **proxy idealizado**, mantiene reclamaciones netas y financiación bruta, descuenta intereses al 5,8% como hipótesis de coste medio de financiación, distinta del coste marginal supuesto del 6,45% usado en WACC, tras impuestos y12anuales de minorías, refinancia sin fricción y resta reclamaciones al terminal. No esCAGR de cotización, consenso de rentabilidad ni retorno garantizado; la real depende de reinversión, distribución y cambios de balance. No se usa8,6%central como veto por un umbral ajeno alplan.

### Itinerario central anual

{t4}
⁶ NOPAT después de la fuga económica antes de impuestos. ⁷ Incluye renovación futura de activos financiados; no añade principal de deuda corriente al capex. CSV de los tres escenarios preservan decimales y todos los años. EVcentral29.410menos6.787 produceequity22.623. El46%del EVproviene del terminal descontado, frente a56%favorable. No se ha reducido la valoración a un múltiplo del último FCF.

## 6. ReverseDCF y sensibilidad conjunta

ConWACC10,5%,impuesto23%,ventas/capital2,5x,ROIC14%,g2,5% y margen inicial14,5% que converge en cuatro años, estas parejas igualan34,07; el crecimiento inicial se mantiene cinco años y luego converge a2,5%:

{t7}

**No son una expectativa de mercado única.** Otro conjunto razonable, crecimiento4%, margen16%,WACC10%,impuesto22%,ventas/capital2,75x yROIC16%, vale33,59. Por eso sería incorrecto afirmar que el precio exige necesariamente8,5%de crecimiento. Lo que exige es alguna combinación suficientemente buena de margen, coste de capital, fiscalidad y reinversión. Esa combinación tiene apoyo parcial en la guía y enmárgenes históricos, pero no está demostrada en cajaTTM.

{t6}

Otros controles reproducidos:
- Una recesión intermedia (ventas−8% en año3, margen11,5%, recuperación posterior) reducecentral a24,41.
- Capex explícito4,9%ventas, aproximadamente ritmo2026, da28,85;5,5%da27,96;6,5%da26,48. La restricción de capex por sí sola no lleva al precio observado, y los tres convergen a inversiónterminal consistente.
- Reserva recurrente de reorganización0,25/0,50/1,00%ventas:27,95/27,32/26,05. No se exige permanentemente el pico de cargos2025 ni se los elimina sin sustituto.
- Eficiencia ventas/capital1,75/2/2,5/3x:26,45/26,81/27,32/27,66;100/250/500adicionales deWCenprimer año:27,21/27,04/26,77.
- Reservar0/750/1.250de caja operativa:28,22/27,32/26,71. Sensibilidadleasing0/183/250:27,54/27,32/27,24.
- El escenario favorable49,08 representa+44%; el adverso11,14 representa−67%. No se asignan probabilidades arbitrarias para fabricar un precio esperado.

## 7. Comparables actuales: contraste, no sustitución del DCF

Cierres regulares3nov y estados aSep30. EV=capitalización + deuda + leasing financiero separado + minoritarios a valor libro − caja/inversiones líquidas. No se ajusta por las reservas adicionales propias del DCFHAL, por lo que ambosEV no son idénticos. EBITDA diagnóstico=EBITGAAP+D&A **despuésdeSBC**; no se mezcla el EBITDA corporativo de Weatherford que añade SBC con el de HAL que lo mantiene. FCF=CFO−capex y demás inversión recurrente; no incluye ventasde activos niM&A. Es una comparaciónGAAP fechada, no una afirmación de flujos igualmente normalizados.

{t5}

HAL cotiza8,42x sobreGAAP y8,11x sobre nuestro EBITDA operativo normalizado4.159. Un rango analítico7,5–9,5x ese EBITDA produce30,97–41,01USD con puente comparable, **no una media de precios objetivo**. El extremo alto capitaliza recuperación y puede ocultar capex/circulante. La diferencia frente a DCF central27,32 procede de reclamaciones económicas adicionales, coste del capital y reinversión explícita, no de que una aritmética sustituya a otra.

- **SLB:** mayor presencia internacional y digital, con exposición a producción. ChampionX se consolida desde agosto de 2025; el TTM cubre cuatro trimestres mayoritariamente bajo el nuevo perímetro, pero el crecimiento interanual contiene compras. Kelvion seguía pendiente, no se presume cerrado. La medida reconstruida de EBIT excluye interest & other income. Se incluyen inversiones APS/datos además de capex. No se justifica trasladar automáticamente su 12,47x a HAL. [10-Q](https://www.sec.gov/Archives/edgar/data/87347/000119312526435577/slb-20260930.htm), [10-K](https://www.sec.gov/Archives/edgar/data/87347/000119312526021017/slb-20251231.htm).
- **WFRD:** el 7,74x muestra que HAL no está aisladamente barata. NCS se compró en septiembre y solo aporta un mes al Q3; el TTM no es proforma. El traslado de sede previsto para el 13 de noviembre no está completado. La amortización de 236 de deuda el 30 de octubre usa caja: no produce 236 de valor gratis. [Anuncio del reembolso](https://www.globenewswire.com/news-release/2026/10/30/3392208/0/en/weatherford-announces-redemption-of-8-625-senior-notes-due-2030.html), [redomiciliación pendiente](https://www.sec.gov/Archives/edgar/data/1603923/000160392326000126/pressrelease_wfrdredomicil.htm). Se conserva el balance de septiembre en ambos lados. La ganancia de venta de 70 de 2025 cancela al reconstruir TTM, no se retira dos veces. [10-Q](https://www.sec.gov/Archives/edgar/data/1603923/000160392326000122/wfrd-20260930.htm), [10-K](https://www.sec.gov/Archives/edgar/data/1603923/000160392326000014/wfrd-20251231.htm).
- **NOV:** fabricante de equipos, cartera de pedidos y circulante distintos; CFO de nueve meses de 32 no es caja normalizada. Leasing financiero de 262 corresponde al último dato anual, no observación de septiembre. El litigio de royalties con HAL sigue en apelación; el crédito de NOV de 144 abarca varios licenciatarios y no se atribuye íntegro a HAL. [10-Q](https://www.sec.gov/Archives/edgar/data/1021860/000119312526435747/nov-20260930.htm), [10-K](https://www.sec.gov/Archives/edgar/data/1021860/000119312526048350/nov-20251231.htm).

BKR no entra en el cuadro cuantitativo por el cambio de perímetro y financiación de Chart en 2026 y su mezcla industrial. [Cierre oficial de Chart](https://investors.bakerhughes.com/news/press-releases/news-details/2026/Baker-Hughes-Completes-Acquisition-of-Chart-Industries/default.aspx). No es necesario inventar un proforma para obtener una lista más larga de comparables. Precios: [HAL](https://stockanalysis.com/stocks/hal/history/), [SLB](https://stockanalysis.com/stocks/slb/history/), [WFRD](https://stockanalysis.com/stocks/wfrd/history/), [NOV](https://stockanalysis.com/stocks/nov/history/). Las acciones, deuda y reconstrucción anual + nueve meses actuales − nueve meses previos quedan en `build_comps.py`/`comps.json`; el extracto de filas seleccionadas está en `peers/source_rows.json`, y el paquete incorpora además las tablas completas disponibles en `peers/*_rows.json` y las tablas anuales y trimestrales de WFRD en `sources/`. Así puede contrastarse cada entrada del cálculo, no solamente ejecutar sus constantes.

## 8. Pruebas de tesis, eventos y condiciones de entrada

**A favor:** guía oficial para 2027 de crecimiento y margen con Norteamérica plana; recuperación internacional diversificada; descenso de costes SAP posible; liquidez amplia frente al vencimiento de 2027; precio compatible con un conjunto constructivo sin hipótesis extremas; margen histórico de 2023/24 superior al objetivo central.

**En contra:** EBIT ajustado y capacidad normalizada TTM siguen inferiores; cobros e inventario consumen caja; capex por debajo de amortización y ventas de activos inflan la apariencia del FCF; reestructuraciones no infrecuentes; exposición a Oriente Medio, México, América Latina y presupuestos de productores; condiciones de Keystone y carveout de químicos no publicados con precisión; obligaciones fiscales y pensiones; precio actual más cercano al caso constructivo que al central.

**Qué mejoraría la tesis:** cobros de Q4 convertidos en caja, salida de SAP con costes residuales controlados, margen operativo acercándose al 15% sin repetir ganancias puntuales, crecimiento internacional con retornos no inferiores al capital invertido, y presupuesto de capex para 2027 que sostenga reposición y crecimiento. **Qué la dañaría:** se prorrogan los cobros, se financia una expansión sin rendimientos, Norteamérica sigue cayendo más que la previsión plana, o el 15% depende de excluir costes que siguen reapareciendo.

**Calendario:** Q3 ya está publicado, por lo que no hay razón para posponer esta revisión por una publicación pendiente esta semana. Al 4 de noviembre, el [calendario IR](https://ir.halliburton.com/news-and-events/event-calendar) no anuncia fecha exacta de Q4 2026; no se inventa una fecha de enero de 2027. Próximos hitos operativos: cierre del SAP en Q4, cobros de fin de año, guía formal de 2027 y detalles de Keystone. La actualización de Argentina de octubre limita el trabajo en Sea Lion/Malvinas, no describe una salida general de Argentina. [Comunicado sobre Argentina](https://www.halliburton.com/en/about-us/press-release/halliburton-provides-update-on-argentina.html).

La eventual entrada exige precio actual, señal Stage 3.5 y riesgo de cartera verificados. El viejo RSI de 53,3 y Stage 2 «Sí» del escáner del 2 de noviembre no autorizan una entrada hoy. No se usa un «descuento mínimo del 15%», no hay un mínimo de crecimiento impuesto y no hay un stop inventado. **Conclusión: investigación cerrada con limitaciones del dato explícitas; candidato de recuperación condicional, sin señal operativa validada.**

## 9. Reproducción y límites de precisión

`python build_history.py`, `python model.py`, `python build_comps.py`, `python build_report.py`. Los tres CSV contienen diez años de FCFF. `history/history.csv` y JSON separan GAAP, estimaciones de SBC/leasing y normalización. Los archivos de origen extraídos conservan celdas y URLs; el paquete público no necesita republicar transcripciones licenciadas completas.

Este análisis termina con lo que el emisor públicamente permite comprobar: no hay datos inventados de SBC trimestral, carveout orgánico, términos de Keystone, futura resolución tributaria o señal técnica. Las estimaciones explícitas permiten valorar con rangos; no justifican prometer certeza ni un balance proforma exacto. Las cifras redondeadas del texto pueden diferir de decimales en JSON; código y JSON son la referencia aritmética.
'''
# Editorial spacing in Spanish narrative: preserve ordinary word boundaries, never emit compressed handoff style.
replacements={
 'despuésdeSBC':'después de SBC','FCFF':'FCFF','noestáaisladamente barata':'no está aisladamente barata',
}
for a,b in replacements.items():text=text.replace(a,b)
import re
# Keep links and code identifiers intact while adding ordinary prose word spacing.
parts=re.split(r'(https?://[^)\s]+|`[^`]+`)',text)
for i in range(0,len(parts),2):
 z=parts[i]
 z=re.sub(r'([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])(\d)',r'\1 \2',z)
 z=re.sub(r'(\d)([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])',r'\1 \2',z)
 z=re.sub(r'(%)([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])',r'\1 \2',z)
 z=re.sub(r',(?=[A-Za-zÁÉÍÓÚÜÑáéíóúüñ])',', ',z)
 z=re.sub(r'([a-záéíóúüñ])([A-ZÁÉÍÓÚÜÑ])',r'\1 \2',z)
 parts[i]=z
text=''.join(parts)
for a,b in {'hastaagosto':'hasta agosto','enfebrero':'en febrero','enproveedores':'en proveedores','decuentas':'de cuentas','D&Acentral':'D&A central','ybeta':'y beta','alplan':'al plan','EVcentral':'EV central','produceequity':'produce equity','EVproviene':'EV proviene','enmárgenes':'en márgenes','reducecentral':'reduce central','inversiónterminal':'inversión terminal','WCenprimer':'WC en el primer','Sensibilidadleasing':'Sensibilidad leasing','Stock Analysis':'StockAnalysis','Champion X':'ChampionX','DCFHAL':'DCF de HAL','EBITGAAP':'EBIT GAAP','ventasde activos':'ventas de activos','A 137':'A137','BBB+/A 3':'BBB+/A3','Balance Sep 30':'Balance del 30 de septiembre','balance Sep 30':'balance del 30 de septiembre','a Sep 30':'al 30 de septiembre','leasings':'leasing'}.items():text=text.replace(a,b)
text=re.sub(r'\bQ ([1-4])\b',r'Q\1',text)
text=re.sub(r'\b9 M\b','9M',text)
text=text.replace(';41','; 41').replace('Vs.34,07','Vs. 34,07').replace('porΔventas','por Δventas').replace(';5,5','; 5,5').replace(';6,5','; 6,5').replace(';100','; 100').replace('ventas:27','ventas: 27').replace('operativa:28','operativa: 28').replace('año:27','año: 27')
(P/'report.md').write_text(text)
print('written',len(text.split()),'words')
