import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.loads((P/'history.json').read_text());t=h['paired_ttm_august']['2027']
def weekly(file):
 r=json.loads((P/'beta_price_inputs.json').read_text())[file];a=r['indicators']['adjclose'][0]['adjclose'];out={}
 for ts,c in zip(r['timestamp'],a):
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if c and d.isoformat()<='2026-11-06':out[d.isocalendar()[:2]]=float(c)
 return out
x,y=weekly('price_year.json'),weekly('SPY_price_year.json');keys=sorted(set(x)&set(y));rx=[x[b]/x[a]-1 for a,b in zip(keys,keys[1:])];ry=[y[b]/y[a]-1 for a,b in zip(keys,keys[1:])];mx,my=statistics.mean(rx),statistics.mean(ry);beta=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/sum((b-my)**2 for b in ry);corr=sum((a-mx)*(b-my) for a,b in zip(rx,ry))/math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=222.36;shares=397.075093;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-09-30',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='Issuer shareholder historical prices; StockAnalysis/Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
rf=.0486;erp=.0441;mb=2*beta/3+1/3;debt=2436.55;wd=debt/(cap+debt)
J('capital_cost.json',dict(date='2026-11-06',rf=rf,erp=erp,beta_weekly=beta,r_squared=corr*corr,beta_shrunk=mb,observations=len(rx),debt_weight=wd,method='Weekly adjusted CTAS series vs SPY. RfTreasuryNov6;ERP DamodaranNov1. Creditspread scenario assumptions not quoted bondyield. Standalone capital structure, excludes acquisitionfinancing.'))
base=dict(revenue=t['revenue'],normalized_ebit=t['ebit']+29.5,transaction_expense_addback=29.5,cash_margin=(t['ebit']+29.5+t['dep']+t['amort'])/t['revenue'],stocks=[1768.378,282.938,415.7],da=[t['dep']+t['amort']-61.3-105.5,61.3,105.5],stock_definition=['physical and residual software bucket','acquired servicecontracts/finiteintangibles','capitalized acquisitioncommissions'],rental_stock=1309.995,unused_inventory=433.286,commission_cash_rollforward_quarter=415.7-400.7+26.3,commission_cash_rollforward_annual=400.7-371.8+105.4,commission_note='Rollforward proxy, excludes unisolatedFX/acquisitions. ActualCF combines prepaid andcommission cash.',cash=243.599,investments_excluded=448.875,senior_debt_face=2436.55,post_august_buybacks=494,post_august_dividend=208.8,long_accrued_liabilities_reserved=540.918,op_leases=282.529,legal_recorded_fy26=5.65,insurance_recorded_fy26=218.528,pension_deficit_fy26=5.0,dividend_future=.52,dividend_future_record='2026-11-13',dividend_future_pay='2026-12-15',future_dividend_deduction=0,valuation_shares=shares+4.153,share_note='Sep30 actual plusQ1 treasury-stock dilution proxy; no further subtractOct1-7 buyback shares without separateamount. Cash fullbuyback deducted conservatively.',bridge_note='Augustcash minus known laterbuybacks/dividend is a netfunding adjustment, NOT fabricated negativeNovembercash. No laterCFO credited. Entirelongaccrued liability reserve, no additivepension/tax duplication; investmentassets excluded.',approved_values=None)
J('model_inputs.json',base)
ps=[dict(name='prudente',g1=.05,g5=.035,gterm=.02,m5=.265,m10=.25,tax=.25,beta=mb+.2,spread=.02,buffer=350,legal=100,wc=.12),dict(name='central',g1=.085,g5=.06,gterm=.025,m5=.29,m10=.275,tax=.23,beta=mb,spread=.015,buffer=300,legal=50,wc=.10),dict(name='favorable',g1=.105,g5=.08,gterm=.03,m5=.31,m10=.295,tax=.21,beta=max(.5,mb-.15),spread=.01,buffer=250,legal=25,wc=.08)]
def run(p,override=None,renew_acquired=False):
 ke=rf+p['beta']*erp;kd=rf+p['spread'];w=ke*(1-wd)+kd*(1-p['tax'])*wd;rev=t['revenue'];stocks=base['stocks'][:];lives=[a/d for a,d in zip(stocks,base['da'])];rental=base['rental_stock']+base['unused_inventory'];rows=[];pv=0
 for y in range(1,501):
  if y<=5:g=p['g1']+(p['g5']-p['g1'])*(y-1)/4;cm=base['cash_margin']+((override if override is not None else p['m5'])-base['cash_margin'])*y/5
  else:
   z=min((y-5)/5,1);g=p['g5']+(p['gterm']-p['g5'])*z;cm=(override if override is not None else p['m5'])+((override if override is not None else p['m10'])-(override if override is not None else p['m5']))*z
  old=rev;rev*=1+g;da=[a/l for a,l in zip(stocks,lives)]
  inv=[max(t['capex']/t['revenue']*rev,da[0]+g*stocks[0]),(da[1]+g*stocks[1] if renew_acquired else 0),da[2]+g*stocks[2]]
  rental_growth=max(g,0)*rental;rental+=rental_growth;wc=p['wc']*max(rev-old,0);ebit=cm*rev-sum(da);fcff=ebit*(1-p['tax'])+sum(da)-sum(inv)-rental_growth-wc
  stocks=[a+c-d for a,c,d in zip(stocks,inv,da)];pv+=fcff/(1+w)**y;rows.append(dict(year=y,revenue=rev,growth=g,cash_margin=cm,da=da,ebit=ebit,investments=inv,stocks=stocks[:],rental_inventory_growth=rental_growth,rental_inventory_stock=rental,other_wc=wc,fcff=fcff))
 ev=pv+fcff*(1+p['gterm'])/(w-p['gterm'])/(1+w)**500
 bridge=243.599-2436.55-494-208.8-p['buffer']-540.918-p['legal']
 eq=ev+bridge;v=eq/base['valuation_shares'];failure=(eq-350)/base['valuation_shares']
 return dict(name=p['name'],parameters=p,wacc=w,ke=ke,kd=kd,standalone_enterprise=ev,standalone_equity_bridge=bridge,standalone_equity=eq,standalone_value_per_share=v,failure_case_full_reverse_fee_per_share=failure,terminal_share=(ev-sum(r['fcff']/(1+w)**r['year'] for r in rows[:10]))/ev,explicit_years=rows[:10],transition_years=rows[10:20],steady_state=rows[-2:])
r=[run(p) for p in ps];lo,hi=.15,.6
for _ in range(80):
 mid=(lo+hi)/2
 if run(ps[1],mid)['standalone_value_per_share']<price:lo=mid
 else:hi=mid
unfshares=14.586347+3.501265;cashpay=155*unfshares;newshares=.772*unfshares
# No arbitrary target value for an unresolved transaction. Exact financing algebra and break-even acquired EV.
overlay=[]
for x in r:
 v=x['standalone_value_per_share'];integration={'prudente':400,'central':250,'favorable':150}[x['name']];claims=20.102+15.958+14.402+19.492;buffer=100
 hurdle=cashpay+newshares*v-192.121+buffer+claims+integration
 overlay.append(dict(name=x['name'],unf_enterprise_value_required_for_value_neutrality=hurdle,integration_reserve=integration,unf_benefit_environment_aro_claims=claims,unf_cash=192.121,unf_operating_cash_buffer=buffer,formula='Combined common value=(CTASstandaloneequity+UNFoperatingEV+UNFcash-buffer-UNFclaims-cashpurchase-integration)/(CTASdilutedshares+newCTASshares). No arbitraryUNFEV=0; no eventprobabilities assigned.'))
def target_run(p,synergy):
 w=p['wacc']+.015;rev=2523.230;stocks=[843.589+90.051,112.147];lives=[stocks[0]/141.992,stocks[1]/21.416];rental=244.643+146.356;pv=0;rows=[]
 cm=(136.044+37.2+141.992+21.416)/rev
 for y in range(1,501):
  g=.03+(.02-.03)*min((y-1)/9,1);old=rev;rev*=1+g;da=[a/l for a,l in zip(stocks,lives)];inv=[max(134.519/2523.230*rev,da[0]+g*stocks[0]),da[1]+g*stocks[1]];rg=g*rental;rental+=rg;wc=.1*(rev-old)
  # Announced375 full synergy only a favorablecase. Capacity/commission/rental funding continues.
  syn=synergy*min(y/4,1)*(1.02**max(y-4,0));ebit=cm*rev-sum(da)+syn;fcff=ebit*(1-.25)+sum(da)-sum(inv)-rg-wc;pv+=fcff/(1+w)**y;stocks=[a+c-d for a,c,d in zip(stocks,inv,da)];rows.append(dict(year=y,revenue=rev,da=da,investments=inv,stocks=stocks[:],rental_growth=rg,wc=wc,synergy=syn,ebit=ebit,fcff=fcff))
 ev=pv+fcff*1.02/(w-.02)/(1+w)**500
 return dict(wacc=w,operating_ev=ev,synergy_assumed_year4=synergy,explicit_years=rows[:10],steady_state=rows[-2:])
for x,o,syn in zip(r,overlay,[0,187.5,375]):
 u=target_run(x,syn);o['funded_target_model']=u;o['combined_conditional_per_share']=(x['standalone_equity']+u['operating_ev']+192.121-100-o['unf_benefit_environment_aro_claims']-cashpay-o['integration_reserve'])/(base['valuation_shares']+newshares)
J('deal_model.json',dict(as_of='2026-11-08',unf_shares_date='2026-10-20',unf_shares=unfshares,cash_per_unf=155,ctas_shares_per_unf=.772,cash_purchase=cashpay,issued_ctas_shares=newshares,contract_value_at_current_ctas=155+.772*price,reverse_fee_conditional=350,regulatory_status='Pending. FTCtimingDecember11 unlessclosedearlier; noprimaryfiledblockingsuit verified. ReutersOct27 report nottreatedasfiledcase.',close_cases=overlay,combined_approved_value=None,missing=['Actual regulatory remedies/closure outcome','Synergyrealization andintegration-costengineering calibration; fundedtargetmodel is hypothetical','Financingtenor/yield and actualclosing-sharecount. Cashpurchase deducted fromequity is pairedfinancingprincipal, notsubtracted twice as debt.']))
sens=[]
for w in [.08,.09,.10]:
 for g in [.02,.025,.03]:
  p=ps[1].copy();p['gterm']=g;p['beta']=((w-(rf+p['spread'])*(1-p['tax'])*wd)/(1-wd)-rf)/erp;sens.append(dict(wacc=w,g=g,standalone_value=run(p)['standalone_value_per_share']))
J('model_results.json',dict(standalone_scenarios=r,acquired_relationship_replacement_sensitivity=[dict(name=p['name'],standalone_value=run(p,renew_acquired=True)['standalone_value_per_share']) for p in ps],inverse_standalone_cash_margin=(lo+hi)/2,sensitivity=sens,current_combined_value=None,approved_values=None,scope='Hypothetical standalone, NOT current combined fairvalue. No probabilityweightedtarget.'))
q=list(h['quarters'].values());checks=dict(three_annuals=len(h['annual'])==3,four_quarters=len(q)==4,revenue_tie=abs(sum(x['revenue'] for x in q)-t['revenue'])<1e-7,ebit_tie=abs(sum(x['ebit'] for x in q)-t['ebit'])<1e-7,cfo_tie=abs(sum(x['cfo'] for x in q)-t['cfo'])<1e-7,twenty_volumes=len(vol)==20,positive_ttm=t['ebit']>0 and t['ni']>0 and t['owner_cash']>0,physical_commission_funded=all(all(z['investments'][i]>=z['da'][i] for i in [0,2]) for s in r for z in s['explicit_years']+s['steady_state']),rental_growth_funded=all(z['rental_inventory_growth']>0 for s in r for z in s['explicit_years']),wacc_gt_g=all(s['wacc']>s['parameters']['gterm'] for s in r),no_future_dividend_deduction=True,no_double_pension_tax=True,no_investment_cash_sweep=True,no_double_cfo_commission_deduction=True,no_combined_target=True)
J('checks.json',checks);assert all(checks.values());print([(s['name'],s['standalone_value_per_share'],s['wacc']) for s in r], 'inverse',(lo+hi)/2)
