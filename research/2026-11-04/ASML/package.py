from pathlib import Path
import zipfile,json,hashlib
P=Path(__file__).parent
files=['README.md','capital.py','capital.json','model.py','model.json','build_financials.py','financials.json','peers.py','peers.json','report.py','report.md','report.html','publication.json','prepare.py','english_evidence.md','research_notes.md','qa.py','qa.json','package.py','evidence/claims.json']
files += ['history/extracts/'+f for f in ['core_history.json','core_history.csv','quarterly_rows.json','annual_rows.json','qa.json']]
files += ['history/README.md','history/source_manifest.json']
files += ['comps/'+f for f in ['calculate.py','inputs.json','results.json','numeric_rows.csv','README.md']]
files=sorted(set(files));(P/'checksums.txt').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in files)+'\n')
with zipfile.ZipFile(P/'ASML_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+['checksums.txt']:z.write(P/f,f)
(P/'manifest.sha256').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in ['report.md','model.json','financials.json','publication.json','ASML_support.zip'])+'\n')
print((P/'manifest.sha256').read_text())
