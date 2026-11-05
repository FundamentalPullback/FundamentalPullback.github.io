"""Conditional consolidated FCFF. USD millions, capacity million tonnes/year.
Main EV values 100% consolidated operating cash flows. Outside CQP common
is subtracted at observed market value, NOT at book value or 49.4% of EV.
This market-bridge convention is explicit and separately sensitized.
"""
from pathlib import Path
from copy import deepcopy
import json,datetime
P=Path(__file__).parent
I=json.loads((P/'model/inputs.json').read_text());C=json.loads((P/'capital.json').read_text())['capital']

def value(c,wacc=None,unit_profit_scale=1.,nci_scale=1.,terminal_haircut=None,g_override=None):
 c=deepcopy(c);w=c['wacc']if wacc is None else wacc;g=c['terminal_growth']if g_override is None else g_override
 haircut=c['terminal_fee_haircut']if terminal_haircut is None else terminal_haircut
 rows=[];prev_rev=None
 # Initial five years from volume, gas pass-through and normalized unit economics.
 for y in range(1,6):
  vol=c['volume_mtpa'][y-1];infl=(1+c['unit_profit_inflation'])**max(0,y-3)
  recurring_ebitda=vol*c['runrate_ebitda']/c['runrate_capacity']*infl*unit_profit_scale
  temporary_marketing=c['temporary_marketing_premium'][y-1]
  adj_ebitda=recurring_ebitda+temporary_marketing
  sbc=c['sbc_2027']*(1+c['sbc_growth'])**(y-1)
  da=c['da'][y-1];ebit=adj_ebitda-sbc-da;tax=c['tax_rates'][y-1];nopat=ebit*(1-tax)
  revenue=vol*(I['gas_mmbtu_per_tonne']*I['henry_hub']*I['feedgas_multiplier']+c['cash_other_cost_per_tonne']*infl)+adj_ebitda
  wc=c['initial_wc'] if y==1 else max(0,revenue-prev_rev)*c['wc_incremental_ratio']
  maintaining=c['maintenance_capex'][y-1];growth=c['growth_capex'][y-1];finance_new=c['new_finance_asset_capex'][y-1]
  capex=maintaining+growth+finance_new;reinvestment=capex-da+wc;fcff=nopat-reinvestment
  rows.append(dict(year=2026+y,index=y,volume=vol,revenue=revenue,adjusted_ebitda=adj_ebitda,temporary_marketing_premium=temporary_marketing,sbc=sbc,da=da,ebit=ebit,tax_rate=tax,nopat=nopat,maintenance_capex=maintaining,committed_growth_capex=growth,new_finance_asset_capex=finance_new,total_capex=capex,incremental_wc=wc,net_reinvestment=reinvestment,fcff=fcff));prev_rev=revenue
 y5=rows[-1]
 for y in range(6,11):
  k=y-5;f=k/5
  # No unfunded capacity: only pricing/inflation and a gradual recontracting haircut.
  adj_ebitda=y5['adjusted_ebitda']*(1+g)**k*(1-haircut*f)
  sbc=y5['sbc']*(1+g)**k;da=y5['da']*(1+g)**k
  ebit=adj_ebitda-sbc-da;tax=y5['tax_rate']+(c['terminal_tax']-y5['tax_rate'])*f;nopat=ebit*(1-tax)
  revenue=y5['revenue']*(1+g)**k-(y5['adjusted_ebitda']*(1+g)**k-adj_ebitda)
  wc=max(0,revenue-prev_rev)*c['wc_incremental_ratio']
  # Young-asset cash-capex benefit explicitly ends; terminal reinvestment is g/ROIC.
  young_capex=(y5['maintenance_capex']+y5['new_finance_asset_capex'])*(1+g)**k
  young_net=young_capex-da+wc
  mature_net=nopat*g/c['terminal_roic']
  reinvestment=(1-f)*young_net+f*mature_net;capex=reinvestment+da-wc;fcff=nopat-reinvestment
  rows.append(dict(year=2026+y,index=y,volume=y5['volume'],revenue=revenue,adjusted_ebitda=adj_ebitda,sbc=sbc,da=da,ebit=ebit,tax_rate=tax,nopat=nopat,maintenance_capex=None,committed_growth_capex=0,new_finance_asset_capex=None,total_capex=capex,incremental_wc=wc,net_reinvestment=reinvestment,fcff=fcff));prev_rev=revenue
 last=rows[-1];terminal_nopat=last['nopat']*(1+g);terminal_reinvestment=terminal_nopat*g/c['terminal_roic'];terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(w-g)
 stub=(datetime.date(2026,12,31)-datetime.date(2026,11,4)).days/365
 for r in rows:r['discount_years']=r['index']+stub;r['discount_factor']=(1+w)**r['discount_years'];r['pv_fcff']=r['fcff']/r['discount_factor']
 pv_explicit=sum(r['pv_fcff']for r in rows);pv_terminal=tv/rows[-1]['discount_factor'];ev=pv_explicit+pv_terminal
 nci=C['nci_market_equity']*nci_scale;cash=I['cash']-c['operating_cash_buffer'];bridge_adjustment=c['post_quarter_cash_adjustment'];equity=ev-C['total_financial_debt']+cash+bridge_adjustment-nci
 return dict(wacc=w,terminal_growth=g,terminal_roic=c['terminal_roic'],terminal_fee_haircut=haircut,rows=rows,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,terminal_value=tv,pv_explicit=pv_explicit,pv_terminal=pv_terminal,ev=ev,terminal_share_of_ev=pv_terminal/ev,nominal_debt=C['nominal_debt'],finance_leases=C['finance_leases'],cash_excess_proxy=cash,post_quarter_cash_adjustment=bridge_adjustment,nci_market_equity=nci,equity=equity,shares=C['shares_proxy_m'],value_per_share=equity/C['shares_proxy_m'],price=C['price'],upside=equity/C['shares_proxy_m']/C['price']-1,mos=1-C['price']/(equity/C['shares_proxy_m']))
def solve(fn,lo,hi,target):
 a=fn(lo)-target;b=fn(hi)-target
 if a*b>0:return None
 for _ in range(100):
  mid=(lo+hi)/2;v=fn(mid)-target
  if a*v<=0:hi=mid
  else:lo=mid;a=v
 return(lo+hi)/2
if __name__=='__main__':
 cases={k:value(v)for k,v in I['cases'].items()};base=I['cases']['base'];price=C['price'];sensitivity=[]
 for w in [.05,.055,.06,.065,.07,.075,.08,.09]:
  for g in [0,.01,.015,.02]:sensitivity.append(dict(wacc=w,g=g,value=value(base,wacc=w,g_override=g)['value_per_share']))
 reverse=dict(wacc=solve(lambda x:value(base,wacc=x)['value_per_share'],.025,.15,price),normalized_ebitda_multiplier=solve(lambda x:value(base,unit_profit_scale=x)['value_per_share'],.3,2,price),terminal_fee_haircut=solve(lambda x:value(base,terminal_haircut=x)['value_per_share'],0,.7,price))
 stress={}
 for n,mod in [('same_wacc_operating_downside',{'runrate_ebitda':7300,'terminal_fee_haircut':.15}),('same_wacc_operating_upside',{'runrate_ebitda':8000,'terminal_fee_haircut':0}),('tax_21pct_from_start',{'tax_rates':[.21]*5,'terminal_tax':.21}),('no_terminal_haircut',{'terminal_fee_haircut':0})]:
  c=deepcopy(base);c.update(mod);stress[n]=value(c)['value_per_share']
 out=dict(status='independently_reviewed_conditional_observation',cases=cases,sensitivity=sensitivity,reverse=reverse,stress=stress,nci_sensitivity={str(x):value(base,nci_scale=x)['value_per_share']for x in [.75,1,1.25]},bridge_cash_sensitivity_per_1000=1000/C['shares_proxy_m'])
 (P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:{z:v[z]for z in ['value_per_share','ev','terminal_share_of_ev','wacc']}for k,v in cases.items()},indent=2));print('reverse',reverse,'stress',stress)
