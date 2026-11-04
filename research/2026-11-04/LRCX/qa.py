from pathlib import Path
import json,math
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=(P/'report.md').read_text();m=json.loads((P/'model/results.json').read_text());tests=[]
def ck(n,c):tests.append({'name':n,'pass':bool(c)});assert c,n
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' null',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved','latestCompletedEligible']:ck(k+' false',s[k] is False)
ck('current Stage2 unknown',s['scanStage2Current'] is None);ck('next earnings unknown',s['nextEvent']['date'] is None and s['nextEvent']['confirmed'] is False)
ck('original scan',s['scanPrice']==318.84 and s['scanDate']=='2026-10-09');ck('latest close',s['latestClose']==221.43 and s['latestCloseDate']=='2026-11-04')
for k,d in m.items():
 ck(k+' conditional equal',abs(s['conditionalDcfCases'][k]-d['perShareConditional'])<1e-10);ck(k+' ten years',len(d['rows'])==10);ck(k+' finite',math.isfinite(d['perShareConditional']))
for side in ['pros','cons']:
 ck(side+' count',1<=len(s[side])<=3)
 for n,v in enumerate(s[side]):
  ck(f'{side}{n} exact evidence',v['evidence'] in r);ck(f'{side}{n} contiguous paragraph','\n\n' not in v['evidence']);ck(f'{side}{n} Spanish limit',len(v['textEs'])<=320);ck(f'{side}{n} English limit',len(v['textEn'])<=360)
for k,u in s['sources'].items():ck(k+' source in report',u in r)
ck('no URL placeholder','URLPLACEHOLDER' not in r);ck('no internal paths','/workspace/' not in r);ck('current price not inferred from scanner',s['scanPrice']!=s['latestClose'])
(P/'qa.json').write_text(json.dumps({'passed':len(tests),'checks':tests},indent=2)+'\n');print(len(tests),'package QA PASS')
