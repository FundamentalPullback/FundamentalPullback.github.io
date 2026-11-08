"""Conditional segment FCFF, USD millions. All approved values null.
Amazon option claim deducted once; forecasts BEFORE customer warrant accounting reduction.
New Way target given explicit asset-based proxy, never cost-only/target-zero.
"""
from pathlib import Path
import csv,json,copy
P=Path(__file__).resolve().parent
PRICE=176.78;SHARES=58.988982+.715644+.001117;ZARUSD=1.1165/18.4649
BRIDGE={'cash_september':393.671,'operating_cash_reserve':-175,'debt_principal_and_finance_leases':-1338.478,'contingent_consideration_all_including_stock_portion':-120.107,'legal_accrual':-30.644,'legacy_clean_energy_warranty_reserve_proxy':-14.293,'redeemable_and_other_nci':-.100,'amazon_warrant_full_grant_fair_value_proxy':-112.463,'newway_cash_paid':-110*ZARUSD,'newway_vendor_debt':-110*ZARUSD}
S={'adverso':dict(resg=.025,legacyg=.025,dc=[1200,1600,1800,1950,2100],resm=.17,legm=.08,dcm=.11,wacc=.13,g=.02,roic=.16,rt=.14,maint=.027,gcap=.18,nwc=.20,ip=.006,newway_haircut=.25,newway_adjust=40,legal_extra=40,dealer_loss=.10),
'central':dict(resg=.055,legacyg=.06,dc=[2200,3000,3600,4000,4400],resm=.20,legm=.12,dcm=.18,wacc=.12,g=.025,roic=.22,rt=.18,maint=.025,gcap=.14,nwc=.17,ip=.005,newway_haircut=.5,newway_adjust=20,legal_extra=20,dealer_loss=.05),
'favorable':dict(resg=.08,legacyg=.08,dc=[2600,3800,4600,5300,5800],resm=.22,legm=.15,dcm=.22,wacc=.11,g=.03,roic=.28,rt=.22,maint=.024,gcap=.12,nwc=.15,ip=.005,newway_haircut=.75,newway_adjust=0,legal_extra=5,dealer_loss=.02)}
def calc(s,dcscale=1,physical_only=False):
 # 2026 guidance-anchored segment proxies: residential3bn + legacyCI1.4bn + DC.5bn, not presented as historical reported.
 res=3000;legacy=1400;dc=500;sales=4900;pv=0;rows=[]
 for y in range(1,12):
  prev=sales;old_dc=dc
  rg=s['resg'] if y<=5 else s['resg']+(s['g']-s['resg'])*min(y-5,5)/5
  lg=s['legacyg'] if y<=5 else s['legacyg']+(s['g']-s['legacyg'])*min(y-5,5)/5
  res*=1+rg;legacy*=1+lg
  if y<=5:dc=s['dc'][y-1]*dcscale
  else:
   anchor=s['dc'][-1]/s['dc'][-2]-1;dc*=1+anchor+(s['g']-anchor)*min(y-5,5)/5
  sales=res+legacy+dc;growth=sales/prev-1
  rm=s['resm'];lm=s['legm'];dm=max(s['dcm']-.02,0)+(s['dcm']-max(s['dcm']-.02,0))*min(y-1,3)/3
  ebita=res*rm+legacy*lm+dc*dm;tax=.25;nopat=ebita*(1-tax)
  da=sales*.024;maint=max(sales*s['maint'],120*1.025**min(y,10)*(1+s['g'])**max(y-10,0));growthcap=max(0,sales-prev)*s['gcap'];capex=maint+growthcap;wc=max(0,sales-prev)*s['nwc'];ip=sales*s['ip']
  roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5;explicit=capex-da+wc+ip;reinv=max(explicit,0) if physical_only else max(explicit,nopat*max(growth,0)/roic);fcff=nopat-reinv
  row=dict(year=y,residential_sales=res,legacy_ci_sales=legacy,datacenter_sales=dc,total_sales=sales,growth=growth,residential_cash_ebita_margin=rm,legacy_ci_cash_ebita_margin=lm,dc_cash_ebita_margin=dm,cash_ebita=ebita,nopat=nopat,physical_da=da,maintenance_capex=maint,growth_capex=growthcap,cash_capex=capex,delta_nwc=wc,incremental_ip_budget=ip,explicit_reinvestment=explicit,roic=roic,reinvestment=reinv,other_funded_capital=max(0,reinv-explicit),fcff=fcff);rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
 tv=rows[-1]['fcff']/(s['wacc']-s['g'])/(1+s['wacc'])**10;ev=pv+tv
 newway=250.2*ZARUSD*s['newway_haircut'];bridge=sum(BRIDGE.values())+newway-s['newway_adjust']*ZARUSD-s['legal_extra']-181.7*s['dealer_loss'];eq=ev+bridge
 return dict(value_per_share=eq/SHARES,enterprise_value=ev,equity_value=eq,bridge=bridge,newway_asset_value_proxy=newway,newway_price_adjustment=s['newway_adjust']*ZARUSD,explicit_pv=pv,terminal_pv=tv,terminal_weight=tv/ev,rows=rows)
def main():
 out={k:calc(s) for k,s in S.items()}
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 sens=[]
 for w in [.11,.12,.13]:
  for g in [.02,.025,.03]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sens.append(dict(wacc=w,g=g,value=calc(s)['value_per_share']))
 lo,hi=.05,.6
 for _ in range(100):
  mid=(lo+hi)/2;s=copy.deepcopy(S['central']);s['dcm']=mid
  if calc(s)['value_per_share']<PRICE:lo=mid
  else:hi=mid
 grid=[{'dc_scale':i/100,'value':calc(S['central'],i/100)['value_per_share']} for i in range(10,801)]
 best=max(grid,key=lambda x:x['value'])
 ke=.0486+1.85*.0441;dw=1338.478/(PRICE*SHARES+1338.478);kd=(700*.0493+490*.0543)/1190
 r=dict(ticker='GNRC',as_of='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_close',shares=SHARES,bridge_items=BRIDGE,scenarios=out,physical_only={k:calc(s,physical_only=True)['value_per_share'] for k,s in S.items()},sensitivity=sens,inverse_dc_terminal_margin=(lo+hi)/2,inverse_dc_scale_root=None,dc_scale_grid_best=best,inverse_warning='DC growth scaling is nonmonotonic under funded investment; no price root in scale0.1-8 grid; margin inverse used instead.',cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',erp_source_rf=.0529,date_basis_mismatch=True,beta=1.85,ke=ke,reported_weighted_term_rate=kd,marginal_kd_assumed=.0636,debt_weight=dw,mechanical_wacc=ke*(1-dw)+.0636*.75*dw,base_wacc=.12),approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,gaps=['Firm data-center order terms, cancellation protections and customer concentration not fully disclosed; backlog is not ASC606 RPO.','Physical capacity/unit economics, installation ramp and incremental ROIC not certified.','New Way closing price adjustment and operating valuation incomplete; explicit nonzero net-asset proxies, not acquisition cost-only.','Unresolved clean-energy/standby litigation and dealer repurchase losses not quantified; buffers illustrative, not bounds.','Amazon option valuation is grant-date full-award proxy, not current probability-weighted fair value; no duplicate warrant dilution or future contra-revenue.','Next primary earnings date unannounced.','Forecast begins from estimated FY2026 segment base; annual normalized discounting omits a precise November-to-year-end stub.','Incremental IP budget is assumed distinct from expensed R&D and software capex; no primary split validates absence of overlap.','Ordinary incremental diluted-share proxy and contingent stock settlements require current instrument-level reconciliation.'])
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:{a:v[a] for a in ['value_per_share','enterprise_value','terminal_weight','newway_asset_value_proxy']} for k,v in out.items()});print('inverse',r['inverse_dc_terminal_margin'],r['dc_scale_grid_best'],'physical',r['physical_only'],'wacc',r['cost_of_capital'])
if __name__=='__main__':main()
