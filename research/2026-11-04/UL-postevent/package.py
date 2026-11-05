from pathlib import Path
import json,hashlib,zipfile
P=Path(__file__).parent;state=json.loads((P/'publication_state.json').read_text());suffix='FINAL' if state['ready'] else 'HOLD'
files=['README.md','publication_state.json','inputs/legacy_full_model.json','inputs/legacy_audit_summary.json','inputs/event_inputs.json','inputs/source_map.json','inputs/legacy_cost_note.md','source_review.md','model/recompute.py','model/results.json','model/qa.json','build_report.py','build_summary.py','report.md','report.html','summary.json','qa.py','qa.json','reproduce.py','package.py']
manifest={'scope':'UL November4 Investor Event supplement only; no current certified fair value, target or entry.','status':state['status'],'files':[{'path':x,'bytes':(P/x).stat().st_size,'sha256':hashlib.sha256((P/x).read_bytes()).hexdigest()}for x in files]}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
out=P/f'UL_postevent_20261104_{suffix}.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for file in files+['manifest.json']:
  info=zipfile.ZipInfo(file,date_time=(2026,11,5,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,(P/file).read_bytes())
print(out);print('SHA256',hashlib.sha256(out.read_bytes()).hexdigest(),'members',len(files)+1)
