import json,csv
from pathlib import Path
D=Path(__file__).parent
x=json.loads((D/'inputs.json').read_text())
rows=[]
for t,v in x['companies'].items():
 rows.append({'ticker':t,'price_Nov3_USD':v['price'],'actual_shares_m':v['actual_shares']/1e6,'equity_market_value_USDm':v['price']*v['actual_shares']/1e6,'Q3_sales_USDm':v['q3_sales'],'Q3_parent_net_income_USDm':v['q3_parent_net_income'],'Q3_diluted_EPS_USD':v['q3_diluted_eps']})
u=x['uan']; own=u['cvi_owned_units_prior_exact']; external=u['total_units']-own
c=x['companies']['CVI']; market=c['price']*c['actual_shares']/1e6
out={'units':'USD millions except prices, EPS and units','peer_scope':'Factual scale and reported earnings only. No homogeneous enterprise multiple or peer-derived target.','companies':rows,'uan_bridge':{'owned_units_prior_disclosure':own,'external_units_inferred':external,'owned_market_value':own*u['price']/1e6,'external_market_value':external*u['price']/1e6,'owned_distribution_declared':own*u['declared_distribution_per_unit']/1e6,'UAN_debt_principal_and_all_finance_leases':u['senior_notes_principal_USDm']+u['finance_lease_current_USDm']+u['finance_lease_noncurrent_USDm'],'UAN_cash':u['cash_USDm'],'ownership_caveat':u['ownership_caveat']},'cvi_consolidated_capital_bridge':{'equity_market_value':market,'debt_principal_and_finance_leases':1794,'cash_including_UAN':1278,'external_UAN_market_value':external*u['price']/1e6,'enterprise_value_indicative':market+1794-1278+external*u['price']/1e6,'erroneous_NCI_omission_understatement':external*u['price']/1e6,'book_NCI_instead_of_market_understatement':external*u['price']/1e6-172},'cvi_normalization':{'Q3_GAAP_operating_income':724,'Q3_GAAP_operating_income_less_SRE_only':724-253,'Q3_SRE_benefit':253,'Q3_RFS_reconciliation_including_SRE_and_RVO':-314,'Q3_company_adjusted_EBITDA':804-314+127-35,'Q3_petroleum_company_adjusted_EBITDA':787-314+127-35,'SBC_removed':0,'warning':'Subtracting SRE only is an isolated diagnostic, not normalized EBIT. Company adjusted EBITDA also changes RVO, derivatives and inventory, and excludes D&A including capitalized turnaround amortization.'}}
assert out['cvi_normalization']['Q3_company_adjusted_EBITDA']==582
assert out['cvi_normalization']['Q3_petroleum_company_adjusted_EBITDA']==565
assert own+external==u['total_units']
(D/'outputs.json').write_text(json.dumps(out,indent=2)+'\n')
with (D/'peer_facts.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(out,indent=2))
