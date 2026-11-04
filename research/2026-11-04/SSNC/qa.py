import pathlib,json,math,re,subprocess,sys,copy
P=pathlib.Path(__file__).parent
from model import *
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)));assert ok,name
m=json.loads((P/'model_results.json').read_text());v=json.loads((P/'valuation_checks.json').read_text());s=json.loads((P/'summary.json').read_text());p=json.loads((P/'pros_cons.json').read_text());report=(P/'report.md').read_text()
for k,c in m['scenarios'].items():
 check(k+' reproducible',abs(model(c['assumptions'])['value']-c['value'])<1e-10)
 check(k+' ten years',len(c['rows'])==10)
 check(k+' wacc above growth',c['assumptions']['wacc']>c['assumptions']['g'])
 for r in c['rows']:
  check(k+' FCFF identity '+str(r['year']),abs(r['ebita']-r['cash_tax']+r['ordinary_depreciation_software_amortization']-r['ppe_software_capex']-r['delta_wc']-r['additional_economic_investment']-r['fcff'])<1e-8)
  check(k+' capital floor '+str(r['year']),r['net_reinvestment']>=r['minimum_net_investment']-1e-8)
 check(k+' equity bridge',abs(c['ev']+c['excess_cash']-c['claims']-c['equity'])<1e-8)
 for side in ['bear','base','bull']:check('summary '+side,abs(s[side]-m['scenarios'][side]['value'])<1e-10)
check('A119 exactly reconstructed',abs(old_model()-43.68499154518281)<1e-8)
check('migration final',abs(v['migration'][-1]['value']-s['base'])<1e-8)
for side in ['pros','cons']:
 check(side+' count',1<=len(p[side])<=3)
 for i,d in enumerate(p[side]):
  check(f'{side}{i} evidence',d['evidence'] in report)
  check(f'{side}{i} length',len(d['es'])<=320 and len(d['en'])<=360)
  check(f'{side}{i} URL',not d['sourceUrl']or d['sourceUrl']in report)
check('no entry',s['approvedEntry']is False and s['approvedBuyCeiling']is None and s['approvedStop']is None and s['authorizedShares']==0)
check('unknown event date',s['nextEventDate']is None)
check('refinancing not completed','no hay cierre' in report and 'propuesta' in report)
check('no placeholder urls','URLPLACEHOLDER'not in report)
subprocess.run([sys.executable,str(P/'history/calculate.py')],check=True,stdout=subprocess.DEVNULL);subprocess.run([sys.executable,str(P/'history/validate.py')],check=True)
h=json.loads((P/'history/history.json').read_text())['periods'];check('Q4 EPSdirect',h['Q42025']['eps_diluted']==.77);check('Q4 sharesdirect',h['Q42025']['shares_diluted']==251.5);check('TTM summed EPS',h['TTM092026']['eps_diluted']==3.48)
for c in json.loads((P/'peers.json').read_text())['peers']:
 check(c['ticker']+' EV arithmetic',abs(c['price']*c['shares']+c['debt_principal']-c['cash']+c['nci']-c['ev'])<1e-8)
 check(c['ticker']+' EV EBIT arithmetic',abs(c['ev']/c['ebit']-c['ev_ebit'])<1e-8)
(P/'qa.json').write_text(json.dumps(dict(passed=True,count=len(checks),checks=checks),indent=2));print('PASS',len(checks))
