from pathlib import Path
import subprocess,sys,json
p=Path(__file__).resolve().parent
for f in ['build_history.py','prepare_summary.py']:subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
x=json.loads((p/'summary.json').read_text());assert all(x[k]is None for k in ['fairValue','totalFairValue','bear','base','bull']);assert not x['entryApproved'] and not x['stage3Complete']
