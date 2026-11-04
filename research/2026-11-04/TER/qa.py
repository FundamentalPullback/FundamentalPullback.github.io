from pathlib import Path
import json
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());t=(P/'report.md').read_text();checks=[]
def ck(n,c):
 assert c,n
 checks.append(n)
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' null',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved']:ck(k+' false',not s[k])
ck('current technical not old scanner',s['scanStage2Current'] is None and s['scanStage2Historical'])
ck('prices separate',s['scanPrice']==386.55 and s['scanComparisonClose']==383.85 and s['latestClose']==269.35)
ck('TER no confirmed date',s['nextEvent']['date'] is None and not s['nextEvent']['confirmed']);ck('investee only date',s['investeeNextEvent']['company']=='Technoprobe' and s['investeeNextEvent']['date']=='2026-11-11')
for side in ['pros','cons']:
 ck(side+' count',1<=len(s[side])<=3)
 for i,a in enumerate(s[side]):
  ck(side+str(i)+' exact contiguous evidence',a['evidence'] in t);ck(side+str(i)+' link in report',a['sourceUrl'] in t);ck(side+str(i)+' lengths',len(a['textEs'])<=320 and len(a['textEn'])<=360)
for n,a in r.items():
 ck(n+' ten years',len(a['rows'])==10);ck(n+' summary equality',s['conditionalHybridScenarios'][n]==a['hybridConditionalPerShare']);ck(n+' report formatted',f"{a['hybridConditionalPerShare']:,.2f}" in t);ck(n+' total not certified',a['certifiedTotalFairValue'] is None)
for phrase in ['precio por fórmula','no se deducen otros 7,2 mecánicamente','bloqueo financiero original de 36 meses no sigue vigente','después de SBC','Compromiso posterior con FormFactor','no como previsión empresarial','No significativo']:ck(phrase,phrase in t)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2,ensure_ascii=False)+'\n');print(len(checks),'package QA PASS')
