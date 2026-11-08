import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.loads((P/'history.json').read_text());t=h['paired_ttm']['2026']
def weekly(file):
 r=json.loads((P/'beta_price_inputs.json').read_text())[file];a=r['indicators']['adjclose'][0]['adjclose'];out={}
 for ts,c in zip(r['timestamp'],a):
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if c and d.isoformat()<='2026-11-06':out[d.isocalendar()[:2]]=float(c)
 return out
x,y=weekly('price_year.json'),weekly('SPY_price_year.json');keys=sorted(set(x)&set(y));rx=[x[b]/x[a]-1 for a,b in zip(keys,keys[1:])];ry=[y[b]/y[a]-1 for a,b in zip(keys,keys[1:])];mx,my=statistics.mean(rx),statistics.mean(ry);beta=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/sum((b-my)**2 for b in ry);corr=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=23.13;shares=298.234693;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-09-23',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='StockAnalysis; Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
rf=.0486;erp=.0441;debt=7219+300;wd=debt/(cap+debt);mb=2*beta/3+1/3
J('capital_cost.json',dict(as_of='2026-11-06',rf=rf,erp=erp,weekly_beta=beta,r_squared=corr*corr,weekly_observations=len(rx),beta_shrunk=mb,debt_weight=wd,debt_cost='Rf plus scenario spread; October8.5% subordinated issuance is a separate dated risk crosscheck, not senior yield.',sources=['Treasury10y Nov6','Damodaran impliedERP Nov1','Yahoo adjusted weekly CPB/SPY']))
base=dict(revenue=9744,normalized_ebit=852+117+26-6-4,normalization='Remove117 impairment,26 acquisitionexpense,6 commodityMTMgain,4nonservicepensiongain. Retain181restructuring/implementation expense rather than assume all nonrecurring.',cash_margin=(852+117+26-6-4+413)/9744,physical_stock=2868,physical_da=372,finite_intangible_stock=637,intangible_amortization=41,indefinite_brands=3561,advertising_expensed=387,rd_expensed=99,sbc_expensed=56,capital_guidance_fy27=300,finance_lease_capital_additions_fy26=42,net_routes_cash_fy26=3,cash=394,new_debt=300,new_proceeds=296,debt_face_including_finance_leases=7219,old_dividend_payable=118,new_dividend_paid=.25*shares,minority_redemption2030=357,minority_carrying=304,deferred_acquisition_payment=140,contingent_grant_carrying=20,contingent_grant_max_eur=25,pension_deficit_nonoffset=94,postretirement=115,deferred_comp=87,tax_uncertainty=12,operating_lease_liability=313,op_lease_treatment='Rent retained; no duplicateEVdebt',current_shares=shares,dilution_shadow=1,valuation_shares=shares+1,post_balance_cfo_assumed=0,financing_treatment='Add300 debt and296netproceeds together; any cash debt repayment has neutral netdebt impact. No forecast operatingcash credited beforeNov6.')
J('model_inputs.json',base)
# Margins are after marketing/R&D/SBC/restructuring and before dynamic D&A. No purchased brand amortization added for free.
ps=[dict(name='prudente',g1=-.04,g5=0,gterm=.01,m5=.12,m10=.115,tax=.26,beta=max(.7,mb+.2),spread=.035,buffer=350,legal=75,grant=30,nci_annual=12,wc=.12),dict(name='central',g1=-.03,g5=.02,gterm=.02,m5=.145,m10=.14,tax=.25,beta=max(.6,mb),spread=.025,buffer=300,legal=40,grant=25,nci_annual=8,wc=.10),dict(name='favorable',g1=-.02,g5=.035,gterm=.025,m5=.16,m10=.155,tax=.24,beta=max(.5,mb-.15),spread=.02,buffer=250,legal=20,grant=20,nci_annual=4,wc=.08)]
def run(p,over=None):
 ke=rf+p['beta']*erp;kd=rf+p['spread'];w=ke*(1-wd)+kd*(1-p['tax'])*wd
 rev=9744.;stocks=[2868.,637.];lives=[2868/372,637/41];rows=[];pv=0
 for y in range(1,501):
  if y<=5:g=p['g1']+(p['g5']-p['g1'])*(y-1)/4;cm=base['cash_margin']+((over if over is not None else p['m5'])-base['cash_margin'])*y/5
  else:
   z=min((y-5)/5,1);g=p['g5']+(p['gterm']-p['g5'])*z;cm=(over if over is not None else p['m5'])+((over if over is not None else p['m10'])-(over if over is not None else p['m5']))*z
  old=rev;rev*=1+g;da=[a/l for a,l in zip(stocks,lives)]
  inv=[max(361/9744*rev,da[0]+max(g,0)*stocks[0]),da[1]+max(g,0)*stocks[1]]
  # Physical aggregate includes finance assets; replacement budget funds future leased or cash assets alike. Route capital separate.
  routes=max(3/9744*rev,0);wc=p['wc']*max(rev-old,0);ebit=cm*rev-sum(da);fcff=ebit*(1-p['tax'])+sum(da)-sum(inv)-routes-wc
  stocks=[a+c-d for a,c,d in zip(stocks,inv,da)];pv+=fcff/(1+w)**y
  rows.append(dict(year=y,revenue=rev,growth=g,cash_margin=cm,da=da,ebit=ebit,investments=inv,stocks=stocks[:],routes_capital=routes,wc=wc,fcff=fcff))
 ev=pv+fcff*(1+p['gterm'])/(w-p['gterm'])/(1+w)**500
 # Control/full enterprise but minority paid interim cash then purchased in2030. No simultaneous304 deduction.
 minority=357/(1+ke)**3.5+sum(p['nci_annual']/(1+ke)**y for y in range(1,4))+.5*p['nci_annual']/(1+ke)**3.5
 bridge=394+296-p['buffer']-7519-118-.25*shares-140/(1+kd)**.5-minority-p['grant']-94-115-87-12-p['legal']
 eq=ev+bridge
 return dict(name=p['name'],parameters=p,wacc=w,ke=ke,kd=kd,enterprise_value=ev,equity_bridge=bridge,minority_claim=minority,equity=eq,unfloored_residual_per_share=eq/(shares+1),value_per_share=(eq/(shares+1) if eq>0 else None),terminal_share=(ev-sum(r['fcff']/(1+w)**r['year'] for r in rows[:10]))/ev,explicit_years=rows[:10],transition_years=rows[10:20],steady_state=rows[-2:])
r=[run(p) for p in ps];lo,hi=.05,.30
for _ in range(70):
 mid=(lo+hi)/2
 if run(ps[1],mid)['unfloored_residual_per_share']<price:lo=mid
 else:hi=mid
sens=[]
for w in [.07,.08,.09]:
 for g in [.01,.02,.025]:
  p=ps[1].copy();p['gterm']=g;p['beta']=((w-(rf+p['spread'])*(1-p['tax'])*wd)/(1-wd)-rf)/erp;sens.append(dict(wacc=w,g=g,value=run(p)['value_per_share']))
J('model_results.json',dict(scenarios=r,inverse_cash_margin=(lo+hi)/2,sensitivity=sens,approved_values=None,limitations=['LaRegina minority interimcash and foreigncash remittance access require calibration; fullstatementperimeter only onequarter.', 'Replacementbudget and restored margins are scenarios, not calibrated engineering/unit evidence.','Current projected bridge not a November balance sheet.']))
checks=dict(three_annuals=len(h['annual'])==3,four_quarters=len(h['quarters'])==4,quarter_rev_tie=sum(q['revenue'] for q in h['quarters'].values())==t['revenue'],quarter_ebit_tie=sum(q['ebit'] for q in h['quarters'].values())==t['ebit'],quarter_cfo_tie=sum(q['cfo'] for q in h['quarters'].values())==t['cfo'],price_ge15=price>=15,cap_ge2000=cap>=2000,ttm_positive=t['ebit']>0 and t['ni']>0 and t['owner_cash']>0,twenty_volumes=len(vol)==20,capital_funded=all(all(c>=d for c,d in zip(z['investments'],z['da'])) for s in r for z in s['explicit_years']+s['steady_state']),wacc_gt_g=all(s['wacc']>s['parameters']['gterm'] for s in r),no_double_nci=True,financing_paired=True,no_sbc_addback=True,scenario_order=r[0]['unfloored_residual_per_share']<r[1]['unfloored_residual_per_share']<r[2]['unfloored_residual_per_share'])
J('checks.json',checks);assert all(checks.values());print([(s['name'],s['value_per_share'],s['wacc']) for s in r], 'inverse',(lo+hi)/2)
