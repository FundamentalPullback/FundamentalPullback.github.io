"""Own ECO FCFF with funded cohort replacement. All capital after June is explicitly estimated."""
import pathlib,json,csv,copy
P=pathlib.Path(__file__).parent
PRICE=93.26;SHARES=39.044655
FLEET=[('Milos','Suezmax',2016),('Poliegos','Suezmax',2017),('Kimolos','Suezmax',2018),('Folegandros','Suezmax',2018),('Nissos Sikinos','Suezmax',2020),('Nissos Sifnos','Suezmax',2020),('Nissos Piperi','Suezmax',2026),('Nissos Serifopoula','Suezmax',2026),('Nissos Tigani','Suezmax',2026),('Nissos Vous','Suezmax',2026)]+[(n,'VLCC',y)for n,y in [('Nissos Rhenia',2019),('Nissos Despotiko',2019),('Nissos Donoussa',2019),('Nissos Kythnos',2019),('Nissos Keros',2019),('Nissos Anafi',2020),('Nissos Kea',2022),('Nissos Nikouria',2022)]]
REPLACEMENT={'VLCC':136,'Suezmax':99.3};SCRAP={'VLCC':20,'Suezmax':12}
# July1-Nov3 CFO is a scenario, not reported cash. Issuer June balance, July draw/delivery and August dividend.
CAPITAL={'June_unrestricted_cash':222.591472,'June_restricted_cash_excluded':25.215431,'June_loan_principal':726.797584,'June_office_lease':.050171,'July_new_loan':45,'Vous_remaining_delivery_payment':79.4,'August_dividend':SHARES*5.25,'July1_Nov3_CFO_assumption':300,'July1_Nov3_other_capex_assumption':5,'July1_Nov3_principal_repayments_assumption':18,'operating_cash_reserve':40,'retirement_claim':.061629}
def capital(cfo=300,reserve=40):
 cash=CAPITAL['June_unrestricted_cash']+45-79.4-CAPITAL['August_dividend']+cfo-5-18
 debt=726.797584+45-18
 # Net liquid cash may be below reserve: negative net cash is a funding deficit, not clipped away.
 claims=debt+.050171+.061629-(cash-reserve)
 return {'estimated_cash':cash,'estimated_debt_principal':debt,'operating_reserve':reserve,'net_claims':claims,'preforecast_CFO_assumption':cfo,'not_measured_November_balance':True}
BASE={'rates':{'VLCC':[220000,120000,85000,70000,62500],'Suezmax':[130000,80000,60000,50000,45000]},'wacc':.105,'g':.02,'roic':.12,'util':.97,'tax':.01,'life':20,'cfo':300,'opex_scale':1,'replacement_scale':1,'charter_days':106}
SCENARIOS={'base':BASE,'bear':dict(BASE,renew=False,rates={'VLCC':[140000,75000,55000,45000,40000],'Suezmax':[85000,55000,40000,35000,30000]},wacc=.12,g=.015,roic=.10,util=.94,cfo=200,replacement_scale=1.15),'bull':dict(BASE,rates={'VLCC':[300000,180000,120000,95000,85000],'Suezmax':[180000,120000,85000,70000,60000]},wacc=.095,g=.025,roic=.15,util=.985,cfo=400)}
def calculate_renew(s,normal_shift=0,reserve=40):
 s=copy.deepcopy(s);rows=[];previous=None;life=s['life'];infl=1;w=s['wacc'];g=s['g'];renewal=sum((REPLACEMENT[k]-SCRAP[k])*s['replacement_scale']/life for _,k,_ in FLEET)
 for i in range(1,11):
  if i>1:infl*=1.02 if i<=5 else 1+g
  rates={k:(v[i-1]+normal_shift*(i-1)/4*(1 if k=='VLCC' else .75))if i<=5 else(v[-1]+normal_shift*(1 if k=='VLCC' else .75))*(1+g)**(i-5)for k,v in s['rates'].items()}
  tce=sum(365*s['util']*rates[k]/1e6 for _,k,y in FLEET)
  if i==1:tce+=(90000-rates['VLCC'])*s.get('charter_days',106)/1e6
  opex=18*365*10000*infl*s['opex_scale']/1e6;ga=20*infl;da=60*infl;ebit=tce-opex-ga-da;tax=max(0,ebit)*s['tax'];nopat=ebit-tax
  wc=0 if previous is None else .08*(tce-previous)
  dry=8*infl;hull_normal=renewal*infl
  # Conservative end-of-period cohort convention: replacement at build year + life.
  actual=sum((REPLACEMENT[k]-SCRAP[k])*infl*s['replacement_scale'] for _,k,y in FLEET if 2026+i>=y+life and(2026+i-y)%life==0)
  minimum_net=hull_normal+dry-da+wc;growth_charge=max(0,nopat)*g/s['roic'];blend=max(0,(i-5)/5)
  additional=max(0,growth_charge-minimum_net)*blend
  capex=actual+dry+additional;fcff=nopat+da-capex-wc
  rows.append({'year':i,'period_end_year':2026+i,'TCE_rates':rates,'TCE_revenue':tce,'vessel_opex':opex,'GA':ga,'economic_DA':da,'EBIT':ebit,'tax':tax,'NOPAT':nopat,'working_capital':wc,'drydock_capex':dry,'normalized_hull_reserve':hull_normal,'actual_hull_replacement_net_scrap':actual,'additional_growth_investment':additional,'total_capex':capex,'FCFF':fcff,'PV':fcff/(1+w)**i});previous=tce
 last=rows[-1];tn=last['NOPAT']*(1+g);td=last['economic_DA']*(1+g);tdry=last['drydock_capex']*(1+g);tr=last['normalized_hull_reserve']*(1+g);tw=.08*last['TCE_revenue']*g;tre=max(tr+tdry-td+tw,tn*g/s['roic']);tfc=tn-tre;tv_smooth=tfc/(w-g)
 tail=0
 for j in range(1,life+1):
  inflation=infl*(1+g)**j;year=2036+j;actual=sum((REPLACEMENT[k]-SCRAP[k])*inflation*s['replacement_scale']for _,k,y in FLEET if year>=y+life and(year-y)%life==0)
  tail+=(renewal*inflation-actual)/(1+w)**j
 correction=tail/(1-((1+g)/(1+w))**life);tv=tv_smooth+correction;pvt=tv/(1+w)**10;pv=sum(x['PV']for x in rows);bridge=capital(s['cfo'],reserve);ev=pv+pvt
 return {'assumptions':s,'capital_bridge_estimated':bridge,'rows':rows,'PV_flows':pv,'terminal_nopat':tn,'terminal_net_reinvestment':tre,'terminal_fcff':tfc,'terminal_smooth_value':tv_smooth,'terminal_cohort_correction':correction,'terminal_value':tv,'PV_terminal':pvt,'terminal_weight':pvt/ev,'EV':ev,'equity':ev-bridge['net_claims'],'shares':SHARES,'value':(ev-bridge['net_claims'])/SHARES,'normalized_hull_reserve_year1':renewal,'calendar':'Ten forward annual periods from November4 2026; year-end cohort convention, not FY forecasts. July1-Nov3 capital estimated separately.'}
def calculate(s,normal_shift=0,reserve=40):
 a=calculate_renew(s,normal_shift,reserve)
 if s.get('renew',True):return a
 rows=[];previous=None;infl=1;life=s['life']
 for i in range(1,life+1):
  if i>1:infl*=1.02 if i<=5 else 1+s['g']
  year=2026+i;active=[(n,k,y)for n,k,y in FLEET if year<=y+life]
  if not active:continue
  rates={k:(v[i-1]+normal_shift*(i-1)/4*(1 if k=='VLCC' else .75))if i<=5 else(v[-1]+normal_shift*(1 if k=='VLCC' else .75))*(1+s['g'])**(i-5)for k,v in s['rates'].items()}
  tce=sum(365*s['util']*rates[k]/1e6 for _,k,_ in active)
  if i==1:tce+=(90000-rates['VLCC'])*s.get('charter_days',106)/1e6
  n=len(active);opex=n*365*10000*infl*s['opex_scale']/1e6;ga=20*infl*n/18;da=60*infl*n/18;ebit=tce-opex-ga-da;tax=max(0,ebit)*s['tax'];nopat=ebit-tax;dry=8*infl*n/18;wc=0 if previous is None else .08*(tce-previous)
  scrap=sum(SCRAP[k]*infl for _,k,y in active if year==y+life);cap=dry-scrap;fcff=nopat+da-cap-wc
  rows.append({'year':i,'period_end_year':year,'vessels':n,'TCE_rates':rates,'TCE_revenue':tce,'vessel_opex':opex,'GA':ga,'economic_DA':da,'EBIT':ebit,'tax':tax,'NOPAT':nopat,'working_capital':wc,'drydock_capex':dry,'normalized_hull_reserve':0,'actual_hull_replacement_net_scrap':-scrap,'additional_growth_investment':0,'total_capex':cap,'FCFF':fcff,'PV':fcff/(1+s['wacc'])**i});previous=tce
 release=.08*previous/(1+s['wacc'])**life;ev=sum(x['PV']for x in rows)+release;pv=sum(x['PV']for x in rows[:10]);tail=ev-pv;bridge=capital(s['cfo'],reserve)
 a.update(rows=rows[:10],finite_tail_rows=rows[10:],finite_working_capital_release_PV=release,PV_flows=pv,PV_terminal=tail,terminal_value=tail*(1+s['wacc'])**10,terminal_nopat=0,terminal_net_reinvestment=0,terminal_fcff=0,terminal_smooth_value=0,terminal_cohort_correction=0,terminal_weight=tail/ev,EV=ev,equity=ev-bridge['net_claims'],value=(ev-bridge['net_claims'])/SHARES,normalized_hull_reserve_year1=0,terminal_method='Existing fleet runoff and scrap, no uneconomic perpetual renewal',forced_perpetual_renewal_stress_value=a['value'])
 return a

def main():
 m={'price':PRICE,'price_date':'2026-11-03','valuation_date':'2026-11-04','fleet':FLEET,'capital_inputs':CAPITAL,'scenarios':{k:calculate(v)for k,v in SCENARIOS.items()}}
 (P/'model_results.json').write_text(json.dumps(m,indent=2));rows=[dict(scenario=k,**r)for k,v in m['scenarios'].items()for r in v['rows']]
 with(P/'ten_year_model.csv').open('w',newline='')as f:a=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));a.writeheader();a.writerows(rows)
 print({k:round(v['value'],2)for k,v in m['scenarios'].items()})
if __name__=='__main__':main()
