from pathlib import Path
import subprocess,sys
P=Path(__file__).parent
steps=['history/build_history.py','capital/checks.py','model/model.py','model/rates.py','model/checks.py','comps/reproduce.py','build_report.py','qa.py']
for x in steps:subprocess.run([sys.executable,str(P/x)],cwd=P,check=True)
print(len(steps),'offline steps PASS')
