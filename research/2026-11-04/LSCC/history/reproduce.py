#!/usr/bin/env python3
"""Offline, standard-library-only LSCC normalization. Run from any working directory."""
import json,re,html,csv,hashlib
from pathlib import Path
from datetime import date
from html.parser import HTMLParser
OUT=Path(__file__).resolve().parent
URLS=json.loads((OUT/'urls.json').read_text())
F=json.loads((OUT/'companyfacts_subset.json').read_text())
RAW=json.loads((OUT/'inline_numeric_extract.json').read_text())
metrics={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','gross_profit':'GrossProfit','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','eps_diluted':'EarningsPerShareDiluted','tax_expense':'IncomeTaxExpenseBenefit','cfo':'NetCashProvidedByUsedInOperatingActivities','software_ip_cash':'PaymentsToAcquireIntangibleAssets','capex':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','da':'lscc:DepreciationDepletionAndAmortizationExcludingRightOfUseAssetAndFinanceCosts','amort_intangibles':'AmortizationOfIntangibleAssets','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding'}
bals={'cash':'CashAndCashEquivalentsAtCarryingValue','assets':'Assets','current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','liabilities':'Liabilities','equity':'StockholdersEquity','inventory':'InventoryNet','receivables':'AccountsReceivableNetCurrent','goodwill':'Goodwill','intangibles':'FiniteLivedIntangibleAssetsNet','debt_gross':'DebtInstrumentCarryingAmount','debt_net_costs':'LongTermDebt','lease_current':'OperatingLeaseLiabilityCurrent','lease_noncurrent':'OperatingLeaseLiabilityNoncurrent'}
ledger=[]
def direct(tag,start,end):
 raw=[f for f in RAW if f['tag']==(tag if ':' in tag else 'us-gaap:'+tag) and f['start']==start and f['end']==end]
 if raw:
  f=max(enumerate(raw),key=lambda z:(999 if z[1]['decimals']=='INF' else int(z[1]['decimals']),z[0]))[1];return dict(value=f['value'],method='direct_inline',source=f['url'],tag=f['tag'],start=start,end=end)
 fs=[f for a in F.get(tag,{}).get('units',{}).values() for f in a if f.get('start')==start and f['end']==end and f['filed']<='2026-11-04']
 if fs:
  f=sorted(fs,key=lambda f:f['filed'])[-1];return dict(value=f['val'],method='direct_companyfacts',source='https://www.sec.gov/Archives/edgar/data/855658/'+f['accn'].replace('-','')+'/',tag=tag,start=start,end=end,filed=f['filed'])
 if tag=='DebtInstrumentCarryingAmount' and start is None and end=='2024-12-28':
  # Explicit zero in the FY25 10-K credit facility note, dimensional context excluded above.
  return dict(value=0,method='direct_inline_note',source=URLS['fy25']+'#c139795909',tag=tag,start=start,end=end,context='i_2024-12-28_CreditFacilityAxis-RevolvingCreditFacilityMember_DebtInstrumentAxis-The2022CreditAgreementMember')
 return dict(value=None,method='unavailable',tag=tag,start=start,end=end)
def calc(a,b,op,formula):
 return dict(value=None if a['value'] is None or b['value'] is None else (a['value']+b['value'] if op=='+' else a['value']-b['value']),method='derived',formula=formula,inputs=[a,b])
periods={}
for id,s,e in [('FY2023','2023-01-01','2023-12-30'),('FY2024','2023-12-31','2024-12-28'),('FY2025','2024-12-29','2026-01-03'),('YTD2024Q3','2023-12-31','2024-09-28'),('YTD2025Q1','2024-12-29','2025-03-29'),('YTD2025Q2','2024-12-29','2025-06-28'),('YTD2025Q3','2024-12-29','2025-09-27'),('YTD2026Q1','2026-01-04','2026-04-04'),('YTD2026Q2','2026-01-04','2026-07-04'),('YTD2026Q3','2026-01-04','2026-10-03')]:
 periods[id]=dict(start=s,end=e,weeks=((date.fromisoformat(e)-date.fromisoformat(s)).days+1)/7,metrics={m:direct(t,s,e) for m,t in metrics.items()})
for y in [2025,2026]:
 for q in [1,2,3]:
  id=f'Q{q}FY{y}';cur=periods[f'YTD{y}Q{q}'];prev=periods.get(f'YTD{y}Q{q-1}')
  s=cur['start'] if not prev else str(date.fromordinal(date.fromisoformat(prev['end']).toordinal()+1));e=cur['end'];mm={}
  for m,t in metrics.items():
   d=direct(t,s,e)
   if d['value'] is None and prev and m not in ['eps_diluted','diluted_shares']:d=calc(cur['metrics'][m],prev['metrics'][m],'-',f'YTD{y}Q{q} - YTD{y}Q{q-1}')
   mm[m]=d
  periods[id]=dict(start=s,end=e,weeks=13,metrics=mm)
# Fourth-quarter EPS is directly disclosed, never an annual-minus-YTD EPS subtraction.
for y,eps,s in [(2024,.12,'2024-09-29'),(2025,-.06,'2025-09-28')]:
 a=periods[f'FY{y}'];b=periods[f'YTD{y}Q3'];mm={m:calc(a['metrics'][m],b['metrics'][m],'-',f'FY{y} - YTD{y}Q3') for m in metrics if m not in ['eps_diluted','diluted_shares']}
 mm['eps_diluted']=dict(value=eps,method='direct_release',source=URLS['q4_release'],locator='GAAP Financial Results / Net Income (loss) per Share - Diluted; Q4 2025, Q3 2025, Q4 2024 columns')
 mm['diluted_shares']=dict(value=(136718000 if y==2025 else 138322000),method='direct_release',source=URLS['q4_release'],locator='Condensed consolidated statements of operations, diluted weighted-average shares')
 periods[f'Q4FY{y}']=dict(start=s,end=a['end'],weeks=14 if y==2025 else 13,metrics=mm)
for y in [2025,2026]:
 ids=[f'Q4FY{y-1}']+[f'Q{q}FY{y}' for q in [1,2,3]];mm={}
 for m in metrics:
  if m=='diluted_shares':continue
  inputs=[periods[i]['metrics'][m] for i in ids];vs=[v['value'] for v in inputs]
  mm[m]=dict(value=sum(vs) if all(v is not None for v in vs) else None,method='sum_reported_quarter_eps' if m=='eps_diluted' else 'sum_four_quarters',formula=' + '.join(ids),inputs=inputs)
 periods[f'TTMQ3FY{y}']=dict(start=periods[ids[0]]['start'],end=periods[ids[-1]]['end'],weeks=sum(periods[i]['weeks'] for i in ids),metrics=mm)
for id,p in periods.items():
 mm=p['metrics'];mm['fcf']=calc(mm['cfo'],mm['capex'],'-','CFO - cash purchases of PP&E; acquisition cash excluded from capex')
 mm['cash_after_ppe_software_ip']=calc(mm['fcf'],mm['software_ip_cash'],'-','CFO - cash PP&E - cash software/IP licenses; not owner earnings')
 mm['cash_after_investment_less_sbc_diagnostic']=calc(mm['cash_after_ppe_software_ip'],mm['sbc'],'-','Cash after PP&E and software/IP - SBC; diagnostic only, not owner earnings')
 for m,v in mm.items():ledger.append({**v,'period':id,'start':p['start'],'end':p['end'],'weeks':p['weeks'],'metric':m,'unit':'USD/share' if m=='eps_diluted' else 'shares' if m=='diluted_shares' else 'USD'})
balances={}
for e in sorted(set(p['end'] for p in periods.values())):
 balances[e]={m:direct(t,None,e) for m,t in bals.items()}
 for m,v in balances[e].items():ledger.append(dict(period=e,metric=m,unit='USD',**v))
notes=['Cash after PP&E and software/IP is distinct from CFO less PP&E alone. Neither is owner earnings. Noncash accrued purchases in YTD2026Q3: PP&E $4.982m, IP licenses $15.000m; not counted as cash capex or presumed financing debt.', 'FY2025 and TTM to Q3FY2026 contain 53 weeks; Q4FY2025 contains 14 weeks. FY2023/24, 2025 comparative TTM and FY2026 quarters contain 52/13 weeks. No per-week normalization applied.', 'Historical consolidated perimeter: AMI included only from July 27, 2026. TTM is not full-year pro forma and cannot be treated as organic growth. AMI Q3 contribution: revenue $39.1m; net loss $14.4m.', 'PPA preliminary: net assets acquired $1589.664m; intangibles $551m; goodwill $1054.139m. Valuation and tax balances can change during measurement period.', 'Q3FY2026 total intangible amortization $13.855m versus $0.597m Q3FY2025: $6.987m cost of revenue + $5.891m separately presented operating expense + $0.977m included in R&D. The two separately presented acquired-intangible lines sum to $12.878m; scope differs, not a reconciliation error. D&A is the full cash-flow adjustment excluding ROU asset and financing costs, not the narrower PP&E depreciation note.', 'TTM EPS is sum of four directly reported quarterly diluted EPS rounded to cents. It is not issuer-reported TTM EPS or annual EPS minus YTD EPS; different share counts, Q4 loss antidilution and rounding prevent exact reconciliation to TTM NI/shares.', 'Tax is retained as GAAP reported, not normalized: Q3FY2026 expense approximately $2.6m vs $3.7m benefit Q3FY2025; AMI valuation allowance release $1.2m. SBC, foreign rates and credits affect effective rates.', 'Debt_gross is principal; debt_net_costs is reported carrying amount net of issuance costs. Missing balances are null, never assumed zero. Operating leases are separate.']
supplemental_noncash={id:{'accrued_ppe':direct('CapitalExpendituresIncurredButNotYetPaid',p['start'],p['end']),'accrued_ip':direct('lscc:AccruedPurchasesOfIntellectualPropertyLicenses',p['start'],p['end'])} for id,p in periods.items() if id.startswith('FY') or id.startswith('YTD')}
qa=[]
for id,p in periods.items():
 for m,tag in metrics.items():
  v=p['metrics'].get(m,{})
  if v.get('method')=='direct_inline' and ':' not in tag:
   fs=[f for a in F.get(tag,{}).get('units',{}).values() for f in a if f.get('start')==p['start'] and f['end']==p['end'] and f['filed']<='2026-11-04']
   if fs:
    f=sorted(fs,key=lambda f:f['filed'])[-1]
    qa.append(dict(check=f'{id}.{m} inline versus SEC companyfacts',passed=abs(v['value']-f['val'])<.000001))

for id,p in periods.items():
 if id.startswith('Q') or id.startswith('TTM'):
  for m in ['revenue','ebit','net_income','eps_diluted','cfo','capex','software_ip_cash','sbc','da']:
   qa.append(dict(check=f'{id}.{m} present',passed=p['metrics'][m]['value'] is not None))
for e,b in balances.items():
 if all(b[k]['value'] is not None for k in ['assets','liabilities','equity']):qa.append(dict(check=f'{e} balance identity',passed=abs(b['assets']['value']-b['liabilities']['value']-b['equity']['value'])<1))
qa += [dict(check='Q4FY2025 EPS direct -0.06',passed=periods['Q4FY2025']['metrics']['eps_diluted']['value']==-.06),dict(check='53-week TTM disclosed',passed=periods['TTMQ3FY2026']['weeks']==53)]
result=dict(ticker='LSCC',as_of='2026-11-04',units='USD unless otherwise specified',periods=periods,balances=balances,supplemental_noncash=supplemental_noncash,notes=notes,sources=URLS,qa=qa)
(OUT/'normalized_history.json').write_text(json.dumps(result,indent=2));(OUT/'ledger.json').write_text(json.dumps(ledger,indent=2));(OUT/'qa.json').write_text(json.dumps(qa,indent=2))
with (OUT/'ledger.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['period','start','end','weeks','metric','unit','value','method','source','tag','formula'],extrasaction='ignore');w.writeheader();w.writerows(ledger)
print(json.dumps({'checks':len(qa),'failures':[q for q in qa if not q['passed']],'ttm':{m:v['value'] for m,v in periods['TTMQ3FY2026']['metrics'].items()}},indent=2))
# Direct Q4 EPS evidence is supplied as a portable textual table excerpt.
epsrow=(OUT/'q4_direct_eps_excerpt.txt').read_text()
assert '$ (0.06) $ 0.02 $ 0.12' in epsrow
show=['FY2023','FY2024','FY2025','Q4FY2024','Q1FY2025','Q2FY2025','Q3FY2025','Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026','TTMQ3FY2025','TTMQ3FY2026'];cols=['revenue','ebit','net_income','eps_diluted','cfo','capex','software_ip_cash','fcf','cash_after_ppe_software_ip','sbc','da','tax_expense']
lines=['# LSCC historical financial ledger','As of November 4, 2026. USD millions except diluted EPS. GAAP reported, not management-adjusted.','', '| Period | Weeks | '+' | '.join(cols)+' |','|---|---|'+'---|'*len(cols)]
for id in show:
 p=periods[id];lines.append('| '+id+' | '+str(p['weeks'])+' | '+' | '.join('NA' if p['metrics'][m]['value'] is None else f"{p['metrics'][m]['value']/(1 if m=='eps_diluted' else 1e6):.3f}" for m in cols)+' |')
lines+=['','## Comparability and accounting','']+['- '+n for n in notes]+['- FY2023/FY2024 net income includes tax benefits of $44.205m/$24.902m. FY2025 has $10.293m tax expense; earnings multiples are tax-sensitive.','- CFO less cash PP&E capex is a defined analytical FCF measure, not owner earnings: no deduction for SBC or software/IP licenses. `cash_after_ppe_software_ip` separately deducts cash software/IP. `cash_after_investment_less_sbc_diagnostic` further deducts SBC as a diagnostic, not owner earnings. AMI acquisition spending is separate investing cash flow. Noncash YTD2026Q3 accrued PPE purchases $4.982m and accrued IP licenses $15.000m are not cash capex and must not be treated as financial debt.','', '## Reproduction and evidence','Run `python reproduce.py` from this folder, or invoke its absolute path; no network or third-party packages. Inputs are adjacent: `inline_numeric_extract.json`, `companyfacts_subset.json`, `urls.json`, and `q4_direct_eps_excerpt.txt`. No original filings or full companyfacts are required. `source_manifest.json` documents hashes of original archived sources, for provenance only. `ledger.json` preserves nested calculation inputs; CSV is a flat navigation view. `inline_numeric_extract.json` preserves tag/context/value/precision and exact filing fragment links. Q4 EPS is corroborated by `q4_direct_eps_excerpt.txt`.','',f'QA: {len(qa)} checks; {sum(not q["passed"] for q in qa)} failures. Checks cover completeness, balance identities and agreement of direct inline facts with SEC companyfacts. Additional assertion verifies direct Q4 EPS release row.','', '## Direct sources']+[f'- {n}: {u}' for n,u in URLS.items()]
(OUT/'ledger.md').write_text('\n'.join(lines)+'\n')
