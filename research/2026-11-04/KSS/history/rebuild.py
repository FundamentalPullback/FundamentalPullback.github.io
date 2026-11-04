#!/usr/bin/env python3
"""Offline rebuild. Python standard library only; no network or external source files."""
import csv, json, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
inputs=json.loads((P/'inputs.json').read_text())
base={p:{k:v['value'] for k,v in d['facts'].items()} for p,d in inputs['periods'].items()}
NONADDITIVE={'shares_basic','shares_diluted','eps_diluted','eps_basic'}
def combine(terms):
    common=set.intersection(*(set(base[p]) for p,w in terms))-NONADDITIVE
    return {k:round(sum(base[p][k]*w for p,w in terms),6) for k in common}
def quarter(direct, terms):
    r=combine(terms);r.update(base[direct]);return r
series={k:dict(base[k]) for k in ['FY2023','FY2024','FY2025']}
series['Q32025']=quarter('Q32025',[('9M2025',1),('H12025',-1)])
series['Q42025']=quarter('Q42025',[('FY2025',1),('9M2025',-1)])
series['Q12026']=dict(base['Q12026'])
series['Q22026']=quarter('Q22026',[('H12026',1),('Q12026',-1)])
series['TTM2026Q2']=combine([('FY2025',1),('H12025',-1),('H12026',1)])
series['TTM2025Q2']=combine([('FY2024',1),('H12024',-1),('H12025',1)])
for label,r in series.items():
    r['fcf_cfo_less_capex']=r['cfo']-r['capex']
    r['fcf_after_sbc']=r['fcf_cfo_less_capex']-r['sbc']
    r['ebit_margin']=round(r['ebit']/r['revenue'],6)
    r['wc_contribution_ex_operating_leases']=sum(r[k] for k in ['inventory_cf','other_assets_cf','ap_cf','accruals_cf'])
    r['cfo_ex_wc_contribution']=r['cfo']-r['wc_contribution_ex_operating_leases']
    if 'lease_financing_principal' in r:
        r['fcf_after_lease_financing_principal']=r['fcf_cfo_less_capex']-r['lease_financing_principal']
        r['company_adjusted_fcf']=r['fcf_after_lease_financing_principal']+r['financing_obligation_proceeds']
    if 'other_investing_cash' in r:
        r['fcf_after_net_other_investing']=r['fcf_cfo_less_capex']+r['other_investing_cash']
    if 'legal_gain' in r:
        r['ebit_partial_normalized']=r['ebit']-r['legal_gain']+r['special_charges']-r.get('tariff_cogs_benefit',0)
# Tariff recovery exists only H1 2026; prior periods predate recovery.
series['TTM2026Q2']['tariff_cogs_benefit']=100
series['TTM2026Q2']['tariff_cash_refund']=150
series['TTM2026Q2']['ebit_partial_normalized']=series['TTM2026Q2']['ebit']-100-(129-129)+(15-11)
series['TTM2026Q2']['fcf_ex_gross_tariff_receipts_sensitivity']=series['TTM2026Q2']['fcf_cfo_less_capex']-150
series['TTM2026Q2']['fcf_after_sbc_lease_principal_other_investing']=series['TTM2026Q2']['fcf_after_lease_financing_principal']-series['TTM2026Q2']['sbc']+series['TTM2026Q2']['other_investing_cash']
# 9.19 scanner reconciliation requires unknown scanner denominator/date; do not assert identity.
raw=series['TTM2026Q2']['fcf_cfo_less_capex']
bridge={'scanner_fcf_per_share_user_supplied':9.19,'reported_ttm_fcf_millions':raw,'implied_scanner_share_count_millions':raw/9.19,'shares_q2_diluted_millions':base['Q22026']['shares_diluted'],'fcf_per_q2_diluted_share':raw/base['Q22026']['shares_diluted'],'shares_h1_diluted_millions':base['H12026']['shares_diluted'],'fcf_per_h1_diluted_share':raw/base['H12026']['shares_diluted'],'shares_h1_basic_millions':base['H12026']['shares_basic'],'fcf_per_h1_basic_share':raw/base['H12026']['shares_basic'],'conclusion':'9.19 is consistent with ~112.514m denominator, but scanner exact denominator and as-of unavailable; not a verified GAAP diluted FCF/share.'}
qa=[]
def check(name,condition,details=''):
    qa.append({'test':name,'pass':bool(condition),'details':details})
for label,r in series.items():
    if all(k in r for k in ['net_sales','other_revenue']):check(label+' revenue total',r['revenue']==r['net_sales']+r['other_revenue'])
    if all(k in r for k in ['noncash_lease','lease_liability_cf','impairment_cf']):
        cfo=sum(r[k] for k in ['net_income','da','sbc','deferred_tax','impairment_cf','noncash_lease','other_noncash','inventory_cf','other_assets_cf','ap_cf','accruals_cf','lease_liability_cf'])
        check(label+' CFO component reconciliation',abs(cfo-r['cfo'])<=1,{'component_sum':cfo,'reported_cfo':r['cfo'],'tolerance_millions':1})
check('four quarters sum TTM revenue',sum(series[q]['revenue'] for q in ['Q32025','Q42025','Q12026','Q22026'])==series['TTM2026Q2']['revenue'])
check('four quarters sum TTM CFO',sum(series[q]['cfo'] for q in ['Q32025','Q42025','Q12026','Q22026'])==series['TTM2026Q2']['cfo'])
check('four quarters sum TTM capex',sum(series[q]['capex'] for q in ['Q32025','Q42025','Q12026','Q22026'])==series['TTM2026Q2']['capex'])
check('Q4 EPS and diluted shares directly sourced',all(series['Q42025'][k]==base['Q42025'][k] for k in NONADDITIVE) and series['Q42025']['eps_diluted']==1.07 and series['Q42025']['shares_diluted']==117)
check('Q2 normalized EBIT comparator',series['Q22026']['ebit_partial_normalized']==base['Q22025']['ebit']-129+11==161)
check('FY23 is 53 weeks',inputs['periods']['FY2023']['start']=='2023-01-29' and inputs['periods']['FY2023']['end']=='2024-02-03')
meta={'company':'Kohls Corporation','ticker':'KSS','financial_cutoff':'2026-08-01','latest_source_filing_date':'2026-09-03','units':inputs['units'],'method':'Fiscal labels use fiscal year, not ending calendar year. Q3 cash flow=9M-H1; Q4=FY-9M; Q2 cash flow=H1-Q1; TTM=FY minus prior H1 plus current H1. EPS/shares never differenced. FY2023 53 weeks; FY2024/FY2025 52 weeks.','source_inputs_sha256':hashlib.sha256((P/'inputs.json').read_bytes()).hexdigest()}
(P/'normalized_history.json').write_text(json.dumps({'metadata':meta,'periods':series,'balance_sheets':inputs['balance_sheets'],'scanner_bridge':bridge},indent=2,sort_keys=True))
keys=sorted(set().union(*(set(r) for r in series.values())))
with (P/'normalized_history.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['period']+keys);writer.writeheader();writer.writerows({'period':p,**r} for p,r in series.items())
with (P/'ttm_comparison.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['metric','TTM2025Q2','TTM2026Q2','change','change_pct'])
    old,new=series['TTM2025Q2'],series['TTM2026Q2']
    for k in sorted(set(old)&set(new)):
        writer.writerow([k,old[k],new[k],round(new[k]-old[k],6),round((new[k]/old[k]-1)*100,4) if old[k] else ''])
(P/'qa.json').write_text(json.dumps({'all_pass':all(q['pass'] for q in qa),'checks':qa},indent=2))
print(json.dumps({'qa_pass':all(q['pass'] for q in qa),'checks':len(qa),'ttm':series['TTM2026Q2'],'scanner':bridge},indent=2))
assert all(q['pass'] for q in qa),[q for q in qa if not q['pass']]
