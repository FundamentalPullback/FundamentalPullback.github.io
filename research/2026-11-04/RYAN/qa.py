import json
from pathlib import Path
p=Path(__file__).parent;j=lambda f:json.loads((p/f).read_text());s=j('summary.json');r=(p/'report.md').read_text();n=0
for k in ['fairValue','fairValueTotal','bear','base','bull']:assert s[k] is None;n+=1
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:assert s[k] is False;n+=1
for d in s['pros']+s['cons']:assert d['evidence'] in r;assert len(d['es'])<=320 and len(d['en'])<=360;n+=3
m=j('model/results.json');i=j('model/inputs.json')
for c in m['cases'].values():
 assert len(c['rows'])==10;assert c['terminal']['reinvestment']>=c['terminal']['physicalFloor'];n+=2
 assert abs(c['conditionalClassAResidual']-((c['ev']+c['opcoBridge'])/c['allEconomicUnitsProxy']+c['parentBridge']/c['classAProxy']))<1e-7;n+=1
 assert c['allEconomicUnitsProxy']>c['classAProxy'];n+=1
assert s['scanPrice']!=s['lastClose'];n+=1
assert s['nextEarningsConfirmed'] is None;n+=1
assert m['cases']['bear']['conditionalClassAResidual']<0;n+=1
assert i['opcoCash']+i['parentCash']==168.811;n+=1
for inv in ['inverseFinanced','inverseEfficiency']:assert abs(m[inv]['residual'])<1e-7 and m[inv]['monotonicIntervals']==1000;n+=1
(p/'qa_results.json').write_text(json.dumps({'checks':n,'allPass':True},indent=2)+'\n')
