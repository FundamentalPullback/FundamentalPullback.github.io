from value import *
import math
checks=[]
def check(label,a,b,tol=1e-7):checks.append(dict(check=label,actual=a,expected=b,pass_check=abs(a-b)<=tol))
for n in I['cases']:
 z=value(n);rows=z['rows']
 check(n+' 10years',len(rows),10)
 for r in rows:
  check(n+str(r['year'])+' EBIT',r['ebit'],r['revenue']*r['ebit_margin'])
  check(n+str(r['year'])+' NOPAT',r['nopat'],r['ebit']*(1-z['inputs']['tax']))
  check(n+str(r['year'])+' FCFF',r['fcff'],r['nopat']-r['net_reinvestment'])
  check(n+str(r['year'])+' reinvestment',r['net_reinvestment'],r['ppe_or_aggregate_capex']+(r['acquisition_cash']or 0)+r['nwc_increment']+r['contract_capitalization']+r['dso_stress']-r['da'])
 check(n+' terminalreinvestment',z['terminal_reinvestment'],z['terminal_nopat']*z['inputs']['terminal_g']/z['inputs']['terminal_roic'])
 check(n+' EV',z['enterprise_value'],sum(r['pv_fcff']for r in rows)+z['pv_terminal']+z['pv_stub'])
 check(n+' equity',z['equity_value'],z['enterprise_value']+z['excess_cash']-z['financial_claims'])
 check(n+' price',z['per_share'],z['equity_value']/z['shares'])
 check(n+' terminalcoherence',rows[-1]['net_reinvestment'],rows[-1]['nopat']*z['inputs']['terminal_g']/z['inputs']['terminal_roic'])
 check(n+' DyFlexincluded',rows[0]['dyflex_cash'],210)
 check(n+' funded MAfirstyear',rows[0]['acquisition_cash'],I['base_revenue']*z['inputs']['new_acquired_runrate']*z['inputs']['acquisition_multiple'])
F=json.loads((P/'source_review/financials.json').read_text())
for k in ['revenue','ebit','net_income','cfo','capex','sbc','da_cashflow','acquisition_cash']:
 check('quarterTTM '+k,sum(F[p][k]for p in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026']),F['TTM_2026_09'][k])
check('pricecutoff',I['price'],json.loads((P/'technical.json').read_text())['close'])
check('cashdebtgross',I['cash']+I['short_investments']-I['debt'],0)
check('dilutedpositive',int(shares>I['shares_actual_oct23']),1)
check('sourcechecks',sum(x['status']=='PASS'for x in json.loads((P/'source_review/validation_checks.json').read_text())),23)
o=dict(count=len(checks),failures=sum(not c['pass_check']for c in checks),checks=checks)
(P/'QA.json').write_text(json.dumps(o,indent=2));assert o['failures']==0;print('QA',len(checks),'PASS')
