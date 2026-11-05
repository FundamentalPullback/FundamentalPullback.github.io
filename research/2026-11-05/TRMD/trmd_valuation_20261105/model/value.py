"""TRMD economic fleet FCFF. USD million unless USD/day or share noted.
Primary source data are preserved in adjacent input files. Analyst assumptions are explicit.
No trades, no publishing. Deterministic cohort model, not generic CAGR proxy.
"""
from pathlib import Path
from collections import Counter
import math,json,csv,copy,hashlib,itertools
from scipy.optimize import brentq
P=Path(__file__).resolve().parent; ROOT=P.parent
VAL=2026+307/365; BEGIN=2026.75; PRICE=37.64
CL=['MR','LR1','LR2']; OPEX={'MR':7680.,'LR1':7401.,'LR2':8752.}; COST={'MR':48.6,'LR1':60.,'LR2':75.}; DOCK={'MR':1.5,'LR1':1.8,'LR2':2.2}
# Fiscal bands published at Sep30 are spread uniformly across their 12 months.
COMMIT={2026:47.8+1.375,2027:143.4+20.075+4.375,2028:60.225+52.2+.75,2029:156.6+18.375,2030:55.125+13.75,2031:41.25}
fleet=json.loads((P/'fleet.json').read_text())
for v in fleet:v.update(built=v['built_year']+.5,delivery=BEGIN,committed=False)
for year,n in [(2027,4),(2028,2),(2029,6),(2030,2)]:
 for i in range(n):fleet.append(dict(name=f'MR contractual {year}-{i+1}',type='MR',built=year+.5,delivery=year+.5,committed=True,cost=(608.8+71)/14,source='Q3 report note10 plus presentation detailed delivery schedule'))
COMMON=dict(inflation=.02,life=25,wacc=.09,rate_scale=1.,cost_scale=1.,repair_days=5,dock_days=25,age_opex=.01,wc_pct=.22,cash_reserve=75.,ga=109.4,other_gross=5.8,incremental_ga=.20,tonnage_tax=3.,scrap=.10,shares=104.7,jv_net=0.,settlement_net=0.,financial_assets=25.7,claims=1150.3,normal={'MR':26000.,'LR1':28000.,'LR2':34000.},start={'MR':33000.,'LR1':36000.,'LR2':44000.},detailed_end={'MR':27500.,'LR1':29500.,'LR2':36000.},q4_tce=674.1,q4_ebitda=534.4,q4_drydock=20.,other_capex=4.)
CASES={
 'bear':dict(COMMON,life=20,wacc=.105,normal={'MR':20500.,'LR1':22500.,'LR2':27000.},start={'MR':26000.,'LR1':28000.,'LR2':34000.},detailed_end={'MR':21000.,'LR1':23000.,'LR2':28000.},cost_scale=1.15,repair_days=8,age_opex=.015,q4_tce=599.1,q4_ebitda=459.4,jv_net=-80.),
 'base':dict(COMMON),
 'bull':dict(COMMON,wacc=.08,normal={'MR':31000.,'LR1':34000.,'LR2':42000.},start={'MR':40000.,'LR1':44000.,'LR2':56000.},detailed_end={'MR':33000.,'LR1':36000.,'LR2':45000.},q4_tce=749.1,q4_ebitda=609.4,jv_net=60.)}
def inf(p,t):return (1+p['inflation'])**(t-2026)
def rates(p,y,c):
 if y<=2031:r=p['start'][c]+(p['detailed_end'][c]-p['start'][c])*(y-2027)/4
 else:r=p['detailed_end'][c]+(p['normal'][c]-p['detailed_end'][c])*min(1,(y-2031)/5)
 return r*p['rate_scale']*inf(p,y+.5)
def docks(L):return [5,10,15]+list(range(17,L,2))
def newbuild(p,c,discount=None):
 """Unlevered cash NPV at ordering, with20/20/60 payments and two years to delivery.
 Cost is expressed in delivery-date nominal USD; inflation across working life is retained.
 This gate tests new incremental vessels, not existing sunk assets or binding contracts.
 """
 w=p['wacc'] if discount is None else discount;L=p['life'];price=COST[c]*p['cost_scale'];s=p['scrap'];wc=p['normal'][c]*p['rate_scale']*(365-p['repair_days']-p['dock_days']*len(docks(L))/L)/1e6*p['wc_pct']+p['cash_reserve']/95
 vals=[(0,-.2*price),(1,-.2*price),(2,-.6*price-wc)]
 for a in range(L):
  scale=(1+p['inflation'])**(a+.5);is_dock=any(a<=d<a+1 for d in docks(L));days=365-p['repair_days']-p['dock_days']*is_dock
  rev=p['normal'][c]*p['rate_scale']*scale*days/1e6;ox=OPEX[c]*scale*365*(1+p['age_opex']*max(a+.5-15,0))/1e6
  maint=DOCK[c]*(1.25 if a>=15 else 1)*scale*p['cost_scale']*is_dock
  cf=rev-ox-p['incremental_ga']*scale-p['tonnage_tax']/95*scale-maint-wc*p['inflation']*(1+p['inflation'])**a
  vals.append((2+a+.5,cf))
 vals.append((2+L,COST[c]*s*(1+p['inflation'])**L+wc*(1+p['inflation'])**L))
 npv=sum(cf/(1+w)**t for t,cf in vals)
 try:irr=brentq(lambda r:sum(cf/(1+r)**t for t,cf in vals),-.05,.50)
 except ValueError:irr=None
 return {'npv_at_order':npv,'irr':irr,'renew':npv>=0,'purchase_price_delivery_basis':price}
def periods(v,p,allow):
 b=v['built'];first=True
 while b<2200:
  yield (max(v['delivery'],b),b+p['life'],b,first)
  if not allow:break
  b+=p['life'];first=False

def run(p,full=False,policy='economic',last=2186):
 if policy=='economic':
  candidates=[run(p,full,dict(zip(CL,flags)),last) for flags in itertools.product([False,True],repeat=3)]
  best=max(candidates,key=lambda z:z['equity']);best['policy']='economic_optimal_8_class_combinations';best['policy_alternatives']=[dict(renewal=x['renewal'],value=x['per_share']) for x in candidates];return best
 p=copy.deepcopy(p); w=p['wacc'];L=p['life'];g=p['inflation'];gates={c:newbuild(p,c) for c in CL}
 renewal=policy if isinstance(policy,dict) else {c:policy=='renew' for c in CL}
 rows={y:dict(year=y,phase='stub' if y==2026 else 'detailed' if y<=2031 else 'transition' if y<=2036 else 'terminal_cohorts',tce=0.,opex=0.,hull_da=0.,drydock=0.,replacement=0.,scrap=0.,owner_days=0.,revenue_days=0.,retired=0.,new_replacement=0.,committed=COMMIT.get(y,0.),counts={c:0. for c in CL},byclass={c:dict(tce=0.,opex=0.,revenue_days=0.) for c in CL}) for y in range(2026,last+1)}
 initialweights={v['name']:COST[v['type']]*(.1+.9*max(0,(v['built']+25-BEGIN))/25) for v in fleet if not v['committed']}
 weights=sum(initialweights.values())
 for v in fleet:
  c=v['type'];segs=list(periods(v,p,renewal[c]))
  for a,b,built,first in segs:
   if a>=last+1:break
   # Existing asset book is allocated only for EBIT presentation; tonnage tax does not depend on EBIT.
   if first and not v['committed']:
    bv=2723.2*initialweights[v['name']]/weights;salv=COST[c]*p['scrap'];da=max(0,bv-salv)/max(.25,b-BEGIN)
   else: da=((v['cost'] if first else COST[c]*p['cost_scale']*inf(p,built))*(1-p['scrap']))/L
   for y in range(max(2026,int(a)),min(last+1,math.ceil(b))):
    start=max(BEGIN if y==2026 else y,a);end=min(y+1,b)
    if end<=start:continue
    r=rows[y];dur=end-start;mid=(start+end)/2;age=mid-built;od=dur*365
    de=[built+d for d in docks(L) if start<=built+d<end]
    dc=sum(DOCK[c]*(1.25 if d-built>=15 else 1)*inf(p,d)*p['cost_scale'] for d in de)
    rd=max(0,od-p['repair_days']*dur-p['dock_days']*len(de))
    rev=rates(p,y,c)*rd/1e6 if y!=2026 else 0.
    ox=OPEX[c]*inf(p,mid)*(1+p['age_opex']*max(0,age-15))*od/1e6
    r['tce']+=rev;r['opex']+=ox;r['hull_da']+=da*dur;r['drydock']+=dc;r['owner_days']+=od;r['revenue_days']+=rd;r['counts'][c]+=dur
    r['byclass'][c]['tce']+=rev;r['byclass'][c]['opex']+=ox;r['byclass'][c]['revenue_days']+=rd
   # Economic retirement of each vintage; future replacement is paid only if its NPV is positive.
   y=int(b)
   if 2026<=y<=last:rows[y]['scrap']+=COST[c]*p['scrap']*inf(p,b);rows[y]['retired']+=1
   if renewal[c]:
    purchase=COST[c]*p['cost_scale']*inf(p,b)
    for date,share in [(b-2,.2),(b-1,.2),(b,.6)]:
     # Hypothetical renewal prepays before the matched balance were NOT already funded. Charge them at the cut-off.
     cashdate=max(date,BEGIN)
     if int(cashdate)<=last:rows[int(cashdate)]['replacement']+=share*purchase
    if 2026<=y<=last:rows[y]['new_replacement']+=1
 # Opening operating WC excludes all derivatives; 17.7 financial hedge FV goes in bridge.
 # Operating FFA/bunker FV3.4 is not also added: Q4 TCE guidance includes FFAs.
 prevwc=300.5+p['cash_reserve'];out=[]
 for y,r in rows.items():
  start=BEGIN if y==2026 else y;dur=y+1-start;mid=(start+y+1)/2;count=r['owner_days']/365/dur;scale=inf(p,mid)
  full_count=95+sum(1 for v in fleet if v['committed'] and v['delivery']<=mid)
  ratio=min(1,count/max(1,full_count))
  ga=(p['ga']+p['incremental_ga']*max(0,full_count-95))*scale*dur*ratio
  other=p['other_gross']*scale*dur*ratio
  tax=p['tonnage_tax']*scale*dur*count/95
  if y==2026:r['tce']=p['q4_tce'];ebitda=p['q4_ebitda'];ga=r['tce']-r['opex']+other-ebitda
  else:ebitda=r['tce']-r['opex']-ga+other
  if y==2026:r['drydock']=p['q4_drydock']
  other_capex=p['other_capex']*scale*dur*ratio
  # Recurring maintenance component shown in D&A at current maintenance equivalent.
  da=r['hull_da']+r['drydock']+other_capex;ebit=ebitda-da;nopat=ebit-tax
  annualrev=r['tce']/dur;reserve=p['cash_reserve']*count/95*inf(p,y+1);nwc=annualrev*p['wc_pct']+reserve;dnwc=nwc-prevwc;prevwc=nwc
  runoff_tax=0.
  # Non-renewed classes have no indefinite held-over-tax deferral: prorata charge on their final retirement.
  for c in CL:
   if not renewal[c]:
    lastret=max(v['built']+L for v in fleet if v['type']==c)
    if y<=lastret<y+1:runoff_tax+=45.2*sum(v['type']==c and not v['committed'] for v in fleet)/95
  fcff=nopat+da-r['drydock']-r['replacement']+r['scrap']-r['committed']-dnwc-runoff_tax-other_capex
  r.update(other_capex=other_capex,avg_fleet=count,ga=ga,other_gross=other,ebitda=ebitda,da=da,ebit=ebit,tax=tax,nopat=nopat,nwc=nwc,dnwc=dnwc,fcff=fcff,pv=fcff/(1+w)**(mid-VAL),period_mid=mid,runoff_tax=runoff_tax);out.append(r)
 explicit=sum(r['pv'] for r in out if r['year']<=2036);tail=sum(r['pv'] for r in out if r['year']>2036)
 steady=terminal(p,renewal)
 gordonpv=steady['fcff']/(w-g)/(1+w)**(2036.5-VAL) if steady['fcff'] else 0.
 # Exact cohort tail minus uniform replacement steady state; separate from Gordon, never year10 carry-forward.
 ageadj=tail-gordonpv
 ev=explicit+tail;cash=446.2-p['cash_reserve'];equity=ev+cash+p['financial_assets']-p['claims']+p['jv_net']+p['settlement_net'];per=equity/p['shares']
 return dict(case=p.get('case',''),assumptions=p,policy=policy,renewal_gate=gates,renewal=renewal,rows=out if full else out[:11],operating_ev=ev,explicit_pv=explicit,tail_pv=tail,terminal_weight=tail/ev if ev else None,gordon_pv=gordonpv,age_adjustment_pv=ageadj,terminal=steady,equity=equity,per_share=per,upside=per/PRICE-1,mos=(per-PRICE)/per,bridge=dict(cash=446.2,cash_reserve=p['cash_reserve'],cash_excess=cash,claims=p['claims'],loan_receivable=4.4,other_investments=3.6,financial_hedges=17.7,jv_net=p['jv_net'],settlement_net=p['settlement_net'],shares=p['shares']))

def terminal(p,renewal):
 L=p['life'];g=p['inflation'];w=p['wacc'];t=2037;scale=inf(p,t);counts=Counter(v['type'] for v in fleet if renewal[v['type']]);N=sum(counts.values())
 if not N:return dict(year=t,counts={},fcff=0.,nopat=0.,economic_nopat=0.,capital_prior=0.,roic=None,formula_fcff=0.,g=g)
 events=docks(L);days=365-p['repair_days']-p['dock_days']*len(events)/L
 rev=sum(n*p['normal'][c]*p['rate_scale']*scale*days/1e6 for c,n in counts.items())
 ox=sum(n*OPEX[c]*scale*365*(1+p['age_opex']*max(L-15,0)**2/(2*L))/1e6 for c,n in counts.items())
 ga=(p['ga']+p['incremental_ga']*14)*scale*N/109;other=p['other_gross']*scale*N/109
 dock=sum(n*DOCK[c]*scale*p['cost_scale']*sum(1.25 if d>=15 else 1 for d in events)/L for c,n in counts.items())
 C=sum(n*COST[c]*scale*p['cost_scale'] for c,n in counts.items());gross=C/L;s=p['scrap']/p['cost_scale'];scrap=s*C/L
 # Annual replacement payments are advanced20% two years and20% one year before delivery.
 # Stable capital includes construction-in-progress at previous year end, separately derived.
 advancefactor=.6+.2*(1+g)+.2*(1+g)**2;capex=gross*advancefactor
 Khull=sum(C/L/(1+g)**j*(1-(1-s)*(j-1)/L) for j in range(1,L+1))
 Kcip=(.4+.2*(1+g))*gross
 da=sum((1-s)/L*C/L/(1+g)**j for j in range(1,L+1));retiredbook=s*C/L/(1+g)**L;scrapgain=scrap-retiredbook
 reserve=p['cash_reserve']*N/95*inf(p,t+1);nwc=rev*p['wc_pct']+reserve;Kwc=nwc/(1+g);K=Khull+Kcip+Kwc
 tax=p['tonnage_tax']*scale*N/95
 # Drydocks treated as recurring economic maintenance expense in sustainable EBIT, no fictitious benefit.
 other_maintenance=p['other_capex']*scale*N/109
 ebit=rev-ox-ga+other-dock-da-other_maintenance;nopat=ebit-tax;econ_nopat=nopat+scrapgain;netreinv=capex-scrap-da+nwc*g/(1+g)
 fcff=nopat-netreinv;roic=econ_nopat/K;formula=econ_nopat*(1-g/roic)
 return dict(year=t,counts=dict(counts),rev=rev,opex=ox,ga=ga,other_gross=other,maintenance_drydock=dock,other_maintenance=other_maintenance,gross_replacement=gross,advanced_cash_capex=capex,scrap=scrap,da=da,retired_book=retiredbook,scrap_gain=scrapgain,nopat=nopat,economic_nopat=econ_nopat,net_reinvestment=netreinv,nwc=nwc,hull_capital_prior=Khull,construction_capital_prior=Kcip,wc_capital_prior=Kwc,capital_prior=K,roic=roic,economic_reinvestment=g*K,fcff=fcff,formula_fcff=formula,g=g)

if __name__=='__main__':
 results={}
 for k,p in CASES.items():p['case']=k;results[k]=run(p,True);r=results[k];print(k,r['per_share'],r['operating_ev'],r['terminal']['roic'],r['renewal'], 'terminal identity',r['terminal']['fcff']-r['terminal']['formula_fcff'])
 (P/'assumptions.json').write_text(json.dumps(CASES,indent=2));(P/'results.json').write_text(json.dumps(results,indent=2));(P/'modeled_fleet.json').write_text(json.dumps(fleet,indent=2))
 for k,r in results.items():
  with (P/f'{k}_annual.csv').open('w') as f:
   fields=[a for a in r['rows'][0] if a not in ('counts','byclass')];o=csv.DictWriter(f,fieldnames=fields);o.writeheader();o.writerows({a:v for a,v in row.items() if a in fields} for row in r['rows'])
