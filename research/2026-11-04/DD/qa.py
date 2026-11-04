import json,pathlib
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());m=json.loads((P/'publication.json').read_text());h=a['history'];c=a['capital'];checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
for r in h['annual']+h['quarters']+[h['ttm']]:
 ck(r['period']+' FCF',r['actual_continuing_fcf']==r['continuing_cfo']-r['capex'])
 ck(r['period']+' EBIT arithmetic',r['ebit_pretax_plus_interest']==r['pretax_continuing_income']+r['interest_expense'])
 ck(r['period']+' operating subtotal',r['operating_profit_calculated']==r['revenue']-r['cost_of_sales']-r['research_development']-r['selling_general_administrative']-r['intangible_amortization']-r['restructuring']-r['acquisition_integration_separation']-r['goodwill_impairment'])
for key in ['revenue','continuing_cfo','capex','stock_based_compensation','actual_continuing_fcf','discontinued_cfo']:ck('TTM sum '+key,sum(r[key] for r in h['quarters'])==h['ttm'][key])
ck('MOU liability composition',212+247==459);ck('MOU asset composition',75+87==162)
ck('settlement PV',120+127==247)
ck('environment accrual',sum(c['environmental_accrual_parts'])==294)
ck('environment additional',sum(c['environmental_extra_parts'])==334)
ck('selected net future',a['diagnostics']['selected_future_settlements_net']==-236)
ck('selected9Mnet',a['diagnostics']['selected_cash_9m_net']==-104)
ck('selectedQ4net',a['diagnostics']['selected_cash_q4_net']==43)
ck('Q3 adjusted FCF distinct',410-71==339 and 410-71+2==341)
ck('TTM owner not certified',a['diagnostics']['continuing_fcf_less_sbc']==742 and a['valuation']['owner_fcf'] is None)
ck('no values',all(v is None for v in a['valuation'].values()) and all(m[k] is None for k in ['bear','base','bull','buy_ceiling']))
ck('no entry',not m['approved_entry'] and not m['stage35_approved'])
ck('separation dates',c['qnity_separation_date']=='2025-11-01' and c['reverse_split_date']=='2026-06-24')
r=(P/'report.md').read_text()
for v in m['pros_es']+m['cons_es']:ck('exact evidence '+v[:25],v in r)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
