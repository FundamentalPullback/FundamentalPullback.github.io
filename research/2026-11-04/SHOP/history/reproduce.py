#!/usr/bin/env python3
"""Offline, stdlib-only SHOP financial-history reproduction. All dollars USD millions except EPS."""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'source_numeric_subsets.json').read_text())
F={'da':'Amortization and depreciation','sbc':'Stock-based compensation','cfo':'Net cash provided by operating activities','ppe_cash_signed':'Purchases of property and equipment','lending_originations_cash_signed':'Purchases and originations of loans','lending_repayments_cash':'Repayments and sales of loans'}
def cf(table,i):return {k:D[table][v][i] for k,v in F.items()}
def income(table,i,annual=False):
 t=D[table]
 return dict(revenue=t['Subscription solutions'][i]+t['Merchant solutions'][i],gross_profit=t['Gross profit'][i],gaap_ebit=t['Income (loss) from operations' if annual else 'Income from operations'][i],gaap_net_income=t['Net income' if annual else 'Net income (loss)'][i],direct_diluted_eps=t['Diluted'][i])
def decorate(r):
 r['ppe_cash_spend']=-r['ppe_cash_signed'];r['net_investing_lending_funding']=-r['lending_originations_cash_signed']-r['lending_repayments_cash']
 r['cfo_minus_ppe']=r['cfo']-r['ppe_cash_spend']
 r['cfo_minus_ppe_legacy_presentation']=r['cfo_minus_ppe']-r['mca_presentation_shift']
 r['cash_after_ppe_and_investing_lending']=r['cfo_minus_ppe']-r['net_investing_lending_funding']
 r['cash_after_ppe_lending_intangibles']=r['cash_after_ppe_and_investing_lending']-r['intangible_cash_spend']
 r['cash_after_ppe_lending_intangibles_sbc']=r['cash_after_ppe_lending_intangibles']-r['sbc']
 r['operating_margin_pct']=round(100*r['gaap_ebit']/r['revenue'],4)
 return r
rows=[]
for i,y in enumerate([2025,2024,2023]):
 r=dict(period=f'FY{y}',kind='FY',**income('fy25_table_38',i,True),**cf('fy25_table_40',i),mca_presentation_shift=0,intangible_cash_spend=0,source_tables='fy25_table_38;fy25_table_40',cash_method='direct')
 r['mca_cash_flow_already_in_cfo']=D['fy25_table_40']['Merchant cash advances and related receivables, net'][i]
 rows.append(decorate(r))
qs=[]
for i,period in enumerate(['2026Q3','2026Q2','2026Q1','2025Q4','2025Q3','2025Q2','2025Q1','2024Q4']):
 if i in [3,7]:
  ai=0 if i==3 else 1;ni=2 if i==3 else 3
  a=cf('fy25_table_40',ai);n=cf('q3prior_table_14',ni);cash={k:a[k]-n[k] for k in a};src='fy25_table_40 minus q3prior_table_14';method='Q4 additive cash items = FY minus 9M; EPS direct quarterly table'
 else:
  table={0:'q3_table_14',1:'q2_table_14',2:'q1_table_14',4:'q3_table_14',5:'q2_table_14',6:'q1_table_14'}[i];cash=cf(table,0 if i<3 else 1);src=table;method='direct'
 r=dict(period=period,kind='quarter',**income('q3_table_54',i),**cash,mca_presentation_shift={0:30,1:37}.get(i,0),intangible_cash_spend=99 if i==0 else 0,source_tables='q3_table_54;'+src,cash_method=method,mca_cash_flow_already_in_cfo=None)
 qs.append(decorate(r))
rows+=qs
additive=['revenue','gross_profit','gaap_ebit','gaap_net_income',*F.keys(),'mca_presentation_shift','intangible_cash_spend']
for period,block in [('TTM2026Q3',qs[:4]),('TTM2025Q3',qs[4:])]:
 r=dict(period=period,kind='TTM',**{k:sum(q[k] for q in block) for k in additive},direct_diluted_eps=None,sum_reported_quarterly_diluted_eps=round(sum(q['direct_diluted_eps'] for q in block),2),source_tables='sum of four quarterly records',cash_method='sum additive quarterly items; EPS sum separately labeled, not GAAP TTM EPS',mca_cash_flow_already_in_cfo=None)
 rows.append(decorate(r))
assert qs[0]['cash_after_ppe_and_investing_lending']==587
assert rows[-2]['cfo_minus_ppe']==2661 and rows[-1]['cfo_minus_ppe']==1903
assert rows[-2]['net_investing_lending_funding']==789
assert sum(q['cfo'] for q in qs[:3])==D['q3_table_14']['Net cash provided by operating activities'][2]
result={'ticker':'SHOP','units':'USD millions except EPS USD/share and percentages','as_of':'2026-11-04','records':rows}
(P/'shop_financial_history.json').write_text(json.dumps(result,indent=2)+'\n')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (P/'shop_financial_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
print(json.dumps(rows[-2:],indent=2))
