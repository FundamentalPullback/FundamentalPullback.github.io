from pathlib import Path
import subprocess,sys
p=Path(__file__).parent
steps=['scripts/rebuild.py','model/model.py','model/rates.py','capital/model_bridge.py','build_report.py','build_summary.py','qa.py']
for f in steps:subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
print(len(steps),'offline steps reproduced')
