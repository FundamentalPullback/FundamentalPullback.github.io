from pathlib import Path
import hashlib,json,zipfile
P=Path(__file__).parent
rootfiles=['README.md','report.md','summary.json','build_report.py','reproduce.py','qa.py','qa.json','package.py']
files=[P/f for f in rootfiles]
for d in ['history','capital','model','comps']:
 files += [p for p in (P/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.py','.json','.csv','.md','.txt'] and p.name not in ['manifest.sha256','build.py']]
files=sorted(set(files));manifest={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files};(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
status='FINAL' if json.loads((P/'summary.json').read_text())['readyForPublication'] else 'HOLD'
z=P/f'PANW_research_20261104_{status}.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files+[P/'manifest.json']:
  info=zipfile.ZipInfo(str(p.relative_to(P)),date_time=(2026,11,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;f.writestr(info,p.read_bytes())
print(len(files),'files',z,hashlib.sha256(z.read_bytes()).hexdigest())
