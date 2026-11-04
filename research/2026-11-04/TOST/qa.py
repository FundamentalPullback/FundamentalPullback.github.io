import json
from pathlib import Path
p=Path(__file__).parent;s=json.loads((p/'summary.json').read_text());r=json.loads((p/'model/results.json').read_text());rep=(p/'report.md').read_text();checks=[]
for k in ['fairValue','fairValueTotal','bear','base','bull','technicalGate','nextEarningsConfirmed']:assert s[k] is None;checks.append(k)
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:assert s[k] is False;checks.append(k)
for k in ['pros','cons']:
 for q in s[k]:
  assert q['evidence'] in rep;assert len(q['es'])<=320;assert len(q['en'])<=360;checks.extend([k+'evidence',k+'es',k+'en'])
for n,v in r['cases'].items():
 assert len(v['rows'])==10;assert abs(s['scenarioEconomicsOnly'][n]['economicResidualPerShareProxy']-v['conditionalResidualPerShare'])<1e-9;assert v['selectedLiquidBridgeCoversModeledDeficit'];checks.extend([n]*3)
assert r['inverseFinanced']['firstYearFcff'] < -1885;checks.append('inverseUnfunded')
for inv in ['inverseFinanced','inverseEfficiencyOnly']:assert abs(r[inv]['residualError'])<1e-7;checks.append(inv)
assert '19,57' in rep and 'no pretende reproducir exactamente' in rep;checks.append('priorModelPreserved')
assert s['scanPrice']!=s['lastClose'];checks.append('separatePrices')
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'allPass':True,'checks':checks},indent=2)+'\n');print('QA',len(checks),'PASS')
