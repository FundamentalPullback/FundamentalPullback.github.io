from pathlib import Path
import subprocess,sys
p=Path(__file__).parent
for f in ['build_history.py','model/model.py','write_report.py','render_report.py','audit_independent.py']:
 subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
print('Reproduced. All investment approval gates must remain false/null. Changes require fresh independent review.')
