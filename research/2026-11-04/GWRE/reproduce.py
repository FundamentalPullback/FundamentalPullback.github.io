from pathlib import Path
import subprocess,sys
p=Path(__file__).parent
steps=['history/build_history.py','capital_research/build_capital.py','transaction/target_checks.py','transaction/reproduce.py','model/rates.py','model/model.py','comps/reproduce.py','build_report.py','build_summary.py','qa.py']
for s in steps:subprocess.run([sys.executable,str(p/s)],check=True,cwd=p,stdout=subprocess.DEVNULL)
print(str(len(steps))+' steps PASS')
