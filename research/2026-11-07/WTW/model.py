import pathlib,json
P=pathlib.Path(__file__).parent;H=json.loads((P/'history.json').read_text());h=H['paired_ttm']['2026'];R0=h['revenue']-49-143
# Remove 49 book settlements, 143 interest in revenues, 13 building gain; reverse 14 noncash impairment. No SBC/program addback.
M0=(h['ebit']-49-143-13+14+h['depreciation']+h['amortization'])/R0
S0={'fixed_and_internal_software':665.,'client_relationships':724.,'acquired_software':94.,'trade_names_other':613.}
L={'fixed_and_internal_software':3.5,'client_relationships':5.5,'acquired_software':5.,'trade_names_other':12.}
floor={'fixed_and_internal_software':.024,'client_relationships':.015,'acquired_software':.003,'trade_names_other':.004}
CFG={'stress':dict(g0=.035,g=.02,margin=.255,beta=1.2,tax=.25,float_income=95.,wc=.18,legal_extra=150.,post_cash=75.),'central':dict(g0=.065,g=.025,margin=.28,beta=1.,tax=.23,float_income=125.,wc=.15,legal_extra=75.,post_cash=40.),'upside':dict(g0=.09,g=.03,margin=.305,beta=.8,tax=.21,float_income=155.,wc=.12,legal_extra=25.,post_cash=20.)}
def run(c,g0=None):
 g0=c['g0'] if g0 is None else g0;ke=.0486+c['beta']*.0441;w=.85*ke+.15*.055*(1-c['tax']);R=R0;S=dict(S0);pv=tail=0;rows=[]
 for y in range(1,1011):
  g=g0+(c['g']-g0)*min(y-1,9)/9;Rn=R*(1+g);m=M0+(c['margin']-M0)*min(y,5)/5;I={};D={};Sn={}
  for k,s in S.items():
   I[k]=max((s/L[k]+g*s)/(1-.5/L[k]),floor[k]*Rn);D[k]=(s+.5*I[k])/L[k];Sn[k]=s+I[k]-D[k]
  transformation=[240.,240.,138.][y-1] if y<=3 else 0.
  interest=c['float_income']*(Rn/R0);ebit=m*Rn+interest-sum(D.values())-transformation;nopat=ebit*(1-c['tax']);dw=c['wc']*(Rn-R);fcf=nopat+sum(D.values())-sum(I.values())-dw
  if y<=10:pv+=fcf/(1+w)**y
  else:tail+=fcf/(1+w)**y
  if y<=11:rows.append(dict(year=y,g=g,revenue_core=Rn,cash_margin=m,interest_revenue=interest,stock_open=S,investment=I,da=D,stock_close=Sn,propel_cash_cost=transformation,ebit=ebit,nopat=nopat,delta_wc=dw,fcff=fcf))
  S=Sn;R=Rn
 nci=15*(1+c['g'])/(ke-c['g']);bridge=1946-750-6532-583-368-73-108-32-89-102-c['post_cash']-c['legal_extra']-nci
 ev=pv+tail;eq=ev+bridge;shares=92.216232+1.561
 return {'assumptions':c,'ke':ke,'wacc':w,'ev_core_conditional':ev,'equity_residual_ex_unvalued_interests':eq,'per_share_residual_conditional':eq/shares,'bridge':bridge,'nci_income_proxy':nci,'shares_proxy':shares,'pv_explicit':pv,'pv_tail':tail,'tail_share':tail/ev,'years':rows,'approved_value':None}
r={n:run(c) for n,c in CFG.items()};lo,hi=0,.5
for _ in range(70):
 mid=(lo+hi)/2
 if run(CFG['central'],mid)['per_share_residual_conditional']<328.86:lo=mid
 else:hi=mid
j={'date':'2026-11-08','scope':'Conditional consolidated operating core with known financial claims and reserved Willis Re funding; excludes unvalued associate interests and unquantified AFW incremental economics. NOT whole-current-equity fair value.','units':'USD millions except per share','cases':r,'inverse_core_initial_growth':(lo+hi)/2,'stock_lives':L,'investment_floors':floor,'initial_cash_margin':M0,'approved_values':None,'unvalued_assets':{'Willis_Re_existing_plus_BMS_Re_US_interest':None,'other_equity_method_interests':None,'AFW_incremental_full_year_cash_flows':None,'recoverable_pension_surplus':None},'unquantified_claims':{'ultimate_litigation_above_provisions':None,'actual_postquarter_cash_bridge':None,'Newfront_future_service_conditioned_awards':None}}
(P/'model_results.json').write_text(json.dumps(j,indent=2));print({k:round(v['per_share_residual_conditional'],2) for k,v in r.items()},j['inverse_core_initial_growth'])
