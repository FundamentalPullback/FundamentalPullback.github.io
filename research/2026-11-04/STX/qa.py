import pathlib,json,math
P=pathlib.Path(__file__).parent;M=json.loads((P/'model.json').read_text());H=json.loads((P/'history/financial_history.json').read_text());A=json.loads((P/'publication.json').read_text());R=(P/'report.md').read_text();C=[]
def ck(n,v):
 assert v,n
 C.append({'name':n,'pass':True})
for r in H:ck(r['period']+'_fcf',math.isclose(r['fcf'],r['cfo']-r['capex'],abs_tol=1e-6))
for k,c in M['cases'].items():
 ck(k+'_ten_years',len(c['years'])==10)
 for r in c['years']:
  ck(k+str(r['year'])+'_fcff',math.isclose(r['fcff'],r['nopat']+r['da']-r['capex']-r['delta_nwc']-r['additional_reinvestment_reserve'],abs_tol=1e-7))
  ck(k+str(r['year'])+'_physical_floor',r['reinvestment']+1e-7>=r['physical_reinvestment'])
  ck(k+str(r['year'])+'_economic_floor',r['reinvestment']+1e-7>=r['economic_reinvestment'])
 ck(k+'_terminal_physical_floor',c['terminal']['reinvestment']+1e-7>=c['terminal']['physical_reinvestment'])
 ck(k+'_terminal_economic_floor',c['terminal']['reinvestment']+1e-7>=c['terminal']['economic_reinvestment'])
 ck(k+'_equity',math.isclose(c['value']*c['shares'],c['ev']+c['bridge'],abs_tol=1e-7))
 ck(k+'_metadata',A[k]==round(c['value'],2))
ck('bridge',math.isclose(M['cases']['base']['bridge'],-2740.92,abs_tol=1e-7))
for k in ['buy_ceiling','owner_fcf']:ck(k+'_null',A[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+'_false',not A[k])
for i,s in enumerate(A['pros_es']+A['cons_es']):ck('evidence'+str(i),s in R)
ck('no_forced_reverse_root',len(M['reverse_margin']['roots'])==0)
ck('restricted_separate','no se restan también de esos 1.258' in R)
ck('redemption_not_cash_premium','Esa pérdida no es una prima de caja exacta' in R)
ck('sbc_not_double','no resta SBC por segunda vez' in R)
(P/'qa.json').write_text(json.dumps({'pass_count':len(C),'checks':C},indent=2)+'\n');print(len(C),'checks pass')
