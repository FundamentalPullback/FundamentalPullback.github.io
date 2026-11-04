from pathlib import Path
import json,csv
P=Path(__file__).parent; S=P/'sources'; H=P/'history'; H.mkdir(exist_ok=True)
urls=json.loads((S/'filing_urls.json').read_text()); source_rows=[]
def n(x):
 x=x.strip().replace('$','').replace(',','').replace('—','0').replace('–','0')
 return -float(x[1:-1]) if x.startswith('(') else float(x)
def tables(file):return json.loads((S/(file+'_tables.json')).read_text())
def find(ts,marker):return next(t for t in ts if any(row and row[0]==marker for row in t['rows']))
def extract(file,table,col,mapping,period):
 out={}
 for key,prefix in mapping.items():
  hits=[r for r in table['rows'] if r and (r[0]==prefix or r[0].startswith(prefix+' (') or (prefix=='Interest expense, net' and r[0].startswith(prefix)))]
  if not hits:out[key]=None;continue
  r=hits[0];out[key]=n(r[col]);source_rows.append(dict(period=period,field=key,value=out[key],unit='USD million except EPS/shares',source_url=urls[file+'.html'],table=table['table'],row=r[0],column=col))
 return out
ops={'revenue':'Total revenue','services':'Services','products':'Product sales','cost_services':'Cost of services','cost_products':'Cost of sales','charges':'Impairments and other charges','sga':'General and administrative','sap':'SAP S4 upgrade expense','ebit':'Operating income','interest_net_signed':'Interest expense, net','pretax':'Income before income taxes','tax_signed':'Income tax provision','net_income':'Net income','net_income_common':'Net income attributable to company','diluted_shares':'Diluted weighted average common shares outstanding'}
cf={'cfo':'Total cash flows provided by operating activities','da':'Depreciation, depletion, and amortization','ar_cash':'Receivables','inventory_cash':'Inventories','ap_cash':'Accounts payable','other_operating':'Other operating activities','capex_signed':'Capital expenditures','ppe_sales':'Proceeds from sales of property, plant, and equipment','acquisitions_signed':'Payments to acquire businesses, net of cash acquired','interest_cash':'Interest','tax_cash':'Income taxes','buybacks_signed':'Stock repurchase program','dividends_signed':'Dividends to shareholders'}
rows={}
file='hal-20251231';ts=tables(file);ot=find(ts,'Total operating costs and expenses');ct=find(ts,'Cash flows from operating activities:')
for y,col in [(2025,1),(2024,2),(2023,3)]:
 label='FY'+str(y);rows[label]=extract(file,ot,col,ops,label)|extract(file,ct,col,cf,label);rows[label]['sbc_actual']={2025:213,2024:223,2023:219}[y]; source_rows.append(dict(period=label,field='sbc_actual',value=rows[label]['sbc_actual'],unit='USD million',source_url=urls[file+'.html'],table='Note14 stock compensation',row='Stock-based compensation cost',column=col)); rows[label]['days']=365 if y!=2024 else 366
for file,labels in [('hal-20260930',['Q3_2026','Q3_2025','9M_2026','9M_2025']),('hal-20260630',['Q2_2026','Q2_2025','H1_2026','H1_2025']),('hal-20260331',['Q1_2026','Q1_2025']),('hal-20250930',['Q3_2025','Q3_2024','9M_2025','9M_2024'])]:
 ts=tables(file);ot=find(ts,'Total operating costs and expenses');ct=find(ts,'Cash flows from operating activities:')
 for i,label in enumerate(labels):
  if label in rows:continue
  rows[label]=extract(file,ot,i+1,ops,label)
  if len(labels)==2 or i>=2:rows[label].update(extract(file,ct,i-1 if len(labels)>2 else i+1,cf,label))
  rows[label]['sbc_actual']=None
# derive cumulative cash deltas; no fake quarterly EPS/share sum
for y in [2025,2026]:
 for q,hi,lo in [(2,'H1','Q1'),(3,'9M','H1')]:
  for k in cf:rows[f'Q{q}_{y}'][k]=rows[f'{hi}_{y}'][k]-rows[f'{lo}_{y}'][k] if rows[f'{hi}_{y}'].get(k)!=None and rows[f'{lo}_{y}'].get(k)!=None else None

def combine(label,terms):
 out={}
 for k in list(ops)+list(cf):
  if k=='diluted_shares':continue
  vals=[rows[a].get(k) for a,_ in terms];out[k]=None if None in vals else sum(rows[a][k]*mult for a,mult in terms)
 out['sbc_actual']=None;rows[label]=out
combine('Q4_2025',[('FY2025',1),('9M_2025',-1)])
combine('TTM_2026_09',[('FY2025',1),('9M_2026',1),('9M_2025',-1)])
combine('TTM_2025_09',[('FY2024',1),('9M_2025',1),('9M_2024',-1)])
# quarter cash flow does not separately disclose SBC expense. The equity issuance line is NOT SBC expense.
for label,r in rows.items():
 r['period']=label
 r['gross_profit']=r['revenue']-r['cost_services']-r['cost_products']
 r['adjusted_ebit_ex_charges']=r['ebit']+r['charges']
 r['normalized_ebit_pre_sap_after_0_5pct_recurring_reserve']=r['ebit']+r['charges']+r['sap']-.005*r['revenue']
 r['normalized_nopat_23pct']=r['normalized_ebit_pre_sap_after_0_5pct_recurring_reserve']*.77
 if r.get('capex_signed') is not None:
  r['capex']=-r['capex_signed'];r['fcf_ex_asset_sales']=r['cfo']-r['capex'];r['issuer_fcf_incl_ppe_sales']=r['fcf_ex_asset_sales']+r['ppe_sales'];r['trade_wc_cash']=r['ar_cash']+r['inventory_cash']+r['ap_cash']
  r['sbc_analyst_mid']=r['sbc_actual'] if r['sbc_actual'] is not None else r['revenue']*.01
  r['owner_cash_after_sbc_mid']=r['fcf_ex_asset_sales']-r['sbc_analyst_mid']
  r['owner_cash_trade_wc_neutral_mid']=r['owner_cash_after_sbc_mid']-r['trade_wc_cash']
  r['owner_cash_trade_wc_neutral_low']=r['fcf_ex_asset_sales']-r['trade_wc_cash']-(r['sbc_actual'] if r['sbc_actual'] is not None else r['revenue']*.011)
  r['owner_cash_trade_wc_neutral_high']=r['fcf_ex_asset_sales']-r['trade_wc_cash']-(r['sbc_actual'] if r['sbc_actual'] is not None else r['revenue']*.009)
  r['finance_lease_principal_actual']= {'FY2023':37,'FY2024':33,'FY2025':48}.get(label)
  r['finance_lease_principal_analyst_mid']=r['finance_lease_principal_actual'] if r['finance_lease_principal_actual'] is not None else (48 if label.startswith('TTM') else 36 if label.startswith('9M') else 24 if label.startswith('H1') else 12)
  r['owner_cash_after_sbc_and_finance_lease_mid']=r['owner_cash_after_sbc_mid']-r['finance_lease_principal_analyst_mid']
  r['owner_cash_wc_neutral_after_finance_lease_mid']=r['owner_cash_trade_wc_neutral_mid']-r['finance_lease_principal_analyst_mid']
  r['owner_cash_wc_neutral_fcff_proxy']=r['owner_cash_wc_neutral_after_finance_lease_mid']+(-r['interest_net_signed'])*.77
  r['normalized_fcff_before_growth_wc_with_actual_capex']=r['normalized_nopat_23pct']+r['da']-r['capex']-r['finance_lease_principal_analyst_mid']
  r['eps_gaap_reported']= {'FY2023':2.92,'FY2024':2.83,'FY2025':1.50,'Q4_2025':.70,'Q1_2026':.55,'Q2_2026':.64,'Q3_2026':.50}.get(label)
  r['net_reinvestment_cash']=r['capex']-r['da']-r['trade_wc_cash']
checks=[]
for l,r in rows.items():
 checks.append({'test':l+' operating identity','pass':abs(r['gross_profit']-r['sga']-r['sap']-r['charges']-r['ebit'])<.01})
 if r.get('cfo')!=None:
  # interim other operating contains deferred taxes; annual statement separates them.
  deferred={ 'FY2025':23,'FY2024':148,'FY2023':196 }.get(l,0)
  if l in ['Q4_2025','TTM_2026_09']:deferred=23
  if l=='TTM_2025_09':deferred=148
  checks.append({'test':l+' CFO identity','pass':abs(r['net_income']+r['da']+r['charges']+r['trade_wc_cash']+r['other_operating']+deferred-r['cfo'])<.01})
for k in ['revenue','ebit','cfo','capex','da','trade_wc_cash']:
 checks.append({'test':'four quarter '+k,'pass':abs(sum(rows[q][k] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])-rows['TTM_2026_09'][k])<.01})
(H/'history.json').write_text(json.dumps(rows,indent=2));(H/'source_rows.json').write_text(json.dumps(source_rows,indent=2));(H/'checks.json').write_text(json.dumps(checks,indent=2))
fields=['period']+sorted(set(k for r in rows.values() for k in r if k!='period'))
with (H/'history.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows.values())
print('checks',len(checks),'failed',[x for x in checks if not x['pass']],'sourced cells',len(source_rows))
for label in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','TTM_2025_09','TTM_2026_09']:
 print(label,{k:round(rows[label][k],2) for k in ['revenue','ebit','charges','sap','adjusted_ebit_ex_charges','cfo','capex','ppe_sales','trade_wc_cash','owner_cash_trade_wc_neutral_mid','normalized_ebit_pre_sap_after_0_5pct_recurring_reserve']})
assert all(x['pass'] for x in checks)

# Diagnostic sensitivity only: annual 2026 contractual finance-lease payments include interest.
lease_sensitivity={'basis':'Actual interim principal not separately disclosed. Last annual actual principal48 is an estimate for TTM; 2026 contractual gross finance-lease payments103 include interest. 103 treated entirely as principal is a conservative diagnostic stress, not observed principal or a limit on future new leases. DCF unchanged.', 'annual_2026_contractual_gross_payment_including_interest':103,'source_url':urls['hal-20251231.html'],'source_note':'Note7 leases, 2026 maturity row','periods':{}}
for period in ['TTM_2025_09','TTM_2026_09']:
 r=rows[period];lease_sensitivity['periods'][period]=[{'principal_assumption':x,'owner_cash_after_sbc_and_lease':r['owner_cash_after_sbc_mid']-x,'owner_cash_wc_neutral_after_lease':r['owner_cash_trade_wc_neutral_mid']-x} for x in [0,48,80,100,103]]
(H/'lease_principal_sensitivity.json').write_text(json.dumps(lease_sensitivity,indent=2))
