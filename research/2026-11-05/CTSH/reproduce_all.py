from pathlib import Path
import subprocess,sys,json
P=Path(__file__).parent
steps=['beta.py','technical.py','value.py','sensitivity.py','supplement.py','peer_check.py','qa.py','write_report.py','render_html.py'];out=[]
for step in steps:
 r=subprocess.run([sys.executable,str(P/step)],cwd=P,capture_output=True,text=True);out.append(dict(step=step,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
 if r.returncode:break
status=dict(artifact_type='deterministic_support_for_HTML_research',banker_formula_workbook=False,all_steps_passed=len(out)==len(steps)and all(x['exit_code']==0 for x in out),steps=out)
(P/'run_log.json').write_text(json.dumps(status,indent=2));print('PASS'if status['all_steps_passed']else'FAIL',len(out),'steps');assert status['all_steps_passed']
