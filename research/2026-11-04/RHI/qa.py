import pathlib,json,subprocess,sys
from model import *
P=pathlib.Path(__file__).parent;checks=[]
def check(n,b):
 checks.append({'name':n,'pass':bool(b)})
 assert b,n
m=json.loads((P/'model_results.json').read_text());s=json.loads((P/'summary.json').read_text());r=(P/'report.md').read_text()
for name,result in m['scenarios'].items():
 check(name+' reproduced',calculate(SCENARIOS[name])==result)
 for row in result['rows']:
  check(name+str(row['year'])+' FCFF',abs(row['nopat']-row['reinvestment']-row['fcff'])<1e-8)
  check(name+str(row['year'])+' investment funded',row['reinvestment']+1e-8>=max(row['net_reinvestment_floor'],row['economic_growth_reinvestment']))
  check(name+str(row['year'])+' calendar',abs(row['pv']-row['fcff']/(1+SCENARIOS[name]['wacc'])**(row['year']-2026+57/365))<1e-8)
 check(name+' terminal floor',result['terminal_reinvestment']>=result['terminal_reinvestment_floor'])
 check(name+' capital bridge',abs(result['enterprise_value']+CASH-150-result['equity_value_before_unquantified_contingency'])<1e-8)
 check(name+' summary',s[name]==result['value'])
check('original scan',s['scanPrice']==41.87 and s['scanDate']=='2026-10-28' and s['lastClose']==43.73)
check('explicit legal uncertainty','no puede estimar un rango de pérdida' in r)
check('no incomplete peers placeholder','Contraste pendiente'not in r)
check('margin investment stress',calculate(BASE,charge_margin_growth=True)['value']<calculate(BASE)['value'])
for n,item in enumerate(json.loads((P/'pros_cons.json').read_text())):
 check(str(n)+' exact evidence',item['evidence'] in r)
 check(str(n)+' ES length',len(item['text_es'])<=320)
 check(str(n)+' EN length',len(item['text_en'])<=360)
 if item.get('sourceUrl'):check(str(n)+' source',item['sourceUrl']in r)
check('history validation',subprocess.run([sys.executable,str(P/'history/validate.py')],capture_output=True).returncode==0)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2));print('PASS',len(checks))
