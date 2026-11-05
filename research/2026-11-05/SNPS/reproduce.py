from pathlib import Path
import subprocess,sys,json,hashlib
P=Path(__file__).resolve().parent;logs=[]
for script in ['model/history.py','model/value.py','model/analyze.py','model/build_workbook.py','write_report.py','qa.py']:
 r=subprocess.run([sys.executable,str(P/script)],cwd=P,capture_output=True,text=True);logs.append({'script':script,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,(script,r.stdout,r.stderr)
r=subprocess.run(['pandoc','report.md','-s','--metadata','pagetitle=SNPS | Fundamental Pullback','--css','report.css','-o','report.html'],cwd=P,capture_output=True,text=True);logs.append({'script':'pandoc','returncode':r.returncode,'stderr':r.stderr});assert r.returncode==0
(P/'run_log.json').write_text(json.dumps({'status':'passed','workbook_mode':'custom_formula_workbook','model_status':'screen-grade','steps':logs},indent=2));print('Reproduction passed: 7 steps')
