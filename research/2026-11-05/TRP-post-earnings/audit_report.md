Aviso de entrega pública: este informe conserva el resultado de la revisión de V2.1. Los 30 hashes citados corresponden al conjunto original revisado; los hashes de esta copia editorial pública figuran en PUBLIC_MANIFEST.json. Los PDFs de fuentes externas no están incluidos.

# Dictamen final: TRP V2.1

**APTO CON SALVEDADES para publicar como «En observación; sin entrada». NO APTO como valoración validada ni puente financiero actual de noviembre.**

539 controles independientes sin fallos materiales. Escenarios reproducidos: US$7,786814 / 30,159182 / 77,890443. Se han incorporado una sola vez dividendos por pagar933 e intereses devengados904; la base caeUS$1,262772 frente aV1. No hay cambio de método.

La caja reportada continúa siendoC$8.596m de CFO continuo yC$1.767m residual común. La exclusiónCGL199 se presenta ahora como ajuste parcial/ilustrativo, no normalización completa, y se examina simétricamente el posible ajuste78. El déficit de evidencia sobre lease,JV,NCI, roll-forward y comparables homogéneos permanece visible y bloquea la entrada.

Paquete aprobado para esa finalidad limitada: paquete analítico TRP-POST-Q326-v2.1 (referencia relativa: .). Los30 hashes del manifiesto coinciden. Certificado y hashes de documentos/modelo en audit_certificate_v2_1.json. No se publicó ni operó nada.

## Clasificación de los cambios

- Corrección del puente: derechos omitidos933+904. No era un error de suma o fórmula; era omisión de claims económicos bajo el diseño deFCFF.
- Normalización:199 y posible78. No se alteran datos reportados; son análisis de recurrencia con una sublínea de caja aún no identificada individualmente.
- Incertidumbre persistente: lease/JV/NCI y movimientos posteriores a30Sep, no resuelta mediante un descuento inventado.
- Requisito canónico aclarado: tres ejercicios, últimos cuatro trimestres yTTM contraTTM previo; ocho trimestres documentados facilitan el cálculo, no son una regla adicional. Contraste homogéneo frente a pares e historia sigue pendiente.

El texto del paquete conserva el aviso «pendiente de auditoría» por ser una congelación previa. El publicador puede actualizar exclusivamente ese aviso y el estado de auditoría para reflejar este alcance limitado, sin cambiar cifras o supuestos. No usar «valoración aprobada».


---

## Informe de revisión V1 y trazabilidad de hallazgos

# Auditoría independiente de TRP tras Q3 2026

Fecha: 5 de noviembre de 2026. Paquete inicial revisado: TRP-POST-Q326-v1. Este documento es un informe de revisión, no una valoración alternativa ni una autorización de operar. No se publicó nada ni se modificó el paquete del autor.

## Dictamen inicial

**Aritmética: APTO. Valoración para decidir: NO APTO. Publicación: CONDICIONADA a corregir el puente financiero y precisar la normalización de caja.** La conclusión «En observación; sin entrada» está justificada por la información esencial pendiente y es coherente con el plan. Esa conclusión no exime de corregir errores o de describir con exactitud qué se ha auditado.

Se reprodujeron por una implementación independiente los tres escenarios, los treinta años-escenario proyectados, las veinte sensibilidades WACC/g y las tres soluciones inversas. Se contrastaron historia anual, ocho trimestres, TTM y caja con fuentes primarias. Resultado: 529 comprobaciones, sin divergencias materiales; diferencia máxima absoluta 2,91×10^-11, atribuible a coma flotante. No se ejecutó ni importó model.py del autor.

Los valores V1 reproducidos son US$9,049586 / 31,421954 / 79,153215. Son resultados correctos de los supuestos y del puente V1, **no valores económicos aprobados**. El modelo utiliza proxies materiales para participadas, arrendamiento financiero y minoritarios. La revisión demuestra reproducibilidad, no que los supuestos representen adecuadamente el negocio.

## 1. Correcciones de puente financiero

### A02. Balance de septiembre, pagos y fecha de valoración

P1, PDF62, informa a 30Sep2026 caja1.249, deuda2.780+3.197+44.418+12.639=63.034, preferentes2.255, NCI9.773, dividendos por pagar933 e intereses devengados904, todo en C$m. V1 resta exactamente64.959 de derechos netos, pero no incluye los933 ni los904.

No es una suma equivocada: **la suma programada es correcta, pero el conjunto de derechos financieros es incompleto bajo el diseño empleado**. El FCFF del modelo parte de EBIT y no paga intereses; el ΔWC futuro equivale a1% del crecimiento de ventas y no contiene las cuentas financieras. Por ello no hay evidencia de que esos904 ya estén descontados en los flujos. Debe adoptarse explícitamente una convención de deuda/precio limpio/interés devengado que los recoja una sola vez.

P4, PDF6, establece que el dividendo común C$0,8775 era pagadero el30Oct2026 a titulares al29Sep2026. Conservar su caja dentro del balance de septiembre como si correspondiera al comprador de la acción exdiv de5Nov sobrevalora el puente. Deducir el derecho al30Sep y deducir otra vez el pago al actualizar caja sería, en cambio, doble descuento. La solución es un puente coherente, no dos recortes.

Sensibilidades ilustrativas, no nueva valoración:933 equivalen aUS$0,64135/acción;904 aUS$0,62142. Incorporar ambos una vez reduce mecánicamente la base V1 de31,42195 a30,15918. El autor debe recalcular todos los escenarios y el texto, no solo cambiar la cifra central.

P1, PDF76, documenta además un nuevo préstamo deUS$200m y amortización deUS$89m el29Oct. Estos movimientos tienen contrapartida en caja: no se debe deducir el nuevo endeudamiento bruto de septiembre sin reflejar su financiación recibida. La participación indígena de octubre también requiere conocer contraprestación y cesión de derechos.

V1 descuenta flujos2027–2036 a5Nov con56/365 años adicionales. Ese factor temporal está bien; el problema es que **el tramo1Oct–5Nov no está reconciliado con el balance30Sep**, mientras el stub declarado cubre5Nov–31Dic. La versión siguiente debe reconocer el hueco o documentar un puente/hipótesis de caja para todo el tramo. No basta afirmar que se «lleva» el balance de septiembre a noviembre.

### Otros derechos revisados

- El100% de las subordinadas debe deducirse de comunes; el50% de crédito de equity de ratings no justifica omitir deuda.
- Factoring84 es financiación, no un aumento recurrente del CFO; P1 PDF74 y61 lo apoyan.
- Préstamo de afiliada218=111+107 es una aproximación sujeta a FX, no saldo exacto auditado. Sur de Texas es acreedor y participada al60%; su derecho acreedor y las distribuciones futuras requieren una reconciliación consistente, no una eliminación automática del100% del préstamo.
- OPEB no financiado76 está soportado por P2 PDF196. No sumar el superávit de pensiones como efectivo libre. Debe mantenerse consistencia entre servicio corriente y déficit previo.
- Caja excedentaria749 resulta de1.249−reserva asumida500;500 es una hipótesis, no una cifra de caja restringida publicada.
- Guadalajara: conservar economía operativa sin añadir los ingresos de una venta no cerrada evita el doble conteo inmediato. Una valoración final deberá pasar a la economía/producido neto de venta con fecha coherente.

## 2. Caja continuada, normalización y comparaciones

### Lo comprobado y correcto

P1 PDF61/66: CFO Q3 total1.782 menos CFO discontinuado−122=1.904. El comparable2025 es1.920−12=1.908. Por tanto la caída del CFO total de138 no representa un deterioro equivalente del negocio continuo:134 procede del cambio en el flujo discontinuado y4 del continuo.

TTM actual: CFO total8.496 menos discontinuado−100=8.596. Reinversión pagada5.485 deja3.111; distribuciones a NCI «y otros»1.231 y preferentes113 dejan1.767. Dividendos comunes3.597. Coberturas reportadas49,12% y86,49% antes de NCI/preferentes. Estos cálculos concuerdan; no son un FCFE oficial ni una medida de caja recurrente ya normalizada.

El TTM previo continuo7.631 se calcula con la misma definición. La mejora12,65% es real en la medida reportada reconstruida. La reinversión2024 elimina solo el circuito CGL3.137 de contribución/repago, dejando sin netear los10 de repago adicional. Esto concuerda con P2 PDF156/168/170. Los capitales de operaciones discontinuadas127 y49 se excluyen correctamente de2024 y2023.

### A03. Cobro extraordinario CGL199 y normalización simétrica

P2 PDF45 y168 documenta un cobro único CGL de199 en octubre2025 por trabajo completado/cierre de costes, reconocido previamente como distribución en sustancia en2024. Pertenece a la ventana TTM que termina en septiembre2026 y **no constituye crecimiento de beneficios2025**. V1 no lo identifica en su discusión de caja.

La nota confirma cobro y fecha, pero no asigna expresamente los199 a la línea de distribuciones operativas de JV. La inferencia de que afecta CFO se apoya en la cuenta por cobrar previamente registrada y en los estados de inversión; debe verificarse o señalarse como inferencia. No es válido afirmar sin más que199 de los2.120 de distribuciones operativas TTM son esa partida. Puede haber pasado por cambios en cuentas por cobrar. La normalización debe evitar quitarlo dos veces.

Sensibilidad parcial si199 están en CFO:8.596−199=8.397; residual1.767−199=1.568; cobertura43,59%. **No llamar a esta cifra CFO o FCF plenamente normalizado.** P1 PDF47 también contiene un pago de liquidación con terceros de78 neto de impuesto; aceptarlo como no recurrente elevaría ese residual parcial a1.646, cobertura45,76%. Hace falta justificar ambas exclusiones, junto con el circulante y otras partidas.

Los347 de distribuciones CGL financiadas con deuda enQ32026 están correctamente excluidos de caja operativa recurrente, porque se presentan en inversión. No compensan automáticamente el déficit después de dividendos.

La base propia de distribuciones JV1.900 es próxima a2.120−199=1.921, pero esa proximidad **no prueba** que el modelo haya normalizado correctamente la partida: falta asignación por entidad y línea. Registrar la justificación, no inferir intenciones del autor.

## 3. Perímetro lease, JV y NCI

### A01/A04. Diseño sensato, cifras todavía no aptas para decidir

Separar núcleo FCFF, equity de JV alKe y lease financiero finito es conceptualmente válido. El EBITDA comparable incluye equity income, no EBITDA proporcional completo de todas las JV; excluir ese ingreso del núcleo evita mezclar niveles. El modelo no suma simultáneamente book equity deJV ni deduce otra vez su deuda.

El lease9.366 es el saldo neto total a31Dic2025, no un DCF nuevo. P2 PDF167 concilia pagos mínimos29.764−ingreso no devengado20.397−ECL141+residual140=9.366; corriente1.256 y largo8.110. P1 PDF62 solo permite verificar largo8.391 a30Sep. No se debe inferir que el total actual es8.391, ni conservar sin explicación el corriente1.256. P1 PDF74 documenta una nueva modificación del contrato y reasignación lease/no-lease en agosto2026. La sensibilidad±15% es una hipótesis, no sustituto del calendario actualizado, impuestos, residual y riesgo de cobro.

Core y lease deben conservar O&M, impuestos y derechos de TGNH en la misma base económica. Eliminar ingreso de lease del EBIT y añadir un activo financiero bruto no prueba por sí solo que todos los impuestos y derechos sobre sus flujos estén tratados. No se prescribe deducir toda la DTL consolidada: se exige un puente de los impuestos pertinentes y evitar doble conteo con los impuestos del FCFF.

NCI9.773 es book value. La modificación de±30% muestra sensibilidad, no una valoración proporcional de Columbia, TGNH o tax equity. P1 PDF39 confirma Columbia40%, TGNH13,01% y derechos ClassA de tax equity, que no equivalen al100% de todo el parque eólico.

La operación indígena de octubre recae sobre derechos económicos en la entidad que posee la participación35% de CGL, no necesariamente sobre una nueva consolidación directa del gasoducto. Se puede capturar mediante un derecho sobre laJV o un NCI del holding, **una vez**. No se confirmó doble conteo en V1; faltan términos económicos para cerrar el puente. P1 PDF45 añade que la participación CFE puede subir al15% y a≈35% en2055. Este cambio afecta también a cualquier extrapolación perpetua más allá del contrato.

Las contribuciones JV se pagan en el modelo y la política terminalg/ROE limita distribuciones; buena disciplina algebraica. Falta la reconciliación por Bruce, CGL, Sur de Texas y otras: earnings, distribuciones operativas, retornos de capital, deuda del proyecto, aportaciones y disponibilidad para TRP. La deuda por debajo de laJV no puede eliminarse del razonamiento solo porque no se deduzca otra vez en el puente.

## 4. Controles numéricos y supuestos

Escenarios V1, C$m: coreEV65.539,293/90.278,873/148.784,267; equityJV12.930,417/20.797,780/32.278,480; equity común13.164,760/45.710,654/115.147,047. Dividir por1.042m acciones y1,3961CAD/USD reproduce los precios citados.

Base: peso terminal73,1302% del coreEV y65,6648% de core+JV+lease. TerminalFCFF5.446,318=Nopat terminal×(1−g/ROIC). WACC>g yKe>g en todos los escenarios. Las transiciones, capex, NWC y cashJV reproducen las cifras publicadas. La diferencia del ancla EBIT propio6.410 frente a15.070×42,5%=6.404,75 es redondeo/hipótesis, no un fallo material.

Inversas V1 reproducidas: WACC5,360628%; crecimiento inicial21,407473%; margen61,907084%. Son raíces del mismo modelo, no evidencia independiente ni expectativas de mercado inequívocas. Las raíces cambiarán tras corregir el puente.

WACC6,75%=60%×8,5%+40%×5,5%×(1−25%) está bien calculado. Pesos, equity risk, impuesto y reinversión/retornos requieren evidencia. El crecimiento core, margen yJV cash no se validan porque concuerden aproximadamente con un año de guidance.

Las sensibilidades V1 de NCI±30% (±US$2,015), lease±15% (±0,966), deuda fairvalue (+1,226) ystub±250 (±0,172) reproducen. Llevar NCI a cero dejaría la base≈38,14; no valida la base ni demuestra que solo los minoritarios expliquen la brecha. La gran distancia al precio también exige revisar flujos, crecimiento, reinversión y coste de capital.

## 5. Cumplimiento del plan canónico, sin inventar reglas

El PDF vigente es la edición30Oct2026/v2. Stage3 apartado3 exige **tres ejercicios completos, últimos cuatro trimestres, TTM frente alTTM anterior y próximos doce meses**. No establece literalmente «ocho trimestres independientes obligatorios», aunque ocho observaciones consecutivas son una forma apropiada de construir ambosTTM. El paquete supera el mínimo de historia visible y hace correctamente las restas FY−9M paraQ4.

- Hechos y series: cumplen sustancialmente períodos, moneda, beneficio/ventas/márgenes/caja y distinción continuado/discontinuado. EBIT segmentado incluyeJV y está rotulado, no se presenta como EBIT puro delDCF.
- Normalización: reconciliación de EPSQ3 correcta; la caja requiere la precisiónA03. No retirar SBC sistemáticamente ni perpetuar costes «no recurrentes» por hábito.
- FCFF:10años,5+5, terminalg/ROIC, escenarios y sensibilidad presentes. La descomposición se documentó antes del cálculo, y no sustituye el método por un múltiplo favorable.
- Comparables: P/E TTM23,3457x y dividend yield3,9052% bien calculados con el FX supuesto. Los múltiplos del proveedor no se han reconstruido en un perímetro homogéneo ni contrastado con historia. El apartado9 pide ambos. Cumplimiento incompleto, no un requisito inventado.
- Precio: no hay rango justo validado ni máximo autorizado; esto es correcto mientras falta información esencial. El plan manda observación, no inventar un15% adicional ni reducir tamaño para compensar datos ausentes.
- La puntuación técnica no apruebaStage3. El plan no obliga a asignar probabilidad a escenarios ni a un descuento universal, y no exige una llamada/transcripción como condición universal. En este caso la llamada es una fuente pertinente para resolver dudas, no una nueva regla canónica.
- Stage3.5 no está aprobado; faltan condiciones patrimoniales y de señal/stop. No procede operar ni utilizar estos valores para una salida fundamental automática.

## 6. Fuentes y trazabilidad

Los ocho archivos con hash en sources.json coinciden con los hashes calculados: siete PDFs yprice_history.json. Esto demuestra integridad respecto del manifiesto, no una segunda verificación remota del documento original.

P1 PDF56 verifica las ocho observaciones de ingresos, beneficio común continuo y EPS. P2 PDF19/20/137/154/155–157 verifica los tres ejercicios, CFO y reinversión. P1 PDF61/66, P3 PDF60/67, P4 PDF57/62, P5 PDF53/58, P6 PDF58 yP7 PDF53 soportan el puente trimestral de caja. El informe y las cifras se contrastaron con esos textos.

Elraw chart retenido identifica TRP, NYSE, acciónUSD y64,10 a15:55:27UTC del5Nov. La referencia64,38 a15:34:29 figura en el manifiesto, pero su respuesta nativa no está retenida en este paquete. Se puede conservar como referencia analítica del autor, no como quote independientemente verificado por este audit. FX/yields/pares cuentan con enlaces y fechas, no con snapshots nativos auditables. No se sustituye el precio silenciosamente.

La reconstrucción técnica desde las velas completadas reproduce cierre62,6100, high25271,4700, retroceso12,3968%, volumen medio2.245.685, EMA20/50/20062,309118/62,158466/62,005991. La pendienteEMA20020sesiones es apenas positiva. No se reconstruyóQP100: faltan ventanas exactas de estructura y son scores históricos importados delscanner4Nov. Elpayload deberá conservar ese contexto.

## 7. Disposición y cierre pendiente

1. Autor: corregir el puenteA02, explicar el tramo temporal, actualizar escenarios/inversas/textos y conservarV1.
2. Autor: añadir normalizaciónA03 separada de los datos reportados, con evidencia y límites de clasificación.
3. Auditor: revisar la versión congeladaV2, verificar que no se descuentan derechos/pagos dos veces y recalcular independientemente.
4. Solo entonces emitir dictamen de publicación de la nota de observación. No autorizar entrada ni llamar «valoración aprobada» a escenarios provisionales.

Soporte incluido en esta entrega pública: independent_recalculation_v2_1.py/json, audit_original_recalculation_v2_1.json, audit_certificate_v2_1.json y PUBLIC_MANIFEST.json. Los registros históricos iniciales se conservan por separado. El autor fue notificado de los hallazgos; la reaudit deV2 sigue pendiente al redactar este informe.


## Cierre de reaudit V2.1

El estado pendiente al final del informe inicial queda sustituido por el dictamen final anterior. Se revisó el diff V1→V2→V2.1, se repitió la implementación independiente y se verificaron30 hashes. No se detectaron nuevos fallos numéricos ni doble descuento de derechos/pagos. Los bloqueos restantes son de decisión, no impedimentos para informar honestamente del estado de observación.
