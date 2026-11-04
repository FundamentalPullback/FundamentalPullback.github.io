from pathlib import Path
import json,zipfile,hashlib
P=Path(__file__).parent
files=['report.py','report.md','report.html','build_financials.py','financials.json','capital.py','capital.json','method_before_valuation.md','publication.json','sources.json','qa.py','package.py','sources/urls.json','sources/capital_notes.txt','sources/calendar_notes.txt','sources/funding_gap.txt','sources/price_fact.txt']
files += ['sources/'+f for f in json.load(open(P/'financials.json'))['source_tables']]
files += ['sources/'+f for f in ['q3_table_13.txt','q3_table_49.txt','q3_table_90.txt','q3_table_110.txt','q3_table_112.txt','q3_table_115.txt','q3_table_127.txt','release_table_5.txt','release_table_6.txt','release_table_10.txt','release_table_11.txt','release_table_12.txt']]
files=sorted(set(files))
(P/'checksums.txt').write_text(''.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in files))
files.append('checksums.txt')
with zipfile.ZipFile(P/'WEX_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(set(files)):z.write(P/f,f)
files+=['WEX_support.zip'];(P/'manifest.sha256').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in sorted(set(files)))+'\n')
