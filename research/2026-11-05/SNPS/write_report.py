from pathlib import Path
import json
from readability import spaced
P=Path(__file__).resolve().parent;A=json.loads((P/'model/assumptions.json').read_text());O=json.loads((P/'model/results.json').read_text());X=json.loads((P/'model/analysis.json').read_text());H=json.loads((P/'model/history.json').read_text());D=H['history'];S=json.loads((P/'source_ledger.json').read_text());B=O['cases']['base'];fmt=lambda n:f'{n:,.2f}'
s='''# SNPS: mejora real, precio todavía exigente

**5 noviembre 2026 | Fundamental Pullback | S3-SNPS-20261105-v2 | Investigación auditada con salvedades**

**Decisión: EN OBSERVACIÓN. No pasar a Stage 3.5 ni ejecutar.** El Investor Day de septiembre cambia materialmente las expectativas frente a A104, pero no demuestra una compensación suficiente por el riesgo a $462,95. No se rechaza por superar un único valor central: el caso de cumplir el plan de dirección llega a unos $423 y, con un WACC 50 puntos básicos menor, a $466. Ese último caso explica el precio, pero apenas ofrece holgura de valoración frente a un estrés moderado que reduce su valor a $312. La brecha de valor de ese caso (~0,7%) no es una estimación de rentabilidad anual: a precio justo, podría ofrecer aproximadamente su rentabilidad exigida. La observación responde a la combinación necesaria de ejecución y menor descuento, y a su fragilidad bajo estrés. El escenario favorable no constituye una aprobación.

Abrir primero [el modelo editable](output/SNPS_DCF.xlsx). Estado **screen-grade** para aprobación: las cuentas, fórmulas y fuentes están trazadas; persiste el límite de comparabilidad económica proforma. La auditoría independiente concluye que es apto con salvedades para investigación condicional y observación. La decisión de no comprar hoy no necesita inventar una certeza de valor intrínseco. Este informe no modifica posiciones ni registra órdenes. Opportunity100≥85 permanece sin cambios; la verificación técnica se hace por separado.

## 1. Corte y novedad decisiva

Precio de referencia, confirmado por dos proveedores: **$462,95**, cierre regular del 4 noviembre, 16:00 EST, observado en la página histórica y estadística de StockAnalysis. No se usa el $465 del scanner ni el $460 fuera de horario. Se conserva evidencia fechada; cierre confirmado también por la serie Yahoo y reconstrucción independiente de la revisión técnica. Las cuentas publicadas más recientes son Q3FY26, 31 julio. FY26 terminó el 31 octubre, pero sus resultados todavía no se habían publicado al corte.

La guía del 30 septiembre para FY27 es ingresos $11.100–11.200 millones, margen operativo no-GAAP ~44%, EPS ajustado $19,04–19,12, FCF ~$3.100 millones y capex ~$500 millones. SBC esperada $960–980 millones. Los objetivos FY26–30 son crecimiento agregado ~15%, margen no-GAAP ~50% al final y crecimiento de FCF en la veintena media. Son objetivos de dirección, no resultados asegurados. El modelo incorpora esta información, ausente del cálculo condicional A104. [Investor Day](https://news.synopsys.com/2026-09-30-Synopsys-Details-Growth-Strategy-and-Long-term-Financial-Model-at-2026-Investor-Day).

## 2. Historia: no confundir adquisición y crecimiento orgánico

USD millones; ingresos y beneficio de operaciones continuadas. CFO/FCF FY23–24 son del grupo y aún incluyen Software Integrity. No se usan como serie homogénea de crecimiento de caja.

|Periodo|Ventas|EBIT GAAP|BN continuado|CFO grupo|Capex|FCF grupo|SBC continuada|EPS económico proxy|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for k in ['FY2023','FY2024','FY2025','TTM2025','TTM2026']:
 r=D[k];s+='|'+k+'|'+'|'.join(fmt(r[x]) for x in ['revenue','ebit','net_income_cont','cfo_total','capex','fcf_total','sbc_cont','normalized_eps'])+'|\n'
s+='''
TTM26=FY25+9M26−9M25; TTM25=FY24+9M25−9M24. FY24 tuvo 53 semanas. La inversión FY23 de191,822 suma compras de PPE netas189,618 y software capitalizado2,204; no es una diferencia entre capex bruto y neto. Las ventas de edificios FY24/25 de16,339/74,279 son líneas de caja separadas y no se descuentan nuevamente de las compras de PPE. Software Integrity se vendió en septiembre2024 y está excluida de ingresos/EPS comparativos. Ansys se incorporó el17julio2025; usar el salto de ingresos reportados como orgánico sería incorrecto.

**Corrección de calidad:** los filings dan EBIT TTM26 de802,356, no los ~$1.040 millones de la página secundaria. A104 usaba SBC total FY23/24 (563,292/692,316); la continuada es513,094/657,935. Las cifras primarias controlan. [10-K](https://www.sec.gov/Archives/edgar/data/883241/000088324125000028/snps-20251031.htm), [10-Q actual](https://www.sec.gov/Archives/edgar/data/883241/000088324126000025/snps-20260731.htm).

|Trimestre|Ventas|EBIT GAAP|BN continuado|CFO|Capex|FCF|EPS económico proxy|
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for k in ['Q42025','Q12026','Q22026','Q32026']:
 r=D[k];s+='|'+k+'|'+'|'.join(fmt(r[x]) for x in ['revenue','ebit','net_income_cont','cfo_total','capex','fcf_total','normalized_eps'])+'|\n'
s+='''
El archivo History incluye también cada trimestre comparable del año anterior. Los flujos trimestrales se obtienen por diferencias de acumulados, no anualizando Q3. Fuentes: S1–S5.

### Comparación de perímetro y límite del crecimiento de beneficio

Las notas de adquisición ofrecen ingresos combinados proforma: FY24 $8.450,296; FY25 $8.920,890; 9M24 $6.385,630; 9M25 $6.666,029. Así, el TTM comparable anterior asciende a $8.730,695 frente a $9.416,465 actuales: **+7,86%**, mucho menos que el salto reportado. Q1/Q2/Q3FY26 frente al proforma previo crecen aproximadamente8,6%/5,5%/8,1%. Este cálculo aún no ajusta totalmente desinversiones ni los $60 millones del cambio de reconocimiento del canal Ansys comunicado en Q2. Restar esos60 del TTM actual reduce el crecimiento a7,17%; retirar negocios vendidos del denominador aumentaría el porcentaje. Es una banda de contexto, no una medida oficial orgánica.

El EPS económico proxy se calcula de forma uniforme: EBIT + amortización adquirida + reestructuración + costes operativos de adquisición/desinversión −1% de ventas como coste económico de renovación; menos intereses publicados y tasa normalizada20%. Conserva SBC y compensación diferida. Excluye ganancias de desinversión y otros ingresos no operativos. El 1% es una estimación explícita, no una medida publicada de amortización económica. La I+D permanece como gasto. El aumento TTM del proxy refleja Ansys, financiación y dilución; **no certifica crecimiento homogéneo de EPS proforma**. No se usa el aumento como pase automático de la regla≥5%, ni se declara crecimiento negativo a partir de GAAP distorsionado.

La historia sí muestra recuperación operativa: IP Q3 vuelve a crecer, pero 9M ventas IP aún retroceden ligeramente y su margen ajustado cae frente al año anterior. La prueba prospectiva es que esa recuperación sostenga caja después de SBC y la inversión. Para aprobar deberá cerrarse la comparación económica combinada o una evidencia posterior suficientemente comparable; no se exige para concluir que hoy no hay compensación robusta por precio.

## 3. Caja, amortización y reinversión

FCF TTM publicado2.747,706 menos SBC950,016 deja1.797,690 antes de desapalancar el flujo. No es FCFF. La conversión debe añadir intereses después de impuestos y normalizar circulante, impuestos e inversión. La aportación NVIDIA de2.000 millones es financiación, no caja operativa; ya está en el balance julio y no se añade otra vez.

**Puente FY27:** guíaFCF3.100 −SBC970 +interés bruto supuesto500×(1−20%) ≈2.530 de FCFF económico. El interés bruto es una estimación coherente con el principal y los cupones, no confundirlo con la guía de interés y otros netos−460. El modelo por EBIT produce2.543,883: NOPAT3.150,567 +DA223,128 −capex502,038 −circulante216,210 −reinversión intangible111,564. La diferencia de14 es pequeña, no se introduce un ajuste de caja para forzar igualdad. La guíaFY26 tiene redondeos: CFO~2.800 menos capex~225 no suma exactamente FCF~2.600.

No se añade automáticamente una deducción fiscal del20% de toda la amortización PPA. El precio pagado asignó12.990 millones a intangibles y reconoció pasivos fiscales diferidos materiales; amortización contable no equivale a deducibilidad fiscal. El modelo usa impuestos20%, con18% en favorable, y ningún activo fiscal PPA adicional. La guía de amortización FY27~1.545 millones se separa del desgaste ordinario. El margen económico excluye la amortización adquirida, pero **mantiene I+D, SBC, compensación y costes operativos de sostener productos**. Capex3,5–4,5% de ventas, DA2%, circulante incremental y1% de inversión estratégica pagan renovación y crecimiento. Eliminar ese1% eleva la valoración solo~$4: no explica la conclusión.

## 4. Balance y acciones: recompra pagada

|Puente de capital|USD millones|
|---|---:|
|Caja e inversiones líquidas julio|3.607,669|
|FCF Q4 implícito en guíaFY26|457,486|
|ASR octubre, desembolso contado una vez|−1.000,000|
|Reserva de caja operativa estimada|−500,000|
|Caja excedentaria proyectada al cierreFY26|2.565,155|
|Principal y compromiso treasury-lock|−10.110,449|
|Ajuste EV→equity|−7.545,294|

No se presenta este rollforward como balance publicado de noviembre. No se añade también FCFF Q4 al DCF: sus flujos empiezan enFY27. Variar la caja proyectada±500 millones cambia el valor±$2,61. La caja extranjera~1.700 millones no está toda certificada como inmediatamente repatriable; la reserva/sensibilidad acota el riesgo, sin inventar un impuesto concreto.

Acciones julio191,605 millones; guía plenamente diluida FY26 midpoint193. Denominador:193−1,735 de entrega inicial ASR =**191,265**. Es estimación diluida, no conteo actual certificado, coherente con guíaFY27 190–192. Esa guía se publicó junto con la intención de recomprar1.000 millones; no se presume que excluyera esa recompra y no se le resta el ASR de nuevo. No se descuenta entrega adicional pendiente ni se incorporan recompras futuras gratuitas. La liquidación ASR está prevista como máximo5enero2027. Un millón de acciones extra reduce base~$1,86. [ASR oficial](https://news.synopsys.com/2026-10-05-Synopsys-Initiates-1-Billion-Accelerated-Share-Repurchase-Agreement).

Se usa principal10.110,449 en vez de valor contable10.037,360; incluye compromiso treasury-lock99,526 sin duplicarlo. Arrendamientos operativos~804,429 siguen en gasto, no se deducen nuevamente como deuda. Compensación diferida tiene activos y pasivos emparejados; no se añade su activo bruto. No se concede valor a participaciones estratégicas no líquidas. Vencen~1.025 millones en2027 y otro tanto2028, cubiertos en principio por caja y generación proyectada. Riesgo de integración real, no financiación actualmente demostrada como frágil.

## 5. WACC coherente, sin prima arbitraria

CAPM: Rf4,90% +beta1,18×ERP4,41% =Ke10,10%. Peso deuda10%, coste marginal supuesto5,60%, impuesto20%: **WACC9,54142%**. Rf es Treasury4nov; ERP Damodaran1nov usa una referenciaRf5,29% distinta: mezclar fechas introduce incertidumbre, expresamente sometida a sensibilidad. No se llama a ese dato una cotización simultánea perfecta. Beta publicada5años de SNPS1,18; pares CDNS1,10/ADSK1,25 contextualizan el riesgo. La beta retrospectiva tampoco mide perfectamente el nuevo perímetro Ansys.

La deuda equivale aproximadamente10% del capital de mercado. Cupones4,55–5,70% y rendimientos efectivos de emisión4,84–5,80% respaldan el orden de magnitud del5,60%, que **no** se presenta como yield observado hoy. No hay prima por tamaño ni empresa. Bear10,54%/bull8,79% son riesgos alternativos; no se cambia la tasa para aprobar. El9,5% de A104 era una rentabilidad exigida, no una estimación WACC.

## 6. Pronóstico 5+5 y terminal pagado

FY26 ingresos9715: simulación2980 según guía; IP1800 y EDA/otros4935 son reparto propio anclado en mezcla9M/Q3. No son tres segmentos contables publicados: EDA+simulación pertenecen a Design Automation. La desagregación permite probar motores distintos sin inventar previsiones oficiales de cada unidad.

|Motor|Año1|Año2|Año3|Año4|Año5|
|---|---:|---:|---:|---:|---:|
|EDA/otros, crecimiento base|16%|14%|13%|12%|11%|
|Simulación, crecimiento base|11%|11%|10,5%|10%|9%|
|IP, crecimiento base|18%|18%|17%|16%|14%|
|Margen EBIT económico base|35,3%|37,5%|39,5%|41,5%|42%|

Año1 total11.156,4 coincide aproximadamente con guía11.150. La ruta base no perpetúa un salto adquirido: ya parte del perímetro combinado, y no añade compras futuras sin coste. IngresosFY31~17.910 yFY36~24.224. Margen41,5%FY30 supone una cargaSBC y otros costes que separa la guía no-GAAP50% del beneficio económico. La mejora exige eficiencia real y éxito de productos, no solo eliminación de SBC.

Años6–10: cada motor desacelera linealmente a3%; margen42%; inversión neta converge a NOPAT×g/ROIC. Terminal g3%, ROICincremental25%: reinvertir12% del NOPAT, no crecimiento gratis. ROICincremental no es ROIC histórico sobre los35.000 millones pagados por Ansys. El soporte es la economía de software y los gastos de I+D ya incorporados; el25% sigue siendo hipótesis, probada entre20–30%. Valor terminal~59,8% delEV exige prudencia. Descuento fin de año con FY27 como primer flujo; no convención de mitad de año oculta.

## 7. Escenarios, precio razonable y estrés

|Caso|Valor/acción|Cambio vs462,95|WACC|g / ROIC|Peso terminal|
|---|---:|---:|---:|---:|---:|
'''
for k in ['bear','base','bull']:
 r=O['cases'][k];p=A['cases'][k];s+=f"|{k}|{r['value']:.2f}|{r['upside']:.1%}|{r['wacc']:.2%}|{p['g']:.1%} / {p['roic']:.0%}|{r['terminal_weight']:.1%}|\n"
s+='''
Bear: crecimiento por motor~7–11% inicial, margen32→35%, impuesto22%, ejecución lenta y mayor descuento. Bull: crecimientoEDA18%, simulación14%, IP23% iniciales; margen36,5→45%, impuesto18%, ROIC30% y menorWACC. No son probabilidades ni precios garantizados.

**Prueba más justa que precio>base:** la guía de dirección cubre el CAGR FY26–FY30, cuatro años. Este contraste prolonga por hipótesis propia el15% también hastaFY31, un año adicional, antes de desacelerar: no es una réplica pura de la guía. Mantener15% de crecimiento agregado durante cinco años y margen35,3→43% produce$423,23. RebajarWACC50pb produce$465,99: sí existe una combinación defendible que explica el precio. Sin embargo, ~0,7% de ventaja frente al precio no compensa que crecimiento13%, margen2puntos menor, WACC+50pb y g2,5% reduzcan ese caso a$311,52. No se exige un descuento fijo; se rechaza la escasa compensación frente a desviaciones moderadas. El estrés equivalente sobre el modelo segmentado base arroja$261,79. La asimetría favorable+31% frente a adverso−65% tampoco justifica forzar una compra con el bull.

Otros límites: tasa fiscal18% base da$367,38; ROIC20/30% da$347,32/$363,53; eliminar reserva de caja da$359,66. Ninguna de esas pequeñas incertidumbres basta para explicar el precio. La sensibilidad WACC/g completa está en el workbook y JSON. La principal incertidumbre es duración del crecimiento/margen, no unos millones en el puente de caja.

## 8. Valoración inversa y múltiplos

Con márgenes/reinversión/WACC base, el precio exige crecimiento agregado constante **16,97% durante cinco años**, seguido de desaceleración a3%: ingresosFY31~21.268 millones frente a17.910 en base. Manteniendo la ruta de ventas, exige añadir **10,60 puntos** a todos los márgenes económicos, llevando el maduro a~52,6%, después de SBC. Son alternativas del mismo modelo, no dos pruebas independientes. El caso dirección+menorWACC muestra otra combinación posible; no existe una expectativa única.

Al precio observado, PERFY27 sobre guía ajustada19,08≈24,3; no confundirlo con beneficio económico. El PER sobre EPSGAAPTTM publicado aproximado5,64 ronda82. El EPS proxy económicoTTM8,52 implica~54,3, pero su perímetro cambia. Para comparables homogéneos se presentan métricasGAAPTTM secundarias al mismo corte, sin convertirlas en valoración principal: CDNS PER65,52/EVventas14,95/EVEBIT49,94; ADSK35,00/7,16/25,50. CDNS es el par más cercano; ADSK difiere en mercados y mix. Los múltiplos actuales de SNPS se recalculan con filings, porque el EBIT de agregador es inconsistente. Con EVeconómico~96.090 millones y ventasTTM9.416,465, EVventas~10,2; EV/EBITGAAP~119,8; EV/EBITnormalizado~36,1. Las definiciones no se mezclan ni se promedian.

No se ha reconstruido una serie histórica de múltiplos de mercado con precios y contabilidad homogéneos. El salto de perímetro y márgenes impide afirmar «barata frente a su media». Esta limitación reduce la confianza para aprobar, pero no se convierte en una barrera artificial a terminar el análisis económico.

## 9. Riesgos, catalizadores y siguiente prueba

Ansys amplía simulación y venta cruzada; acuerdosAI/IP de septiembre respaldan oportunidades, no ingresos ya ganados. Backlog julio~10.900 millones incluye1.900 de compromisosFSA no asignados; de lo restante se espera reconocer49% en doce meses. No equivale a ventas libres de riesgo ni cubre toda la previsión.

Causas verificadas de presión histórica: restricciones de exportación y debilidadIP documentadas en filings, problemas de demanda de un cliente de fundición y ejecución de roadmap. No se asigna una causa única al retroceso diario de octubre sin evidencia. La subida de octubre tras Investor Day muestra que la expectativa nueva ya es conocida. Riesgos principales: monetización deAI, ritmo deIP, integraciónAnsys, restriccionesChina, presión competitiva y conversión de margen a caja. Lo primero que rompe el caso es crecimientoIP o márgenes que no se conviertan enFCF después deSBC y capex.

La páginaIR no muestra una fecha oficial futura confirmada al corte. **9diciembre2026 es estimación externa**, no fecha oficial; 10diciembre2025 pertenece al ejercicio anterior. Revalidar anuncio oficial antes de cualquier ficha operativa. ASR: liquidación esperada no después5enero2027.

Reabrir cuando el precio deje margen frente a un caso razonable resistente, o la evidencia eleve de forma sustentable ventas/margen/caja. No hay techo de compra ni señal técnica activada. Próximas pruebas: FY26 y nueva guíaFY27, conversiónFCF frente a2.600/3.100, SBC, inversión~500, recuperaciónIP y acciones/deuda despuésASR. No se aprueba una posición pequeña para sortear incertidumbre fundamental.

## 9b. Comprobación técnica separada

La revisión independiente conserva Yahoo histórico y barra final StockAnalysis, y su EMA fue reconstruida en este paquete: cierre462,95; EMA20 462,5895; EMA50 448,9774; EMA200 447,4292; EMA200 sube1,038% en20sesiones; ATR14 18,8451; RSI14 51,4755; volumen medio20~2,227millones; retroceso desde máximo252~14,186%. Los filtros técnicos básicos pasan. El máximo29oct491,39 sigue por debajo del9oct512,49 y el mínimo3nov445,56 aún no tiene dos sesiones posteriores para confirmarse como pivote. No hay señal, stop ni tamaño aprobados. Una estructura favorable no invalida la valoración. Los volúmenes finales difieren ligeramente por proveedor y no se usa una señal de volumen.

## 10. Migración desde A104 y reproducibilidad

A104 base227,25/bull378,34 eran condicionales, no valoraciones actuales vinculantes. La reproducción de inputs publicados arroja227,34, diferencia0,09 atribuible a detalle no preservado/redondeo, no se afirma réplica exacta. Puente secuencial con el mismo marco:

|Paso|Valor|
|---|---:|
'''
for label,v in X['migration']:s+=f'|{label}|{v:.2f}|\n'
s+='''
El aumento viene de nueva guía/mezcla/márgenes, no de rebajar la tasa para alcanzar el precio. Los cambios de reinversión, capital y denominador están separados. Las dos versiones se conservan; esta revisión auditada sustituye la valoración económica condicional, sin convertirla en aprobación.

Paquete: assumptions/history/results/analysis JSON, CSV por escenario, fuentes primarias descargadas, evidencia web fechada, ledger y modelo editable. Ejecutar `python reproduce.py` desde esta carpeta regenera cálculo, workbook, informe y controles sin red. Las fuentes históricas permanecen congeladas. El modelo editable de10 años contiene702 fórmulas con resultados comprobados; se recalculó con un segundo motor de hojas de cálculo y se inspeccionó visualmente como QA propia, no como auditoría independiente. Las sensibilidades estáticas deben regenerarse con el script después de cambios; los tres casos principales son fórmulas editables.

**Auditoría independiente completada:** [acta y salvedades](audit/report.md). Reconstrucción separada con992 controles DCF,134 de fuentes primarias,10 sensibilidades adicionales y453 celdas del libro verificadas tanto en caché como tras recálculo nativo. Las pruebas activas de tasa y crecimiento también coinciden. No quedan errores materiales identificados; esto no convierte supuestos en hechos ni concede aprobación de compra.

**Pendientes expresos:** comparación homogénea de beneficio/FCF combinado y calendario oficial. No están ocultos ni transformados en datos inventados. No hay publicación externa ni operación realizada.

## Fuentes
'''
for x in S:s+=f"- {x['id']}: [{x['name']}]({x['url']}) · {x['date']}. {x['scope']}\n"
(P/'report.md').write_text(spaced(s))
