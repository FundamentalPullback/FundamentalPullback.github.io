# FRPT — comprobación posterior a la conferencia Q3 2026

**Corte: 4 de noviembre de 2026, 15:04 UTC.** Complemento de A189, no reemplazo del modelo ni nueva autorización de entrada. Precio de referencia conservado: cierre regular del 3 de noviembre, $69.60; no se presenta como cotización intradía.

## Resultado

La comprobación posterior a la conferencia está terminada con la evidencia pública accesible. **No encontramos una corrección material que justifique cambiar los valores A189: adverso $10.92, central $44.38 y favorable $84.79.** La lectura nueva refuerza que una caída puntual de capex no representa inversión mínima permanente. Añadimos sensibilidades explícitas y conservamos la distinción entre negocio atractivo, precio razonable bajo hipótesis más exigentes y señal de entrada todavía no validada.

## Qué se pudo verificar

Los [comentarios preparados oficiales](https://investors.freshpet.com/static-files/c7c74ec5-1ed3-410b-8411-deca2f2f769e) y la [presentación oficial](https://investors.freshpet.com/static-files/f82d5c97-c5cc-4996-bcf7-5114ee716771) siguen idénticos a los incorporados al informe. Sus SHA-256 son, respectivamente, 4a2c403d8f970da788d89a9af316aa39af760994d68e40ff09e91d72f64d1232 y e6ea4bbc46a10761874c223bbd2a44676af3437f39be4098e8ca120a24d5c52c. La guía oficial continúa: ventas FY26 +12–13%, EBITDA ajustado $215–220m, capex $125–150m; objetivo EBITDA ajustado FY27 20–22%, con cautela hacia la mitad inferior sin alivio de inflación.

Se leyó la transcripción completa de la llamada, incluido el turno de preguntas y cierre, publicada por **Benzinga y distribuida por [Webull](https://www.webull.com.au/news-detail/15865906545714176)**. Es una transcripción automática de terceros, no una transcripción certificada por el emisor. Sus cifras preparadas coinciden con las fuentes oficiales. El enlace oficial de audio devuelve un error del proveedor tanto en navegador normal como en lectura directa; no se eludió esa restricción ni se afirma haber escuchado el audio. El índice SEC consultado todavía no mostraba el 10-Q de este trimestre.

### Aclaraciones del Q&A, atribuidas a dirección

- Capex de aproximadamente $150m sigue siendo una referencia razonable al crecimiento actual mientras se revisa la capacidad disponible; no constituye guía formal FY27.
- El cliente con menores compras relativas al consumo opera con mayor rotación. No se prometió reposición inmediata de inventario en Q4.
- La mejora tecnológica de unos 100 puntos básicos en 2027 es total frente al punto de partida, no 100 adicionales a los 35 previstos para 2026.
- Aproximadamente dos tercios del incremento logístico corresponden a transporte y un tercio a combustible. Los aumentos selectivos de precio buscan preservar volumen.
- La empresa afirma no observar deterioro de ventas o retención donde entraron nuevos competidores. Es una observación de dirección, no verificación independiente.
- El negocio directo representa menos del 2% de ventas; no debe confundirse con todo el comercio electrónico.

Estas aclaraciones proceden de la transcripción enlazada. Las limitaciones de atribución y posible error automático siguen vigentes.

## Prueba de inversión: cálculo propio reproducible

El modelo original central usa mínimos de inversión de $140m/$130m en los dos primeros años rodantes. No son una previsión oficial de los ejercicios 2027 y 2028. Manteniendo los demás supuestos:

| Prueba | Valor por acción |
|---|---:|
| Central A189, sin cambios | $44.38 |
| Mínimo de $150m en años 1–2, capacidad integrada | $44.27 |
| Mínimo de $150m en años 1–3, capacidad integrada | $44.16 |
| Mínimo de $150m todos los años, capacidad integrada | $43.18 |
| Mínimo de $150m en años 1–2, sin crédito por más capacidad | $43.86 |
| Mínimo de $150m en años 1–3, sin crédito por más capacidad | $43.25 |
| Mínimo de $150m todos los años, sin crédito por más capacidad | $42.99 |

La primera familia reconoce capacidad comprada por inversión superior al mantenimiento y, por ello, menor necesidad posterior de expansión. La segunda es una superposición conservadora de coste: descuenta el exceso de capex sin conceder capacidad ni desplazamiento de inversión futura. Es una sensibilidad de coste, no un escenario operativo integrado adicional. No equivale a una banda estadística de confianza.

La sensibilidad más prudente no acerca el central al precio de referencia. Tampoco demuestra que el escenario favorable sea imposible. El caso alternativo conjunto ya publicado, con crecimiento cercano al 10%, mayor margen y menor coste de capital, sigue valiendo aproximadamente $68.34. La decisión depende de esas hipótesis y de la evidencia futura, no de un descuento universal del 15%.

## Alcance residual

No se dispone todavía del detalle Q3 de altas no monetarias de finance leases, premios pendientes ni un calendario preciso de mantenimiento/expansión FY27. El Q&A no aporta un desglose suficiente para sustituir esas incertidumbres por ceros. El informe previo ya las identifica y cuantifica donde corresponde. La comprobación posterior a la llamada queda cerrada; cualquier actualización futura debe partir del 10-Q o de nueva evidencia, no de fingir hechos no publicados.

Archivos reproducibles: check_call_sensitivities.py y call_sensitivities.json. El modelo original no se modifica.
