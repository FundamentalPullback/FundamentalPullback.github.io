"""Reproduce UPS schedules from captured primary-source tables. USD millions."""
import json,csv,re
from pathlib import Path
R=Path(__file__).parent
T={s:json.loads((R/'sources'/f'{s}_tables.json').read_text()) for s in ['S1','S3','S4','S5','S6']}
def row(s,t,label):
 a=next(r for r in T[s][t] if r and r[0].strip()==label)
 out=[]
 for v in a[1:]:
  if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',v):out.append(0.0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')','')))
 return out
def period(s,it,ct,ic,cc):
 d={k:row(s,it,label)[ic] for k,label in [('revenue','Revenue'),('ebit','Operating Profit'),('net_income','Net Income'),('da','Depreciation and amortization')]}
 for k,label in [('cfo','Net cash from operating activities'),('capex','Capital expenditures'),('sbc','Stock compensation expense'),('pension_cash','Pension and postretirement benefit contributions')]:
  if s=='S6' and k=='sbc':label='Stock compensation expense (benefit)'
  d[k]=row(s,ct,label)[cc]*(-1 if k in ['capex','pension_cash'] else 1)
 d['simple_fcf']=d['cfo']-d['capex'];return d
def sub(a,b):return {k:a[k]-b[k] for k in a}
def add(a,b):return {k:a[k]+b[k] for k in a}
P={f'FY{y}':period('S3',35,37,i,i) for i,y in enumerate([2025,2024,2023])}
P['9M2026']=period('S1',8,10,2,0);P['9M2025']=period('S1',8,10,3,1);P['9M2024']=period('S6',8,10,3,1)
P['H12026']=period('S4',8,10,2,0);P['Q12026']=period('S5',8,10,0,0)
P['Q22026']=sub(P['H12026'],P['Q12026']);P['Q32026']=sub(P['9M2026'],P['H12026']);P['Q42025']=sub(P['FY2025'],P['9M2025']);P['TTM2026']=add(P['Q42025'],P['9M2026']);P['TTM2025']=add(sub(P['FY2024'],P['9M2024']),P['9M2025'])
D={'9M_cfo_change':5986-5148,'9M_pension_cash_reduction':1338-897,'9M_capex_reduction':2969-2221,'9M_simple_fcf_change':(5986-2221)-(5148-2969),'9M_company_fcf':5986-2221+473-18,'cash_diagnostic_after_noncash_pension_and_customer_refund':5986-2221-450-270,'debt_and_finance_leases':957+25121,'net_debt_simple':957+25121-6837,'operating_leases':725+3487,'class_A_plus_B_million':(99812037+751657335)/1e6,'illustrative_equity_value':(99812037+751657335)/1e6*110.96,'Q3_adjusted_ebit':1744+171+182-43,'Q3_2025_adjusted_ebit_ex_saleleaseback':1804+328-330,'9M_adjusted_ebit':3941+1398+182-43,'9M_2025_adjusted_ebit_ex_saleleaseback':5292+460+19-362,'9M_simple_fcf_minus_dividends':5986-2221-4064}
for metric in ['revenue','ebit','cfo','simple_fcf']:
 D['TTM_'+metric+'_growth_pct']=(P['TTM2026'][metric]/P['TTM2025'][metric]-1)*100
D['Q3_revenue_growth_pct']=(22853/21415-1)*100;D['Q3_ebit_growth_pct']=(1744/1804-1)*100
out={'units':'USD millions except ratios/percentages','periods':P,'diagnostics':D,'limits':['Simple FCF is CFO less cash capex, not normalized FCFF.','Pension-note and customer-refund diagnostic is not complete normalization.','Statement net income follows issuer presentation; two share classes required.','Quarterly cash derived by subtracting YTD; TTM FY minus prior9M plus current9M.']}
(R/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
with (R/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(P['FY2025']));w.writeheader();w.writerows(dict(period=p,**v) for p,v in P.items())
print(json.dumps(out,indent=2))
