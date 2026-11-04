# UL: auditoría independiente del candidato a valor razonable

**Corte económico: 4 de noviembre de 2026, 06:30 UTC. Comprobaciones técnicas terminadas antes de las 06:45 UTC.** Se revisan el informe Stage3, `full_model.json` y el anexo histórico del mismo día. Esta revisión no fue realizada por el autor del modelo. No modifica los archivos originales, no publica cambios por sí misma ni autoriza una orden.

## Dictamen

**La investigación puede considerarse completa con lo publicado; UL sigue siendo un candidato neutral bajo revisión, no una entrada parcial aprobada.** El método admite comprar a valor razonable si el retorno compensa el riesgo. Eso no convierte automáticamente un retorno estimado próximo al 8% en suficiente, ni obliga a exigir 15% de descuento. A 64,81 USD, el caso con la operación ya vale menos que la cotización, mientras el caso sin operación ofrece poco margen. La valoración depende de crecimiento nominal en euros, coste de capital y ejecución de dos transformaciones.

Reproduje con funciones independientes los valores originales: **67,2638 USD sin operación y 62,4886 USD con Foods/McCormick**. También los escenarios directo adverso 33,0463 y favorable 107,9647. No encontré un error grande de moneda ni doble contabilización evidente de Foods, del efectivo recibido o de Ice Cream. Hay dos clarificaciones cuantificadas que deben acompañar la conclusión:

1. La TIR central de la operación, 8,14%, usa un calendario distinto al DCF del paquete. Con el mismo tramo inicial de 0,67 años seguido de diez años completos, la aproximación de retorno es **7,83%**. No sustituye una previsión de distribuciones reales.
2. Una convergencia explícita de reinversión hacia el ROIC terminal durante los años 6–10 produce **66,52 USD sin operación y 61,67 USD con operación**. Con ambas precisiones, el retorno del paquete resulta aproximadamente **7,67%**. Son sensibilidades justificadas, no recortes arbitrarios de precio ni nuevos hechos de la empresa.

El rango original 62–67 USD describe correctamente valores centrales cercanos al mercado, no un margen de seguridad demostrado. La transición de reinversión amplía la lectura central aproximadamente a **61,7–67,3 USD**. No se propone promediar ambos perímetros como si fueran escenarios con probabilidades conocidas.

## 1. Propiedad, financiación y doble conteo

La lógica principal del puente es correcta:

- **Ice Cream:** el 80,15% distribuido en diciembre de 2025 no pertenece a un nuevo comprador de UL y no se añade. Solo se valora la participación retenida de 19,85%. El histórico se reconstruye sin el negocio discontinuado. La consolidación de ocho acciones nuevas por nueve antiguas ya está reflejada en los datos actuales; el ADR sigue representando una ordinaria.
- **Foods:** 55,1% para los accionistas y 9,9% retenido por UL suman el 65%. Se cuenta ese paquete una sola vez, después de restar deuda y minoritarios de la compañía combinada. Los aproximadamente 7,92 USD distribuidos y 1,42 USD retenidos del informe están dentro del total, no son un suplemento al valor de 62,49 USD.
- **Efectivo de 15.700 millones USD:** se añade a UL, pero la financiación equivalente se deduce en la compañía combinada antes de aplicar el 65%. La reserva de impuestos/separación de 4.000 millones EUR se resta una vez. El efectivo no es creación gratuita de riqueza.
- **Perímetros alternativos:** el DCF de UL actual y la SOTP después de la transacción son alternativas, nunca sumandos. La UL denominada HPC conserva determinados negocios Foods excluidos del acuerdo; no equivale literalmente a eliminar toda la categoría del segmento actual.
- **Dividendos y recompras:** la TIR reparte toda la caja atribuible bajo su hipótesis. No añade después el dividendo ordinario ni la recompra sobre la misma caja. La recompra ya finalizada está reflejada en las acciones actuales; el programa futuro no se suma como un activo independiente.

Estas estructuras están respaldadas por el [anuncio del acuerdo](https://www.unilever.com/news/press-and-media/press-releases/2026/unilever-announces-the-combination-of-unilever-foods-with-mccormick/), la [presentación](https://www.unilever.com/files/a-sharper-focused-hpc-pureplay-presentation.pdf), su [transcripción](https://www.unilever.com/files/a-sharper-focused-hpc-pureplay-transcript.pdf), el [histórico sin Ice Cream](https://www.unilever.com/files/unilever-half-year-historical-financials-excluding-ice-cream-pdf.pdf) y la [documentación ADS/consolidación](https://www.sec.gov/Archives/edgar/data/217410/000021741025000070/a2025-12x08xverdixsharec.htm).

**Dividendo concreto pendiente:** el comunicado Q3 fija **0,5219 USD por ADR**, no una conversión futura desconocida; exdividendo ADR 13/11, registro 13/11 y pago 18/12/2026. La tasa indicativa anualizada ronda 3,22% a 64,81 USD. No debe describirse como cobrado hoy ni añadirse otra vez al DCF sin ajustar el calendario de caja/balance. [Comunicado Q3, tabla de dividendo](https://www.unilever.com/files/unilever-q3-2026-results-full-announcement.pdf).

## 2. Divisas, claims y capital

Las operaciones de UL/HPC están en EUR y Foods/MKC en USD. Los flujos se descuentan en su moneda con tasas distintas; USD se convierte a EUR dividiendo por 1,1179 USD/EUR y el equity total vuelve a USD multiplicando por ese cambio. En los componentes que originalmente son USD, las conversiones se cancelan. No hay inversión incorrecta del tipo cruzado. Mantener ese tipo constante a diez años es una hipótesis de riesgo, no una previsión del ECB ni una cobertura contratada.

Los 25.961 millones EUR de deuda neta son del último balance completo, junio, no septiembre. Los 913 millones de déficits de pensiones no se compensan con todo el superávit contable. Los otros activos 1.169 millones se reconstruyen como 3.322 de activos financieros no corrientes menos 101 de derivados incluidos en deuda neta, 1.852 de valor contable MICC y 200 de depósitos judiciales. MICC se vuelve a incorporar a precio de mercado: no además de su coste contable. La participación en JV está fuera del EBIT y se valora separadamente. [H1 2026, notas de deuda, pensiones e instrumentos financieros](https://www.unilever.com/files/unilever-q2-2026-results-full-announcement.pdf).

Los minoritarios de 9.043 millones y JV de 3.877 millones son DCF analíticos, no precios observados. Suponen conversión a caja del beneficio y tasas explícitas; deben mantenerse como sensibilidades. Utilizar el valor bursátil completo de HUL encima del EBIT consolidado duplicaría activos. A la inversa, sustituir automáticamente el claim intrínseco por un minoritario a múltiplo bursátil alto mezclaría bases de valoración.

**Reserva específica:** H1 confirma la compra del 80% de Grüns por 767 millones EUR y reconoce una obligación de compra futura del minoritario. Si una parte de los beneficios minoritarios proyectados a perpetuidad corresponde exactamente a una participación cuya compra futura ya figura en deuda, esa parte debe terminar al adquirirla. El informe no demuestra ese puente granular. No se ha probado un error material ni existe en lo revisado un desglose suficiente para cuantificarlo; no procede inventar una deducción. Conviene sustituir la afirmación absoluta de ausencia de duplicación por esta precisión. El modelo es conservador si paga la compra y mantiene indefinidamente el mismo minoritario. [H1, nota 7](https://www.unilever.com/files/unilever-q2-2026-results-full-announcement.pdf).

Arrendamientos: incluir deuda de contratos existentes y renovación futura de activos no es por sí mismo doble conteo. D&A añade depreciación de derechos de uso; se necesita inversión de reposición. La reserva histórica 450 millones EUR es estimación, no capex mantenible revelado. Las adiciones anuales de derechos de uso 2025 sirven de referencia pero incluyen el perímetro existente durante ese ejercicio, no una medida pura del futuro HPC. La remuneración en acciones se conserva como coste económico en EBIT; no se añade como caja gratuita. La reserva dilutiva de premios existentes no debe convertirse además en una segunda penalización anual por la misma compensación.

Hay una pequeña limitación de las sensibilidades FX: MICC se convierte a EUR al cambio base y se mantiene fijo en EUR al variar el cambio de escenario. Eso altera en unos céntimos su valor USD pese a mantener fijo el precio USD de la participación. No afecta al caso base. Para una sensibilidad limpia, mantener MICC en su moneda de cotización antes de convertir.

## 3. Historia: beneficio total, no únicamente EPS

Los tres ejercicios y los cuatro trimestres de ventas ya están cubiertos por el informe y su anexo. UL publica beneficios/caja semestrales, no cuentas completas Q1/Q3. No se puede fabricar un EBIT o CFO trimestral dividiendo H1 por dos. El último TTM económico completo es junio de 2026; las ventas TTM septiembre no actualizan automáticamente el beneficio.

Esta auditoría añade el beneficio total atribuible continuo, útil para separar negocio de recompras. EUR miles de millones:

| Periodo | Beneficio GAAP atribuible | Beneficio subyacente atribuible |
|---|---:|---:|
| FY2023 | 6,002 | 6,069 |
| FY2024 | 5,430 | 6,816 |
| FY2025 | 5,682 | 6,761 |
| H1 2024 | 3,287 | 3,607 |
| H1 2025 | 3,125 | 3,451 |
| H1 2026 | 3,024 | 3,508 |
| TTM junio 2025 | 5,268 | 6,660 |
| TTM junio 2026 | 5,581 | 6,818 |

TTM anterior = FY2024 + H1 2025 − H1 2024; actual = FY2025 + H1 2026 − H1 2025. El beneficio subyacente total crece **2,37%**, frente a aproximadamente 3,31% del EPS subyacente; el beneficio GAAP continuo crece **5,94%**. Esto no acredita crecimiento estructural de beneficios del 15%, pero el plan no impone ese mínimo universal. El FY2025 subyacente total retrocedió 0,81%, aun cuando el EPS subió.

La misma reserva recurrente del autor, 0,6% de ventas después de impuesto al 26%, aplicada íntegramente al beneficio atribuible da un proxy de **6,431→6,593**, +2,52%. Es conservador respecto a la asignación del gasto a minoritarios y no es una cifra reportada ni una medida exacta de beneficio normalizado atribuible.

El FCFF económico consolidado comparable del anexo se reproduce: **6,345758→6,511707**, +**2,62%**, después de la misma reserva de reestructuración, reposición de leases y circulante normalizado. No se confunde con FCF después de intereses. El FCF reportado **5,443→6,386**, +17,3%, está ayudado por la mejora del circulante; no demuestra por sí solo crecimiento recurrente de caja a esa tasa.

Fuentes: [Annual Report 2025, reconciliación de EPS y beneficio, página impresa 43](https://www.unilever.com/files/unilever-annual-report-and-accounts-2025.pdf), [históricos H1 2024/2025, páginas 2–3](https://www.unilever.com/files/unilever-half-year-historical-financials-excluding-ice-cream-pdf.pdf) y [H1 2026, reconciliación de EPS](https://www.unilever.com/files/unilever-q2-2026-results-full-announcement.pdf). `history_check.py` reproduce esta tabla y los dos puentes normalizados.

## 4. Diez años, reinversión y retorno comparable

La DCF original contiene diez años explícitos, una segunda fase de desaceleración del crecimiento y terminal con reinversión g/ROIC. No he encontrado crecimiento terminal gratuito. Sin embargo, capex/D&A/lease/circulante permanecen fijados por porcentajes, mientras el ROIC incremental implícito del año diez aún es **30,60%** para UL actual, frente al **19%** terminal. En Foods sigue cerca de 43,9%, frente al 15% terminal. Se necesita justificar esa transición o mostrar su efecto.

Prueba independiente: conservar años 1–5; durante 6–10 mezclar gradualmente la reinversión mecánica con NOPAT × crecimiento anual / ROIC terminal. La ponderación de la segunda aumenta 20 puntos anuales hasta 100%. Se conserva el terminal y no se suma simultáneamente la reinversión completa y la mecánica. Esto reduce el valor directo en **0,75 USD** y el de la operación en **0,82 USD**. No es una corrección obligatoria única: una marca puede sostener rendimientos incrementales altos. Es una prueba explícita que evita esconder un salto de reinversión en el terminal.

Para el retorno, el código original de la SOTP usa 0,67 años previos y después diez flujos completos. La función de TIR utiliza diez años naturales, con 67% UL y 33% paquete en el primero. Ambas son aproximaciones admisibles por separado, pero no son la misma serie de caja y no deben presentarse como perfectamente reconciliadas. La reconstrucción independiente paga el tramo inicial en t=0,67; los diez flujos posteriores en t=1,67…10,67; y el residual en t=10,67. Mantiene deuda estática, distribuye toda la caja y desplaza JV/minoritarios por el tiempo transcurrido. Produce 7,83%, o 7,67% con la transición de reinversión. El horizonte pasa a 10,67 años y se rotula como tal.

No es una TIR bursátil garantizada: depende de distribuciones, financiación, monedas y valoración terminal. No agrega dividendo, recompras o pago de deuda sobre la misma caja. Para una cifra única definitiva, el autor debe adoptar un calendario común y una política explícita de deuda/distribuciones en DCF y retorno; entretanto las cifras pueden publicarse como alternativas identificadas.

## 5. Coste de capital y comparables

El WACC EUR 7,5% se construye con Bund 3,31%, beta supuesta 0,80, prima de mercado 5%, prima de ejecución 1%, coste marginal de deuda supuesto 4,3% y ponderación deuda cercana a 15%. Reproduce aritméticamente aproximadamente 7,54%. **Beta, prima y coste marginal de deuda son elecciones analíticas, no mediciones empíricas independientes demostradas por el expediente.** Esta auditoría no convierte esa calibración en un hecho observado. La sensibilidad al 8% reduce el valor directo a 59,72 USD y el paquete a 56,68 USD; importa mucho más que redondear los múltiplos.

El WACC USD de Foods 8,5% es distinto, como corresponde. Con el apalancamiento central y deuda al 6%, supone un coste de equity del negocio combinado aproximadamente del 10,9%, no un coste de equity del 8,5%. El coste de equity EUR de UL es 8,31%. No puede afirmarse simplemente que una TIR del paquete próxima a 8% supera el coste de capital porque sea mayor que 7,5%: se estaría comparando retorno al accionista con WACC y mezclando monedas/negocios. Un inversor puede aceptar ese perfil, pero necesita una justificación propia del riesgo asumido.

La dirección de la comparación PG/CL/MKC es razonable y los EPS de guía proceden de publicaciones recientes. Revisión puntual: [PG del 22/10](https://us.pg.com/newsroom/news-releases/PG-Announces-Fiscal-Year-2027-First-Quarter-Results/) da 6,89–7,11 USD y punto medio 7,00, por lo que a 162,06 el P/E es 23,15x; la aproximación 6,993 del informe no cambia su 23,2x redondeado. [CL del 30/10](https://investor.colgatepalmolive.com/news-releases/news-release-details/colgate-palmolive-announces-3rd-quarter-2026-results) confirma crecimiento de EPS base 5–7%. [MKC Q3](https://ir.mccormick.com/node/34076/pdf), descargado en el expediente, sostiene la guía utilizada.

El múltiplo ponderado que implica 77,68 USD no es una segunda prueba independiente de valor justo: mezcla años fiscales, categorías, crecimiento y ejecución, y sus ponderaciones no son una asignación auditada de beneficios futuros. Sirve como contraste. El modelo operativo sí está construido por flujos, no copiando ese múltiplo, pero su independencia de construcción no prueba que sus supuestos sean conservadores.

## 6. Evento y aplicación del plan

El [sitio oficial del Investor Event](https://www.unilever.com/investors/unilever-investor-event-2026/) mantiene 4 de noviembre, 08:30–14:30 Eastern Time: **13:30–19:30 UTC**. A las 06:30 aún no ha empezado. El anuncio del [6-K del 3/11](https://www.sec.gov/Archives/edgar/data/217410/000165495426009451/a6665b.htm) es información ya pública; no equivale a haber escuchado el evento. No se incorporan futuras intervenciones ni Q&A. Q3 ya fue publicado; no hay que tratar el evento como unas cuentas Q3 aún pendientes.

Con el [plan vigente](https://fundamentalpullback.github.io/data/plan/Plan_Completo_2026-10-30.pdf), la lectura es:

- Calidad de negocio y balance: tesis plausible, con claims y ejecución analizados.
- Beneficio/caja: comparaciones completas disponibles, crecimiento económico reciente modesto; las previsiones requieren aceleración, no mera extrapolación del FCF reportado.
- Precio: próximo al intervalo central, con transacción central por debajo del mercado; no una ganga acreditada.
- Retorno frente al riesgo: **condición todavía no demostrada de forma robusta**, por sensibilidad a tasas, FX, calendario y términos finales. No se impone una rentabilidad mínima universal.
- Evento: revisar material nuevo cuando exista; no declarar hoy que confirma el modelo.
- **Resultado: candidato de seguimiento a valor razonable; no aprobación fundamental automática de una compra parcial. Stage3.5 sigue completamente separado.**

Esto no exige etiquetar la investigación como inconclusa por no poder observar cuentas trimestrales que el emisor no publica o costes legales finales aún no determinados. La investigación está completa con rangos y supuestos explícitos; una decisión de inversión puede seguir siendo esperar.

## Reproducción y alcance

`recompute.py` lee el JSON original y reimplementa las fórmulas, sin importar los módulos originales que escriben resultados. `audit_calculations.json` contiene flujos, terminales, cuatro comprobaciones de reproducción y las alternativas de reinversión/calendario. `history_check.py` y `earnings_history_check.json` contienen los datos primarios transcritos y cuatro controles de TTM. El manifiesto identifica por hash las entradas auditadas. Se conservan tanto los valores originales como las sensibilidades, para que el lector no confunda una auditoría metodológica con una nueva noticia del emisor.
