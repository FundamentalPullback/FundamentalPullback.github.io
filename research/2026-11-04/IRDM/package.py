from pathlib import Path
import hashlib,json,zipfile
P=Path(__file__).parent
files=[P/f for f in ['README.md','report.md','summary.json','build_report.py','reproduce.py','qa.py','qa.json','package.py']]
for d in ['history','capital','model','comps','transaction']:
 files.extend(p for p in (P/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.json','.md','.py','.csv','.txt'] and p.name not in ['build_inputs.py','build.py','manifest.sha256'])
files=sorted(set(files));m={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files};(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');status='FINAL' if json.loads((P/'summary.json').read_text())['readyForPublication'] else 'HOLD';z=P/f'IRDM_research_20261104_{status}.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[P/'manifest.json']:
  i=zipfile.ZipInfo(str(p.relative_to(P)),date_time=(2026,11,4,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;f.writestr(i,p.read_bytes())
print(len(files),'files',hashlib.sha256(z.read_bytes()).hexdigest(),z)
