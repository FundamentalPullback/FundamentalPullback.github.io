from pathlib import Path
import json,math
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());report=(P/'report.md').read_text();checks=[]
def ck(n,a):assert a,n;checks.append(n)
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' null',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved']:ck(k+' false',s[k] is False)
for n in r:ck(n+' numeric component',math.isclose(s['conditionalIndustrialScenarios'][n],r[n]['conditionalIndustrialPerShare']))
ck('future calendar unknown',s['nextEvent']['date'] is None and not s['nextEvent']['confirmed'])
ck('scanner original',s['scanPrice']==123.84 and s['scanDate']=='2026-10-14')
ck('price date separate',s['latestClose']==96.79 and s['latestCloseDate']=='2026-11-03')
ck('current technical unknown',s['scanStage2Current'] is None)
for side in ['pros','cons']:
 ck(side+' size',1<=len(s[side])<=3)
 for i,a in enumerate(s[side]):
  ck(f'{side}{i} ES',len(a['textEs'])<=320);ck(f'{side}{i} EN',len(a['textEn'])<=360);ck(f'{side}{i} contiguous',a['evidence'] in report.split('\n\n'));ck(f'{side}{i} source',a['sourceUrl'] in report)
for phrase in ['17,20','52,82','113,93','13,95','50,57','113,40','FICT','infrautilización','55 M','2,234887','56,397','200%','no aprobación','no es un cap table','40,13','3,81','25,80']:
 ck('report '+phrase,phrase in report)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2,ensure_ascii=False)+'\n');print('PASS',len(checks))
