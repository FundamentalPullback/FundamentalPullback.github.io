"""HRB issuer-only refresh. USD thousands; source extraction and additive-period bridges.
Run beside sources/. No market-price retrieval; scanner price is historical, not executable.
"""
from pathlib import Path
import json,re,csv,hashlib
P=Path(__file__).resolve().parent
ledger=[]
def row(s,t,label,col):
 rows=next(a['rows'] for a in json.loads((P/'sources'/f'{s}_tables.json').read_text()) if a['table']==t)
 r=next(r for r in rows if r and r[0]==label)
 nums=[float(v.replace(',','').replace('(','-').replace(')','')) for v in r[1:] if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?',v)]
 value=nums[col];ledger.append(dict(source=s,table=t,label=label,column_zero_based=col,value=value));return value
cf={'da':'Depreciation and amortization','sbc':'Stock-based compensation','capex_signed':'Capital expenditures','acquisitions_signed':'Payments made for business acquisitions, net of cash acquired','dividends_signed':'Dividends paid','repurchases_signed':'Repurchase of common stock, including shares surrendered','franchise_funding_signed':'Franchise loans funded','franchise_repayments':'Payments from franchisees'}
def period(s,it,ic,ct,cc,positive=False):
 d={}
 if s=='S1':d['revenue']=row(s,it,'Total revenues',ic)
 else:d['revenue']=row(s,it,'Service revenues',ic)+row(s,it,'Royalty, product and other revenues',ic)
 d['opex']=row(s,it,'Total operating expenses',ic)
 d['ebit']=d['revenue']-d['opex']
 d['net_continuing']=row(s,it,'Net income from continuing operations' if positive else 'Net loss from continuing operations',ic)
 d['net_income']=row(s,it,'NET INCOME' if positive else 'NET LOSS',ic)
 for k,label in cf.items():d[k]=row(s,ct,label,cc)
 d['cfo']=row(s,ct,'Net cash provided by operating activities' if s in ['S3','S4'] else 'Net cash used in operating activities',cc)
 return d
p={'FY2026':period('S3',59,0,63,0,True),'FY2025':period('S3',59,1,63,1,True),'Q1FY2027':period('S1',6,0,12,0),'Q1FY2026':period('S6',6,0,10,0),'Q1FY2025':period('S6',6,1,10,1),'H1FY2026':period('S5',6,2,10,0),'9MFY2026':period('S4',6,2,10,0,True)}
def combine(*pairs):return {k:sum(p[name][k]*mult for name,mult in pairs) for k in p['FY2026']}
p['Q2FY2026']=combine(('H1FY2026',1),('Q1FY2026',-1))
p['Q3FY2026']=combine(('9MFY2026',1),('H1FY2026',-1))
p['Q4FY2026']=combine(('FY2026',1),('9MFY2026',-1))
p['TTM2026-09']=combine(('FY2026',1),('Q1FY2026',-1),('Q1FY2027',1))
p['TTM2025-09']=combine(('FY2025',1),('Q1FY2025',-1),('Q1FY2026',1))
for d in p.values():
 d['simple_fcf']=d['cfo']+d['capex_signed'];d['simple_fcf_less_sbc']=d['simple_fcf']-d['sbc'];d['ebit_margin_pct']=100*d['ebit']/d['revenue']
for k in p['FY2026']:
 if k=='ebit_margin_pct':continue
 assert abs(sum(p[q][k] for q in ['Q2FY2026','Q3FY2026','Q4FY2026','Q1FY2027'])-p['TTM2026-09'][k])<.001,k
out={'units':'USD thousands unless percentage','scanner':{'date':'2026-11-09','opportunity':100,'price_usd':51.02,'not_current_quote':True},'periods':p,'source_rows':ledger,'method':'Q2=H1-Q1; Q3=9M-H1; Q4=FY-9M; TTM=FY-Q1prior+Q1new. Simple FCF=CFO-capex, not FCFF. SBC subtraction is diagnostic only.'}
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(p['FY2026']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in p.items())
print(json.dumps({k:{a:round(v[a]/1000,3) for a in ['revenue','ebit','net_income','cfo','simple_fcf','sbc']} for k,v in p.items()},indent=2))
# Balance sheet evidence (two identically named lease rows retain their order).
b={}
for key,label in {'cash':'Cash and cash equivalents','restricted_cash':'Cash and cash equivalents - restricted','current_assets':'Total current assets','current_liabilities':'Total current liabilities','debt_book':'Long-term debt','equity':"Total stockholders' equity (deficiency)"}.items():
 b[key]=row('S1',10,label,0)
b['net_debt_book_excluding_restricted_cash']=b['debt_book']-b['cash']
out['balance_2026_09_30']=b;out['source_rows']=ledger
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
