from pathlib import Path
import json
P=Path(__file__).parent;PRICE=503.69;SHARES=173.3;START=8176
BRIDGE=dict(cash=1513,short_investments=108,operating_cash_reserve=500,principal_debt=7120,nci=144,pension_other_retirement_liability_proxy=220,uncertain_tax=167,utp_interest=49,MAKS_indemnities=19,net_derivative_liability=488,divestiture_receivable_excluded=154,affiliate_assets_excluded=489,pension_assets_excluded=82)
NET=1513+108-500-7120-144-220-167-49-19-488;BRIDGE['net']=NET

def calc(gd=0,md=0,w=.10,g=.025,roic=.25,tax=.25,net=NET,start=START,shares=SHARES,nopat_anchor_margin=None):
 gs=[.07+gd,.06+gd,.06+gd,.05+gd,.05+gd];gs += [gs[-1]+(g-gs[-1])*i/5 for i in range(1,6)];margins=[.44+md,.445+md,.45+md,.455+md,.46+md]+[.46+md]*5
 r=start;rows=[];pv=0;previous_nopat=start*(nopat_anchor_margin if nopat_anchor_margin is not None else .44)*(1-tax)
 for i,gr in enumerate(gs):
  prev=r;r*=1+gr;nopat=r*margins[i]*(1-tax);da=r*.055;capex=r*.045;nwc=(r-prev)*.05;explicit=capex-da+nwc;economic=(max(0,nopat-previous_nopat)/roic if nopat_anchor_margin is not None else nopat*gr/roic);previous_nopat=nopat;re=max(explicit,economic);fc=nopat-re;p=fc/(1+w)**(i+1);pv+=p
  rows.append(dict(year=i+1,revenue=r,growth=gr,ebit_margin=margins[i],ebit=r*margins[i],nopat=nopat,da=da,capex=capex,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,additional_reinvestment_reserve=re-explicit,reinvestment=re,fcff=fc,pv_fcff=p))
 tr=r*(1+g);tn=tr*margins[-1]*(1-tax);te=tr*(.045-.055)+(tr-r)*.05;tri=max(te,tn*g/roic);tcf=tn-tri;tv=tcf/(w-g)/(1+w)**10;ev=pv+tv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,pv_explicit=pv,pv_terminal=tv,terminal_weight=tv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,net=net,start=start,shares=shares,growth_delta_first5=gd,margin_delta_all10terminal=md,nopat_anchor_margin=nopat_anchor_margin))
def scan(fn,lo,hi):
 a=[dict(x=lo+(hi-lo)*i/400,value=fn(lo+(hi-lo)*i/400)) for i in range(401)];roots=[]
 for v,z in zip(a,a[1:]):
  if (v['value']-PRICE)*(z['value']-PRICE)<0:
   l=v['x'];h=z['x'];fl=v['value']-PRICE
   for _ in range(75):
    m=(l+h)/2
    if (fn(m)-PRICE)*fl>0:l=m
    else:h=m
   roots.append((l+h)/2)
 return dict(scan=a,roots=roots,maximum=max(a,key=lambda x:x['value']))
cases=dict(bear=calc(gd=-.04,md=-.05,w=.11,g=.015,roic=.18,tax=.27),base=calc(),bull=calc(gd=.04,md=.03,w=.09,g=.03,roic=.30,tax=.24))
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03',capital_bridge=BRIDGE,cases=cases,reverse_growth=scan(lambda x:calc(gd=x)['value'],0,.6),reverse_margin=scan(lambda x:calc(md=x)['value'],0,.35),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.09,.095,.10,.105,.11] for g in [.015,.02,.025,.03]],nopat_growth_sensitivity=[dict(anchor_margin=x,value=calc(nopat_anchor_margin=x)['value'],method='max(explicit reinvestment, positive delta NOPAT / ROIC), including margin evolution; terminal unchanged') for x in [3644/8176,.44]],capital_sensitivity={k:calc(net=NET+v)['value'] for k,v in dict(receivable154_received=154,affiliate_assets_book=489,remove_all_derivative_reserve=488,remove_all_retirement_proxy=220,pension_assets_available=82,operating_cash300=200,operating_cash700=-200,nonincome_tax_extra16=-16).items()},perimeter_sensitivity=[dict(revenue_reduction=x,value=calc(start=START-x)['value']) for x in [50,100,150]],dilution_sensitivity=calc(shares=SHARES*1.03)['value'],roic_sensitivity=[dict(roic=x,value=calc(roic=x)['value']) for x in [.15,.20,.25,.30,.40]])
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print('net',NET,'growth',out['reverse_growth']['roots'],'margin',out['reverse_margin']['roots'])
