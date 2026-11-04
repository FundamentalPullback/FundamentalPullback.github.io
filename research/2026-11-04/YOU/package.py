from pathlib import Path
import hashlib,zipfile
p=Path(__file__).parent
files=sorted(f for f in p.rglob('*') if f.is_file() and not any(x in f.parts for x in ['sources_private','__pycache__']) and f.suffix not in ['.zip','.pyc'] and f.name not in ['manifest.sha256','STATUS.md','audit_independent_20261104.md','extract_tables_private.py'])
(p/'manifest.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
z=p/'YOU_research_20261104_FINAL.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for f in files+[p/'manifest.sha256']:out.write(f,f.relative_to(p))
print(len(files)+1,'files',hashlib.sha256(z.read_bytes()).hexdigest())
