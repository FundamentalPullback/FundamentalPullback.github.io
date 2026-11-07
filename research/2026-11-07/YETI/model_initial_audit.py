import json,datetime,pathlib
P=pathlib.Path(__file__).parent
f=json.load(open(P/'companyfacts.json'))['facts']['us-gaap']
tags={'sales':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','cfo':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','da':'DepreciationDepletionAndAmortization'}
def fact(tag,end,dayslo,dayshi):
 rows=[x for x in f[tag]['units']['USD'] if x['end']==end and x.get('start') and dayslo<=(datetime.date.fromisoformat(end)-datetime.date.fromisoformat(x['start'])).days<=dayshi and x['filed']<='2026-11-07']
 return sorted(rows,key=lambda x:x['filed'])[-1]['val']/1e6 if rows else None
hist={}
for label,end,lo,hi in [('FY2023','2023-12-30',350,380),('FY2024','2024-12-28',350,380),('FY2025','2026-01-03',350,380),('H12025','2025-06-28',170,195),('H12026','2026-07-04',170,195),('Q32025','2025-09-27',80,100),('Q12026','2026-04-04',80,100),('Q22026','2026-07-04',80,100)]:
 hist[label]={k:fact(v,end,lo,hi) for k,v in tags.items()}
# Q4 derived FY minus9m; quarterly CF derived from cumulative cash flow.
for k,v in tags.items():
 if hist['Q32025'][k] is None:
  hist['Q32025'][k]=fact(v,'2025-09-27',260,285)-hist['H12025'][k]
 if hist['Q22026'][k] is None: hist['Q22026'][k]=hist['H12026'][k]-hist['Q12026'][k]
hist['Q22026']['sbc']=hist['H12026']['sbc']-hist['Q12026']['sbc']
hist['Q42025']={k:hist['FY2025'][k]-fact(v,'2025-09-27',260,285) for k,v in tags.items()}
hist['TTM']={k:hist['FY2025'][k]-hist['H12025'][k]+hist['H12026'][k] for k in tags}
for a in hist.values(): a['fcf']=a['cfo']-a['capex'];a['fcf_less_sbc']=a['fcf']-a['sbc']
# Illustrative FCFF; no calibrated WACC claim. SBC retained in GAAP-like margin.
# Years1-5 explicit capex, DA and working capital; years6-10 blend toward growth/ROIC reinvestment.
def dcf(growth=.07,margin=.135,wacc=.09,terminal_roic=.18):
 rev=1868.494*1.075;pv=0;rows=[]
 for y in range(1,11):
  g=growth if y<=5 else growth+(0.025-growth)*(y-5)/5
  old=rev;rev*=1+g
  m=margin+(0.15-margin)*min(y,10)/10
  nopat=rev*m*.76
  explicit=rev*(.033-.029)+(rev-old)*.15
  reinv=explicit if y<=5 else explicit*(1-(y-5)/5)+(nopat*g/terminal_roic)*((y-5)/5)
  fcff=nopat-reinv;pv+=fcff/(1+wacc)**y
  rows.append({'year':y,'sales':rev,'growth':g,'margin':m,'nopat':nopat,'reinvestment':reinv,'fcff':fcff})
 tv=rows[-1]['nopat']*1.025*(1-.025/terminal_roic)/(wacc-.025)
 # cash59.823, reserve40 assumption, gross debt101.7; finance-lease reconciliation pending, no invented amount
 eq=pv+tv/(1+wacc)**10+19.823-101.7
 return {'value_per_share':eq/74.1,'pv_terminal_share':(tv/(1+wacc)**10)/(pv+tv/(1+wacc)**10),'rows':rows}
scenarios={'bear':dcf(.03,.115,.10,.15),'central_illustrative':dcf(),'bull':dcf(.09,.15,.08,.22)}
sensitivity={str(w):dcf(wacc=w)['value_per_share'] for w in [.07,.08,.09,.10,.11]}
lo,hi=-.03,.3
for _ in range(80):
 m=(lo+hi)/2
 if dcf(growth=m)['value_per_share']<45:lo=m
 else:hi=m
out={'unit':'USD millions except per share','history':hist,'assumptions':{'FY26_sales_reference':1868.494*1.075,'cash_reserve':40,'diluted_shares_reference':74.1,'tax':.24,'terminal_growth':.025,'central_wacc_illustrative_not_calibrated':.09,'lease_treatment':'operating rent retained in operating margin; do not also subtract operating lease liabilities'},'scenarios':scenarios,'wacc_sensitivity':sensitivity,'reverse_initial_growth_at_45_with_other_central_assumptions':(lo+hi)/2}
json.dump(out,open(P/'model.json','w'),indent=2);print(json.dumps({'history':hist,'values':{k:v['value_per_share'] for k,v in scenarios.items()},'sensitivity':sensitivity,'reverse':out['reverse_initial_growth_at_45_with_other_central_assumptions']},indent=2))
# Additional sourced calibration, separate from initial illustrative grid.
raw_beta=1.63
normalized_beta=2/3*raw_beta+1/3 # transparent shrinkage alternative, not a rule adopted by user
rf=.0486;erp=.0441;kd=.0553
E=45*74.1;D=101.7;dw=D/(D+E)
cal={}
for label,beta in [('raw_5y_monthly',raw_beta),('two_thirds_shrinkage',normalized_beta)]:
 ke=rf+beta*erp;w=ke*(1-dw)+kd*(1-.24)*dw
 lo,hi=-.03,.3
 for _ in range(80):
  mid=(lo+hi)/2
  if dcf(growth=mid,wacc=w)['value_per_share']<45:lo=mid
  else:hi=mid
 cal[label]={'beta':beta,'ke':ke,'wacc':w,'value':dcf(wacc=w)['value_per_share'],'reverse_growth_at_45':(lo+hi)/2,'terminal_weight':dcf(wacc=w)['pv_terminal_share']}
out['sourced_calibration']={'rf':rf,'rf_date':'2026-11-06 secondary corroboration; H15 indexed prior day4.84','erp':erp,'erp_date':'2026-11-01 Damodaran indexed snapshot','kd':kd,'kd_period':'Q2FY2026 term loan weighted rate; proxy not fresh marginal quote','debt_weight':dw,'cases':cal,'refund_asset_not_added':'68.749 receivable not added separately; sensitivity upper bound net tax approx52.249 or0.705pershare, less costs/timing and no duplicate cash projection'}
json.dump(out,open(P/'model.json','w'),indent=2)
print(json.dumps(out['sourced_calibration'],indent=2))
