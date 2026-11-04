from pathlib import Path
import json,math
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());t=(P/'report.md').read_text();checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' null',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved']:ck(k+' false',not s[k])
ck('No current Stage2',s['scanStage2Current'] is None);ck('Dates separate',s['scanDate']=='2026-10-13' and s['latestCloseDate']=='2026-11-03');ck('No invented earnings',s['nextEvent']['date'] is None)
for side in ['pros','cons']:
 ck(side+' count',1<=len(s[side])<=3)
 for i,a in enumerate(s[side]):
  ck(side+str(i)+' exact evidence',a['evidence'] in t);ck(side+str(i)+' source',a['sourceUrl'] in t);ck(side+str(i)+' text lengths',len(a['textEs'])<=320 and len(a['textEn'])<=360)
for n,a in r.items():
 ck(n+' 10years',len(a['rows'])==10);ck(n+' summary sync',s['counterfactualScenarios'][n]==a['counterfactualPerShare']);ck(n+' displayed',f"{a['counterfactualPerShare']:,.2f}" in t);ck(n+' current total null',a['currentTotalFairValue'] is None)
for phrase in ['contrafactual','no hay ratio mínimo','no es conciliación exacta','461','486','sin reconciliación completa','cum-dividend','no es un precio objetivo','No se promedian','Hubbell','COL']:
 ck(phrase,phrase in t)
ck('no unfinished comps','en preparación' not in t)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'labels':checks},indent=2,ensure_ascii=False)+'\n');print(len(checks),'package QA PASS')
