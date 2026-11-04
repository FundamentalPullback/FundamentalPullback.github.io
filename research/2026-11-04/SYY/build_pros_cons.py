import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;paras=(P/'report.md').read_text().split('\n\n')
def p(start):return next(x for x in paras if x.startswith(start))
x={'ticker':'SYY','pros':[{'es':'La escala de compras y la densidad logística pueden respaldar márgenes y retornos. JRD añade un formato de mayor margen, pero no una expansión sin fricciones.','en':'Purchasing scale and route density can support margins and returns. JRD adds a higher-margin format, but integration is not frictionless.','evidence':p('La tesis favorable')}],'cons':[{'es':'El FCF anunciado de JRD, unos1.900 millones, es EBITDA ajustado menos capex. Excluye impuestos, intereses y circulante; no equivale a caja distribuible ni FCFF.','en':'JRD headline FCF of roughly $1.9bn is adjusted EBITDA less capex. It excludes tax, interest and working capital and is not distributable cash or FCFF.','evidence':p('Los aproximadamente 1.900')},{'es':'La operación sigue pendiente de condiciones regulatorias. Financiación completada no equivale a aprobación ni cierre; la comisión de ruptura1.164 millones depende de la ruta contractual.','en':'The deal remains subject to regulatory conditions. Completed financing is not approval or closing; the $1,164m termination fee depends on the contractual termination route.','evidence':p('La última fuente primaria')} ]}
for k in ['pros','cons']:
 for row in x[k]:
  urls=re.findall(r'https://[^)\s]+',row['evidence'])
  if urls:row['sourceUrl']=urls[0]
(P/'pros_cons.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
