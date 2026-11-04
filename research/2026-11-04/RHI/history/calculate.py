"""Offline deterministic calculation; USD millions, shares millions, EPS USD/share."""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
I=json.load(open(P/'inputs.json'));r=copy.deepcopy(I['periods']);cf=I['cash_flow_fields']
fields=[k for k,v in r['FY2025'].items() if isinstance(v,(float,int)) and k not in ['eps_diluted','diluted_shares']]
def combine(name,terms):
 d={'currency':'USD','units':'millions except EPS','sources':list(dict.fromkeys(u for _,n in terms for u in r[n]['sources'])),'calculation':' + '.join(f'{s} × {n}'for s,n in terms),'eps_diluted':None,'diluted_shares':None}
 for k in fields:d[k]=sum(s*r[n][k]for s,n in terms)
 r[name]=d
combine('Q42025',[(1,'FY2025'),(-1,'9M2025')])
q=I['q4_2025_direct'];r['Q42025'].update({k:q[k]for k in ['eps_diluted','diluted_shares']});r['Q42025']['sources'].append(q['source'])
for name,total,prior in [('Q22026','6M2026','Q12026'),('Q32026','9M2026','6M2026'),('Q32025','9M2025','6M2025')]:
 for k in cf:r[name][k]=r[total][k]-r[prior][k]
 r[name]['cash_flow_calculation']=f'{total} minus {prior}'
combine('TTM2026-09',[(1,'FY2025'),(1,'9M2026'),(-1,'9M2025')]);combine('TTM2025-09',[(1,'FY2024'),(1,'9M2025'),(-1,'9M2024')])
for d in r.values():
 d['normalized_ebit']=d['reported_ebit']+d['trust_investment_income']
 d['reported_ebit_margin_pct']=100*d['reported_ebit']/d['revenue'];d['normalized_ebit_margin_pct']=100*d['normalized_ebit']/d['revenue']
 d['effective_tax_rate_pct']=100*d['tax']/d['pretax']
 d['fcf_cfo_less_capex']=d['cfo']-d['capex']
 d['fcf_after_plan_cash']=d['fcf_cfo_less_capex']-d['plan_purchase']+d['plan_redemptions']
 d['owner_fcf_proxy']=d['fcf_after_plan_cash']-d['sbc']
 # Diagnostic only: remove reported trust-specific CFO reconciling lines; not distributable FCF.
 d['cfo_without_plan_reconciling_lines']=d['cfo']-d['trust_cf_gain_adjustment']-d['plan_liability_change']
 for k,v in d.items():
  if isinstance(v,float):d[k]=round(v,6)
growth={k:round(100*(r['TTM2026-09'][k]/r['TTM2025-09'][k]-1),4) for k in ['revenue','reported_ebit','normalized_ebit','net_income','cfo','fcf_cfo_less_capex','fcf_after_plan_cash','owner_fcf_proxy']}
for d in I['balance_sheets'].values():
 d['plan_surplus_not_unrestricted_cash']=None if d['plan_assets'] is None or d['plan_liability'] is None else round(d['plan_assets']-d['plan_liability'],6)
 d['corporate_cash_less_cash_borrowings']=None if d.get('cash_borrowings') is None else round(d['cash']-d['cash_borrowings'],6)
roic={'formula':'Capital = equity + financial cash borrowings - corporate cash - plan assets + plan obligations. Goodwill stays included. Operating leases are neither added nor netted out; lease expense remains in EBIT.','tax_assumption_pct':30.0,'tax_assumption_status':'Analytical sensitivity, not management guidance','period':'TTM2026-09','capital_by_date':{}}
for date in ['2025-09-30','2026-09-30']:
 d=I['balance_sheets'][date];roic['capital_by_date'][date]=round(d['equity']+d['cash_borrowings']-d['cash']-d['plan_assets']+d['plan_liability'],6)
roic['average_capital']=sum(roic['capital_by_date'].values())/2
roic['nopat_30pct_tax']=round(r['TTM2026-09']['normalized_ebit']*0.70,6)
roic['operating_cash_reserve_sensitivity']=[{'reserve_at_both_dates':x,'average_capital':round(roic['average_capital']+x,6),'roic_pct':round(100*roic['nopat_30pct_tax']/(roic['average_capital']+x),4)}for x in [0,100,200]]
roic['roic_using_actual_ttm_etr_pct']=round(100*r['TTM2026-09']['normalized_ebit']*(1-r['TTM2026-09']['effective_tax_rate_pct']/100)/roic['average_capital'],4)
obj={'roic_diagnostic':roic,'share_denominator':I['share_denominator'],'as_of':I['as_of'],'units':'USD millions, shares millions, EPS USD/share','periods':r,'balance_sheets':I['balance_sheets'],'ttm_growth_pct':growth,'definitions':{'normalized_ebit':'GAAP operating income + signed trust investment income. Removes matched market gains/losses from compensation expenses; does NOT add back recurring employee compensation.','fcf_cfo_less_capex':'Reported CFO less capital expenditures. Cloud implementation cash costs already deducted within CFO; do not deduct twice.','fcf_after_plan_cash':'CFO - capex - trust purchases + trust redemptions. Cash available after net trust investment funding; retains genuine compensation cost.','owner_fcf_proxy':'FCF after plan cash minus SBC. Conservative economic proxy, not GAAP or literal cash measure; SBC is an economic charge not a second cash payment.','cfo_without_plan_reconciling_lines':'Diagnostic CFO minus signed investment gain/loss reconciliation minus plan liability change. Not a distributable-cash measure.','cash':'Separate corporate cash and equivalents; plan trust assets and surplus are excluded from unrestricted cash. Gross corporate cash is not necessarily all excess cash; operational reserve not quantified.','EPS':'Direct reported quarterly/FY diluted EPS only. TTM EPS not computed by subtracting annual and 9M EPS, and null denotes unavailable.'}}
(P/'history.json').write_text(json.dumps(obj,indent=2))
cols=['period']+[k for k in r['FY2025'] if isinstance(r['FY2025'][k],(float,int))]
with open(P/'history.csv','w')as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
 for k in ['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025-09','TTM2026-09','9M2025','9M2026','Q32025']:w.writerow({'period':k,**r[k]})
print(json.dumps(growth,indent=2))
