from pathlib import Path
import json,math,re
p=Path(__file__).parent;s=json.loads((p/'summary.json').read_text());m=json.loads((p/'model/results.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text());text=(p/'report.md').read_text();checks=[]
for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases','ownerFCF','certifiedEquityBridge','scenarioEconomicsOnly']:
 assert s[k] is None;checks.append('null '+k)
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:
 assert s[k] is False;checks.append('false '+k)
for k in ['technicalGate','nextEarningsConfirmed']:assert s[k] is None;checks.append('no invented '+k)
for side in ['pros','cons']:
 for v in s[side]:assert v['evidence'] in text;checks.append('contiguous evidence '+side)
assert s['scanPrice']!=s['lastClose'];checks.append('scanner vs verified close kept separate')
assert math.isclose(m['historicalCashBridge']['cashLessDebtAndAllCommitments'],100.965,abs_tol=1e-9);checks.append('liquidity arithmetic')
assert math.isclose(m['earningsQuality']['issuerAdjustedNIRebuilt'],127.359,abs_tol=1e-9);checks.append('NI bridge')
assert math.isclose(h['periods']['TTM_2026_09']['ebit_ex_vessel_gains'],601.883,abs_tol=1e-6);checks.append('TTM ex gains')
assert h['periods']['TTM_2026_09']['eps_diluted'] is None;checks.append('no false TTM diluted EPS')
for scenario in m['economicBreakEvenCases'].values():
 for row in scenario.values():
  assert row['notActualFCFF'] and row['notOwnerCash'] and row['notFairValue'];checks.append('economic sensitivity not value')
for e in m['q4BookingArithmetic']:assert e['notGuidance'] and e['notGuaranteedMinimum'];checks.append('not guaranteed booking floor')
assert 'pendiente de revisión independiente' in text or 'Revisión independiente completada para este alcance parcial' in text;checks.append('review status visible')
assert not re.search(r'\bTODO\b|\bTBD\b|\[INSERT',text);checks.append('no placeholders')
(p/'qa.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks},indent=2)+'\n');print('Package QA:',len(checks),'PASS')
