"""Conditional FCFF; analyst forecasts, not execution approval."""
import json,pathlib,copy
P=pathlib.Path(__file__).parent
h=json.loads((P/'history/financial_history.json').read_text())['periods']['TTM_September_2026']
r0=h['revenue'];e0=h['ebit']-(10.4-9.0+4.1);shares=742.6;contract_ratio=815.4/r0
inputs={'cash':3750.6,'afs_investments':1536.7,'equity_securities_excluded':31.1,'debt_principal':500,'utb_gross_stress':96.2+13.5,'op_cash_ratio':.15,'shares_proxy':shares,'price':128.11,'contract_asset_ratio':contract_ratio}
bridge=3750.6+1536.7-500-109.7-r0*.15
cases={
'bear':dict(g=[.08,.06,.05,.04,.03,.03,.025,.025,.02,.02],m=[.30,.29,.28,.27,.27,.27,.27,.27,.27,.27],w=.11,tg=.02,roic=.15,tax=.25),
'base':dict(g=[.15,.13,.12,.11,.10,.08,.07,.06,.05,.04],m=[.33,.33,.325,.32,.32,.32,.32,.32,.32,.32],w=.10,tg=.03,roic=.20,tax=.225),
'bull':dict(g=[.20,.18,.16,.15,.14,.12,.10,.08,.06,.05],m=[.35,.36,.37,.37,.37,.37,.37,.37,.37,.37],w=.09,tg=.035,roic=.25,tax=.20)}
def calc(c,capex_override=None,contract=contract_ratio,nwc=.05,cash_ratio=.15,shares_override=shares,tax_reserve=109.7):
 rev=r0;prev=e0*(1-c['tax']);rows=[];pv=0
 for j,(g,m) in enumerate(zip(c['g'],c['m'])):
  y=j+1;old=rev;rev*=1+g;nopat=rev*m*(1-c['tax']);cr=capex_override if capex_override is not None else [.045,.04,.035,.0325,.03,.03,.03,.03,.03,.03][j];dr=.015+.005*j/9
  capex=rev*cr;da=rev*dr;dnwc=(rev-old)*nwc;dc=(rev-old)*contract;phys=capex-da+dnwc+dc;econ=max(0,nopat-prev)/c['roic'];reinv=max(phys,econ);fcff=nopat-reinv;discount=(1+c['w'])**y;pv+=fcff/discount
  rows.append(dict(year=y,revenue=rev,growth=g,margin=m,ebit=rev*m,nopat=nopat,capex=capex,da=da,delta_nwc=dnwc,delta_contract_assets=dc,physical_reinvestment=phys,economic_reinvestment=econ,additional_reinvestment_reserve=reinv-phys,reinvestment=reinv,fcff=fcff,pv=fcff/discount));prev=nopat
 tr=rev*(1+c['tg']);tn=tr*c['m'][-1]*(1-c['tax']);tp=tr*(cr-dr)+(tr-rev)*(nwc+contract);te=tn*c['tg']/c['roic'];ti=max(tp,te);tf=tn-ti;pvt=tf/(c['w']-c['tg'])/(1+c['w'])**10;ev=pv+pvt;b=3750.6+1536.7-500-tax_reserve-r0*cash_ratio
 return dict(value=(ev+b)/shares_override,ev=ev,bridge=b,shares=shares_override,pv_explicit=pv,pv_terminal=pvt,terminal_share=pvt/ev,rows=rows,terminal=dict(revenue=tr,nopat=tn,physical_reinvestment=tp,economic_reinvestment=te,reinvestment=ti,fcff=tf))
out={'method':'10-year FCFF; GAAP SBC retained; margin growth funded using delta NOPAT; physical floor includes net contract assets, no deferred-revenue financing credit; terminal maximum of physical/economic reinvestment. No acquisition/intangible amortization addback.','inputs':inputs,'scenarios':cases,'anchor':h,'normalized_anchor_ebit':e0,'ttm_ip_gain_removed':5.5,'cases':{k:calc(c) for k,c in cases.items()}}
base=cases['base'];s={}
for n,kw in [('tax_reserve_zero',{'tax_reserve':0}),('tax_reserve_double',{'tax_reserve':219.4}),('capex_5pct',{'capex_override':.05}),('contract_assets_double',{'contract':contract_ratio*2}),('nwc_10pct',{'nwc':.10}),('opcash_25pct',{'cash_ratio':.25}),('shares_plus_5pct',{'shares_override':shares*1.05})]:s[n]=calc(base,**kw)['value']
for w in [.09,.10,.11,.12]:
 for tg in [.02,.03,.035]:s[f'w{w}_g{tg}']=calc(dict(base,w=w,tg=tg))['value']
for tax in [.18,.25]:s[f'tax_{tax}']=calc(dict(base,tax=tax))['value']
for roic in [.15,.25]:s[f'roic_{roic}']=calc(dict(base,roic=roic))['value']
out['sensitivities']=s
scan=[{'delta':d/1000,'value':calc(dict(base,m=[m+d/1000 for m in base['m']]))['value']} for d in range(0,601,5)]
out['inverse_margin_scan']=scan;out['inverse_margin_solution']=None
brackets=[(a['delta'],b['delta']) for a,b in zip(scan,scan[1:]) if (a['value']-128.11)*(b['value']-128.11)<0]
if brackets:
 lo,hi=brackets[0]
 for _ in range(70):
  mid=(lo+hi)/2;v=calc(dict(base,m=[m+mid for m in base['m']]))['value']
  if v<128.11:lo=mid
  else:hi=mid
 out['inverse_margin_solution']={'shift':mid,'terminal_margin':base['m'][-1]+mid,'value':v,'note':'Mathematical sensitivity, not a business forecast; all ten margins shifted.'}
(P/'model.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v['value'] for k,v in out['cases'].items()});print(s);print(out['inverse_margin_solution'])
