from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for f in ['model.py','verification.py','write_report.py','publication_metadata.py']:
 subprocess.run([sys.executable,str(p/f)],cwd=p,check=True)
