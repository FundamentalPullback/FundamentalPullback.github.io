"""Independent invariant checks; execute after calculate.py."""
import json,pathlib,math,subprocess,sys
P=pathlib.Path(__file__).parent
I=json.load(open(P/'inputs.json'));H=json.load(open(P/'history.json'));r=H['periods'];n=0
def eq(a,b):
 global n
 assert math.isclose(a,b,rel_tol=1e-9,abs_tol=0.000002),(a,b)
 n+=1
for k,d in r.items():
 eq(d['reported_ebit']+d['trust_investment_income'],d['normalized_ebit'])
 eq(d['pretax']-d['tax'],d['net_income'])
 eq(d['cfo']-d['capex'],d['fcf_cfo_less_capex'])
 eq(d['fcf_cfo_less_capex']-d['plan_purchase']+d['plan_redemptions'],d['fcf_after_plan_cash'])
 eq(d['fcf_after_plan_cash']-d['sbc'],d['owner_fcf_proxy'])
for f in ['revenue','reported_ebit','trust_investment_income','pretax','tax','net_income']+I['cash_flow_fields']:
 eq(sum(r[q][f]for q in ['Q42025','Q12026','Q22026','Q32026']),r['TTM2026-09'][f])
 eq(r['FY2025'][f]+r['9M2026'][f]-r['9M2025'][f],r['TTM2026-09'][f])
 eq(r['FY2024'][f]+r['9M2025'][f]-r['9M2024'][f],r['TTM2025-09'][f])
for f in ['revenue','reported_ebit','net_income','eps_diluted','diluted_shares']:eq(r['Q42025'][f],I['q4_2025_direct'][f])
eq(r['Q32026']['normalized_ebit'],72.552);eq(r['Q32025']['normalized_ebit'],61.209)
eq(r['9M2026']['normalized_ebit'],139.815);eq(r['9M2025']['normalized_ebit'],139.114)
assert r['TTM2026-09']['eps_diluted'] is None
assert H['balance_sheets']['2026-09-30']['cash']==321.291
assert H['balance_sheets']['2026-09-30']['plan_assets']==844.170
assert H['balance_sheets']['2026-09-30']['plan_surplus_not_unrestricted_cash']==16.409
eq(H['roic_diagnostic']['average_capital'],891.108)
eq(H['roic_diagnostic']['nopat_30pct_tax'],128.2778)
eq(H['share_denominator']['q3_basic_weighted_m']+H['share_denominator']['q3_potential_dilution_m'],H['share_denominator']['q3_diluted_weighted_m'])
# Reproduce offline and check exact serialized outputs.
before=[(P/f).read_bytes()for f in ['history.json','history.csv']]
subprocess.run([sys.executable,str(P/'calculate.py')],check=True,stdout=subprocess.DEVNULL)
assert before==[(P/f).read_bytes()for f in ['history.json','history.csv']]
print(f'PASS: {n} arithmetic checks; null/EPS/cash safeguards; deterministic rerun.')
