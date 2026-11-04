import pathlib,json,math
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());p=json.loads((P/'publication.json').read_text());r=(P/'report.md').read_text();checks=[]
def ck(name,condition):
 assert condition,name
 checks.append({'name':name,'pass':True})
for name,c in m['cases'].items():
 for row in c['rows']:
  ck(name+'_fcff_'+str(row['year']),math.isclose(row['fcff'],row['nopat']+row['da']-row['capex']-row['delta_nwc']-row['delta_contract_assets']-row['additional_reinvestment_reserve'],abs_tol=1e-8))
  ck(name+'_floor_'+str(row['year']),row['reinvestment']>=row['physical_reinvestment']-1e-8 and row['reinvestment']>=row['economic_reinvestment']-1e-8)
 t=c['terminal'];ck(name+'_terminal',math.isclose(t['fcff'],t['nopat']-max(t['physical_reinvestment'],t['economic_reinvestment']),abs_tol=1e-8));ck(name+'_value',math.isclose(c['value'],(c['ev']+c['bridge'])/c['shares'],abs_tol=1e-8));ck(name+'_public',p[name]==round(c['value'],2))
for i,t in enumerate(p['pros_es']+p['cons_es']):ck('exact_evidence_'+str(i),t in r)
ck('no_entry',not p['approved_entry'] and not p['stage35_approved'] and not p['latestCompleted']);ck('cash_bridge',math.isclose(m['cases']['base']['bridge'],3495.465,abs_tol=1e-8));ck('no_forced_root',m['inverse_margin_solution'] is None);ck('new_date_separate','128,11' in r and '174,08' in r and '129,00' in r)
(P/'qa.json').write_text(json.dumps({'checks':checks,'pass_count':len(checks)},indent=2)+'\n');print(len(checks),'checks passed')
