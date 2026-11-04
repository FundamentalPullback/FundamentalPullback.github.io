from pathlib import Path
import json,math
P=Path(__file__).parent;s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());text=(P/'report.md').read_text();c=[]
def ck(n,b):assert b,n;c.append(n)
for k in ['fairValue','fairValueTotal','bear','base','bull']:ck(k+' null',s[k] is None)
for k in ['entryApproved','stage3Complete','stage35Approved']:ck(k+' false',s[k] is False)
for n,a in r.items():ck(n+' conditional residual',math.isclose(s['standaloneCapitalResidualCases'][n],a['standaloneResidualPerShare']))
ck('negative residual not stock price',s['negativeResidualsAreNotStockPrices'])
ck('merger illustration',math.isclose(s['conditionalMergerIllustration'],27+.4*54.43))
ck('calendar not certified',not s['nextEvent']['confirmed'] and s['nextEvent']['date'] is None)
ck('scan separate',s['scanPrice']==48.36 and s['latestClose']==43.87)
ck('current technical unknown',s['scanStage2Current'] is None)
for side in ['pros','cons']:
 ck(side+' size',1<=len(s[side])<=3)
 for i,a in enumerate(s[side]):
  ck(f'{side}{i}ES',len(a['textEs'])<=320);ck(f'{side}{i}EN',len(a['textEn'])<=360);ck(f'{side}{i}evidence',a['evidence'] in text.split('\n\n'));ck(f'{side}{i}source',a['sourceUrl'] in text)
for word in ['103,868','31,618','2.159,458','3,947','223,62','48,772','17,5','SBC','2031','no valor','sin aprobación','cap','54','null']:
 ck('report '+word,word in text)
(P/'qa.json').write_text(json.dumps({'passed':len(c),'checks':c},indent=2,ensure_ascii=False)+'\n');print('PASS',len(c))
