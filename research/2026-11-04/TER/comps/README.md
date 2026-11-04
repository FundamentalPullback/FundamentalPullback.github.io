# TER: comparación sectorial al cierre de 3 de noviembre de 2026

**Conclusión: útil como contraste, no como precio objetivo por mediana.** Advantest es el comparable operativo principal, pero tiene margen muy superior y otra mezcla de producto; Cohu es un comparable secundario del ciclo de test/handling, con EBIT TTM negativo. Ninguna media de estos dos negocios demuestra que TER esté barato.

## Lectura rápida

| TTM, moneda local en millones | TER, USD | Advantest, JPY | Cohu, USD |
|---|---:|---:|---:|
| Ventas | 5.000,771 | 1.447.077 | 569,307 |
| EBIT publicado, SBC incluida | 1.605,983 | 723.494 | -13,552 |
| Margen EBIT | 32,11% | 50,00% | -2,38% |
| CFO menos capex | 1.024,864 | 463.173 | 55,854 |
| SBC | 80,087 | 4.968 | 22,972 |
| FCF menos SBC, proxy económico | 944,777 | 458.205 | 32,882 |
| EV/ventas, pantalla convencional | 8,28x | 17,64x | 3,81x |
| EV/EBIT, pantalla convencional | 25,80x | 35,28x | No significativo |
| FCF/capitalización básica | 2,44% | 1,79% | 2,36% |

La diferencia de EV/ventas entre TER y Advantest no es una diferencia equivalente en valoración de beneficios: sus márgenes EBIT son distintos. El descuento de TER frente al EBIT de Advantest es aproximadamente 27%, pero estos múltiplos no están normalizados por crecimiento futuro, rentabilidad de mitad de ciclo ni riesgo comercial. Que ambos estén caros frente a sus flujos sostenibles sigue siendo posible.

Cohu muestra por qué evitar la mediana: nueve meses de EBIT ligeramente positivo más un cuarto trimestre anterior débil producen una pérdida TTM. Su EBIT ajustado TTM de $43,799 millones excluye partidas que la comparación principal mantiene. No sustituimos esa cifra por EBIT GAAP para fabricar un múltiplo positivo.

## Definiciones y controles

- TTM Advantest: ejercicio abril2025-marzo2026 menos abril-septiembre2025 más abril-septiembre2026. TER y Cohu: FY2025 menos9M2025 más9M2026. Fechas finales septiembre27,30 y26, respectivamente.
- Capex Advantest incluye PPE e intangibles. Su FCF después de principal de arrendamientos es ¥458.437 millones; después de arrendamientos y SBC, ¥453.469 millones. IFRS clasifica ese principal en financiación. No confundir el FCF sin ese ajuste con una medida perfectamente comparable al US GAAP.
- SBC se conserva como coste del EBIT. FCF menos SBC es una sensibilidad económica, no flujo GAAP ni sustituto exacto de la dilución. Para Advantest se utiliza gasto de SBC de la nota de segmentos, no simplemente movimientos patrimoniales.
- Las tres capitalizaciones usan acciones observadas, no acciones medias de EPS. En Advantest se incluyen sólo los cambios de octubre expresamente publicados. La caja se reduce por la recompra publicada; no es una estimación completa de caja a noviembre.
- Cotizaciones de pares corroboradas en dos proveedores secundarios, no certificadas por el emisor. Advantest usa ¥35.770 del2noviembre porque el3noviembre fue festivo bursátil en Japón. Cohu usa $50,03 del3noviembre. No se mezclan los precios intradía del4noviembre.

## Puentes que no deben ocultarse

**TER:** la pantalla convencional usa capitalización más deuda menos caja/inversiones líquidas y no descuenta Technoprobe. La variante industrial descuenta $1.777,502 millones de participación marcada, añade pensiones $152,910 millones y NCI rescatable contable $49,065 millones: EV/EBIT24,81x. El NCI contable no es su valor económico total. El modelo principal puede usar otra estimación explícita de NCI. No añadir además el valor contable de Technoprobe.

**Advantest:** deuda convertible nominal ¥100.000 millones, no sólo valor contable IFRS¥89.486 millones. A¥35.770 está ligeramente bajo el precio de conversión¥35.946,5; las concesiones de acciones futuras siguen existiendo. Los valores de inversión¥432.586 millones no se tratan automáticamente como caja. Restar sólo su valor contable de septiembre como sensibilidad reduce EV/EBIT de35,28x a34,68x; no es una valoración actual de cada inversión. Incluir pasivos de arrendamientos aumenta el múltiplo a35,30x, pero tampoco armoniza el EBIT con US GAAP.

**Cohu:** deuda nominal$309,804 millones frente a valor contable$302,061 millones. Su convertible de$287,5 millones está dentro del dinero. La pantalla básica3,81xventas omite opciones de conversión. Una sensibilidad de valor intrínseco, sumando conversión y restando el capped call, da3,98x; sin offset da4,24x. El cap$41,02 está por debajo de$50,03. Las fechas de liquidación y el valor temporal impiden llamar a esa sensibilidad valor razonable. No se añaden simultáneamente toda la deuda y todas las acciones de conversión. Las RSU/PSU pendientes tampoco se convierten sin más en acciones emitidas.

## Qué falta antes de usarlo para una decisión

Actualizar acciones/caja al mismo corte y valorar convertibles/opciones; reconciliar arrendamientos a una base común; separar inversiones estratégicas a mercado; establecer beneficios sostenibles y estimaciones futuras homogéneas. No hay consenso forward ni precio objetivo por pares en este archivo. Los múltiplos actuales sirven para contrastar exigencia y calidad, no para reemplazar el DCF.

## Reproducibilidad

Ejecutar `python reproduce.py` sin red ni dependencias externas. `inputs.json` contiene las cifras seleccionadas, fechas, localizadores y URLs; `results.json` conserva puentes y sensibilidades; `comparison.csv` resume; `checks.json` contiene pruebas. `build_inputs.py` documenta la importación inicial de los datos TER del paquete vecino y no se necesita para reproducir los cálculos. No se incluyen PDFs ni filings completos.
