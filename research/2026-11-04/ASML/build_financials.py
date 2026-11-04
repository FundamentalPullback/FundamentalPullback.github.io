from pathlib import Path
import json
P=Path(__file__).parent
q=json.load(open(P/'history/extracts/quarterly_rows.json'));a=json.load(open(P/'history/extracts/annual_rows.json'))
keys={'sales':'Total net sales','ebit':'Income from operations','net_income':'Net income','eps_basic':'Basic net income per ordinary share','eps_diluted':'Diluted net income per ordinary share','cfo':'Net cash provided by (used in) operating activities','capex_ppe':'Purchase of property, plant and equipment','capex_intangible':'Purchase of intangible assets','sbc':'Share-based compensation expense','da':'Depreciation and amortization','working_capital_change':'Changes in assets and liabilities','equity_gain':'Gain (loss) on equity investments','tax':'Benefit from (provision for) income taxes','pretax':'Income before income taxes'}
am={**keys,'cfo':'Net cash provided by operating activities','tax':'Income tax expense','da':'Depreciation and amortization1','capex_ppe':'Purchase of property, plant and equipment3'};h={}
for yr in [2023,2024,2025]:
 rr=[r for r in a if r['period']==f'FY{yr}'];v={k:next((r['value'] for r in rr if r['metric']==m),None) for k,m in am.items()};v['working_capital_change']=round(sum(r['value'] for r in rr if r['metric'] in ['Accounts receivable, net','Finance receivables, net','Inventories','Other assets','Accrued and other liabilities','Accounts payable','Current tax assets and liabilities','Contract assets and liabilities']),1);h[f'FY{yr}']=v
for d in sorted({r['period_end'] for r in q}):
 rr=[r for r in q if r['period_end']==d];h[d]={k:next((r['value'] for r in reversed(rr) if r['metric']==m),None) for k,m in keys.items()}
for v in h.values():
 for k in ['capex_ppe','capex_intangible']:v[k]=abs(v[k]) if v[k] is not None else None
 v['capex']=round(v['capex_ppe']+v['capex_intangible'],2) if v['capex_ppe'] is not None and v['capex_intangible'] is not None else None;v['fcf']=round(v['cfo']-v['capex'],2) if v['cfo'] is not None and v['capex'] is not None else None
for yr in [2025,2026]:
 ps=sorted(p for p in h if (p.startswith(f'{yr}-') and p[5:7]<'10') or p==f'{yr-1}-12-31');h[f'TTM{yr}-09-30']={k:round(sum(h[p][k] for p in ps),2) if all(h[p][k] is not None for p in ps) else None for k in h[ps[0]]}
assert h==json.load(open(P/'history/extracts/core_history.json'))
json.dump(h,open(P/'financials.json','w'),indent=2)
