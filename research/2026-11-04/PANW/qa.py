from pathlib import Path
import json,math
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());t=(P/'report.md').read_text();checks=[]
def ck(n,c):
 assert c,n
 checks.append(n)
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' unresolved',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved']:ck(k+' false',not s[k])
ck('Stage2 missing',s['scanStage2'] is None);ck('distinct prices',s['scanPrice']==377.95 and s['latestClose']==350.2 and s['scanComparisonClose']==380.57)
ck('confirmed calendar',s['nextEvent']['date']=='2026-11-18' and s['nextEvent']['confirmed'])
for side in ['pros','cons']:
 ck(side+' count',1<=len(s[side])<=3)
 for i,a in enumerate(s[side]):
  ck(side+str(i)+' exact contiguous',a['evidence'] in t)
  ck(side+str(i)+' source present',a['sourceUrl'] in t)
  ck(side+str(i)+' lengths',len(a['textEs'])<=320 and len(a['textEn'])<=360)
for n,a in r.items():
 ck(n+' ten years',len(a['rows'])==10)
 ck(n+' summary',s['conditionalDcfScenarios'][n]==a['conditionalValuePerShare'])
 ck(n+' not current capital',not a['actualCapitalCertified'])
 ck(n+' report formatted',f"{a['conditionalValuePerShare']:,.2f}" in t)
for phrase in ['No se ha establecido un conjunto homogéneo','Las dos anclas tienen diferente alcance','no un número reconciliado','no obligación incremental neta demostrada','sin añadir también toda la conversión','26,31 puntos','Stage 2 está vacío']:ck(phrase,phrase in t)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2,ensure_ascii=False)+'\n');print('package QA',len(checks),'PASS')
