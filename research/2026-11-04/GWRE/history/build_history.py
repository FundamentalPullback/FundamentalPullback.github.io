#!/usr/bin/env python3
"""Offline stdlib calculator. USD thousands unless shares. Facts manually checked against cited SEC statements; no network."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sources={
'FY25_10K':'https://www.sec.gov/Archives/edgar/data/1528396/000152839625000221/gwre-20250731.htm',
'FY26_10K':'https://www.sec.gov/Archives/edgar/data/1528396/000152839626000046/gwre-20260731.htm',
'Q1_10Q':'https://www.sec.gov/Archives/edgar/data/1528396/000152839625000244/gwre-20251031.htm',
'Q2_10Q':'https://www.sec.gov/Archives/edgar/data/1528396/000152839626000014/gwre-20260131.htm',
'Q3_10Q':'https://www.sec.gov/Archives/edgar/data/1528396/000152839626000027/gwre-20260430.htm',
'Q4_release':'https://ir.guidewire.com/node/26281/pdf'}
fields='period end revenue subscription_support license services gross_profit ebit_gaap net_income sbc_expense cfo capex_cash software_capitalized_cash contract_cost_amortization deferred_revenue_cfo acquired_intangible_amortization acquisition_holdback basic_wavg_shares diluted_wavg_shares tax_provision pretax_income source'.split()
raw=[
['FY2024','2024-07-31',980497,549087,250176,181234,583361,-52573,-6103,146460,195748,6362,12165,28413,72572,5468,143,82291483,82291483,-20735,-26838,'FY26_10K'],
['FY2025','2025-07-31',1202459,731296,251935,219228,752053,41068,69804,161556,300867,5741,14714,30893,56617,5444,177,83846793,85911653,-20409,49395,'FY26_10K'],
['FY2026','2026-07-31',1475363,970885,234578,269900,947368,149874,139283,181799,389716,12056,19003,35011,93675,6701,1510,84186951,85405177,24834,164117,'FY26_10K'],
['Q1FY2026','2025-10-31',332639,222203,41967,68469,209522,18478,31308,43316,-67398,4878,5088,8802,-88785,1455,177,84780201,86451737,-6806,24502,'Q1_10Q'],
['Q2FY2026','2026-01-31',359095,237209,59528,62358,231521,38441,60110,46758,44648-(-67398),8162-4878,8192-5088,17304-8802,-32515-(-88785),1748,447,84858179,86116567,14442,74552,'Q2_10Q'],
['Q3FY2026','2026-04-30',372541,244738,55996,71807,236645,30637,16471,44941,105830-44648,9934-8162,13939-8192,25812-17304,-40781-(-32515),1765,440,84241069,85065999,3289,19760,'Q3_10Q'],
['Q4FY2026','2026-07-31',411088,266735,77086,67266,269679,62318,31395,46784,283886,2122,5064,9199,134456,6701-4968,445,82870116,83620224,13908,45303,'Q4_release']]
rows=[dict(zip(fields,r)) for r in raw]
rows.append(dict(rows[2],period='TTM_2026-07-31'))
for r in rows:
 r['fcf']=r['cfo']-r['capex_cash']-r['software_capitalized_cash']
 r['fcf_less_sbc_sensitivity']=r['fcf']-r['sbc_expense']
 r['fcf_ex_deferred_revenue_inflow_sensitivity']=r['fcf']-r['deferred_revenue_cfo']
 r['ebit_plus_acquired_amort_retaining_sbc']=None if r['acquired_intangible_amortization'] is None else r['ebit_gaap']+r['acquired_intangible_amortization']
 r['nongaap_ebit_reconstructed']=None if r['acquired_intangible_amortization'] is None else r['ebit_gaap']+r['sbc_expense']+r['acquired_intangible_amortization']+r['acquisition_holdback']
 r['company_nongaap_ebit']={'FY2024':99498,'FY2025':208245,'FY2026':339884,'TTM_2026-07-31':339884,'Q1FY2026':63426,'Q2FY2026':87394,'Q3FY2026':77784,'Q4FY2026':111280}[r['period']]
 r['nongaap_reconciliation_rounding']=r['company_nongaap_ebit']-r['nongaap_ebit_reconstructed']
 for num,label in [('gross_profit','gross_margin'),('ebit_gaap','ebit_margin'),('fcf','fcf_margin'),('fcf_less_sbc_sensitivity','fcf_less_sbc_margin'),('sbc_expense','sbc_revenue_ratio')]:r[label]=round(r[num]/r['revenue'],8)
 r['source_url']=sources[r['source']]
 if r['period']=='FY2024': r['source_url']+=' ; '+sources['FY25_10K']
with (ROOT/'normalized_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'normalized_history.json').write_text(json.dumps({'units':'USD thousands; shares count; ratios decimal','as_of':'2026-11-04','rows':rows,'sources':sources},indent=2))
checks=[]
for field in ['revenue','subscription_support','license','services','gross_profit','ebit_gaap','net_income','sbc_expense','cfo','capex_cash','software_capitalized_cash','contract_cost_amortization','deferred_revenue_cfo','tax_provision']:
 delta=sum(r[field] for r in rows[3:7])-rows[2][field]; assert abs(delta)<=1,(field,delta)
 checks.append({'test':'sum_4Q_equals_FY26_'+field,'delta_usd_thousands':delta,'tolerance':1,'pass':True})
assert rows[2]['fcf']==358657
assert rows[2]['fcf_less_sbc_sensitivity']==176858
(ROOT/'checks.json').write_text(json.dumps(checks,indent=2))
print('Wrote normalized 3FY,4Q,TTM; all quarterly bridge checks pass within $1k rounding.')
