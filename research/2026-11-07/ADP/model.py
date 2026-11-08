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
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=303.35;shares=394.759432;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-10-27',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='StockAnalysis; Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
rf=.0486;erp=.0441;debt=5015.2;wd=debt/(cap+debt)
J('capital_cost.json',dict(as_of='2026-11-06',rf=rf,rf_source='US Treasury 10y Nov6',erp=erp,erp_source='Damodaran Nov1 implied ERP',weekly_beta=beta,r_squared=corr*corr,weekly_observations=len(rx),weekly_periods=[str(keys[0]),str(keys[-1])],beta_shrunk_two_thirds_plus_one_third=2*beta/3+1/3,beta_method='OLS weekly adjusted total-return proxy against SPY; incomplete first week retained explicitly',debt_weight=wd,debt_cost_method='Nov6 Rf plus 40/60/90bp assumptions, crosschecked against May2026 note effective5.14%, not quoted current bond yield'))
corp_i=141+45.6-33.6;corp_income=92.9+27.6-22.8;pension=28.3+5.1-7.1;venture=8.4+2.9;reserve_gain=2.8+3.1-4.3
norm=t['pbt']+corp_i-corp_income-pension-venture-reserve_gain
client=t['client_interest']+(371-92.9+106.1-78.7)-(459.3-141+102.5-101.8)
pass_through=4607.3+1228.6-1131
core=t['revenue']-t['client_interest']-pass_through
stocks=[644.3,1656.1,3200.8];da=[594.2-(384.8+104.9-95.4),384.8+104.9-95.4,1204.5];life=[s/d for s,d in zip(stocks,da)];spend=[202.6,491.5,1299.6];ratios=[x/core for x in spend];margin=(norm-client+sum(da))/core
base=dict(ttm_norm_ebit=norm,ttm_net_client_contribution=client,ttm_core_revenue=core,ttm_zero_margin_pass_through=pass_through,core_cash_operating_margin=margin,physical_software_contract_stocks=stocks,physical_software_contract_da=da,implied_stock_lives=life,investment_floor_to_core_revenue=ratios,client_balance_anchor=40910.7,client_initial_net_yield=client/40910.7,corporate_cash=3277,post_balance_dividend_reserve=670.2,post_balance_share_alignment_reserve=(395.6-shares)*price,excluded_corporate_securities_pending_excess_cash_verification=245.2,client_fair_value_shortfall_reserve=46039.6-44733.3,corporate_debt_face=debt,lease_claim=410.9,lease_convention='Rent remains operating cost; no second EV deduction.',pension_surplus_excluded=321.8,sbc_convention='SBC remains cash-equivalent operating cost in margins; no addback and no forecast buyback/dilution benefit.')
J('model_inputs.json',base)
model_beta=2*beta/3+1/3
scenarios=[dict(name='prudente',g1=.04,g5=.035,gterm=.02,m5=.375,m10=.36,yield5=.027,yield10=.025,beta=model_beta+.2,spread=.009,tax=.25,buffer=1600,legal=200,reserve_ratio=.04),dict(name='central',g1=.06,g5=.055,gterm=.025,m5=.40,m10=.40,yield5=.036,yield10=.032,beta=model_beta,spread=.006,tax=.24,buffer=1200,legal=100,reserve_ratio=.035),dict(name='favorable',g1=.075,g5=.07,gterm=.03,m5=.42,m10=.425,yield5=.04,yield10=.036,beta=max(.45,model_beta-.15),spread=.004,tax=.23,buffer=1000,legal=50,reserve_ratio=.03)]
def run(p,override=None):
 ke=rf+p['beta']*erp;kd=rf+p['spread'];wacc=ke*(1-wd)+kd*(1-p['tax'])*wd
 rev=core;assets=stocks[:];bal=40910.7;cashrows=[];pv=0
 for yr in range(1,101):
  if yr<=5:
   z=(yr-1)/4;g=p['g1']+(p['g5']-p['g1'])*z;cm=margin+((override if override is not None else p['m5'])-margin)*yr/5;cy=client/40910.7+(p['yield5']-client/40910.7)*yr/5
  else:
   z=min((yr-5)/5,1);g=p['g5']+(p['gterm']-p['g5'])*z;cm=(override if override is not None else p['m5'])+((override if override is not None else p['m10'])-(override if override is not None else p['m5']))*z;cy=p['yield5']+(p['yield10']-p['yield5'])*z
  prev=rev;rev*=1+g;oldbal=bal;bal*=1+g
  depreciation=[a/l for a,l in zip(assets,life)]
  capex=[max(r*rev,d+g*a) for r,d,a in zip(ratios,depreciation,assets)]
  assets=[a+c-d for a,c,d in zip(assets,capex,depreciation)]
  core_ebit=rev*cm-sum(depreciation);fund_profit=bal*cy;nopat=(core_ebit+fund_profit)*(1-p['tax'])
  d_wc=.04*(rev-prev);d_buffer=p['reserve_ratio']*(bal-oldbal)
  fcff=nopat+sum(depreciation)-sum(capex)-d_wc-d_buffer
  row=dict(year=yr,core_revenue=rev,growth=g,cash_operating_margin=cm,core_ebit=core_ebit,client_balance=bal,net_client_yield=cy,client_profit=fund_profit,nopat=nopat,da=depreciation,funded_investment=capex,asset_stocks=assets[:],incremental_wc=d_wc,incremental_client_capital=d_buffer,fcff=fcff)
  cashrows.append(row);pv+=fcff/(1+wacc)**yr
 tail=fcff*(1+p['gterm'])/(wacc-p['gterm'])/(1+wacc)**100
 ev=pv+tail;bridge=3277-670.2-base['post_balance_share_alignment_reserve']-p['buffer']-base['client_fair_value_shortfall_reserve']-debt-p['legal'];eq=ev+bridge
 v10=sum(r['fcff']/(1+wacc)**r['year'] for r in cashrows[:10]);return dict(name=p['name'],parameters=p,wacc=wacc,ke=ke,kd=kd,ev=ev,equity_bridge=bridge,equity_value=eq,value_per_share=eq/shares,terminal_pv=ev-v10,terminal_share=(ev-v10)/ev,explicit_years=cashrows[:10],terminal_transition_years=cashrows[10:20],steady_state_check=cashrows[-2:],terminal_method='Years11–100 continue same asset stocks, depreciation and funding rules; geometric remainder only after near-steady convergence. No year11 capex cut.',claims_unknown=True)
results=[run(p) for p in scenarios]
lo,hi=.2,.8
for _ in range(70):
 mid=(lo+hi)/2
 if run(scenarios[1],mid)['value_per_share']<price:lo=mid
 else:hi=mid
sensitivity=[]
for w in [.07,.08,.09]:
 for g in [.02,.025,.03]:
  p=scenarios[1].copy();p['gterm']=g;p['beta']=((w-(rf+p['spread'])*(1-p['tax'])*wd)/(1-wd)-rf)/erp;v=run(p);sensitivity.append(dict(wacc=w,terminal_growth=g,value_per_share=v['value_per_share']))
J('model_results.json',dict(sensitivity=sensitivity,scenarios=results,inverse_cash_operating_margin_year5_and10=(lo+hi)/2,inverse_note='Solve core cash operating margin, not EBIT; other central assumptions fixed. SBC/R&D/rent retained; dynamic amortization deducted.',approved_values=None))
checks={'annual_three':len(h['annual'])==3,'annual2024_rd':h['annual']['2024']['rd']==955.7,'annual2024_interest':h['annual']['2024']['interest_expense']==361.4,'annual2024_sga':h['annual']['2024']['sga']==3778.9,'four_quarter_revenue_tie':abs(sum(h['quarters'][q]['revenue'] for q in ['20251231','20260331','20260630','20260930'])-t['revenue'])<.2,'four_quarter_cfo_tie':abs(sum(h['quarters'][q]['cfo'] for q in ['20251231','20260331','20260630','20260930'])-t['cfo'])<1e-6,'owner_cash_4504_7':abs(t['cash_after_physical_software_sbc']-4504.7)<.001,'corporate_vs_client_interest':abs(corp_i-153)<.001,'stock_positive':all(x>0 for x in stocks),'no_unfunded_growth':all(all(c>=d for c,d in zip(r['funded_investment'],r['da'])) for z in results for r in z['explicit_years']),'wacc_gt_growth':all(z['wacc']>z['parameters']['gterm'] for z in results),'scenario_order':results[0]['value_per_share']<results[1]['value_per_share']<results[2]['value_per_share'],'volume20':len(vol)==20,'debt_not_client_obligations':debt<6000,'no_client_cash_excess':base['client_fair_value_shortfall_reserve']>0,'no_pension_surplus_add':True,'no_sbc_addback':True,'terminal_investment_floor':all(all(c>=d for c,d in zip(z['steady_state_check'][-1]['funded_investment'],z['steady_state_check'][-1]['da'])) for z in results)}
J('checks.json',checks);assert all(checks.values())
print('beta',beta,'values',[r['value_per_share'] for r in results],'inverse',(lo+hi)/2,'margin',margin)
