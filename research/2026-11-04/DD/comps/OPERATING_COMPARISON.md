# Ecolab y 3M: referencias operativas limitadas para DuPont

Corte: 4 de noviembre de 2026. Importes en millones de USD. No incluye múltiplos, precios, valoración ni recomendación. Los ingresos y resultados son trimestrales donde se indica Q3; CFO, inversión en PP&E, D&A y SBC son acumulados de nueve meses. Los campos de caja trimestral quedan vacíos deliberadamente: no se etiqueta un acumulado como trimestre.

## Ecolab: agua e industria, pero no una réplica de DuPont

Q3 2026: ventas 4.694,8; beneficio operativo GAAP 810,5; margen operativo 17,26%; EPS diluido reportado 1,95. Q3 2025: ventas 4.165,0; beneficio operativo 760,2; margen 18,25%; EPS 2,05.

9M2026: CFO 1.939,1; capex 902,0; CFO menos capex 1.037,1; D&A 819,3 y SBC 116,0. 9M2025: CFO menos capex 1.146,3. Por tanto, el crecimiento de ventas no se traduce mecánicamente en mayor caja libre medida así.

Ecolab sirve como referencia de exposición al agua, relaciones recurrentes de servicio y aplicaciones industriales. Su mezcla de servicios, higiene y equipos no equivale a los materiales y consumibles de DuPont. Además, las adquisiciones Ovivo Electronics y CoolIT Systems afectan ingresos, costes, capital invertido y financiación. El 10-Q señala pagos de incentivos extraordinarios a empleados de esas adquisiciones por 200 millones incluidos en CFO y aproximadamente 4.700 millones de inversión en adquisiciones/afiliadas durante 9M2026. Se mantiene CFO real: no se suman de vuelta los 200 millones.

Los márgenes de segmentos Ecolab tampoco son directamente comparables con EBITDA de segmentos DuPont: Ecolab excluye de sus segmentos amortización de determinadas adquisiciones y cargos especiales. La comparación numérica suministrada usa resultado operativo GAAP consolidado.

Fuente: https://www.sec.gov/Archives/edgar/data/31462/000162828026068208/ecl-20260930.htm (estados de resultados y caja; discusión de caja, adquisiciones y segmentos).

## 3M: diversificación industrial y contingencias diferentes

Q3 2026: ventas 6.584; beneficio operativo GAAP 1.558; margen 23,66%; EPS diluido 2,63. Q3 2025: ventas 6.517; beneficio operativo 1.447; margen 22,20%; EPS 1,55.

9M2026: CFO 2.046; compras de PP&E 704; CFO menos PP&E 1.342; D&A 997 y SBC 167. 9M2025: CFO menos PP&E 61. Las contingencias, pagos de acuerdos y cambios de cartera hacen que una extrapolación de esta recuperación sea especialmente peligrosa. No se añade la venta de activos a esta medida de caja.

3M tiene seguridad/industrial, transporte/electrónica y consumo, una combinación distinta de los segmentos actuales de DuPont. Sus contingencias propias no establecen una tasa de pasivo aplicable a DD. Tampoco se comparan márgenes ajustados: en Q3 2026 3M cambió su presentación no-GAAP para excluir amortización de intangibles como partida especial en todos los periodos presentados. Usar la cifra GAAP evita mezclar esa definición con la de DD.

Fuente Q3: https://www.sec.gov/Archives/edgar/data/66740/000006674026000311/mmm-20260930.htm

Fuente de cambio de definición: https://investors.3m.com/financials/sec-filings/content/0000066740-26-000308/q32026-8kerexx991.htm

## Hecho posterior material de 3M: no está en Q3

El 8-K de 3 de noviembre de 2026 comunica un acuerdo para resolver gran parte de reclamaciones de lesiones personales relacionadas con PFAS en el litigio AFFF. Compromiso nominal de 7.350 millones entre 2026 y 2034, sujeto a condiciones de participación; cargo estimado de 5.800 millones antes de impuestos en Q4 2026 por el valor presente. Es un hecho posterior al balance Q3, no un importe que deba insertarse retrospectivamente en su deuda o EBIT de septiembre. Tampoco debe trasladarse a DuPont como obligación propia.

Fuente primaria: https://www.sec.gov/Archives/edgar/data/66740/000006674026000318/mmm-20261103.htm

## Reproducción y límites

`python reproduce.py` reconstruye JSON/CSV de cifras operativas usando únicamente `source_numeric_subsets.json`, sin red ni dependencias externas. Los subconjuntos incluyen filas, etiquetas, URL, índice de tabla y huella SHA-256 de las tablas extraídas de los estados oficiales. D&A de Ecolab suma depreciación y amortización; SBC se conserva separada. CFO menos capex es una medida calculada, no una cifra GAAP denominada FCF.

El subtotal operativo reconstruido de DuPont resta todos los costes operativos presentados antes de ingresos de afiliadas y otros ingresos. Los pares reportan directamente beneficio operativo GAAP; esa diferencia de presentación debe acompañar cualquier visual. No se comparan beneficios de segmentos ni EBITDA con beneficios operativos consolidados. La tabla no sustituye un análisis completo de deuda, pensiones, NCI, litigios, adquisiciones ni flujo normalizado de cada par.
