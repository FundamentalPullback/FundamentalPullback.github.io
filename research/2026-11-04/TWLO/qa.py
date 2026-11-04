import pathlib,json,math
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());p=json.loads((P/'publication.json').read_text());r=(P/'report.md').read_text();checks=[]
def ck(n,v):
 assert v,n
 checks.append({'name':n,'pass':True})
for k,c in m['cases'].items():
 for row in c['rows']:
  ck(k+'_fcff_'+str(row['year']),math.isclose(row['fcff'],row['nopat']+row['da']-row['capex']-row['delta_nwc']-row['delta_commission_assets']-row['additional_reinvestment_reserve'],abs_tol=1e-8));ck(k+'_floor_'+str(row['year']),row['reinvestment']>=max(row['physical_reinvestment'],row['economic_reinvestment'])-1e-8)
 t=c['terminal'];ck(k+'_terminal',math.isclose(t['fcff'],t['nopat']-max(t['physical_reinvestment'],t['economic_reinvestment']),abs_tol=1e-8));ck(k+'_value',math.isclose(c['value'],(c['ev']+c['bridge'])/c['shares'],abs_tol=1e-8));ck(k+'_public',p[k]==round(c['value'],2))
for i,s in enumerate(p['pros_es']+p['cons_es']):ck('exact_evidence_'+str(i),s in r)
ck('bridge',math.isclose(m['cases']['base']['bridge'],690.0557,abs_tol=1e-8));ck('no_entry',not p['approved_entry'] and not p['stage35_approved'] and not p['latestCompleted']);ck('no_forced_root',m['inverse_margin_solution'] is None);ck('no_internal_placeholders','{HISTORY' not in r and '{PEERS}' not in r)
(P/'qa.json').write_text(json.dumps({'pass_count':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'checks pass')
