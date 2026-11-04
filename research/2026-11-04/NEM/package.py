from pathlib import Path
import hashlib,json,zipfile,sys
p=Path(__file__).resolve().parent
files=['README.md','report_body.md','build_report.py','build_summary.py','report.md','summary.json','reproduce.py','qa.py','qa_results.json','package.py','history/financial_inputs.json','history/financial_history.json','history/financial_history.csv','history/factual_context.json','history/normalization_notes.md','history/rebuild_history.py','history/checks.txt','reserves/facts.json','reserves/analysis.md','capital/facts.json','capital/analysis.md','market/facts.json','analysis/inputs.json','analysis/results.json','analysis/reproduce.py']
m={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in files}
(p/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
label=sys.argv[1] if len(sys.argv)>1 else 'HOLD'
z=p/f'NEM_research_20261104_{label}.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED) as out:
 for f in files+['manifest.json']:
  info=zipfile.ZipInfo(f,date_time=(2026,11,4,22,0,0));info.compress_type=zipfile.ZIP_DEFLATED
  out.writestr(info,(p/f).read_bytes())
print(z,hashlib.sha256(z.read_bytes()).hexdigest(),len(files),'manifest files')
