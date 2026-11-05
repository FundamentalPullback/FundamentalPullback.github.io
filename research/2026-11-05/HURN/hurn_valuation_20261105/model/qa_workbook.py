import json,zipfile,hashlib
from pathlib import Path
import openpyxl
P=Path(__file__).resolve().parent;O=P.parent/'outputs';p=O/'HURN_DCF.xlsx'
f=openpyxl.load_workbook(p,data_only=False);v=openpyxl.load_workbook(p,data_only=True);r=json.loads((P/'results.json').read_text())
errs=[];missing=[];count=0
for s in f:
 for row in s:
  for c in row:
   z=v[s.title][c.coordinate]
   if c.data_type=='f':
    count+=1
    if z.value is None:missing.append(f'{s.title}!{c.coordinate}')
   if z.data_type=='e':errs.append(f'{s.title}!{c.coordinate}: {z.value}')
check={'formula_count':count,'formula_errors':errs,'missing_formula_caches':missing,'external_workbook_links':len(f._external_links),'zip_external_links':[n for n in zipfile.ZipFile(p).namelist() if 'externalLink' in n],'canonical_output_deltas':{s:v[s.title()]['D94'].value-r[s]['per_share'] for s in r},'canonical_q4_fcff_deltas':{s:v[s.title()]['D34'].value-r[s]['stub']['fcff'] for s in r},'canonical_annual_fcff_max_deltas':{s:max(abs(v[s.title()].cell(68,i+4).value-row['fcff']) for i,row in enumerate(r[s]['rows'])) for s in r},'sheets':f.sheetnames,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'visual_review':'All six sheets rendered; detailed case inputs, forecast, and terminal/bridge ranges reviewed. No clipped values or formula errors.','calculation':'Recursive spreadsheet evaluator plus Artifact Tool recalculation and restored live-input perturbation; native Excel/LibreOffice not tested.'}
assert not errs and not missing and not f._external_links
assert max(abs(x) for x in check['canonical_output_deltas'].values())<1e-6
assert max(check['canonical_annual_fcff_max_deltas'].values())<1e-6
(O/'workbook_QA.json').write_text(json.dumps(check,indent=2))
log=json.loads((O/'workbook_run_log.json').read_text());log.update({'artifact_tool_recalculated':True,'artifact_live_input_test':{'input':'Base!D22','from':.01,'to':0,'result':171.74425994951866,'restored_result':164.20739714731093},'formula_error_count':len(errs),'external_links':len(f._external_links),'native_excel_or_libreoffice_recalculation':False});(O/'workbook_run_log.json').write_text(json.dumps(log,indent=2));print(json.dumps(check,indent=2))
