import json,pathlib,math,subprocess,sys
from model import *
P=pathlib.Path(__file__).parent;checks=[]
def check(name,ok):
 checks.append({'name':name,'pass':bool(ok)})
 if not ok:raise AssertionError(name)
m=json.loads((P/'model_results.json').read_text());s=json.loads((P/'summary.json').read_text());report=(P/'report.md').read_text();v=json.loads((P/'valuation_checks.json').read_text())
for name,result in m['scenarios'].items():
 check(name+' reproduced',calculate(SCENARIOS[name])==result)
 for row in result['rows']:
  check(name+str(row['year'])+' cash identity',abs(row['nopat']-row['reinvestment']-row['fcff'])<1e-8)
  check(name+str(row['year'])+' reinvestment funded',row['reinvestment']+1e-8>=max(row['net_reinvestment_floor'],row['positive_nopat_growth_reinvestment']))
  check(name+str(row['year'])+' ordinaryDA not acquired',row['ordinary_da']/row['revenue']==SCENARIOS[name]['ordinary_da'] or abs(row['ordinary_da']/row['revenue']-SCENARIOS[name]['ordinary_da'])<1e-12)
 check(name+' terminal floor',result['terminal_reinvestment']+1e-8>=result['terminal_reinvestment_floor'])
 check(name+' enterprise/equity',abs(result['enterprise_value']-result['claims']-result['equity_value'])<1e-8)
 check(name+' summary',s[name]==result['usd_per_adr'])
check('A111 rounded reconstruction',round(reconstruct_a111()['usd_per_adr'],2)==29.59)
check('GBP FX division',abs(FX-1.1179/.83358)<1e-12)
check('no scan overwrite',s['scanPrice']==39.32 and s['lastClose']==39.40)
check('capital bridge',8733==8906-220+73-26)
check('pension not called net liability','esos 149 no son pensiones netas' in report)
for n,item in enumerate(json.loads((P/'pros_cons.json').read_text())):
 check(str(n)+' contiguous evidence',item['evidence']in report)
 check(str(n)+' ES length',len(item['text_es'])<=320)
 check(str(n)+' EN length',len(item['text_en'])<=360)
 if item.get('sourceUrl'):check(str(n)+' url',item['sourceUrl']in report)
for key in ['margin_at_growth5_5','growth_at_margin36_5']:check('reverse '+key,abs(v['reverse'][key]['value']-39.40)<1e-8)
check('missing future earnings not invented','next earnings date unconfirmed'in s['nextEvent'])
r=subprocess.run([sys.executable,str(P/'history/validate.py')],capture_output=True,text=True);check('history validation',r.returncode==0)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2));print('PASS',len(checks))
