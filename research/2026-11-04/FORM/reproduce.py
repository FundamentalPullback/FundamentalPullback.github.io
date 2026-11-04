from pathlib import Path
import subprocess,sys
P=Path(__file__).parent
steps=['history/reproduce.py','capital/checks.py','model/model.py','model/checks.py','model/rates.py','comps/reproduce.py','build_report.py','qa.py']
for x in steps:subprocess.run([sys.executable,str(P/x)],cwd=P,check=True)
print(len(steps),'offline steps PASS')
