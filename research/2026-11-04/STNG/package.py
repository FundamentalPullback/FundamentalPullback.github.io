from pathlib import Path
import json,hashlib,zipfile
p=Path(__file__).parent
fs=[]
for folder in ['facts','model','comparables','history']:
 fs.extend(f for f in (p/folder).rglob('*') if f.is_file() and f.suffix in ['.py','.json','.md','.csv'] and '__pycache__'not in f.parts)
for f in ['report.md','report.html','summary.json','qa.json','README.md','reproduce.py','build_report.py','build_summary.py','qa.py','package.py']:
 fs.append(p/f)
# Only derived analytical notes, not full third-party source captures.
fs.append(p/'capital_review/capital_bridge_review.md');fs.append(p/'capital_review/model_design_review.md')
fs=sorted(fs)
manifest={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest()for f in fs}
(p/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
z=p/'STNG_research_20261104_FINAL.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED)as a:
 for f in fs+[p/'manifest.json']:a.write(f,str(f.relative_to(p)))
print(z,hashlib.sha256(z.read_bytes()).hexdigest(),len(fs)+1)
