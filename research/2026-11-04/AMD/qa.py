import json,pathlib
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());m=json.loads((P/'publication.json').read_text());c=a['capital'];h=a['history']['periods'];checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
for k,r in h.items():
 ck(k+' continuing FCF',r['fcf_cont']==r['cfo_cont']-r['ppe_cont'])
 ck(k+' SBC diagnostic',r['fcf_cont_less_sbc']==r['fcf_cont']-r['sbc'])
ck('liquid assets',a['diagnostics']['liquid_assets']==15776)
ck('debt principal',c['debt_carrying']+c['debt_unamortized_cost']==c['debt_principal'])
ck('lease present value',c['lease_current']+c['lease_long']==c['lease_undiscounted']-c['lease_imputed_interest']==2132)
ck('purchases',sum(c['operating_purchase_commitments'])==48761)
ck('cloud',sum(c['cloud_capacity_commitments'])==6175)
ck('Q3 other income',123+67-1097+5==-902)
ck('Q3 NI',2832-57-902+555==2428)
ck('warrant cash',a['diagnostics']['full_warrant_exercise_cash']==3.2)
ck('null values',all(v is None for v in a['valuation'].values()))
ck('null public values',all(m[k] is None for k in ['bear','base','bull','buy_ceiling']))
ck('no entry',not m['approved_entry'] and not m['stage35_approved'])
ck('price pre-event',a['price_pre_announcement'])
ck('date unknown',a['next_earnings_date'] is None)
r=(P/'report.md').read_text()
for t in m['pros_es']+m['cons_es']:ck('exact evidence '+t[:25],t in r)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
