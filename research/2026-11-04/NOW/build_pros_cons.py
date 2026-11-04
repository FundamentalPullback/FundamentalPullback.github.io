import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
paragraphs=(P/'report.md').read_text().split('\n\n')
def para(start):return next(p for p in paragraphs if p.startswith(start))
out={'ticker':'NOW','pros':[{'es':'Suscripción Q3 +21% y cRPO +20,5% respaldan la demanda de la plataforma. El objetivo de ACV de IA no equivale a ingresos ni caja reconocidos.','en':'Q3 subscription revenue rose21% and cRPO20.5%, supporting platform demand. The AI ACV target is not recognized revenue or cash.','evidence':para('ServiceNow integra')}], 'cons':[{'es':'SBC TTM2.340 millones sigue siendo un coste económico. CFO menos capex y SBC deja2.410 millones, una aproximación de propietario, no FCFF exacto.','en':'TTM SBC of $2,340m remains an economic cost. CFO less capex and SBC leaves $2,410m, an owner-cash proxy rather than exact FCFF.','evidence':para('SBC de P&L')},{'es':'DCF central56,39 USD frente a cierre109,16. El favorable125,93 requiere crecimiento más duradero, mayores márgenes después de SBC y reinversión eficiente.','en':'Base DCF $56.39 versus $109.16 close. Bull $125.93 requires longer growth, higher after-SBC margins and efficient reinvestment.','evidence':para('El modelo de FCFF')}]}
for k in ['pros','cons']:
 for p in out[k]:
  urls=re.findall(r'https://[^)\s]+',p['evidence'])
  if urls:p['sourceUrl']=urls[0]
(P/'pros_cons.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
