from pathlib import Path
import subprocess,sys
p=Path(__file__).parent
steps=['history/build_history.py','model/analyze.py','comparables/reproduce.py','build_report.py','build_summary.py','qa.py']
for f in steps:subprocess.run([sys.executable,'-S',str(p/f)],cwd=p,check=True,stdout=subprocess.DEVNULL)
print('Six offline steps PASS')
