import json
from pathlib import Path
p=Path(__file__).parent;j=lambda f:json.loads((p/f).read_text());s=j('summary.json');r=(p/'report.md').read_text();n=0
for k in ['fairValue','fairValueTotal','bear','base','bull']:assert s[k] is None;n+=1
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:assert s[k] is False;n+=1
for d in s['pros']+s['cons']:assert d['evidence'] in r;assert len(d['es'])<=320 and len(d['en'])<=360;n+=3
m=j('model/results.json');h=j('history/history.json');b=j('capital/verified.json')
for c in m['cases'].values():
 assert len(c['rows'])==10;assert abs(c['conditionalResidual']-(c['ev']+c['bridge'])/c['shares'])<1e-8;n+=2
 assert c['terminal']['reinvestment']>=c['terminal']['physicalFloor'];n+=1
assert abs(h['TTM20260930']['fcf']-984)<1e-8;n+=1
assert s['scanPrice']!=s['lastClose'];n+=1
assert s['nextEarningsConfirmed'] is None;n+=1
(p/'qa_results.json').write_text(json.dumps({'checks':n,'allPass':True},indent=2)+'\n')
