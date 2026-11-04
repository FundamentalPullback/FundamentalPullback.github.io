#!/usr/bin/env python3
from pathlib import Path
import json,math,re
P=Path(__file__).resolve().parent
s=json.loads((P/'summary.json').read_text()); m=json.loads((P/'model/results.json').read_text());p=json.loads((P/'pros_cons.json').read_text());v=json.loads((P/'valuation_checks.json').read_text());report=(P/'report.md').read_text()
checks=[]
def ck(name,ok):checks.append({'name':name,'pass':bool(ok)})
for n in ['bear','base','bull']:ck(n+' metadata',math.isclose(s[n],m['results'][n]['value'],abs_tol=1e-9))
ck('earnings unconfirmed',s['earningsDateConfirmed']==False);ck('calendar not passed',s['calendarGatePassed']==False);ck('scanner fixed',s['scanDate']=='2026-10-30' and s['scanPrice']==335.53);ck('regular close separate',s['lastCloseDate']=='2026-11-03' and s['lastClose']==344.28);ck('source link',s['lastCloseSource'] in report)
for typ in ['pros','cons']:
 ck(typ+' count',1<=len(p[typ])<=3)
 for i,x in enumerate(p[typ]):
  ck(f'{typ}{i} ES length',len(x['es'])<=320);ck(f'{typ}{i} EN length',len(x['en'])<=360);ck(f'{typ}{i} evidence exact paragraph',x['evidence'] in report.split('\n\n'));ck(f'{typ}{i} URL',not x.get('sourceUrl') or x['sourceUrl'] in report)
for x in v['checks']:ck('model '+x['name'],x['pass'])
ck('range ascending',s['sensitivityRange'][0]<s['sensitivityRange'][1]);ck('canada limitation','No es un modelo postventa limpio' in report);ck('not FCF','No es caja libre distribuible' in report);ck('WACC selected','no redondeo' in report);ck('license tail','2052' in report);ck('history exists',(P/'history/inputs.json').exists());ck('comps exists',(P/'comps/comps_inputs.json').exists())
out={'passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks}
(P/'qa.json').write_text(json.dumps(out,indent=2)+'\n');print(f"{out['passed']}/{out['total']} checks pass");assert out['passed']==out['total']
