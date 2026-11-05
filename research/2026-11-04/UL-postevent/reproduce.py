from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent
for f in ['model/recompute.py','build_report.py','build_summary.py','qa.py']:
 subprocess.run([sys.executable,str(P/f)],cwd=P,check=True)
print('All four offline steps passed. Numerical outputs are conditional diagnostics, not current fair value.')
