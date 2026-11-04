from pathlib import Path
import json,zipfile,hashlib
P=Path(__file__).parent
files=['report.py','report.md','report.html','model.py','model.json','build_financials.py','financials.json','peers.py','peers.json','sources.json','publication.json','qa.py','package.py','sources/urls.json','sources/claims.json','sources/h15_numeric.txt']
files += ['sources/'+x for x in json.load(open(P/'financials.json'))['source_tables']]
files += ['sources/'+x for x in ['q3_table_6.txt','q3_table_18.txt','q3_table_27.txt','q3_table_29.txt','q3_table_37.txt','q3_table_38.txt','k25_table_59.txt']]
files += ['comps/'+x for x in ['inputs.json','reproduce.py','results.json','results.csv','bridge.csv','README.md','sources.csv','numeric_evidence.txt'] if (P/'comps'/x).exists()]
files=sorted(set(files));hashes={p:hashlib.sha256((P/p).read_bytes()).hexdigest() for p in files}
(P/'checksums.txt').write_text('\n'.join(h+'  '+p for p,h in hashes.items())+'\n')
with zipfile.ZipFile(P/'HAS_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+['checksums.txt']:z.write(P/p,p)
(P/'manifest.sha256').write_text('\n'.join(hashlib.sha256((P/p).read_bytes()).hexdigest()+'  '+p for p in ['report.md','model.json','financials.json','publication.json','HAS_support.zip'])+'\n')
print((P/'manifest.sha256').read_text())
