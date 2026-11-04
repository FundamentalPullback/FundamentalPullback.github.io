from pathlib import Path
import hashlib,json,zipfile,sys
p=Path(__file__).resolve().parent
files=['README.md','report_body.md','build_report.py','build_summary.py','report.md','summary.json','reproduce.py','qa.py','qa_results.json','package.py']
for folder,names in {'history':['inputs.json','normalization_notes.md','normalized_history.csv','normalized_history.json','qa.json','rebuild.py','ttm_comparison.csv'],'capital':['facts.json','analysis.md'],'market':['facts.json'],'model':['inputs.json','model.py','results.json','validate.py','checks.json','sensitivities.py','sensitivities.json','inverse.json','rates.py','rates_results.json','export.py','bear_10years.csv','base_10years.csv','bull_10years.csv'],'comps_m':['facts.json','analysis.md','ratios.py','ratios_output.json'],'comparables':['inputs.json','reproduce.py','results.json']}.items():files += [folder+'/'+n for n in names]
m={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in files};(p/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
label=sys.argv[1] if len(sys.argv)>1 else 'HOLD';z=p/f'KSS_research_20261104_{label}.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED) as out:
 for f in files+['manifest.json']:
  info=zipfile.ZipInfo(f,date_time=(2026,11,4,22,0,0));info.compress_type=zipfile.ZIP_DEFLATED;out.writestr(info,(p/f).read_bytes())
print(z,hashlib.sha256(z.read_bytes()).hexdigest(),len(files),'manifest files')
