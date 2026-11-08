"""Reproducible historical diagnostics. Not a DCF or approved fair value."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
F=json.loads((P/'financial_inputs.json').read_text())
def fact(tag,start,end):
 a=[x for arr in F.get(tag,{}).get('units',{}).values() for x in arr if x.get('start')==start and x['end']==end and x.get('filed','')<='2026-11-08']
 return sorted(a,key=lambda x:x['filed'])[-1]['val']/1e6 if a else None
T={'net_income':'NetIncomeLoss','pretax_income':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','cfo':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','da':'DepreciationDepletionAndAmortization','interest_incurred':'RealEstateInventoryCapitalizedInterestCostsIncurred','interest_cogs':'RealEstateInventoryCapitalizedInterestCostsCostOfSales1'}
h={}
for year in range(2016,2026):
 h['FY'+str(year)]={k:fact(t,f'{year}-01-01',f'{year}-12-31') for k,t in T.items()}
for year in [2024,2025,2026]:
 h['9M'+str(year)]={k:fact(t,f'{year}-01-01',f'{year}-09-30') for k,t in T.items()}
# Revenue manual source tie-out: official annual 2025 and Q3 2025/2026 releases. USD millions.
for period,home,land,fin in [('FY2023',6056.784,56.229,25.250),('FY2024',6341.546,22.326,31.163),('FY2025',5763.597,60.838,33.202),('9M2024',4745.618,4.970,22.734),('9M2025',4357.148,39.766,24.967),('9M2026',3658.085,28.162,21.566)]:
 h[period].update(home_revenue=home,total_revenue=home+land+fin)
for y in [2025,2026]:
 h['TTM'+str(y)]={k:h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in h['FY2025'] if all(h[x].get(k) is not None for x in ['FY'+str(y-1),'9M'+str(y),'9M'+str(y-1)])}
for d in h.values():
 d['cfo_minus_ppe']=d['cfo']-d['capex'] if d.get('cfo') is not None and d.get('capex') is not None else None
quarters=[{'period':'Q42025','homes':3755,'orders':3224,'home_revenue':1406.449,'gross_margin_pct':16.5,'net_income':84.031,'diluted_eps':1.20,'cfo':118.288-(-125.385),'capex':25.722-20.145}, {'period':'Q12026','homes':2967,'orders':3664,'home_revenue':1107.822,'gross_margin_pct':17.5,'net_income':55.309,'diluted_eps':.82,'cfo':101.309,'capex':4.308},{'period':'Q22026','homes':3725,'orders':3575,'home_revenue':1387.911,'gross_margin_pct':18.3,'net_income':90.630,'diluted_eps':1.37,'cfo':290.781-101.309,'capex':9.876-4.308},{'period':'Q32026','homes':3187,'orders':3083,'home_revenue':1162.352,'gross_margin_pct':17.4,'net_income':67.784,'diluted_eps':1.04,'cfo':259.523-290.781,'capex':13.917-9.876}]
price=68.05;shares=64.423225;book=5044.358;ttm=h['TTM2026'];prior=h['TTM2025']
results={'ticker':'MTH','as_of':'2026-11-08','status':'material_partial','quality_label':'not-decision-ready','stage3_complete':False,'entry_approved':False,'canonical_approved_value':None,'approved_values':{'adverso':None,'central':None,'favorable':None},'price':price,'price_session':'2026-11-06 regular close 16:00 America/New_York','current_basic_shares_m':shares,'shares_as_of':'2026-10-26','book_equity_m':book,'book_value_per_basic_share':book/shares,'price_book':price/(book/shares),'market_cap_m':price*shares,'ttm_earnings_yield_using_current_shares':ttm['net_income']/(price*shares),'ttm_pe_using_current_shares_not_gaap_eps':price*shares/ttm['net_income'],'ttm_net_income_change':ttm['net_income']/prior['net_income']-1,'ttm_home_revenue_change':ttm['home_revenue']/prior['home_revenue']-1,'ttm_cfo_less_ppe_change_m':ttm['cfo_minus_ppe']-prior['cfo_minus_ppe'],'ttm_earnings_on_ending_book':ttm['net_income']/book,'historical':h,'quarters':quarters,'cash_proxy_warning':'CFO minus PPE is levered, includes inventory and interest cash timing; not normalized FCFF. Financing of land and JV investment require reconciliation.','scenario_diagnostics':[]}
# Required ROE under P/B=(ROE-g)/(Ke-g), illustrative steady-state identity, not forecast or target.
for ke in [.10,.11,.12]:
 for g in [0,.02]:results['scenario_diagnostics'].append({'ke_analyst_assumption':ke,'g_analyst_assumption':g,'implied_sustainable_roe':g+results['price_book']*(ke-g),'fair_value':None})
results['extension_artifact']='extended_results.json'
results['confirmed_fundamental_gate']='Net income TTM -45%, home revenue -14.9%, declining orders and margins; recovery unproven, independent of valuation incompleteness'
(P/'results.json').write_text(json.dumps(results,indent=2))
keys=['period']+list(h['FY2025'])
with (P/'historical.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({'period':k,**v} for k,v in h.items())
with (P/'quarters.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(quarters[0]));w.writeheader();w.writerows(quarters)
assert abs(sum(q['net_income'] for q in quarters)-ttm['net_income'])<1e-6
assert abs(sum(q['home_revenue'] for q in quarters)-ttm['home_revenue'])<1e-6
assert abs(sum(q['cfo'] for q in quarters)-ttm['cfo'])<1e-6
assert all(v is None for v in results['approved_values'].values())
(P/'self_check.json').write_text(json.dumps({'historical_ttm_quarters_tie':True,'approved_values_null':True,'source_asof_guard':True,'valuation_model_completed':False,'independent_audit':False},indent=2))
print(json.dumps({k:v for k,v in results.items() if k not in ['historical','quarters','scenario_diagnostics']},indent=2))
