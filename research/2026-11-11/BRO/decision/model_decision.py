"""Decision overlay; preserves original packet. Run from any cwd. USD millions."""
import pathlib,json,csv,hashlib,itertools
P=pathlib.Path(__file__).parent; BASE=P.parent/'model.py'
N={'__file__':str(BASE)}
exec(compile(BASE.read_text().split('cases={k:value(k)')[0],str(BASE),'exec'),N)
value=N['value']; PRICE=71.89; E=PRICE*331.691829; D=7292; WE=E/(E+D); WD=1-WE
RF=.0498; ERP=.0441; BETA=.52
# Dated curve mark, rolled by change in Treasury, NOT a traded yield.
KD=.06183+(.0498-.0491)
def wacc(beta=BETA,erp=ERP,kd=KD,tax=.25,debt=D):
 wd=debt/(E+debt)
 return (RF+beta*erp)*(1-wd)+kd*(1-tax)*wd
def calc(beta=BETA,erp=ERP,kd=KD,tax=.25,replacement=0,cash=0,extra_shares=0,bridge_debt=7822,case='central'):
 N['TAX']=tax;w=wacc(beta,erp,kd,tax);r=value(case,w=w,replacement=replacement,cash=cash,shares=332.691829+extra_shares)
 r['price']+=(7822-bridge_debt)/(332.691829+extra_shares)
 return dict(wacc=w,price=r['price'],fcff1=r['rows'][0]['fcff'],terminal_share=r['terminal_share'])
settings={
 'published_beta_reference':{},
 'constant_market_return_ERP':{'erp':.0494+.0441-RF},
 'beta_shrink_convention':{'beta':(2*BETA+1)/3},
 'beta_shrink_and_constant_market_return':{'beta':(2*BETA+1)/3,'erp':.0494+.0441-RF},
 'published_beta_extra_retention_1pct':{'replacement':.01},
 'beta_shrink_extra_retention_1pct':{'beta':.68,'replacement':.01},
 'beta_shrink_extra_retention_fullcash_marketdebt':{'beta':.68,'replacement':.01,'cash':1099,'bridge_debt':7292},
 'beta_shrink_tax22_1pct':{'beta':.68,'tax':.221}}
R={'date':'2026-11-11','decision':'WATCH_NO_ROBUST_MARGIN_AT_71_89','execution_controls':{'canonical_intrinsic_value':None,'max_buy_price':None,'trade_authorized':False},
'inputs':{'rf':RF,'rf_date':'2026-11-10','ERP':ERP,'ERP_date':'2026-11-01','ERP_original_treasury':.0494,'published_equity_beta':BETA,'beta_period':'5Y; monthly corroborated by Yahoo search; not independently regressed','kd_reference':KD,'kd_method':'Nov2 issuer curve-implied6.183% + Nov10 minus Nov2 Treasury change7bp; not current trade','gross_debt_weight':WD,'equity_value_for_weights':E,'gross_market_debt_september_proxy':D,'cash_in_weights':'not netted','leases':'operating expense retained; no debt addition','debt_bridge_base':7822},
'cases_at_reference_rate':{k:calc(case=k) for k in N['C']},'named_tests':{k:{'parameters':v,**calc(**v)} for k,v in settings.items()},
'cross_matrix':[{'beta':b,'ERP':e,'replacement':r,**calc(beta=b,erp=e,replacement=r)} for b,e,r in itertools.product([.52,.68],[.0441,.0437],[0,.01,.02])],
'bounded_bridge_test':{name:{'low':calc(beta=b,extra_shares=4.4)['price'],'high':calc(beta=b,cash=1099)['price'],'high_with_sept_market_debt':calc(beta=b,cash=1099,bridge_debt=7292)['price']} for name,b in [('published_beta',.52),('shrink_convention',.68)]},
'debt_cost_sensitivity':[{'kd':k,'beta':b,**calc(kd=k,beta=b)} for b in [.52,.68] for k in [.055,.06,KD,.065]],
'cash_and_leverage_beta_diagnostic':{'equity_beta':BETA,'unlevered_at_current_gross_debt_proxy':BETA/(1+.75*D/E),'cash_corrected_operating_beta_all_reportedcash':BETA/(1+.75*D/E)/(1-1099/(D+E)),'not_forward_estimate':'Contemporary unlevering of historical equity beta is illustrative, not a reconstructed historical leverage adjustment; direct0.52 is NOT relevered again.'},
'omitted_other_income_flat_perpetuity_diagnostic':{'annual_pretax':95,'increment_per_share_published_beta':95*.75/wacc()/332.691829,'increment_per_share_shrink_beta':95*.75/wacc(beta=.68)/332.691829,'warning':'Hypothetical full recurring retained income, flat forever; not an upper bound or approved addition, and do not also add associated surplus cash if income arises on it.'},
'source_base_model_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest()}
N['TAX']=.25
R['checks']={'source_hash_matches_previous_audit':R['source_base_model_sha256']=='2daa74b66866bde4af16490abcc5504966a6dd7a37f0c882562b7bd9b3f51088','wacc_weights_sum':abs(WE+WD-1)<1e-12,'beta_shrink':abs((2*BETA+1)/3-.68)<1e-12,'canonical_null':R['execution_controls']['canonical_intrinsic_value'] is None,'watch_not_robust_buy':R['named_tests']['published_beta_reference']['price']>PRICE>R['named_tests']['beta_shrink_convention']['price']}
(P/'results_decision.json').write_text(json.dumps(R,indent=2))
with (P/'cross_matrix.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(R['cross_matrix'][0]));writer.writeheader();writer.writerows(R['cross_matrix'])
print(json.dumps({k:R[k] for k in ['named_tests','bounded_bridge_test','cash_and_leverage_beta_diagnostic','checks']},indent=2))
