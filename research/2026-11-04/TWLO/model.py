"""Conditional FCFF; analyst scenario assumptions, not execution approval."""
import pathlib,json,copy
P=pathlib.Path(__file__).parent;src=json.loads((P/'history/source_numeric_extracts.json').read_text());d={}
for x in src['observations']:d.setdefault(x['period'],{})[x['metric']]=x['value']
h={k:(d['FY2025'][k]+d['9M2026'][k]-d['9M2025'][k])/1000 for k in ['revenue','ebit','ni_common','cfo','sbc_cfo','da_cfo','commission_amortization','software_cash','capex_cash']};r0=h['revenue'];e0=h['ebit'];shares=161.746027
inputs={'cash':1061.531,'short_investments':1829.940,'debt_principal':1000,'nonincome_tax_reserve':46,'historical_gross_utb_stress':280.696,'operating_cash_ratio':.15,'strategic_excluded':24.2,'equity_method_excluded':225.180,'shares_proxy':shares,'price':213.77}
cases={'bear':dict(g=[.05,.04,.04,.03,.03,.025,.025,.02,.02,.02],m=[.08,.09,.10,.10,.10,.10,.10,.10,.10,.10],tax=.27,w=.115,tg=.02,roic=.15),'base':dict(g=[.14,.12,.10,.09,.08,.06,.05,.04,.03,.03],m=[.10,.12,.13,.14,.15,.15,.15,.15,.15,.15],tax=.25,w=.105,tg=.025,roic=.20),'bull':dict(g=[.20,.18,.15,.13,.12,.10,.08,.06,.05,.04],m=[.12,.15,.17,.19,.20,.20,.20,.20,.20,.20],tax=.23,w=.095,tg=.03,roic=.25)}
def calc(c,capex_override=None,nwc=.10,commissions=.03,utb=280.696,opcash=.15,shares_override=shares,strategic_add=0,prepaid_loss=0):
 rev=r0;prev=e0*(1-c['tax']);pv=0;rows=[]
 for j,(g,m) in enumerate(zip(c['g'],c['m'])):
  old=rev;rev*=1+g;ebit=rev*m-prepaid_loss;nopat=ebit*(1-c['tax']);cr=capex_override if capex_override is not None else .025-.005*j/9;dr=.012+.003*j/9;capex=rev*cr;da=rev*dr;dnwc=(rev-old)*nwc;dc=(rev-old)*commissions;phys=capex-da+dnwc+dc;econ=max(0,nopat-prev)/c['roic'];reinv=max(phys,econ);fcff=nopat-reinv;pv+=fcff/(1+c['w'])**(j+1)
  rows.append(dict(year=j+1,revenue=rev,growth=g,margin=m,ebit=ebit,nopat=nopat,capex=capex,da=da,delta_nwc=dnwc,delta_commission_assets=dc,physical_reinvestment=phys,economic_reinvestment=econ,additional_reinvestment_reserve=reinv-phys,reinvestment=reinv,fcff=fcff,pv=fcff/(1+c['w'])**(j+1)));prev=nopat
 tr=rev*(1+c['tg']);tn=(tr*c['m'][-1]-prepaid_loss)*(1-c['tax']);tp=tr*(cr-dr)+(tr-rev)*(nwc+commissions);te=tn*c['tg']/c['roic'];ti=max(tp,te);tf=tn-ti;pvt=tf/(c['w']-c['tg'])/(1+c['w'])**10;ev=pv+pvt;b=1061.531+1829.940-1000-46-utb-r0*opcash+strategic_add
 return dict(value=(ev+b)/shares_override,ev=ev,bridge=b,shares=shares_override,pv_explicit=pv,pv_terminal=pvt,terminal_share=pvt/ev,rows=rows,terminal=dict(revenue=tr,nopat=tn,physical_reinvestment=tp,economic_reinvestment=te,reinvestment=ti,fcff=tf))
out={'method':'10-year FCFF, SBC retained, delta NOPAT-funded growth, physical floor including software/PPE and incremental commission/NWC funding, coherent terminal. Historical gross UTB is stress, not current payable.','inputs':inputs,'anchor':h,'scenarios':cases,'cases':{k:calc(c) for k,c in cases.items()}}
s={};base=cases['base']
for n,kw in [('utb_zero',{'utb':0}),('utb_double',{'utb':561.392}),('opcash_25pct',{'opcash':.25}),('capex_4pct',{'capex_override':.04}),('commissions_6pct',{'commissions':.06}),('nwc_20pct',{'nwc':.20}),('shares_plus5pct',{'shares_override':shares*1.05}),('strategic_75pct_book',{'strategic_add':(24.2+225.180)*.75}),('additional_prepaid_loss32_8_every_year',{'prepaid_loss':32.8})]:s[n]=calc(base,**kw)['value']
for w in [.095,.105,.115,.125]:
 for tg in [.02,.025,.03]:s[f'w{w}_g{tg}']=calc(dict(base,w=w,tg=tg))['value']
for tax in [.21,.30]:s[f'tax{tax}']=calc(dict(base,tax=tax))['value']
out['sensitivities']=s
scan=[{'delta':n/1000,'value':calc(dict(base,m=[m+n/1000 for m in base['m']]))['value']} for n in range(0,601,5)];out['inverse_margin_scan']=scan;out['inverse_margin_solution']=None
brackets=[(a['delta'],b['delta']) for a,b in zip(scan,scan[1:]) if (a['value']-213.77)*(b['value']-213.77)<0]
if brackets:
 lo,hi=brackets[0]
 for _ in range(70):
  mid=(lo+hi)/2;v=calc(dict(base,m=[m+mid for m in base['m']]))['value']
  if v<213.77:lo=mid
  else:hi=mid
 out['inverse_margin_solution']={'shift':mid,'terminal_margin':base['m'][-1]+mid,'value':v,'interpretation':'One-variable mathematical sensitivity shifting all ten margins, not forecast.'}
(P/'model.json').write_text(json.dumps(out,indent=2)+'\n');print({k:round(v['value'],5) for k,v in out['cases'].items()});print(out['inverse_margin_solution']);print('bridge',out['cases']['base']['bridge'])
