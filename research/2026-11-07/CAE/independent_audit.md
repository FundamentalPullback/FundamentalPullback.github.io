# Auditoría independiente de CAE

Fecha de corte: 8 de noviembre de 2026. Dictamen: el paquete condicional es reproducible, pero la investigación sigue materialmente parcial y no autoriza entrada ni operaciones.

## Resultado

Se ejecutaron 146 comprobaciones sobre hashes, fuentes archivadas, TTM pareados, suma de los cuatro trimestres, flujos, valoración y continuidad terminal. Todas pasan. La ejecución del modelo en un directorio temporal reproduce exactamente `results.json` y `history.csv`, sin modificar las salidas originales. Valor por acción: 4,821941705 / 11,929452159 / 20,635875056 USD, frente a 26,85 USD del cierre del 6 de noviembre.

Se revisaron el informe, modelo, resultados, historia, estado, manifiestos y archivos primarios anuales FY2025/FY2026 y trimestrales. Los estados respaldan las cifras IFRS utilizadas. La historia de caja FY2024 incluye Healthcare discontinuado y está expresamente separada del uso valorativo. El EBIT comparable TTM, excluido el resultado después de impuestos de participadas, es 659,7 y 619,9 millones CAD antes de la hipótesis recurrente de 30 millones. El nuevo beneficio ajustado excluye amortización adquirida y no se empalma con la definición anterior. El modelo conserva esa amortización y la remuneración basada en acciones en los márgenes.

El aumento de caja TTM no se trata como aumento permanente del beneficio. Se contrastan circulante, inversión material e intangible, y dividendos/aportaciones de participadas. Las distribuciones de participadas se valoran al coste de equity, netas de aportaciones y ya en la participación de CAE; no se multiplican nuevamente por la propiedad ni se suma su valor contable. La futura remesa neta sigue siendo hipótesis material pendiente.

El anuncio primario archivado identifica 500 millones USD como valor empresarial de Flightscape, no efectivo neto para CAE. No se incorpora ingreso por venta al modelo que retiene el negocio. La deuda de 3.214,9 millones CAD incorpora arrendamientos e I+D y se deduce una sola vez. No se vuelve a deducir principal de arrendamientos en FCFF, aunque sí se usa en la comprobación histórica separada. No se suman pagos contractuales no descontados a la deuda registrada.

El cambio CAD/USD de 1,4113, libre de riesgo CAD del 3,67% y ERP de 4,41% más 0,22 puntos están respaldados por los archivos fechados del Banco de Canadá y Damodaran. Beta y coste de deuda son hipótesis declaradas. Las acciones son ordinarias, sin multiplicador ADR; 324 millones es denominador prudencial, no número plenamente diluido actualizado y certificado.

## Reinversión y reservas

En todos los años, inversión bruta más circulante menos D&A iguala reinversión neta y FCFF iguala NOPAT menos reinversión menos transformación. La inversión bruta es positiva. El año 10 converge a NOPAT × g / ROIC y la reinversión terminal es exactamente la del año 10 multiplicada por 1 + g. No hay salto mecánico terminal ni liberación gratuita de D&A.

Estas identidades no validan un plan físico de activos ni el stock de capital que produciría el ROIC supuesto. Falta una conciliación de renovación, capacidad ociosa y capital operativo; se conserva como brecha material. Los 150 millones de caja operativa, 30 millones de reorganización recurrente y 60 millones de transformación adicional son hipótesis separadas, no pasivos certificados. El balance respalda 109,9 millones de obligaciones de prestaciones y 73,5 de minoritarios, pero falta validar financiación actuarial y valor económico de minoritarios. No se da por probado que usar valor contable de minoritarios sea conservador.

## Correcciones realizadas

Se corrigió la descripción de 29,2 millones TTM: es remuneración liquidada en acciones añadida de vuelta en CFO, no todo el gasto de SBC. El gasto total FY2026 neto de equity swap es 60,0 millones frente a 36,7 millones liquidado en acciones. Restar únicamente el componente no monetario en el diagnóstico evita duplicar lo ya pagado en efectivo. Se añadió comentario equivalente en el código. No cambian flujos ni valoraciones.

Se precisó en el informe que inversión bruta y ROIC terminal no constituyen una validación física, y que minoritarios a valor contable no son una valoración independiente. Se actualizaron los hashes del manifiesto congelado y se repitieron las comprobaciones sobre el paquete final.

## Evento y alcance

El aviso primario archivado fija resultados el 11 de noviembre después del cierre y conferencia el 12 a las 08:00 ET. No existen en el modelo resultados reales posteriores a junio ni se fabrican cifras de Q2.

El cierre posterior a Flightscape, capital incremental/capacidad ociosa, financiación de participadas, claims actualizados y calibración específica de tasas siguen pendientes. No hay bloqueo de herramientas ni acción denegada. No se ejecutaron escrituras remotas, publicación ni operaciones. Los archivos de comprobación son evidencia local de auditoría, no autorización para invertir.
