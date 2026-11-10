"""Reproduce RMB-million schedules from preserved primary SEC HTML tables.
Run in this folder; source URLs are in public_sources.json and raw copies in sources/.
Amounts are in RMB thousands in sources; all output financial amounts are RMB millions.
"""
from pathlib import Path
from lxml import html
import re,json,csv
P=Path(__file__).resolve().parent
E=[]
def row(src,tab,label,n,occ=0):
 t=html.parse(str(P/'sources'/f'{src}.html')).xpath('//table')[tab]
 rows=[]
 for tr in t.xpath('.//tr'):
  cells=[' '.join(x.text_content().replace('\u200b','').split()) for x in tr.xpath('./td|./th')]
  if cells and cells[0]==label:rows.append(cells)
 c=rows[occ];s=' '.join(c[1:]);a=re.findall(r'\(?\s*[-]?\d[\d,]*(?:\.\d+)?\s*\)?|—',s)
 vals=[]
 for v in a:
  if v.strip()=='—':vals.append(0.0);continue
  neg='(' in v or '-' in v;z=float(re.sub('[^0-9.]','',v));vals.append(-z if neg else z)
 vals=vals[-n:];assert len(vals)==n,(src,tab,label,vals)
 E.append(dict(source=src,table=tab,label=label,values_thousands=vals));return vals
M={'revenue':('Net revenues',False),'ebit':('Operating profit',False),'net_income':('Net income',False),'parent_income':('Net income attributable to the Company’s shareholders',False),'da':('Depreciation and amortization',True),'sbc':('Share-based compensation cost',True),'cfo':('Net cash provided by operating activities',True),'capex':('Purchase of property, equipment and software',True),'content_capex':('Purchase of intangible assets, content and licensed copyrights',True),'contract_liability_cash':('Contract liabilities',True),'cash_taxes':('Cash paid for income taxes, net',True)}
D={}
def extract(src,it,ct,n,mapping):
 for key,(label,cf) in M.items():
  vals=row(src,ct if cf else it,label,n)
  for period,idx in mapping.items():D.setdefault(period,{})[key]=round((abs(vals[idx]) if key in ['capex','content_capex'] else vals[idx])/1000,6)
extract('S1',426,428,4,{'FY2023':0,'FY2024':1,'FY2025':2})
extract('S2',20,21,7,{'Q2_2025':0,'Q1_2026':1,'Q2_2026':2,'H1_2025':4,'H1_2026':5})
extract('S3',14,15,7,{'Q4_2024':0,'Q3_2025':1,'Q4_2025':2})
extract('S6',24,25,7,{'H1_2024':4})
for p,terms in {'TTM_Jun2026':[('FY2025',1),('H1_2025',-1),('H1_2026',1)],'TTM_Jun2025':[('FY2024',1),('H1_2024',-1),('H1_2025',1)]}.items():D[p]={k:round(sum(D[a][k]*b for a,b in terms),6) for k in M}
for d in D.values():
 d['fcf_simple']=round(d['cfo']-d['capex'],6);d['cash_after_content']=round(d['fcf_simple']-d['content_capex'],6);d['cash_after_content_sbc_diagnostic']=round(d['cash_after_content']-d['sbc'],6)
checks={}
for k in M:checks[k]=round(sum(D[q][k] for q in ['Q3_2025','Q4_2025','Q1_2026','Q2_2026'])-D['TTM_Jun2026'][k],6)
assert all(abs(x)<.002 for x in checks.values()),checks
B={}
for label,key,occ in [('Cash and cash equivalents','cash',0),('Time deposits','current_deposits',0),('Time deposits','noncurrent_deposits',1),('Restricted cash','restricted_current',0),('Restricted cash','restricted_noncurrent',1),('Short-term investments','short_investments',0),('Short-term loans','loans',0),('Contract liabilities','contract_liabilities',0),('Noncontrolling interests','nci_book',0),('Redeemable noncontrolling interests','redeemable_nci',0)]:B[key]=row('S2',19,label,3,occ)[1]/1000
B['issuer_netcash']=sum(B[k] for k in ['cash','current_deposits','noncurrent_deposits','restricted_current','restricted_noncurrent','short_investments'])-B['loans']
B['netcash_ex_restricted']=B['issuer_netcash']-B['restricted_current']-B['restricted_noncurrent']
C={'q2_revenue_growth_pct':(D['Q2_2026']['revenue']/D['Q2_2025']['revenue']-1)*100,'q2_ebit_growth_pct':(D['Q2_2026']['ebit']/D['Q2_2025']['ebit']-1)*100,'q2_parent_growth_pct':(D['Q2_2026']['parent_income']/D['Q2_2025']['parent_income']-1)*100,'q2_cfo_growth_pct':(D['Q2_2026']['cfo']/D['Q2_2025']['cfo']-1)*100,'h1_cfo_growth_pct':(D['H1_2026']['cfo']/D['H1_2025']['cfo']-1)*100,'ads_equiv_million_nov2':3201470116/5/1e6,'illustrative_equity_usdm':3201470116/5/1e6*129.35}
O=dict(units='RMB million except explicitly USD or percentages',asof='2026-11-10',periods=D,balance_June2026=B,diagnostics=C,quarter_sum_residuals=checks,entry_approved=False,valuation_status='unavailable',source_rows=E)
(P/'calculations.json').write_text(json.dumps(O,ensure_ascii=False,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(D.values())).keys()));w.writeheader();w.writerows(dict(period=p,**d) for p,d in D.items())
print(json.dumps(dict(periods=D,diagnostics=C,balance=B),indent=2))
