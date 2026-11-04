import json
from pathlib import Path
p=Path(__file__).resolve().parent
h=json.loads((p/'history.json').read_text());r={(x['period'],x['metric']):x['value'] for x in h}
assert len(r)==len(h),'Duplicate period metric'
for m in ('revenue','ebit_gaap','net_income','cfo','capex_ppe','sbc_pnl','sbc_cfo','ppe_depreciation','acquired_intangible_amortization','deferred_commission_amortization'):
 assert abs(sum(r[q,m] for q in ('Q4-2025','Q1-2026','Q2-2026','Q3-2026'))-r['TTM-September-2026',m])<1e-7,m
assert r['TTM-September-2026','cfo']==5334
assert r['Q3-2026','fcf_cfo_minus_ppe']==748
assert r['TTM-September-2026','ppe_depreciation']==608
assert r['2026-09-30','shares_outstanding']==1037.917
print('PASS: no duplicate rows; discrete quarter sums equal TTM; key CFO, capex, SBC, depreciation and split checks agree.')
