"""Conditional finite refinery cash model. USD millions, barrels USD; assumptions not engineering certification."""
import pathlib,json
P=pathlib.Path(__file__).parent
CASES={'stress':dict(gm0=15,gm10=11.5,volume=190,prod=7.8,log=120,retail=65,corp=115,renew=15,life=20,beta=1.8,tax=.27,decline=.015,closure=500,legal=150,laramie=100), 'central':dict(gm0=20,gm10=14,volume=200,prod=7.3,log=135,retail=80,corp=110,renew=30,life=25,beta=1.5,tax=.25,decline=.0075,closure=350,legal=75,laramie=120), 'upside':dict(gm0=25,gm10=17,volume=210,prod=7,log=150,retail=95,corp=105,renew=50,life=30,beta=1.2,tax=.24,decline=0,closure=250,legal=25,laramie=120)}
def calc(c):
 c=c.copy();ke=.0486+c['beta']*.0441;kd=.07375;w=.85*ke+.15*kd*(1-c['tax']);stock=1237.365;ta=180.;intang=9.680;wc=800.;rows=[];ev=0.;renew_ev=0.;jvpv=0
 for t in range(1,c['life']+1):
  inf=1.02**(t-1);v=188+(c['volume']-188)*min(t/5,1)
  if t>10:v*= (1-c['decline'])**(t-10)
  gm=(c['gm0']+(c['gm10']-c['gm0'])*min((t-1)/9,1))*inf
  ref=v*.365*(gm-c['prod']*inf)
  log=c['log']*inf*(v/188);ret=c['retail']*inf*(1.01**min(t,10));corp=c['corp']*inf
  renew=c['renew']*min(t/3,1)*inf
  cash_ebitda=ref+log+ret-corp+renew # includes recurring SBC in corporate cost; no SRE/FIFO/mark-to-market bonus
  growth=(40 if t<=3 else 15 if t<=10 else 0)*inf
  cap=max(110*inf,(stock/14)/(1-.5/14))+growth
  tacap=max(55*inf,(ta/4)/(1-.5/4));icap=max(2.5*inf,(intang/5)/(1-.5/5))
  da=(stock+.5*cap)/14;taa=(ta+.5*tacap)/4;ia=(intang+.5*icap)/5
  ebit=cash_ebitda-da-taa-ia;tax=max(0,ebit)*c['tax'] # no assumed cash refunds or additional NOL credit
  targetwc=800*(v/188)*inf;dWC=max(0,targetwc-wc);wc=max(wc,targetwc) # no free working capital releases
  fcf=cash_ebitda-tax-cap-tacap-icap-dWC
  # NCI is 36.5% of a conservative renewables unlevered cash proxy; no book-NCI double deduction.
  nci_fc=.365*(renew*(1-c['tax'])-15*inf)
  nci_pv=nci_fc/(1+w)**t;renew_ev+=nci_pv
  # Existing equity-method distribution cash, not consolidation of investee debt or EBIT.
  jvcash={'stress':10,'central':14,'upside':18}.get(c.get('name','central'),14)*inf
  jvpv+=jvcash/(1+ke)**t
  pv=fcf/(1+w)**t;ev+=pv
  rows.append(dict(year=t,mbpd=v,gross_margin_per_bbl=gm,refining_cash=ref,logistics_cash=log,retail_cash=ret,corporate_cash=corp,renewables_cash=renew,cash_ebitda=cash_ebitda,physical_open=stock,physical_capex=cap,physical_da=da,physical_close=stock+cap-da,turnaround_open=ta,turnaround_cash=tacap,turnaround_amort=taa,turnaround_close=ta+tacap-taa,intangible_open=intang,intangible_capex=icap,intangible_amort=ia,intangible_close=intang+icap-ia,ebit=ebit,cash_tax=tax,working_capital=wc,incremental_wc=dWC,fcff=fcf,pv=pv,nci_cash=nci_fc,jv_distributions=jvcash))
  stock+=cap-da;ta+=tacap-taa;intang+=icap-ia
 # Finite closure; no perpetuity, salvage or WC release. Closure scenario subsumes ARO and known remediation, not incremental double deduction.
 closurepv=c['closure']*1.02**c['life']/(1+w)**c['life'];ev-=closurepv
 # Pending Laramie: close proceeds scenario plus deferred fixed amount; no 30 earn-out assumed; own equity proceeds, no investee debt added again.
 lara=c['laramie']/(1+ke)**.25+27.5/(1+ke)**5.25-30 # provisional disposal tax/friction reserve, not verified tax basis
 bridge=731.060-250-505.432-10.279-2-101.473-5-c['legal']-20 # cash reserve; gross term; finance leases; current lease proxy; accrued income tax; pension proxy; legal; post-period cash unknown reserve
 # Inventory financing treated as operating supplier funding, fees remain in cash margin; cannot deduct again without gross-up cash margins.
 equity=ev-max(0,renew_ev)+jvpv+lara+bridge
 shares=50.076962+1.104 # diluted-basic Q3 difference proxy for existing awards, not precise award inventory
 return dict(inputs=c,ke=ke,wacc=w,enterprise_conditional=ev,nci_cash_value=max(0,renew_ev),jv_distribution_value=jvpv,laramie_conditional_value=lara,bridge_ex_laramie=bridge,shares=shares,conditional_per_share=equity/shares,closure_pv=closurepv,year11_plus_pv=sum(r['pv'] for r in rows[10:])-closurepv,rows=rows)
out={k:calc(dict(v,name=k)) for k,v in CASES.items()};lo,hi=5.,40.
for _ in range(90):
 m=(lo+hi)/2;c=dict(CASES['central'],name='central',gm10=m)
 if calc(c)['conditional_per_share']<68.06:lo=m
 else:hi=m
sensitivity={}
for tag,changes in [('margin_minus2',{'gm10':12}),('margin_plus2',{'gm10':16}),('life20',{'life':20}),('life30',{'life':30}),('beta1_2',{'beta':1.2}),('beta1_8',{'beta':1.8})]:sensitivity[tag]=calc(dict(CASES['central'],name='central',**changes))['conditional_per_share']
r={'asof':'2026-11-08','type':'finite conditional asset cash model, not whole-equity certified valuation','approved_fair_value':None,'approved_entry':None,'cases':out,'inverse':{'price':68.06,'central_required_year10_real_gross_margin':(lo+hi)/2,'changes_only':'gm10; initial20 unchanged; linear years1-10; all other central assumptions held'},'sensitivity':sensitivity,'unknowns':{'engineering_economic_lives':None,'complete_closure_cost':None,'net_litigation_cost':None,'parent_access_to_cash':None,'current_award_fair_dilution':None,'standalone_renewables_maintenance_and_debt':None,'incremental_Alohi_put_value':None,'current_inventory_financing_normalized_fee_split':None,'laramie_close_tax_cost':None,'post_Oct30_equity_changes':None}}
(P/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:{z:v[z] for z in ['conditional_per_share','wacc','enterprise_conditional','closure_pv']} for k,v in out.items()},indent=2));print(r['inverse']);print(sensitivity)
