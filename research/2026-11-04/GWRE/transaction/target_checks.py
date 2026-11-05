"""Build reproducible target normalization checks from target_accounts.json. GBP, not thousands."""
import json
from pathlib import Path
p=Path(__file__).parent
d=json.loads((p/'target_accounts.json').read_text())
checks=[]
def ck(name,a,b):
    checks.append({'check':name,'actual':a,'expected':b,'passed':abs(a-b)<0.000001})
for k,v in d['periods'].items():
    ck(k+' gross profit',v['revenue']-v['cost_of_sales'],v['gross_profit'])
    ck(k+' EBIT',v['gross_profit']-v['administrative_expenses'],v['ebit'])
    ck(k+' PBT',v['ebit']+v['interest_received']-v['interest_expense'],v['profit_before_tax'])
    ck(k+' net income',v['profit_before_tax']+v['tax_credit'],v['net_income'])
    ck(k+' CFO sum',sum(v['cfo_bridge'].values()),v['cfo'])
    ck(k+' cash rollforward',v['opening_cash']+v['cfo']-v['cash_capex']+v['interest_received']-v['cash_financing_outflow']+v['fx_cash'],v['closing_cash'])
    ck(k+' raw CFO-capex',v['cfo']-v['cash_capex'],v['cfo_less_capex'])
m=d['periods']['two_months_mar2026']; j=d['periods']['year_jan2026'];n=d['normalizations']
ck('March revenue ex transition',m['revenue']-204716,n['march_revenue_ex_transition'])
ck('March EBIT ex transition only',m['ebit']-204716,n['march_ebit_ex_transition_only'])
ck('March EBIT ex transition and FX gain',m['ebit']-204716-444274,n['march_ebit_ex_transition_and_fx'])
ck('March cash flow before debtor/creditor movements',m['cfo']-14281700+7060959,n['march_cfo_before_debtor_creditor_movements'])
ck('Jan cash flow before debtor/creditor movements',j['cfo']+2296771-9399462,n['jan_cfo_before_debtor_creditor_movements'])
ck('March CFO-capex after all lease cash',m['cfo']-m['cash_capex']-77522-12801,n['march_cfo_less_capex_after_all_lease_cash'])
ck('March no debtor/creditor movement cash after capex and leases',129944-27338-77522-12801,n['march_no_wc_cash_after_capex_and_leases'])
ck('Lease balance split',977950+954933,1932883)
ck('ROU carrying value',2010405-83767,1926638)
result={'passed':all(c['passed'] for c in checks),'count':len(checks),'checks':checks,'limitations':d['limitations']}
(p/'target_checks_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['passed']
