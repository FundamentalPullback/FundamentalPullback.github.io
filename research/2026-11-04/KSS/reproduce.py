from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
steps=['history/rebuild.py','model/model.py','model/validate.py','model/sensitivities.py','model/rates.py','model/export.py','comps_m/ratios.py','comparables/reproduce.py','build_report.py','build_summary.py','qa.py']
for f in steps:subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
print(len(steps),'offline steps complete')
