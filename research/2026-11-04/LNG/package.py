from pathlib import Path
import json,hashlib,zipfile
P=Path(__file__).parent;state=json.loads((P/'publication_state.json').read_text());suffix='FINAL'if state['ready']else'HOLD'
files=['README.md','publication_state.json','facts/inputs.json','source_register.json','history/observations.json','history/build_history.py','history/history.json','history/history.csv','history/qa.json','history_review/observations.json','history_review/reproduce.py','history_review/history_extended.json','history_review/history_extended.csv','history_review/qa.json','history_review/earnings_bridge.csv','history_methodology.md','capital_review/inputs.json','capital_review/waterfall.py','capital_review/waterfall_outputs.json','capital_methodology.md','comparables/inputs.json','comparables/reproduce.py','comparables/outputs.json','analyze.py','analysis.json','normalize.py','normalization.json','normalization_qa.json','build_report.py','build_summary.py','report.md','report.html','summary.json','qa.py','qa.json','reproduce.py','package.py']
manifest={'scope':'LNG conditional partial research; no certified total value, owner FCF or entry.','status':state['status'],'files':[{'path':f,'bytes':(P/f).stat().st_size,'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest()}for f in files]}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
out=P/f'LNG_research_20261104_{suffix}.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for file in files+['manifest.json']:
  info=zipfile.ZipInfo(file,date_time=(2026,11,5,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,(P/file).read_bytes())
print(out);print('SHA256',hashlib.sha256(out.read_bytes()).hexdigest(),'members',len(files)+1)
