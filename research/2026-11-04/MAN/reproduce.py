from pathlib import Path
import subprocess,sys
P=Path(__file__).parent
steps=['history/reproduce.py','model/model.py','model/sensitivities.py','model/validate.py','model/rates.py','comparables/reproduce.py','build_report.py','build_summary.py','qa.py']
for step in steps:subprocess.run([sys.executable,str(P/step)],cwd=P,check=True,stdout=subprocess.DEVNULL)
print('PASS',len(steps),'offline steps')
