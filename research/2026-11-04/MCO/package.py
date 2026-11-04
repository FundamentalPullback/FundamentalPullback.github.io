from pathlib import Path
import zipfile,hashlib
P=Path(__file__).parent
files=['README.md','build_financials.py','financials.json','model.py','model.json','peers.py','peers.json','report.py','report.md','report.html','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py','sources/urls.json','sources/numeric_tables.json']
files += [f'sources/q3_table_{i}.txt' for i in [12,15,16,55,56,58,59,60,61,64,65,67,170,171]]
files += ['sources/q4release_table_29.txt','sources/k25_table_139.txt','sources/k25_table_140.txt']
files += ['comps/'+f for f in ['inputs.json','calculate.py','results.json','numeric_rows.csv','README.md']]
files=sorted(set(files));(P/'checksums.txt').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in files)+'\n')
with zipfile.ZipFile(P/'MCO_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+['checksums.txt']:z.write(P/f,f)
(P/'manifest.sha256').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in ['report.md','model.json','financials.json','publication.json','MCO_support.zip'])+'\n');print((P/'manifest.sha256').read_text())
