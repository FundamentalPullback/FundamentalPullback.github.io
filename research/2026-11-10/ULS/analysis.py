from pathlib import Path
import json,csv,hashlib
r=Path(__file__).parent
keys=['revenue','operating_income','net_income','parent_net_income','da','cfo','capex_cash','sbc_cf_addback']
raw={'FY2023':[2678,368,276,260,154,467,215,0],'FY2024':[2870,462,345,326,172,524,237,23],'FY2025':[3053,522,345,325,188,600,197,47],'9M2024':[2131,347,260,245,125,394,179,16],'9M2025':[2264,404,274,258,137,456,139,36],'9M2026':[2397,450,469,447,142,594,199,58],'H12026':[1574,288,352,339,93,379,138,35],'Q12026_direct':[758,138,97,92,47,219,69,12]}
d={k:dict(zip(keys,v)) for k,v in raw.items()}
def add(name,a,b,c=None):d[name]={k:d[a][k]-d[b][k]+(d[c][k] if c else 0) for k in keys}
add('TTM2026','FY2025','9M2025','9M2026');add('TTM2025','FY2024','9M2024','9M2025');add('Q42025_derived','FY2025','9M2025');add('Q22026_derived','H12026','Q12026_direct');add('Q32026_derived','9M2026','H12026')
for v in d.values():v['simple_fcf']=v['cfo']-v['capex_cash'];v['simple_fcf_less_sbc_addback']=v['simple_fcf']-v['sbc_cf_addback']
calc={'units':'USD millions except prices/shares/growth','raw_and_derived':d,'rounding':{'Q22026_net_income_direct':254,'Q22026_net_income_derived':d['Q22026_derived']['net_income'],'Q22026_parent_net_income_direct':246,'Q22026_parent_net_income_derived':d['Q22026_derived']['parent_net_income'],'explanation':'Q1 direct net97/parent92; H1 net352/parent339 less Q2 direct254/246 implies98/93. Retain $1m rounding differences, use cumulative for TTM.'},'diagnostics':{'ttm_revenue_growth_pct':100*(d['TTM2026']['revenue']/d['TTM2025']['revenue']-1),'ttm_op_growth_pct':100*(d['TTM2026']['operating_income']/d['TTM2025']['operating_income']-1),'ttm_op_margin_pct':100*d['TTM2026']['operating_income']/d['TTM2026']['revenue'],'sept_net_debt_gross_basis':766-1016,'sept_net_debt_carrying_basis':764-1016,'oct30_gross_debt':689,'acquisition_cash_approx':686,'dqs_sale_approx':117,'dqs_gain_approx':93,'ehs_sale_gain':191,'ehs_cash_proceeds_cf':199,'shares_oct23_million':(78147947+123755000)/1e6,'scanner_price':81.19,'illustrative_market_cap':81.19*(78147947+123755000)/1e6,'9m_cf_sbc':58,'9m_sbc_expense':60,'9m_sbc_cash_settled':2,'9m_working_asset_liability_rows_sum':-44-41-2+42-8+112,'valuation_available':False,'entryApproved':False}}
(r/'calculations.json').write_text(json.dumps(calc,indent=2)+'\n')
with (r/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(d.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in d.items())
print(json.dumps(calc['diagnostics'],indent=2));print(d['TTM2026'],d['TTM2025'])
