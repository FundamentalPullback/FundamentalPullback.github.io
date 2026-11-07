import json,csv,math
from pathlib import Path
P=Path(__file__).parent
# All USD million except per-share values; directly transcribed continuing-operation statements.
cols=['sales','cogs','sga','dep','amort','rd','pretax','interest_exp','interest_inc','net_cont','eps_cont','cfo_cont','capex','sbc']
raw={
'FY2023':[16242,9678,3401,360,154,424,1690,247,140,1223,5.16,2294,516,56],
'FY2024':[15845,9252,3391,360,132,423,1852,241,177,1344,5.72,1391,721,42],
'FY2025':[15875,9316,3439,403,125,423,2045,241,153,1571,6.92,1936,778,46],
'9M2024':[12116,7036,2556,273,100,317,1771,184,135,1342,5.70,1056,513,30],
'9M2025':[11961,7000,2534,297,97,314,1656,183,129,1269,5.57,1047,477,35],
'9M2026':[12778,7551,2692,321,79,326,1717,199,124,1294,5.78,1160,464,37],
'Q12026':[3930,2275,885,105,27,113,517,61,37,382,1.70,33,196,11],
'H12026':[8425,4962,1816,213,53,220,1086,132,79,821,3.66,594,309,27],
'Q32026':[4353,2589,876,108,26,106,631,67,45,473,2.12,566,155,10]}
a={k:dict(zip(cols,v)) for k,v in raw.items()}
for name,plus,minus in [('Q42025','FY2025','9M2025'),('Q22026','H12026','Q12026')]:a[name]={c:a[plus][c]-a[minus][c] for c in cols}
for name,fy,new,old in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:a[name]={c:a[fy][c]+a[new][c]-a[old][c] for c in cols}
for k,v in a.items():
 v['ebit_unlevered_reported']=v['pretax']+v['interest_exp']-v['interest_inc']
 v['operating_subtotal_before_other']=v['sales']-sum(v[x] for x in ['cogs','sga','dep','amort','rd'])
 v['fcf_equity_proxy']=v['cfo_cont']-v['capex'];v['da']=v['dep']+v['amort']
# normalized EBIT keeps SBC & acquisition amortization; recurring environmental/reorganization reserve modeled explicitly.
base_sales=a['TTM2026']['sales']; initial_margin=(a['TTM2026']['operating_subtotal_before_other']-50)/base_sales
bridge={'gross_debt':6841,'cash_and_short_investments':1642,'minimum_operating_cash':base_sales*.02,'pension_and_opeb_after_tax':(546+385)*.76,'nci':143,'diluted_shares':223.2}
bridge['deductions']=6841-1642+base_sales*.02+(546+385)*.76+143
scenarios={
'bear':{'growth':[-.02,.00,.01,.02,.02],'margin5':.12,'margin10':.12,'wacc':.10,'g':.02,'roic':.10,'capex':.042,'nwc':.20},
'base':{'growth':[.04]*5,'margin5':.14,'margin10':.14,'wacc':.09,'g':.025,'roic':.13,'capex':.04,'nwc':.19},
'bull':{'growth':[.06,.06,.055,.05,.045],'margin5':.155,'margin10':.15,'wacc':.085,'g':.03,'roic':.16,'capex':.04,'nwc':.19}}
def dcf(p):
 sales=base_sales;out=[];previous_nopat=base_sales*initial_margin*.76
 for year in range(1,11):
  gr=p['growth'][year-1] if year<=5 else p['growth'][-1]+(p['g']-p['growth'][-1])*(year-5)/5
  margin=initial_margin+(p['margin5']-initial_margin)*year/5 if year<=5 else p['margin5']+(p['margin10']-p['margin5'])*(year-5)/5
  new=sales*(1+gr);ebit=new*margin;nopat=ebit*.76;da=new*.032;capex=new*p['capex'];dnwc=(new-sales)*p['nwc']
  physical=capex-da+dnwc;economic=max(0,nopat-previous_nopat)/p['roic']; reinvest=max(physical,economic)
  # Extra economic investment included in capex, not added as an unexplained cash deduction.
  capex+=max(0,economic-physical);fcff=nopat+da-capex-dnwc
  out.append(dict(year=year,sales=new,growth=gr,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,dnwc=dnwc,physical_reinvestment=physical,economic_reinvestment=economic,additional_economic_investment=max(0,economic-physical),opening_nopat=previous_nopat,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+p['wacc'])**year));sales=new;previous_nopat=nopat
 terminal_sales=sales*(1+p['g']);tn=terminal_sales*p['margin10']*.76
 te=p['g']*tn/p['roic'];tp=terminal_sales*(p['capex']-.032)+(terminal_sales-sales)*p['nwc'];tr=max(te,tp);tf=tn-tr
 tv=tf/(p['wacc']-p['g']);pvt=tv/(1+p['wacc'])**10;ev=sum(x['pv'] for x in out)+pvt;equity=ev-bridge['deductions']
 return {'rows':out,'terminal':{'sales':terminal_sales,'nopat':tn,'economic_reinvestment':te,'physical_reinvestment':tp,'reinvestment':tr,'fcff':tf,'value':tv,'pv':pvt},'ev':ev,'equity':equity,'per_share':equity/223.2,'terminal_pv_share':pvt/ev}
r={k:dcf(v) for k,v in scenarios.items()}
sens=[{'wacc':w,'g':g,'value':dcf(dict(scenarios['base'],wacc=w,g=g))['per_share']} for w in [.08,.09,.10] for g in [.015,.025,.035]]
# Inverse margin needed at $122.38, same growth, reinvestment, discount, bridge.
lo,hi=.05,.40
for _ in range(100):
 mid=(lo+hi)/2; val=dcf(dict(scenarios['base'],margin5=mid,margin10=mid))['per_share']
 if val<122.38:lo=mid
 else:hi=mid
inverse=(lo+hi)/2
result={'actuals':a,'initial_margin':initial_margin,'bridge':bridge,'assumptions':scenarios,'results':r,'sensitivity':sens,'inverse_margin':inverse,'price':122.38,'valuation_only_25pct_buffer':r['base']['per_share']*.75,'legal_cash_sensitivity':[{'aftertax_cash_cost':x,'per_share_reduction':x/223.2} for x in [100,500,1000]],'qa':{'quarter_sales_sum':sum(a[k]['sales'] for k in ['Q42025','Q12026','Q22026','Q32026']),'ttm_sales':a['TTM2026']['sales'],'terminal_reinvestment_pass':all(v['terminal']['reinvestment']>=max(v['terminal']['economic_reinvestment'],v['terminal']['physical_reinvestment']) for v in r.values()),'no_sbc_addback':True}}
(P/'inputs_and_results.json').write_text(json.dumps(result,indent=2))
with (P/'actuals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in a.items())
with (P/'fcff_projection.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(r['base']['rows'][0].keys()));w.writeheader();w.writerows(dict(case=k,**v) for k,x in r.items() for v in x['rows'])
print(json.dumps({k:{x:v[x] for x in ['ev','per_share','terminal_pv_share']} for k,v in r.items()},indent=2));print('inverse',inverse,'sens',sens);print('actuals',a['TTM2026'],a['TTM2025']);print('bridge',bridge)
assert result['qa']['quarter_sales_sum']==result['qa']['ttm_sales']
assert result['qa']['terminal_reinvestment_pass']
# Five-year conditional shareholder return: exit value discounts only years 6-10 and terminal to year 5.
# Constant debt/cash bridge and shares; $2.96 annual dividend; no credit for excess cash retention/buybacks.
returns={}
for k,v in r.items():
 w=scenarios[k]['wacc'];exit_ev=sum(x['fcff']/(1+w)**(x['year']-5) for x in v['rows'][5:])+v['terminal']['value']/(1+w)**5
 exit_price=(exit_ev-bridge['deductions'])/223.2
 lo,hi=-.9,1
 for _ in range(100):
  ir=(lo+hi)/2;pv=sum(2.96/(1+ir)**n for n in range(1,6))+exit_price/(1+ir)**5
  if pv>122.38:lo=ir
  else:hi=ir
 returns[k]={'year5_exit_price':exit_price,'annual_dividend':2.96,'five_year_irr':(lo+hi)/2}
result['conditional_returns']=returns
(P/'inputs_and_results.json').write_text(json.dumps(result,indent=2))
print('returns',returns)
# Cost-envelope stress: permanent extra $50m pre-tax cost scaled with base sales.
delta=50/base_sales
coststress=dcf(dict(scenarios['base'],margin5=.14-delta,margin10=.14-delta))['per_share']
result['extra_50m_recurring_cost_stress']=coststress
result['physical_floor_only_base_value']=None # intentionally not a fair-value override
(P/'inputs_and_results.json').write_text(json.dumps(result,indent=2))
print('coststress',coststress)

# Machine-readable qualifications and reproducible numerical QA.
result.update({'researchComplete':False,'researchPackageComplete':True,'stage3Complete':False,'entryApproved':False,'approvedValuation':None,'valuationGrade':'conditional operating FCFF; incomplete capital-claim reconciliation'})
for k,v in a.items():
 v['eps_cont_basis']='approximate derived across weighted-share periods' if k in ['Q42025','Q22026','TTM2025','TTM2026'] else 'reported continuing EPS'
bridge['debt_basis']='balance-sheet carrying debt proxy, not reconciled contractual face'
bridge['pension_basis']='noncurrent recognized pension and OPEB only; current claims reconciliation open'
result['dated_current_pension_opeb_sensitivity']={'date':'2025-12-31','current_claims':75,'assumed_aftertax_claims':57,'per_share_reduction':57/223.2,'pension_asset_not_credited':126}
grid=[dcf(dict(scenarios['base'],margin5=.05+i*.0005,margin10=.05+i*.0005))['per_share'] for i in range(701)]
residual=dcf(dict(scenarios['base'],margin5=inverse,margin10=inverse))['per_share']-122.38
qa={'inverse_bracket':[grid[0],grid[-1]],'inverse_monotonic':all(b>a for a,b in zip(grid,grid[1:])),'inverse_residual':residual}
assert grid[0]<122.38<grid[-1] and qa['inverse_monotonic'] and abs(residual)<1e-7
for c,z in r.items():
 for row in z['rows']:
  assert abs(row['economic_reinvestment']-max(0,row['nopat']-row['opening_nopat'])/scenarios[c]['roic'])<1e-7
  assert abs(row['reinvestment']-max(row['economic_reinvestment'],row['physical_reinvestment']))<1e-7
  assert abs(row['fcff']-(row['nopat']+row['da']-row['capex']-row['dnwc']))<1e-7
result['qa'].update(qa)
(P/'inputs_and_results.json').write_text(json.dumps(result,indent=2))
with (P/'actuals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in a.items())
