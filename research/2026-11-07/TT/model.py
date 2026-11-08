import pathlib,json,csv
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());R0=h['TTM2026']['revenue'];DA=h['TTM2026']['da'];AM=164.5+135.8-128.4;DEP=DA-AM;S0=2456.2;I0=840.9;cm0=(h['TTM2026']['ebit']+DA)/R0
cfg={'stress':dict(g0=.06,g=.02,cm=.205,tax=.24,beta=1.3,physical_life=8,nwc=.15,asbestos=1000),'central':dict(g0=.10,g=.025,cm=.225,tax=.22,beta=1.1,physical_life=S0/DEP,nwc=.10,asbestos=742.5),'upside':dict(g0=.14,g=.03,cm=.245,tax=.20,beta=.9,physical_life=12,nwc=.08,asbestos=545)}
def calc(c,g0=None):
 R=R0;S=S0;I=I0;ke=.0486+c['beta']*.0441;w=ke*.95+.055*(1-c['tax'])*.05;pv=0;rows=[];gr0=c['g0'] if g0 is None else g0
 for y in range(1,11):
  gr=gr0+(c['g']-gr0)*(y-1)/9;nr=R*(1+gr);cm=cm0+(c['cm']-cm0)*min(y/5,1)
  # Existing acquired intangibles amortize; sustaining R&D (~2% revenue) stays expensed in cash margin.
  # Future modeled growth is organic. No acquisition is credited without acquisition spending.
  ipam=min(I,I0/5);I-=ipam
  rate=1/c['physical_life'];cap=(rate*S+gr*S)/(1-rate/2);dep=rate*S+rate*cap/2
  ebit=cm*nr-dep-ipam;nopat=ebit*(1-c['tax']);nwc=c['nwc']*(nr-R);fcff=nopat+dep+ipam-cap-nwc
  endS=S+cap-dep
  rows.append(dict(year=y,revenue=nr,growth=gr,cash_margin=cm,expensed_sustaining_budget_reference=.02*nr,physical_start=S,physical_capex=cap,physical_depreciation=dep,physical_end=endS,intangible_amortization=ipam,intangible_end=I,ebit=ebit,nopat=nopat,nwc_investment=nwc,fcff=fcff))
  pv+=fcff/(1+w)**y;R=nr;S=endS
 g=c['g'];nr=R*(1+g);rate=1/c['physical_life'];cap=(rate*S+g*S)/(1-rate/2);dep=rate*S+rate*cap/2;nwc=c['nwc']*g*R;ebit=c['cm']*nr-dep;nopat=ebit*(1-c['tax']);reinvest=cap-dep+nwc;fcff=nopat-reinvest;tv=fcff/(w-g);ev=pv+tv/(1+w)**10
 # Asbestos reserves are gross stress allowances, NOT net final legal liability. Already-funded270 not credited as unrestricted cash.
 nci=25.6*(1+g)/(ke-g);bridge=1227.4-500-4217.6-485.6-51.8-15.8-c['asbestos']-nci-150
 shares=218.895337+1.3
 return dict(wacc=w,ke=ke,years=rows,terminal=dict(fcff=fcff,nopat=nopat,reinvestment=reinvest,physical_capex=cap,physical_depreciation=dep,nwc=nwc,g=g,implied_incremental_roic=nopat*g/reinvest),operating_ev=ev,conditional_bridge=bridge,nci_hypothesis=nci,share_denominator=shares,conditional_per_share=(ev+bridge)/shares,terminal_weight=tv/(1+w)**10/ev)
cases={n:calc(c) for n,c in cfg.items()};lo,hi=0,.5
for _ in range(90):
 m=(lo+hi)/2
 if calc(cfg['central'],m)['conditional_per_share']<401.76:lo=m
 else:hi=m
bars=list(csv.DictReader((P/'daily_closes.csv').open()));ema={}
for n in [20,50]:
 e=float(bars[0]['close'])
 for x in bars[1:]:e=2/(n+1)*float(x['close'])+(1-2/(n+1))*e
 ema[str(n)]=e
out={'as_of':'2026-11-08','units':'USD million except per-share','price_date':'2026-11-06 regular close','price':401.76,'current_shares_million':218.895337,'market_cap':218.895337*401.76,'ema':ema,'technical_pass':401.76>ema['50'] and ema['20']>ema['50'],'volume20':sum(float(x['volume']) for x in csv.DictReader((P/'volume_screen_input.csv').open()))/20,'base_depreciation':DEP,'base_amortization':AM,'base_cash_margin':cm0,'risk_free':.0486,'risk_free_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','config':cfg,'cases':cases,'inverse_initial_growth':(lo+hi)/2,'approved_value':None,'approved_entry':None,'current_nonoperating_equity_method_value':None,'incremental_asbestos_liability_certified':None,'current_pension_net_deficit':None,'current_lease_balance':None,'closing_bridge_status':'conditional; no whole-equity fair value certified'}
(P/'model_results.json').write_text(json.dumps(out,indent=2))
with (P/'scenarios.csv').open('w') as f:
 wri=csv.DictWriter(f,fieldnames=['scenario']+list(cases['central']['years'][0]));wri.writeheader();wri.writerows(dict(scenario=n,**x) for n,c in cases.items() for x in c['years'])
print({n:(c['conditional_per_share'],c['terminal']['implied_incremental_roic']) for n,c in cases.items()});print('inverse',(lo+hi)/2)
