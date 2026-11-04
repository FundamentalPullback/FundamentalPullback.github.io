from pathlib import Path
import zipfile,hashlib
p=Path(__file__).parent
files=sorted(f for f in p.rglob('*') if f.is_file() and not any(x in f.parts for x in ['sources','__pycache__']) and f.suffix not in ['.zip','.pyc'] and f.name not in ['manifest.sha256','STATUS.md','audit_independent_20261104.md'])
(p/'manifest.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
z=p/'TOST_update_20261104_FINAL.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for f in files+[p/'manifest.sha256']:out.write(f,f.relative_to(p))
print(z,hashlib.sha256(z.read_bytes()).hexdigest())
