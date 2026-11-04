"""SSNC operating FCFF; research draft pending independent audit. USD millions."""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
PRICE=80.88;REVENUE=6756.;SHARES=240.6;CASH=525.4;DEBT=7483.5;NCI=69.;RESERVE=150.
BASE=dict(growth=[.04,.045,.045,.04,.035],margin=[.32,.3225,.325,.325,.325],tax=.25,ordinary_da=.035,capex=.046,wc=.10,roic=.18,terminal_roic=.18,terminal_margin=.32,g=.025,wacc=.09,extra_replacement=0.,additional_claims=122.)
BEAR={**BASE,'growth':[.01,.02,.025,.025,.025],'margin':[.30,.295,.295,.295,.295],'tax':.27,'capex':.05,'roic':.13,'terminal_roic':.13,'terminal_margin':.29,'g':.02,'wacc':.105}
BULL={**BASE,'growth':[.06,.065,.065,.06,.05],'margin':[.33,.34,.345,.35,.35],'tax':.24,'capex':.045,'roic':.23,'terminal_roic':.23,'terminal_margin':.34,'g':.03,'wacc':.085}
def model(s):
 r=REVENUE;rows=[];lastnopat=r*.32*(1-s['tax'])
 for i in range(1,11):
  a=max(0,(i-5)/5);g=s['growth'][i-1]if i<=5 else(1-a)*s['growth'][-1]+a*s['g'];m=s['margin'][i-1]if i<=5 else(1-a)*s['margin'][-1]+a*s['terminal_margin'];prev=r;r*=1+g
  ebita=r*m;tax=ebita*s['tax'];nopat=ebita-tax;da=r*s['ordinary_da'];capex=r*s['capex'];wc=(r-prev)*s['wc'];roic=(1-a)*s['roic']+a*s['terminal_roic']
  # Fund positive NOPAT growth, including margin improvement. Efficiencies are not free capital.
  reinv_growth=max(0,nopat-lastnopat)/roic;floor=capex-da+wc;extra=r*s['extra_replacement'];net=max(floor,reinv_growth)+extra
  # Transition actual ΔNOPAT funding to steady-state NOPAT*g/ROIC, retaining investment floor.
  net=(1-a)*net+a*max(floor,nopat*g/roic+extra)
  fcff=nopat+da-capex-wc-(net-floor)
  rows.append(dict(year=2026+i,revenue=r,growth=g,ebita_margin_after_SBC=m,ebita=ebita,cash_tax=tax,cash_nopat=nopat,ordinary_depreciation_software_amortization=da,ppe_software_capex=capex,delta_wc=wc,incremental_roic=roic,positive_nopat_growth_funding=reinv_growth,minimum_net_investment=floor,additional_economic_investment=net-floor,net_reinvestment=net,fcff=fcff,pv_fcff=fcff/(1+s['wacc'])**i));lastnopat=nopat
 tn=r*(1+s['g'])*s['terminal_margin']*(1-s['tax']);tr=tn*s['g']/s['terminal_roic']+r*(1+s['g'])*s['extra_replacement'];tf=tn-tr;tv=tf/(s['wacc']-s['g'])/(1+s['wacc'])**10;ev=sum(x['pv_fcff']for x in rows)+tv
 claims=DEBT+NCI+s.get('additional_claims',0);eq=ev+CASH-s.get('reserve',RESERVE)-claims
 return dict(value=eq/SHARES,ev=ev,equity=eq,claims=claims,excess_cash=CASH-s.get('reserve',RESERVE),pv_terminal=tv,terminal_weight=tv/ev,terminal_nopat=tn,terminal_reinvestment=tr,terminal_fcff=tf,rows=rows)
def old_model(growth=None,margins=None,wacc=.1,g=.025,roic=.18,da=.109,investment=.091,claims=7027.1,shares=240.6):
 growth=growth or [.05,.045,.04,.035,.03];margins=margins or [.245,.25,.25,.25,.25];r=6756.;pv=0
 for i in range(1,11):
  a=max(0,(i-5)/5);gr=growth[i-1]if i<=5 else(1-a)*growth[-1]+a*g;m=margins[i-1]if i<=5 else margins[-1];old=r;r*=1+gr;n=r*m*.75
  raw=r*(investment-da)+(r-old)*.1
  if i<=5:reinv=raw;ratio5=raw/n
  else:reinv=n*((1-a)*ratio5+a*g/roic)
  pv+=(n-reinv)/(1+wacc)**i
 tv=r*(1+g)*margins[-1]*.75*(1-g/roic)/(wacc-g)/(1+wacc)**10
 return(pv+tv-claims)/shares
if __name__=='__main__':
 cases={k:dict(assumptions=s,**model(s))for k,s in [('bear',BEAR),('base',BASE),('bull',BULL)]}
 sens=[dict(wacc=w,g=g,value=model({**BASE,'wacc':w,'g':g})['value'])for w in [.085,.09,.10,.11]for g in [.02,.025,.03]]
 robustness={}
 for label,change in [('extra_replacement1pct',{'extra_replacement':.01}),('extra_replacement2pct',{'extra_replacement':.02}),('cash_tax22_5pct',{'tax':.225}),('roic13pct',{'roic':.13,'terminal_roic':.13}),('roic23pct',{'roic':.23,'terminal_roic':.23}),('no_cash_reserve',{'reserve':0}),('additional_claims150m',{'additional_claims':272})]:robustness[label]=model({**BASE,**change})['value']
 out=dict(draft=True,price=PRICE,price_date='2026-11-03',shares=SHARES,scenarios=cases,sensitivity=sens,robustness=robustness,prior_A119_reconstructed=old_model())
 (P/'model_results.json').write_text(json.dumps(out,indent=2))
 with(P/'ten_year_model.csv').open('w')as f:
  rows=[dict(scenario=k,**r)for k,c in cases.items()for r in c['rows']];w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print({k:c['value']for k,c in cases.items()});print('A119',old_model());print(robustness)
