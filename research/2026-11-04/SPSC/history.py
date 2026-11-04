import json,pathlib,csv
P=pathlib.Path(__file__).parent
F=json.loads((P/'inputs/xbrl_subset.json').read_text())['facts']['us-gaap']
T={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','cfo':'NetCashProvidedByUsedInOperatingActivities','ppe_capex':'PaymentsToAcquirePropertyPlantAndEquipment','ppe_da':'DepreciationDepletionAndAmortization','acquired_amort':'AmortizationOfIntangibleAssets','sbc':'ShareBasedCompensation','acquisition_cash':'PaymentsToAcquireBusinessesNetOfCashAcquired','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding','eps':'EarningsPerShareDiluted'}
provenance={}
def get(k,start,end):
 vals=[x for x in next(iter(F[T[k]]['units'].values())) if x.get('start')==start and x['end']==end and x['filed']<='2026-11-04']
 if not vals: return None
 v=sorted(vals,key=lambda x:x['filed'])[-1];provenance[f'{k}:{start}:{end}']=v
 return v['val']/(1 if k=='eps' else 1e6)
def per(label,start,end):
 d={'period':label}
 for k in T:d[k]=get(k,start,end)
 return d
annual=[per(str(y),f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]]
ytd={f'{y}Q{q}':per(f'{y}Q{q}',f'{y}-01-01',f'{y}-{m}') for y in [2024,2025,2026] for q,m in [(1,'03-31'),(2,'06-30'),(3,'09-30')]}
qs=[]
for y,q in [(2025,4),(2026,1),(2026,2),(2026,3)]:
 d={'period':f'{y}Q{q}'}
 for k in T:
  if q==4:
   a=annual[-1][k];b=ytd[f'{y}Q3'][k]
   if k in ['diluted_shares','eps']:d[k]=get(k,f'{y}-10-01',f'{y}-12-31')
   else:d[k]=a-b if a is not None and b is not None else None
  elif q==1:d[k]=ytd[f'{y}Q1'][k]
  elif k in ['diluted_shares','eps','revenue','ebit','net_income','acquired_amort']:
   d[k]=get(k,f'{y}-'+('04-01' if q==2 else '07-01'),f'{y}-'+('06-30' if q==2 else '09-30'))
  else:
   a=ytd[f'{y}Q{q}'][k];b=ytd[f'{y}Q{q-1}'][k];d[k]=a-b if a is not None and b is not None else None
 qs.append(d)
# Exact Q4 values from issuer February 12, 2026 earnings release, not inferred averages.
qs[0]['diluted_shares']=37.763
qs[0]['eps']=0.68
provenance['Q42025_share_and_eps']={'source':'https://investors.spscommerce.com/news-releases/news-release-details/sps-commerce-reports-fourth-quarter-and-fiscal-year-2025','diluted_shares_m':37.763,'eps':0.68}
ttms=[]
for year,ann in [(2025,annual[1]),(2026,annual[2])]:
 d={'period':f'TTM September {year}'}
 for k in T:
  if k=='diluted_shares':d[k]=None;continue
  a,b,c=ann[k],ytd[f'{year}Q3'][k],ytd[f'{year-1}Q3'][k];d[k]=a+b-c if None not in [a,b,c] else None
 ttms.append(d)
rows=annual+qs+ttms
for d in rows:
 d['fcf_cash']=d['cfo']-d['ppe_capex'];d['fcf_after_sbc_diagnostic']=d['fcf_cash']-d['sbc'];d['ebit_ex_sale_loss']=d['ebit']+(23.454 if d['period'] in ['2026Q2','TTM September 2026'] else 0)
 d['ebita_after_sbc_ex_sale_loss']=d['ebit_ex_sale_loss']+d['acquired_amort'];d['ebit_margin']=d['ebit']/d['revenue'];d['ebit_norm_margin']=d['ebit_ex_sale_loss']/d['revenue']
(P/'history.json').write_text(json.dumps(rows,indent=2));(P/'history_provenance.json').write_text(json.dumps(provenance,indent=2))
with (P/'history.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))
