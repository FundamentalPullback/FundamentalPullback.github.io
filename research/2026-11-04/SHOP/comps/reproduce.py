#!/usr/bin/env python3
"""Offline standard-library reproduction; output USD millions."""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent;D=json.loads((P/'comps_numeric_subsets.json').read_text())
def v(t,k,i,scale=1):return D[t][k][i]/scale
rows=[]
for i,period in enumerate(['2026Q2','2025Q2','2026H1','2025H1']):
 def w(t,k):return v('wix_table_'+str(t),k,i,1000)
 r=dict(ticker='WIX',period=period,revenue=w(1,'Creative Subscriptions')+w(1,'Business Solutions'),gaap_ebit=w(1,'Operating income (loss)'),gaap_ni=w(1,'Net income (loss)'),cfo=w(5,'Net cash provided by operating activities'),ppe_and_lease_cash=-w(5,'Purchase of property and equipment and lease prepayment'),software_cash_separate=-w(5,'Capitalization of internal use of software'),sbc=w(5,'Share based compensation expenses'),da=w(5,'Depreciation')+w(5,'Amortization'),reported_fcf=w(24,'Free Cash Flow'),adjusted_fcf=w(24,'Free Cash Flow excluding acquisition and restructuring costs'),fcf_restructuring_addback=w(24,'Restructuring and other costs'),fcf_acquisition_cost_addback=w(24,'Cash paid for acquisition-related costs'),non_gaap_ebit=w(20,'Non GAAP operating income'),perimeter='consolidated Wix including Base44; quarter ends June30')
 r['capex_total']=r['ppe_and_lease_cash']+r['software_cash_separate'];rows.append(r)
for i,period in enumerate(['2026Q3','2025Q3','2026YTD9M','2025YTD9M']):
 def e(t,k):return v('ebay_table_'+str(t),k,i)
 r=dict(ticker='EBAY',period=period,revenue=e(4,'Net revenues'),gaap_ebit=e(4,'Income from operations'),gaap_ni=e(4,'Income from continuing operations'),cfo=e(5,'Net cash provided by continuing operating activities'),consolidated_cfo=e(5,'Net cash provided by operating activities'),ppe_and_lease_cash=-e(5,'Purchases of property and equipment'),software_cash_separate=None,sbc=e(5,'Stock-based compensation'),da=e(5,'Depreciation and amortization'),reported_fcf=e(13,'Free cash flow'),adjusted_fcf=None,non_gaap_ebit=e(11,'Non-GAAP operating income'),acquisition_cash=-e(5,'Acquisition of Depop, net of cash acquired'),perimeter='continuing operations; Depop from July30 2026; prior comparatives retrospectively recast for software accounting')
 r['capex_total']=r['ppe_and_lease_cash'];rows.append(r)
for r in rows:
 assert abs(r['cfo']-r['capex_total']-r['reported_fcf'])<0.000001
 r['fcf_minus_sbc_sensitivity']=round(r['reported_fcf']-r['sbc'],3)
 r['gaap_operating_margin_pct']=round(100*r['gaap_ebit']/r['revenue'],4)
 r['reported_fcf_margin_pct']=round(100*r['reported_fcf']/r['revenue'],4)
 for k,val in r.items():
  if isinstance(val,float):r[k]=round(val,4)
for first,prior in [(0,1),(4,5)]:
 rows[first]['revenue_growth_pct']=round(100*(rows[first]['revenue']/rows[prior]['revenue']-1),4)
 rows[first]['fcf_growth_pct']=round(100*(rows[first]['reported_fcf']/rows[prior]['reported_fcf']-1),4)
(P/'operating_comps.json').write_text(json.dumps({'as_of':'2026-11-04','units':'USD millions except percentages','records':rows},indent=2)+'\n')
with (P/'operating_comps.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
print(json.dumps([rows[0],rows[4]],indent=2))
