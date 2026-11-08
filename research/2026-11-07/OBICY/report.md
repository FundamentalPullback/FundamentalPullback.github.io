# OBICY: descarte operativo fechado por liquidez del ADR

**Fecha de revisión: 8 de noviembre de 2026. Última sesión utilizada: 6 de noviembre.** Resultado: el instrumento OBICY no supera actualmente el filtro de volumen del plan. No es una exclusión permanente de OBIC ni una conclusión sobre su valor intrínseco. No hay operación, precio objetivo ni entrada aprobada.

## Razón suficiente y reproducible

El plan exige volumen medio de veinte sesiones de al menos **500.000 acciones**. Para el ADR estadounidense OBICY, las veinte sesiones del 12 de octubre al 6 de noviembre arrojan:

- Stock Analysis: **45.627,15 ADR por sesión**.
- Yahoo Finance: **45.623,15 ADR por sesión**.

Ambas fuentes quedan aproximadamente un 91% por debajo del umbral. La diferencia de cuatro unidades en el promedio procede de una diferencia de 80 ADR en el volumen de la última sesión; no cambia la decisión. `screen_prices.csv` conserva las veinte observaciones y `screen.py` reproduce el cálculo.

La tabla del 6 de noviembre de Stock Analysis muestra cierre de **19,18 USD**, mientras Yahoo muestra **19,19 USD**. Se conserva la discrepancia, sin declarar una falsa precisión de cierre consolidado OTC. Las dos referencias superan 15 USD; **el precio no es el motivo del descarte**. El 15,77 del scanner del 1 de octubre es histórico, no cotización actual. El cálculo usa la tabla diaria fechada al 6 de noviembre, no una captura anterior.

Fuentes: [histórico OBICY](https://stockanalysis.com/quote/otc/OBICY/history/) y [serie diaria contrastada](https://query1.finance.yahoo.com/v8/finance/chart/OBICY?range=1y&interval=1d).

## Identidad, unidades y capitalización

OBIC Co., Ltd. es el emisor japonés de sistemas empresariales, integración y software, **Tokyo 4684**, sector tecnología. No es OBIC Business Consultants 4733 ni una empresa sanitaria o inmobiliaria.

Citi y Deutsche Bank identifican OBICY, CUSIP 674388103, como ADR OTC. Deutsche Bank confirma que es **no patrocinado**. La relación es **1 ordinaria por 2 ADR**: cada ADR representa media acción ordinaria. No se puede sustituir su volumen por el volumen de Tokio, convertir yenes en dólares sin FX o interpretar dos ADR como dos acciones ordinarias.

Al 30 de septiembre había 492 millones de acciones emitidas, incluidas 63,419551 millones en autocartera. Las 428,580449 millones netas equivalen económicamente a 857,160898 millones de ADR, pero **esa equivalencia no representa ADR efectivamente emitidos o negociables**. Aplicando 19,18–19,19 USD resulta una capitalización indicativa de 16.440–16.449 millones, sobre la base accionarial de septiembre. No se presenta como capitalización exacta actual porque posteriores recompras pueden modificar el denominador. No hay indicio de que el umbral de 2.000 millones explique el descarte.

Se archivó además una observación diaria USD/JPY del 6 de noviembre de 157,498. Es una referencia con horario propio, no un fixing simultáneo al cierre OTC; no se utiliza para forzar paridad exacta entre mercados. El desdoblamiento 5:1 de las ordinarias ocurrió el 1 de octubre de 2024 y los EPS comparativos publicados ya están ajustados.

[Identificación Citi](https://depositaryreceipts.citi.com/adr/guides/pgm_dispabook.aspx?cusip=674388103&pageId=15&subpageID=111), [programa Deutsche Bank](https://adr.db.com/drwebrebrand/dr-universe/dr_details.html?identifier=12462).

## Contexto fundamental actual, sin valoración ficticia

Los resultados publicados el 27 de octubre corresponden al semestre abril–septiembre 2026, **H1 del ejercicio que termina en marzo 2027**, bajo Japanese GAAP. No son resultados anuales 2027 ni un trimestre aislado. En millones de yenes:

- Ventas 75.023, frente 65.784, crecimiento 14,0%.
- Resultado operativo 51.038, frente 43.655, crecimiento 16,9%.
- Beneficio atribuible 44.383, frente 37.303, crecimiento 19,0%.
- CFO 38.009; compras de inmovilizado 767 e intangibles 57; caja final 206.420.
- Recompras 21.282 y dividendos pagados 20.366 explican por qué un CFO positivo no supone aumento equivalente de caja.

El margen operativo semestral es aproximadamente 68,0%, pero no constituye rentabilidad sostenible demostrada. Beneficios de participadas, ingresos financieros y realización de inversiones deben separarse de software recurrente antes de valorar. La guía anual revisada es 151.200 de ventas, 100.500 de resultado operativo y 85.000 de beneficio atribuible, no resultados ya realizados.

El dividendo intermedio ordinario es 47 JPY, con pago previsto 24 de noviembre. No se convierte en dividendo neto ADR sin impuestos, comisiones y aviso del depositario. El calendario primario sitúa la siguiente publicación en **finales de enero 2027**, todavía sin día exacto; 6 de noviembre era la fecha prevista del informe semestral, no una nueva presentación de resultados.

[Resultados semestrales](https://www.obic.co.jp/e/ir/pdf/602qe.pdf), [resultados FY marzo2026](https://www.obic.co.jp/e/ir/pdf/594qe.pdf), [calendario del emisor](https://www.obic.co.jp/e/ir/calendar.html).

## Alcance y seguimiento

Opportunity 85 del 1 de octubre permite investigar bajo el umbral de 65.

El score supera el mínimo 65 para investigar, pero no elimina el filtro de liquidez. Dado el incumplimiento cuantificado, este paquete es una revisión limitada de elegibilidad, no un estudio completo de tres ejercicios/cuatro trimestres ni un DCF. No se publican múltiplos, comparables o valores terminales incompletos como valoración aprobada. Se reconsiderará OBICY si su media móvil de veinte sesiones supera el umbral o si el usuario modifica expresamente el universo/instrumento permitido. Analizar o negociar 4684 en Tokio requeriría evaluar ese instrumento por separado, no asumir autorización o liquidez del ADR.
