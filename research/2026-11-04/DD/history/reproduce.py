"""Offline, standard-library-only DD history build from included numeric subsets.
Run python reproduce.py. No network calls, dependencies or original filings required.
USD millions except EPS and ratios; positive capex = cash spent.
"""
import json,pathlib,csv
P=pathlib.Path(__file__).resolve().parent; S=json.loads((P/'source_numeric_subsets.json').read_text())
def get(t,s,i=0):
 rows=[r for r in S[t]['rows'] if s.lower() in r['label'].lower()]
 assert rows,(t,s)
 return rows[0]['values'][i]
def base(name,inc,cf,ii,ci,eps_factor=1):
 g=lambda s:get(inc,s,ii); c=lambda s:get(cf,s,ci)
 x={'period':name,'revenue':g('Net sales'),'cost_of_sales':g('Cost of sales'),'research_development':g('Research and development'),'selling_general_administrative':g('Selling, general'),'intangible_amortization':g('Amortization of intangibles'),'restructuring':g('Restructuring'),'acquisition_integration_separation':g('Acquisition, integration'),'pretax_continuing_income':g('before income taxes'),'interest_expense':g('Interest expense'),'continuing_net_income':g('operations, net of tax'),'diluted_eps_continuing_as_reported':g('operations - diluted') if inc.startswith('fy') else g('operations – diluted') if inc.startswith(('q1','q2')) else g('operations - diluted'),'eps_split_multiplier':eps_factor,'continuing_cfo':c('Cash provided by operating activities'),'capex':-c('Capital expenditures'),'depreciation_amortization':c('Depreciation and amortization'),'stock_based_compensation': c('Stock based compensation') if inc.startswith(('fy','q1','q2')) else c('Stock-based compensation'),'discontinued_cfo':c('Cash provided by operations - discontinued') if inc.startswith('fy') else c('operating activities – discontinued') if inc.startswith(('q1','q2')) else c('operating activities - discontinued'),'source_tables':[inc,cf]}
 x['goodwill_impairment']=g('Goodwill impairment') if inc.startswith('fy') else 0
 return x
annual=[base('FY2023','fy25_38','fy25_41',2,2,3),base('FY2024','fy25_38','fy25_41',1,1,3),base('FY2025','fy25_38','fy25_41',0,0,3)]
q1=base('Q1 2026','q1_7','q1_10',0,0,3); q2=base('Q2 2026','q2_7','q2_10',0,0); q3=base('Q3 2026','q3_7','q3_10',0,0)
ytd25=base('9M2025','q3_7','q3_10',3,1); ytd26=base('9M2026','q3_7','q3_10',2,0)
flow=['continuing_cfo','capex','depreciation_amortization','stock_based_compensation','discontinued_cfo']
for k in flow:
 q2[k]-=q1[k]
 q3[k]-=q1[k]+q2[k]
nonadd={'period','source_tables','diluted_eps_continuing_as_reported','eps_split_multiplier'}
q4={'period':'Q4 2025','source_tables':['fy25_38','fy25_41','fy25_70','fy25_132','q3_7','q3_10','q3_26'],'diluted_eps_continuing_as_reported':get('fy25_132','operations - diluted',3),'eps_split_multiplier':3}
for k in annual[-1]:
 if k not in nonadd:q4[k]=annual[-1][k]-ytd25[k]
# Continuing income available to common is direct EPS-note numerator, not total NI minus total NCI.
for r,i in zip(annual,[2,1,0]):r['continuing_net_income_common']=get('fy25_70','operations attributable to common',i)
ytd25['continuing_net_income_common']=get('q3_26','operations attributable to common',3)
ytd26['continuing_net_income_common']=get('q3_26','operations attributable to common',2)
q4['continuing_net_income_common']=annual[-1]['continuing_net_income_common']-ytd25['continuing_net_income_common']
q2['continuing_net_income_common']=get('q2_26','operations attributable to common',0)
q1['continuing_net_income_common']=get('q2_26','operations attributable to common',2)-q2['continuing_net_income_common']
q3['continuing_net_income_common']=get('q3_26','operations attributable to common',0)
qs=[q4,q1,q2,q3];ttm={'period':'TTM 2026-09-30','source_tables':sorted(set(t for q in qs for t in q['source_tables'])),'diluted_eps_continuing_as_reported':None,'eps_split_multiplier':None}
for k in q4:
 if k not in nonadd:ttm[k]=sum(q[k] for q in qs)
for r in annual+qs+[ttm,ytd25,ytd26]:
 r['ebit_pretax_plus_interest']=r['pretax_continuing_income']+r['interest_expense']
 r['operating_profit_calculated']=r['revenue']-sum(r[k] for k in ['cost_of_sales','research_development','selling_general_administrative','intangible_amortization','restructuring','acquisition_integration_separation','goodwill_impairment'])
 r['actual_continuing_fcf']=r['continuing_cfo']-r['capex']
 r['gross_margin_pct']=round(100*(r['revenue']-r['cost_of_sales'])/r['revenue'],4)
 for k in ['ebit_pretax_plus_interest','operating_profit_calculated','continuing_net_income','actual_continuing_fcf']:
  r[k+'_margin_pct']=round(100*r[k]/r['revenue'],4)
 r['diluted_eps_split_adjusted_rounded']=round(r['diluted_eps_continuing_as_reported']*r['eps_split_multiplier'],2) if r['eps_split_multiplier'] else None
 if r is ttm:r['sum_quarterly_split_adjusted_eps_approximate']=round(sum(q['diluted_eps_split_adjusted_rounded'] for q in qs),2)
 r['eps_note']='Historical x3 conversion uses already-rounded direct filing EPS; not a newly reported EPS. TTM EPS is not computed from NI/shares.' if r.get('eps_split_multiplier')==3 or r is ttm else 'Direct filing continuing diluted EPS, post-reverse-split scale.'
# Segment revenue and company-defined segment EBITDA. Corporate is not allocated to segment margins.
segments=[]
for name,t,idx in [('FY2023','fy25_124',4),('FY2024','fy25_124',2),('FY2025','fy25_124',0),('9M2025','q3_46',2),('9M2026','q3_46',0),('Q1 2026','q1_39',0),('Q2 2026','q2_45',0),('Q3 2026','q3_45',0)]:
 for offset,label in enumerate(['Healthcare & Water Technologies','Diversified Industrials']):
  segments.append({'period':name,'segment':label,'revenue':get(t,'Segment net sales',idx+offset),'segment_operating_ebitda':get(t,'Segment operating EBITDA',idx+offset),'source_tables':[t]})
for label in ['Healthcare & Water Technologies','Diversified Industrials']:
 f=lambda p:next(r for r in segments if r['period']==p and r['segment']==label)
 for period,a,b,c in [('Q4 2025','FY2025','9M2025',None),('TTM 2026-09-30','FY2025','9M2025','9M2026')]:
  row={'period':period,'segment':label,'source_tables':list(dict.fromkeys(f(a)['source_tables']+f(b)['source_tables']+(f(c)['source_tables'] if c else [])))}
  for k in ['revenue','segment_operating_ebitda']:row[k]=f(a)[k]-f(b)[k]+(f(c)[k] if c else 0)
  segments.append(row)
for r in segments:r['segment_operating_ebitda_margin_pct']=round(100*r['segment_operating_ebitda']/r['revenue'],4)
result={'units':'USD millions except per-share USD and percentages','perimeter':'Continuing operations, excludes Electronics/Qnity and Aramids for all presented periods; not pro-forma standalone cost/financing structure','annual':annual,'quarters':qs,'ttm':ttm,'ytd':[ytd25,ytd26],'segments':segments}
(P/'financial_history.json').write_text(json.dumps(result,indent=2)+'\n')
for filename,rows in [('financial_history.csv',annual+qs+[ttm]),('segment_history.csv',segments)]:
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (P/filename).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
assert all(sum(q[k] for q in qs)==ttm[k] for k in ['revenue','continuing_cfo','capex','continuing_net_income'])
assert ttm['revenue']==7061 and ttm['actual_continuing_fcf']==793
print(json.dumps({'ttm':ttm,'annual_fcf':[r['actual_continuing_fcf'] for r in annual]},indent=2))
