from pathlib import Path
import json,zipfile,hashlib
P=Path(__file__).parent
files=['report.py','report.md','report.html','model.py','model.json','build_financials.py','financials.json','peers.py','peers.json','sources.json','publication.json','qa.py','package.py','sources/urls.json','sources/peer_urls.json','sources/peer_inputs.json','sources/capital_notes.txt','sources/price_fact.txt','sources/calendar_fact.txt','sources/h15_numeric.txt','sources/regulatory_search.json','sources/peer_claims.txt']
files+=['sources/'+f for f in json.load(open(P/'financials.json'))['source_tables']]
files+=['sources/q2_table_15.txt','sources/q2_table_22.txt','sources/q2_table_23.txt']
files += [str(x.relative_to(P)) for x in (P/'sources').glob('peer_*_*.txt')]
with zipfile.ZipFile(P/'DLTR_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(set(files)):z.write(P/f,f)
files+=['DLTR_support.zip'];(P/'manifest.sha256').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in sorted(set(files)))+'\n')
print('Package selected numerical facts and own notes; no entire filing.')
