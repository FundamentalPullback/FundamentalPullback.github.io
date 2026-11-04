import json,pathlib,html
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());h=json.loads((P/'history/financial_history.json').read_text())['periods']
s='''# Fortinet (FTNT): crecimiento rentable, caja anticipada y valoración condicionada

Corte de investigación: 4 de noviembre de 2026, 20:01 UTC. USD millones salvo precios y EPS. Investigación condicionada con auditoría independiente completada; no cierre integral de Stage 3, no latestCompleted, no aprobación Stage 3.5 ni entrada. No modifica gestión ni operaciones.

## 1. Conclusión y evidencia favorable/adversa

Los ingresos TTM aumentan de 6.554,7 a 7.880,9 millones USD y el EBIT GAAP de 2.033,2 a 2.599,2 millones, manteniendo la remuneración en acciones como coste operativo.

El FCF TTM de definición corporativa sube de 2.014,4 a 3.414,3 millones USD, pero 652,4 millones de la mejora proceden de mayor aportación de ingresos diferidos y 164 millones de menor capex.

La caja y las inversiones de renta fija suman 5.287,3 millones USD frente a 500 millones de principal de deuda, antes de reservas operativas y fiscales.

Los escenarios condicionados de 29,28 / 51,35 / 95,85 USD quedan por debajo del cierre de referencia de 128,11 USD; ninguno acredita margen de seguridad para una entrada.

La discrepancia entre el escáner del 28 de octubre a 129,00 USD y el cierre histórico de esa sesión a 174,08 USD sigue sin conciliar; no se sustituyen ni se mezclan ambas observaciones.

Fortinet combina equipos de seguridad, software y servicios recurrentes. La base instalada y FortiOS/FortiASIC pueden favorecer renovaciones, integración y eficiencia, pero esas ventajas no prueban por sí solas cuota futura ni inmunidad frente a fallos. Crecimiento de producto ligado al ciclo de renovación, competencia de plataformas, ejecución de SASE y coste de ampliar infraestructura son riesgos económicos concretos. No se presenta una evaluación técnica independiente de vulnerabilidades o una certificación de cumplimiento normativo.

## 2. Historia comparable y definiciones

La tabla siguiente recoge tres ejercicios, los últimos cuatro trimestres, sus cuatro comparativos y TTM. EBIT es operativo GAAP, no EBITDA ajustado. CFO y capex trimestrales se obtienen por diferencias YTD; Q4 por FY menos 9M. EPS de Q4 es directamente publicado; TTM suma cuatro EPS trimestrales redondeados, no un EPS anual GAAP certificado. El historial adjunto contiene márgenes, producto/servicios, SBC, contratos, impuestos y todas las fuentes.

'''
s+='| Periodo | Ingresos | EBIT | NI | EPS | CFO | PPE | FCF compañía | SBC CF |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for k in ['FY2023','FY2024','FY2025','Q42024','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','TTM_September_2025','TTM_September_2026']:
 r=h[k];s+='| '+k+' | '+' | '.join(f'{r[x]:,.2f}' for x in ['revenue','ebit','net_income','diluted_eps','cfo','capex','fcf_company_definition','sbc_cf'])+' |\n'
s+='''
El CFO menos PPE TTM es 3.431,3, distinto del FCF corporativo de 3.414,3 por el cobro de escrow de 17 en Q3. El comparativo corporativo excluye 14 de cobro por propiedad intelectual. FCF corporativo menos SBC del estado de flujos es 3.109,9 frente a 1.741,6: sensibilidad económica calculada, no owner FCF publicado ni FCFF. SBC es un ajuste no monetario en el estado de flujos, no pago en efectivo. Q3: CFO 946,0 menos PPE 64,2 menos escrow 17,0 = 864,8.

El crecimiento TTM del CFO es 1.238,9. La aportación de ingresos diferidos pasa de 631,5 a 1.283,9, y representa aproximadamente 34,8 % del CFO actual. Son anticipos estructurales de clientes, no ingresos ficticios; tampoco son incremento perpetuo de beneficio. Retirar toda esa aportación es solo una sensibilidad, no normalización preferida. En el modelo no se concede financiación incremental por ingresos diferidos y tampoco se resta su saldo completo como deuda: una decisión conservadora explícita, no una estimación demostrada de coste de servicio pendiente.

Los costes de contratos diferidos son distintos: activo de 815,4 y gasto de caja 9M de 370,1 frente a amortización de 290,2. La amortización de contratos no se añade a D&A del DCF; se financia el crecimiento del activo neto. SBC queda en márgenes y no se resta otra vez del FCFF proyectado. Las acciones futuras aún pueden diluir.

Linksys se consolida al 100 % desde el 31 de enero de 2025: el TTM comparativo incluye ocho meses frente a doce actuales. No se llama orgánico a todo el crecimiento. El precio adicional de compra fue 20,8; el valor del interés anterior 21,5 y los ajustes de compra generaron ganancia de 39,9, revalorización de 10,8 y baja fiscal de 30,6. Las ganancias están debajo del EBIT; no se restan del operativo otra vez. Lacework también altera comparabilidad histórica. La adquisición de seguridad AI Q3 de 13,4 en efectivo no equivale al flujo neto 9M de adquisiciones de 9,8. No se certifica un perímetro orgánico reconstruido.

## 3. Beneficio, impuestos y reinversión

El beneficio 9M se beneficia de deducciones FDDEI de 104,1 y beneficios fiscales de SBC de 52,5, frente a impuesto total de 356,5. La tasa efectiva de aproximadamente 17 % no se perpetúa automáticamente. El escenario central utiliza 22,5 %, adverso 25 % y favorable 20 %, supuestos del analista. Sensibilidad a 18 % no es certificación de una tasa sostenible. La dirección indica ausencia de efecto material de Pilar Dos durante 9M; eso no cierra toda la exposición futura.

El capex TTM de 255,6 está por debajo del comparativo de 419,6. La guía primaria de PPE para 2026 es 390–420. De las compras 9M, 95,8 corresponden a inmuebles (64,2 terrenos, 31,6 edificios); no se añaden de vuelta como si fueran automáticamente excedentarios. Depreciación física 9M 91,5 frente a D&A total 120,6; el DCF no devuelve amortización adquirida ni contratos. Tampoco se suma valor inmobiliario a un negocio cuyos costes y rentas puedan depender de esos activos.

Compromisos de inventario de 1.929,5 (1.144,5 resto de 2026), reserva por exceso de 30,3 ya contabilizada, y otros compromisos contractuales de 134,1 exponen a errores de demanda. No se convierten todos en deuda financiera ni se resta dos veces la reserva. El inventario pasó de 399,5 a 591,2. La liquidez no elimina el riesgo de normalización del ciclo.

## 4. Puente de capital y dilución

Caja 3.750,6 + inversiones disponibles para venta 1.536,7 = 5.287,3. Se excluyen del caso base 31,1 de valores de renta variable, sin declararlos sin valor. El saldo total de inversiones cortas y largas es 1.567,8. Los importes son del 30 de septiembre, no una certificación a 3 de noviembre.

Se resta principal de deuda de 500 (valor contable 497,1); los otros 500 vencidos en marzo ya se pagaron. Se retiene caja operativa equivalente a 15 % de ventas TTM, 1.182,135, y estrés bruto fiscal de 109,7 (UTB 96,2 más intereses/penalidades 13,5). Este último no es una pérdida esperada ni un vencimiento cierto; cuantía y calendario son inciertos y la reserva puede ser conservadora frente al tratamiento de impuestos normalizados. Las sensibilidades de reserva cero y doble (219,4) cuantifican ese posible solapamiento, sin cambiar el caso central. Resultado: puente positivo de 3.495,465.

No se monetizan activos fiscales diferidos de 1.306,9, goodwill ni inmuebles. Arrendamientos conservan renta operativa en EBIT y no se deducen de nuevo como deuda; pagos futuros de alquiler de 63,4 no son saldo financiero descontado. No se certifica ausencia de contingencias adicionales o disponibilidad irrestricta de todo el efectivo por jurisdicción.

Denominador: 742,6 millones, promedio diluido Q3, como proxy y no máximo futuro. Al 30 de septiembre había 734,6 millones emitidos, 7,7 millones de RSU y 5,5 millones de opciones con strike medio 59,15; no se suman indiscriminadamente al promedio diluido. Nuevas PSU pueden pagar hasta 200 % de objetivo; no hay reconstrucción completa de todos los premios futuros. Se muestra sensibilidad de +5 % de acciones, manteniendo SBC como coste. La autorización de recompra restante de unos 2.000 al 29 de octubre no es recompra ejecutada ni caja que deba deducirse hoy.

## 5. DCF de 10 años: hipótesis, no guía de la empresa

No existía DCF ejecutable de A112: esto es nueva investigación, no réplica certificada del modelo antiguo. Cinco años explícitos más cinco de transición; no se capitaliza directamente el FCF extraordinariamente alto actual. Ancla TTM: ingresos 7.880,9 y EBIT GAAP 2.599,2. Se retiran 5,5 de ganancias por propiedad intelectual (FY25 10,4 menos 9M25 9,0 más 9M26 4,1), dejando 2.593,7 como ancla normalizada de NOPAT; los márgenes futuros no incorporan nuevas ganancias de esta clase. Esta ganancia contable no equivale al cobro de 14 excluido del FCF comparativo. Los escenarios no tienen probabilidades asignadas.

'''
s+='| Escenario | Crecimiento años 1–5 | Crecimiento años 6–10 | Márgenes años 1–10 | Tasa | g terminal | ROI supuesto | Impuesto | Valor |\n|---|---|---|---|---:|---:|---:|---:|---:|\n'
for k,c in m['scenarios'].items():
 s+='| '+k+' | '+', '.join(f'{100*x:g}%' for x in c['g'][:5])+' | '+', '.join(f'{100*x:g}%' for x in c['g'][5:])+' | '+', '.join(f'{100*x:g}%' for x in c['m'])+' | '+ ' | '.join(f'{100*c[x]:g}%' for x in ['w','tg','roic','tax'])+f" | {m['cases'][k]['value']:.2f} |\n"
s+='''
Las tasas de descuento 9–11 % son exigencias de rentabilidad del analista, no WACC calibrado mediante beta/ERP/riesgo país contemporáneos. ROI 15–25 % es hipótesis económica, no ROIC incremental demostrado. La desaceleración central y margen terminal de 32 % reflejan riesgo de ciclo, competencia y reinversión; la guía no confirma ese recorrido. La guía FY26 es ingresos 8.125–8.215 y margen operativo NO GAAP 36,5–37,5 %, no los márgenes GAAP del modelo. Q4 guía ingresos 2.155–2.245 y margen no GAAP 35,5–37,5 %; no se convierte esa guía automáticamente a GAAP.

NOPAT = ventas × margen GAAP × (1 − impuesto). Capex/ventas: 4,5 / 4 / 3,5 / 3,25 / 3 % y después 3 %. D&A física/ventas sube linealmente de 1,5 a 2 %; no es amortización de intangibles adquiridos. Capital circulante incremental: 5 % del crecimiento de ventas, separado del crecimiento de activos netos de contratos a razón 815,4 / 7.880,9. No hay crédito por nuevos anticipos.

Reinversión física = capex − D&A + Δcapital circulante + Δcontratos. Reinversión económica = máximo(0, ΔNOPAT) / ROI, financiando también expansión de margen. Reinversión final = máximo de ambas. FCFF = NOPAT − reinversión. El archivo explicita una reserva adicional que permite conciliar NOPAT + D&A − capex − Δcirculante − Δcontratos − reserva. No se ignoran FCFF negativos si aparecen.

Terminal: ventas y NOPAT crecen a g, y se usa el máximo entre suelo físico coherente y NOPAT terminal × g / ROI. EV suma valores presentes explícitos y terminal; se añade el puente y divide por acciones. Los suelos físicos dominan tres años adversos; el económico domina los diez centrales y favorables. Por ello las sensibilidades físicas pueden dejar el caso central idéntico: no significa que capex o contratos sean económicamente irrelevantes.

'''
s+='| Caso | EV | Puente | PV terminal/EV | Valor/acción |\n|---|---:|---:|---:|---:|\n'
for k,r in m['cases'].items():s+=f"| {k} | {r['ev']:.3f} | {r['bridge']:.3f} | {100*r['terminal_share']:.2f}% | {r['value']:.5f} |\n"
s+='\n### Sensibilidades y contraste inverso\n\n'
for k,v in m['sensitivities'].items():s+=f'- {k}: {v:.5f} USD.\n'
s+='''
El barrido inverso desplaza simultáneamente los diez márgenes de 0 a +60 puntos porcentuales en pasos de 0,5. No encuentra cruce con 128,11: su máximo es 115,51 con margen terminal 92 %. No se fuerza una raíz ni se afirma imposibilidad fuera del dominio. Tampoco se presenta ese margen extremo como económicamente plausible. La dependencia del terminal central de 64,68 % y favorable de 75,13 % limita precisión.

## 6. Pares y calidad comparativa

'''
cp=P/'comps/README.md'
s+=cp.read_text() if cp.exists() else 'Comparables primarios en preparación; no se certifica homogeneidad ni se aplica múltiplo sectorial.\n'
s+='''
## 7. Calendario, precio, riesgos y condiciones de revisión

El Q3 ya se publicó el 28 de octubre a las 16:05 EDT y el 10-Q el 30 de octubre. No hay que esperar a un evento ya ocurrido. Próxima fecha exacta de resultados no confirmada. El comunicado anuncia participación en BMO el 12 de noviembre, UBS el 2 de diciembre y Barclays el 9 de diciembre; son conferencias, no fechas de resultados y pueden cambiar. La página de eventos no fue accesible en una comprobación; eso no demuestra que no exista fecha futura.

Precio utilizado: cierre Nasdaq de 3 de noviembre, 128,11 USD. Se preserva A112 y la observación de escáner del 28 de octubre a 129,00 con QP 80 / Opportunity 85; el cierre histórico 174,08 de esa fecha es evidencia distinta, discrepancia sin resolver. No se inventa un nuevo escáner o señal técnica. Los scores históricos no levantan filtros ni aprueban compra.

Riesgos: ralentización del reemplazo de equipos, duración de contratos y menor financiación por anticipos; demanda de SASE que no compense hardware; presión competitiva y márgenes; mayor capex/contratos; dilución; fiscalidad internacional y contingencias; adquisiciones sin puente orgánico; fallos de seguridad y litigios. El filing describe alegaciones en litigios, no hechos probados por este informe; los accruals no materiales no equivalen a pérdida futura cero. Falta un análisis jurídico/técnico independiente y conciliación de disponibilidad fiscal de caja.

Para mejorar la decisión: contrastar billings y renovaciones con conversión de caja; comprobar capex FY26 frente a 390–420; reconstruir premios y caja al nuevo corte; normalizar contratos y coste de servir ingresos diferidos; calibrar coste de capital y pares homogéneos; confirmar siguiente resultado y reconciliar el precio del escáner. Ningún rango aquí es techo de compra aprobado. Owner FCF normalizado y valor integral certificado permanecen sin determinar.

## 8. Fuentes y reproducción

- Q3 10-Q: https://www.sec.gov/Archives/edgar/data/1262039/000126203926000027/ftnt-20260930.htm
- FY25: https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm
- Q3 previo: https://www.sec.gov/Archives/edgar/data/1262039/000126203925000039/ftnt-20250930.htm
- Q2: https://www.sec.gov/Archives/edgar/data/1262039/000126203926000021/ftnt-20260630.htm
- Q1: https://www.sec.gov/Archives/edgar/data/1262039/000126203926000013/ftnt-20260331.htm
- Comunicado Q3/guía/calendario: https://investor.fortinet.com/news-releases/news-release-details/fortinet-reports-strong-third-quarter-2026-financial-results
- Precios de cierre: https://stockanalysis.com/stocks/ftnt/history/

El paquete permite recalcular historia, modelo, comparables, informe y controles sin red. Contiene extractos numéricos y referencias, no filings completos. Hipótesis están separadas de hechos; investigación condicionada, no asesoramiento de ejecución.
'''
(P/'report.md').write_text(s)
(P/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>FTNT: investigación condicionada</title><style>body{max-width:1050px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(s)+'</pre></body></html>')
