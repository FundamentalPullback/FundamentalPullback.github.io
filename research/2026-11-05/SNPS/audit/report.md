# SNPS: auditoría independiente de la revisión del 5 de noviembre de 2026

## Dictamen y uso permitido

**Apto con salvedades para investigación condicional y observación. No constituye aprobación fundamental, ficha Stage 3.5 ni autorización de entrada.** La revisión corrige una omisión material del expediente A104 al incorporar el Investor Day del 30 de septiembre. El modelo nuevo no fuerza un descuento cambiando arbitrariamente la tasa. Tampoco demuestra una ventaja suficiente al cierre regular de 462,95 dólares del 4 de noviembre.

Reconstruí el cálculo sin importar ni ejecutar el motor de valoración del autor. Los tres escenarios coinciden: adverso 163,094273; base 357,045578; favorable 607,619749 dólares por acción. No son probabilidades, pisos ni objetivos garantizados. La comparación más útil no es simplemente precio superior a base: el contraste de ejecución empresarial vale 423,227440; con WACC 50 puntos básicos menor, 465,991388. Ese último resultado explica aproximadamente el precio, pero no ofrece holgura frente a desviaciones. El estrés integrado sobre esa ejecución reduce el valor a 311,515677. Son sensibilidades analíticas, no nueva guía de la compañía.

El trabajo puede publicarse como una actualización sustancial y terminada de la valoración condicional, conservando expresamente las limitaciones de comparación económica. No debe rotularse como aprobación completa de todas las puertas de Fundamental Pullback. La falta de una serie homogénea de EPS y caja combinados continúa siendo una limitación real para aprobar, no un dato negativo inventado ni una excusa para omitir la valoración.

## Alcance y resultados reproducibles

- **992 controles de cálculo:** tres casos completos de diez años, desglose de ingresos, EBIT, impuestos, reinversión, FCFF, descuentos, terminal, puente de capital, valoración inversa, sensibilidad y contraste de ejecución. Error máximo frente al motor del autor: 1,46×10⁻¹¹ en las unidades del modelo.
- **134 controles contra HTML primario:** estados anuales, trimestrales y acumulados; ingresos, EBIT, beneficio atribuible continuado, acciones diluidas, SBC, amortización adquirida, reestructuración, costes de adquisición, intereses, CFO y PPE/software. Los flujos de Q2 y Q3 se reconstruyen por diferencias de acumulados. Las convenciones de signo de gastos están identificadas.
- **Libro con 702 fórmulas:** 453 importes y resultados contrastados con mi motor, más los mismos 453 después de recálculo nativo en LibreOffice. Sin errores de fórmula, cachés ausentes o enlaces externos. No se afirma haber usado Microsoft Excel.
- **Pruebas activas adicionales en Artifact Tool:** aumentar Rf del 4,9% al 5,0% lleva WACC a 9,63142% y valor base a 351,177847; elevar el crecimiento EDA de FY31 del 11% al 12% cambia años posteriores y lleva el valor a 361,426486. Ambos resultados coinciden con cálculos independientes. Los cambios fueron temporales, se restauraron y no modificaron el libro entregado.
- **Técnica:** el cierre se verificó con dos proveedores. Las EMA se reconstruyeron separadamente por el autor a partir de la revisión técnica independiente. El volumen final difiere ligeramente entre proveedores; no se certifica una señal de volumen ni una entrada.

Las verificaciones no convierten hipótesis en hechos. Las sensibilidades/reversos exportados como valores requieren regeneración si se modifican supuestos; los casos principales sí contienen fórmulas editables. La inspección visual de portada y proyección no detectó importes ilegibles; se pidió corregir altura del título y retirar detalles de herramientas que no aportaban al lector.

## Hallazgo corregido antes de la versión final

**Contradicción de etiqueta, no de valor:** el importe FY23 de 191,822 millones no es PPE bruto frente a PPE neto de 189,618. El 10-K presenta PPE neto de 189,618 y otra línea de software capitalizado de 2,204. La suma de 191,822 es inversión PPE más software. El autor corrigió la explicación, el generador histórico y el libro sin modificar el DCF. Las ventas de inmuebles FY24/FY25 están separadas en el estado de caja; no se descontaron del PPE para fabricar mayor flujo libre.

## Fuentes y consistencia económica

**Historia y perímetro.** El EBIT TTM controlado por filings es 914,927 + 680,963 − 793,534 = 802,356 millones, no la cifra aproximada de 1.040 de un agregador. El SBC continuado FY23/FY24 es 513,094/657,935, distinto del SBC total del grupo. Los ingresos proforma combinados permiten reconstruir el comparador TTM de 8.730,695 millones y crecimiento de ingresos del 7,86%; no permiten certificar el mismo grado de homogeneidad para beneficio y caja. Software Integrity, Ansys, desinversiones y el cambio de reconocimiento del canal impiden llamar orgánico al salto reportado. La normalización conserva SBC y no capitaliza ganancias de desinversión.

**Guía prospectiva.** La fuente primaria de septiembre confirma la renovación de objetivos y el aumento de inversión. El modelo reconcilia el FCFF por EBIT con una conversión orientativa de la guía FCF, restando SBC y añadiendo intereses después de impuestos; no confunde FCF con FCFF. El interés bruto utilizado es una estimación, no la guía de interés y otros ingresos netos. La amortización de intangibles adquiridos no se deduce como mantenimiento mecánico ni se convierte automáticamente en ahorro fiscal deducible. I+D, SBC, capex, circulante y una reserva de inversión pagan mantenimiento/crecimiento.

**Guía frente a escenario.** El CAGR objetivo de aproximadamente 15% cubre FY26–FY30, cuatro años. El contraste del modelo prolonga ese ritmo hasta FY31 antes de desvanecerlo. Esa prolongación y el margen económico después de SBC son hipótesis del analista, no reproducción literal de toda la guía. La reserva estratégica del 1% tampoco es un coste obligatorio verificado; quitarla aumenta el valor unos cuatro dólares y no resuelve la diferencia principal.

**Capital.** El nominal de deuda y treasury-lock suma 10.110,449 millones frente a 10.037,360 contables. La diferencia por costes/descuento no es caja disponible. El desembolso ASR de 1.000 millones se cuenta una vez; no se acredita entrega pendiente ni recompra futura gratis. La caja de cierre FY26 está proyectada desde julio con el FCF restante de la guía, no certificada por un balance de noviembre. El denominador 193 − 1,735 = 191,265 millones es una estimación diluida. La guía FY27 de 190–192 ya se publicó junto a intención de recompras; no se le vuelve a restar el ASR. Arrendamientos operativos siguen en gastos y no se deducen otra vez como deuda.

**Descuento y terminal.** La fórmula de WACC 9,54142% reproduce CAPM, deuda y efecto fiscal sin prima adicional. Beta histórica, coste de deuda supuesto y peso objetivo conservan incertidumbre, especialmente tras Ansys. La referencia de Treasury del 4 de noviembre y ERP mensual no es una cotización simultánea perfecta; el informe lo expone. El crecimiento terminal se paga con reinversión NOPAT×g/ROIC y no usa una perpetuidad sin inversión. El 25% de ROIC incremental no se presenta como rentabilidad histórica sobre el precio pagado por Ansys. Aproximadamente el 60% del EV base depende del terminal: el rango sigue siendo sensible a duración, margen y descuento.

## Puertas de decisión y condiciones de reapertura

Opportunity 100 conserva el umbral vigente de 85. Los filtros técnicos básicos pasan: cierre por encima de EMA50, EMA20 superior a EMA50, liquidez y retroceso dentro de límites. La EMA200 tiene pendiente positiva. No hay obligación de comprar por cumplirlos: el máximo del 29 de octubre es inferior al del 9 y el mínimo del 3 de noviembre aún no era un pivote confirmado con dos sesiones posteriores al corte.

No se ha establecido una configuración prospectiva con señal, máximo técnico/fundamental, invalidación, stop, riesgo de campaña, capital y tamaño. Cantidad aprobada: cero. La fecha del próximo resultado no está confirmada en una fuente primaria; la estimación externa de diciembre no puede convertirse en evento confirmado ni en veto artificial por la semana de resultados.

Reabrir ante resultados FY26 y guía FY27 que confirmen ingresos, recuperación de IP, SBC, capex y caja económica, o ante un precio que deje compensación suficiente en un escenario razonable resistente. El escenario favorable por sí solo no resuelve la comparabilidad ni autoriza una compra pequeña para eludir la puerta fundamental.

## Fuentes controlantes

- [10-K FY25, historia y perímetro](https://www.sec.gov/Archives/edgar/data/883241/000088324125000028/snps-20251031.htm).
- [10-Q Q3 FY26, balance y acumulados](https://www.sec.gov/Archives/edgar/data/883241/000088324126000025/snps-20260731.htm).
- [Investor Day del 30 de septiembre](https://news.synopsys.com/2026-09-30-Synopsys-Details-Growth-Strategy-and-Long-term-Financial-Model-at-2026-Investor-Day).
- [ASR del 5 de octubre](https://news.synopsys.com/2026-10-05-Synopsys-Initiates-1-Billion-Accelerated-Share-Repurchase-Agreement).
- [Cierre histórico](https://stockanalysis.com/stocks/snps/history/), contrastado con la serie Yahoo preservada.

El directorio de auditoría contiene scripts de reconstrucción, resultados, comprobaciones y hashes. El acta no afirma que el contenido esté ya publicado en la web; esa verificación corresponde a la liberación posterior.
