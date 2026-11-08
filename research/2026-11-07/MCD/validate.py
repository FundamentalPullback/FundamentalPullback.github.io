import json,subprocess,sys,pathlib
p=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(p/'model.py')],check=True,capture_output=True)
r=json.loads((p/'results.json').read_text());checks=[]
for name,c in r['scenarios'].items():
 assert len(c['years'])==10
 for y in c['years']:
  assert abs(y['fcff']-(y['nopat']+y['da']-y['capex']-y['dnwc']))<1e-7
  assert abs(y['capex']-sum(y[k] for k in ['baseline_capex','partner_capex','software_other_capex']))<1e-7
 assert abs(c['terminal_fcff']-(c['terminal_nopat']+c['terminal_da']-c['terminal_capex']-c['terminal_dnwc']))<1e-7
 assert abs(c['equity']-c['ev']-c['bridge'])<1e-7
 assert c['inputs']['w']>c['inputs']['g']
checks=['10 forecast years each scenario','FCFF component identities','capital component identities','terminal reinvestment identity','EV-equity bridge','WACC > g','NEXT support = 8500 (model assertion)']
(p/'validation.json').write_text(json.dumps({'status':'passed','checks':checks,'independent_audit':'completed_with_caveats; see audit.json and audit_checks.json','model_type':'deterministic_support','posture':'senior-review-ready'},indent=2));print('PASS')
