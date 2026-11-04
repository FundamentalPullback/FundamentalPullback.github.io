from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for file in ['history/rebuild_history.py','analysis/reproduce.py','build_report.py','build_summary.py','qa.py']:
 subprocess.run([sys.executable,str(p/file)],cwd=p,check=True)
print('Five offline steps complete; no NAV or DCF produced')
