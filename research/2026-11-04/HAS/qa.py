from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));mdata=json.load(open(P/'publication.json'));claims=json.load(open(P/'sources/claims.json'));s=(P/'report.md').read_text();count=0
def check(v,msg):
 global count
 assert v,msg
 count+=1
for metric in ['revenue','operating_income','net_income','tax','interest','cfo','capex','sbc']:
 check(math.isclose(sum(q[metric] for q in f['quarters']),f['ttm'][-1][metric],abs_tol=1e-8),metric)
for r in f['annual']+f['quarters']+f['ttm']:
 check(math.isclose(r['owner_cash_proxy'],r['cfo']-r['ppe']-r['software']-r['sbc'],abs_tol=1e-8),'cash proxy')
check(f['quarters'][0]['eps']==1.41,'Q4 EPS')
check(m['capital_bridge']['nominal_debt']==claims['q3_10q']['debt_nominal'],'principal')
b=m['capital_bridge'];check(math.isclose(b['net'],b['cash']+b['treasuries']-sum(b[k] for k in ['operating_cash_reserve','nominal_debt','nci','pension_prior_year_proxy','tax_prior_year_proxy','legacy_environmental']),abs_tol=1e-8),'bridge')
for name,c in m['cases'].items():
 a=c['assumptions'];check(len(c['rows'])==10,'years')
 check(math.isclose(sum(r['pv_fcff'] for r in c['rows']),c['pv_explicit'],abs_tol=1e-8),'PV')
 check(math.isclose(c['value'],(c['pv_explicit']+c['pv_terminal']+b['net'])/a['shares'],abs_tol=1e-8),'DCF')
 for r in c['rows']:
  check(math.isclose(r['fcff'],r['nopat']+r['da']-r['capex']-r['delta_nwc']-r['additional_reinvestment_reserve'],abs_tol=1e-8),'cash bridge')
  check(r['reinvestment']>=r['economic_reinvestment']-1e-8,'funded growth')
  check(r['reinvestment']>=r['explicit_reinvestment']-1e-8,'funded investment')
 check(math.isclose(c['terminal_reinvestment'],max(c['rows'][-1]['revenue']*(1+a['g'])*(a['capex_ratio']-a['da_ratio'])+c['rows'][-1]['revenue']*a['g']*.10,c['terminal_nopat']*a['g']/a['roic']),abs_tol=1e-8),'terminal')
 check(math.isclose(mdata[name],round(c['value'],2),abs_tol=1e-8),'metadata')
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for t in mdata[k]:check(t in s,'exact quote')
check(not mdata['approved_entry'] and not mdata['stage35_approved'],'not entry')
check('reconstrucción nueva' in s and 'MAT' in s and 'no está confirmada' in s,'limits')
check(math.isclose(f['ttm'][-1]['operating_income']-54.5,1283.1,abs_tol=1e-8),'normalized EBIT current')
check(math.isclose(f['ttm'][0]['operating_income']+1021.9+25,820.3,abs_tol=1e-8),'normalized EBIT prior')
print(f'PASS {count} checks: financials, model, source capital, terminal, exact pros/cons and no entry.')
