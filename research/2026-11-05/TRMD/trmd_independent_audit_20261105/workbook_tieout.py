from pathlib import Path
import json,openpyxl,hashlib
from independent_checks import rebuild,A,R,check,checks
P=Path(__file__).resolve().parent;f=P.parent/'trmd_valuation_20261105/outputs/trmd_fleet/TRMD_fleet_FCFF.xlsx';w=openpyxl.load_workbook(f,data_only=True)
for case,sheet,col in [('bear','Bear FCFF','B'),('base','Base FCFF','C'),('bull','Bull FCFF','D')]:
 r=R[case];ev,v,rows=rebuild(A[case],r['renewal'],max(x['year'] for x in r['rows']))
 for i,x in enumerate(rows,5):
  check(f'{case} workbook year {i}',w[sheet][f'A{i}'].value,x['year'])
  check(f'{case} workbook FCFF {i}',w[sheet][f'S{i}'].value,x['fcff'],1e-6)
  check(f'{case} workbook PV {i}',w[sheet][f'U{i}'].value,x['pv'],1e-6)
 check(case+' workbook EV',w['Bridge'][f'{col}5'].value,ev,1e-6)
 check(case+' workbook per share',w['Bridge'][f'{col}16'].value,v,1e-7)
output={'workbook_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'scope':'Independent source-to-engine cohort rebuild and cached workbook FCFF/PV/EV/value tieout. This is not a native Excel recalc.','passed':sum(x['pass_'] for x in checks),'failed':sum(not x['pass_'] for x in checks),'checks':checks}
(P/'workbook_tieout.json').write_text(json.dumps(output,indent=2));print(output['passed'],output['failed'])
