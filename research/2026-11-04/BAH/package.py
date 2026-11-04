from pathlib import Path
import json,hashlib,zipfile
p=Path(__file__).parent
fs=sorted(f for f in p.rglob('*') if f.is_file() and 'sources_private' not in f.parts and '__pycache__' not in f.parts and f.suffix!='.zip' and f.name not in ['manifest.json','STATUS.md','audit_independent_20261104.md'] and not f.name.startswith('audit'))
manifest={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in fs};(p/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
z=p/'BAH_research_20261104_FINAL.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in fs+[p/'manifest.json']:a.write(f,str(f.relative_to(p)))
print(z,hashlib.sha256(z.read_bytes()).hexdigest(),len(fs)+1)
