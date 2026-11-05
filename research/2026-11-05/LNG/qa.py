from pathlib import Path
import json,math
P=Path(__file__).parent;R=json.loads((P/'results.json').read_text());I=json.loads((P/'model/inputs.json').read_text());C=json.loads((P/'capital.json').read_text());M=json.loads((P/'minority_check.json').read_text());N=json.loads((P/'facts/normalization_extension.json').read_text());checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
def eq(a,b):return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-6)
for name,v in R['cases'].items():
 c=I['cases'][name];check(name+' ten forecast years',len(v['rows'])==10);check(name+' WACC above growth',v['wacc']>v['terminal_growth']);check(name+' no optional expansion',max(c['volume_mtpa'])<=63)
 for r in v['rows']:
  y=str(r['year']);check(name+y+' EBIT after SBC',eq(r['ebit'],r['adjusted_ebitda']-r['sbc']-r['da']));check(name+y+' NOPAT tax',eq(r['nopat'],r['ebit']*(1-r['tax_rate'])));check(name+y+' net reinvestment',eq(r['net_reinvestment'],r['total_capex']-r['da']+r['incremental_wc']));check(name+y+' FCFF',eq(r['fcff'],r['nopat']-r['net_reinvestment']));check(name+y+' PV',eq(r['pv_fcff'],r['fcff']/r['discount_factor']));check(name+y+' positive capital spending',r['total_capex']>=0)
 check(name+' endfade g/ROIC',eq(v['rows'][-1]['net_reinvestment'],v['rows'][-1]['nopat']*v['terminal_growth']/v['terminal_roic']));check(name+' terminal continuity',eq(v['terminal_fcff'],v['rows'][-1]['fcff']*(1+v['terminal_growth'])));check(name+' terminal Gordon',eq(v['terminal_value'],v['terminal_fcff']/(v['wacc']-v['terminal_growth'])));check(name+' PVsum',eq(v['ev'],sum(r['pv_fcff']for r in v['rows'])+v['pv_terminal']));check(name+' equity bridge once',eq(v['equity'],v['ev']-v['nominal_debt']-v['finance_leases']+v['cash_excess_proxy']+v['post_quarter_cash_adjustment']-v['nci_market_equity']));check(name+' shares',eq(v['value_per_share'],v['equity']/v['shares']));check(name+' no cash distributions subtracted from FCFF','outside_nci_distribution'not in v['rows'][0]);check(name+' transient not terminal',c['temporary_marketing_premium'][-1]==0)
 for r in M[name]['rows']:
  check(name+str(r['year'])+' CQP allocation sums',eq(r['outside']+r['parent'],r['cash_available']));check(name+str(r['year'])+' CQP funded',r['unfunded_cash_deficit']==0)
check('outside CQP units',eq(C['capital']['cqp_outside_units_m'],(484057704-239872502)/1e6));check('outside CQP market',eq(C['capital']['nci_market_equity'],244.185202*56.68));check('LNG current diluted proxy',eq(C['capital']['shares_proxy_m'],204.203914+.6));check('financial debt',C['capital']['total_financial_debt']==24138+1385);check('WACC',eq(C['capital']['wacc'],C['capital']['cost_equity']*(1-C['capital']['debt_weight'])+C['capital']['cost_debt']*(1-C['capital']['taxshield_rate'])*C['capital']['debt_weight']));check('2029 normal anchor',eq(R['cases']['base']['rows'][2]['adjusted_ebitda'],7650));check('2027 locked margin premium',eq(I['cases']['base']['temporary_marketing_premium'][0],4*52*(10-2.75)));check('committed base project capex1625',sum(I['cases']['base']['growth_capex'])==1625)
for k in ['FY2025','FY2024','Q42025','Q42024']:
 d=N[k];check(k+' EBITDA bridge',eq(d['gaap_ebit']-d['fair_value_gains']+d['da']+d['noncash_comp_adjustment']+d['other_addback'],d['adj_ebitda']))
check('normalizedTTMEBIT6073',N['TTM2026']['limited_ebit']==6073);check('normalizedTTMEBITDA7714',N['TTM2026']['adj_ebitda_after_credit']==7714)
from model import value
for w in [.05,.06,.07,.08]:check('WACC monotonic'+str(w),value(I['cases']['base'],wacc=w)['value_per_share']>value(I['cases']['base'],wacc=w+.001)['value_per_share'])
check('reverse WACC matchesprice',eq(value(I['cases']['base'],wacc=R['reverse']['wacc'])['value_per_share'],C['capital']['price']));check('reverse EBITDA matchesprice',eq(value(I['cases']['base'],unit_profit_scale=R['reverse']['normalized_ebitda_multiplier'])['value_per_share'],C['capital']['price']))
T=json.loads((P/'technical.json').read_text());check('technical latestsession',T['date']=='2026-11-04');check('technical close',eq(T['close'],292.02));check('technical overlap',T['overlap_rows']==49 and T['max_overlap_ohlc_difference']<.021);check('long trend supportive',T['long_trend_supportive']);check('entry not approved',T['technical_entry_approved']is False)
(P/'QA.json').write_text(json.dumps(dict(status='author_checks_passed_independent_review_attached',count=len(checks),checks=checks),indent=2));print(len(checks),'author checks passed')
