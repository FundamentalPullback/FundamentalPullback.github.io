# PANW: comparación operativa con FTNT y CHKP

Corte: 4 de noviembre de 2026. USD millones, salvo ratios. Paquete de apoyo factual, sin recomendación ni precio objetivo. Se reutilizan cifras y extractos acotados de la investigación FTNT completada hoy; no se incluyen filings completos. Fuentes primarias, filas y columnas: `inputs.json`; matices y cronología: `SOURCE_CONTEXT.md`.

## Lectura principal

| Último trimestre publicado | PANW FY26 Q4 | FTNT 2026 Q3 | CHKP 2026 Q3 |
|---|---:|---:|---:|
| Inicio | 1 mayo | 1 julio | 1 julio |
| Fin | 31 julio | 30 septiembre | 30 septiembre |
| Ingresos | 3.410,0 | 2.078,4 | 669,8 |
| EBIT GAAP, SBC retenida | 172,0 | 704,3 | 177,2 |
| Margen EBIT GAAP | 5,0 % | 33,9 % | 26,5 % |
| CFO | 1.357,0 | 946,0 | 264,3 |
| Inversión descontada en FCF base | 103,0 | 64,2 | 6,4 |
| FCF antes de ajustes corporativos | 1.254,0 | 881,8 | 257,9 |
| SBC del estado de flujos | 460,0 | 80,1 | 54,8 |
| SBC / ingresos | 13,5 % | 3,9 % | 8,2 % |
| Ajuste corporativo al FCF | +35,0 | −17,0 | 0,0 |
| FCF corporativo tras ajustes | 1.289,0 | 864,8 | 257,9 |
| FCF base menos SBC, sensibilidad | 794,0 | 801,7 | 203,1 |

FTNT es referencia de plataforma de seguridad y appliances; CHKP de seguridad de red y rentabilidad/caja. Son referencias operativas secundarias, no un conjunto suficiente para fijar el múltiplo de PANW: mezcla de producto, escala de plataforma, crecimiento adquirido y calendarios difieren. No se aplican medias ni medianas para un precio objetivo.

## Interpretación y límites decisivos

1. PANW no ha publicado todavía su trimestre terminado el 31 de octubre. El calendario reutilizado anuncia resultados el 18 de noviembre. Su Q4 FY26 es mayo–julio. Los márgenes no son simultáneos y la estacionalidad de cobros puede distorsionar una comparación de caja trimestral.
2. PANW incluye Chronosphere desde enero y CyberArk desde febrero, además de Koi y Portkey. Embrace y Console cerraron después de julio y no están en FY26. No llamar orgánico al crecimiento total. CHKP también adquirió negocios; ambos trimestres FTNT incluyen Linksys, pero eso no demuestra organicidad.
3. PANW: SBC de flujos 460 = FY 1.774 menos 9M 1.314. No confundir con 487 de cargos operativos relacionados con SBC. EBIT GAAP ya retiene SBC. La sensibilidad FCF menos SBC no es FCFF, ni un coste en efectivo publicado, ni se vuelve a restar en el DCF que ya retiene SBC.
4. PANW descuenta compras de propiedad, equipo y otros activos. El subtotal 103 se mantiene completo; no se declara cero software. No hay un importe trimestral de software capitalizado en efectivo separado en las tablas revisadas. El aumento del saldo neto y su amortización no permiten reconstruirlo con precisión. FCF ajustado añade 7 de activos corporativos y 28 de costes de adquisición; son distintos del precio pagado por adquisiciones.
5. CHKP descuenta PPE, arrendamientos prepagados y software. En Q3 2025 pagó 159,9 por un arrendamiento prepagado, de modo que el crecimiento bruto de FCF no demuestra la misma mejora recurrente. En Q3 2026 un beneficio de subvenciones de 25 reduce I+D: EBIT sin ese beneficio, como sensibilidad aislada, sería 152,2 (22,7 %). Reconocimiento contable no equivale a cobro confirmado.
6. FTNT resta 17 de ingreso de escrow para pasar de CFO menos PPE 881,8 a FCF corporativo 864,8. La dirección de ajuste es opuesta a los addbacks de PANW.
7. La comparación mantiene EBIT GAAP para todos. No aplica una amortización adquirida normalizada común ni una ventaja fiscal automática. El modelo PANW que devuelve amortización adquirida debe mostrar esa conciliación separadamente; no comparar su margen ajustado contra EBIT GAAP de pares como si fueran equivalentes.

## Valoración: no acreditada en este paquete

No se publican EV/ventas ni EV/EBIT entre los tres. Falta un juego consistente de precios de cierre 3 de noviembre, acciones contemporáneas, deuda/caja y denominadores TTM para todos, especialmente CHKP. No se anualiza un trimestre ni se sustituye capitalización por EV.

Los insumos existentes de FTNT usan cierre 128,11 del 3 de noviembre y capital de septiembre; 742,6 millones es promedio diluido trimestral, no acciones básicas al cierre. PANW tiene referencia 350,20 del 3 de noviembre facilitada por el trabajo principal, capital de julio, acciones del 9 de octubre y adquisiciones posteriores a julio. Además, su convertible tiene componente económico dependiente del precio y capped calls. Esas fechas y bases no acreditan por sí solas un EV contemporáneo comparable. Los precios aquí son referencias heredadas, no una verificación independiente realizada por este paquete.

## Reproducción offline

Ejecutar `python enrich.py` con Python 3 estándar desde cualquier directorio. Regenera las tablas históricas de 10 periodos, los tres registros trimestrales seleccionados y `checks.json`. No realiza descargas. `manifest.sha256` permite verificar integridad con `sha256sum -c manifest.sha256` desde esta carpeta.

- `latest_quarter_comparison.json` y `.csv`: tres trimestres, ratios y crecimientos derivados, sin valoración.
- `operating_comparables.json` y `.csv`: periodos originales; no comparar FY PANW con 9M CHKP como duraciones equivalentes.
- `inputs.json`: cifras, fuentes y mapa de evidencia.
- `excerpts/`: extractos seleccionados necesarios; no filings completos.
- `checks.json`: aritmética, fechas y distinción de SBC. PASS no certifica normalización económica, autenticidad independiente ni cierre integral de diligencia.
