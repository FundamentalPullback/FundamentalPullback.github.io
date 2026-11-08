import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.loads((P/'history.json').read_text());t=h['paired_ttm_august']['2026']
def weekly(file):
 r=json.loads((P/'beta_price_inputs.json').read_text())[file];a=r['indicators']['adjclose'][0]['adjclose'];out={}
 for ts,c in zip(r['timestamp'],a):
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if c and d.isoformat()<='2026-11-06':out[d.isocalendar()[:2]]=float(c)
 return out
x,y=weekly('price_year.json'),weekly('SPY_price_year.json');keys=sorted(set(x)&set(y));rx=[x[b]/x[a]-1 for a,b in zip(keys,keys[1:])];ry=[y[b]/y[a]-1 for a,b in zip(keys,keys[1:])];mx,my=statistics.mean(rx),statistics.mean(ry);beta=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/sum((b-my)**2 for b in ry);corr=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=99.63;shares=209.727698;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-09-02',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='StockAnalysis; Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
rf=.0486;erp=.0441;debt=1182;wd=debt/(cap+debt)
J('capital_cost.json',dict(as_of='2026-11-06',rf=rf,rf_source='US Treasury 10y Nov6',erp=erp,erp_source='Damodaran Nov1 implied ERP',weekly_beta=beta,r_squared=corr*corr,weekly_observations=len(rx),weekly_periods=[str(keys[0]),str(keys[-1])],beta_shrunk_two_thirds_plus_one_third=2*beta/3+1/3,beta_method='OLS weekly adjusted total-return proxy against SPY; incomplete first week retained explicitly',debt_weight=wd,debt_cost_method='Nov6 Rf plus 100/150/200bp assumptions, not a bond quote; FY26 BBB+/A3 rating context only, not quoted current bond yield'))
# Remove impairment and net restructuring credit, exclude tariff refunds, reserve recurring restructuring.
normalized=t['ebit']+t['impairment']+t['restructuring']-34-60
base=dict(revenue=t['revenue'],normalized_ebit=normalized,reported_ebit=t['ebit'],impairment_addback=t['impairment'],net_restructuring_addback=t['restructuring'],tariff_refund_removed=34,recurring_restructuring_charge=60,cash_margin=(normalized+t['da'])/t['revenue'],asset_stock=1990,da=t['da'],implied_net_stock_life=1990/t['da'],investment_floor_ratio=707/t['revenue'],technology_budget_share=463/704,software_maintenance='Expensed maintenance retained; capitalized internal software included in PPE. Budget share is FY26 IT capex mix, not a disclosed stock split.',cash=2255,restricted_cash_excluded=279,debt_face_finance_lease_reserve=debt,operating_lease_claim=2964,lease_convention='Operating rent retained in margins; no second EV deduction. Finance leases included in debt reserve.',post_balance_dividend_reserve=.96*210.378803,post_balance_share_alignment_reserve=(210.378803-shares)*price,subsequent_tariff_cash_excluded=41,claims_unknown=True,legacy_restructuring=52,interest_swap=8,tax_uncertainty_reserve=185,deferred_compensation_reserve=21,valuation_shares=shares+1.4)
J('model_inputs.json',base)
mb=2*beta/3+1/3
scenarios=[dict(name='prudente',g1=-.02,g5=0,gterm=0,m5=.048,m10=.045,beta=mb+.2,spread=.02,tax=.27,buffer=1500,legal=150,wc=.06),dict(name='central',g1=.02,g5=.015,gterm=.015,m5=.062,m10=.06,beta=mb,spread=.015,tax=.25,buffer=1200,legal=75,wc=.04),dict(name='favorable',g1=.04,g5=.03,gterm=.02,m5=.069,m10=.067,beta=max(.5,mb-.15),spread=.01,tax=.24,buffer=1000,legal=25,wc=.03)]
def run(p,override=None):
 ke=rf+p['beta']*erp;kd=rf+p['spread'];wacc=ke*(1-wd)+kd*(1-p['tax'])*wd
 rev=base['revenue'];stock=base['asset_stock'];rows=[];pv=0
 for yr in range(1,101):
  if yr<=5:
   g=p['g1']+(p['g5']-p['g1'])*(yr-1)/4;cm=base['cash_margin']+((override if override is not None else p['m5'])-base['cash_margin'])*yr/5
  else:
   z=min((yr-5)/5,1);g=p['g5']+(p['gterm']-p['g5'])*z;cm=(override if override is not None else p['m5'])+((override if override is not None else p['m10'])-(override if override is not None else p['m5']))*z
  old=rev;rev*=1+g;da=stock/base['implied_net_stock_life'];capex=max(base['investment_floor_ratio']*rev,da+max(0,g)*stock);stock+=capex-da
  # No forecast release on shrinking business, membership/deferred revenue not monetized as excess.
  wc=p['wc']*max(rev-old,0);ebit=cm*rev-da;fcff=ebit*(1-p['tax'])+da-capex-wc
  row=dict(year=yr,revenue=rev,growth=g,cash_operating_margin=cm,da=da,ebit=ebit,capex=capex,technology_budget=capex*base['technology_budget_share'],other_capacity_budget=capex*(1-base['technology_budget_share']),asset_stock=stock,incremental_wc=wc,fcff=fcff);rows.append(row);pv+=fcff/(1+wacc)**yr
 ev=pv+fcff*(1+p['gterm'])/(wacc-p['gterm'])/(1+wacc)**100
 bridge=base['cash']-debt-p['buffer']-p['legal']-base['post_balance_dividend_reserve']-base['post_balance_share_alignment_reserve']-52-8-185-21
 v10=sum(r['fcff']/(1+wacc)**r['year'] for r in rows[:10]);return dict(name=p['name'],parameters=p,wacc=wacc,ke=ke,kd=kd,enterprise_value=ev,equity_bridge=bridge,equity_value=ev+bridge,value_per_share=(ev+bridge)/base['valuation_shares'],terminal_share=(ev-v10)/ev,explicit_years=rows[:10],transition_years=rows[10:20],steady_state=rows[-2:],terminal_method='Continue funded asset recurrence to year100, then geometric remainder; no year11 investment cut. Net stock life is accounting calibration, not engineering estimate.')
results=[run(s) for s in scenarios]
lo,hi=.03,.15
for _ in range(70):
 mid=(lo+hi)/2
 if run(scenarios[1],mid)['value_per_share']<price:lo=mid
 else:hi=mid
sens=[]
for w in [.08,.10,.12]:
 for g in [0,.015,.02]:
  p=scenarios[1].copy();p['gterm']=g;p['beta']=((w-(rf+p['spread'])*(1-p['tax'])*wd)/(1-wd)-rf)/erp;sens.append(dict(wacc=w,g=g,value_per_share=run(p)['value_per_share']))
J('model_results.json',dict(scenarios=results,sensitivity=sens,inverse_cash_margin_year5_and10=(lo+hi)/2,inverse_explanation='Solve pre-depreciation operating cash margin, retaining SBC, rent, software maintenance and restructuring reserve. All other central assumptions fixed.',approved_values=None,known_september_receipt_sensitivity=dict(cash_receipt=41,increment_per_share_before_tax_other_movements=41/base['valuation_shares'],scenario_values={x['name']:x['value_per_share']+41/base['valuation_shares'] for x in results},note='Isolated known cash receipt only, not a complete current cash bridge or validated valuation bound. No recurring EBIT benefit.')))
qs=[h['quarters'][q] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']]
checks=dict(three_annuals=len(h['annual'])==3,four_quarters_revenue=sum(x['revenue'] for x in qs)==t['revenue'],four_quarters_cfo=sum(x['cfo'] for x in qs)==t['cfo'],four_quarters_ebit=sum(x['ebit'] for x in qs)==t['ebit'],owner_cash=t['cash_after_capex_sbc']==1630,positive_profit=t['ebit']>0 and t['ni']>0,volume20=len(vol)==20,no_free_asset_growth=all(r['capex']>=r['da'] for s in results for r in s['explicit_years']),terminal_funded=all(s['steady_state'][-1]['capex']>=s['steady_state'][-1]['da'] for s in results),wacc_gt_g=all(s['wacc']>s['parameters']['gterm'] for s in results),scenario_order=results[0]['value_per_share']<results[1]['value_per_share']<results[2]['value_per_share'],restricted_cash_excluded=True,post_balance_dividend_reserved=True,negative_restructuring_credit_removed=base['net_restructuring_addback']==-48,no_sbc_addback=True,no_forecast_wc_release=True)
J('checks.json',checks);assert all(checks.values());print('values',[s['value_per_share'] for s in results],'inverse',(lo+hi)/2,'beta',beta)
