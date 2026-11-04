from pathlib import Path
import hashlib,zipfile
p=Path(__file__).parent
names=['analyze.py','analysis.json','report.py','report_body.md','report.md','report.html','prepare.py','publication.json','qa.py','qa.json','package.py','README.md','facts/inputs.json','comparables/inputs.json','comparables/reproduce.py','comparables/outputs.json','facts/q2_numeric_tables.txt']
names+=['history/'+x.strip() for x in (p/'history/PUBLIC_FILES.txt').read_text().splitlines() if x.strip()]
files=[p/x for x in sorted(set(names))]
(p/'manifest.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
with zipfile.ZipFile(p/'support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[p/'manifest.sha256']:z.write(f,str(f.relative_to(p)))
for n in ['report.md','analysis.json','publication.json','support.zip']:print(n,hashlib.sha256((p/n).read_bytes()).hexdigest())
