"""Public-source Radian diagnostics and conditional RI/FCFE; no approved fair values."""
import json,csv,math
from pathlib import Path
P=Path(__file__).resolve().parent
f=json.loads((P/'financial_inputs.json').read_text())
tags={'revenue':'Revenues','premiums':'PremiumsEarnedNet','continuing_income':'IncomeLossFromContinuingOperations','net_income':'NetIncomeLoss','continuing_cfo':'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations','total_cfo':'NetCashProvidedByUsedInOperatingActivities','pretax_continuing':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'}
def fact(tag,start,end):
 a=[x for x in f[tag]['units']['USD'] if x.get('start')==start and x['end']==end and x.get('filed','')<='2026-11-08']
 return sorted(a,key=lambda x:x['filed'])[-1]['val']/1e6 if a else None
h={}
for y in [2023,2024,2025]:h['FY'+str(y)]={k:fact(t,f'{y}-01-01',f'{y}-12-31') for k,t in tags.items()}
for y in [2024,2025,2026]:h['9M'+str(y)]={k:fact(t,f'{y}-01-01',f'{y}-09-30') for k,t in tags.items()}
for y in [2025,2026]:h['TTM'+str(y)]={k:h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in tags}
q=[{'quarter':'Q42025','revenue':300.512,'net_income':154.843,'continuing_income':158.802,'eps':1.12,'diluted_shares':138.250,'mortgage_apoi':221.994,'specialty_apoi':None}, {'quarter':'Q12026','revenue':466.337,'net_income':124.093,'continuing_income':129.466,'eps':.89,'diluted_shares':138.485,'mortgage_apoi':220.799,'specialty_apoi':40.069},{'quarter':'Q22026','revenue':574.959,'net_income':115.914,'continuing_income':118.228,'eps':.85,'diluted_shares':136.283,'mortgage_apoi':207.821,'specialty_apoi':28.596},{'quarter':'Q32026','revenue':624.111,'net_income':163.655,'continuing_income':172.207,'eps':1.22,'diluted_shares':134.385,'mortgage_apoi':206.286,'specialty_apoi':86.465}]
# Quarterly cash flow reconstructed from same-perimeter cumulative SEC facts.
for field in ['continuing_cfo','total_cfo']:
 q[0][field]=h['FY2025'][field]-h['9M2025'][field]
 prior=0
 for i,end in enumerate(['2026-03-31','2026-06-30','2026-09-30'],start=1):
  cumulative=fact(tags[field],'2026-01-01',end)
  q[i][field]=cumulative-prior;prior=cumulative
 assert abs(sum(x[field] for x in q)-h['TTM2026'][field])<1e-7
for k in ['revenue','net_income','continuing_income']:assert abs(sum(x[k] for x in q)-h['TTM2026'][k])<1e-7
book=4649.790-117.0 # only October repurchase adjustment, NOT actual November equity
shares_basic=126.437454; shares=shares_basic+1.225 # reported Q3 dilutive increment, proxy NOT point-date fact
price=35.97;rf=.0486;erp=.0441;beta=.66
# Group nine-month APOI, remove actual favorable releases and retain recurring acquired-intangible amortization.
normalized_pretax_proxy=681.356-84.406-79.576-15.688
# Timing annualization diagnostic only: specialty starts Feb 2, no seasonal/catastrophe forecast inferred.
roe_proxy=normalized_pretax_proxy*.75*4/3/book

def ri(roe_first,roe_terminal,ke,g,write=None):
 b=book; pvri=0;pvpotential=0;forecast=[]
 for yr in range(1,6):
  roe=roe_first+(roe_terminal-roe_first)*(yr-1)/4
  ni=b*roe;retention=b*g;potential=ni-retention;ri=ni-ke*b
  pvri+=ri/(1+ke)**yr;pvpotential+=potential/(1+ke)**yr
  forecast.append({'year':yr,'begin_book':b,'roe':roe,'income':ni,'retention_capital':retention,'potential_fcfe_before_regulatory_gate':potential,'approved_distribution':None,'residual_income':ri,'end_book':b+retention});b+=retention
 terminal_ri=(roe_terminal-ke)*b/(ke-g);terminal_ddm=b*(roe_terminal-g)/(ke-g)
 val=book+pvri+terminal_ri/(1+ke)**5
 ddm=pvpotential+terminal_ddm/(1+ke)**5
 assert abs(val-ddm)<1e-7
 if write:
  with (P/f'forecast_{write}.csv').open('w') as fh:
   w=csv.DictWriter(fh,fieldnames=list(forecast[0]));w.writeheader();w.writerows(forecast)
 return {'first_roe':roe_first,'terminal_roe':roe_terminal,'ke':ke,'g':g,'year5_book':b,'year6_retained_capital':b*g,'year6_income':b*roe_terminal,'terminal_retention_ratio':g/roe_terminal,'conditional_equity':val,'conditional_value_per_share':val/shares,'potential_fcfe_value_tie':ddm,'terminal_ddm_share':terminal_ddm/(1+ke)**5/val,'approved_value':None,'distribution_schedule_approved':False,'clean_surplus_and_instant_remittability_assumed_for_identity_only':True}
cases={k:ri(*args,write=k) for k,args in {'adverso':(.08,.08,.115,.01),'central':(.11,.10,.105,.02),'favorable':(.13,.12,.095,.025)}.items()}
sensitivity=[{'ke':ke,'terminal_roe':tr,'conditional_value_per_share':ri(.11,tr,ke,.02)['conditional_value_per_share']} for ke in [.095,.105,.115] for tr in [.08,.10,.12]]
lo,hi=0,.30
for _ in range(100):
 m=(lo+hi)/2
 if ri(.11,m,.105,.02)['conditional_value_per_share']<price:lo=m
 else:hi=m
mortgage_increase=170.129*(1.25*(.10/.075)*1.15-1)
capital={'pmier_available':5329.,'pmier_required':5329.-1478.,'pmier_excess':1478.,'pmier_coverage':5329./(5329.-1478.),'reinsurance_requirement_relief':1891.163,'mortgage_statutory_surplus':554.097,'intercompany_min_surplus':500.,'surplus_over_note_floor':54.097,'mortgage_statutory_income_9m':455.037,'remittances_9m':515.,'q4_dividend_planned_not_approved':145.,'restricted_subsidiary_net_assets_approx':4600.,'inigo_statutory_capital':1780.,'inigo_required_lagged':1551.,'inigo_cushion_before_lag_adjustment':229.,'inigo_loc_included_sep':620.,'inigo_loc_outstanding_oct29_parent_guaranteed':880.,'holdco_liquidity_sep':376.,'holdco_liquidity_minus_oct_repurchase_only':259.,'holdco_2027_notes_principal':450.,'holdco_2029_notes_principal':625.,'holdco_undrawn_revolver':500.}
res={'ticker':'RDN','as_of':'2026-11-08','price':price,'price_timestamp':'2026-11-06T16:00:00-05:00','status':'material_partial','quality':'not-decision-ready','stage3_complete':False,'stage35_complete':False,'entry_approved':False,'approved_values':dict.fromkeys(cases),'canonical_approved_value':None,'method':'conditional residual income / potential FCFE clean-surplus tie, NOT industrial FCFF','reported_book_sep30':4649.790,'october_repurchase_cash':117.,'proforma_book_only_repurchase_adjusted':book,'proforma_book_warning':'Not actual November book; October earnings/OCI/tax/other equity changes unknown','current_basic_shares':shares_basic,'basic_share_date':'2026-11-04','q3_dilutive_increment':1.225,'diluted_point_proxy':shares,'historical':h,'quarters':q,'ttm_income_change':h['TTM2026']['net_income']/h['TTM2025']['net_income']-1,'ttm_continuing_income_change':h['TTM2026']['continuing_income']/h['TTM2025']['continuing_income']-1,'market_cap_using_current_basic':price*shares_basic,'proforma_basic_bvps':book/shares_basic,'proforma_diluted_bvps':book/shares,'proforma_price_book_diluted':price/(book/shares),'capital':capital,'normalization':{'nine_month_adjusted_pretax':681.356,'mortgage_prior_year_release':84.406,'specialty_prior_year_release':79.576,'retained_finite_intangible_amortization':15.688,'pretax_proxy':normalized_pretax_proxy,'annualized_income_proxy_not_forecast':normalized_pretax_proxy*.75*4/3,'roe_proxy_not_forecast':roe_proxy,'warning':'Removes all favorable releases as stress, not actuarial estimate; purchase adjustments not fully validated; eight months acquired specialty in nine-month numerator'},'cost_equity':{'rf':rf,'erp':erp,'observed_beta_5y':beta,'mechanical_capm':rf+beta*erp,'applied_range':[.095,.105,.115],'applied_range_reason':'Analyst scenarios for new specialty/catastrophe/regulatory-transfer risk not represented by legacy 5Y beta; not externally calibrated estimate'},'conditional_cases':cases,'sensitivity':sensitivity,'reverse_terminal_roe_other_base_inputs':(lo+hi)/2,'stress_diagnostics':{'mortgage_new_default_factor':1.25,'mortgage_default_to_claim':.10,'reported_default_to_claim':.075,'severity_factor':1.15,'incremental_nine_month_mortgage_provision_proxy':mortgage_increase,'specialty_extra_lossratio_10pp_on_8mo_npe':.10*743.212,'combined_pretax_stress_proxy':mortgage_increase+.10*743.212,'no_statutory_capital_mapping':True},'no_cash_investment_portfolio_or_pmiers_surplus_added_to_value':True}
(P/'results.json').write_text(json.dumps(res,indent=2))
with (P/'historical.csv').open('w') as fh:
 w=csv.DictWriter(fh,fieldnames=['period']+list(tags));w.writeheader();w.writerows({'period':k,**v} for k,v in h.items())
with (P/'quarters.csv').open('w') as fh:
 w=csv.DictWriter(fh,fieldnames=list(q[0]));w.writeheader();w.writerows(q)
(P/'self_check.json').write_text(json.dumps({'ttm_equals_four_quarters':True,'ri_fcfe_clean_surplus_tie':True,'approved_values_null':True,'independent_audit':False,'economic_capital_gate_closed':False,'point_diluted_shares_actual':False},indent=2))
print(json.dumps({k:res[k] for k in ['ttm_income_change','ttm_continuing_income_change','proforma_basic_bvps','proforma_diluted_bvps','normalization','cost_equity','conditional_cases','reverse_terminal_roe_other_base_inputs','stress_diagnostics']},indent=2))
