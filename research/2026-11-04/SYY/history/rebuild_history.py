"""Offline rebuild from own selected observations. Python standard library only."""
from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent
O=json.loads((P/'observations.json').read_text())
METRICS=['revenue','ebit','net_income','cfo','ppe_capex','ppe_sale_proceeds','sbc','da_ex_financing','acquisition_intangible_amortization','cash_taxes','tax_expense','receivables_increase','inventory_increase','prepaids_increase','payables_increase','accruals_increase','tax_payables_increase','deferred_tax_asset_increase','operating_lease_liability_increase','other_assets_increase','other_liabilities_increase','acquisitions_net','basic_shares','diluted_shares','diluted_eps','defined_contribution_cost','multiemployer_contribution_cost']
PERIODS={'FY24':('2023-07-02','2024-06-29'),'FY25':('2024-06-30','2025-06-28'),'FY26':('2025-06-29','2026-06-27'),'Q1FY25':('2024-06-30','2024-09-28'),'Q1FY26':('2025-06-29','2025-09-27'),'Q2FY26':('2025-09-28','2025-12-27'),'Q3FY26':('2025-12-28','2026-03-28'),'Q4FY26':('2026-03-29','2026-06-27'),'Q1FY27':('2026-06-28','2026-09-26')}
SUBTRACT={'Q2FY26':(('2025-06-29','2025-12-27'),PERIODS['Q1FY26']),'Q3FY26':(('2025-06-29','2026-03-28'),('2025-06-29','2025-12-27')),'Q4FY26':(PERIODS['FY26'],('2025-06-29','2026-03-28'))}
NONADDITIVE={'basic_shares','diluted_shares','diluted_eps'}
def get(m,period,seg=None):
 for r in O:
  dims=r['dimensions'];rs=dims.get('us-gaap:StatementBusinessSegmentsAxis')
  if rs is None and dims.get('srt:ConsolidationItemsAxis')=='us-gaap:CorporateNonSegmentMember':rs='Global Support Center'
  if m==r['metric'] and r.get('startdate')==period[0] and r.get('enddate')==period[1] and ((seg is None and not dims) or (seg is not None and seg==rs)):
   return {'value':r['value'],'unit':r['unit'],'method':'reported','observation_ids':[r['observation_id']]}
 return None
def calc(terms,method):
 if any(r is None for _,r in terms):return None
 return {'value':round(sum(s*r['value'] for s,r in terms),6),'unit':terms[0][1]['unit'],'method':method,'observation_ids':list(dict.fromkeys(i for _,r in terms for i in r['observation_ids']))}
def one(m,k,seg=None):
 v=get(m,PERIODS[k],seg)
 if v:return v
 if k in SUBTRACT and m not in NONADDITIVE:
  a,b=SUBTRACT[k];return calc([(1,get(m,a,seg)),(-1,get(m,b,seg))],'annual_minus_nine_months' if k=='Q4FY26' else 'YTD_difference')
 return None
rows={k:{'start':a,'end':b,'weeks':52 if k.startswith('FY') else 13,'metrics':{m:one(m,k) for m in METRICS}} for k,(a,b) in PERIODS.items()}
for k,annual,add,sub,start,end in [('TTM','FY26','Q1FY27','Q1FY26','2025-09-28','2026-09-26'),('PRIOR_TTM','FY25','Q1FY26','Q1FY25','2024-09-29','2025-09-27')]:
 rows[k]={'start':start,'end':end,'weeks':52,'metrics':{m:calc([(1,rows[annual]['metrics'][m]),(1,rows[add]['metrics'][m]),(-1,rows[sub]['metrics'][m])],'annual_plus_latest_Q1_minus_prior_Q1') if m not in NONADDITIVE else None for m in METRICS}}
for r in rows.values():
 m=r['metrics'];m['fcf_gross_capex']=calc([(1,m['cfo']),(-1,m['ppe_capex'])],'CFO_minus_gross_cash_PP&E_capex')
 m['company_fcf']=calc([(1,m['cfo']),(-1,m['ppe_capex']),(1,m['ppe_sale_proceeds'])],'CFO_minus_cash_PP&E_capex_plus_PP&E_sale_proceeds')
 m['fcf_after_sbc']=calc([(1,m['fcf_gross_capex']),(-1,m['sbc'])],'CFO_minus_gross_capex_minus_SBC_analytical_not_GAAP')
 m['working_capital_core_cash_effect']=calc([(-1,m['receivables_increase']),(-1,m['inventory_increase']),(-1,m['prepaids_increase']),(1,m['payables_increase']),(1,m['accruals_increase'])],'minus_AR_inventory_prepaids_plus_AP_accruals_excludes_taxes_and_leases')
segments={}
ss=sorted(set(r['dimensions'].get('us-gaap:StatementBusinessSegmentsAxis') for r in O if r['dimensions'].get('us-gaap:StatementBusinessSegmentsAxis')))+['Global Support Center']
for seg in ss:
 segments[seg]={k:{m:one(m,k,seg) for m in ['revenue','ebit','da']} for k in PERIODS}
 for k,a,b,c in [('TTM','FY26','Q1FY27','Q1FY26'),('PRIOR_TTM','FY25','Q1FY26','Q1FY25')]:
  segments[seg][k]={m:calc([(1,segments[seg][a][m]),(1,segments[seg][b][m]),(-1,segments[seg][c][m])],'annual_plus_latest_Q1_minus_prior_Q1') for m in ['revenue','ebit','da']}
balances={}
for d in sorted(set(r['instant'] for r in O if r.get('instant') and r['instant']>='2024-06-29')):
 ms={}
 for m in ['cash','current_debt','long_term_debt','total_debt','issued_shares','treasury_shares','actual_shares','cover_actual_shares','current_operating_lease','noncurrent_operating_lease','assets','equity']:
  matches=[r for r in O if r.get('instant')==d and not r['dimensions'] and r['metric']==m]
  if matches:
   z=matches[0];ms[m]={'value':z['value'],'unit':z['unit'],'method':'reported','observation_ids':[z['observation_id']]}
 if 'total_debt' not in ms:ms['total_debt']=calc([(1,ms.get('current_debt')),(1,ms.get('long_term_debt'))],'current_plus_noncurrent_book_debt_including_finance_leases')
 if 'actual_shares' not in ms:ms['actual_shares']=calc([(1,ms.get('issued_shares')),(-1,ms.get('treasury_shares'))],'issued_minus_treasury_actual_point_in_time_not_weighted_average')
 balances[d]=ms
changes={}
for m in rows['TTM']['metrics']:
 a=rows['TTM']['metrics'][m];b=rows['PRIOR_TTM']['metrics'][m]
 changes[m]=None if not a or not b else {'absolute':a['value']-b['value'],'percent':100*(a['value']/b['value']-1) if b['value'] else None}
result={'schema_version':1,'as_of':'2026-11-04','currency':'USD','financial_unit':'millions unless explicitly shares or EPS','periods':rows,'ttm_vs_prior':changes,'segments':segments,'balance_sheets':balances,'limitations':['All FY24-FY26 and historical TTM periods contain 52 weeks; FY27 guidance is a separate 53-week outlook.','Quarter CF values not reported separately are YTD differences; Q4 income is reported in the annual earnings release; Q4 CF is annual less nine months. Differences of rounded filings can differ from reported quarter by $1m.','No quarter weighted-share inference. Q4 weighted shares/EPS are reported in the annual earnings release; TTM weighted shares/EPS left null.','September 26 balance includes JRD prefunding and excludes subsequent October financing and unclosed acquisition. It is not November pro forma net debt.','Acquisition intangible amortization excludes acquisition diligence/costs; do not substitute total non-GAAP D&A adjustment.','CFO is after interest, cash taxes and working capital; CFO-capex is not unlevered FCFF.','Pension detail remains in dimensioned source observations; unavailable quarterly contributions are not zero.']}
(P/'history.json').write_text(json.dumps(result,indent=2))
with (P/'history.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['period','start','end','weeks','metric','value','unit','method','observation_ids'])
 for k,r in rows.items():
  for m,v in r['metrics'].items():w.writerow([k,r['start'],r['end'],r['weeks'],m,v['value'] if v else '',v['unit'] if v else '',v['method'] if v else 'not_available_not_inferred',';'.join(v['observation_ids']) if v else ''])
print('Rebuilt history.json and history.csv')
