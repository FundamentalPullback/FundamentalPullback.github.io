from pathlib import Path
import json,csv,re
from decimal import Decimal as D
from lxml import html
P=Path(__file__).parent
labels={'revenue':'Revenues','ebit':'Operating Income','net_parent':'Net Income Attributable to Ingersoll Rand Inc.','amortization':'Amortization of intangible assets','depreciation':'Depreciation','sbc':'Stock-based compensation expense','cfo':'Net cash provided by operating activities','capex':'Capital expenditures','acquisition_cash':'Net cash paid in acquisitions'}
def parse(n):
 doc=html.fromstring((P/'sources'/f'{n}.html').read_bytes()); ts=doc.xpath('//table');inc=next(t for t in ts if 'Operating Income' in t.text_content() and 'Basic earnings' in t.text_content());cf=next(t for t in ts if 'Net cash provided by operating activities' in t.text_content() and 'Capital expenditures' in t.text_content() and 'Cash Flows From Operating Activities' in t.text_content());out={}
 for k,l in labels.items():
  t=inc if k in ['revenue','ebit','net_parent'] else cf
  for tr in t.xpath('.//tr'):
   c=[' '.join(x.text_content().split()) for x in tr.xpath('./td|./th')]
   if c and (c[0]==l or (k=='net_parent' and c[0]=='Net Income (Loss) Attributable to Ingersoll Rand Inc.')):
    vals=[]
    for x in c[1:]:
     y=x.replace(',','').replace(' ','').replace('$','');y=y.replace('(','-').replace(')','');y='0' if y=='—' else y
     if re.fullmatch('-?\d+(\.\d+)?',y):vals.append(D(y))
    out[k]=vals;break
 return out
raw={n:parse(n) for n in ['fy2025','q3_2026','q2_2026','q1_2026','q3_2025']}
rows={}
def take(n,i,j=None):
 return {k:abs(v[j if j is not None and k not in ['revenue','ebit','net_parent'] else i]) if k in ['capex','acquisition_cash'] else v[j if j is not None and k not in ['revenue','ebit','net_parent'] else i] for k,v in raw[n].items()}
for i,y in enumerate([2025,2024,2023]):rows[f'FY{y}']=take('fy2025',i)
rows['9M2026']=take('q3_2026',2,0);rows['9M2025']=take('q3_2026',3,1);rows['9M2024']=take('q3_2025',3,1)
rows['H12026']=take('q2_2026',2,0);rows['Q12026']=take('q1_2026',0)
def diff(a,b):return {k:a[k]-b[k] for k in labels}
rows['Q22026']=diff(rows['H12026'],rows['Q12026']);rows['Q32026']=diff(rows['9M2026'],rows['H12026']);rows['Q42025']=diff(rows['FY2025'],rows['9M2025'])
for y in [2025,2026]:rows[f'TTM{y}']={k:rows[f'FY{y-1}'][k]-rows[f'9M{y-1}'][k]+rows[f'9M{y}'][k] for k in labels}
for r in rows.values():r['da']=r['amortization']+r['depreciation'];r['simple_fcf']=r['cfo']-r['capex']
diag={'q3_ebit_ex_recoveries_refunds':D('782.5')-D('380.1')-D('32.3'),'9m_ebit_ex_recoveries_refunds':D('1452.5')-D('405.1')-D('42.6'),'9m2025_ebit_ex_impairments':D('754.4')+D('265.8'),'ttm_ebit_ex_recoveries_refunds':rows['TTM2026']['ebit']-D('405.1')-D('42.6'),'9m_fcf_less_gross_collections_refunds':rows['9M2026']['simple_fcf']-D('187.5')-D('42.6'),'ttm_fcf_less_gross_collections_refunds_sbc':rows['TTM2026']['simple_fcf']-D('187.5')-D('42.6')-rows['TTM2026']['sbc'],'book_net_debt':D('4736.5')-D('1342.7'),'face_debt_plus_finance_other':D('4736.5')+D('33.9')+D('32.5')+D('8.7'),'uncollected_gross_settlement':D('425.1')-D('187.5')}
def conv(o):
 if isinstance(o,dict):return {k:conv(v) for k,v in o.items()}
 if isinstance(o,list):return [conv(x) for x in o]
 return float(o) if isinstance(o,D) else o
(P/'calculations.json').write_text(json.dumps(conv({'units':'USD millions','raw_statement_rows':raw,'periods':rows,'diagnostics':diag,'limits':'Diagnostic cash deductions are gross, pre-tax/timing reconciliation; not normalized FCFF. New IVEK purchase price/cash bridge unavailable.'}),indent=2))
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(rows.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in rows.items())
print(json.dumps(conv({'periods':rows,'diagnostics':diag}),indent=2))
