from pathlib import Path
import json,csv,re,hashlib,datetime
B=Path(__file__).parent
S=json.loads((B/'sources.json').read_text())
raw={k:json.loads((B/'raw'/f'{k}_tables.json').read_text()) for k in S}
rows=[]; data={};prov={}; checks=[];flags=[]
ends={'FY2024':'2024-03-30','FY2025':'2025-03-29','FY2026':'2026-03-28','H1FY2025':'2024-09-28','H1FY2026':'2025-09-27','H1FY2027':'2026-09-26','9MFY2025':'2024-12-28','9MFY2026':'2025-12-27','Q1FY2026':'2025-06-28','Q1FY2027':'2026-06-27','Q2FY2026':'2025-09-27','Q2FY2027':'2026-09-26','Q3FY2026':'2025-12-27','Q4FY2026':'2026-03-28','TTM2025':'2025-09-27','TTM2026':'2026-09-26'}
starts={'FY2024':'2023-04-02','FY2025':'2024-03-31','FY2026':'2025-03-30','H1FY2025':'2024-03-31','H1FY2026':'2025-03-30','H1FY2027':'2026-03-29','9MFY2025':'2024-03-31','9MFY2026':'2025-03-30','Q1FY2026':'2025-03-30','Q1FY2027':'2026-03-29','Q2FY2026':'2025-06-29','Q2FY2027':'2026-06-28','Q3FY2026':'2025-09-28','Q4FY2026':'2025-12-28','TTM2025':'2024-09-29','TTM2026':'2025-09-28'}
def nval(c):
 c=c.strip().replace('$','').replace(',','').replace(' ','')
 if c in ['—','–','-']:return 0.
 if re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',c):return float(c.strip('()'))*(-1 if c.startswith('(') else 1)
 return None
def get(source,tab,label,occ=0):
 rr=[r for r in raw[source][tab]['rows'] if r and r[0]==label]
 if len(rr)<=occ:raise KeyError((source,tab,label,occ))
 row=rr[occ];return [v for c in row[1:] if (v:=nval(c)) is not None]
def put(p,m,v,sid,loc,evidence='fact_source_reported',note='',unit='USD million'):
 v=None if v is None else round(v,6)
 data.setdefault(p,{})[m]=v
 pr={'period':p,'period_start':starts.get(p),'period_end':ends.get(p),'metric':m,'value':v,'unit':unit,'currency':'USD','source_id':sid,'source_location':loc,'evidence_label':evidence,'note':note}
 rows.append(pr);prov[(p,m)]=pr

def extract(p,source,tab,col,m,label,occ=0,scale=1000,sign=1,note=''):
 vs=get(source,tab,label,occ);put(p,m,vs[col]/scale*sign,source,f'table {tab}; {label}; occurrence {occ}; column {col}',note=note,unit='USD/share' if scale==1 and m.startswith('eps') else 'million shares' if m.startswith('shares') else 'USD million')
ISMAP={'revenue':'Revenues','cogs':'Cost of goods sold','sga':'Selling, general and administrative expenses','impairment_operating':'Impairment of goodwill and intangible assets','interest_income':'Interest income','interest_expense':'Interest expense','other_nonoperating':'Other income (expense), net','income_tax_expense':'Income tax expense'}
def income(p,s,t,c):
 available={r[0] for r in raw[s][t]['rows'] if r}
 for m,l in ISMAP.items():
  if l not in available:
   if m=='impairment_operating':put(p,m,0,s,f'table {t}; no separate impairment row',note='No impairment in statement; zero for reported bridge.');continue
   if m=='income_tax_expense':l='Income tax benefit'
  extract(p,s,t,c,m,l,sign=-1 if m=='interest_expense' else 1)
 for m,labels in {'ebit':['Operating income (loss)','Operating income','Operating loss'],'pretax_cont':['Income (loss) from continuing operations before income taxes','Income from continuing operations before income taxes','Income before income taxes','Loss before income taxes'],'net_income_cont':['Income (loss) from continuing operations','Income from continuing operations','Net income','Net loss'],'net_income_total':['Net income (loss)','Net income','Net loss'],'net_income_discontinued':['Income (loss) from discontinued operations, net of tax','Loss from discontinued operations, net of tax']}.items():
  chosen=next((l for l in labels if l in available),None)
  if chosen:extract(p,s,t,c,m,chosen)
  else:put(p,m,0,s,f'table {t}; no discontinued operation',note='No discontinued operation in period.')
 for m,label in [('shares_basic','Basic'),('shares_diluted','Diluted')]:
  count=sum(r and r[0]==label for r in raw[s][t]['rows']);extract(p,s,t,c,m,label,occ=count-1)
 if 'Continuing operations' in available:
  extract(p,s,t,c,'eps_cont_basic','Continuing operations',occ=0,scale=1)
  extract(p,s,t,c,'eps_cont_diluted','Continuing operations',occ=1,scale=1)
  extract(p,s,t,c,'eps_total_diluted','Total earnings (loss) per common share - diluted',scale=1)
 else:
  extract(p,s,t,c,'eps_cont_basic','Basic',occ=0,scale=1)
  extract(p,s,t,c,'eps_cont_diluted','Diluted',occ=0,scale=1)
  extract(p,s,t,c,'eps_total_diluted','Diluted',occ=0,scale=1)
 put(p,'gross_profit',data[p]['revenue']-data[p]['cogs'],s,f'table {t}; revenue minus COGS','derived_calculation')
CFMAP={
'cf_impairment':'Impairment of goodwill and intangible assets',
'cf_rou_reduction':'Reduction in the carrying amount of right-of-use assets',
'sbc':'Stock-based compensation','cf_bad_debt':'Provision for doubtful accounts',
'cf_pension_asset_reversion':'Pension termination asset reversion, net',
'cf_deferred_tax':'Deferred income taxes','cf_tax_receivable_writeoff':'Write-off of income tax receivables and interest',
'cf_gain_sale_reversal':'Gain on sale of business','cf_other':'Other, net',
'wc_ar':'Accounts receivable','wc_inventory':'Inventories','wc_ap':'Accounts payable','wc_tax':'Income taxes',
'wc_accrued':'Accrued liabilities','cf_lease_cash_change':'Operating lease right-of-use assets and liabilities','wc_other':'Other assets and liabilities',
'capex_ppe':'Capital expenditures','capex_software':'Software purchases',
'investing_sale_proceeds':'Proceeds from sale of businesses, net of cash sold','investing_sale_wc_payment':'Payment for working capital adjustment for sale of business','investing_asset_sale_proceeds':'Proceeds from sale of assets'}
def cash(p,s,t,c):
 avail={r[0] for r in raw[s][t]['rows'] if r}
 for m,l in CFMAP.items():
  if l in avail:extract(p,s,t,c,m,l,sign=-1 if m in ['capex_ppe','capex_software','investing_sale_wc_payment'] else 1)
  elif m in ['cf_deferred_tax']:put(p,m,None,s,f'table {t}; not disaggregated',evidence='missing_required_source',note='Interim deferred tax included within other adjustments; do not read missing as zero.')
  else:put(p,m,0,s,f'table {t}; no separate row',note='Zero for presentation bridge only where absent; cf_other may include additional components.')
 for m,labels in {'da_and_other_asset_writedowns':['Depreciation, amortization and other asset write-downs','Depreciation and amortization'],'cf_pension':['Pension expense in excess of (less than) contributions','Pension expense less than contributions'],'cfo_cont':['Cash provided by operating activities - continuing operations','Cash used by operating activities - continuing operations','Cash provided by operating activities','Cash used by operating activities'],'cfo_total':['Cash provided by operating activities','Cash used by operating activities'],'cfo_discontinued':['Cash provided by operating activities - discontinued operations'],'investing_discontinued':['Cash used by investing activities - discontinued operations']}.items():
  chosen=next((l for l in labels if l in avail),None)
  if chosen:extract(p,s,t,c,m,chosen,note='FY annual row includes other asset write-downs; interim label is depreciation and amortization. Not a pure D&A comparable series.' if m=='da_and_other_asset_writedowns' else '')
  else:put(p,m,0,s,f'table {t}; no separate discontinued row')
 # harmonized other including deferred tax for annual-v-interim rollforwards
 put(p,'cf_other_including_deferred_tax',data[p]['cf_other']+(data[p]['cf_deferred_tax'] or 0),s,f'table {t}; other + separately disclosed deferred tax','derived_calculation',note='Interim deferred tax is not separately disclosed and is already in other.')
 for m in ['cash_taxes_paid','cash_interest_paid']:
  put(p,m,None,s,'No interim cash tax/interest disaggregation found',evidence='missing_required_source',note='Do not infer cash tax/interest from income statement expense or change in tax working capital.')
for c,p in enumerate(['FY2026','FY2025','FY2024']):
 income(p,'FY2026_10K',98,c);cash(p,'FY2026_10K',100,c)
 extract(p,'FY2026_10K',177,c,'cash_taxes_paid','Income taxes paid, net of refunds (a)',note='Note26 footnote(a): includes BOTH continuing and discontinued operations; not a retained cash-tax series.')
 extract(p,'FY2026_10K',177,c,'cash_interest_paid','Interest paid, net of amounts capitalized')
 extract(p,'FY2026_10K',177,c,'capex_ppe_accrued_unpaid','Property, plant and equipment expenditures included in accounts payable or accrued liabilities')
 extract(p,'FY2026_10K',177,c,'capex_software_accrued_unpaid','Computer software costs included in accounts payable or accrued liabilities')
for p,s,c in [('Q2FY2027','Q2FY2027_10Q',0),('Q2FY2026','Q2FY2027_10Q',1),('H1FY2027','Q2FY2027_10Q',2),('H1FY2026','Q2FY2027_10Q',3),('Q1FY2027','Q1FY2027_10Q',0),('Q1FY2026','Q1FY2027_10Q',1),('Q3FY2026','Q3FY2026_10Q',0),('9MFY2026','Q3FY2026_10Q',2),('9MFY2025','Q3FY2026_10Q',3),('H1FY2025','Q2FY2026_10Q',3)]:income(p,s,6,c)
for p,s,c in [('H1FY2027','Q2FY2027_10Q',0),('H1FY2026','Q2FY2027_10Q',1),('Q1FY2027','Q1FY2027_10Q',0),('Q1FY2026','Q1FY2027_10Q',1),('9MFY2026','Q3FY2026_10Q',0),('9MFY2025','Q3FY2026_10Q',1),('H1FY2025','Q2FY2026_10Q',1)]:cash(p,s,8,c)
CFmetrics=set(data['H1FY2027'])-set(data['Q2FY2027'])
CFmetrics-= {'cf_deferred_tax','cf_other'}
ISmetrics=set(data['Q3FY2026'])
ISmetrics-= {m for m in ISmetrics if m.startswith(('eps','shares'))}
def derive(p,terms,metrics):
 for m in sorted(metrics):
  if all(data.get(x,{}).get(m) is not None for x,_ in terms):
   v=sum(data[x][m]*s for x,s in terms)
   put(p,m,v,';'.join(sorted({q for x,_ in terms for q in prov[(x,m)]['source_id'].split(';')})),'; '.join(f'{s:+}*{x}.{m}' for x,s in terms),'derived_calculation',note='Mechanical cumulative-period difference or trailing 52-week bridge; not seasonally annualized.')
  else:put(p,m,None,';'.join(sorted({prov[(x,m)]['source_id'] for x,_ in terms if (x,m) in prov})),'; '.join(f'{s:+}*{x}.{m}' for x,s in terms),'missing_required_source',note='One or more required components not disclosed.')
derive('Q3FY2026',[('9MFY2026',1),('H1FY2026',-1)],CFmetrics)
derive('Q4FY2026',[('FY2026',1),('9MFY2026',-1)],ISmetrics|CFmetrics)
derive('Q2FY2027',[('H1FY2027',1),('Q1FY2027',-1)],CFmetrics)
derive('Q2FY2026',[('H1FY2026',1),('Q1FY2026',-1)],CFmetrics)
put('Q4FY2026','eps_cont_diluted',-.30,'FY2026_RELEASE','table 0; Three Months Ended March 2026; diluted loss per share from continuing operations',unit='USD/share')
put('Q4FY2026','eps_total_diluted',-.30,'FY2026_RELEASE','No discontinued results; diluted continuing EPS',unit='USD/share')
for p,terms in [('TTM2026',[('FY2026',1),('H1FY2027',1),('H1FY2026',-1)]),('TTM2025',[('FY2025',1),('H1FY2026',1),('H1FY2025',-1)])]:derive(p,terms,ISmetrics|CFmetrics)
for p,d in list(data.items()):
 if d.get('cfo_cont') is not None and d.get('capex_ppe') is not None:
  for m,v,formula in [('capex_all',d['capex_ppe']+d['capex_software'],'PPE + software'),('fcf_reported_cont',d['cfo_cont']-d['capex_ppe']-d['capex_software'],'CFO_cont − PPE − software'),('fcf_less_sbc',d['cfo_cont']-d['capex_ppe']-d['capex_software']-d['sbc'],'FCF_reported_cont − SBC'),('cash_trade_wc',d['wc_ar']+d['wc_inventory']+d['wc_ap'],'cash-flow changes in AR + inventory + AP'),('cash_all_wc_exleases',sum(d[x] for x in ['wc_ar','wc_inventory','wc_ap','wc_tax','wc_accrued','wc_other']),'cash-flow changes in AR + inventory + AP + tax + accrued + other')]:put(p,m,v,prov[(p,'cfo_cont')]['source_id'],formula,'derived_calculation')
# Unique final long-form rows, keep superseded staging in separate artifact
with (B/'extraction_staging_including_superseded.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
finalrows=[prov[k] for k in sorted(prov)]
with (B/'Normalized_Financials_Long.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(finalrows[0]));w.writeheader();w.writerows(finalrows)
for name,periods in [('annual_history',['FY2024','FY2025','FY2026']),('quarter_history',['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']),('ttm_history',['TTM2025','TTM2026']),('all_periods_history',list(data))]:
 metrics=sorted(set().union(*(data[x] for x in periods)))
 with (B/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=['period','period_start','period_end']+metrics);w.writeheader();w.writerows([{'period':p,'period_start':starts[p],'period_end':ends[p],**data[p]} for p in periods])
# validations
for p,d in data.items():
 for name,value in [('income_identity',d.get('net_income_total',0)-d.get('net_income_cont',0)-d.get('net_income_discontinued',0)),('ebit_identity',d['gross_profit']-d['sga']-d['impairment_operating']-d['ebit']),('pretax_identity',d['ebit']+d['interest_income']-d['interest_expense']+d['other_nonoperating']-d['pretax_cont']),('net_income_identity',d['pretax_cont']-d['income_tax_expense']-d['net_income_cont'])]:
  checks.append({'period':p,'check':name,'difference':round(value,6),'pass':abs(value)<.0011})
 if 'cfo_cont' in d:
  fields=['net_income_cont','cf_impairment','da_and_other_asset_writedowns','cf_rou_reduction','sbc','cf_bad_debt','cf_pension','cf_pension_asset_reversion','cf_tax_receivable_writeoff','cf_gain_sale_reversal','cf_other_including_deferred_tax','wc_ar','wc_inventory','wc_ap','wc_tax','wc_accrued','cf_lease_cash_change','wc_other']
  val=sum(d.get(x,0) or 0 for x in fields)-d['cfo_cont'];checks.append({'period':p,'check':'cashflow_operating_identity','difference':round(val,6),'pass':abs(val)<.0011})
for m in sorted(CFmetrics|ISmetrics):
 if all(data[p].get(m) is not None for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027','TTM2026']):
  val=sum(data[p][m] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-data['TTM2026'][m];checks.append({'period':'TTM2026','check':'four_quarter_tie_'+m,'difference':round(val,6),'pass':abs(val)<.0011})
(B/'Validation_Checks.json').write_text(json.dumps(checks,indent=2))
(B/'history.json').write_text(json.dumps({'as_of':'2026-11-04','units':'USD million except per-share and million-share rows','perimeter':'GAAP continuing excludes Supreme; includes Dickies through November 12 2025. Cash not same retained perimeter.','periods':{p:{'start':starts[p],'end':ends[p],**d} for p,d in data.items()}},indent=2))
index=[{'source_id':k,'url':u,'local_html':f'raw/{k}.html','local_tables':f'raw/{k}_tables.json','retrieved_at':'2026-11-04','sha256':hashlib.sha256((B/'raw'/f'{k}.html').read_bytes()).hexdigest(),'owner':'V.F. Corporation','status':'audited' if '10K' in k else 'unaudited'} for k,u in S.items()]
(B/'Source_Index.json').write_text(json.dumps(index,indent=2))
print(json.dumps({'periods':len(data),'final_rows':len(finalrows),'checks':len(checks),'failed_checks':[x for x in checks if not x['pass']],'ttm_current':data['TTM2026'],'ttm_prior':data['TTM2025']},indent=2))
