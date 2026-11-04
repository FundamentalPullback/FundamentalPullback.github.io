import pathlib,json,math
p=pathlib.Path(__file__).parent;h=json.loads((p/'history/history.json').read_text())['periods'];a=json.loads((p/'analysis.json').read_text());m=json.loads((p/'publication.json').read_text());r=(p/'report.md').read_text();c=[]
def ck(n,v):
 assert v,n
 c.append({'name':n,'pass':True})
for k,v in h.items():ck(k+'_fcf',math.isclose(v['fcf'],v['cfo']-v['capex'],abs_tol=1e-6))
for key in ['revenue','ebit_operating','cfo','capex','sbc','fcf']:
 ck(key+'_fourquarters',math.isclose(sum(h[k][key] for k in ['Q42025','Q12026','Q22026','Q32026']),h['TTM20260930'][key],abs_tol=1e-5))
ck('factoring_bridge',a['cash_quality']['ttm_fcf_less_receivables_financing']==512.87)
ck('sbc_sensitivity',a['cash_quality']['ttm_fcf_less_receivables_financing_sbc_sensitivity']==456.111)
ck('scf_increase',a['cash_quality']['scf_balance_increase_9m']==65.538)
ck('carrying_debt',a['capital_arithmetic_not_valuation']['debt_carrying']==5110.237)
ck('asbestos_net',a['capital_arithmetic_not_valuation']['net_asbestos_pv']==247)
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge']:ck(k+'_null',m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+'_false',not m[k])
for i,s in enumerate(m['pros_es']+m['cons_es']):ck('exact_evidence_'+str(i),s in r)
ck('dates_distinct','130,18' in r and '124,27' in r)
ck('no_pension_double_add','Añadir 741,967 al EBIT operativo sería doble cómputo.' in r)
ck('split_not_closed','Los estados actuales no reflejan la escisión.' in r)
ck('calendar_unknown',a['inputs']['next_exact_earnings_date'] is None)
(p/'qa.json').write_text(json.dumps({'pass_count':len(c),'checks':c},indent=2)+'\n');print(len(c),'checks pass')
