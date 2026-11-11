import json,math,pathlib
P=pathlib.Path(__file__).resolve().parents[1];I=json.load(open(P/'inputs.json'));R=json.load(open(P/'results.json'));L=json.load(open(P/'legacy_results.json'));F=json.load(open(P/'rate_refresh.json'));checks=[]
def eq(a,b,label):
 assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7),(label,a,b)
 checks.append(label)
def calc(c):
 rev=I['rental_revenue_2026'];fleet=I['fleet_oec']*c['replacement_cost_premium'];cash=[]
 for t in range(1,11):
  z=max(0,t-5)/5;g=c['growth'][t-1] if t<6 else (1-z)*c['growth'][4]+z*c['terminal_g'];inf=(1-z)*c['equipment_inflation']+z*c['price_growth'];eff=c['efficiency'][t-1] if t<6 else 0
  vol=max(0,(1+g)/(1+c['price_growth'])/(1+eff)-1);old=rev;rev*=1+g
  rep=fleet*(1+inf)/c['holding_life']*(1-c['residual_fraction']/(1+inf)**c['holding_life']);add=fleet*(1+inf)*vol;fleet*= (1+inf)*(1+vol)
  m=c['core_margin_start']+(c['core_margin_y5']-c['core_margin_start'])*t/5 if t<6 else (1-z)*c['core_margin_y5']+z*c['core_margin_terminal']
  profit=(rev*m-rep-I['other_net_maintenance_2026']*rev/I['rental_revenue_2026'])*(1-(c['tax_first5'][t-1] if t<6 else c['tax']))
  phys=add+max(0,rev-old)*c['other_growth_ratio']+(rev-old)*c['nwc_ratio']
  if 'guided_net_capex_ratio' in c:phys+=c['guided_net_capex_ratio']*rev-rep-add
  cash.append(profit-((1-z)*phys+z*profit*g/c['terminal_roic']))
 terminal=profit*(1+c['terminal_g'])*(1-c['terminal_g']/c['terminal_roic']);ev=sum(v/(1+c['wacc'])**(n+1) for n,v in enumerate(cash))+terminal/(c['wacc']-c['terminal_g'])/(1+c['wacc'])**10
 claim=sum(I[k] for k in ['gross_debt','financing_obligations','fleet_purchase_payables'])+sum(c[k] for k in ['accrued_interest_reserve','pension_reserve','other_claim_reserve','operating_cash_buffer'])-I['cash']-c['earnout_value']
 return cash,ev,max(0,ev-claim)/c['shares'],claim
for name,case in list(R.items())+list(F['cases'].items()):
 if name=='reverse':continue
 vals,ev,v,b=calc(case['assumptions']);eq(ev,case['enterprise_value'],name+' EV');eq(v,case['value_per_share'],name+' equity');eq(b,case['bridge'],name+' bridge')
 for n,x in enumerate(vals):eq(x,case['rows'][n]['fcff'],name+str(n))
 if name in L:
  eq(ev,L[name]['enterprise_value'],name+' legacy EV')
  eq(v,L[name]['value_per_share'],name+' legacy equity')
p=F['inputs'];E=p['price']*p['cover_shares'];ke=p['rf']+p['erp']*p['beta'];w=(E*ke+p['gross_financing']*p['marginal_debt_rate_assumption']*(1-p['tax']))/(E+p['gross_financing']);eq(w,F['wacc'],'WACC');eq(ke,F['ke'],'KE')
for key,rkey in [('wacc','base_break_even_wacc'),('holding_life','base_break_even_holding_life'),('core_margin_terminal','base_break_even_terminal_margin')]:
 c=I['scenarios']['base'].copy();c[key]=R['reverse'][rkey];eq(calc(c)[2],I['price'],rkey)
c=I['scenarios']['base'].copy()
for k in ['core_margin_start','core_margin_y5','core_margin_terminal']:c[k]+=R['reverse']['uniform_core_margin_uplift']
eq(calc(c)[2],I['price'],'uniform margin inverse')
eq(R['base']['price_implied_ev'],I['price']*I['scenarios']['base']['shares']+R['base']['bridge'],'price EV')
json.dump({'status':'PASS','checks':len(checks),'labels':checks,'wacc':w,'notes':'Independent input-based operating reconstruction; no production model import. Legacy operating value unchanged, four inverses independently evaluated.'},open(P/'audit/output.json','w'),indent=2)
print(len(checks),'PASS')
