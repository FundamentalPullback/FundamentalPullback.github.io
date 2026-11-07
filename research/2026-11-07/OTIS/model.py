import json,pathlib
P=pathlib.Path(__file__).parent
PRICE=78.96;SHARES=381.9
# USD millions. Consolidated FCFF; leases retained as operating costs.
BRIDGE={'debt':8275,'cash':866,'operating_cash_reserve':200,'pension_net_proxy':320,'minority_value_proxy':900}
CASES={'adverso':dict(sg=.035,ng=-.03,m5=.15,m10=.15,tax=.27,w=.09,g=.02,roic=.15),'central':dict(sg=.06,ng=0,m5=.175,m10=.18,tax=.26,w=.08,g=.025,roic=.20),'favorable':dict(sg=.08,ng=.025,m5=.19,m10=.195,tax=.25,w=.07,g=.03,roic=.25)}
def calc(c,delta_growth=0,delta_margin=0):
 s,n=10116.,5019.;r=s+n;rows=[];pv=0
 for y in range(1,11):
  tr=max(0,(y-5)/5)
  sg=(c['sg']+delta_growth)*(1-tr)+c['g']*tr;ng=(c['ng']+delta_growth)*(1-tr)+c['g']*tr
  s*=1+sg;n*=1+ng;nr=s+n;growth=nr/r-1
  margin=(.1535+(c['m5']-.1535)*y/5 if y<=5 else c['m5']+(c['m10']-c['m5'])*tr)+delta_margin
  ebit=nr*margin;nopat=ebit*(1-c['tax']);da=nr*.011;capex=nr*.015;acq=nr*.008;nwc=max(0,nr-r)*.05
  detailed=capex+acq+nwc-da
  reinv=detailed*(1-tr)+nopat*growth/c['roic']*tr
  fcff=nopat-reinv;pvf=fcff/(1+c['w'])**y;pv+=pvf
  rows.append(dict(year=y,service=s,new_equipment=n,revenue=nr,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,acquisitions=acq,nwc=nwc,reinvestment=reinv,fcff=fcff,pv=pvf));r=nr
 terminal_nopat=nopat*(1+c['g']);terminal_reinv=terminal_nopat*c['g']/c['roic'];tv=(terminal_nopat-terminal_reinv)/(c['w']-c['g']);pvt=tv/(1+c['w'])**10;ev=pv+pvt
 eq=ev-BRIDGE['debt']+BRIDGE['cash']-BRIDGE['operating_cash_reserve']-BRIDGE['pension_net_proxy']-BRIDGE['minority_value_proxy']
 return dict(value=eq/SHARES,ev=ev,equity=eq,pv_terminal_share=pvt/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,rows=rows)
def solve(fn,lo,hi):
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2
if __name__=='__main__':
 result={k:calc(v) for k,v in CASES.items()};b=CASES['central']
 result['sensitivity']=[dict(w=w,g=g,value=calc(dict(b,w=w,g=g))['value']) for w in [.07,.075,.08,.085,.09] for g in [.02,.025,.03]]
 result['inverse']={'extra_segment_growth':solve(lambda x:calc(b,delta_growth=x)['value'],-.02,.2),'parallel_margin_increase':solve(lambda x:calc(b,delta_margin=x)['value'],-.05,.15)}
 result['capm']={'rf':.0486,'observed_beta':.87,'normalized_beta':1.,'erp_assumption':.045,'kd_assumption':.055,'debt_weight':8275/(8275+380.710513*PRICE),'tax':.26}
 a=result['capm'];a['wacc_observed_beta']=(1-a['debt_weight'])*(a['rf']+a['observed_beta']*a['erp_assumption'])+a['debt_weight']*a['kd_assumption']*(1-a['tax']);a['wacc_normalized_beta']=(1-a['debt_weight'])*(a['rf']+a['normalized_beta']*a['erp_assumption'])+a['debt_weight']*a['kd_assumption']*(1-a['tax'])
 result['capm_sensitivity']=[dict(beta=b,erp=e,wacc=(1-a['debt_weight'])*(a['rf']+b*e)+a['debt_weight']*a['kd_assumption']*(1-a['tax'])) for b in [.8,.87,1,1.1] for e in [.04,.045,.05]]
 result['bridge']=BRIDGE;result['inputs']=CASES;result['price']=PRICE;result['shares']=SHARES
 assert all(v['value']>0 and len(v['rows'])==10 for k,v in result.items() if k in CASES)
 (P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:{x:v[x] for x in ['value','ev','pv_terminal_share']} for k,v in result.items() if k in CASES},indent=2));print(result['inverse']);print(result['capm'])
