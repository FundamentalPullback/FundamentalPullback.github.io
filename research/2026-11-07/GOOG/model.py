import pathlib,json,csv,math,datetime
P=pathlib.Path(__file__).parent;H=json.loads((P/'history.json').read_text());R0=H['TTM2026']['revenue'];C0=(H['TTM2026']['ebit']+H['TTM2026']['depreciation']+1500)/R0
# USD million. Economic depreciation of physical capital, including capacity activation.
# No expensed R&D capitalization. Cash margin keeps SBC, R&D and operating rent as costs.
rf=.0486;erp=.0441
cfg={'stress':dict(g0=.10,cm=.37,life=5,beta=1.4,g=.02,tax=.23,cap=[240000,250000,240000,220000,210000],equity_haircut=.25,private_haircut=.40,nci_multiple=3), 'central':dict(g0=.16,cm=.42,life=6,beta=1.2,g=.025,tax=.21,cap=[240000,260000,260000,240000,220000],equity_haircut=.10,private_haircut=.25,nci_multiple=2),'upside':dict(g0=.22,cm=.46,life=7,beta=1,g=.03,tax=.19,cap=[250000,280000,290000,270000,250000],equity_haircut=0,private_haircut=.10,nci_multiple=1)}
def solve(c,g_override=None):
 g0=c['g0'] if g_override is None else g_override;rate=.65/c['life']+.35/20
 ke=rf+c['beta']*erp;kd=.0575;wacc=ke*.96+kd*(1-c['tax'])*.04
 R=R0;S=227557;CIP=145270;I=8817;rows=[];pv=0;cum=0;low=0
 for y in range(1,11):
  gr=g0+(c['g']-g0)*(y-1)/9;nr=R*(1+gr);cm=C0+(c['cm']-C0)*min(y/5,1);lease_rate=({'stress':.03,'central':.02,'upside':.01}[next(n for n,v in cfg.items() if v is c)])*min(y/5,1)
  placed=145270*([.5,.3,.2][y-1] if y<=3 else 0);CIP-=placed
  steadycap=(rate*(S+placed)+gr*(S+placed))/(1-rate/2)
  if y<=5:cap=c['cap'][y-1]
  else:cap=(1-(y-5)/5)*c['cap'][-1]+((y-5)/5)*steadycap
  # Replacement floor: no run-down to manufacture cash. Cap includes needed renewal.
  cap=max(cap,rate*(S+placed)/(1-rate/2));da=rate*(S+placed)+rate*cap/2
  ipcap=max(.005*nr,(I/5+gr*I)/(1-.1));ipa=I/5+.1*ipcap
  ebit=cm*nr-da-ipa;tax=ebit*c['tax'] if ebit>0 else 0;nopat=ebit-tax;nwc=.03*(nr-R)
  fcff=nopat+da+ipa-cap-ipcap-nwc
  endS=S+placed+cap-da;endI=I+ipcap-ipa;cum+=fcff;low=min(low,cum)
  rows.append(dict(year=y,revenue=nr,growth=gr,cash_margin=cm,incremental_lease_cost_assumption=lease_rate*nr,cash_margin_before_incremental_leases=cm+lease_rate,physical_start=S,cip_activated=placed,cip_end=CIP,physical_capex=cap,physical_da=da,physical_end=endS,intangible_start=I,intangible_capex=ipcap,intangible_amort=ipa,intangible_end=endI,ebit=ebit,nopat=nopat,nwc_investment=nwc,fcff=fcff,cumulative_fcff=cum))
  pv+=fcff/(1+wacc)**y;R=nr;S=endS;I=endI
 g=c['g'];tailS=S;tailI=I;tailR=R;tv=0;first=None
 # Continue the same acquired-intangible floor and asset stocks; do not erase renewal at year 11.
 for t in range(1,1001):
  nr=tailR*(1+g);cap=(rate*tailS+g*tailS)/(1-rate/2);da=rate*tailS+rate*cap/2
  ipcap=max(.005*nr,(tailI/5+g*tailI)/.9);ipa=tailI/5+.1*ipcap;nwc=.03*(nr-tailR)
  ebit=c['cm']*nr-da-ipa;nopat=ebit-max(ebit,0)*c['tax'];reinvest=cap+ipcap-da-ipa+nwc;fcff=nopat-reinvest
  if first is None:first=(nr,cap,da,ipcap,ipa,nwc,nopat,reinvest,fcff)
  tv+=fcff/(1+wacc)**t;tailS+=cap-da;tailI+=ipcap-ipa;tailR=nr
 nr,cap,da,ipcap,ipa,nwc,nopat,reinvest,fcff=first;ev=pv+tv/(1+wacc)**10

 # A conditional, disclosed claim bridge, not certified market value of NCI/investments.
 bridge=174714-30000+90384*(1-c['equity_haircut'])+135230*(1-c['private_haircut'])-127485-3705-13807-12219-(27833-1458)-35921-6900*c['nci_multiple']
 # Treat mandatory preferred through conversion + PV coupons, not simultaneous principal deduction.
 preferred_shares=19.25/2*(2.8160+2.8420);rsu_proxy=112;denom=12294+rsu_proxy+preferred_shares
 prefdiv=19250*.0625;dates=[datetime.date(y,m,15) for y in [2026,2027,2028,2029] for m in [2,5,8,11] if datetime.date(2026,11,6)<datetime.date(y,m,15)<=datetime.date(2029,5,15)];pref_coupon_pv=sum(prefdiv/4/(1+ke)**((d-datetime.date(2026,11,6)).days/365.25) for d in dates)
 residue=ev+bridge-pref_coupon_pv
 return dict(wacc=wacc,ke=ke,physical_decay_rate=rate,years=rows,terminal_continuation_years=1000,terminal_value_at_year10=tv,terminal=dict(revenue=nr,physical_capex=cap,physical_da=da,intangible_capex=ipcap,intangible_amort=ipa,nwc=nwc,nopat=nopat,reinvestment=reinvest,fcff=fcff,implied_incremental_roic=nopat*g/reinvest,g=g),operating_ev=ev,terminal_weight=(tv/(1+wacc)**10)/ev if ev else None,conditional_bridge=bridge,preferred_coupon_pv=pref_coupon_pv,conditional_share_denominator=denom,conditional_equity_residue=residue,conditional_per_share=residue/denom,maximum_cumulative_operating_funding_need=-low,available_cash_debt_securities_less_reserve=144714,external_operating_funding_need=max(0,-low-144714))
res={n:solve(c) for n,c in cfg.items()};inverse={}
for price in [283.93,284.78]:
 lo,hi=0,.65
 for _ in range(90):
  m=(lo+hi)/2
  if solve(cfg['central'],m)['conditional_per_share']<price:lo=m
  else:hi=m
 inverse[str(price)]=(lo+hi)/2
out={'as_of':'2026-11-08','model_start':'prospective 12 months from research cutoff, no claimed calendar-year forecast','units':'USD million, except per-share','base_revenue':R0,'base_cash_margin':C0,'intangible_amortization_anchor':1500,'intangible_anchor_note':'Q3 expense375 annualized proxy, not certified TTM; future acquired-intangible renewal budget is conditional and distinct from expensed R&D' ,'risk_free':rf,'risk_free_date':'2026-11-06','erp':erp,'erp_date':'2026-11-01','beta_status':'scenario hypotheses, not measured regression','cases':res,'config':cfg,'inverse_initial_sales_growth':inverse,'nov5_debt_issuance_eur_m':6000,'nov5_cash_debt_delta_treatment':'gross proceeds and principal approximately offset; fees, FX, deployment unverified, not invented as zero-certified bridge','approved_value':None,'approved_entry':None,'unquantified_claims':None,'nci_fair_value':None,'funding_commitment_gap':'contract maxima cannot be mapped exactly to capex/opex/leases; no whole-equity certification'}
(P/'model_results.json').write_text(json.dumps(out,indent=2))
with (P/'scenarios.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['scenario']+list(res['central']['years'][0]));w.writeheader();w.writerows(dict(scenario=n,**y) for n,c in res.items() for y in c['years'])
print({n:{k:c[k] for k in ['operating_ev','conditional_per_share','external_operating_funding_need']} for n,c in res.items()});print(inverse)
