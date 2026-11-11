import sys,json,copy,datetime,pathlib,importlib.util
P=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('prior',P.parent/'prior/model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PRICE=47.28; RF=.0498; ERP=.0441; BETA=1.08
WACC=(RF+BETA*ERP)*.65+.07*(1-.26)*.35
OFFSET=(datetime.date(2026,11,10)-datetime.date(2026,8,1)).days/365.25
b=copy.deepcopy(m.CASES['base']);b['wacc']=WACC
def calc(c):
 r=m.model(c,offset=OFFSET)
 r['upside']=r['price']/PRICE-1
 return r
base=calc(b);gap=320.1-base['rows'][0]['fcff']
def finite(n):return base['price']+sum(gap/(1+WACC)**(t-OFFSET) for t in range(1,n+1))/m.SHARES
out={'price':PRICE,'price_date':'2026-11-10 16:00 EST','status':'WATCH; not prioritized for entry','canonical_fair_value':None,'maximum_entry':None,'stop':None,'new_shares':0,'wacc':WACC,'offset':OFFSET,'balance_date':'2026-08-01','cases':{'base':base,'bear':calc(m.CASES['bear']),'bull':calc(m.CASES['bull'])},'cash_gap':gap,'finite_gap_years':{str(n):finite(n) for n in [1,2,3,5,10]},'finite_two_plus_later_shield':finite(2)+sum(66*.26/(1+WACC)**(t-OFFSET) for t in [3,4,5])/m.SHARES,'sensitivity':[]}
for w in [WACC,.085,.09,.095,.10]:
 for shift in [-.001,0,.001]:
  c=dict(b,wacc=w,margin=[x+shift for x in b['margin']],terminal_margin=b['terminal_margin']+shift)
  out['sensitivity'].append({'wacc':w,'margin_shift':shift,'value':calc(c)['price']})
alt=copy.deepcopy(b);shift=gap/(31500*.74);alt['margin']=[x+shift for x in alt['margin']];alt['terminal_margin']+=shift
out['permanent_gap_margin_value']=calc(alt)['price'];out['equivalent_margin_shift']=shift
out['cash_debt_sensitivity_per_100m']=100/m.SHARES
out['full_awards_base']=m.model(b,offset=OFFSET,shares=m.BASIC+5.814628)['price']
out['same_market_return_erp']=.0935-RF
out['same_market_return_base']=calc(dict(b,wacc=(RF+BETA*(.0935-RF))*.65+.07*.74*.35))['price']
out['break_even_margin_shift']=m.solve(lambda s:calc(dict(b,margin=[x+s for x in b['margin']],terminal_margin=b['terminal_margin']+s))['price'],PRICE,-.005,.01)
out['break_even_wacc']=m.solve(lambda w:-calc(dict(b,wacc=w))['price'],-PRICE,.04,.15)
out['break_even_finite_year_count']=next((n for n in range(1,11) if finite(n)>=PRICE),None)
out['audits']={'prior_base_reproduced':abs(m.OUT['base']['price']-43.71)<.01,'cases_ordered':out['cases']['bear']['price']<base['price']<out['cases']['bull']['price'],'cash_gap':abs(gap-105.78)<1e-8,'no_new_canonical_valuation':out['canonical_fair_value'] is None,'finite_monotone':all(finite(i)<finite(i+1) for i in range(1,10)),'bridge_preserved':base['bridge']==1610,'shares_preserved':base['shares']==62.153154,'no_stale_valuation_date':OFFSET>m.OFFSET,'terminal_g_below_wacc':all(x['wacc']>x['g'] for x in m.CASES.values())}
(P/'results_decision.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['cases','sensitivity']},indent=2));print({k:v['price'] for k,v in out['cases'].items()})
