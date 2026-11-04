from pathlib import Path
import json,math
p=Path(__file__).resolve().parent;s=json.loads((p/'summary.json').read_text());r=(p/'report.md').read_text();v=json.loads((p/'model/results.json').read_text());iv=json.loads((p/'model/inverse.json').read_text());checks=[]
def check(x,label):
 assert x,label
 checks.append(label)
for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases']:check(s[k] is None,k+' null')
for k in ['entryApproved','stage3Complete','stage35Approved','latestCompletedEligible']:check(s[k] is False,k+' false')
for side in ['pros','cons']:
 check(1<=len(s[side])<=3,side+' count')
 for j,x in enumerate(s[side]):
  check(x['evidence'] in r,side+str(j)+' contiguous evidence')
  check(len(x['textEs'])<=320,side+str(j)+' ES length')
  check(len(x['textEn'])<=360,side+str(j)+' EN length')
check('{{' not in r,'all report placeholders resolved')
check(s['latestClose']==25.37 and s['scanPrice']==22,'separate scan/close')
check(s['scanStage2Current'] is None,'current technical unknown')
check(s['nextEvent']['date']=='2026-11-24' and s['nextEvent']['confirmed'],'official call date')
check(abs(v['base']['equityResidualPerShare']-11.498763141784051)<1e-10,'central11.50')
check(abs(v['bull']['equityResidualPerShare']-29.32983903066851)<1e-10,'favorable29.33')
check(v['bear']['equityResidualPerShare']<0 and v['bear']['conditionalPriceIfPositive'] is None,'deficit not price')
check(iv['fullyFundedInverseFirstYearFcff']<0 and iv['fullyFundedInverseExternalFundingNotModeled'],'inverse funding warning')
check(abs(iv['value']-25.37)<1e-8 and abs(iv['efficiencyAlternative']['value']-25.37)<1e-8,'both inverse solutions')
check('−6.676 M' in r and '4,08%' in r,'inverse caveats prominent')
check('NO se restan otra vez' in r,'lease no double count')
check('No hay mediana' in r,'no false relative target')
check('recompra anunciada' in r,'not executed buyback')
check('cap table' in r and 'proxy' in r,'capital limitation')
check('113,376445' in r,'dated cover count')
(p/'qa_results.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'package QA PASS')
