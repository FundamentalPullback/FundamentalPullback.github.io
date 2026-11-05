from pathlib import Path
from collections import Counter
import json, csv, math, copy, hashlib
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent.parent
CLASSES=['Handymax','MR','LR2','VLCC']; VAL=2026+307/365.25; BEGIN=2027-92/365.25
RATE0={'Handymax':8058,'MR':8383,'LR2':9433,'VLCC':12000}
PRICE0={'Handymax':35.,'MR':46.33,'LR2':72.8,'VLCC':135.}
DOCK0={'Handymax':1.2,'MR':1.5,'LR2':2.2,'VLCC':3.5}
CHARTERS={
'STI Battersea':(2025.25,2027.25,24000), 'STI Bronx':(2026+11/12,2029+11/12,23900), 'STI Pontiac':(2026+11/12,2029+11/12,23900),
'STI Notting Hill':(2026+11/12,2029+11/12,25000),'STI Westminster':(2026+11/12,2029+11/12,25000),
'STI Bosphorus':(2025+7/12,2037.5,13150),'STI Jardins':(2024.75,2027.75,29550),'STI Orchard':(2025+7/12,2030+7/12,28350),
'STI Rose':(2026+1/12,2031+1/12,29000),'STI Alexis':(2026.,2031.,29000),'STI Spiga':(2025+10/12,2026+10/12,35000),
'STI Lombard':(2026+2/12,2031+2/12,33000),'STI Grace':(2025+11/12,2026+11/12,36000),
'STI Jermyn':(2026.75,2029.75,42500),'STI Guard':(2022.5,2027.5,28000),'STI Guide':(2026.5,2027.5,33000),
'STI Rambla':(2026+2/12,2034+2/12,30500),'STI Gauntlet':(2025+10/12,2026+10/12,36000),'STI Gladiator':(2026+8/12,2029+8/12,40188)}
fleet=[]
for l in (ROOT/'sources/primary_archive/q3_table_12.txt').read_text().splitlines():
 p=[x.strip() for x in l.split('|') if x.strip()]
 if p and p[0].isdigit():
  n,name,year,dwt,ice,em,cl,sc=p[:8];fleet.append(dict(name=name,built=float(year)+.5,delivery=float(year)+.5,type=cl,dwt=int(dwt.replace(',','')),cost=PRICE0[cl]/1.02**(2026-int(year)),source='Q3 fleet table 12',sale=2026+10.5/12 if name in ['STI Elysees','STI Veneto'] else None))
# Quarter midpoint delivery assumptions within issuer windows; exact delivery days are not company guidance.
new=[('YZJF2024-002','MR',2027.125,45,49800),('YZJF2024-003','MR',2027.375,45,49800),('YZJF2024-004','MR',2027.375,45,49800),('YZJ2026-1869','MR',2030.125,46.33,50000),('YZJ2026-1870','MR',2030.125,46.33,50000),('P110K-102','LR2',2027.625,70.8,115000),('P110K-103','LR2',2027.625,70.8,115000),('P110K-104','LR2',2029.625,68.5,115000),('P110K-105','LR2',2029.875,68.5,115000),('HT-OT114-672','LR2',2029.375,72.8,114000),('HT-OT114-673','LR2',2029.625,72.8,114000),('HT-OT114-674','LR2',2029+9.5/12,72.8,114000),('HT-OT114-675','LR2',2029+10.5/12,72.8,114000),('5540','VLCC',2028.625,128,300000),('5541','VLCC',2028.875,128,300000),('HL-T300K-121','VLCC',2028.625,135,306000),('HL-T300K-123','VLCC',2028.875,135,306000)]
for n,c,d,p,dwt in new:fleet.append(dict(name='Hull '+n,built=d,delivery=d,type=c,cost=p,dwt=dwt,source='Q3 fleet tables 13-14 / purchase announcements',sale=None))
COMMIT={2026:45.6,2027:298.2,2028:481.9,2029:379.2,2030:91.0}
# Intentionally all disclosed combined payments deducted once. New VLCC JV future economics not invented.
# Separate valuation increment stress gives the shareholder value of that omitted interest at as-of date.
COMMON=dict(inflation=.02,life=25,fade_years=2,scrap=.10,wc_pct=.15,cash_reserve=125,cash_ga=69.936,sbc=78.0,ga_per_new=.20,repair_days=5,age_opex=.01,replacement_premium=1.,tax=0.,rate_scale=1.,wacc=.10,jv_value=0.,ampera=6.002,dual_jv=11.323,volare=2.4*164.6/9.2278,claims=718.621,additional_shares=0.,pool_capital=39.644)
CASES={
 'bear':dict(COMMON,normal={'Handymax':17000,'MR':21000,'LR2':27000,'VLCC':38000},start={'Handymax':22000,'MR':29000,'LR2':45000,'VLCC':55000},wacc=.115,life=20,fade_years=1,tax=.02,replacement_premium=1.15,repair_days=8,age_opex=.015,ampera=0.,dual_jv=7.9261,volare=COMMON['volare']*.8),
 'base':dict(COMMON,normal={'Handymax':21000,'MR':27000,'LR2':35000,'VLCC':45000},start={'Handymax':28000,'MR':38000,'LR2':65000,'VLCC':70000}),
 'bull':dict(COMMON,normal={'Handymax':25000,'MR':33000,'LR2':45000,'VLCC':60000},start={'Handymax':34000,'MR':47000,'LR2':85000,'VLCC':90000},wacc=.09,fade_years=4,replacement_premium=.95,ampera=12.004)}
# End of year economic working capital. Cash operating reserve excluded from equity cash addback.
def inflate(p,y):return (1+p['inflation'])**(y-2026)
def dateship(v,p,start,end,renew=True):
 # Ownership segments with actual cohort replacement. Replacement once at assumed life; same-day handover.
 if v['delivery']>=end:return []
 last=min(end,v['sale'] or end)
 if last<=start:return []
 built=v['built']; cost=v['cost']; out=[]
 while built+p['life']<=start:
  if not renew:return []
  built+=p['life'];cost=PRICE0[v['type']]*inflate(p,built)*p['replacement_premium']
 while built<last:
  segstart=max(start,built,v['delivery']);segend=min(last,built+p['life'])
  if segend>segstart:out.append((segstart,segend,built,cost))
  if built+p['life']>=last or not renew:break
  built+=p['life'];cost=PRICE0[v['type']]*inflate(p,built)*p['replacement_premium']
 return out

def operating(year,p,renew=True):
 start=BEGIN if year==2026 else year;end=year+1;dur=end-start;mid=(start+end)/2
 rev=op=da=dry=days=owner=tc_days=spot_days=bare_days=repl=salv=0.;counts=Counter();byclass={x:dict(tce=0,owner_days=0,revenue_days=0,opex=0,da=0) for x in CLASSES}
 for v in fleet:
  cl=v['type'];segs=dateship(v,p,start,end,renew)
  for a,b,built,cost in segs:
   frac=b-a;od=frac*365.25;age=(a+b)/2-built
   # Aging cost increment starts only above age 15; no double technical-management fee.
   ox=RATE0[cl]*inflate(p,mid)*(1+p['age_opex']*max(age-15,0))*od/1e6
   dock_ages=[5,10,15]+[17.5+2.5*i for i in range(20) if 17.5+2.5*i<p['life']]
   de=[built+x for x in dock_ages if a<=built+x<b]
   dc=sum(DOCK0[cl]*(1.25 if d-built>=15 else 1)*inflate(p,d)*p['replacement_premium'] for d in de)
   off=p['repair_days']*frac+25*len(de)
   if year==2027:off=543*od/sum(sum((z[1]-z[0])*365.25 for z in dateship(w,p,year,year+1,renew)) for w in fleet)
   if year==2026:off=212*od/sum(sum((z[1]-z[0])*365.25 for z in dateship(w,p,start,end,renew)) for w in fleet)
   rd=max(0,od-off)
   charter=CHARTERS.get(v['name']) if built==v['built'] else None
   cf=max(0,min(b,charter[1])-max(a,charter[0]))/frac if charter else 0
   isbare=v['name']=='STI Bosphorus' and cf>0
   # Fixed gross charter less 1.25% commission and commercial daily fee; bareboat published net 12,986.
   if charter: fixed=12986 if isbare else charter[2]*(1-.0125)-(285 if cl=='LR2' else 335)
   else:fixed=0
   if year==2026:
    unfixed={'bear':{'LR2':40000,'MR':22000,'Handymax':17000},'base':{'LR2':72283,'MR':31183,'Handymax':24253},'bull':{'LR2':181000,'MR':56000,'Handymax':40000}}[p.get('case','base')]
    coverage={'LR2':.44,'MR':.47,'Handymax':.37};booked={'LR2':181000,'MR':56000,'Handymax':40000}
    spot=coverage[cl]*booked[cl]+(1-coverage[cl])*unfixed[cl]
   else:
    # Base normalizes by 2029; bear by2028, bull by2031. Transition years preserve real rates but age/replacement still changes costs.
    w=max(0,1-(year-2027)/p['fade_years'])
    spot=(p['normal'][cl]*p['rate_scale']*(1-w)+p['start'][cl]*w)*inflate(p,year)
   r=rd*(cf*fixed+(1-cf)*spot)/1e6
   if isbare:ox*=1-cf;dc*=1-cf;bare_days+=rd*cf
   tc_days+=rd*cf*(not isbare);spot_days+=rd*(1-cf)
   dd=cost*(1-p['scrap'])/p['life']*frac
   # Recurring drydock depreciation proxy cancels the cash-flow addback. Tax sensitivity only.
   dd+=DOCK0[cl]/3.75*inflate(p,mid)*frac*(1-cf*isbare)
   rev+=r;op+=ox;da+=dd;dry+=dc;days+=rd;owner+=od;counts[cl]+=frac
   bc=byclass[cl];bc['tce']+=r;bc['owner_days']+=od;bc['revenue_days']+=rd;bc['opex']+=ox;bc['da']+=dd
   if built>v['built'] and start<=built<end:
    repl+=PRICE0[cl]*inflate(p,built)*p['replacement_premium'];salv+=PRICE0[cl]*inflate(p,built)*p['scrap']
  if not renew:
   retirement=v['built']+p['life']
   if start<=retirement<end and not v['sale']:salv+=PRICE0[cl]*inflate(p,retirement)*p['scrap']
 # Complete Q4 revenue-day guidance is more precise than inferred charter start/sale dates.
 # Rates are already reported net TCE. Coverage applies to these full-quarter spot days.
 if year==2026:
  q4days={'LR2':(1025,1025,0),'MR':(2919,154,91),'Handymax':(1183,91,0)}
  q4tc={'LR2':32150,'MR':26100,'Handymax':23000}
  rev=days=tc_days=spot_days=bare_days=0.
  for cl,(sd,td,bd) in q4days.items():
   qrate=coverage[cl]*booked[cl]+(1-coverage[cl])*unfixed[cl]
   qrev=(sd*qrate+td*q4tc[cl]+bd*12986)/1e6
   rev+=qrev;days+=sd+td+bd;spot_days+=sd;tc_days+=td;bare_days+=bd
   byclass[cl]['tce']=qrev;byclass[cl]['revenue_days']=sd+td+bd
 avg_count=owner/365.25/dur
 if year==2027:dry=19.6
 if year==2026:dry=11.3
 ga=(p['cash_ga']+p['sbc']+p['ga_per_new']*max(avg_count-72,0))*inflate(p,mid)*dur
 if not renew:
  full_count=sum(sum(z[1]-z[0] for z in dateship(v,p,start,end,True)) for v in fleet)/dur
  ga*=min(1,avg_count/full_count) if full_count else 0 # No overhead benefit until actual retirement; proportional decline remains a sensitivity.
 ebitda=rev-op-ga;ebit=ebitda-da;tax=max(0,ebit)*p['tax'];nopat=ebit-tax
 return dict(year=year,phase='stub' if year==2026 else 'detailed' if year<=2031 else 'transition' if year<=2036 else 'renewal_tail',tce=rev,opex=op,ga=ga,sbc=p['sbc']*inflate(p,mid)*dur,ebitda=ebitda,da=da,ebit=ebit,tax=tax,nopat=nopat,drydock=dry,replacement=repl,scrap=salv,committed=COMMIT.get(year,0.),owner_days=owner,revenue_days=days,time_charter_days=tc_days,spot_days=spot_days,bareboat_days=bare_days,avg_fleet=avg_count,counts=dict(counts),byclass=byclass,period_mid=mid)

def run(p,full=False,renew=True):
 p=copy.deepcopy(p); w=p['wacc']; g=p['inflation'];yearend=2196 if renew else 2061
 rows=[];opening_nwc=229.759+10.337+6.978-30.255-84.123+p['pool_capital']+p['cash_reserve'];prevnwc=opening_nwc
 for year in range(2026,yearend+1):
  row=operating(year,p,renew)
  # Annualize stub TCE only to estimate quarter-end receivables, not long-run operating income.
  runrev=row['tce']/(1-BEGIN%1) if year==2026 else row['tce']
  reserve=p['cash_reserve']*(row['avg_fleet']/74)*inflate(p,year+1)
  nwc=runrev*p['wc_pct']+reserve
  row.update(nwc=nwc,dnwc=nwc-prevnwc);prevnwc=nwc
  row['fcff']=row['nopat']+row['da']-row['drydock']-row['replacement']+row['scrap']-row['committed']-row['dnwc']
  row['pv']=row['fcff']/(1+w)**(row['period_mid']-VAL);rows.append(row)
 # Net pending sales (gross143 less1% fees), offset by stopping their operations at assumed15Nov26.
 sales_pv=143*.99/(1+w)**(2026+11/12-VAL)
 explicit_pv=sum(r['pv'] for r in rows if r['year']<=2036)
 tail_pv=sum(r['pv'] for r in rows if r['year']>2036)
 # Gordon steady-state: uniform cohort ages. Historical-cost depreciation of net reinvestment correctly embeds inflation.
 count=Counter(v['type'] for v in fleet if not v['sale']);L=p['life'];t=2037;scale=inflate(p,t)
 steady_rev=sum(n*p['normal'][c]*p['rate_scale']*scale*(365.25-p['repair_days']-25*(3+max(0,int((L-15)/2.5)-1))/L) for c,n in count.items())/1e6
 # Average age surcharge, averaged continuously over a stable age distribution.
 steady_opex=sum(n*RATE0[c]*scale*365.25*(1+p['age_opex']*max(L-15,0)**2/(2*L)) for c,n in count.items())/1e6
 steady_ga=(p['cash_ga']+p['sbc']+p['ga_per_new']*17)*scale
 events=[5,10,15]+[17.5+2.5*i for i in range(20) if 17.5+2.5*i<L]
 steady_dry=sum(n*DOCK0[c]*scale*sum(1.25 if a>=15 else 1 for a in events)/L*p['replacement_premium'] for c,n in count.items())
 gross_repl=sum(n*PRICE0[c]*scale*p['replacement_premium']/L for c,n in count.items())
 scrap=sum(n*PRICE0[c]*scale*p['scrap']/L for c,n in count.items()); net_repl=gross_repl-scrap
 # Stable end-of-year capital at t-1 inferred from a full 25/20-year historical-cost replacement cycle; not g/ROIC chosen independently.
 hull_da=net_repl*sum((1+g)**(-a) for a in range(L))/L
 # Include recurring drydock maintenance in D&A; it cancels against cash drydock when computing net reinvestment.
 steady_da=hull_da+steady_dry
 steady_ebit=steady_rev-steady_opex-steady_ga-steady_da;steady_nopat=steady_ebit-max(0,steady_ebit)*p['tax']
 steady_nwc=steady_rev*p['wc_pct']+p['cash_reserve']*(89/74)*inflate(p,t+1)
 net_reinvest=net_repl-hull_da+steady_nwc*g/(1+g)
 steady_fcff=steady_nopat-net_reinvest
 # Independent vintage-by-vintage capital roll-forward, not capital inferred as reinvestment/g.
 C=sum(n*PRICE0[c]*scale*p['replacement_premium'] for c,n in count.items())
 # Scrap proceeds reflect current prices; historical residual book value is smaller.
 s_eff=scrap/gross_repl if gross_repl else 0
 hull_capital_prior=sum(C/(1+g)**j/L*(1-(1-s_eff)*(j+1)/L) for j in range(L))/(1+g)
 retired_book=s_eff*C/(1+g)**L/L
 ordinary_scrap_gain=scrap-retired_book
 capital_prior=hull_capital_prior+steady_nwc/(1+g)
 economic_nopat=steady_nopat+ordinary_scrap_gain
 economic_reinvestment=g*capital_prior
 roic=economic_nopat/capital_prior if capital_prior else None
 # Midyear discounting of perpetuity streams: Gordon at2036.5, while explicit last midpoint is2036.5.
 gordon_at2036_5=steady_fcff/(w-g)
 gordon_pv=gordon_at2036_5/(1+w)**(2036.5-VAL)
 # This adjustment is the PV of the actual known age profile minus stable replacement/cost assumptions.
 age_adjustment=tail_pv-gordon_pv
 op_ev=explicit_pv+tail_pv
 investments=p['volare']+p['ampera']+p['dual_jv']+p['jv_value']
 # Matched September30 balance sheet plus full Q4 forecast. October Volare purchase is not in Sep30 cash.
 volare_purchase_pv=38.4/(1+w)**(2026+9.5/12-VAL)
 assets=op_ev+sales_pv+2042.088-p['cash_reserve']+investments-volare_purchase_pv
 shares=51.078851+p['additional_shares'];equity=assets-p['claims'];per=equity/shares
 par=(assets-655)/shares;conversion=(assets-50)/(shares+6.0978555);par_convert=min(par,conversion) if par>99.215207 else par
 return dict(case=p.get('case',''),assumptions=p,rows=rows if full else rows[:11],operating_ev=op_ev,explicit_pv=explicit_pv,tail_pv=tail_pv,gordon_pv=gordon_pv,age_adjustment_pv=age_adjustment,terminal_weight=tail_pv/op_ev if op_ev else None,gordon=dict(year=2037,rev=steady_rev,opex=steady_opex,ga=steady_ga,drydock=steady_dry,net_replacement=net_repl,da=steady_da,nopat=steady_nopat,nwc=steady_nwc,net_reinvestment=net_reinvest,capital_prior=capital_prior,hull_capital_prior=hull_capital_prior,retired_book=retired_book,ordinary_scrap_gain=ordinary_scrap_gain,economic_nopat=economic_nopat,economic_reinvestment=economic_reinvestment,roic=roic,fcff=steady_fcff,g=g,formula_fcff=economic_nopat*(1-g/roic) if roic else None),bridge=dict(cash_reported=2042.088,cash_date='2026-09-30',latest_cash_crosscheck_20261026=2051.865,operating_cash_reserved=p['cash_reserve'],cash_excess=2042.088-p['cash_reserve'],post_balance_volare_purchase_pv=volare_purchase_pv,pending_sales_pv=sales_pv,volare=p['volare'],ampera=p['ampera'],dual_jv=p['dual_jv'],new_jv_increment=p['jv_value'],investments=investments,claims=p['claims'],shares=shares),equity=equity,per_share=per,par_conversion_equivalent=par_convert,par_only=par,physical_conversion=conversion,upside=per/85.05-1,renew=renew)

if __name__=='__main__':
 results={}
 for k,p in CASES.items():p['case']=k;results[k]=run(p,True)
 (ROOT/'model/fleet.json').write_text(json.dumps(fleet,indent=2))
 (ROOT/'model/assumptions.json').write_text(json.dumps(CASES,indent=2))
 (ROOT/'model/results.json').write_text(json.dumps(results,indent=2))
 for k,r in results.items():
  with (ROOT/f'model/{k}_annual.csv').open('w') as f:
   fields=[x for x in r['rows'][0] if x not in ['counts','byclass']];out=csv.DictWriter(f,fieldnames=fields);out.writeheader();out.writerows({x:v for x,v in row.items() if x in fields} for row in r['rows'])
  print(k,'value',r['per_share'],'EV',r['operating_ev'],'TV%',r['terminal_weight'],'ROIC',r['gordon']['roic'],'ageadj',r['age_adjustment_pv'])
