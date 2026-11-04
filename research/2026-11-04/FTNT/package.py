import pathlib,hashlib,zipfile
P=pathlib.Path(__file__).parent
files=[P/x for x in ['model.py','model.json','report.py','report.md','report.html','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py','README.md']]
files += [f for d in ['facts','history','comps'] for f in (P/d).rglob('*') if f.is_file() and f.name not in ['manifest.sha256'] and '__pycache__' not in str(f)]
(P/'manifest.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(P))+'\n' for p in sorted(files)))
with zipfile.ZipFile(P/'support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[P/'manifest.sha256']:z.write(p,str(p.relative_to(P)))
for x in ['report.md','model.json','publication.json','support.zip']:print(x,hashlib.sha256((P/x).read_bytes()).hexdigest())
