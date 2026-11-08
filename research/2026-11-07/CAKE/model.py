import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.loads((P/'history.json').read_text());t=h['paired_ttm_september']['2026']
def weekly(file):
 r=json.loads((P/'beta_price_inputs.json').read_text())[file];a=r['indicators']['adjclose'][0]['adjclose'];out={}
 for ts,c in zip(r['timestamp'],a):
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if c and d.isoformat()<='2026-11-06':out[d.isocalendar()[:2]]=float(c)
 return out
x,y=weekly('price_year.json'),weekly('SPY_price_year.json');keys=sorted(set(x)&set(y));rx=[x[b]/x[a]-1 for a,b in zip(keys,keys[1:])];ry=[y[b]/y[a]-1 for a,b in zip(keys,keys[1:])];mx,my=statistics.mean(rx),statistics.mean(ry);beta=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/sum((b-my)**2 for b in ry);corr=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=106.76;shares=49.855413;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-10-26',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='StockAnalysis; Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
rf=.0486;erp=.0441;debt=575;wd=debt/(cap+debt)
J('capital_cost.json',dict(as_of='2026-11-06',rf=rf,rf_source='US Treasury 10y Nov6',erp=erp,erp_source='Damodaran Nov1 implied ERP',weekly_beta=beta,r_squared=corr*corr,weekly_observations=len(rx),weekly_periods=[str(keys[0]),str(keys[-1])],beta_shrunk_two_thirds_plus_one_third=2*beta/3+1/3,beta_method='OLS weekly adjusted total-return proxy against SPY; incomplete first week retained explicitly',debt_weight=wd,debt_cost_method='Nov6 Rf plus 100/150/200bp assumptions, not a bond quote; convertible coupon is not a current straight-debt yield, not quoted current bond yield'))
# FY25 fair-value expense10.5 plus YTD26 credit13.2 less YTD25 zero = net TTM gain2.7.
normalized=t['ebit']-2.7
base=dict(revenue=t['revenue'],normalized_ebit=normalized,ttm_frc_fair_value_gain_removed=2.7,quarter_gain=13.2,cash_margin=(normalized+t['da'])/t['revenue'],stocks=[937.230,7.280],stock_dates=['2026-09-29 physical','2025-12-30 definite intangible latest separate breakdown'],initial_da=[t['da']-1.263,1.263],physical_life=937.230/(t['da']-1.263),intangible_remaining_life=7.280/1.263,capex_guide_2026=210,expensed_repairs_2025=110.5,preopening_in_margin=t['preopening'],cash=249.269,borrowed_principal=575,convert_rate_per1000=14.1552,conversion_strike=1000/14.1552,convert_shares=575*.0141552,operating_lease_liability=1581.435,nonqualified_asset=140.169,nonqualified_liability=140.095,nonqualified_surplus_not_added=True,gift_card_liability=176.386,frc_recorded_liability=0,frc_contract_claim_maximum=None,frc_contract_last_payment_year=2027,declared_dividend=.30,dividend_record='2026-11-10',dividend_payment='2026-11-24',dividend_bridge_deduction=0,dividend_note='Nov6 cum-dividend quote before future record/payment; do not deduct future distribution mechanically.',conversion_reset='2026-11-10 pending',sbc_convention='Retained in margins; issued shares already include restricted awards, no duplicate full-RSU addition.')
J('model_inputs.json',base);mb=2*beta/3+1/3
scenarios=[dict(name='prudente',g1=.04,g5=.025,gterm=.02,pricegrowth=.02,m5=.075,m10=.07,beta=mb+.2,spread=.025,tax=.26,buffer=125,legal=25,frc=20,wc=.04,new_unit_capital_per_sales=.8),dict(name='central',g1=.08,g5=.05,gterm=.025,pricegrowth=.025,m5=.10,m10=.095,beta=mb,spread=.02,tax=.20,buffer=100,legal=15,frc=10,wc=.03,new_unit_capital_per_sales=.65),dict(name='favorable',g1=.10,g5=.07,gterm=.03,pricegrowth=.025,m5=.115,m10=.11,beta=max(.5,mb-.15),spread=.015,tax=.17,buffer=80,legal=5,frc=5,wc=.02,new_unit_capital_per_sales=.55)]
def bond_value(date,yield_rate):
 dates=[datetime.date(y,m,15) for y in range(2027,2031) for m in [3,9] if datetime.date(y,m,15)<=datetime.date(2030,3,15)]
 return sum((5.75+(575 if d==datetime.date(2030,3,15) else 0))/(1+yield_rate/2)**(2*(d-date).days/365.25) for d in dates if d>date)
def call_value(v,date,r,sigma):
 if v<=0:return 0
 T=(datetime.date(2030,3,15)-date).days/365.25;K=base['conversion_strike'];q=1.2/106.76
 d1=(math.log(v/K)+(r-q+sigma*sigma/2)*T)/(sigma*math.sqrt(T));d2=d1-sigma*math.sqrt(T);N=lambda x:(1+math.erf(x/math.sqrt(2)))/2
 return v*math.exp(-q*T)*N(d1)-K*math.exp(-r*T)*N(d2)
sepdate=datetime.date(2026,9,29);nowdate=datetime.date(2026,11,6);sepprice=107.3499984741211
lo,hi=.01,2
for _ in range(100):
 mid=(lo+hi)/2;v=bond_value(sepdate,.0498+.02)+base['convert_shares']*call_value(sepprice,sepdate,.0498,mid)
 if v<923.4:lo=mid
 else:hi=mid
sigma=(lo+hi)/2
J('convertible_calibration.json',dict(observed_fair_value=923.4,date='2026-09-29',stock_close=sepprice,treasury_3y=.0498,current_treasury_3y=.0459,assumed_credit_spread=.02,implied_volatility=sigma,dividend_yield_proxy=1.2/106.76,method='Semiannual bond PV plus European call, with immediate conversion floor. Calibration conditional on assumed credit spread; omits issuer call/make-whole/reset exact path, not a certified option valuation. Current November10 dividend reset is pending.'))
def allocate(pool,p):
 lo,hi=0,max(1,pool/shares)
 for _ in range(100):
  v=(lo+hi)/2;debt_claim=max(575+base['convert_shares']*max(v-base['conversion_strike'],0),bond_value(nowdate,.0459+p['spread'])+base['convert_shares']*call_value(v,nowdate,.0459,sigma))
  if v*shares+debt_claim<pool:lo=v
  else:hi=v
 v=(lo+hi)/2;return dict(value_per_share=v,convertible_total_claim=max(575+base['convert_shares']*max(v-base['conversion_strike'],0),bond_value(nowdate,.0459+p['spread'])+base['convert_shares']*call_value(v,nowdate,.0459,sigma)))
def run(p,override=None):
 ke=rf+p['beta']*erp;kd=rf+p['spread'];wacc=ke*(1-wd)+kd*(1-p['tax'])*wd
 rev=t['revenue'];assets=base['stocks'][:];rows=[];pv=0;lives=[base['physical_life'],base['intangible_remaining_life']]
 for yr in range(1,1001):
  if yr<=5:
   g=p['g1']+(p['g5']-p['g1'])*(yr-1)/4;cm=base['cash_margin']+((override if override is not None else p['m5'])-base['cash_margin'])*yr/5
  else:
   z=min((yr-5)/5,1);g=p['g5']+(p['gterm']-p['g5'])*z;cm=(override if override is not None else p['m5'])+((override if override is not None else p['m10'])-(override if override is not None else p['m5']))*z
  old=rev;rev*=1+g;pg=min(p['pricegrowth'],g);units=max((1+g)/(1+pg)-1,0);da=[a/l for a,l in zip(assets,lives)]
  # New-capacity investment plus replacement-cost inflation; sales leverage never buys free restaurants.
  growth_cap=p['new_unit_capital_per_sales']*old*units;physical=max(.02*rev,da[0])+growth_cap+pg*assets[0];intang=max(t['intangibles']/t['revenue']*rev,da[1]+g*assets[1]);capex=[physical,intang];assets=[a+c-d for a,c,d in zip(assets,capex,da)];wc=p['wc']*max(rev-old,0);ebit=cm*rev-sum(da);fcff=ebit*(1-p['tax'])+sum(da)-sum(capex)-wc
  row=dict(year=yr,revenue=rev,growth=g,price_mix_growth=pg,capacity_volume_growth=units,cash_operating_margin=cm,da=da,ebit=ebit,funded_investment=capex,growth_capacity_capex=growth_cap,asset_stocks=assets[:],incremental_wc=wc,fcff=fcff);rows.append(row);pv+=fcff/(1+wacc)**yr
 ev=pv+fcff*(1+p['gterm'])/(wacc-p['gterm'])/(1+wacc)**1000;bridge=249.269-p['buffer']-p['legal']-p['frc'];pool=ev+bridge;alloc=allocate(pool,p);v10=sum(r['fcff']/(1+wacc)**r['year'] for r in rows[:10]);return dict(name=p['name'],parameters=p,wacc=wacc,ke=ke,kd=kd,enterprise_value=ev,equity_bridge=bridge,equity_pool_before_conversion_premium=pool,allocation=alloc,value_per_share=alloc['value_per_share'],terminal_share=(ev-v10)/ev,explicit_years=rows[:10],transition_years=rows[10:20],steady_state=rows[-2:])
results=[run(s) for s in scenarios];lo,hi=.05,.3
for _ in range(80):
 mid=(lo+hi)/2
 if run(scenarios[1],mid)['value_per_share']<price:lo=mid
 else:hi=mid
sens=[]
for w in [.08,.10,.12]:
 for g in [.02,.025,.03]:
  p=scenarios[1].copy();p['gterm']=g;p['beta']=((w-(rf+p['spread'])*(1-p['tax'])*wd)/(1-wd)-rf)/erp;sens.append(dict(wacc=w,g=g,value_per_share=run(p)['value_per_share']))
J('model_results.json',dict(scenarios=results,sensitivity=sens,inverse_cash_margin_year5_and10=(lo+hi)/2,inverse_note='Pre-D&A after rent, SBC, repairs, preopening costs and recurring corporate costs; all central funding/claims fixed.',approved_values=None))
qs=list(h['quarters'].values());checks=dict(three_annuals=len(h['annual'])==3,annual_revenue_correct=h['annual']['2025']['revenue']==3751.806,four_quarters_revenue=abs(sum(x['revenue'] for x in qs)-t['revenue'])<1e-8,four_quarters_cfo=abs(sum(x['cfo'] for x in qs)-t['cfo'])<1e-8,four_quarters_ebit=abs(sum(x['ebit'] for x in qs)-t['ebit'])<1e-8,economic_cash=abs(t['cash_after_capex_intangibles_sbc']-188.710)<1e-8,positive_profit=t['ni']>0 and t['ebit']>0,volume20=len(vol)==20,capital_funded=all(all(c>=d for c,d in zip(r['funded_investment'],r['da'])) for s in results for r in s['explicit_years']),terminal_capital_funded=all(all(c>=d for c,d in zip(s['steady_state'][-1]['funded_investment'],s['steady_state'][-1]['da'])) for s in results),wacc_gt_g=all(s['wacc']>s['parameters']['gterm'] for s in results),scenario_order=results[0]['value_per_share']<results[1]['value_per_share']<results[2]['value_per_share'],no_double_rent_claim=True,no_current_dividend_deduction=True,no_zero_unknown_frc_maximum=True,no_sbc_addback=True)
J('checks.json',checks);assert all(checks.values());print('values',[s['value_per_share'] for s in results],'beta',beta,'inverse',(lo+hi)/2)
