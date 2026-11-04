import json,pathlib,datetime,csv
P=pathlib.Path(__file__).resolve().parent;P.mkdir(exist_ok=True)
sources=json.load(open(P/'source_index.json'))
mapn={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','cogs':'CostOfGoodsAndServicesSold','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','eps_basic':'EarningsPerShareBasic','eps_diluted':'EarningsPerShareDiluted','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding','cfo':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','da':'DepreciationDepletionAndAmortization','acquired_amortization':'AmortizationOfIntangibleAssets','tax':'IncomeTaxExpenseBenefit','pretax_income':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','restructuring_line':'RestructuringExpenseBenefit','debt_gain_loss':'GainsLossesOnExtinguishmentOfDebt','interest_expense':'InterestExpenseNonoperating','legal_settlement':'LossContingencyLossInPeriod','acquisitions_cash':'PaymentsToAcquireBusinessesNetOfCashAcquired','divestiture_cash':'ProceedsFromDivestitureOfBusinesses','tax_paid':'IncomeTaxesPaidNet','depreciation':'Depreciation','inventory_provision':'InventoryWriteDown','warranty_issued':'StandardProductWarrantyAccrualWarrantiesIssued'}
raw=json.load(open(P/'source_numeric_extracts.json'))
index={(r['metric'],r['start'],r['end']):r for r in raw}
conflicts=json.load(open(P/'source_conflicts.json'))
for r in json.load(open(P/'additional_numeric_extracts.json')):
 index[(r['metric'],r['start'],r['end'])]=r
# quarter/fiscal date boundaries explicitly reported in source contexts
periods=[('FY2024','2023-07-01','2024-06-28'),('FY2025','2024-06-29','2025-06-27'),('FY2026','2025-06-28','2026-07-03'),('Q1FY2025','2024-06-29','2024-09-27'),('Q2FY2025','2024-09-28','2024-12-27'),('Q3FY2025','2024-12-28','2025-03-28'),('Q4FY2025','2025-03-29','2025-06-27'),('Q1FY2026','2025-06-28','2025-10-03'),('Q2FY2026','2025-10-04','2026-01-02'),('Q3FY2026','2026-01-03','2026-04-03'),('Q4FY2026','2026-04-04','2026-07-03'),('Q1FY2027','2026-07-04','2026-10-02')]
q4={'Q4FY2025':{'revenue':2444,'cogs':1530,'ebit':568,'net_income':488,'eps_basic':2.30,'eps_diluted':2.24,'diluted_shares':218,'tax':4,'pretax_income':492,'restructuring_line':13,'interest_expense':75,'debt_gain_loss':-3,'da':61,'sbc':59,'cfo':508,'capex':83},'Q4FY2026':{'revenue':3629,'cogs':1731,'ebit':1559,'net_income':1294,'eps_basic':5.75,'eps_diluted':5.58,'diluted_shares':232,'tax':211,'pretax_income':1505,'restructuring_line':4,'interest_expense':64,'debt_gain_loss':-10,'da':70,'sbc':54,'cfo':1305,'capex':187,'acquired_amortization':1}}
q4url='https://www.sec.gov/Archives/edgar/data/1137789/000113778926000153/stxq42026pressreleasefinan.htm'
manual=[];out=[]
for label,start,end in periods:
 row={'period':label,'start':start,'end':end,'weeks':((datetime.date.fromisoformat(end)-datetime.date.fromisoformat(start)).days+1)/7};prov={}
 for m in mapn:
  k=(m,start,end)
  if k in index:row[m]=index[k]['value'];prov[m]={'basis':'reported','sources':[index[k]]}
  elif label in q4 and m in q4[label]:
   row[m]=q4[label][m];r={'metric':m,'start':start,'end':end,'value':row[m],'url':q4url,'table':'Condensed operations / FCF / EBITDA reconciliation'};manual.append(r);prov[m]={'basis':'reported','sources':[r]}
  elif label.startswith('Q') and not m.startswith('eps') and m!='diluted_shares':
   ystart='2024-06-29' if '2025' in label else '2025-06-28' if '2026' in label else '2026-07-04';prev=(datetime.date.fromisoformat(start)-datetime.timedelta(days=1)).isoformat();a=index.get((m,ystart,end));b=index.get((m,ystart,prev))
   if a and b:row[m]=round(a['value']-b['value'],8);prov[m]={'basis':'derived_ytd_difference','sources':[a,b]}
  if m not in row:row[m]=None;prov[m]={'basis':'missing_required_source'}
 row['provenance']=prov
 if row['cfo'] is not None and row['capex'] is not None:row['fcf']=row['cfo']-row['capex'];row['fcf_after_sbc']=row['fcf']-row['sbc'] if row['sbc'] is not None else None
 row['ebit_margin_pct']=row['ebit']/row['revenue']*100;row['net_margin_pct']=row['net_income']/row['revenue']*100
 out.append(row)
for year in [2026,2027]:
 qs=[x for x in out if x['period'] in [f'Q2FY{year-1}',f'Q3FY{year-1}',f'Q4FY{year-1}',f'Q1FY{year}']];r={'period':f'TTM_Q1FY{year}','start':qs[0]['start'],'end':qs[-1]['end'],'weeks':sum(q['weeks'] for q in qs),'provenance':{}}
 for m in [*mapn,'fcf','fcf_after_sbc']:
  if m=='diluted_shares':r[m]=None;continue
  vals=[q.get(m) for q in qs];r[m]=round(sum(vals),8) if all(x is not None for x in vals) else None;r['provenance'][m]={'basis':'sum_reported_quarter_eps' if m.startswith('eps') else 'sum_four_quarters','periods':[q['period'] for q in qs]}
 r['ebit_margin_pct']=r['ebit']/r['revenue']*100;r['net_margin_pct']=r['net_income']/r['revenue']*100;out.append(r)
json.dump(out,open(P/'financial_history.json','w'),indent=2);json.dump(manual,open(P/'manual_release_extracts.json','w'),indent=2)
cols=[k for k in out[0] if k!='provenance']
with open(P/'financial_history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(out)
print('conflicts',len(conflicts))
for r in out:print({k:r.get(k) for k in ['period','weeks','revenue','ebit','net_income','eps_diluted','cfo','capex','sbc','da','tax','fcf']})
