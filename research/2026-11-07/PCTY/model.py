import pathlib,json,csv,math
P=pathlib.Path(__file__).parent;H=json.loads((P/'history.json').read_text());h=H['paired_ttm']['2026'];R0=h['recurring'];contract_amort=128.792+26.527-30.590
cash_margin=(h['ebit']-h['float_income']+h['da']+contract_amort)/R0
cfg={'stress':dict(g0=.07,g=.02,margin=.29,tax=.30,beta=1.5,yield_= .02,nwc=.06,post_cash=80,legal=50), 'central':dict(g0=.12,g=.025,margin=.33,tax=.28,beta=1.25,yield_=.03,nwc=.04,post_cash=60,legal=25), 'upside':dict(g0=.17,g=.03,margin=.37,tax=.26,beta=1,yield_=.04,nwc=.03,post_cash=40,legal=10)}
# Net carrying-stock/economic remaining-life convention, NOT the reported gross acquisition life.
stocks0={'physical':70.326,'software':149.942,'contracts':578.697,'acquired':83.425}
lives={'physical':4.5,'software':2.7,'contracts':5.4,'acquired':4.5}
floors={'physical':.012,'software':88.037/R0,'contracts':(177.130+46.038-41.210)/R0,'acquired':.012}
shares=51.963311+2.698

def run(c,gstart=None):
 c=dict(c);gstart=c['g0'] if gstart is None else gstart;w=.0486+c['beta']*.0441 # near-net-cash target unlevered financing, Ke=WACC
 R=R0;stocks=dict(stocks0);rows=[];pv=0
 for y in range(1,12):
  g=gstart+(c['g']-gstart)*min(y-1,9)/9;Rn=R*(1+g);m=cash_margin+(c['margin']-cash_margin)*min(y,5)/5
  # Three billion average client float is a modeling proxy, not ending client balance or free cash.
  float_income=3000*(Rn/R0)*c['yield_'];cap={};da={};new={}
  for k,S in stocks.items():
   L=lives[k];required=(S/L+g*S)/(1-.5/L)
   cap[k]=max(required,floors[k]*Rn);da[k]=S/L+.5*cap[k]/L;new[k]=S+cap[k]-da[k]
  ebit=m*Rn+float_income-sum(da.values());nopat=ebit*(1-c['tax']);dw=c['nwc']*(Rn-R);fcff=nopat+sum(da.values())-sum(cap.values())-dw
  rows.append(dict(year=y,growth=g,recurring_revenue=Rn,float_income=float_income,cash_margin=m,opening_stocks=stocks,investment=cap,amortization=da,closing_stocks=new,ebit=ebit,nopat=nopat,delta_wc=dw,fcff=fcff))
  if y<=10:pv+=fcff/(1+w)**y
  R=Rn;stocks=new
 # At year10, floor ratios/stock dynamics may not yet be stationary. Use explicit 1000-year funded tail, no abrupt Gordon switch.
 tail=0;last=rows[-1];tail+=last['fcff']/(1+w)**11
 for y in range(12,1011):
  Rn=R*(1+c['g']);cap={};da={};new={}
  for k,S in stocks.items():
   L=lives[k];cap[k]=max((S/L+c['g']*S)/(1-.5/L),floors[k]*Rn);da[k]=S/L+.5*cap[k]/L;new[k]=S+cap[k]-da[k]
  ebit=c['margin']*Rn+3000*(Rn/R0)*c['yield_']-sum(da.values());fcff=ebit*(1-c['tax'])+sum(da.values())-sum(cap.values())-c['nwc']*(Rn-R)
  tail+=fcff/(1+w)**y;R=Rn;stocks=new
 ev=pv+tail;bridge=194.523-75-131.250-10.722-.701-c['post_cash']-c['legal'];eq=ev+bridge
 return dict(assumptions=c,wacc=w,initial_cash_margin=cash_margin,ev=ev,equity=eq,conditional_per_share=eq/shares,pv_explicit=pv,pv_tail=tail,tail_share=tail/ev,bridge=bridge,diluted_proxy=shares,years=rows,approved_value=None)
res={k:run(c) for k,c in cfg.items()}
lo,hi=0,.6
for _ in range(70):
 mid=(lo+hi)/2
 if run(cfg['central'],mid)['conditional_per_share']<173.15:lo=mid
 else:hi=mid
out={'date':'2026-11-08','units':'USD millions except per share','cases':res,'inverse_central_initial_growth':(lo+hi)/2,'stock_lives':lives,'investment_floors':floors,'method':'Conditional FCFF with full expensed SBC retained, capitalized SBC cash-equivalent; dynamic DA and funded client acquisition/software/physical/IP stocks; 1000-year discounted funded tail','approved_values':None,'unresolved_claims':{'BIPA_appeal_loss':None,'postquarter_net_cash':None,'economic_customer_renewal_life':None,'acquired_IP_renewal_overlap_with_RD':None}}
(P/'model_results.json').write_text(json.dumps(out,indent=2));print({k:round(v['conditional_per_share'],2) for k,v in res.items()},out['inverse_central_initial_growth'])
