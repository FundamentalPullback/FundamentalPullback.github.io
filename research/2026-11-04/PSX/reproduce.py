import subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
scripts=['history/rebuild.py','model/model.py','model/rates.py','model/sensitivities.py','model/valuation_checks.py','comps/mpc/calculate_mpc.py','comps/calculate.py','build_report.py','qa.py']
for s in scripts:
 subprocess.run([sys.executable,str(P/s)],cwd=P,check=True)
print('All',len(scripts),'offline steps PASS')
