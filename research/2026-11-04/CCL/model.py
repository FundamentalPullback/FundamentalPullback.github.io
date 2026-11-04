import json
# Everything in USD billions except per-share values; years 1-10 = 2027-2036.
def dcf(ebit,tax,g1,g2,roic1,roic2,wacc,tg,troic,netclaims,shares,jv=0,capexfloor=None):
    nopat=ebit*(1-tax);pv=0;yrs=[]
    for t in range(1,11):
        g=g1 if t<=5 else g2;r=roic1 if t<=5 else roic2
        nopat*=1+g
        economic=nopat*g/r
        floor=capexfloor[t-1] if capexfloor and t<=len(capexfloor) else 0
        reinv=max(economic,floor)
        fcf=nopat-reinv;p=fcf/(1+wacc)**t;pv+=p
        yrs.append(dict(t=t,nopat=nopat,economic_reinvestment=economic,commitment_floor=floor,reinvestment=reinv,fcff=fcf,pv=p))
    tcf=nopat*(1+tg)*(1-tg/troic);tv=tcf/(wacc-tg);pvtv=tv/(1+wacc)**10;ev=pv+pvtv
    return dict(price=(ev+jv-netclaims)/shares,ev=ev,jv=jv,netclaims=netclaims,pv_explicit=pv,pv_terminal=pvtv,terminal_percent=pvtv/ev,year10nopat=nopat,terminal_fcff=tcf,years=yrs)
def ddm(cf,k=.11,g1=.05,g2=.03,tg=.025):
    pv=0
    for t in range(1,11):cf*=1+(g1 if t<=5 else g2);pv+=cf/(1+k)**t
    return pv+cf*(1+tg)/(k-tg)/(1+k)**10
jv=ddm(.35)
floors={'RCL':[2.532+1.5-2.0+.1,4.918+1.5*1.03-2.1+.1,3.605+1.5*1.03**2-2.2+.1,2.066+1.5*1.03**3-2.3+.1], 'CCL':[1.6+2.7-3.0+.1,1.5+2.7*1.03-3.1+.1,1.8+2.7*1.03**2-3.2+.1,1.7+2.7*1.03**3-3.3+.1]}
params={'RCL':dict(ebit=5.5,tax=.02,g1=.09,g2=.05,roic1=.25,roic2=.18,wacc=.10,tg=.025,troic=.12,netclaims=22.872-(.851-.5)+.2,shares=.268,jv=jv,capexfloor=floors['RCL']), 'CCL':dict(ebit=4.22,tax=.02,g1=.07,g2=.04,roic1=.25,roic2=.18,wacc=.10,tg=.025,troic=.12,netclaims=24.559-(1.220-.75)+.019,shares=1.368,jv=0,capexfloor=floors['CCL'])}
scenarios={'RCL':{'bear':params['RCL']|dict(ebit=4.95,tax=.04,g1=.03,g2=.03,roic1=.15,roic2=.12,wacc=.11,tg=.02,troic=.09,jv=3.8,netclaims=params['RCL']['netclaims']+.75),'base':params['RCL'],'bull':params['RCL']|dict(g1=.12,g2=.07,roic1=.30,roic2=.22,wacc=.09,tg=.03,troic=.15,jv=6.0,netclaims=params['RCL']['netclaims']-1)},'CCL':{'bear':params['CCL']|dict(ebit=3.8,tax=.04,g1=.02,g2=.02,roic1=.15,roic2=.12,wacc=.11,tg=.02,troic=.09),'base':params['CCL'],'bull':params['CCL']|dict(g1=.10,g2=.06,roic1=.30,roic2=.22,wacc=.09,tg=.03,troic=.15)}}
out={}
for n,sc in scenarios.items():
 out[n]={};print('\n',n,'floors',floors[n]);target=313.46 if n=='RCL' else 29.16
 for s,p in sc.items():
  r=dcf(**p);out[n][s]=dict(params=p,result=r);print(s,'price',round(r['price'],2),'vsprice',round(r['price']/target-1,3),'ev',round(r['ev'],2),'y1',round(r['years'][0]['fcff'],2),'y10',round(r['year10nopat'],2),'terminal share',round(r['terminal_percent'],3))
 p=sc['base'];print('WACC x perpetual g 2/2.5/3%; terminal ROIC12% fixed')
 for w in [.09,.1,.11]:print(w,[round(dcf(**(p|dict(wacc=w,tg=g)))['price'],2) for g in [.02,.025,.03]])
 print('Reverse constant NOPAT g for10y; incrementalROIC25% all10')
 for w in [.09,.10,.11]:
  lo,hi=0,.24
  for _ in range(100):
   g=(lo+hi)/2;r=dcf(**(p|dict(g1=g,g2=g,roic1=.25,roic2=.25,wacc=w)))
   if r['price']<target:lo=g
   else:hi=g
  print(w,round(g*100,2),round(r['price'],2),round(r['year10nopat'],2))
 lo,hi=0,20
 for _ in range(100):
  e=(lo+hi)/2;r=dcf(**(p|dict(ebit=e)))
  if r['price']<target:lo=e
  else:hi=e
 print('Reverse starting EBIT at base growth/return assumptions',round(e,2))
 print('Tax 5,10%',[(t,round(dcf(**(p|dict(tax=t)))['price'],2)) for t in [.05,.10]])
 print('ROIC 1-5/6-10',[(a,b,round(dcf(**(p|dict(roic1=a,roic2=b)))['price'],2)) for a,b in [(.15,.12),(.20,.15),(.25,.18),(.30,.22)]])
 print('Quarterly de-risking $1b reduction netdebt/share',round(1/p['shares'],2),'SBC flat share denominator10% dilution impact', round(dcf(**p)['price']/1.1,2))
open('cruise_commitments_scenarios.json','w').write(json.dumps(out,indent=2))
