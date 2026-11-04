"""Offline arithmetic, lineage, units and anti-double-count checks."""
import json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(P/'rebuild_history.py')],check=True)
h=json.loads((P/'history.json').read_text());o=json.loads((P/'observations.json').read_text());ids={r['observation_id'] for r in o};checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def v(p,m):return h['periods'][p]['metrics'][m]['value']
for r in o:check(r['source_url'].startswith('https://www.sec.gov/Archives/') and r['unit'] is not None,'primary source and unit '+r['observation_id'])
for p,r in h['periods'].items():
 for m,x in r['metrics'].items():
  if x:check(set(x['observation_ids'])<=ids,p+' '+m+' lineage')
 check(v(p,'fcf_gross_capex')==v(p,'cfo')-v(p,'ppe_capex'),p+' gross-capex FCF')
 check(v(p,'company_fcf')==v(p,'fcf_gross_capex')+v(p,'ppe_sale_proceeds'),p+' company FCF')
 check(v(p,'fcf_after_sbc')==v(p,'fcf_gross_capex')-v(p,'sbc'),p+' SBC cost')
 for m in ['revenue','ebit']:
  z=[s[p][m] for s in h['segments'].values() if s[p][m]]
  check(abs(sum(x['value'] for x in z)-v(p,m))<=2,p+' '+m+' segment reconciliation within rounding')
for m in ['revenue','ebit','net_income','cfo','ppe_capex','sbc','da_ex_financing','acquisition_intangible_amortization']:
 check(abs(sum(v(p,m) for p in ['Q1FY26','Q2FY26','Q3FY26','Q4FY26'])-v('FY26',m))<=1,m+' annual quarter sum within $1m rounding')
 check(v('TTM',m)==v('FY26',m)+v('Q1FY27',m)-v('Q1FY26',m),m+' TTM roll')
for p in ['TTM','PRIOR_TTM']:
 for m in ['basic_shares','diluted_shares','diluted_eps']:check(h['periods'][p]['metrics'][m] is None,p+' '+m+' not inferred')
check(v('Q4FY26','diluted_shares')==480232028,'Q4 weighted diluted shares directly reported')
check(h['balance_sheets']['2026-09-26']['total_debt']['value']==13820,'Sep26 book debt')
check(h['balance_sheets']['2026-09-26']['actual_shares']['value']==491927413,'Sep26 issued minus treasury')
check(v('Q1FY27','ebit')==717,'derivative gain not added to EBIT')
report={'status':'PASS','checks':len(checks),'rounding_tolerance_USD_million':1,'segment_rounding_tolerance_USD_million':2,'note':'Quarterly income and YTD/annual values are independently rounded; FY26 quarter EBIT/NI sum can differ by $1m. This is retained, not forcibly patched.'}
(P/'check_results.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
