from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent
steps=['history/rebuild_history.py','history/check_history.py','transaction/checks.py','comps/build.py','model/model.py','model/rates.py','model/sensitivities.py','model/valuation_checks.py','build_report.py','build_summary.py','build_pros_cons.py','qa.py']
for f in steps:subprocess.run([sys.executable,str(P/f)],cwd=P,check=True)
print('PASS:',len(steps),'steps')
