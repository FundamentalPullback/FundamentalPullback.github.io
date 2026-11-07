from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for f in ['history/build.py','model/model.py','comparables/calculate.py','build_report.py','prepare_summary.py','qa.py']:
 subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
