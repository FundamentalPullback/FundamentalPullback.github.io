from pathlib import Path
import json
p=Path(__file__).parent;x=json.loads((p/'model/inputs.json').read_text());o=json.loads((p/'model/results.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text());b=o['scenarios']['base'];rates=json.loads((p/'model/rates.json').read_text())
def f(v):return f'{v:,.2f}'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(c) for c in row)+' |' for row in rows)+'\n'
text='''# Guidewire (GWRE): negocio legado, compra de Hyperexponential y capital sin cerrar

Corte: 4 de noviembre de 2026, después del cierre regular de EE. UU. Investigación propia parcial condicionada. Revisión independiente completada para este alcance parcial. No es una valoración integral ni una aprobación de entrada. USD millones salvo indicación; acciones en millones; cuentas de Hyperexponential en GBP, sin conversión implícita.

## Conclusión

Guidewire mejora su negocio publicado: ingresos FY26 crecen 22,7%, EBIT GAAP pasa de 41,1 a 149,9 y suscripciones/soporte llegan a 970,9. El FCF publicado de 358,7 incluye el efecto de SBC y cobros anticipados; FCF menos SBC es 176,9 como diagnóstico, no FCFF normalizado ni beneficio distribuible certificado.

La compra anunciada de Hyperexponential exige 1.700 de efectivo, ajustables, y hasta 400 adicionales; el préstamo comprometido de 1.000 no elimina ese coste económico. Las cuentas públicas del target permiten analizar su historia, pero no cierran el precio ajustado, retenciones, earnout, PPA, sinergias ni capital combinado. Por eso el valor total de GWRE queda nulo.

El modelo separa un contrafactual del negocio legado sin adquisición y un residuo de ese negocio después de financiar la compra, todavía sin sumar el valor desconocido del target. Ninguno es una tasación de la acción actual ni una cota inferior. El residuo adverso negativo es un déficit económico del ejercicio, no un precio negativo ni una valoración de cero.

Scanner 4nov: Last169,66, Quality100, Opportunity90, RSI52,5; margen operativo ausente y Stage2 ausente. No se rellenan con estimaciones ni se hereda un Sí antiguo. Cierre regular verificado170,50 a16:00EST, separado del scanner y de cualquier after-hours. [Histórico de mercado](https://stockanalysis.com/stocks/gwre/history/). Triage previo A102 no aporta un modelo ejecutable recuperado: esta es una construcción propia nueva.

## Negocio, calidad y qué puede fallar

Guidewire vende infraestructura crítica de pólizas, siniestros y facturación a aseguradoras P&C. La migración cloud, costes de sustitución e integración apoyan permanencia, pero no garantizan rentabilidad: compradores concentrados tienen poder negociador; implementación, fiabilidad, ciberseguridad y competencia de plataformas o IA pueden erosionar precios y retención. El negocio es software, no una aseguradora; no se trata como cartera financiera.

RPO divulgado al31jul es aproximadamente4.300; no equivale a caja disponible ni incluye todos los servicios cancelables por tiempo/materiales. Licencias a plazo reconocidas de inicio y suscripciones reconocidas durante el contrato distorsionan comparación trimestral. ARR y Fully Ramped ARR son métricas contractuales diferentes de ventas, y no se transforman automáticamente en EBIT. La compañía advierte que el CFO seguirá concentrado enQ4 por facturación anual. [10-K FY26, negocio y notas1–2](https://www.sec.gov/Archives/edgar/data/1528396/000152839626000046/gwre-20260731.htm).

## Historia normalizada y ancla

TTM disponible termina31jul2026 y coincide con FY26; no hay resultados de octubre publicados en este corte. Las cuatro filas trimestrales suman el año con tolerancia de1.000USD por redondeo. FY24 procede del10-KFY25 para comparativos no presentes en elFY26. Cuentas USGAAP; no mezclar EPS ajustado original con el recasteado desdeQ3 por cambio de tratamiento FX.

'''
text+=table(['Período','Ventas','EBIT GAAP','EBIT + amort. adquirida','CFO','PPE + software caja','FCF','SBC','FCF − SBC'],[[r['period']]+[f(r[k]/1000) for k in ['revenue','ebit_gaap','ebit_plus_acquired_amort_retaining_sbc','cfo']]+[f((r['capex_cash']+r['software_capitalized_cash'])/1000)]+[f(r[k]/1000) for k in ['fcf','sbc_expense','fcf_less_sbc_sensitivity']] for r in h['rows']])
text+='''
La reconstrucción FY26 es149,874 EBIT+6,701 amortización adquirida=156,575 antes de esa amortización, reteniendo181,799 de SBC y1,510 de gasto de adquisición/holdback. No se usa339,884 de EBIT non-GAAP como beneficio del propietario. Impuesto pleno24% sobre el EBIT previo a amortización adquirida: no se inventa escudo fiscal de compra. La amortización de software propio14,4 permanece en EBIT y se suma con depreciación8,8 como D&A productivo23,2; su reposición se financia en capex. No sumar nuevamente6,701 como D&A en el modelo.

FCF FY26=389,716−12,056−19,003=358,657; FY25=280,412; FY24=177,221. Restar SBC produce176,858/118,856/30,761, únicamente diagnóstico de coste económico. Comisiones capitalizadas ya consumen CFO, por lo que no se vuelven a restar al FCF. Amortización de costes contractuales35,011 no se añade como efectivo gratis al FCFF; el circulante/reinversión del modelo debe financiar nuevos contratos.

El aumento de ingresos diferidos aportó93,675 al CFOFY26 frente56,617FY25; FCF excluyendo ese flujo sería264,982, pero esta resta tampoco es una normalización completa porque omite otros cambios de circulante. Q4 produjo283,886/389,716, aproximadamente73% del CFO anual. No se anualiza ese trimestre. FY26 impuesto contable24,834, efectivo13,171 y beneficio fiscal SBC20,908 son distintos;24% es hipótesis sostenible, no extrapolación de tasa efectiva15,1% ni de beneficios fiscales anteriores. DTA286,585 no se suma además como caja.

[10-K FY26](https://www.sec.gov/Archives/edgar/data/1528396/000152839626000046/gwre-20260731.htm); [10-K FY25](https://www.sec.gov/Archives/edgar/data/1528396/000152839625000221/gwre-20250731.htm); [Q1](https://www.sec.gov/Archives/edgar/data/1528396/000152839625000244/gwre-20251031.htm); [Q2](https://www.sec.gov/Archives/edgar/data/1528396/000152839626000014/gwre-20260131.htm); [Q3](https://www.sec.gov/Archives/edgar/data/1528396/000152839626000027/gwre-20260430.htm); [Q4/FY26 resultados](https://ir.guidewire.com/node/26281/pdf).

## Hyperexponential: contrato y financiación

Anuncio27oct:1.700 cash, incluido pool de retención de empleados según presentación, sujeto a ajustes de circulante/caja/deuda/ciertas retenciones. Hasta400 adicionales dependen de objetivos de ingresos recurrentes después del cierre; no es su valor razonable. El8-K afirma que la adquisición no está sujeta a condiciones de cierre y no depende de obtener financiación. Esto NO prueba que ya haya cerrado. Se esperaQ2FY27, hasta31ene2027. La financiación sí tiene condiciones limitadas. No se inventa una probabilidad de ruptura.

Préstamo TermA comprometido1.000 conBofA/Citi; SOFR+1–2% o base+0–1%, por apalancamiento; vence2dic2029, amortización anual5% desde el quinto trimestre fiscal completo posterior al cierre. Es compromiso, no deuda ya dispuesta. Contrato íntegro de adquisición/carta de deuda se anunció para el próximo10-Q; el8-K resumido no permite certificar todas las retenciones, covenants o ajustes.

Álgebra: nueva caja+1.000, compra−1.700, nueva deuda−1.000⇒cambio neto−1.700 antes de earnout/fees/valor adquirido. No deducir2.700 ni contar1.000 como patrimonio. El escenario de financiación central añade reserva ilustrativa200 de earnout y25fees:−1.925 netos. Son hipótesis, no deuda contractual valorada a mercado. Se prueban0/200/400 y0/25/50. Caja base1.215,285−700−200−25=290,285, como stress de reserva inmediata (no calendario contractual de pago deearnout), antes de flujos intermedios y ajustes, inferior a reserva operativa seleccionada300; no se certifica suficiencia de liquidez ni refinanciación de vencimientos2029. Revolver300 es capacidad condicionada, no caja.

La presentación promete al menos650pb de crecimiento ARR inorgánicoFY27 y150pb adicionales de crecimiento ARR orgánico después deFY27. No es una divulgación de ventas/FCF del target ni una sinergia ya cobrada. La guíaQ1 permanece; se actualizaráFY27 en llamada de diciembre. No se da por confirmado un día exacto de resultados.

[8-K27oct](https://www.sec.gov/Archives/edgar/data/1528396/000119312526432656/d121813d8k.htm); [presentación oficial](https://ir.guidewire.com/static-files/53058aa6-a03a-4559-ac18-f5560365c89e); [anuncio](https://ir.guidewire.com/news-releases/news-release-details/guidewire-signs-definitive-agreement-acquire-hyperexponential).

## Cuentas primarias del target: datos disponibles, no tasación ausente por desconocimiento

HyperexponentialLtd, company11044276, publica cuentas consolidadas británicas. FY31ene2026:ventas£34,826463m, EBIT−£6,153648m, neto−£4,541497m, CFO£1,914824m yPPEcash£0,243240m. FY31ene2025:ventas£24,368383m y EBIT−£5,413777m. La comparación muestra crecimiento, no rentabilidad madura.

El siguiente período es SOLO dos meses,1feb–31mar2026:ventas£7,869244m, EBIT£0,060223m, neto£0,257095m, CFO£7,350685m yPPEcash£0,027338m. El estado de resultados muestra gasto administrativo£5,810749m; no usar el errorOCR£6,810749m ni una mención narrativa de beneficio operativo£0,6m como si conciliara con la tabla. La transición de ingresos FRS102 aporta£0,204716m: excluirla sola llevaría EBIT a−£0,144493m antes de ajustes de leases/FX. No multiplicar ventas o CFO de dos meses por seis para llamarlo año normalizado.

El CFO corto está dominado por liberación de deudores£14,281700m menos reducción de acreedores£7,060959m. Desde1feb adopta nuevas reglasFRS102 de ingresos y leases, con comparativos no recasteados; ROU inicial≈£2,01m y lease liability≈£1,9m. El reordenamiento de pagos de alquiler entre CFO/financiación impide comparar FCF crudo sin ajustes. GBP no es USD y FRS102 no es USGAAP; no se mezcla el target con GWRE a una FX no indicada.

Excluyendo además la ganancia FX operativa£0,444274m, el EBIT corto sería−£0,588767m antes de homogeneizar leases. Los movimientos netos de deudores/acreedores explican98,2%delCFO; quitarlos, capex y todo el cash de leases deja£0,012283m, todavía incluyendo devolución fiscal£0,315546m. No se presenta esa cifra como beneficio sostenible. No existe desglose suficiente para inventar capitalización deI+D. Note24redondea pasivo inicialleases£1,9m, frente≈£2,010m implícitos por mecánica; se mantiene la discrepancia, no se fabrica conciliación.

Estas cuentas verifican tamaño y calidad del flujo, pero no entregan un caso futuro validado para monetizar crecimiento, retención, sinergias y coste de adquisición. El valor operativo deHX queda desconocido, no cero. Tampoco se añade su caja histórica£42,779m de marzo encima del precio sin conciliar la cláusula de ajuste por caja/deuda. Las cifras y comprobaciones detalladas están en transaction/target_accounts.*.

[Companies House, historial oficial](https://find-and-update.company-information.service.gov.uk/company/11044276/filing-history); [cuentas enero2026](https://find-and-update.company-information.service.gov.uk/company/11044276/filing-history/MzUzMjk1NDcyNGFkaXF6a2N4/document?download=0&format=pdf); [cuentas marzo2026](https://find-and-update.company-information.service.gov.uk/company/11044276/filing-history/MzUzOTEwOTYwM2FkaXF6a2N4/document?download=0&format=pdf).

## Capital: reservas explícitas y límites

Caja372,887+inversionesCP380,175+LP462,223=1.215,285 al31jul. Principal convertible690, no carrying678,094. Reserva operativa300 elegida; reserva28,906 por grossUTB histórica, no pago fiscal cierto (parte reduce atributos fiscales); excise recompras3,1. Puente seleccionado antes de compra193,279, después de−1.925 de financiación de compra−1.731,721. Se prueba liberarUTB y cambiar caja/reservas. Ninguna cifra certifica capital al4nov.

Se excluyen inversiones estratégicas35,029 de valoración económica no conciliada; no valen cero ni se deducen otra vez como gasto futuro. Sus ganancias no operativas no están en EBIT. Caja de julio no recoge recompras o flujos posteriores desconocidos. RecomprasFY26 consumieron606,309 frente358,657FCF; autorización remanente31,9 no es ejecución ni obligación. Sensibilidad−31,9 es sólo un stress. No se infiere ausencia de recompras de la diferencia de202acciones entre julio y agosto.

Acciones spot81,992669 al31ago frente81,992467 al31jul; modelo84,2 como selección ilustrativa de dilución cercana a awards completos2,146189 y opciones0,096573 a strike65,42. No es captable actual, denominadorGAAP ni cierre de todas las futuras concesiones/retencionesHX. FY26 diluidas ponderadas85,405177 son otra medida. SBC pendiente307,868 no se suma automáticamente como deuda, porque el coste operativo futuro ya permanece en márgenes.

Convertible2029:690principal, cupón1,25%, strike244,65, capcappedcalls329,33. Se liquida al menos principal en cash; a170,50 no hay exceso intrínseco. No se suman2,820375acciones completas manteniendo690 de deuda. La sensibilidad separa exceso de conversión y compensación teórica de cappedcalls; coste histórico58,788 ya pagado, no se descuenta otra vez. Cobertura no es garantía perfecta ante contraparte/ajustes. Para precios superiores alcap sería necesaria dilución incremental; las centrales del legado son inferiores alstrike. Inversos resueltos al170,50 observado no necesitan asumir convert por encima delcap.

Arrendamientos operativos36,893 no se restan como deuda cuando el margen conserva alquileres. NuevoHQ firmado3sep:90meses desde1jul2027, pagos mínimos41,5; no se descuenta toda esa suma sin descontar y además la renta del modelo. Su coste y capacidad siguen en el riesgo de margen. Circulante/reserva300 no es una conciliación exacta de bonus86,824 y demás devengos: se prueba caja adicional y margen, sin calificar todas las obligaciones operativas como deuda.

## DCF a diez años: sólo legado y residuo financiado

El primer añoFY27 usa ingresos1.717 y EBIT previo a amortización214,625 enbase (margen12,5%), comparable en orden con guía previa207GAAP central más amortización; no es guidance postcompra. Se retieneSBC; márgenes posteriores son hipótesis, no sumas de objetivos non-GAAP. Impuesto24%, depreciación/software23,2 creciendo conventas, capex físico+software2,5%ventas y circulante incremental8%del incremento positivo de ventas. El suelo económico financia TODA subida positiva deNOPAT/ROIC, también la mejora de margen: no presume expansión gratis. Reinversión=max(capex−D&A+WC, ΔNOPATpositivo/ROIC,0).

Terminal conserva ambos suelos: máximo de capex terminal−D&Aterminal+WCterminal yNOPATterminal×g/ROIC. No hay escudo ficticio de amortización adquirida ni doble addback. No se perpetúa CFO por cobros anticipados. La reserva de circulante es proxy, no balance contractual; sensibilidades de inversión importan incluso donde domina el suelo económico.

Fecha: FY27 termina31jul2027,269días después delcorte. Se descuenta a269/365años y los restantes a1,737…9,737. El flujo anualFY27 se pondera269/365 como aproximación de tiempo, NO reproducción de caja restante observada. El modelo no afirma que cobros sean uniformes: hay concentraciónQ4; se prueba primerflujo50%/73,7%/100%. FaltaQ1octubre, de modo que fecha y capital no están certificados y no se llama conservador automáticamente al conjunto.

'''
text+=table(['Caso','WACC seleccionado','g','ROIC','Ventas año10','Margen año10','EV legado','Contrafactual sin compra/acción','Residuo financiado/acción','%EV terminal'],[[k,f(r['discount']*100)+'%',f(r['terminalGrowth']*100)+'%',f(r['roic']*100)+'%',f(r['rows'][-1]['revenue']),f(r['rows'][-1]['margin']*100)+'%',f(r['operatingEV']),f(r['standaloneCounterfactualPerShare']),f(r['fundedLegacyResidualPerShare']),f(r['terminalShareOfEV']*100)+'%']for k,r in o['scenarios'].items()])
text+='\n### Diez años base, columnas que concilian\n'
text+=table(['FY','Ventas','EBIT pre amort adquirida','NOPAT','D&A productivo','Capex','WC','Reinversión neta max','FCFF año','Flujo usado','PV'],[[r['year']]+[f(r[k])for k in ['revenue','ebitBeforeAcquiredAmort','nopat','productiveDA','productiveCapex','workingCapitalInvestment','netInvestment','fcffFullYear','recognizedCash','pv']]for r in b['rows']])
text+=f"\nBase terminal: NOPAT{f(b['terminal']['nopat'])}, inversión{f(b['terminal']['netInvestment'])}, FCFF{f(b['terminal']['fcff'])}, PVterminal{f(b['terminal']['pv'])}. PrimerFCFFanual{f(b['rows'][0]['fcffFullYear'])}: la mejora de margen requiere inversión, no todo beneficio es caja libre.\n"
text+=f"\nTipos: Treasury4nov4,90%, ERP4,41%, beta histórica1,03⇒ke{rates['mechanicalCostEquity']*100:.3f}%; coste deuda marginal elegido6% (no cupón1,25%), WACCproxy precompra{rates['proxyPreDealWacc']*100:.3f}%. Descuento base9,5% seleccionado por incertidumbre, no simple redondeo ni WACC combinado certificado. Escenarios8–11,5%, no probabilidades. [Treasury](https://home.treasury.gov/resource-center-data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026), [ERP](https://pages.stern.nyu.edu/~adamodar/), [beta](https://stockanalysis.com/stocks/gwre/statistics/).\n"
text+='\n## Inversos, sensibilidad y qué está pagando el mercado\n'
for k,r in o['inverse'].items():text+=f"\nInverso {k}: incremento paralelo{r['parameter']*100:.2f}puntos porcentuales, ventas año10{f(r['year10Revenue'])}, margen final{r['year10Margin']*100:.2f}%, primerFCFFanual{f(r['firstYearFCFF'])}.\n"
text+=f"\nAmbos inversos fuerzan que el legado por sí solo explique170,50 DESPUÉS de financiar la compra, sin aportarEVdel target. No afirman que el mercado descuente literalmente ese margen extremo ni prueban sobrevaloración del combinado. Con legado base, el EVadicional/sinergias requerido por identidad es{f(b['unknownTargetEVRequiredAtPrice'])}; no es valor tasado deHX y también puede reflejar hipótesis erradas del legado. La raíz de margen exige financiación inicial superior a liquidez demostrada; no se certifica su viabilidad. Se verificanbracket,residuo y1.000intervalosmonótonos por raíz.\n"
for label,rows in o['sensitivities'].items():
 text+='\n### '+label+' (residuo financiado, no FVtotal)\n';text+=table(list(rows[0]),[[(f(v*100)+'%' if k in ['discount','g','ratio','roic','fraction'] else f(v)) if isinstance(v,(float,int)) else v for k,v in r.items()]for r in rows])
text+='''
Las tablas expresan tasas como porcentajes; los archivosJSON retienen fracciones decimales y precisión completa. No deducir sensibilidad deearnout ypuente dosveces. No usar margen de seguridad contra32,23 como si fuera fairvalue íntegro: falta el activo adquirido y el capital actual.

## Comparables y contraste operativo

Screen a cierresNov4: EV/EBITGAAP89,77xGWRE,24,69xCRM,44,49xWDAY; antes deamortizaciónadquirida85,93x/20,10x/39,60x, reteniendoSBC. MárgenesGAAP10,16%/19,88%/10,68%. No son múltiplos de negocio combinado actual.

Se acompaña comps/ conCRM/WDAY: TTMjulio construido desdeFY+H1−H1previo yGWREFY26julio, precios regularesNov4. SBC retenido y amortización adquirida separada cuando la fuente la revela. Es un contraste de software empresarial, no pares perfectos de seguros. Balances/acciones son fechados y adquisiciones/financiación posteriores pueden impedir un EVactual homogéneo. No se aplica una mediana como target ni se convierte diferencia de múltiplo en oportunidad automática. El screen no sustituye un múltiplo proforma deGWREconHX.

[CRM Q2](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm), [CRM FY26](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm), [WDAY Q2](https://www.sec.gov/Archives/edgar/data/1327811/000132781126000044/wday-20260731.htm), [WDAY FY26](https://www.sec.gov/Archives/edgar/data/1327811/000132781126000014/wday-20260131.htm), [notas WDAY octubre](https://www.sec.gov/Archives/edgar/data/1327811/000110465926118496/tm2626731d6_8k.htm). Precios: [CRM](https://stockanalysis.com/stocks/crm/history/), [WDAY](https://stockanalysis.com/stocks/wday/history/).

## Calendario, pruebas pendientes y decisión

Confirmado: última publicaciónFY26/Q4el3sep; anuncioHX27oct; guía próxima actualización en diciembre2026, día exacto no confirmado en primarias revisadas. Cierre esperadoHXenQ2FY27hasta31ene2027 no es fecha deearnings ni cierre ocurrido. Estimaciones deproveedores2/3dic no liberan el calendario delplan.

Para pasar de parcial a valoraciónintegral: próximo10-Qyguía diciembre; contrato/retenciones/earnout y financiación final; caja/deuda/recompras/acciones actuales; targetnormalizado bajo cambiosFRS102yproformaUSGAAP/PPA; crecimiento rentable conSBC ysoftware financiados; fiscalidad/DTA/UTB reconciliada; pares proforma y filtro técnico vigente. No hay gestión previa ni operación que ejecutar desde este dossier.

ConclusiónES: mejora operativa real, pero adquisición grande y capital incompleto; mantener investigación parcial, sin tasación total ni entrada. ConclusionEN: operating progress is real, but the acquisition and unreconciled capital prevent a certified total valuation or entry. Legacy scenarios are conditional exercises, not current share targets.

## Reproducción y alcance

Ejecutar python -S reproduce.py en una copia limpia. Sólo stdlib; fuentes completas no se distribuyen. Scripts, hechos derivados, ledger y enlaces permiten auditar historia, financiación, DCF10años, inversos, pares y QA. Fuentes primarias enlazadas; precios/beta de proveedor etiquetados. Ninguna autorización de publicación equivale a compra, venta o modificación de cartera.
'''
(p/'report.md').write_text(text)
