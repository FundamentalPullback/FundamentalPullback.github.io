#!/usr/bin/env python3
"""Reproduce RELX history using only compact factual inputs and Python stdlib."""
import json,csv
from pathlib import Path
from datetime import date
P=Path(__file__).resolve().parent
I=json.loads((P/'inputs.json').read_text()); raw=I['periods']; rows={}
STOCKS=('cash','debt_including_leases','lease_liabilities','reported_net_debt')
NONFLOW=set(STOCKS)|{'start','end','source','diluted_shares_m','diluted_eps_p'}
FLOW=[k for k in raw['FY2025'] if k not in NONFLOW]
def days(p):return (date.fromisoformat(p['end'])-date.fromisoformat(p['start'])).days+1
def normalize(name,p,kind):
 r=dict(p);r['period']=name;r['kind']=kind;r['days']=days(r)
 r['ordinary_da']=sum(r[k] for k in ['software_amortization','ppe_depreciation','rou_depreciation','prepublication_amortization'])
 r['consolidated_da']=r['ordinary_da']+r['acquired_amortization']
 r['owner_fcf']=r['cfo']-r['ppe_capex']-r['software_capex']-r['lease_principal']+r['sublease_receipts']+r['jv_dividends']-r['sbc']-r['nci_dividends']
 r['owner_fcf_after_acquisitions']=r['owner_fcf']-r['acquisition_cash']
 r['ebit_margin_pct']=100*r['ebit']/r['revenue'];r['owner_fcf_margin_pct']=100*r['owner_fcf']/r['revenue']
 r['parent_earnings_conversion_pct']=100*r['owner_fcf']/r['parent_net_income']
 r['simple_net_debt_including_leases']=r['debt_including_leases']-r['cash']
 r['debt_excluding_leases']=None if r['lease_liabilities'] is None else r['debt_including_leases']-r['lease_liabilities']
 r['diluted_eps_ni_over_shares_p']=100*r['parent_net_income']/r['diluted_shares_m']
 return r
for n,p in raw.items():rows[n]=normalize(n,p,'reported')
for y in [2024,2025]:
 f,h=raw[f'FY{y}'],raw[f'H1{y}'];r={k:None if f[k] is None or h[k] is None else f[k]-h[k] for k in FLOW}
 r.update({k:f[k] for k in STOCKS});r.update(start=f'{y}-07-01',end=f'{y}-12-31',source=f'FY{y} minus H1{y}',diluted_eps_p=None)
 r['diluted_shares_m']=(f['diluted_shares_m']*days(f)-h['diluted_shares_m']*days(h))/days(r)
 r['eps_arithmetic_difference_p']=f['diluted_eps_p']-h['diluted_eps_p']
 rows[f'H2{y}']=normalize(f'H2{y}',r,'derived half-year; EPS difference is not reported standalone EPS')
for y in [2025,2026]:
 a,b=rows[f'H2{y-1}'],rows[f'H1{y}'];r={k:None if a[k] is None or b[k] is None else a[k]+b[k] for k in FLOW}
 r.update({k:b[k] for k in STOCKS});r.update(start=a['start'],end=b['end'],source=f'FY{y-1} minus H1{y-1} plus H1{y}',diluted_eps_p=None)
 r['diluted_shares_m']=(a['diluted_shares_m']*a['days']+b['diluted_shares_m']*b['days'])/days(r)
 r['eps_arithmetic_sum_p']=a['eps_arithmetic_difference_p']+b['diluted_eps_p']
 rows[f'TTMJune{y}']=normalize(f'TTMJune{y}',r,'derived TTM; EPS sum is diagnostic, not reported IFRS EPS')
order=['FY2023','FY2024','FY2025','H22024','H12025','H22025','H12026','TTMJune2025','TTMJune2026']
out={'units':I['units'],'definition':'Owner FCF = CFO - PPE capex - internally developed intangible capex - lease principal + sublease receipts + JV dividends - SBC - NCI dividends. Diagnostic equity cash flow after interest, not FCFF. Acquisition cash is separately shown.','eps_method':'Reported diluted EPS for FY and H1. H2 EPS arithmetic differences and TTM sums are only diagnostics. NI/day-weighted diluted shares shown separately as an estimate, not company-reported EPS.','prepublication_method':'Capitalization disclosed as current assets; operating working-capital investment is already reflected in CFO. Do not subtract again. Null is unknown, never zero.','sources':I['sources'],'gaps':I['gaps'],'periods':[rows[n] for n in order]}
(P/'history.json').write_text(json.dumps(out,indent=2)+'\n')
fields=list(dict.fromkeys(k for n in order for k in rows[n]))
with (P/'history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows[n] for n in order)
if __name__=='__main__':
 for n in order: print(n,'Revenue',rows[n]['revenue'],'CFO',rows[n]['cfo'],'Owner FCF',rows[n]['owner_fcf'])
