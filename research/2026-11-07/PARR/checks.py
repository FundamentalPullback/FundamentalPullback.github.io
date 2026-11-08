import pathlib,json,math,csv
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());r=json.loads((P/'results.json').read_text());m=json.loads((P/'market.json').read_text());c=[]
def ck(n,b):c.append({'check':n,'pass':bool(b)})
ck('3 annuals',len(h['annual'])==3);ck('4 quarters',len(h['quarters'])==4);ck('paired TTM',len(h['paired_ttm'])==2)
for k in ['revenue','ebit','net_income','cfo','da','sbc','capex','turnaround_cash']:
 ck('TTM26 sum4Q '+k,abs(sum(q[k] for q in h['quarters'].values())-h['paired_ttm']['2026'][k])<1e-6)
ck('actual attributable Q3 NI',h['quarters']['q3_26']['net_income']==353.310);ck('actual negative Q1 CFO',h['quarters']['q1_26']['cfo']==-40.707)
ck('TTM prior net identity',abs(h['paired_ttm']['2025']['net_income']-235.996)<1e-6)
ck('price corroborated',abs(m['price']-68.06)<.001);ck('cap2bn',m['cap']>=2000)
ck('not technical approval',m['ema_pass']==False);ck('approved fair value null',r['approved_fair_value'] is None);ck('entry null',r['approved_entry'] is None)
for n,v in r['cases'].items():
 rows=v['rows'];ck(n+'finite horizon',len(rows)==v['inputs']['life']);ck(n+'funded stocks',all(x['physical_close']>=0 and x['turnaround_close']>=0 and x['intangible_close']>=0 for x in rows));ck(n+'no WC release',all(x['incremental_wc']>=0 for x in rows));ck(n+'EBIT after dynamic DA',all(abs(x['ebit']-(x['cash_ebitda']-x['physical_da']-x['turnaround_amort']-x['intangible_amort']))<1e-6 for x in rows));ck(n+'no perpetual TV',abs(sum(x['pv'] for x in rows)-v['closure_pv']-v['enterprise_conditional'])<1e-6);ck(n+'capacity219',all(x['mbpd']<=219 for x in rows));ck(n+'maintenance floor',all(x['physical_capex']>=110*1.02**(x['year']-1)-1e-6 for x in rows))
 with (P/(n+'_cashflows.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(P/'checks.json').write_text(json.dumps({'all_pass':all(x['pass'] for x in c),'checks':c},indent=2));print(len(c),all(x['pass'] for x in c));assert all(x['pass'] for x in c)
