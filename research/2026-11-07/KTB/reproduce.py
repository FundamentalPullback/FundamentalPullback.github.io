from pathlib import Path
import sys,subprocess
p=Path(__file__).resolve().parent
for f in ['build_report.py','prepare_summary.py']:subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
