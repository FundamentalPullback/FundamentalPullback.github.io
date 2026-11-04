from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());m=json.loads((p/'model.json').read_text());u=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text());checks=[]
def ck(n,b):checks.append({'check':n,'pass':bool(b)});assert b,n
def eq(n,a,b):ck(n,abs(a-b)<1e-6)
eq('finance lease TTM',f['fy26_finance_lease_additions']+f['q1_finance_lease_additions']-f['q1_finance_lease_additions_prior'],f['new_finance_lease_ttm']);eq('EBIT anchor',f['ebit_ttm']-f['lease_gain_ttm'],f['ebit_anchor']);eq('credit availability',f['revolver_limit']-f['revolver_debt']-f['revolver_lc'],f['available_revolver'])
for k,c in m['cases'].items():
 ck(k+'10years',len(c['rows'])==10);s=c['assumptions'];prev=f['ebit_anchor']*(1-s['tax'])
 for r in c['rows']:
  n=k+str(r['year']);eq(n+'NOPAT',r['ebit']*(1-r['tax']),r['nopat']);eq(n+'physical',r['capex']+r['new_finance_lease_assets']-r['da']+r['delta_nwc'],r['physical_reinvestment']);eq(n+'economic',max(0,r['nopat']-prev)/s['roic'],r['economic_reinvestment']);eq(n+'fcff',r['nopat']+r['da']-r['capex']-r['new_finance_lease_assets']-r['delta_nwc']-r['additional_reinvestment_reserve'],r['fcff']);eq(n+'max',r['nopat']-max(r['physical_reinvestment'],r['economic_reinvestment']),r['fcff']);ck(n+'nonnegative reserve',r['additional_reinvestment_reserve']>=-1e-8);eq(n+'discount',r['pv'],r['fcff']/(1+s['wacc'])**r['year']);prev=r['nopat']
 t=c['terminal'];eq(k+'terminal economic',max(0,t['nopat']-prev)/s['roic'],t['economic_reinvestment']);eq(k+'terminal floor',t['reinvestment'],max(t['physical_reinvestment'],t['economic_reinvestment']));eq(k+'terminalfcff',t['fcff'],t['nopat']-t['reinvestment']);eq(k+'TV',t['value'],t['fcff']/(s['wacc']-s['g']));eq(k+'EV',c['ev'],sum(r['pv'] for r in c['rows'])+t['pv']);eq(k+'equity',c['equity'],c['ev']+c['bridge']);eq(k+'per share',c['value_per_share'],c['equity']/f['shares_diluted_q1']);eq(k+'metadata',u[{'bear':'bear','base':'base','bull':'bull'}[k]],c['value_per_share'])
eq('bridge',m['cases']['base']['bridge'],-559.3);eq('reverse',m['reverse_value'],f['price']);ck('reverse bracket',m['reverse_sweep'][0]['value']<=f['price']<=m['reverse_sweep'][-1]['value']);ck('reverse monotonic sweep',all(b['value']>=a['value']-1e-8 for a,b in zip(m['reverse_sweep'],m['reverse_sweep'][1:])));ck('reverse funding not assured',m['reverse_funding_assured'] is False);ck('reverse funding gap visible',m['reverse_first_year_fcff'] < -(f['cash']+f['available_revolver']))
ck('capex sensitivity reduces value',m['sensitivities']['capex_plus_1pp']<m['cases']['base']['value_per_share']);eq('buybackreserve sensitivity',m['sensitivities']['no_postquarter_buyback_reserve']-m['cases']['base']['value_per_share'],65/43)
for k in ['approved_entry','stage35_approved','latestCompleted','bridge_certified','wacc_calibrated']:ck(k+' false',u[k] is False)
for k in ['buy_ceiling','owner_fcf']:ck(k+'null',u[k] is None)
ck('nextdate unknown',f['next_earnings_date'] is None);ck('closeunknown',f['certified_close'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 ck(k+'3items',len(u[k])==3)
 for s in u[k]:ck('exact '+s[:30],s in (p/'report.md').read_text())
for r in h['rows']:eq('FCF '+r['period'],r['cfo']-r['capex_ppe'],r['fcf_ppe'])
for token in ['{HISTORY_TABLE}','{MODEL_RESULTS}']:ck('no placeholder'+token,token not in (p/'report.md').read_text())
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
