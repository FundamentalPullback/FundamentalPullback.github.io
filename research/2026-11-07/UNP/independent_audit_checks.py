"""Independent arithmetic/tie-out checks. Does not execute or overwrite author model."""
import json, math, hashlib
from pathlib import Path
P=Path(__file__).parent
r=json.loads((P/'results.json').read_text())
checks=[]
def check(name,actual,expected,tol=1e-7):
 checks.append(dict(check=name,actual=actual,expected=expected,passed=abs(actual-expected)<=tol))
def dcf(g,m5,m10,c,w,gt,roic):
 rev=26363.; pv=0
 for t in range(1,11):
  old=rev; rev*=1+(g if t<=5 else g+(gt-g)*(t-5)/5)
  margin=10565/26363+(m5-10565/26363)*t/5 if t<=5 else m5+(m10-m5)*(t-5)/5
  cf=rev*(margin*.76+.097-c)-.05*(rev-old)
  pv+=cf/(1+w)**t
 term_nopat=rev*(1+gt)*m10*.76
 reinvestment=max(term_nopat*gt/roic,rev*(1+gt)*(c-.097)+.05*rev*gt)
 ev=pv+(term_nopat-reinvestment)/(w-gt)/(1+w)**10
 env=sum(amount/(1+.086085)**t for t,amount in [(1,65),(2,52.25),(3,52.25),(4,52.25),(5,52.25)])
 return (ev-30324+3086-1500+2000-env)/594.5
w=(.0486+.85*.0441)*(290.16*594.5)/(290.16*594.5+22800)+.0575*.76*22800/(290.16*594.5+22800)
for name,args in [('adverso',(.02,.38,.37,.16,.09,.02,.12)),('central',(.045,.415,.40,.145,w,.025,.15)),('favorable',(.065,.44,.43,.14,.0725,.03,.18))]:check('independent_UNP_'+name,dcf(*args),r['cases'][name]['value'])
check('WACC',w,r['wacc_derived'])
# Source actuals: annual2025 - 9M2025 + 9M2026, UNP 10-K & Q3 10-Q.
for k,a,b,c in [('revenue',24510,18425,20278),('EBIT',9846,7445,8164),('net_income',7138,5290,5770),('DA',2465,1841,1914),('CFO',9290,7065,8302),('cash_capex',3791,2792,2834)]:check('UNP_TTM_'+k,a-b+c,r['TTM'][k])
check('FCFF_normalized',10565*.76+2538-3833-100,r['TTM']['normalized_start_FCFF'])
# NSC independently built DCF.
rev=12963.;pv=0
for t in range(1,11):
 old=rev;rev*=1+.04+(.025-.04)*max(0,(t-5)/5)
 margin=4088/12963+(.355-4088/12963)*min(t/5,1)
 pv+=(rev*(margin*.76+.11-.175)-.05*(rev-old))/(1.085)**t
terminal_nopat=rev*1.025*.355*.76
nsc_reinvest=max(terminal_nopat*.025/.13,rev*1.025*(.175-.11)+.05*rev*.025)
nsc_eq=pv+(terminal_nopat-nsc_reinvest)/(.085-.025)/1.085**10-16613+1598-750-(373+277+125+534)
check('NSC_equity',nsc_eq,r['NSC']['equity'])
check('cash_consideration',225*88.82,r['merger']['cash_consideration_from_share_estimate'])
# Recalculate dated closing bridge without running author model.
for key,f,close,cost,remedy in [('close_full_claim',1,1,3000,0),('close_half_synergies_remedies',.5,1,4000,200),('delay_two_years',1,3,4000,0)]:
 expected=r['merger']['conditional_outcomes'][key]
 sy=0
 for t in range(1,31):
  ramp=min(t/3,1); cash=2750*f*ramp*.66-remedy*ramp-((2100+cost)/3 if t<=3 else 0)
  sy+=cash/1.085**t
 sy+=(2750*f*.66-remedy)/.085/1.085**30
 cu=3086.;cn=1598.;divpv=0
 for t in range(1,close+1):
  uf=r['cases']['central']['rows'][t-1]['fcff'];nf=r['NSC']['rows'][t-1]['fcff']
  env=65 if t==1 else 52.25 if t<=5 else 0
  cu+=uf-1270*.76-3312-env;cn+=nf-782*.76-1215
  divpv+=3312/1.086085**t
 used=min(19984.5,max(0,cu-1500)); debt=30324+16613+19984.5-used; cash=cu+cn-used
 evu=r['cases']['central']['EV']*(1+w)**close-sum(row['fcff']*(1+w)**(close-row['year']) for row in r['cases']['central']['rows'] if row['year']<=close)
 evn=r['NSC']['EV']*1.085**close-sum(row['fcff']*1.085**(close-row['year']) for row in r['NSC']['rows'] if row['year']<=close)
 env_remaining=sum((65 if t==1 else 52.25)/1.086085**(t-close) for t in range(close+1,6))
 eq=evu+evn+sy-debt+cash-2250+2000-1309-env_remaining
 value=divpv/594.5+eq/819.5/1.086085**close
 for label,actual in [('current_old_share_value',value),('closing_equity',eq),('remaining_UNP_EV_at_close',evu),('remaining_NSC_EV_at_close',evn),('postclose_gross_cash',cash),('postclose_gross_debt',debt),('UNP_cash_used_at_close',used),('new_debt_at_close',19984.5-used),('remaining_UNP_environment_PV_at_close',env_remaining),('preclose_distributions_PV',divpv),('net_synergy_value_at_close',sy)]:check(key+'_'+label,actual,expected[label])
 check(key+'_purchase_funding_identity',expected['UNP_cash_used_at_close']+expected['new_debt_at_close'],19984.5)
# Environmental bounded sensitivities: fraction of overlap and tax deductibility, not evidence of actual tax treatment.
envpv=sum((65 if t==1 else 52.25)/1.086085**t for t in range(1,6))
check('environmental_schedule_total',65+4*52.25,274)
check('environmental_PV',envpv,r['environmental_claim_bridge']['PV_deduction'])
envs=[{'overlap_fraction':overlap,'tax_rate_if_deductible':tax,'PV_deduction':envpv*(1-overlap)*(1-tax),'central_value':r['cases']['central']['value']+envpv*(1-(1-overlap)*(1-tax))/594.5} for overlap in [0,.5,1] for tax in [0,.24]]
# Terminal physical capex is D&A + g/ROIC reinvestment minus incremental WC.
terminal_checks=[]
for name,v in r['cases'].items():
 row=v['rows'][-1];rev11=row['revenue']*(1+v['gt']);wc=.05*(rev11-row['revenue']);capex=rev11*.097+v['terminal_reinvestment']-wc
 terminal_checks.append(dict(case=name,implied_terminal_capex=capex,implied_terminal_capex_ratio=capex/rev11,explicit_capex_ratio=v['capex_ratio'],terminal_ROIC=v['terminal_ROIC']))
nsc_terminal_capex_ratio=max(.175,.11+.355*.76*.025/.13-.05*.025/1.025)
for case in terminal_checks:
 check('terminal_floor_'+case['case'],max(0,case['explicit_capex_ratio']-case['implied_terminal_capex_ratio']),0)
check('NSC_terminal_floor',nsc_terminal_capex_ratio,.175)
check('environment_per_share',envpv/594.5,r['environmental_claim_bridge']['per_share_zero_overlap'])
out={'environmental_overlap_tax_sensitivities':envs,'checks':checks,'all_arithmetic_checks_pass':all(x['passed'] for x in checks),'terminal_physical_capex':terminal_checks,'NSC_implied_terminal_capex_ratio':nsc_terminal_capex_ratio,'NSC_explicit_capex_ratio':.175,'source_TTM_NSC':{'revenue':12180-9206+9989,'EBIT':4356-3419+3151,'net_income':2873-2229+2040,'DA':1393-1040+1073,'CFO':4361-3298+2720,'capex':2204-1475+1407,'interest':792-597+587},'incident_CFO_swing':-345-227,'UNP_environmental_claim_full_undiscounted_sensitivity_per_share':274/594.5,'author_artifact_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['model.py','results.json','financials_annual.csv','financials_quarterly.csv']}}
(P/'independent_audit_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['all_arithmetic_checks_pass']
