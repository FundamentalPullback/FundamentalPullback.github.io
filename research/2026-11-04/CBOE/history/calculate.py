#!/usr/bin/env python3
"""Reproduce the CBOE history from inputs.json only; no network or raw filings needed."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def r(x,n=6):return round(x,n)
def writecsv(path,rows):
 keys=[]
 for row in rows:
  for key in row:
   if key not in keys:keys.append(key)
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def calculate(data):
 periods={k:{'period':k,'period_start':v['period_start'],'period_end':v['period_end'],'period_type':v['period_type'],**{m:f['value'] for m,f in v['facts'].items()}} for k,v in data['periods'].items()}
 provenance=[]
 for pid,p in data['periods'].items():
  for m,f in p['facts'].items():provenance.append({'period':pid,'metric':m,**f,'url':data['sources'][f['source_id']]['url'],'currency':'USD','units':'USD/share' if m.startswith('eps') else 'million shares' if m.startswith('shares') else 'USD million','confidence':'high','retrieved_at':data['sources'][f['source_id']]['retrieved_at']})
 # CFO/capex/SBC are cumulative in 10-Qs; subtract YTD periods, never annualize one quarter.
 cf_metrics=[m for m in periods['9M2026'] if m not in periods['Q3_2026'] and m not in ['period','period_start','period_end','period_type']]
 cf_derivations={'Q4_2025':('FY2025','9M2025'),'Q4_2024':('FY2024','9M2024'),'Q2_2026':('6M2026','Q1_2026'),'Q2_2025':('6M2025','Q1_2025'),'Q3_2026':('9M2026','6M2026'),'Q3_2025':('9M2025','6M2025')}
 for pid,(high,low) in cf_derivations.items():
  for m in cf_metrics:
   periods[pid][m]=r(periods[high][m]-periods[low][m])
   provenance.append({'period':pid,'metric':m,'value':periods[pid][m],'evidence':'derived_calculation','formula':f'{high}.{m} - {low}.{m}','source_id':';'.join(sorted({data['periods'][high]['facts'][m]['source_id'],data['periods'][low]['facts'][m]['source_id']})),'currency':'USD','units':'USD million','confidence':'high'})
 for pid,p in periods.items():
  a={m:v['value'] for m,v in data['adjustments'].get(pid,{}).items()}
  p.update(a)
  for m in ['contingent_remeasurement','digital_syndication','cat_note_reserve','restructuring_ex_impairment']:p.setdefault(m,0.)
  if 'restructuring_incl_impairment' in p:p['restructuring_ex_impairment']=r(p['restructuring_incl_impairment']-p['impairment'])
  p['capex_cash']=r(-p['capex_cash_signed'])
  p['cfo_ex_clearing']=r(p['cfo']-p['clearing_customer_cash_flow'])
  p['reported_cfo_less_capex_not_corporate_fcf']=r(p['cfo']-p['capex_cash'])
  p['cash_generation_ex_clearing_proxy']=r(p['cfo_ex_clearing']-p['capex_cash'])
  p['cash_generation_ex_clearing_less_sbc_proxy']=r(p['cash_generation_ex_clearing_proxy']-p['sbc'])
  p['cfo_ex_clearing_and_section31_payable_sensitivity']=r(p['cfo_ex_clearing']-p['section31_payable_flow'])
  p['normalized_ebit_conservative']=r(p['ebit']-p['divestiture_gain']+p['impairment']+p['contingent_remeasurement'])
  p['normalized_ebit_exit_cost_sensitivity']=r(p['normalized_ebit_conservative']+p['restructuring_ex_impairment']+p['digital_syndication'])
  p['normalized_ebit_exit_and_cat_sensitivity']=r(p['normalized_ebit_exit_cost_sensitivity']+p['cat_note_reserve'])
  p['normalized_eps']=None
  p['net_revenue_margin_on_gross']=r(p['net_revenue']/p['gross_revenue'])
  p['ebit_margin_on_net_revenue']=r(p['ebit']/p['net_revenue'])
  p['normalized_ebit_margin']=r(p['normalized_ebit_conservative']/p['net_revenue'])
  p['net_income_common_margin_on_net_revenue']=r(p['net_income_common']/p['net_revenue'])
  p['effective_tax_rate']=r(p['income_tax']/p['pretax_income'])
  p['cash_conversion_ex_clearing_to_common_income']=r(p['cash_generation_ex_clearing_proxy']/p['net_income_common'])
 # Aggregate additive income/cash items; EPS is explicitly sum of quarterly reported EPS, not reported TTM EPS.
 for pid,fy,now,prior,quarters,start,end in [
 ('TTM2026Q3','FY2025','9M2026','9M2025',['Q4_2025','Q1_2026','Q2_2026','Q3_2026'],'2025-10-01','2026-09-30'),
 ('TTM2025Q3','FY2024','9M2025','9M2024',['Q4_2024','Q1_2025','Q2_2025','Q3_2025'],'2024-10-01','2025-09-30')]:
  p={'period':pid,'period_start':start,'period_end':end,'period_type':'TTM','formula':f'{fy} + {now} - {prior}','quarterly_eps_method':'Sum of four separately reported quarterly EPS; source rounding and dilution can differ from FY + YTD - prior YTD EPS.'}
  skip=['period','period_start','period_end','period_type','normalized_eps','net_revenue_margin_on_gross','ebit_margin_on_net_revenue','normalized_ebit_margin','net_income_common_margin_on_net_revenue','effective_tax_rate','cash_conversion_ex_clearing_to_common_income']
  for m,x in periods[fy].items():
   if m in skip or m.startswith('eps') or m.startswith('shares'):continue
   if isinstance(x,(int,float)) and m in periods[now] and m in periods[prior]:p[m]=r(x+periods[now][m]-periods[prior][m])
  p['eps_diluted_quarterly_sum']=r(sum(periods[q]['eps_diluted'] for q in quarters),2)
  p['eps_basic_quarterly_sum']=r(sum(periods[q]['eps_basic'] for q in quarters),2)
  p['shares_diluted_four_quarter_average_proxy']=r(sum(periods[q]['shares_diluted'] for q in quarters)/4)
  p['normalized_eps']=None
  for m,n,d in [('net_revenue_margin_on_gross','net_revenue','gross_revenue'),('ebit_margin_on_net_revenue','ebit','net_revenue'),('normalized_ebit_margin','normalized_ebit_conservative','net_revenue'),('net_income_common_margin_on_net_revenue','net_income_common','net_revenue'),('effective_tax_rate','income_tax','pretax_income'),('cash_conversion_ex_clearing_to_common_income','cash_generation_ex_clearing_proxy','net_income_common')]:p[m]=r(p[n]/p[d])
  periods[pid]=p
 # Balance-sheet and liquidity are point-in-time; never sum balance sheets into TTM.
 bs=[]
 for date,rec in data['balance_sheets'].items():
  p={'date':date,**{m:f['value'] for m,f in rec['facts'].items()}}
  p['debt_carrying']=r(p['debt_current']+p['debt_noncurrent'])
  p['cash_bs_less_embedded_restriction']=r(p['cash_bs']-(5. if date=='2024-12-31' else 0))
  bs.append(p)
 l=data['liquidity_facts']
 liquid={'date':'2026-09-30',**l,'corporate_cash_plus_unmatched_financial_investments_ex_hfs':r(l['latest_cash_bs']+l['latest_financial_investments']-l['latest_deferred_comp_assets']),'other_restricted_cash_excluded':l['latest_other_restricted_cash'],'canada_hfs_cash_excluded':l['latest_cash_held_for_sale'],'clearing_and_customer_cash_excluded':r(l['latest_clearing_restricted_cash']+l['latest_customer_bank_deposits']),'minimum_regulatory_capital_is_not_additive_to_a_combined_operating_regulatory_reserve':True,'section31_liability':46.9,'section31_cash_collected_reported':0.,'section31_treatment':'Retain operating payable; do not mechanically subtract $46.9m from cash because issuer says zero Section31 cash collected. An equal uncollected receivable is plausible but not separately quantified.'}
 liquid['cash_after_minimum_regulatory_capital_proxy']=r(liquid['corporate_cash_plus_unmatched_financial_investments_ex_hfs']-l['latest_minimum_regulatory_capital'])
 liquid['net_cash_after_minimum_regulatory_capital_proxy']=r(liquid['cash_after_minimum_regulatory_capital_proxy']-l['latest_debt_face'])
 current,prior=periods['TTM2026Q3'],periods['TTM2025Q3']
 comparisons={m:{'current':current[m],'prior':prior[m],'change':r(current[m]-prior[m]),'growth':r(current[m]/prior[m]-1) if prior[m]>0 else None} for m in ['net_revenue','gross_revenue','ebit','normalized_ebit_conservative','normalized_ebit_exit_cost_sensitivity','net_income','net_income_common','eps_diluted_quarterly_sum','cfo','clearing_customer_cash_flow','cfo_ex_clearing','capex_cash','sbc','cash_generation_ex_clearing_proxy','cash_generation_ex_clearing_less_sbc_proxy','cash_taxes','royalty_other_cost']}
 result={'as_of':data['as_of'],'units':data['units'],'periods':periods,'balance_sheets':bs,'liquidity':liquid,'ttm_comparison':comparisons,'notes':data['notes']}
 return result,provenance

def main():
 data=json.loads((ROOT/'inputs.json').read_text());out,provenance=calculate(data)
 (ROOT/'history.json').write_text(json.dumps(out,indent=2)+'\n')
 writecsv(ROOT/'history.csv',list(out['periods'].values()))
 writecsv(ROOT/'balance_sheet.csv',out['balance_sheets'])
 writecsv(ROOT/'source_facts.csv',provenance)
 writecsv(ROOT/'source_index.csv',[{'source_id':k,**v} for k,v in data['sources'].items()])
 summary={'as_of':out['as_of'],'currency':'USD','units':out['units'],'ttm':out['periods']['TTM2026Q3'],'prior_ttm':out['periods']['TTM2025Q3'],'ttm_comparison':out['ttm_comparison'],'latest_quarter':out['periods']['Q3_2026'],'liquidity':out['liquidity'],'readiness':'Reported consolidated history is loadable; normalized EBIT and ex-clearing cash generation are explicit analyst proxies, not reported GAAP or unrestricted FCF. Standalone disposed-business pro forma and normalized EPS are unavailable.','missing':['Analyst-normalized EPS/tax by individual adjustment','Exact standalone Australia FY2025 and Q42025 US GAAP net revenue','Canada standalone current P&L and final sale-tax/proceeds bridge','Matched Section31 receivable cash-flow movement','Exact cash-tax normalization'],'raw_sources_excluded':True}
 (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 for k in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM2025Q3','TTM2026Q3']:
  p=out['periods'][k];print(k,{m:p[m] for m in ['net_revenue','ebit','net_income_common','cfo','capex_cash','cash_generation_ex_clearing_proxy','normalized_ebit_conservative','normalized_ebit_exit_cost_sensitivity']})
if __name__=='__main__':main()
