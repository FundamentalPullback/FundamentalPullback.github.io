"""SPSC 10-year operating FCFF. USD millions except per-share values; all forecasts are analyst assumptions."""
import pathlib,json,csv,copy
P=pathlib.Path(__file__).parent
PRICE=85.25;REVENUE=787.9;SHARES=36.209;CASH=153.818+29.683;RESERVE=50;DEBT=0
BASE={'growth':[.04,.05,.05,.045,.04],'cash_margin':[.222,.228,.234,.24,.245], 'tax':.25,'da_pct':.0306,'capex_pct':.04,'nwc_sales':.05,'roic_initial':.25,'roic_terminal':.20,'terminal_growth':.025,'terminal_margin':.23,'wacc':.10}
BEAR={**BASE,'growth':[0,.01,.02,.02,.02],'cash_margin':[.205,.20,.20,.20,.20],'tax':.27,'capex_pct':.045,'roic_initial':.18,'roic_terminal':.15,'terminal_growth':.02,'terminal_margin':.19,'wacc':.11}
BULL={**BASE,'growth':[.07,.08,.08,.07,.06],'cash_margin':[.24,.255,.265,.275,.28],'tax':.24,'capex_pct':.035,'roic_initial':.30,'roic_terminal':.25,'terminal_growth':.03,'terminal_margin':.27,'wacc':.09}
# Acquisition-amortization schedule is a book bridge, not an assumed incremental tax deduction.
AMORT=[40.088,30.052,23.614,21.427,7.011,7.011,7.011,7.011,7.011,0.0]
def model(s,full=False):
 rev=s.get('revenue_base',REVENUE);rows=[];previous_cash_nopat=rev*(174.8/787.9)*(1-s['tax'])
 for i in range(1,11):
  a=max(0,(i-5)/5)
  g=s['growth'][i-1] if i<=5 else s['growth'][-1]*(1-a)+s['terminal_growth']*a
  margin=s['cash_margin'][i-1] if i<=5 else s['cash_margin'][-1]*(1-a)+s['terminal_margin']*a
  old=rev;rev*=1+g;cash_ebit=rev*margin;am=AMORT[i-1];ebit=cash_ebit-am
  # Cash tax on pre-acquired-amort EBIT; do not manufacture a tax shield from book amortization.
  tax=cash_ebit*s['tax'];nopat=ebit-tax;da=rev*s['da_pct']+am
  capex=rev*s['capex_pct'];wc=(rev-old)*s['nwc_sales']
  roic=s['roic_initial']*(1-a)+s['roic_terminal']*a
  minimum_net=capex-rev*s['da_pct']+wc
  growth_net=cash_ebit*(1-s['tax'])*g/roic
  if s.get('charge_margin_growth',False): growth_net=max(growth_net,(cash_ebit*(1-s['tax'])-previous_cash_nopat)/roic)
  previous_cash_nopat=cash_ebit*(1-s['tax'])
  # Additional economic reinvestment funds durable growth, customer/technology renewal and future inorganic needs.
  net= max(minimum_net,growth_net) if i<=5 else (1-a)*max(minimum_net,growth_net)+a*growth_net
  extra=max(0,net-minimum_net) if i<=5 else net-minimum_net
  investment=capex+extra
  fcff=nopat+da-investment-wc
  assert abs(fcff-(cash_ebit*(1-s['tax'])-net))<1e-9
  rows.append({'year':2026+i,'growth':g,'revenue':rev,'cash_ebit_margin_after_SBC':margin,'cash_ebit':cash_ebit,'book_acquired_amortization':am,'ebit_after_book_amortization':ebit,'cash_tax':tax,'nopat':nopat,'total_da':da,'ppe_capex_including_software':capex,'delta_nwc':wc,'incremental_roic':roic,'growth_reinvestment_requirement':growth_net,'net_reinvestment':net,'additional_economic_reinvestment':extra,'total_investment':investment,'fcff':fcff,'pv_fcff':fcff/(1+s['wacc'])**i})
 ng=s['terminal_growth'];nop=rev*(1+ng)*s['terminal_margin']*(1-s['tax']);reinv=nop*ng/s['roic_terminal'];tf=nop-reinv;tv=tf/(s['wacc']-ng);pvt=tv/(1+s['wacc'])**10;ev=sum(r['pv_fcff'] for r in rows)+pvt;equity=ev+CASH-RESERVE-DEBT
 return {'value':equity/SHARES,'ev':ev,'equity':equity,'excess_cash':CASH-RESERVE,'shares':SHARES,'pv_terminal':pvt,'terminal_weight':pvt/ev,'terminal_nopat':nop,'terminal_reinvestment':reinv,'terminal_fcff':tf,'rows':rows if full else None}
def solve(key,target=PRICE):
 lo,hi=(0,.30) if key=='growth' else (.10,.60)
 for _ in range(100):
  mid=(lo+hi)/2;s=copy.deepcopy(BASE)
  if key=='growth':s['growth']=[mid]*5
  else:s['cash_margin']=[mid]*5;s['terminal_margin']=mid
  if model(s)['value']>target:hi=mid
  else:lo=mid
 return (lo+hi)/2
if __name__=='__main__':
 scenarios={k:{'assumptions':s,**model(s,True)} for k,s in [('bear',BEAR),('base',BASE),('bull',BULL)]}
 sensitivity=[{'wacc':w,'g':g,'value':model({**BASE,'wacc':w,'terminal_growth':g})['value']} for w in [.09,.10,.11] for g in [.02,.025,.03]]
 reverse={'constant_initial_growth_at_base_margin':solve('growth'),'constant_cash_margin_at_base_growth':solve('margin'),'growth_margin_combinations':[{'initial_growth':g,'cash_margin':m,'value':model({**BASE,'growth':[g]*5,'cash_margin':[m]*5,'terminal_margin':m})['value']} for g in [.04,.08,.12] for m in [.23,.27,.30]]}
 robustness={'finance_all_positive_nopat_growth':model({**BASE,'charge_margin_growth':True})['value'],'base_revenue_less_10_5':model({**BASE,'revenue_base':REVENUE-10.5})['value'],'roic_initial20_terminal15':model({**BASE,'roic_initial':.20,'roic_terminal':.15})['value'],'all_cash_available':model(BASE)['value']+RESERVE/SHARES,'extra_operating_cost_2pct':model({**BASE,'cash_margin':[m-.02 for m in BASE['cash_margin']],'terminal_margin':BASE['terminal_margin']-.02})['value']}
 offset=57/365
 basev=model(BASE,True)
 robustness['calendar_57day_offset_no_stub']=(basev['ev']/(1+BASE['wacc'])**offset+CASH-RESERVE)/SHARES
 robustness['calendar_57day_offset_with_proxy_stub']=(basev['ev']/(1+BASE['wacc'])**offset+basev['rows'][0]['fcff']*offset/(1+BASE['wacc'])**offset+CASH-RESERVE)/SHARES
 out={'price':PRICE,'price_date':'2026-11-03','units':'USD millions except per-share values','scenarios':scenarios,'sensitivity':sensitivity,'reverse':reverse,'robustness':robustness}
 (P/'model_results.json').write_text(json.dumps(out,indent=2))
 with (P/'ten_year_model.csv').open('w') as f:
  rows=[{'scenario':k,**r} for k,s in scenarios.items() for r in s['rows']];w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps({k:{x:v for x,v in s.items() if x not in ['rows','assumptions']} for k,s in scenarios.items()},indent=2));print(reverse);print(robustness)
