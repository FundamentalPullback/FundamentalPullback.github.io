# KSS: capital y alquileres, corte de información 4-noviembre-2026

Importes USD millones salvo acciones exactas. No hay balance posterior a 1-agosto-2026 en submissions revisado. Las cifras no son caja/deuda observadas en noviembre.

## Fuentes primarias
- [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/885639/000119312526381893/kss-20260801.htm): portada acciones; p3 balance; p6 cash flow; nota3 p9 deuda; nota4 pp10–13 alquileres; notas5/7/8 pp13–14 premios, impuestos y dilución; nota9 p14 dividendo; p26 recompras.
- [FY25 10-K](https://www.sec.gov/Archives/edgar/data/885639/000119312526115982/kss-20260131.htm): nota3 pp54–57 alquileres; nota4 p57 beneficios; nota5 pp58–59 impuestos; nota6 pp60–61 equity awards.
- [Resultados agosto26, sección Capital Allocation Outlook](https://www.sec.gov/Archives/edgar/data/885639/000119312526365860/d171200dex991.htm): reinicio proyectado de recompras hasta100 bajo autorización existente; no es ejecución.
- [Submissions SEC](https://data.sec.gov/submissions/CIK0000885639.json): calendario de documentos revisado hasta formulario3 de noviembre2; los 8-K posteriores a agosto se detallan abajo.

## Puente de capital comprobado
Caja821; notas nominal1342, valor libro1325 (17 de descuentos/costes no amortizados); revolver0. El puente conservador contractual utiliza1342, no1325, y muestra521 de deuda neta antes de caja operativa mínima/claims adicionales. El fair value de notas divulgado ronda1200, pero no debe reemplazar silenciosamente la obligación nominal. No distribuir toda caja si se requiere colchón operativo: separar caja bruta y caja excedente, con supuesto visible.

Finance leases1935 (82 corriente+1853 LP); financing obligations452 (10+442); total2387. Operating leases2709 (96+2613). Deuda+todos los alquileres6438; neto de caja5617. Son cifras para la reconciliación de balance, NO una instrucción para restar5617 a un EV después de renta.

Finance lease assets1480, financing assets34, operating ROU2297. La diferencia activo/pasivo no permite declarar que los pasivos no son económicos. En FY25 financing obligations455 vs activo36 y descuento16%; incluye115 de futura ganancia no monetaria y pagos futuros1411, de los cuales1071 interés. Sigue habiendo cash real79 anualFY25,41 H1FY26. No deducir115 como claim adicional ni tratar36 como importe de liquidación.

## Enfoque recomendado: alquileres como gasto operativo completo
Sobre EBIT normalizado de extraordinarios, sustituir la DA de finance leases y financing assets por su renta cash completa; sustituir el gasto operating por su cash. Fórmula:

EBIT_renta = EBIT_normalizado + DA_finance_financing + gasto_operating − cash_operating − cash_finance_financing.

FY25: DA107+4=111; operating expense271 vs cash278; finance cash117+75=192; financing cash71+8=79. Ajuste total111+271−278−192−79 = −167. Renta total549.

H1FY26: DA59+2=61; operating expense136 vs cash137; finance cash57+40=97; financing cash37+4=41. Renta275.

H1FY25: DA54+2=56; operating expense135 vs cash146; finance cash59+42=101; financing cash36+4=40. Renta287.

TTM agosto: DA111+61−56=116; gasto operating272; operating cash269; finance/financing cash268; total renta537. Ajuste EBIT TTM116+272−269−268 = −149. Usar este TTM trazable antes que copiar−167 FY25. No confundir menor renta con ahorro perpetuo asegurado: sensibilidad FY25−167, cash rent±5–10%, y renovación/escalación por escenarios.

FCFF = EBIT_renta*(1−tasa fiscal normalizada) + DA_residual − capex físico − ΔNWC operativo. DA_residual elimina116 en TTM; no volver a sumar la DA lease excluida. Si se reconstruye cash flow directamente, no añadir como cash los landlord reimbursements/financing proceeds sin contabilizar simultáneamente el coste/obligación correspondiente. Si se parte del estado de cash flow, excluir variaciones de lease liabilities/ROU del NWC para no repetir las conversiones ya hechas.

Puente EV→equity: sumar caja excedente, restar notas1342 y claims independientes justificados. NO restar2387 ni2709: sus pagos están ya incluidos en el gasto/renta recurrente. Mantener renta en todo el período terminal; vencimiento contractual no significa locales gratuitos. Capex de mantenimiento físico sigue siendo necesario, incluyendo mejoras de locales que pague el retailer. El régimen económico cash-rent es una normalización; comprobar diferencia temporal entre cash rent y deducción fiscal real en sensibilidad, no pretender que el gasto fiscal publicado se transforma automáticamente.

## Alternativa capitalizada coherente, no mezclar
Reconstruir operación antes de financiación de alquileres, separar interés implícito de operating leases y su depreciación económica, y modelar adquisición/renovación de ROU como inversión con matching económico. Para finance/financing, EBIT publicado ya excluye su interés pero contiene amortización: modelar sus activos y renovación/reposición, además de capex físico. Los nuevos contratos/reinversiones no son gratis. Una vez flujos y WACC están en base capitalizada consistente, deducir pasivos de alquiler2387+2709 además de notas, con sensibilidad a valor económico frente a carrying amount y condiciones de renovación. El descuento16% de financing obligations hace peligroso utilizar455/452 como PV económico exacto a un WACC distinto. No usar simultáneamente renta íntegra como gasto y deducción total de lease debt, ni sumar toda renta al EBIT perpetuo y olvidar reinversión de ROU.

## Otros claims, impuestos y beneficios
FY25 beneficio definido aquí es defined-contribution savings plan + nonqualified deferred compensation; coste50 ya en operación. No se revela saldo separado contemporáneo de deferred compensation ni activo compensatorio identificable en estos informes. Companyfacts contiene un saldo39 a enero2012: está obsoleto, no utilizable. Tampoco hay base para asumir saldo cero o sumar todo other long-term liabilities243 como deuda adicional. Dejar sensibilidad/reserva explícita si se necesita, no inventar precisión. Otros activos LP433 en Q2 son agregados, no caja disponible ni fondos de pensión verificados.

FY25 gross UTB178; intereses/penalidades20; importe neto que afectaría ETR168. No sumar178+168+20:168 no es un claim distinto. Receivable fiscal LP258, mayormente devolución NOL2020 aún no cobrada, y corriente4; payable corriente84. Falta reconciliar UTB entre contraactivos y pasivos antes de deducir deuda fiscal o añadir receivable. Un método limpio: no reconocer valor separado de estos activos ni pasivos contingentes en caso base, revelar incertidumbre y sensibilidad sobre cobros/pagos futuros; o construir escenarios de resolución explícitos sin doble contar NWC/cash tax. No equiparar automáticamente gross UTB con efectivo futuro a pagar.

DTL netoFY25 59 (balance brutoLP91 menos DTA32); Q2 balance DTL70. No deducir DTL completo adicional si sus reversos se reflejan en cash taxes. Tasa fiscal publicadaFY25 19% favorecida por liberaciones de reservas; H1FY26 24,1%, Q2 23,3%. Normalizar con tasa explícita razonable, no prolongar beneficios no recurrentes ni confundir provisión con impuesto cash. FY25 cash taxes51.

## Acciones y retornos
Portada113.376.445 acciones a28-agosto; promedio Q2 básico113m, diluido118m, más1m antidilutivo excluido; H1 diluido117m y4m antidilutivas. Son conceptos/fechas distintos. Para valoración actual, mostrar cover y sensibilidad diluida118m; no afirmar que118m sea fully diluted spot exacto. FY25 RSA/RSU3,598m y PSU2,609m son inventarios antes de nueva actividad, no sumar mecánicamente al denominador Q2. SBC34 FY25 y19 H1FY26, gasto no reconocido79 FY25 durante1,1 años. No añadir SBC gratis al FCFF y además olvidar futuras emisiones. Los1.747.441 warrants expiraron sin ejercicio el18-abril2026: no incluirlos como dilución vigente.

H1 dividendos cash28 y employee share tax withholding8, incluidos en caja821. Q2 cero recompras del programa; restantes2476 de autorización. Hasta100 en FY26 es plan anunciado, no evidencia de salida ni reducción de acciones. No bajar caja100 ni reducir acciones retrospectivamente. Como escenario futuro, modelar ambas patas con precio de recompra y monto ejecutado, sin crear valor por decreto.

Dividendo0,125 anunciado18-agosto, record9-septiembre, pago previsto23-septiembre. Después de la fecha de balance y antes del corte de valoración. Salida orientativa14,172 con cover shares; confirmar importe efectivo Q3 cuando esté disponible. Puede restarse como pro forma identificado si se pretende actualizar caja hasta noviembre, pero caja ajustada por un solo dividendo no es caja real noviembre: faltan operación, inversiones, recompra y deuda posteriores. No ofrecer este dividendo como próximo catalizador futuro al4-noviembre.

## Subsequent events revisados
- [18-agosto, item8.01](https://www.sec.gov/Archives/edgar/data/885639/000119312526355669/kss-20260818.htm): dividendo descrito.
- [25-agosto, item5.02](https://www.sec.gov/Archives/edgar/data/885639/000119312526365317/kss-20260825.htm): salida Christie Raymond, beneficios por acuerdo ejecutivo no cuantificados; Arianne Parisi nueva Chief Customer Officer. No balance actualizado.
- [26-agosto, items2.02/8.01](https://www.sec.gov/Archives/edgar/data/885639/000119312526365860/d171200d8k.htm): earnings, guía y dividendo; release adjunto recoge hasta100 recompra.
- [31-agosto, item5.02](https://www.sec.gov/Archives/edgar/data/885639/000119312526377068/kss-20260827.htm): salida Nick Jones y derechos de separación no cuantificados; Ryan Waymire nuevo CMO. No movimiento de capital cuantificado.
- [29-octubre, item5.02](https://www.sec.gov/Archives/edgar/data/885639/000119312526437812/kss-20261029.htm): Stacy Taffet al consejo; award previsto13-noviembre valor145.000 dólares, no145 millones, vesting1año; no capital actual confirmado. No tratar award previsto como ya emitido.

No apareció otro8-K posterior hasta el corte en la listaSEC local. No se demuestra ejecución posterior de recompras ni saldo corriente de caja por la mera ausencia de8-K.
