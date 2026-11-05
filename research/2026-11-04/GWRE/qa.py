from pathlib import Path
import json,math
p=Path(__file__).parent;s=json.loads((p/'summary.json').read_text());m=json.loads((p/'model/results.json').read_text());r=(p/'report.md').read_text();checks=[]
for k in ['fairValue','fairValueTotal','bear','base','bull']:assert s[k] is None;checks.append(k)
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:assert s[k] is False;checks.append(k)
assert s['technicalGate'] is None and s['nextEarningsConfirmed'] is None;checks.append('no invented gates')
for side in ['pros','cons']:
 for c in s[side]:assert c['evidence'] in r and len(c['es'])<=320 and len(c['en'])<=360;checks.append('exact contiguous evidence')
for k,c in m['scenarios'].items():
 assert len(c['rows'])==10;assert math.isclose(c['preDealBridge'],193.279);assert math.isclose(c['fundedClosingBridge'],-1731.721);checks.extend([k+'10 years',k+'bridge'])
 for row in c['rows']:assert math.isfinite(row['fcffFullYear']);checks.append(k+str(row['year']))
t=json.loads((p/'transaction/target_accounts.json').read_text());assert t['periods']['year_jan2026']['revenue']==34826463;checks.append('target actual history not null')
assert 'FRS102' in r and '150pb' in r and '269' in r and 'de cierre' in r;checks.append('perimeter limitations')
(p/'qa.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks},indent=2)+'\n')
print('QA',len(checks),'PASS')
