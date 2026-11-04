import pathlib,json,math
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());p=json.loads((P/'publication.json').read_text());h=json.loads((P/'history/normalized_history.json').read_text())['records'];r=(P/'report.md').read_text();checks=[]
def ck(n,v):
 assert v,n
 checks.append({'name':n,'pass':True})
for n,x in h.items():
 q=x['metrics'];ck(n+'_fcf',q['fcf_company_definition']==q['cfo']+q['ppe_cash_signed']+q['software_cash_signed'])
ck('half_year_bridge',a['cash_quality']['h1_after_intangibles_less_sbc_sensitivity']==265)
ck('cash',a['historical_capital']['cash_plus_short']==2299)
ck('shares_no_double_b',math.isclose(a['historical_capital']['issued_a_plus_b'],174.817))
ck('debt_settled',a['inputs']['debt_remaining']==0 and a['inputs']['paid_june_notes']==350)
for k in ['bear','base','bull','owner_fcf','buy_ceiling','equity_bridge']:ck(k+'_null',p[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+'_false',not p[k])
for i,s in enumerate(p['pros_es']+p['cons_es']):ck('exact_evidence_'+str(i),s in r)
ck('calendar_confirmed','1 de diciembre de 2026' in r)
ck('permiso_unknown',a['inputs']['permiso_consideration'] is None)
ck('scanner_distinct','208,24' in r and '213,00' in r and '189,68' in r)
ck('nonoperating_tieout',h['H1FY2027']['metrics']['ebit_gaap']+h['H1FY2027']['metrics']['interest_other_net']==204)
(P/'qa.json').write_text(json.dumps({'pass_count':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'checks pass')
