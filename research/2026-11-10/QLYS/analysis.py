"""Reproduce historical USD-million data from saved SEC HTML (input thousands).
No DCF or current fair-value claim. Old A130 valuation remains historical.
"""
from pathlib import Path
from lxml import html
import re,json,csv
P=Path(__file__).resolve().parent; E=[];D={}
def row(s,t,label,n):
 for tr in html.parse(str(P/'sources'/f'{s}.html')).xpath('//table')[t].xpath('.//tr'):
  a=[' '.join(td.text_content().split()) for td in tr.xpath('./td|./th')]
  if a and a[0]==label:
   v=[0 if x=='—' else (-1 if '(' in x or '-' in x else 1)*float(re.sub('[^0-9.]','',x)) for x in a[1:] if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',x)]
   assert len(v)==n,(s,t,label,v);E.append(dict(source=s,table=t,label=label,values_thousands=v));return v
 raise ValueError((s,t,label))
I={'revenue':'Revenues','ebit':'Income from operations','net_income':'Net income','interest_income':'Interest income','tax_expense':'Income tax provision'}
C={'da':'Depreciation and amortization expense','sbc':'Stock-based compensation, net of amounts capitalized','cfo':'Net cash provided by operating activities','capex':'Purchases of property and equipment','deferred_tax':'Deferred income taxes','wc_receivables':'Accounts receivable','wc_prepaids':'Prepaid expenses and other assets','wc_payables':'Accounts payable','wc_accruals':'Accrued liabilities and other noncurrent liabilities','wc_deferred_revenue':'Deferred revenues','repurchases':'Repurchase of common stock','option_proceeds':'Proceeds from exercise of stock options','award_tax':'Payments for taxes related to net share settlement of equity awards'}
def extract(s,it,ct,ni,nc,im,cm):
 for k,l in I.items():
  v=row(s,it,l,ni)
  for p,j in im.items():D.setdefault(p,{})[k]=v[j]/1000
 for k,l in C.items():
  v=row(s,ct,l,nc)
  for p,j in cm.items():D.setdefault(p,{})[k]=v[j]/1000*(-1 if k in ['capex','repurchases','award_tax'] else 1)
extract('S3',22,24,3,3,{'FY2025':0,'FY2024':1,'FY2023':2},{'FY2025':0,'FY2024':1,'FY2023':2})
extract('S1',9,11,4,2,{'Q3_2026':0,'Q3_2025':1,'9M2026':2,'9M2025':3},{'9M2026':0,'9M2025':1})
extract('S4',9,11,4,2,{'Q2_2026':0,'Q2_2025':1,'H1_2026':2,'H1_2025':3},{'H1_2026':0,'H1_2025':1})
extract('S5',9,11,4,2,{'9M2024':3},{'9M2024':1})
extract('S6',9,11,2,2,{'Q1_2026':0,'Q1_2025':1},{'Q1_2026':0,'Q1_2025':1})
for y in ['2026','2025']:
 for k in C:
  D['Q2_'+y][k]=D['H1_'+y][k]-D['Q1_'+y][k];D['Q3_'+y][k]=D['9M'+y][k]-D['H1_'+y][k]
D['Q4_2025']={k:D['FY2025'][k]-D['9M2025'][k] for k in I|C}
D['TTM2026']={k:D['FY2025'][k]-D['9M2025'][k]+D['9M2026'][k] for k in I|C}
D['TTM2025']={k:D['FY2024'][k]-D['9M2024'][k]+D['9M2025'][k] for k in I|C}
for v in D.values():
 v['fcf_simple']=v['cfo']-v['capex'];v['fcf_less_sbc_diagnostic']=v['fcf_simple']-v['sbc'];v['ebit_margin_pct']=100*v['ebit']/v['revenue'];v['listed_wc_cash']=sum(v[k] for k in C if k.startswith('wc_'))
 for k in v:v[k]=round(v[k],6)
for k in I|C:assert abs(sum(D[q][k] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])-D['TTM2026'][k])<.00001,k
X={}
for period,prior in [('Q3_2026','Q3_2025'),('TTM2026','TTM2025')]:
 for k in ['revenue','ebit','net_income','cfo','fcf_simple']:X[period+'_'+k+'_growth_pct']=(D[period][k]/D[prior][k]-1)*100
X.update(financial_assets_september_m=357.191+163.552+287.296,financial_assets_june_m=250.291+176.003+277.171,lease_liabilities_m=9.213+42.028,commission_asset_m=9.788+19.536,commission_asset_change_m=(9.788+19.536)-(8.705+17.560),shares_september_m=34.924,shares_october23_m=34.909416,market_cap_reference_m=197.31*34.909416,options_september_m=.756,options_strike=129.04,rsu_september_m=1.136,illustrative_tsm_option_increment_m=.756*(1-129.04/197.31),illustrative_spot_dilution_m=34.924+1.136+.756*(1-129.04/197.31),q3_basic_share_change_m=34.924-34.651,q3_issue_option_shares_m=.520,q3_option_cash_m=65.615-.934,old_A130_central=109.43,old_A130_date='2026-11-02',old_value_not_refreshed=True)
(P/'calculations.json').write_text(json.dumps(dict(units='USD millions except shares in millions, percentages and per-share USD',periods=D,diagnostics=X,source_rows=E,entryApproved=False,valuation='unavailable; historical A130 not rerun'),indent=2)+'\n')
with (P/'financials.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(D.values())).keys()));w.writeheader();w.writerows(dict(period=p,**v) for p,v in D.items())
print(json.dumps({k:D[k] for k in ['Q3_2026','TTM2026','TTM2025']},indent=2))
