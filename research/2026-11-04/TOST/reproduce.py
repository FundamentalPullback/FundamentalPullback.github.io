from pathlib import Path
import subprocess,sys
p=Path(__file__).parent
steps=['history/build_history.py','capital/reproduce.py','model/rates.py','model/model.py','comparables/reproduce.py','build_report.py','build_summary.py','qa.py']
for s in steps:subprocess.run([sys.executable,str(p/s)],cwd=p,check=True)
print(len(steps),'offline steps complete')
