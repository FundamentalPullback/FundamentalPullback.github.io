from pathlib import Path
import json
p=Path(__file__).resolve().parent;s=json.loads((p/'summary.json').read_text());t=(p/'report.md').read_text();r=json.loads((p/'model/results.json').read_text());h=json.loads((p/'history/periods.json').read_text());checks=[]
checks.extend(s[k]is None for k in ['fairValue','totalFairValue','bear','base','bull']);checks.extend([s['scanStage2']is None,not s['entryApproved'],not s['stage3Complete'],s['scanPrice']!=s['regularClose']])
for z in s['pros']+s['cons']:checks.extend([z['evidence']in t,z['sourceUrl']in t,len(z['es'])<=320,len(z['en'])<=360])
checks.extend([abs(h['TTM2026']['ebit']-731.6)<1e-8,abs(h['TTM2026']['cfo']-810)<1e-8,abs(r['cases']['base']['bridge']+678.1)<1e-8])
for z in r['inverse']:checks.extend(['value'in z,abs(z.get('residual',1))<1e-7,z.get('monotoneIntervals')==1000])
assert all(checks);(p/'qa.json').write_text(json.dumps({'checks':len(checks),'passed':all(checks)},indent=2)+'\n');print(len(checks),'package checks PASS')
