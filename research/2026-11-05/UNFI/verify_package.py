"""Verify delivered hashes and independently reproduce research in a temporary copy.
Run: python verify_package.py [--live-workbook]
Requires Python3; openpyxl and LibreOffice only for --live-workbook.
Never overwrites the delivered audited workbook or evidence.
"""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
for f in json.loads((P/'manifest.json').read_text()):
 assert hashlib.sha256((P/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
print('Delivered manifest hashes verified.')
with tempfile.TemporaryDirectory(prefix='unfi_reproduce_') as td:
 T=Path(td)/'research';shutil.copytree(P,T,ignore=shutil.ignore_patterns('*.zip','__pycache__','qa_render','live_test','recalculated','template_attempt'))
 for rel in ['reconstruct_technicals.py','independent_audit/reconstruct.py','independent_audit/financial_tieout.py']:
  subprocess.run([sys.executable,str(T/rel)],check=True,cwd=T)
 if '--live-workbook' in sys.argv:subprocess.run([sys.executable,str(T/'independent_audit/workbook_checks.py')],check=True,cwd=T)
 print('Independent reconstruction passed. Delivered files untouched.')
