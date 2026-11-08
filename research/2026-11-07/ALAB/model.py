import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent;J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.load(open(P/'history.json'));t=h['paired_ttm_september']['2026'];price=190.71;basic=174.782075;vest_options=1.672;vest_warrants=1.866936;shares=basic+vest_options+vest_warrants
rows=list(csv.DictReader((P/'daily_closes.csv').open()));rows=[r for r in rows if r['date']<='2026-11-06'];cl=[float(r['close']) for r in rows]
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};hi=max(float(r['high']) for r in rows[-252:]);vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));pull=1-price/hi
J('market.json',dict(date='2026-11-06',session='NASDAQ regular close 16:00 EST',price=price,basic_shares_m=basic,share_date='2026-10-31',market_cap=price*basic,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),high252=hi,pullback=pull,volume20=sum(float(r['volume']) for r in vol)/20,technical_entry_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,no_split_assumed=True))
def weekly(fn):
 r=json.loads((P/'beta_price_inputs.json').read_text())[fn];o={}
 for ts,c in zip(r['timestamp'],r['indicators']['adjclose'][0]['adjclose']):
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if c and d.isoformat()<='2026-11-06':o[d.isocalendar()[:2]]=c
 return o
x,y=weekly('price_year.json'),weekly('SPY_price_year.json');ks=sorted(set(x)&set(y));rx=[x[b]/x[a]-1 for a,b in zip(ks,ks[1:])];ry=[y[b]/y[a]-1 for a,b in zip(ks,ks[1:])];mx,my=statistics.mean(rx),statistics.mean(ry);cov=sum((a-mx)*(b-my) for a,b in zip(rx,ry));beta=cov/sum((b-my)**2 for b in ry);r2=cov**2/(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry));rf=.0486;erp=.0441
J('capital_cost.json',dict(date='2026-11-06',rf=rf,erp=erp,rf_source='Treasury10y Nov6',erp_source='Damodaran Nov1',ols_beta=beta,weekly_observations=len(rx),r_squared=r2,model_beta=2*beta/3+1/3,method='104 weekly adjusted-price returns against SPY; 2/3 regression +1/3 unit prior. Scenario beta +/-0.3. No current debt, WACC=Ke.',period=[str(ks[0]),str(ks[-1])]))
basepre=(t['ebit']+t['da']+t['sbc'])/t['revenue'];bsc=t['sbc']/t['revenue'];capitalratio=abs(t['capex'])/t['revenue'];active=170.713-65.609;cip=65.609
J('model_inputs.json',dict(revenue_ttm=t['revenue'],pre_sbc_cash_operating_margin=basepre,sbc_ratio_ttm=bsc,capital_budget_ratio=capitalratio,physical_net=170.713,cip=cip,active=active,modeled_active_life=4.5,life_source='Production masks5y per issuer, aggregate4.5y analyst assumption for mix/lab/leasehold; not stock/low historical DA.',rd_ttm=t['rd'],cash=209.396,marketable_securities=1168.847,borrowed_debt=0,opening_capex_payable=19.266,opening_software_license_payable=12.82,acquisition_holdback=5,customer_warrant_convention='Future contra-revenue retained as cash-equivalent customer concession within net sales and margins; no addback or simultaneous future warrant dilution. Existing vested warrants included in denominator with zero exercise proceeds conservatively.',employee_convention='SBC retained as future economic cost, minimum annual legacy amortization about397m during first2years; no buyback benefit. Vested options included; unvested RSU/PSU service-earned split unresolved, separate full-shadow sensitivity.',basic_shares=basic,vested_options=vest_options,vested_customer_warrants=vest_warrants,model_shares=shares,unvested_rsu_psu_shadow=8.789))
sc=[dict(name='prudente',g1=.65,g2=.25,g5=.10,gterm=.025,pre1=.43,pre5=.45,pre10=.42,sbc5=.13,sbc10=.13,tax=.25,beta=2*beta/3+1/3+.3,wc=.30,buffer=250,claim=20),dict(name='central',g1=.95,g2=.45,g5=.20,gterm=.03,pre1=.47,pre5=.49,pre10=.46,sbc5=.11,sbc10=.10,tax=.23,beta=2*beta/3+1/3,wc=.25,buffer=175,claim=10),dict(name='favorable',g1=1.15,g2=.60,g5=.30,gterm=.035,pre1=.50,pre5=.53,pre10=.50,sbc5=.09,sbc10=.08,tax=.21,beta=max(1,2*beta/3+1/3-.3),wc=.22,buffer=125,claim=5)]
def run(p,override=None):
 w=rf+p['beta']*erp;r=t['revenue'];stock=active;construction=cip;out=[];pv=0
 for yr in range(1,101):
  if yr==1:g=p['g1'];pre=p['pre1'];sbc=.14
  elif yr<=5:
   z=(yr-1)/4;g=(override if override is not None else p['g2']+(p['g5']-p['g2'])*(yr-2)/3);pre=p['pre1']+(p['pre5']-p['pre1'])*z;sbc=.14+(p['sbc5']-.14)*z
  else:
   z=min((yr-5)/5,1);g=(override if override is not None else p['g5'])*(1-z)+p['gterm']*z;pre=p['pre5']+(p['pre10']-p['pre5'])*z;sbc=p['sbc5']+(p['sbc10']-p['sbc5'])*z
  oldr=r;r*=1+g
  # Commission existing CIP over first two years, no duplicate capital spend.
  commission=min(construction,cip/2) if yr<=2 else 0;construction-=commission
  dep=(stock+.5*commission)/4.5
  investment=max(capitalratio*r,dep+g*stock)
  stock+=commission+investment-dep
  sbc_cost=max(r*sbc,397 if yr<=2 else 0)
  ebit=r*pre-sbc_cost-dep;nopat=ebit*(1-p['tax']);dwc=p['wc']*(r-oldr);fcff=nopat+dep-investment-dwc
  row=dict(year=yr,revenue=r,growth=g,pre_sbc_cash_margin=pre,sbc_cost=sbc_cost,sbc_ratio=sbc_cost/r,commissioned_cip=commission,depreciation=dep,active_stock=stock,remaining_cip=construction,capex=investment,delta_wc=dwc,ebit=ebit,ebit_margin=ebit/r,fcff=fcff)
  out.append(row);pv+=fcff/(1+w)**yr
 tail=fcff*(1+p['gterm'])/(w-p['gterm'])/(1+w)**100;ev=pv+tail;bridge=209.396+1168.847-p['buffer']-19.266-12.82-5-p['claim'];eq=ev+bridge;explicitpv=sum(z['fcff']/(1+w)**z['year'] for z in out[:10])
 return dict(name=p['name'],assumptions=p,wacc=w,ev=ev,equity_bridge=bridge,equity_value=eq,value_per_share=eq/shares,full_unvested_award_shadow_value=eq/(shares+8.789),terminal_pv_share=(ev-explicitpv)/ev,explicit_years=out[:10],terminal_transition=out[10:20],steady_state=out[-2:])
results=[run(p) for p in sc];lo,hi=.01,1.5
for _ in range(70):
 mid=(lo+hi)/2
 if run(sc[1],mid)['value_per_share']<price:lo=mid
 else:hi=mid
inverse=run(sc[1],(lo+hi)/2);sensitivity=[]
for w in [.12,.15,.18]:
 for g in [.025,.03,.035]:
  p=sc[1].copy();p['beta']=(w-rf)/erp;p['gterm']=g;sensitivity.append(dict(wacc=w,terminal_growth=g,value=run(p)['value_per_share']))
J('model_results.json',dict(scenarios=results,inverse_growth_years2_to5=(lo+hi)/2,inverse_year5_revenue=inverse['explicit_years'][4]['revenue'],inverse_year10_revenue=inverse['explicit_years'][9]['revenue'],inverse_note='Year1 central revenue, margins/funding unchanged; solve constant growth years2–5 then taper by year10.',sensitivity=sensitivity,approved_values=None,terminal_method='Same funded asset dynamics after year10; finite computational tail100 plus stabilized geometric remainder. No physical budget cut.'))
checks={'three_annuals':len(h['annual'])==3,'annual2023_sales':h['annual']['2023']['revenue']==115.794,'fourq_revenue':abs(sum(h['quarters'][q]['revenue'] for q in ['20251231','20260331','20260630','20260930'])-t['revenue'])<.01,'fourq_cfo':abs(sum(h['quarters'][q]['cfo'] for q in ['20251231','20260331','20260630','20260930'])-t['cfo'])<.01,'positive_actual_ttm_ebit':t['ebit']>0,'positive_actual_ttm_income':t['net_income']>0,'cfo_less_capex_positive':t['cfo_less_capex']>0,'economic_cash_75_926':abs(t['economic_cash_after_sbc_customer_warrants']-75.926)<.001,'budget_no_terminal_cut':all(z['steady_state'][-1]['capex']/z['steady_state'][-1]['revenue']>=capitalratio-1e-8 for z in results),'cip_funded_once':all(abs(sum(r['commissioned_cip'] for r in z['explicit_years'])-cip)<1e-8 for z in results),'stock_positive':all(r['active_stock']>0 for z in results for r in z['explicit_years']),'sbc_floor_first2':all(r['sbc_cost']>=397 for z in results for r in z['explicit_years'][:2]),'wacc_above_g':all(z['wacc']>z['assumptions']['gterm'] for z in results),'scenario_order':results[0]['value_per_share']<results[1]['value_per_share']<results[2]['value_per_share'],'liquidity20':len(vol)==20}
J('checks.json',checks);assert all(checks.values());print('beta',beta,'values',[r['value_per_share'] for r in results],'inverse',(lo+hi)/2)
