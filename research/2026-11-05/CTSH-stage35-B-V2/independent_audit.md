# Auditoría independiente · CTSH, vía B prospectiva

**Dictamen: lista para entregar como propuesta de paper trading, con condiciones pendientes explícitas. No entrada, orden ni ejecución aprobada.**

Informe revisado antes de la apertura regular del 5 noviembre 2026. La elección B reemplaza la propuesta A como única ficha activa; no modifica la valoración A268 ni el reglamento general.

## Resultado de la revisión

- La corrección distingue requisitos del plan de decisiones del analista. La visita a la antigua zona, vela verde y volumen especial ya no se presentan como obligaciones universales. El techo 65,78 se reconoce como convención sobre el último cierre regular conocido, no nuevo valor ni frontera estadística.
- La referencia 65,26 es el máximo del 29 octubre ya recuperado. La futura vela prueba persistencia, no una ruptura nueva de 66,77. La falta de ventaja demostrada de este setup y del escalonado se declara expresamente.
- Se elige ex ante la primera vela completa regular con cierre >65,26 y ≤65,78, entre 09:45 y 15:45 EST. Solo puede usarse su ventana siguiente de quince minutos. No se fuerzan primera vela del día, visita a 62,50, volumen especial o vela verde.
- El suelo previo al fill coincide con 65,26. M=61,55, S=61,20 y ese suelo táctico tienen funciones distintas. La igualdad a M no rompe estructura; precio≤S, incluido gap, activa salida manual después de entrar. El suelo táctico no se transforma en stop protector.
- DAY no caduca a los quince minutos: se exige vigilancia y confirmación de cancelación. No se presume un fill por tocar un nivel. Una orden CTSH pendiente o incierta impide duplicarla; otras compañías se concilian por separado. La ficha no rearma otra oportunidad después de fallar la primera.
- Una negociación regular >66,50 exige revisión registrada antes de reactivar. Las alternativas A y B diaria permanecen inactivas. No se admite seleccionar temporalidad después del resultado ni atravesar resultados por esta ficha.
- El tamaño se calcula al peor precio permitido. Usar el techo inicial B es una decisión distinta de cambiar precio. El tramo completo solo se presenta como posible campaña posterior o contrafactual de investigación, no primera entrada autorizada.
- R ilustrativo=4,58 y +2R=74,94 concilian. El FCFF no es un take-profit. Se conserva la prioridad del stop manual, salidas completas, trailing previo y parcial única de Stage 4.

## Pruebas y límites

Pasan **22 controles de reglas y coherencia**, **25 comprobaciones sintéticas de límites/horarios**, **14 cálculos privados independientes** y la reproducción pública de **2.503 comprobaciones numéricas**. Las pruebas sintéticas no son datos de mercado, señales ni backtest. La reproducción comprueba aritmética, no capacidad predictiva.

Siguen pendientes una señal futura real, datos operativos actuales, reservas históricas y riesgo agregado completos, precio/spread ejecutables y posibilidad efectiva de vigilancia/cancelación. El dictamen permite entregar investigación prospectiva; no cierra esos requisitos.

La comparación entre parcial y completa debe separar exposición de ventaja estratégica, predefinir añadidos/salidas e incluir efectivo, costes, no-fills y gaps. No se ha probado que el escalonado sea superior ni que deba trasladarse a capital real. No se revisó una captura renderizada del HTML en esta auditoría.

## Integridad

SHA-256 del informe: `916b3617b4d62e2e561b7f498e83279073ea2699cc68de9b807630b6186dcc5b`.

SHA-256 HTML: `876449a3f5745117806c1b579167c3d992e4689cc8750d5bec7eeaa13be48d92`.

SHA-256 datos: `fa19ac247c086e18b4ba4356318720ffb6658582d8bfa4da881d262a6d7dc8b0`.

El registro completo está en `independent_audit.json`. Los cálculos de cuenta permanecen separados y privados. No incluir archivos de construcción o QA que contengan datos personales de la cuenta en una publicación externa.

## Actualización auditada posterior

La nota de cotización y la corrección de límites temporales están verificadas en `delta_audit.md`. El informe actual tiene SHA-256 `f6e362172cd049fa52bae5e2b051010ef37eb5ffadb62759440f1afa65789a68`; los hashes anteriores documentan la versión original conservada. No se modificaron valoración, niveles ni aprobación operativa.
