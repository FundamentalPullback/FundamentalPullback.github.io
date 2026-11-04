import pathlib,json,math,subprocess,sys
from model import *
P=pathlib.Path(__file__).parent;checks=[]
def check(n,b):
 checks.append({'name':n,'pass':bool(b)});assert b,n
m=json.loads((P/'model_results.json').read_text());s=json.loads((P/'summary.json').read_text());r=(P/'report.md').read_text()
check('18 unique ships',len(FLEET)==len(set(n for n,_,_ in FLEET))==18)
check('mix',sum(k=='VLCC' for _,k,_ in FLEET)==8)
for name,a in m['scenarios'].items():
 cfg=SCENARIOS[name];check(name+' reproducible',calculate(cfg)==a);check(name+' summary',s[name]==a['value'])
 for row in a['rows']:
  check(name+str(row['year'])+' cash identity',abs(row['NOPAT']+row['economic_DA']-row['total_capex']-row['working_capital']-row['FCFF'])<1e-8)
  check(name+str(row['year'])+' physical replacement funded',row['total_capex']+1e-8>=row['actual_hull_replacement_net_scrap']+row['drydock_capex'])
  check(name+str(row['year'])+' positive extra investment',row['additional_growth_investment']>=0)
  check(name+str(row['year'])+' PV',abs(row['PV']-row['FCFF']/(1+cfg['wacc'])**row['year'])<1e-8)
 check(name+' equity bridge',abs(a['EV']-a['capital_bridge_estimated']['net_claims']-a['equity'])<1e-8)
 # Independent 500-year discounted tail reproduces analytic perpetual cohort adjustment.
 w=cfg['wacc'];g=cfg['g'];life=cfg['life'];infl=1.02**4*(1+g)**5;renew=sum((REPLACEMENT[k]-SCRAP[k])*cfg['replacement_scale']/life for _,k,_ in FLEET);tv=0
 for j in range(1,501):
  inflation=infl*(1+g)**j;actual=sum((REPLACEMENT[k]-SCRAP[k])*inflation*cfg['replacement_scale']for _,k,y in FLEET if 2036+j>=y+life and(2036+j-y)%life==0)
  cash=a['terminal_fcff']*(1+g)**(j-1)+renew*inflation-actual;tv+=cash/(1+w)**j
 check(name+' 500-year tail matches terminal',abs(tv-a['terminal_value'])<1e-6) if cfg.get('renew',True) else check(name+' finite tail identity',abs(sum(x['PV'] for x in a['finite_tail_rows'])+a['finite_working_capital_release_PV']-a['PV_terminal'])<1e-8)
 check(name+' positive terminal funding',a['terminal_net_reinvestment']>=a['terminal_nopat']*g/cfg['roic']-1e-8)
check('cash no restricted',CAPITAL['June_unrestricted_cash']==222.591472)
check('new vessel payment once',CAPITAL['Vous_remaining_delivery_payment']==79.4)
check('dividend not free',abs(CAPITAL['August_dividend']-204.98443875)<1e-8)
check('cash delta sensitivity',abs((capital(400)['net_claims']-capital(300)['net_claims'])+100)<1e-8)
check('scan distinct',s['scanDate']=='2026-11-03' and s['scanPrice']==93.88 and s['previousScanPrice']==91.18 and s['lastClose']==93.26)
v=json.loads((P/'valuation_checks.json').read_text());check('reverse',abs(v['reverse']['value']-PRICE)<1e-8)
for n,a in enumerate(json.loads((P/'pros_cons.json').read_text())):
 check(str(n)+' evidence',a['evidence']in r);check(str(n)+' es',len(a['text_es'])<=320);check(str(n)+' en',len(a['text_en'])<=360)
check('history QA',subprocess.run([sys.executable,str(P/'history/validate.py')],capture_output=True).returncode==0)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2));print('PASS',len(checks))
