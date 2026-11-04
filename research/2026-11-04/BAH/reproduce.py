import subprocess,sys
from pathlib import Path
p=Path(__file__).parent
for f in ['history/build_history.py','history/normalization.py','capital/reproduce.py','model/rates.py','model/model.py','comps/reproduce.py','build_report.py','build_summary.py','qa.py']:
 subprocess.run([sys.executable,str(p/f)],check=True,cwd=p,stdout=subprocess.DEVNULL)
print('9 steps PASS')
