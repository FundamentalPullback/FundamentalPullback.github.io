#!/usr/bin/env python3
"""Reproduce STNG normalized history offline with Python standard library only.
Input: selected_inputs.json (selected numeric facts, source URLs/row labels).
Output: normalized_history.json and summary.csv. No network or raw filings needed.
"""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
raw=json.loads((ROOT/'selected_inputs.json').read_text())
nonmonetary={'eps_basic','eps_diluted','weighted_shares_basic','weighted_shares_diluted','fleet_average','tce_per_day'}
positive_costs={'vessel_opex','voyage_costs','depreciation','depreciation_owned','depreciation_rou','gna','financial_expense','interest_expense','drydock_other_capex','vessel_acquisition_capex','buybacks','dividends','debt_repayments','scrubber_writeoff'}
periods={}; provenance={}
for p,fs in raw['periods'].items():
 if p.endswith('_RELEASE'):continue
 d={};pr={}
 for k,f in fs.items():
  v=f['value'];v=abs(v) if k in positive_costs else v
  d[k]=v if k in nonmonetary else round(v/1000,6)
  pr[k]={'source':f['source'],'row':f['row'],'method':'reported; expenses/capex displayed as positive magnitudes' if k in positive_costs else 'reported'}
 if 'depreciation_owned' in d:
  d['depreciation']=round(d['depreciation_owned']+d.get('depreciation_rou',0),6)
  pr['depreciation']={'method':'owned plus right-of-use depreciation'}
 periods[p]=d;provenance[p]=pr
cash_fields=set(['working_capital_cash_effect','cfo','sbc','vessel_sale_proceeds','vessel_acquisition_capex','drydock_other_capex','cash_change','buybacks','debt_repayments','debt_issuance','dividends','cfi','cff','convertible_proceeds','interest_paid'])
def difference(target,large,small,keys):
 for k in keys:
  if k in periods[large] and k in periods[small]:
   periods[target][k]=round(periods[large][k]-periods[small][k],6)
   provenance[target][k]={'method':f'{large} minus {small}','source_periods':[large,small]}
difference('Q4_2025','FY2025','9M_2025',cash_fields)
difference('Q2_2026','H1_2026','Q1_2026',cash_fields)
difference('Q3_2026','9M_2026','H1_2026',cash_fields)
for q,end in [('Q4_2025','FY2025'),('Q2_2026','H1_2026'),('Q3_2026','9M_2026')]:
 periods[q]['cash_end']=periods[end]['cash_end'];provenance[q]['cash_end']={'method':f'end-period balance from {end}'}
for name,fy,now,prior,fy_days,prior_days in [('TTM_2026_09','FY2025','9M_2026','9M_2025',365,273),('TTM_2025_09','FY2024','9M_2025','9M_2024',366,274)]:
 periods[name]={};provenance[name]={}
 for k in set(periods[fy])&set(periods[now])&set(periods[prior]):
  if k in nonmonetary or k=='cash_end':continue
  periods[name][k]=round(periods[fy][k]+periods[now][k]-periods[prior][k],6)
  provenance[name][k]={'method':f'{fy} + {now} - {prior}','source_periods':[fy,now,prior]}
 periods[name]['cash_end']=periods[now]['cash_end']
 # Basic weighted shares are time-weighted, never summed. Both TTMs cover 365 days.
 w=(periods[fy]['weighted_shares_basic']*fy_days+periods[now]['weighted_shares_basic']*273-periods[prior]['weighted_shares_basic']*prior_days)/365
 periods[name]['weighted_shares_basic']=round(w,6)
 periods[name]['eps_basic']=round(periods[name]['net_income']*1e6/w,6)
 periods[name]['weighted_shares_diluted']=None;periods[name]['eps_diluted']=None
 provenance[name]['eps_basic']={'method':'calculated NI divided by day-weighted basic shares; not a company-reported TTM EPS'}
 provenance[name]['weighted_shares_basic']={'method':f'({fy} shares × {fy_days} + {now} shares × 273 - {prior} shares × {prior_days}) / 365'}
 provenance[name]['eps_diluted']={'method':'not calculated: if-converted numerator and anti-dilution must be assessed over full TTM'}
for p,d in periods.items():
 if 'revenue' in d and 'voyage_costs' in d:d['tce_revenue']=round(d['revenue']-d['voyage_costs'],6)
 if 'ebit_reported' in d:
  d['ebit_ex_vessel_gains']=round(d['ebit_reported']-d.get('vessel_sale_gain',0),6)
  d['ebit_ex_vessel_gains_margin']=round(d['ebit_ex_vessel_gains']/d['revenue'],6)
 if 'cfo' in d and 'drydock_other_capex' in d:
  d['cfo_less_drydock_other_capex']=round(d['cfo']-d['drydock_other_capex'],6)
  d['cfo_less_all_reported_capex']=round(d['cfo']-d['drydock_other_capex']-d.get('vessel_acquisition_capex',0),6)
  d['cfo_less_all_reported_capex_and_sbc']=round(d['cfo']-d['drydock_other_capex']-d.get('vessel_acquisition_capex',0)-d.get('sbc',0),6)
  d['cfo_less_drydock_other_capex_and_sbc']=round(d['cfo']-d['drydock_other_capex']-d.get('sbc',0),6)
 if 'cfo' in d and 'working_capital_cash_effect' in d:d['cfo_before_working_capital']=round(d['cfo']-d['working_capital_cash_effect'],6)
 if 'cfo' in d and 'net_income' in d and d['net_income']>0:d['cfo_to_ni']=round(d['cfo']/d['net_income'],6)
 if 'cfo' in d and 'revenue' in d:d['cfo_margin']=round(d['cfo']/d['revenue'],6)
# Monetary identities, including source rounding.
checks=[]
for p,d in periods.items():
 if all(k in d for k in ['revenue','vessel_opex','voyage_costs','depreciation','gna','ebit_reported']):
  calc=d['revenue']-d['vessel_opex']-d['voyage_costs']-d['depreciation']-d['gna']+d.get('vessel_sale_gain',0)-d.get('scrubber_writeoff',0)+d.get('vessel_impairment_reversal',0)+d.get('goodwill_impairment',0)
  delta=round(calc-d['ebit_reported'],6)
  assert abs(delta)<=0.002,(p,delta)
  checks.append({'period':p,'check':'EBIT components reconcile','difference_m':delta})
for p,d in periods.items():
 if all(k in d for k in ['cfo','cfi','cff','cash_change']):
  delta=round(d['cfo']+d['cfi']+d['cff']-d['cash_change'],6)
  assert abs(delta)<0.003,(p,'cash flow',delta)
  checks.append({'period':p,'check':'CFO + CFI + CFF equals cash change','difference_m':delta})
for k in ['revenue','net_income','ebit_reported','cfo','sbc','drydock_other_capex']:
 assert abs(sum(periods[p][k] for p in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])-periods['TTM_2026_09'][k])<0.003,k
output={'company':'Scorpio Tankers Inc.','ticker':'STNG','as_of':'2026-11-04','units':'USD millions except per-share EPS, actual weighted share counts, fleet counts, daily rates in USD and ratios as fractions','sources':raw['sources'],'periods':periods,'provenance':provenance,'validation_checks':checks,'limits':['TTM diluted EPS/shares intentionally null. Quarterly and annual EPS/shares are directly reported, never added.','Financial expense is broader than interest expense. FY2020–25 interest expense is separately selected from the financial expense note; quarterly interest is not separately selected.','Drydock_other_capex includes drydock, scrubbers, ballast water treatment and other vessel-related payments where reported; not a pure maintenance number.','Cash flow after reported capex excludes replacement-fleet reserve, lease purchase/reclassification cash flows, and future committed newbuilds. It is not sustainable owner earnings.','EBIT ex vessel gains removes only reported vessel-sale gains/losses; historical impairment and scrubber write-offs remain.','Zero acquisition capex means no separately reported vessel acquisition/construction cash flow in complete investing statement, not no economic fleet investment.']}
(ROOT/'normalized_history.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
cols=['period','revenue','tce_revenue','vessel_opex','depreciation','gna','vessel_sale_gain','ebit_reported','ebit_ex_vessel_gains','net_income','eps_basic','eps_diluted','cfo','sbc','drydock_other_capex','vessel_acquisition_capex','cfo_less_all_reported_capex','cash_end']
with (ROOT/'summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
 for p in ['FY2020','FY2021','FY2022','FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM_2025_09','TTM_2026_09']:w.writerow({'period':p,**periods[p]})
print('Built normalized_history.json and summary.csv; validation passed.')
