"""VNT V2: preserves V1, reconciles economic dates with an explicit Q4 stub.
Primary economic anchor is 2-Oct-2026; information cut is 5-Nov-2026.
This is NOT an ex-ante 2-Oct valuation and NOT a fully reconciled 5-Nov equity value.
USD millions, except per share. Q4 bridge forecasts are analyst estimates.
"""
from pathlib import Path
import datetime as dt,json,copy
P=Path(__file__).parent; v1=json.loads((P/'baseline_v1.json').read_text())
anchor=dt.date(2026,10,2);stub_end=dt.date(2026,12,31);price_date=dt.date(2026,11,5)
def dated_model(a,stub,minimum_reinvestment_ratio=0):
 rev=a['revenue0'];rows=[]
 for i in range(10):
  g=a['growth'][i] if i<5 else a['growth'][-1]+(a['g']-a['growth'][-1])*(i-4)/5
  m=a['margin'][i] if i<5 else a['margin'][-1]
  prev=rev;rev*=1+g;ebit=rev*m;nopat=ebit*(1-a['tax'])
  if i<5:
   da=rev*a['da'];inv=rev*a['investment'];wc=(rev-prev)*a['nwc'];reinv=max(inv+wc-da,nopat*minimum_reinvestment_ratio);rr=reinv/nopat
   if i==4:rr5=rr
  else:rr=rr5+(a['g']/a['roic']-rr5)*(i-4)/5;reinv=nopat*rr;da=inv=wc=None
  fcff=nopat-reinv;date=dt.date(2027+i,12,31);t=(date-anchor).days/365;pv=fcff/(1+a['wacc'])**t
  rows.append(dict(year=2027+i,payment_date=date.isoformat(),discount_years=t,revenue=rev,ebit=ebit,nopat=nopat,da=da,investment=inv,nwc=wc,reinvestment=reinv,reinvestment_ratio=rr,fcff=fcff,pv=pv))
 tn=nopat*(1+a['g']);tf=tn*(1-a['g']/a['roic']);tv=tf/(a['wacc']-a['g']);ptv=tv/(1+a['wacc'])**t
 st=(stub_end-anchor).days/365;sfcff=stub['revenue']*stub['margin']*(1-a['tax'])+stub['revenue']*stub['da']-stub['revenue']*stub['investment']-stub['delta_nwc'];spv=sfcff/(1+a['wacc'])**st
 evnostub=sum(r['pv'] for r in rows)+ptv;ev=evnostub+spv;ded=v1['bridge']['net_deduction'];eq=ev-ded
 return dict(economic_anchor=anchor.isoformat(),information_asof='2026-11-05',value=eq/a['shares'],ev=ev,equity=eq,ev_without_stub=evnostub,value_without_stub=(evnostub-ded)/a['shares'],terminal_weight=ptv/ev,terminal_fcff=tf,terminal_nopat=tn,pv_terminal=ptv,stub={'period_start':'2026-10-03','period_end':stub_end.isoformat(),'discount_years':st,'assumptions':stub,'fcff':sfcff,'pv':spv,'per_share':spv/a['shares']},rows=rows)
stubs={'adverse':{'revenue':785,'margin':.18,'da':.035,'investment':.045,'delta_nwc':20},'central':{'revenue':785,'margin':.205,'da':.035,'investment':.04,'delta_nwc':10},'favorable':{'revenue':785,'margin':.225,'da':.035,'investment':.04,'delta_nwc':0}}
sc={k:dict(assumptions=v['assumptions'],**dated_model(v['assumptions'],stubs[k])) for k,v in v1['scenarios'].items()}
a=v1['scenarios']['central']['assumptions'];b=v1['bridge']
sens=[dict(wacc=w,g=g,value=dated_model(a|dict(wacc=w,g=g),stubs['central'])['value']) for w in [.09,.095,.1,.105,.11] for g in [.02,.025,.03]]
# Measure the missing-stub effect with broad cash-flow sensitivity, not assertions of bounds.
st=(stub_end-anchor).days/365;nostub=sc['central']['value_without_stub']
stub_cash_sensitivity=[{'q4_fcff':x,'value_at_oct2':nostub+x/(1+a['wacc'])**st/a['shares']} for x in [0,50,100,150,200]]
rr_sens=[{'minimum_reinvestment_nopat':q,'value_at_oct2':dated_model(a,stubs['central'],q)['value']} for q in [0,.10,.15,.20]]
# Carrying equity forward is a conditional bridge only; November buybacks and awards unknown.
ke=.0495+1.4*.05;days=(price_date-anchor).days
conditional_nov_equity=sc['central']['equity']*(1+ke)**(days/365)
conditional_nov_ps=conditional_nov_equity/a['shares']
# $10m of unknown value/distribution adjustment changes per-share value by 10/shares only
# when it is a net economic claim change, NOT a matched repurchase + share retirement.
wc={'q3_2025':{'ar_financing':-27.2-17.5,'other_operating':-87.8-(-69.4),'cfo':110.5},'q3_2026':{'ar_financing':-43.3-(-52.2),'other_operating':-76.2-(-73.3),'cfo':142.8}}
for x in wc.values():x['two_rows_sum']=x['ar_financing']+x['other_operating'];x['cfo_before_two_rows']=x['cfo']-x['two_rows_sum']
wc['change']={'ar_financing':wc['q3_2026']['ar_financing']-wc['q3_2025']['ar_financing'],'other_operating':wc['q3_2026']['other_operating']-wc['q3_2025']['other_operating'],'two_rows_sum':wc['q3_2026']['two_rows_sum']-wc['q3_2025']['two_rows_sum'],'cfo':142.8-110.5,'cfo_before_two_rows_pct':wc['q3_2026']['cfo_before_two_rows']/wc['q3_2025']['cfo_before_two_rows']-1}
rd={'revenue_change':736.9-752.5,'cogs_cost_reduction':396.4-386.1,'sga_cost_reduction':151-146.7,'rd_cost_reduction':44.4-30.1,'amortization_cost_reduction':18.3-15.6,'ebit_change':158.4-142.4,'rd_share_of_arithmetic_ebit_change':14.3/16,'retained_rd_change':None,'divested_rd':None}
recon=[{'step':'V1, implicit annual schedule without Q4 stub','value':v1['scenarios']['central']['value']},{'step':'Actual dated FY27–FY36 payments at Oct2 anchor, before Q4 stub','value':nostub},{'step':'Add modeled Q4 operating FCFF, no duplicate cash or transactions','value':sc['central']['value']},{'step':'Conditional equity carry Oct2→Nov5, no distributions/claims/share changes assumed; NOT spot value','value':conditional_nov_ps}]
for i,r in enumerate(recon):r['change']=0 if i==0 else r['value']-recon[i-1]['value']
checks={'q4_days_90':(stub_end-anchor).days==90,'carry_days_34':days==34,'cash_bridge_reconciles':abs(wc['change']['two_rows_sum']-69.1)<1e-9,'cfo_bridge':abs(wc['change']['cfo']-32.3)<1e-9,'rd_bridge':abs(sum(rd[k] for k in ['revenue_change','cogs_cost_reduction','sga_cost_reduction','rd_cost_reduction','amortization_cost_reduction'])-rd['ebit_change'])<1e-9,'scenarios_ordered':sc['adverse']['value']<sc['central']['value']<sc['favorable']['value'],'no_stub_double_cash':b['cash']==258.4,'terminal_reinvestment':all(abs(v['rows'][-1]['reinvestment_ratio']-v['assumptions']['g']/v['assumptions']['roic'])<1e-9 for v in sc.values())}
assert all(checks.values()),checks
out={'version':'V2','status':'screen-grade','fundamental_approved':False,'entry_approved':False,'publication_ready':False,'price_reference':{'value':39.75,'timestamp':'2026-11-05T16:49:00Z'},'valuation_type':'Explicit Oct2 economic anchor with Nov5 information; not a fully reconciled current fair value','anchor_date':anchor.isoformat(),'information_date':'2026-11-05','legacy_v1':v1,'scenarios':sc,'bridge':b,'sensitivity':sens,'date_reconciliation':recon,'stub_cash_sensitivity':stub_cash_sensitivity,'reinvestment_sensitivity':rr_sens,'conditional_nov5':{'days':days,'cost_of_equity':ke,'value':conditional_nov_ps,'assumptions':['No distributions, net new capital claims or change in shares','All interim operating flows retained at modeled economics'],'status':'Conditional illustration only; no verified spot bridge'},'working_capital_diagnostic':wc,'rd_ebit_bridge':rd,'treasury':{'rate':.0495,'observation_date':'2026-11-03','publication_date':'2026-11-04','primary_url':'https://www.federalreserve.gov/feeds/Data/H15_H15_RIFLGFCY10_N.B.XML','file':'../sources/h15_xml.txt','verified':True},'checks':checks}
(P/'calculations.json').write_text(json.dumps(out,indent=2));(P/'run_log.json').write_text(json.dumps({'checks':checks,'independent_audit':'V2 pending','hard_failures':[],'economic_gaps':['Retained perimeter','Current share/award inventory','Full operating FCFF bridge','Current capital flows and balance claims','Economically validated acquisition/reinvestment costs'],'approval':False},indent=2))
print(json.dumps({'scenarios':{k:{x:v[x] for x in ['value','terminal_weight']} for k,v in sc.items()},'date_bridge':recon,'wc':wc,'stub_sens':stub_cash_sensitivity,'reinvestment_sens':rr_sens,'checks':checks},indent=2))
