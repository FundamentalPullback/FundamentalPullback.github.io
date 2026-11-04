#!/usr/bin/env python3
"""Portable stdlib-only reproduction. Run beside numeric_facts.json; no network."""
import csv,json,pathlib
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parent
S=json.loads((P/'numeric_facts.json').read_text());F=S['facts']
K='revenue gaap_ebit net_income_parent cfo da_ex_acquired_intangibles acquired_intangible_amortization sbc capex_ppe technology_license_purchases technology_license_obligation_payments'.split()
def calc(a,b,c=None):
 return {k:float(Decimal(str(F[a][k]))-Decimal(str(F[b][k]))+(Decimal(str(F[c][k])) if c else 0)) for k in K}
def derived(r):
 r=dict(r)
 r['da_total']=round(r['da_ex_acquired_intangibles']+r['acquired_intangible_amortization'],1)
 r['ebitda_unadjusted']=round(r['gaap_ebit']+r['da_total'],1)
 r['fcf_ppe_only']=round(r['cfo']-r['capex_ppe'],1)
 r['fcf_after_technology_purchases']=round(r['fcf_ppe_only']-r['technology_license_purchases'],1)
 r['fcf_after_all_technology_cash']=round(r['fcf_after_technology_purchases']-r['technology_license_obligation_payments'],1)
 r['owner_cash_after_sbc_proxy']=round(r['fcf_after_all_technology_cash']-r['sbc'],1)
 r['ebit_margin_pct']=round(100*r['gaap_ebit']/r['revenue'],4)
 return r
out={n:derived(F[n]) for n in ['FY2024','FY2025','FY2026','Q4FY2026','Q1FY2027']}
q3=calc('9MFY2026','H1FY2026');q3.update(F['Q3FY2026_direct']);out['Q3FY2026']=derived(q3)
q2=calc('H1FY2027','Q1FY2027');q2.update(F['Q2FY2027_direct']);out['Q2FY2027']=derived(q2)
for name,a,b,c in [('TTM','FY2026','H1FY2026','H1FY2027'),('prior_TTM','FY2025','H1FY2025','H1FY2026')]:
 r=calc(a,b,c)
 r['net_income_common_annual_ytd_bridge']=round(F[a]['net_income_common_basic_allocation']-F[b]['net_income_common_basic_allocation']+F[c]['net_income_common_basic_allocation'],1)
 out[name]=derived(r)
quarters=['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']
out['TTM']['eps_diluted_sum_direct_quarters']=round(sum(out[q]['eps_diluted'] for q in quarters),2)
out['TTM']['net_income_common_sum_quarter_allocations']=round(sum(out[q]['net_income_common_basic_allocation'] for q in quarters),1)
out['prior_TTM']['eps_diluted_sum_direct_quarters']=round(sum(S['prior_ttm_direct_quarter_eps_diluted'].values()),2)
for k in K:assert abs(sum(out[q][k]for q in quarters)-out['TTM'][k])<1e-6,(k,'quarter bridge failed')
assert out['TTM']['revenue']==9450.3
assert out['TTM']['net_income_common_annual_ytd_bridge']==2633.4
assert out['TTM']['net_income_common_sum_quarter_allocations']==2631.3
(P/'normalized_history.json').write_text(json.dumps(out,indent=2)+'\n')
fields=['period']+list(dict.fromkeys(k for r in out.values() for k in r if k not in ['source','end']))+['end','source']
with (P/'normalized_history.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({'period':n,**r}for n,r in out.items())
print(json.dumps({n:out[n]for n in ['TTM','prior_TTM']},indent=2))
