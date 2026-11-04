from pathlib import Path
import json,hashlib,zipfile
P=Path(__file__).parent
roots=['history','capital','market','model','comparables'];top=['README.md','report_body.md','build_report.py','report.md','build_summary.py','summary.json','qa.py','qa_results.json','reproduce.py','package.py']
files=[P/x for x in top]+[f for x in roots for f in (P/x).rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix in ['.py','.json','.csv','.md']]
files=sorted(set(files));manifest={'ticker':'MAN','asOf':'2026-11-04','files':{str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
name='MAN_research_20261104_FINAL.zip' if json.loads((P/'summary.json').read_text())['readyForPublication'] else 'MAN_research_20261104_HOLD.zip'
with zipfile.ZipFile(P/name,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[P/'manifest.json']:
  zi=zipfile.ZipInfo(str(f.relative_to(P)),(2026,11,4,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,f.read_bytes())
print(name,len(files),hashlib.sha256((P/name).read_bytes()).hexdigest())
