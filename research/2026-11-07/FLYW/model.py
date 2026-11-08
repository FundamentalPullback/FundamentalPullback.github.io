import json,csv,pathlib
P=pathlib.Path(__file__).parent
H=json.loads((P/'history.json').read_text()); rev0=H['TTM2026']['rev'];cm0=(H['TTM2026']['ebit']+H['TTM2026']['da'])/rev0
shares=122.542824;price=21.57
# Conditional owner-equity bridge: reserve all net settlement obligations. Claims stay an explicit unknown L.
cash_proxy=407.173+3.043+158.772-334.974
bridge=cash_proxy-.10*rev0-5.305
tax=.25;dphys=.20;dip=.125;cap_phys=.02;cap_ip=.01;nwc=.08;gt=.025
def calc(g1,g5,cm5,cm10,beta,write=None,override=None):
 w=.0486+beta*.0441+.01
 R=rev0;K=29.089;I=177.229;pv=0;out=[]
 if override is not None:cm5=cm10=override
 for y in range(1,11):
  if y<=5:g=g1+(g5-g1)*(y-1)/4;cm=cm0+(cm5-cm0)*y/5
  else:g=g5+(gt-g5)*(y-5)/5;cm=cm5+(cm10-cm5)*(y-5)/5
  nr=R*(1+g);dep=dphys*K+dip*I;ebit=cm*nr-dep
  cp=cap_phys*nr;ci=cap_ip*nr;dw=nwc*(nr-R)
  fcff=ebit*(1-tax)+dep-cp-ci-dw;pv+=fcff/(1+w)**y
  K+=cp-dphys*K;I+=ci-dip*I
  out.append(dict(year=y,revenue=nr,growth=g,cash_operating_margin_includes_sbc_rnd=cm,da=dep,ebit=ebit,nopat=ebit*(1-tax),physical_software_capex=cp,acquired_ip_relationship_renewal=ci,delta_nwc=dw,fcff=fcff,physical_stock=K,intangible_stock=I))
  R=nr
 R1=R*(1+gt)
 # Exact infinite continuation of depreciating stocks at fixed funded capex/revenue, no year11 capex haircut.
 dpv=dphys/(w+dphys)*(K+cap_phys*R1/(w-gt))+dip/(w+dip)*(I+cap_ip*R1/(w-gt))
 tv=R1*(cm10*(1-tax)-cap_phys-cap_ip-nwc*gt/(1+gt))/(w-gt)+tax*dpv
 ev=pv+tv/(1+w)**10
 if write:
  with (P/('forecast_'+write+'.csv')).open('w') as f:
   wr=csv.DictWriter(f,fieldnames=out[0]);wr.writeheader();wr.writerows(out)
 return dict(wacc=w,ke=w,beta_assumed=beta,risk_free=.0486,erp=.0441,execution_premium=.01,ev=ev,conditional_equity=ev+bridge,value_per_basic_share_before_unknown_claims=(ev+bridge)/shares,terminal_pv_share=(tv/(1+w)**10)/ev,terminal_value=tv,year10=out[-1],approved_value=None)
sc={'prudente':(.10,.06,.16,.16,1.5),'central':(.18,.12,.21,.22,1.25),'favorable':(.25,.16,.26,.28,1.)}
res={n:calc(*v,write=n) for n,v in sc.items()}
for r in res.values():r['value_per_share_with_q3_incremental_dilution_proxy']=r['conditional_equity']/(shares+129.703126-121.956220)
lo,hi=.01,.8
for _ in range(100):
 mid=(lo+hi)/2
 if calc(*sc['central'],override=mid)['value_per_basic_share_before_unknown_claims']<price:lo=mid
 else:hi=mid
ans={'cutoff':'2026-11-08','quote_date':'2026-11-06','quote':price,'current_shares_m':shares,'market_cap':price*shares,'cash_after_net_settlement_proxy':cash_proxy,'operating_liquidity_reserve_assumed':.1*rev0,'contingent_consideration_book':5.305,'equity_bridge_before_unknown_claims':bridge,'additional_claims_L':None,'claim_sensitivity_per_100m':100/shares,'scenarios':res,'inverse_cash_operating_margin_year5_and10_central_other_assumptions':(lo+hi)/2,'approved_value':None,'approved_entry':None}
(P/'model_results.json').write_text(json.dumps(ans,indent=2));print(json.dumps(ans,indent=2))
