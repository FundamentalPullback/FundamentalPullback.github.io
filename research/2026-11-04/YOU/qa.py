from pathlib import Path
import json,csv
p=Path(__file__).parent;s=json.loads((p/'summary.json').read_text());r=json.loads((p/'model/results.json').read_text());rep=(p/'report.md').read_text();checks=[]
for k in ['fairValue','fairValueTotal','bear','base','bull','technicalGate','nextEarningsConfirmed']:assert s[k] is None;checks.append(k)
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:assert not s[k];checks.append(k)
for k in ['pros','cons']:
 for v in s[k]:
  assert v['evidence'] in rep;assert len(v['es'])<=320;assert len(v['en'])<=360;checks.extend([k]*3)
for n,o in r['cases'].items():
 assert len(o['rows'])==10;assert o['economicUnits']>o['classAWithAwards'];assert abs(o['conditionalClassAResidual']-((o['ev']+o['opcoCash'])/o['economicUnits']+(o['parentCash']+o['parentDtaCredit']-o['parentTra'])/o['classAWithAwards']))<1e-8;checks.extend([n]*3)
for inv in ['inverseFinanced','inverseEfficiency']:assert abs(r[inv]['residual'])<1e-7;assert r[inv]['monotonicIntervals']==1000;checks.extend([inv]*2)
assert r['inverseFinanced']['peakFunding']>632.969;checks.append('inverseUnfunded')
assert s['lastClose']!=s['scanPrice'];checks.append('pricesDistinct')
assert 'No se ha construido DCF' not in rep;checks.append('scopeConsistent')
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'allPass':True,'checks':checks},indent=2)+'\n');print('PASS',len(checks))
