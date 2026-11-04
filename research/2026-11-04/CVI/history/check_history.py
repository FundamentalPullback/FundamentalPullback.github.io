from pathlib import Path
import json,subprocess,sys,hashlib
D=Path(__file__).resolve().parent
files=['history.json','history.csv','segment_observations.json','segment_history.json','segment_history.csv','ex_uan_and_adjustments.json']
before={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in files}
subprocess.run([sys.executable,str(D/'rebuild_history.py')],check=True,stdout=subprocess.DEVNULL)
after={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in files}
assert before==after,'Offline rebuild is not deterministic'
H=json.loads((D/'history.json').read_text())['periods'];O=json.loads((D/'observations.json').read_text());ids={o['observation_id'] for o in O};R={r['period']:r['metrics'] for r in H};checks=[]
for r in H:
 m=r['metrics'];v=lambda x:m[x]['value']
 assert abs(v('net_income_consolidated')-v('net_income_parent')-v('net_income_nci'))<=1
 assert v('fcf_after_turnaround')==v('cfo')-v('gross_capex')-v('cash_turnaround')
 for k,t in m.items():
  assert set(t['observation_ids'])<=ids
  if t['value'] is not None: assert t['source_urls']
 checks.append(r['period']+': NCI and gross cash investment reconciliation passed')
for met in ['revenue','ebit','net_income_parent','cfo','gross_capex','cash_turnaround','sbc','da','cash_taxes']:
 val=sum(R[q][met]['value'] for q in ['Q4 2025','Q1 2026','Q2 2026','Q3 2026'])
 assert abs(val-R['TTM Sep 2026'][met]['value'])<=1,(met,val)
checks.append('Last four quarters reconcile to TTM within independent reporting rounding of $1m')
checks.append('Deterministic offline rebuild passed; all nonmissing values retain primary-source URLs and observation IDs')
out={'status':'PASS','checks':checks,'rounding_caveats':['Q3 2026 reported revenue3281 versus YTD-difference3282; preserve direct quarterly value. TTM9810 derives FY25 plus9M26 minus9M25.','Q3 2026 CF-derived D&A78 versus income-statement D&A79; CF totals use reported YTD differences.'],'coverage_limits':['Quarterly cash taxes, capex, CFO and SBC are YTD differences, not independently reported quarterly values.','Cash taxes negative values are net refunds.','No EPS or weighted-share subtraction is performed.','Consolidated CFO contains100% of UAN and is not all available to CVI common equity.','SBC expense is liability-classified; extra SBC subtraction is an illustrative conservative sensitivity and can double count cash settlements.']}
(D/'check_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
