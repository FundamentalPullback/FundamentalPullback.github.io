import pathlib,subprocess,sys
P=pathlib.Path(__file__).parent
commands=[['history/run_offline.py'],['ownership/reproduce_offline.py'],['model/build_inputs.py'],['model/model.py'],['model/sensitivities.py'],['model/rates.py'],['model/valuation_checks.py'],['comps/atd.py'],['comps/build_walmex.py'],['comps/fmx.py'],['build_report.py'],['prepare.py'],['qa.py']]
for cmd in commands:
 p=subprocess.run([sys.executable,*cmd],cwd=P,capture_output=True,text=True)
 print(cmd[0],p.returncode)
 if p.returncode:print(p.stdout,p.stderr);raise SystemExit(p.returncode)
print('All public computations reproduced offline. This does not approve an investment.')
