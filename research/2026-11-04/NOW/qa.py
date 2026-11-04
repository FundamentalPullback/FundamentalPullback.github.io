import json,math,re
from pathlib import Path
P=Path(__file__).resolve().parent
load=lambda p:json.loads((P/p).read_text())
s=load('summary.json');m=load('model/results.json'); h=load('history/history.json'); pc=load('pros_cons.json');report=(P/'report.md').read_text(); checks=[]
def ck(name,value):checks.append({'check':name,'pass':bool(value)})
for case in ['bear','base','bull']:
 ck(case+' summary exact',s[case]==m[case]['valuePerShare'])
 ck(case+' ten years',len(m[case]['rows'])==10)
 for r in m[case]['rows']:
  ck(case+str(r['year'])+' cash identity',math.isclose(r['fcff'],r['nopat']+r['ppeDepreciation']-r['cashPpeCapexFloor']-r['netCommissionInvestment']-r['otherWcInvestment']-r['additionalGrowthInvestment'],abs_tol=1e-8))
ck('valuation checks',load('model/valuation_checks.json')['failed']==0)
ck('history checks',load('history/QA.json')['status']=='pass')
for k in ['pros','cons']:
 ck(k+' count',1<=len(pc[k])<=3)
 for n,p in enumerate(pc[k]):
  ck(k+str(n)+' evidence contiguous',p['evidence'] in report.split('\n\n'))
  ck(k+str(n)+' ES length',len(p['es'])<=320)
  ck(k+str(n)+' EN length',len(p['en'])<=360)
  if 'sourceUrl' in p:ck(k+str(n)+' source in evidence',p['sourceUrl'] in p['evidence'])
ck('calendar closed',not s['calendarGatePassed']);ck('entry closed',not s['stage35Approved']);ck('s2 missing',s['scannerStage2'] is None)
ck('scanner distinct',s['scanPrice']==123.73 and s['lastClose']==109.16)
ck('capital bridge',m['base']['capitalBridge']==-1345)
ck('GAAP EBIT primary',next(x['value'] for x in h if x['period']=='TTM-September-2026' and x['metric']=='ebit_gaap')==1493)
ck('NOW own comparable',math.isclose(load('comps/now_screen.json')['evBeforeAcquiredAmortAfterSbc'],56.182455483234705))
ck('no guessed CRM URL','000110852426000082' not in report)
ck('no private sources path', '/workspace/' not in report)
result={'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks}
(P/'QA.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['passed'],'package checks;',result['failed'],'failed')
assert result['failed']==0,[x for x in checks if not x['pass']]
