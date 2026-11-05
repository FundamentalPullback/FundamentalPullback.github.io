from pathlib import Path
import hashlib,json,zipfile
P=Path(__file__).parent
root=['README.md','report.html','report.md','summary.json','build_history.py','write_report.py','render_report.py','reproduce.py','audit_independent.py','audit_independent.md','audit_independent_checks.json','package.py','visual_qa.json']
files=[P/x for x in root]+sorted((P/'history').glob('*.json'))+sorted((P/'history').glob('*.csv'))+sorted((P/'model').glob('*.json'))+sorted((P/'model').glob('*.csv'))+[P/'model/model.py',P/'capital/combined_capital.json',P/'capital/sources.json']
manifest={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files};(P/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
z=P/'SWKS_research_20261104_FINAL.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in files+[P/'manifest.json']:a.write(f,str(f.relative_to(P)))
print(z,'files',len(files)+1,'bytes',z.stat().st_size,'sha256',hashlib.sha256(z.read_bytes()).hexdigest())
