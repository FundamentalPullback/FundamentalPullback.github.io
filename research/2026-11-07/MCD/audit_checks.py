"""Independent audit assertions; does not change analyst underwriting assumptions."""
import json,pathlib,subprocess,sys,math
p=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(p/'model.py')],check=True,capture_output=True)
r=json.loads((p/'results.json').read_text()); h=r['history']; checks=[]
for label,a,b,c in [('TTM2026','2025','9M2026','9M2025'),('TTM2025','2024','9M2025','9M2024'),('Q4_2025','2025',None,'9M2025')]:
 for k in ['revenue','ebit','net_income','eps','cfo','da','capex','sbc','other_investing_outflow']:
  assert math.isclose(h[label][k],h[a][k]+(h[b][k] if b else 0)-h[c][k],abs_tol=1e-8)
checks.append('Both TTM periods and Q4 derived independently from fiscal-year and nine-month inputs')
for k in ['revenue','ebit','net_income','cfo','da','capex','sbc','other_investing_outflow']:
 assert abs(sum(h['Q'+str(i)+'_2026'][k] for i in [1,2,3])-h['9M2026'][k])<=4
checks.append('Four-quarter rollforward: reported source differences no more than $4m; retained rather than silently forced')
# Source-document tests remain prior audit evidence, not rerun by this public numerical check.
for name,c in r['scenarios'].items():
 assert len(c['years'])==10
 assert abs(sum(y['partner_capex']+y['rent_support'] for y in c['years'])-8500)<1e-7
 assert abs(sum(y['partner_capex']+y['rent_support'] for y in c['years'][:4])-5000)<1e-7
 for i,y in enumerate(c['years'],1):
  assert y['baseline_capex']>0
  assert abs(y['ebit']-(y['revenue']*y['pre_relief_margin']-y['rent_support']))<1e-7
  assert abs(y['fcff']-(y['nopat']+y['da']-y['capex']-y['dnwc']))<1e-7
  assert abs(y['pv']-y['fcff']/(1+c['inputs']['w'])**(i+54/365))<1e-7
 last=c['years'][-1]; g=c['inputs']['g'];w=c['inputs']['w']
 assert abs(c['terminal_fcff']/last['fcff']-1-g)<1e-10
 assert abs(c['terminal_capex']/last['capex']-1-g)<1e-10
 ev=sum(y['pv'] for y in c['years'])+c['stub_pv']+c['terminal_fcff']/(w-g)/(1+w)**(10+54/365)
 assert abs(ev-c['ev'])<1e-7 and abs(c['value']-(ev+193+2985-39820-70)/707.484744)<1e-7
checks.append('All scenarios: independent PV and bridge, 54-day stub, NEXT totals and single expense/capital treatment, positive physical capex and terminal continuity')
assert [round(r['scenarios'][k]['value'],2) for k in ['adverso','base','favorable']]==[129.26,235.45,368.83]
checks.append('Scenario outputs reproduce $129.26/$235.45/$368.83')
(p/'audit_checks.json').write_text(json.dumps({'status':'passed','checks':checks},indent=2))
print('PASS',len(checks),'independent audit check groups')
