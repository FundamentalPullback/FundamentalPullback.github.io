from pathlib import Path
import hashlib,zipfile
p=Path(__file__).parent
names=['model.py','model.json','report.py','report_body.md','report.md','report.html','prepare.py','publication.json','qa.py','qa.json','package.py','README.md']
files=[p/n for n in names]+[f for d in ['facts','history','comparables'] for f in (p/d).rglob('*') if f.is_file() and f.name!='extract_local.py' and '__pycache__' not in str(f)]
(p/'manifest.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in sorted(files)))
with zipfile.ZipFile(p/'support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[p/'manifest.sha256']:z.write(f,str(f.relative_to(p)))
for n in ['report.md','model.json','publication.json','support.zip']:print(n,hashlib.sha256((p/n).read_bytes()).hexdigest())
