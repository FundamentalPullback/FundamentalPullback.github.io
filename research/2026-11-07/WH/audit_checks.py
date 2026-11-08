"""Independent arithmetic audit. Run locally; does not revise underwriting assumptions."""
import json, pathlib, importlib.util, hashlib, math
p=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('wh',p/'model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
r=json.loads((p/'results.json').read_text());checks=[]
for n,c in m.SC.items():
 d=m.dcf(c)
 assert math.isclose(d['price'],r['scenarios'][n]['price'],abs_tol=1e-9)
 for row in d['rows']:
  assert math.isclose(row['fcff'],row['nopat']+row['da']+row['dan_amortization']-row['capex_including_software']-row['development_notes_net']-row['development_loans_net']-row['delta_wc'],abs_tol=1e-9)
 for row in d['rows'][9:]: assert math.isclose(row['reinvestment'],row['nopat']*c['g']/c['roic'],abs_tol=1e-9)
 assert math.isclose(d['price']*m.SHARES,d['enterprise_value']-m.DEBT+m.CASH,abs_tol=1e-9)
 checks.append(n+': recalculation, FCFF, terminal and equity bridge PASS')
for x in r['inverse']:
 c=m.SC['central'].copy();c['margin']=x['core_margin_year5'];assert abs(m.dcf(c,shift=x['parallel_growth_shift'])['price']-m.P)<1e-7
checks.append('Inverse solutions reproduce observed price input PASS')
d=m.dcf(m.SC['central']);w=m.WACC
fc=[x['nopat']+x['da']+x['dan_amortization']-x['revenue']*45/1446-x['development_notes_net']-x['development_loans_net']-x['delta_wc'] for x in d['rows']]
ev=sum(x/(1+w)**(i+1) for i,x in enumerate(fc[:10]))+fc[-1]/(w-.025)/(1+w)**10
out={'scope':'Independent mechanical recalculation and preserved primary-document tie-out; external quote/beta/Treasury/ERP pages not independently re-fetched in this audit','checks':checks,'illustrative_audit_sensitivities':{'fixed_45_over_1446_capex_ratio_price':(ev-m.DEBT)/m.SHARES,'additional_annual_flat_10m_reinvestment_price':d['price']-10/w/m.SHARES,'base_plus_100bp_wacc_price':m.dcf(m.SC['central'],w+.01)['price'],'additional_annual_flat_reinvestment_that_erases_20pct_MOS':(d['price']-m.P/.8)*w*m.SHARES},'source_hashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['model.py','results.json']}}
(p/'qa.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
