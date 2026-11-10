"""Reproduce USD-million schedules from saved SEC HTML; inputs are USD thousands.
Cash outflows are converted to positive expenditure. FCF_simple includes PP&E
and capitalized software; FCF_extended also deducts intangible/other asset buys.
Neither is normalized FCFF. No share-based expense is removed from EBIT.
"""
from pathlib import Path
from lxml import html
import re,json,csv
P=Path(__file__).resolve().parent; E=[]
def row(s,t,labels,n,zero=False):
 if isinstance(labels,str):labels=[labels]
 for tr in html.parse(str(P/'sources'/f'{s}.html')).xpath('//table')[t].xpath('.//tr'):
  c=[' '.join(x.text_content().split()) for x in tr.xpath('./td|./th')]
  if c and c[0] in labels:
   vals=[]
   for x in c[1:]:
    if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',x):
     vals.append(0 if x=='—' else (-1 if '(' in x or '-' in x else 1)*float(re.sub('[^0-9.]','',x)))
   assert len(vals)==n,(s,t,c[0],vals)
   E.append(dict(source=s,table=t,label=c[0],values_thousands=vals));return vals
 if zero:return [0]*n
 raise ValueError((s,t,labels))
I={'revenue':'Revenue','gross_profit':'Gross profit','ebit':'Operating loss','net_income':['Net income (loss)','Net (loss) income','Net loss'],'interest_income':'Interest income'}
C={'da':'Depreciation and amortization expense','sbc':'Stock-based compensation expense','marketing_amort':'Amortization of prepaid marketing expense','commissions_amort':'Amortization of deferred contract acquisition costs','cfo':'Net cash provided by operating activities','ppe':'Acquisition of property and equipment','software':'Capitalization of software development costs','intangible':'Acquisition of intangible assets','other_capex':'Purchase of other non-current assets','commissions_cash':'Deferred contract acquisition costs','deferred_revenue_cash':'Deferred revenue','cash_taxes':['Cash paid for income taxes','Cash paid for income taxes, net of refunds']}
D={}
def extract(s,it,ct,ni,nc,im,cm):
 for k,label in I.items():
  v=row(s,it,label,ni)
  for period,j in im.items():D.setdefault(period,{})[k]=v[j]/1000
 for k,label in C.items():
  v=row(s,ct,label,nc,zero=k in ['intangible','other_capex'])
  for period,j in cm.items():D.setdefault(period,{})[k]=v[j]/1000*(-1 if k in ['ppe','software','intangible','other_capex','commissions_cash'] else 1)
extract('S3',25,28,3,3,{'FY2025':0,'FY2024':1,'FY2023':2},{'FY2025':0,'FY2024':1,'FY2023':2})
extract('S1',9,12,4,2,{'Q3_2026':0,'Q3_2025':1,'9M2026':2,'9M2025':3},{'9M2026':0,'9M2025':1})
extract('S4',9,12,4,2,{'Q2_2026':0,'Q2_2025':1,'H1_2026':2,'H1_2025':3},{'H1_2026':0,'H1_2025':1})
extract('S5',9,12,4,2,{'9M2024':3},{'9M2024':1})
# Q1 operations from cumulative differences; Q1 cash directly from Q1 filing.
for yr in ['2026','2025']:
 for k in I:D.setdefault('Q1_'+yr,{})[k]=D['H1_'+yr][k]-D['Q2_'+yr][k]
for k,label in C.items():
 v=row('S7',11,label,2,zero=k in ['intangible','other_capex'])
 for yr,j in [('2026',0),('2025',1)]:D['Q1_'+yr][k]=v[j]/1000*(-1 if k in ['ppe','software','intangible','other_capex','commissions_cash'] else 1)
for yr in ['2026','2025']:
 for k in C:
  D['Q2_'+yr][k]=D['H1_'+yr][k]-D['Q1_'+yr][k]
  D['Q3_'+yr][k]=D['9M'+yr][k]-D['H1_'+yr][k]
D['Q4_2025']={k:D['FY2025'][k]-D['9M2025'][k] for k in I|C}
D['TTM2026']={k:D['FY2025'][k]-D['9M2025'][k]+D['9M2026'][k] for k in I|C}
D['TTM2025']={k:D['FY2024'][k]-D['9M2024'][k]+D['9M2025'][k] for k in I|C}
for v in D.values():
 v['fcf_simple']=v['cfo']-v['ppe']-v['software'];v['fcf_extended']=v['fcf_simple']-v['intangible']-v['other_capex'];v['fcf_less_sbc_diagnostic']=v['fcf_extended']-v['sbc'];v['ebit_margin_pct']=100*v['ebit']/v['revenue']
 for k in v:v[k]=round(v[k],6)
for k in I|C:assert abs(sum(D[q][k] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])-D['TTM2026'][k])<.00001,k
X={'q3_revenue_growth_pct':(D['Q3_2026']['revenue']/D['Q3_2025']['revenue']-1)*100,'q3_cfo_growth_pct':(D['Q3_2026']['cfo']/D['Q3_2025']['cfo']-1)*100,'q3_fcf_reported_growth_pct':(24.797/47.055-1)*100,'shares_october31_m':(130150680+151411698)/1e6,'market_cap_october31_shares_m':20.72*(130150680+151411698)/1e6,'shares_september_m':(130925592+151416058)/1e6,'illustrative_market_cap_m':20.72*(130925592+151416058)/1e6,'lease_liabilities_m':27.484+106.850,'commission_asset_m':41.550+65.178,'9m_commission_investment_above_amort_m':61.345-32.020,'9m_fcf_reported':126.223,'9m_fcf_2025_reported':112.927,'9m_2025_employer_tax_addback':10.833,'9m_2026_adjusted_fcf':141.522,'q3_non_gaap_op_reconciliation':-4.489+42.140+1.248+13.224+4.808}
(P/'calculations.json').write_text(json.dumps({'units':'USD millions unless explicitly stated','periods':D,'diagnostics':X,'source_rows':E,'entryApproved':False,'valuation':'unavailable'},indent=2)+'\n')
with (P/'financials.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(D.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in D.items())
print(json.dumps({k:D[k] for k in ['Q3_2026','TTM2026','TTM2025']},indent=2))
