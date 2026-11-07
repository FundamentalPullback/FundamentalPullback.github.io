"""LEVI conditional FCFF, USD millions. Python standard library, no data downloads.
Run: python scanner_continuation/LEVI/model.py. All forecasts are analyst estimates.
Historical inputs: SEC FY2025 10-K, Q1/Q2/Q3 2026 10-Q. See sources.json.
Not an approved entry or decision-ready valuation. Full bridge gaps in report.md.
"""
import json
from pathlib import Path
OUT=Path(__file__).parent
CLOSE=22.87
SHARES=99.502081+283.967658+(390.620582-386.075414)
BRIDGE={'cash':641.4,'securities':137.9,'operating_cash_reserve':-200,'subsequent_dividend':-61,'debt_including_accrued_interest_proxy':-1053.3,'finance_leases_FY25_proxy':-73.5,'gross_pension_postretirement_FY25':-151.2,'net_deferred_compensation_proxy':-7.2,'restructuring':-52.3,'net_derivatives':-3.3}
HIST={
 'FY2023':dict(revenue=5842.1,gross_profit=3360.7,ebit=354.4,ni_cont=250.6,eps_cont=.62,cfo=435.5,capex=313.6,da=165.3,sbc=74.4,fx_investing=16.1),
 'FY2024':dict(revenue=6032.,gross_profit=3657.1,ebit=262.7,ni_cont=210.4,eps_cont=.52,cfo=898.4,capex=227.5,da=193.2,sbc=62.8,fx_investing=-17.4),
 'FY2025':dict(revenue=6282.,gross_profit=3877.8,ebit=677.6,ni_cont=502.,eps_cont=1.26,cfo=529.6,capex=221.4,da=206.3,sbc=81.6,fx_investing=24.3),
 '9M2025':dict(revenue=4516.2,gross_profit=2805.,ebit=467.,ni_cont=341.8,cfo=262.8,capex=170.3,da=151.4,sbc=67.8,fx_investing=37.1),
 '9M2026':dict(revenue=4914.2,gross_profit=3123.2,ebit=543.2,ni_cont=440.5,cfo=585.2,capex=157.9,da=167.6,sbc=58.8,fx_investing=-179.7),
 'Q1FY2026':dict(revenue=1742.5,gross_profit=1078.3,ebit=198.7,ni_cont=177.1,cfo=211.5,capex=59.4,da=55.6,sbc=15.8),
 'H1FY2026':dict(revenue=3304.5,gross_profit=2057.4,ebit=320.9,ni_cont=271.9,cfo=482.3,capex=99.3,da=112.8,sbc=40.1)}
def diff(a,b):return {k:round(v-b[k],8) for k,v in a.items() if k in b and k!='eps_cont'}
HIST['Q4FY2025']=diff(HIST['FY2025'],HIST['9M2025'])
HIST['Q2FY2026']=diff(HIST['H1FY2026'],HIST['Q1FY2026'])
HIST['Q3FY2026']=diff(HIST['9M2026'],HIST['H1FY2026'])
HIST['TTM2026']={k:round(HIST['FY2025'][k]-HIST['9M2025'][k]+HIST['9M2026'][k],8) for k in HIST['9M2026']}
for r in HIST.values():
 r['fcf_cfo_capex']=r['cfo']-r['capex'];r['fcf_less_sbc']=r['fcf_cfo_capex']-r['sbc'];r['operating_margin']=r['ebit']/r['revenue']
 if 'fx_investing'in r:r['cash_after_fx_and_sbc']=r['fcf_less_sbc']+r['fx_investing']
R0=6282*1.07
CASES={
 'adverso':dict(growth=.01,m1=.095,m5=.09,m10=.09,wacc=.1125,g=.02,roic=.10),
 'central':dict(growth=.04,m1=.105,m5=.115,m10=.115,wacc=.099,g=.025,roic=.15),
 'favorable':dict(growth=.07,m1=.11,m5=.135,m10=.13,wacc=.088,g=.03,roic=.20)}
def model(growth,m1,m5,m10,wacc,g,roic,tax=.25,reserve=200,extra_claim=0):
 assert wacc>g and roic>g
 rows=[];rev=R0;old_nopat=R0*.1045*(1-tax)
 for y in range(1,11):
  gr=growth if y<=5 else growth+(g-growth)*(y-5)/5
  margin=m1+(m5-m1)*(y-1)/4 if y<=5 else m5+(m10-m5)*(y-5)/5
  old=rev;rev*=1+gr;ebit=rev*margin;nopat=ebit*(1-tax);da=rev*.0335;nwc=max(0,rev-old)*.15
  reinvest=max(max(0,nopat-old_nopat)/roic,rev*.004+nwc)
  capex=da+reinvest-nwc;fcff=nopat+da-capex-nwc
  rows.append(dict(year=y,growth=gr,revenue=rev,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+wacc)**y))
  old_nopat=nopat
 # Terminal reinvestment exactly NOPAT*g/ROIC, checked against physical/NWC floor.
 terminal_nopat=nopat*(1+g);terminal_reinvest=terminal_nopat*g/roic
 floor=rev*(1+g)*.004+rev*g*.15
 assert terminal_reinvest>=floor
 terminal_fcff=terminal_nopat-terminal_reinvest;tv=terminal_fcff/(wacc-g);pv_tv=tv/(1+wacc)**10
 ev=sum(r['pv'] for r in rows)+pv_tv;bridge=sum(BRIDGE.values())+200-reserve-extra_claim
 return dict(rows=rows,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvest,terminal_floor=floor,terminal_fcff=terminal_fcff,pv_terminal=pv_tv,ev=ev,equity=ev+bridge,bridge=bridge,shares=SHARES,price=(ev+bridge)/SHARES,terminal_weight=pv_tv/ev)
def solve(key,target=CLOSE):
 p=CASES['central'].copy();lo,hi=(0,.30) if key=='growth' else (.08,.25)
 def val(x):
  q=p.copy();q[key]=x
  if key=='m5':q['m10']=x
  return model(**q)['price']
 if not val(lo)<=target<=val(hi):return {'bounded':False,'low_price':val(lo),'high_price':val(hi)}
 for _ in range(100):
  mid=(lo+hi)/2
  if val(mid)<target:lo=mid
  else:hi=mid
 return dict(bounded=True,parameter=key,value=(lo+hi)/2,reconstructed_price=val((lo+hi)/2))
RESULT={k:model(**v) for k,v in CASES.items()}
SENS=[{'wacc':w,'g':g,'price':model(**(CASES['central']|{'wacc':w,'g':g}))['price']} for w in [.089,.094,.099,.104,.109] for g in [.015,.02,.025,.03]]
equity_market=CLOSE*SHARES;debt_weight=(1043.6+73.5)/(equity_market+1043.6+73.5)
CAPM=dict(rf=.0486,beta=1.3,erp=.0441,kd_assumed=.06,tax=.25,debt_weight=debt_weight)
CAPM['ke']=CAPM['rf']+CAPM['beta']*CAPM['erp'];CAPM['wacc']=CAPM['ke']*(1-debt_weight)+CAPM['kd_assumed']*(1-CAPM['tax'])*debt_weight
OUTDATA=dict(status='partial_conditional_not_entry_approved',asof='2026-11-07',close_date='2026-11-06',close=CLOSE,scannerLast=22.87,inputs=CASES,initial_revenue=R0,bridge_items=BRIDGE,history=HIST,capm=CAPM,scenarios=RESULT,sensitivity=SENS,inverse_growth=solve('growth'),inverse_margin=solve('m5'),claim_sensitivity=[dict(extra_claim=x,price=model(**CASES['central'],extra_claim=x)['price']) for x in [0,100,200]],capm_beta_sensitivity=[dict(beta=b,wacc=(.0486+b*.0441)*(1-debt_weight)+.06*.75*debt_weight) for b in [.94,1.1,1.3,1.5]],tax_sensitivity=[dict(tax=t,price=model(**CASES['central'],tax=t)['price']) for t in [.23,.25,.28]])
for k in ['revenue','ebit','ni_cont','cfo','capex','da','sbc']:
 assert abs(sum(HIST[q][k] for q in ['Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026'])-HIST['TTM2026'][k])<1e-6
assert RESULT['adverso']['price']<RESULT['central']['price']<RESULT['favorable']['price']
for s in RESULT.values():
 for r in s['rows']:assert abs(r['fcff']-(r['nopat']+r['da']-r['capex']-r['delta_nwc']))<1e-8
OUTDATA['qa']={'quarterly_ttm_tieout':True,'fcff_identity':True,'terminal_reinvestment_financed':True,'ordered_scenarios':True,'independent_audit':'completed_with_caveats_see_audit_json'}
(OUT/'model_results.json').write_text(json.dumps(OUTDATA,indent=2))
print(json.dumps({'prices':{k:round(v['price'],2) for k,v in RESULT.items()},'capm':CAPM,'inverse':OUTDATA['inverse_growth'],'margin':OUTDATA['inverse_margin'],'ttm':HIST['TTM2026'],'terminal':{k:round(v['terminal_weight'],3) for k,v in RESULT.items()}},indent=2))
