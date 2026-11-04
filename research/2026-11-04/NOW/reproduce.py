import subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
scripts=['history/build_history.py','history/check_history.py','model/model.py','model/rates.py','model/sensitivities.py','model/valuation_checks.py','comps/build_comps.py','comps/now_screen.py','build_report.py','build_summary.py','build_pros_cons.py','qa.py']
for s in scripts:subprocess.run([sys.executable,str(P/s)],cwd=P,check=True)
print('All',len(scripts),'offline steps PASS')
