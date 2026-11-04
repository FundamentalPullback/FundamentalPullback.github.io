import json,math
from pathlib import Path
P=Path(__file__).resolve().parent;load=lambda f:json.loads((P/f).read_text());s=load('summary.json');m=load('model/results.json');pc=load('pros_cons.json');report=(P/'report.md').read_text();checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' intentionally null',s[k] is None)
for k in ['stage3Complete','stage35Approved','entryApproved','technicalGatePassed','calendarGatePassed']:ck(k+' not passed',not s[k])
for c,r in m.items():
 ck(c+' failure summary',s['conditionalRegulatoryFailure'][c]==r['conditionalFailureValuePerShare']);ck(c+' close summary',s['conditionalImmediateClose'][c]==r['conditionalImmediateCloseValuePerShare']);ck(c+' seller shares not current',r['conditionalImmediateCloseShares']==585.5)
 for who in ['syy','jrd']:ck(c+who+' ten years',len(r[who]['rows'])==10)
ck('model QA',load('model/valuation_checks.json')['failed']==0);ck('JRD QA',load('jrd/QA.json')['failed']==0)
for k in ['pros','cons']:
 ck(k+' count',1<=len(pc[k])<=3)
 for n,p in enumerate(pc[k]):
  ck(k+str(n)+' exact paragraph',p['evidence'] in report.split('\n\n'));ck(k+str(n)+' ES length',len(p['es'])<=320);ck(k+str(n)+' EN length',len(p['en'])<=360)
  if 'sourceUrl'in p:ck(k+str(n)+' sourceURL in evidence',p['sourceUrl'] in p['evidence'])
ck('no workspace paths','/workspace/' not in report);ck('source cutoffs',s['scanPrice']==81.74 and s['lastClose']==74.11);ck('historical S2 preserved',s['scannerStage2Literal']=='Sí');ck('contract fundamental value null',all(v['totalCurrentFairValue'] is None for v in m.values()))
r={'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks};(P/'QA.json').write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],'package checks',r['failed'],'failed');assert not r['failed'],[x for x in checks if not x['pass']]
