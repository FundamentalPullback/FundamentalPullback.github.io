import pathlib,hashlib,zipfile
P=pathlib.Path(__file__).parent
files=[P/x for x in ['analysis.py','analysis.json','report.py','report_body.md','report.md','report.html','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py','README.md']]
files += [f for d in ['facts','history','comps'] for f in (P/d).rglob('*') if f.is_file() and f.name!='manifest.sha256' and '__pycache__' not in str(f)]
(P/'manifest.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n' for f in sorted(files)))
with zipfile.ZipFile(P/'support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[P/'manifest.sha256']:z.write(f,str(f.relative_to(P)))
for x in ['report.md','analysis.json','publication.json','support.zip']:print(x,hashlib.sha256((P/x).read_bytes()).hexdigest())
