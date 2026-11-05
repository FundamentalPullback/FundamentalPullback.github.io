from pathlib import Path
import json
p=Path(__file__).parent;c=json.loads((p/'inputs.json').read_text());o={'ticker':'URI','period':c['period'],'source':c['source'],'rows':[]}
for i,y in enumerate([2026,2025]):
 fcf=c['cfo'][i]-c['rental_capex_cash'][i]-c['nonrental_capex_cash'][i]+c['rental_disposal_cash'][i]+c['nonrental_disposal_cash'][i]+c['insurance_cash'][i]
 assert fcf==c['fcf_published'][i]
 o['rows'].append({'year':y,'ebit_margin':c['ebit'][i]/c['revenue'][i],'fcf_reported':fcf,'cash_after_fleet_disposal_before_ppe_insurance':fcf-c['nonrental_disposal_cash'][i]-c['insurance_cash'][i],'fcf_less_sbc_proxy':fcf-c['sbc'][i]})
o['cash_accrual_fleet_capex_gap_2026']=c['rental_capex_accrual_2026']-c['rental_capex_cash'][0];o['homogeneous_valuation_comparable']=False;o['multiple_target']=None
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
