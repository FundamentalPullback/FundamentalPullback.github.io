from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent
steps=['history/reproduce.py','capital/offlinechecks.py','comps/enrich.py','model/model.py','model/rates.py','model/valuation_checks.py','build_report.py','qa.py']
for s in steps:subprocess.run([sys.executable,str(P/s)],cwd=P,check=True)
print(len(steps),'offline steps PASS')
