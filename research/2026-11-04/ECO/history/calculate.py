"""Deterministic history from factual inputs. No web or third-party package dependency."""
import json,csv
from pathlib import Path
from datetime import date
P=Path(__file__).resolve().parent
inputs=json.loads((P/'inputs.json').read_text())
raw=inputs['periods']
def days(p):return (date.fromisoformat(raw[p]['period_end'])-date.fromisoformat(raw[p]['period_start'])).days+1
flow_exclusions={'eps_reported_usd','weighted_average_shares','daily_tce_reported_usd','beginning_cash_usd','ending_cash_usd','sbc_usd'}
def derive(p,f):
 f['total_vessel_opex_usd']=f['vessel_opex_usd']+f['management_fees_usd']
 f['ebit_adjustments_usd']=0
 f['ebit_normalized_usd']=f['ebit_reported_usd']
 f['operating_ebitda_usd']=f['ebit_reported_usd']+f['da_usd']
 f['net_income_adjustments_usd']=-f['unrealized_derivative_gain_usd']+f['debt_extinguishment_loss_usd']-f['loan_modification_gain_usd']
 f['net_income_normalized_usd']=f['net_income_reported_usd']+f['net_income_adjustments_usd']
 f['eps_normalized_calculated_usd']=f['net_income_normalized_usd']/f['weighted_average_shares']
 f['fcf_after_actual_investment_usd']=f['cfo_reported_usd']-f['drydock_capex_usd']-f['vessel_acquisition_cash_usd']
 f['cash_after_drydock_before_acquisitions_usd']=f['cfo_reported_usd']-f['drydock_capex_usd']
 f['cash_before_working_capital_after_interest_usd']=f['cfo_reported_usd']-f['working_capital_cash_change_usd']
 f['unlevered_cash_after_actual_investment_pre_tax_usd']=f['fcf_after_actual_investment_usd']+f['interest_paid_usd']
 f['shareholder_distributions_usd']=f['dividends_paid_usd']+f['capital_distributions_usd']
 f['ebit_margin_gross_revenue_pct']=100*f['ebit_reported_usd']/f['revenue_usd']
 f['ebit_margin_tce_pct']=100*f['ebit_reported_usd']/f['tce_revenue_usd']
 f['cfo_to_reported_ni_pct']=100*f['cfo_reported_usd']/f['net_income_reported_usd']
 f['daily_tce_calculated_usd']=f['tce_revenue_usd']/f['operating_days']
 f['daily_opex_calculated_usd']=f['total_vessel_opex_usd']/f['calendar_days']
 f['ebit_normalization_class']='analyst_adjusted: zero adjustments; not a through-cycle forecast'
 f['net_income_normalization_class']='analyst_adjusted: financial marks and refinancing only; not through-cycle'
 return f
results={p:{'period_start':r['period_start'],'period_end':r['period_end'],'period_kind':r['period_kind'],'source_ids':[r['source_id']],'basis':'reported and independently calculated','metrics':derive(p,{k:v['value']for k,v in r['fields'].items()})}for p,r in raw.items()if not p.endswith(('_RELEASE','_STATEMENTS'))}
for p,fy,old,new,start,end in [('TTM2026-06','FY2025','H12025','H12026','2025-07-01','2026-06-30'),('TTM2025-06','FY2024','H12024','H12025','2024-07-01','2025-06-30')]:
 f={k:raw[fy]['fields'][k]['value']-raw[old]['fields'][k]['value']+raw[new]['fields'][k]['value']for k in raw[fy]['fields'] if k not in flow_exclusions}
 period_days=(date.fromisoformat(end)-date.fromisoformat(start)).days+1
 f['weighted_average_shares']=(raw[fy]['fields']['weighted_average_shares']['value']*days(fy)-raw[old]['fields']['weighted_average_shares']['value']*days(old)+raw[new]['fields']['weighted_average_shares']['value']*days(new))/period_days
 f['eps_reported_usd']=None
 f['eps_ttm_calculated_usd']=f['net_income_reported_usd']/f['weighted_average_shares']
 f['daily_tce_reported_usd']=None;f['sbc_usd']=None
 f['beginning_cash_usd']=raw[old]['fields']['ending_cash_usd']['value'];f['ending_cash_usd']=raw[new]['fields']['ending_cash_usd']['value']
 results[p]={'period_start':start,'period_end':end,'period_kind':'TTM','source_ids':list(dict.fromkeys(raw[q]['source_id']for q in [fy,old,new])),'basis':f'Derived flows: {fy} - {old} + {new}; day-weighted shares; no reported TTM EPS','metrics':derive(p,f)}
# Explicit per-share bases. Current-denominator figure is useful for current equity value; not reported EPS.
current_shares=39044655
for p in ['TTM2026-06','TTM2025-06']:
 f=results[p]['metrics'];f['net_income_per_june30_2026_share_usd']=f['net_income_reported_usd']/current_shares
q=['Q32025','Q42025','Q12026','Q22026']
results['TTM2026-06']['metrics']['sum_reported_quarter_eps_usd']=sum(raw[p]['fields']['eps_reported_usd']['value']for p in q)
results['TTM2025-06']['metrics']['sum_reported_quarter_eps_usd']=sum(raw[p]['fields']['eps_reported_usd']['value']for p in ['Q32024','Q42024','Q12025','Q22025'])
comparisons={}
for now,prior in [('FY2024','FY2023'),('FY2025','FY2024'),('Q32025','Q32024'),('Q42025','Q42024'),('Q12026','Q12025'),('Q22026','Q22025'),('H12026','H12025'),('TTM2026-06','TTM2025-06')]:
 a=results[now]['metrics'];b=results[prior]['metrics']
 comparisons[now+'_vs_'+prior]={k:{'delta':a[k]-b[k],'pct_change':100*(a[k]/b[k]-1)if b[k] else None}for k in ['revenue_usd','tce_revenue_usd','ebit_reported_usd','net_income_reported_usd','net_income_normalized_usd','cfo_reported_usd','fcf_after_actual_investment_usd','operating_days','gna_usd','weighted_average_shares']}
main=['FY2023','FY2024','FY2025','Q32025','Q42025','Q12026','Q22026','TTM2025-06','TTM2026-06']
output={'issuer':inputs['issuer'],'as_of':inputs['as_of'],'currency':inputs['currency'],'units':inputs['units'],'sources':inputs['sources'],'normalization_policy':inputs['normalization_policy'],'main_periods':main,'periods':results,'comparisons':comparisons,'warnings':['Quarterly and interim releases are unaudited; annual audited figures take precedence.','Rounded operating-day totals can differ by one day across the annual/quarterly bridge. Preserve reported daily TCE and derived daily TCE separately.','Reported EPS is taken directly from each original quarter. No annual EPS less nine-month EPS. Derived TTM EPS is explicitly not reported EPS.','No separate SBC amount established; no SBC addback.','Historical normalized EBIT still includes peak freight earnings. These are operating results, not exceptional accounting gains. Use an independent through-cycle valuation scenario.','Cash after disclosed drydock is not sustainable owner earnings: fleet replacement is not fully represented by drydock spending.','Sale-and-leaseback repurchases repay an existing financing liability; do not count them again as fleet capex.']}
(P/'history.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
fields=['period','period_start','period_end','basis']+list(dict.fromkeys(k for p in main for k,v in results[p]['metrics'].items() if not isinstance(v,str)))
with (P/'history.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for p in main:w.writerow({'period':p,'period_start':results[p]['period_start'],'period_end':results[p]['period_end'],'basis':results[p]['basis'],**{k:v for k,v in results[p]['metrics'].items()if k in fields}})
with(P/'Normalized_Financials_Long.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['period','period_start','period_end','metric','value','currency','source_id','source_label','locator','evidence_label']);w.writeheader()
 for p,r in raw.items():
  for k,v in r['fields'].items():w.writerow({'period':p,'period_start':r['period_start'],'period_end':r['period_end'],'metric':k,'value':v['value'],'currency':'USD'if k.endswith('usd')else'','source_id':v['source_id'],'source_label':v['source_label'],'locator':v['locator'],'evidence_label':v['evidence_label']})
with(P/'Source_Index.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(next(iter(inputs['sources'].values())).keys()));w.writeheader();w.writerows(inputs['sources'].values())
print('Wrote history.json, history.csv, long-form factual subset, and source index.')
for p in main:
 f=results[p]['metrics'];print(p,'TCE',round(f['tce_revenue_usd']/1e6,3),'EBIT',round(f['ebit_reported_usd']/1e6,3),'NI',round(f['net_income_reported_usd']/1e6,3),'NI normal',round(f['net_income_normalized_usd']/1e6,3),'CFO',round(f['cfo_reported_usd']/1e6,3),'actual FCF',round(f['fcf_after_actual_investment_usd']/1e6,3))
