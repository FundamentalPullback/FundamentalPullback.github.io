from pathlib import Path
import json
P=Path(__file__).parent
source=json.load(open(P/'sourcefacts.json'))
facts=source['facts']
urls=source['sources']
# Prefer latest comparative; exact dates + dimension match only.
def fact(tag,start,end,dimensions=None):
 a=[x for x in facts if x['tag']==tag and x.get('startdate')==start and x.get('enddate')==end and x['dimensions']==(dimensions or {})]
 if not a:return None
 order=['q3','q2','q1','fy25','q3prior','fy24'];a.sort(key=lambda x:order.index(x['filing']))
 return a[0]['value']/ (1 if tag.endswith('EarningsPerShareDiluted') else 1e6)
tags={'revenue':'us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax','EBIT':'us-gaap:OperatingIncomeLoss','parent_NI':'us-gaap:NetIncomeLoss','EPS_diluted':'us-gaap:EarningsPerShareDiluted','CFO':'us-gaap:NetCashProvidedByUsedInOperatingActivities','DA':'us-gaap:DepreciationAmortizationAndAccretionNet','SBC_total':'us-gaap:ShareBasedCompensation','SBC_equity_recognition_only':'us-gaap:AdjustmentsToAdditionalPaidInCapitalSharebasedCompensationRequisiteServicePeriodRecognitionValue'}
axis='srt:ConsolidatedEntitiesAxis';members={'exVIE':'srt:ConsolidatedEntityExcludingVariableInterestEntitiesVIEMember','DGD':'vlo:VariableInterestEntityPrimaryBeneficiaryDiamondGreenDieselHoldingsLLCMember','otherVIE':'vlo:OtherVariableInterestEntitiesMember'}
# Read actual other VIE member from filings.
for f in facts:
 if f['tag']=='us-gaap:PaymentsToAcquirePropertyPlantAndEquipment' and axis in f['dimensions']:
  m=f['dimensions'][axis]
  if m not in [members['exVIE'],members['DGD']]:members['otherVIE']=m
rows={}
for label,s,e in [('FY2023','2023-01-01','2023-12-31'),('FY2024','2024-01-01','2024-12-31'),('FY2025','2025-01-01','2025-12-31'),('9M2024','2024-01-01','2024-09-30'),('9M2025','2025-01-01','2025-09-30'),('9M2026','2026-01-01','2026-09-30'),('6M2026','2026-01-01','2026-06-30'),('Q1_2026','2026-01-01','2026-03-31')]:
 d={k:fact(t,s,e) for k,t in tags.items()}
 for key,m in members.items():
  d['capex_'+key]=fact('us-gaap:PaymentsToAcquirePropertyPlantAndEquipment',s,e,{axis:m})
  if key!='otherVIE':d['turnaround_catalyst_'+key]=fact('us-gaap:PaymentsForCapitalImprovements',s,e,{axis:m})
 d['JV_investments']=fact('us-gaap:PaymentsToAcquireInterestInJointVenture',s,e) or 0
 cs=['capex_exVIE','capex_DGD','capex_otherVIE'];d['capex_gross']=sum(d[x] for x in cs) if all(d[x] is not None for x in cs) else None
 ks=cs+['turnaround_catalyst_exVIE','turnaround_catalyst_DGD','JV_investments'];d['capital_investments_gross']=sum(d[x] for x in ks) if all(d[x] is not None for x in ks) else None
 d['capital_investments_attributable_calculated']=None if d['capital_investments_gross'] is None else d['capital_investments_gross']-.5*(d['capex_DGD']+d['turnaround_catalyst_DGD'])-d['capex_otherVIE']
 rows[label]=d
for lab,a,b in [('Q4_2025','FY2025','9M2025'),('Q2_2026','6M2026','Q1_2026'),('Q3_2026','9M2026','6M2026')]:
 rows[lab]={k:None if rows[a][k] is None or rows[b][k] is None else round(rows[a][k]-rows[b][k],4) for k in rows[a]}
 # EPS should not be subtracted when actual quarter exists; DA uses total income statement components.
 s,e={'Q4_2025':('2025-10-01','2025-12-31'),'Q2_2026':('2026-04-01','2026-06-30'),'Q3_2026':('2026-07-01','2026-09-30')}[lab]
 for k in ['revenue','EBIT','parent_NI','EPS_diluted']:
  v=fact(tags[k],s,e)
  if v is not None:rows[lab][k]=v
for lab,a,b,c in [('TTM_2026Q3','FY2025','9M2026','9M2025'),('prior_TTM_2025Q3','FY2024','9M2025','9M2024')]:
 rows[lab]={k:None if any(rows[x][k] is None for x in [a,b,c]) else round(rows[a][k]+rows[b][k]-rows[c][k],4) for k in rows[a]}
# TTM EPS = actual last four reported quarterly EPS, explicitly not annual-minus-YTD weighted EPS.
rows['Q4_2025']['EPS_diluted']=source['supplemental_reported_quarterly_EPS']['Q4_2025'] # SEC earnings release 2026-01-29, accession 000162828026003974
rows['TTM_2026Q3']['EPS_diluted']=round(sum(rows[q]['EPS_diluted'] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026']),2)
rows['prior_TTM_2025Q3']['EPS_diluted']=round(source['supplemental_reported_quarterly_EPS']['Q4_2024']+sum(fact(tags['EPS_diluted'],s,e) for s,e in [('2025-01-01','2025-03-31'),('2025-04-01','2025-06-30'),('2025-07-01','2025-09-30')]),2)
json.dump({'units':'USD millions except EPS USD/share','sources':urls,'rows':rows,'notes':['GAAP reported EBIT retains SBC expense. Full quarterly SBC not separately disclosed; null is intentional. Equity recognition is not full SBC expense.','Q4 flow fields are FY minus 9M. Q2 and Q3 cash-flow fields are YTD differences. Q4 2025 EPS3.73 and Q4 2024 EPS0.88 from SEC earnings release https://www.sec.gov/Archives/edgar/data/1035002/000162828026003974/a12312025exh9901earningsre.htm; TTM EPS is sum of four reported quarters, not annual-minus-YTD EPS.','Calculated attributable investment can differ 0.5m from reported due to rounded DGD half-share.','Gross capital investments include deferred turnaround/catalyst costs and nonconsolidated JV investments. Do not subtract only PP&E capex.']},open(P/'financial_history.json','w'),indent=2)
print(json.dumps(rows,indent=2))
