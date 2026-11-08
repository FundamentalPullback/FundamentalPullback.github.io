"""Public-source financial history and conditional common-equity residual-income model.
Not an approved fair value: clean-surplus economics, project waterfalls and dilution unresolved.
Run python model.py from any directory. USD millions, except shares millions/per share.
"""
from pathlib import Path
import json,re,csv
D=Path(__file__).parent
selected=json.loads((D/'financial_inputs.json').read_text())
source_rows={}
def get(file,key,n,occ=0):
 token=f'{file}:{key}:{n}:{occ}';line=selected[token];source_rows[token]=line
 vals=[]
 for c in line.split('|')[1:]:
  c=c.strip()
  if re.fullmatch(r'\(?-?\d[\d,]*(?:\.\d+)?\)?',c): vals.append(float(c.replace(',','').replace('(','-').replace(')','')))
 assert len(vals)==n
 return vals
spec={'revenue':'Total revenue |','net_income_common':'Net income (loss) attributable to controlling stockholders |','interest_expense':'Interest expense |','gain_on_sale':'Gain on sale of assets |'}
data={}
for period,idx in [('FY2025',0),('FY2024',1),('FY2023',2)]:
 data[period]={k:get('fy2025',s,3)[idx]/1000 for k,s in spec.items()}
 data[period]['interest_expense']=abs(data[period]['interest_expense'])
 data[period]['CFO']=get('fy2025','Net cash provided by operating activities |',3)[idx]/1000
 data[period]['CFI']=get('fy2025','Net cash provided by (used in) investing activities |',3)[idx]/1000
 data[period]['CFF']=get('fy2025','Net cash provided by (used in) financing activities |',3)[idx]/1000
 data[period]['adjusted_earnings']=get('fy2025','Adjusted Earnings |',6)[idx*2]/1000
 data[period]['adjusted_EPS_reported']=get('fy2025','Adjusted Earnings |',6)[idx*2+1]
 data[period]['diluted_EPS_reported']=get('fy2025','Diluted earnings (loss) per common share |',3)[idx]
 data[period]['SBC']=get('fy2025','Equity-based expenses |',3)[idx]/1000
for period,file,idx in [('9M2026','q3_2026',2),('9M2025','q3_2026',3),('9M2024','q3_2025',3),('Q3_2026','q3_2026',0),('Q2_2026','q2_2026',0),('Q1_2026','q1_2026',0)]:
 n=2 if 'q1' in file else 4
 data[period]={k:get(file,s,n)[idx]/1000 for k,s in spec.items()}
 data[period]['diluted_EPS_reported']=get(file,'Diluted earnings (loss) per common share |',n)[idx]
 data[period]['adjusted_earnings']=get(file,'Adjusted Earnings |',n*2)[idx*2]/1000
 data[period]['adjusted_EPS_reported']=get(file,'Adjusted Earnings |',n*2)[idx*2+1]
 if period.startswith('9M') or period=='Q1_2026':
  ci=0 if idx in [0,2] else 1
  for k,s in [('CFO','Net cash provided by (used in) operating activities |'),('CFI','Net cash provided by (used in) investing activities |'),('CFF','Net cash provided by (used in) financing activities |'),('SBC','Equity-based expenses |')]:data[period][k]=get(file,s,2)[ci]/1000
for k,s in [('CFO','Net cash provided by (used in) operating activities |'),('CFI','Net cash provided by (used in) investing activities |'),('CFF','Net cash provided by (used in) financing activities |'),('SBC','Equity-based expenses |')]:
 six=get('q2_2026',s,2)[0]/1000
 data['Q2_2026'][k]=six-data['Q1_2026'][k]
 data['Q3_2026'][k]=data['9M2026'][k]-six
for p,fy,a,b in [('Q4_2025','FY2025',None,'9M2025'),('TTM2026-09-30','FY2025','9M2026','9M2025'),('TTM2025-09-30','FY2024','9M2025','9M2024')]:
 data[p]={k:data[fy][k]+(data[a][k] if a else 0)-data[b][k] for k in ['revenue','net_income_common','interest_expense','gain_on_sale','CFO','CFI','CFF','adjusted_earnings','SBC']}
 # EPS from differing diluted weighted shares must not be differenced as a substitute for GAAP TTM EPS.
 data[p]['diluted_EPS_reported']=None;data[p]['adjusted_EPS_reported']=None
data['Q4_2025']['diluted_EPS_reported']=get('release_q4_2025','GAAP Diluted earnings (loss) per share |',4)[0]
data['Q4_2025']['adjusted_EPS_reported']=get('release_q4_2025','Adjusted earnings per share |',4)[0]
for p in data:
 for k,v in data[p].items():
  if isinstance(v,float):data[p][k]=round(v,6)
(D/'history.json').write_text(json.dumps(data,indent=2))
with (D/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(data['FY2025']));w.writeheader()
 for p,v in data.items():w.writerow({'period':p,**v})
(D/'source_rows.json').write_text(json.dumps(source_rows,indent=2,ensure_ascii=False))
book=2735.947-113.173;shares=128.485212;price=38.90
capital={'date':'2026-09-30','assets':9631.123,'liabilities':6895.176,'total_equity':2735.947,'reported_NCI_excluded':113.173,'common_book':book,'cash':102.287,'debt_carrying':6455.826,'nonrecourse_carrying':112.433,'junior_subordinated_principal':1100,'junior_subordinated_carrying':1114.644,'convertible_principal':403,'convertible_carrying':401.010,'common_shares_2026_11_03':shares,'Q3_GAAP_diluted_shares':143.576560,'Q3_adjusted_shares':132.058694,'convertible_shares':14.9,'capped_call_shares':14.8,'capped_call_initial_strike':27.14,'capped_call_initial_cap':43.42,'loan_funding_commitments':242,'jupiter_guarantee_max':53,'jupiter_guarantee_annual_cap':20,'JV_guarantee_max':104,'JV_partner_reimbursement_fraction':.15,'liquidity':1981,'unfunded_co_invest_closed_transactions':300,'common_market_cap':shares*price,'common_book_per_share':book/shares,'price_to_book':price/(book/shares),'debt_to_common_book':6455.826/book}
# After-financing common equity model. Already net of debt/minorities in book and ROE.
# No EV bridge, no second debt subtraction, no adding AUM, securitized assets or unused lines.
def ri(roe,ke,growth,terminal_roe,g,haircut=0,share_dilution=0):
 b=book*(1-haircut);b0=b;pv_ri=0;pv_dist=0;forecast=[]
 for t in range(1,6):
  earnings=b*roe;reinvestment=b*growth;distribution=earnings-reinvestment;residual=earnings-b*ke
  forecast.append({'year':t,'opening_book':b,'earnings':earnings,'required_equity_retention':reinvestment,'potential_distribution':distribution,'residual_income':residual})
  pv_ri+=residual/(1+ke)**t;pv_dist+=distribution/(1+ke)**t;b+=reinvestment
 terminal_ri=b*(terminal_roe-ke)/(ke-g);terminal_fcfe=b*(terminal_roe-g)/(ke-g)
 v=b0+pv_ri+terminal_ri/(1+ke)**5
 v2=pv_dist+terminal_fcfe/(1+ke)**5
 assert abs(v-v2)<1e-7
 return {'conditional_value_per_share':v/(shares*(1+share_dilution)),'common_equity_value':v,'terminal_value_fraction_fcfe':terminal_fcfe/(1+ke)**5/v2,'forecast':forecast,'assumptions':{'roe':roe,'ke':ke,'book_growth':growth,'terminal_roe':terminal_roe,'terminal_growth':g,'initial_book_haircut':haircut,'share_dilution':share_dilution},'RI_FCFE_tieout':v-v2}
scenarios={'stress':ri(.10,.14,.02,.09,.015,.10,.04),'central_conditional':ri(.135,.12,.05,.115,.025),'favorable_conditional':ri(.17,.105,.08,.14,.03)}
sensitivity=[{'ke':ke,'terminal_roe':tr,'value':ri(.135,ke,.05,tr,.025)['conditional_value_per_share']} for ke in [.105,.12,.14] for tr in [.10,.115,.14]]
# Market reverse, single-stage only; not a claim that the market has this exact forecast.
implied_roe=.025+capital['price_to_book']*(.12-.025)
result={'ticker':'HASI','as_of':'2026-11-08','close':{'price':price,'date':'2026-11-06','type':'regular-close'},'method':'Conditional common-equity residual income; equivalent clean-surplus FCFE','valuation_status':'not_certified','decision':'wait_for_proof','entry_approved':False,'current_fair_value':None,'capital':capital,'risk_free':{'rate':.0486,'date':'2026-11-06','source':'US Treasury 10Y nominal par'},'ke_basis':{'base':.12,'base_type':'analyst judgment sensitivity; not empirically calibrated project premium','observed_beta':1.38,'beta_method':'Yahoo Finance 5-year monthly; corroborated StockAnalysis 5Y; retrieved 2026-11-08; underlying regression not independently reproduced','beta_sources':['https://finance.yahoo.com/quote/HASI/','https://stockanalysis.com/stocks/hasi/statistics/'],'ERP':.0441,'ERP_date':'2026-11-01','ERP_method':'Damodaran implied ERP, trailing 12-month adjusted payout','ERP_underlying_RF':.0529,'ERP_source':'https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','november_1_matched_market_inputs_Ke':.0529+1.38*.0441,'november_6_RF_with_monthly_ERP_Ke':.0486+1.38*.0441,'time_alignment_note':'Monthly ERP was solved using 5.29% RF, not November 6 4.86%. Matched RF/ERP snapshot and mixed-date latest-RF sensitivity are separate. No fresh November 6 implied ERP calculation is claimed. Beta is a retrieved historical estimator, not an exact November 1 frozen observation.','judgment_wedge_vs_matched_snapshot':.12-(.0529+1.38*.0441),'judgment_wedge_vs_latest_RF_sensitivity':.12-(.0486+1.38*.0441),'risk_note':'12% is a hurdle sensitivity above public CAPM references, not a measured separate project/country premium. Project losses and ROE stresses must not be interpreted as statistically independent of this hurdle.','country_premium':0,'country_note':'USD/US baseline without separate country add-on. Not evidence that every asset has zero foreign-country exposure; asset geography schedule remains open.'},'scenarios_conditional_not_fair_value_range':scenarios,'sensitivity':sensitivity,'market_input_crosschecks':[{'label':'Monthly matched RF and ERP, retrieved beta','ke':.0529+1.38*.0441,'conditional_value':ri(.135,.0529+1.38*.0441,.05,.115,.025)['conditional_value_per_share']},{'label':'November 6 RF with unchanged November 1 ERP, mixed-date sensitivity','ke':.0486+1.38*.0441,'conditional_value':ri(.135,.0486+1.38*.0441,.05,.115,.025)['conditional_value_per_share']}],'reverse_single_stage_implied_sustainable_ROE':implied_roe,'normalization':{'q3_adjusted_earnings':108.134,'less_unrealized_platform_gain':35,'after_mark_removal':73.134,'less_equity_expenses':3.541,'after_mark_and_SBC':69.593,'economic_project_loss_already_included':21.425,'9M_adjusted_earnings':308.597,'9M_after_mark_and_SBC':308.597-35-27.277,'note':'Not FCFE; does not certify recurring gain-on-sale, cash taxes, project capital replacement or convertible economics.'},'gaps':['Project-by-project cash waterfalls, amortization, tax-equity flips and replacement capital not independently reconciled','Clean-surplus economic common book and noncontrolling claim mapping remain incomplete','Fully diluted settlement and capped-call adjustment mechanics unresolved for valuation','Country-by-country invested capital not fully mapped; no blanket zero-risk assertion','2028 guidance is adjusted earnings, not after-tax cash distributable to common stock','Stage 1 and long-trend technical checks not independently recalculated'],'no_remote_writes':True}
(D/'results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'history':data,'capital':capital,'scenario_values':{k:round(v['conditional_value_per_share'],2) for k,v in scenarios.items()},'implied_roe':implied_roe},indent=2))
