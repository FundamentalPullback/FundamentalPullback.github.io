"""Conditional FCFF research, not certified total equity value or execution."""
import math,json,pathlib,copy
P=pathlib.Path(__file__).parent
h={r['period']:r for r in json.loads((P/'history/shop_financial_history.json').read_text())['records']}
print(list(h)) if not any('TTM' in k for k in h) else None
r=next(r for k,r in h.items() if k=='TTM_Q3_2026') if 'TTM_Q3_2026' in h else next(r for k,r in h.items() if 'TTM' in k and r['revenue']==14167)
inputs=json.loads((P/'facts/model_inputs.json').read_text())
revenue0=r['revenue'];ebit0=r['gaap_ebit'];noncash_revenue_ratio=inputs['noncash_revenue_9m']/inputs['revenue_9m'];loan_ratio=inputs['net_loan_book']/revenue0
shares=sum(inputs['diluted_share_proxy_components_m'].values())
bridge=inputs['cash']+inputs['marketable_short']+inputs['marketable_long']-inputs['operating_cash_ratio']*revenue0-inputs['tax_stress']
cases=inputs['scenarios']
def calc(c, loan=loan_ratio,capexratio=.008,nwc=.05,bridge_override=None,noncash=noncash_revenue_ratio):
 rev=revenue0;prev_nopat=(ebit0-revenue0*noncash)*(1-c['tax']);rows=[];pv=0
 for i,(g,m) in enumerate(zip(c['g'],c['m']),1):
  old=rev;rev*=1+g;nopat=(rev*m-rev*noncash)*(1-c['tax'])
  capex=rev*capexratio;da=rev*.003;dnwc=(rev-old)*nwc;dloan=(rev-old)*loan
  physical=capex-da+dnwc+dloan;economic=max(0,nopat-prev_nopat)/c['roic'];reinv=max(physical,economic);fcff=nopat-reinv;discount=(1+c['w'])**i;pv+=fcff/discount
  rows.append(dict(year=i,growth=g,revenue=rev,margin=m,gaap_ebit=rev*m,noncash_revenue_deduction=rev*noncash,nopat=nopat,capex=capex,da=da,delta_nwc=dnwc,delta_net_loans=dloan,physical_reinvestment=physical,economic_reinvestment=economic,additional_reinvestment_reserve=reinv-physical,fcff=fcff,present_value=fcff/discount));prev_nopat=nopat
 tr=rev*(1+c['tg']);tn=(tr*c['m'][-1]-tr*noncash)*(1-c['tax']);physical=tr*(capexratio-.003)+(tr-rev)*(nwc+loan);econ=tn*c['tg']/c['roic'];tf=tn-max(physical,econ);tv=tf/(c['w']-c['tg']);pvt=tv/(1+c['w'])**10;ev=pv+pvt;b=bridge if bridge_override is None else bridge_override
 return dict(value=(ev+b)/shares,ev=ev,bridge=b,shares=shares,pv_explicit=pv,pv_terminal=pvt,terminal_share=pvt/ev,terminal=dict(revenue=tr,nopat=tn,fcff=tf,physical_reinvestment=physical,economic_reinvestment=econ,reinvestment=max(physical,econ)),rows=rows)
out={'method':'10-year FCFF with funded margin growth and separate loan/NWC physical floor. All forecast inputs are analyst assumptions. Strategic investments excluded from bridge, not written off as fact.','inputs':inputs,'historical_anchor':r,'noncash_revenue_ratio':noncash_revenue_ratio,'loan_ratio':loan_ratio,'cases':{k:calc(c) for k,c in cases.items()}}
base=cases['base'];sens={}
for name,kwargs in [('loan_book_ratio_double',{'loan':loan_ratio*2}),('capex_1_5pct',{'capexratio':.015}),('nwc_10pct',{'nwc':.10}),('strategic_book_after_25pct_haircut',{'bridge_override':bridge+(4911+538)*.75}),('additional_tax_stress_100',{'bridge_override':bridge-100}),('cash_revenue_no_adjustment',{'noncash':0})]:sens[name]=calc(base,**kwargs)['value']
for w in [.09,.10,.11,.12]:
 for tg in [.02,.03,.035]:
  c=copy.deepcopy(base);c.update(w=w,tg=tg);sens[f'w{w}_g{tg}']=calc(c)['value']
# Inverse: all ten margin assumptions shifted together, growth/financing unchanged.
lo=0;hi=.60
if (calc(dict(base,m=[m+lo for m in base['m']]))['value']-inputs['price'])*(calc(dict(base,m=[m+hi for m in base['m']]))['value']-inputs['price'])<0:
 for _ in range(80):
  mid=(lo+hi)/2;v=calc(dict(base,m=[m+mid for m in base['m']]))['value']
  if v<inputs['price']:lo=mid
  else:hi=mid
 out['inverse_margin_shift']={'delta':(lo+hi)/2,'terminal_margin':base['m'][-1]+(lo+hi)/2,'value':calc(dict(base,m=[m+(lo+hi)/2 for m in base['m']]))['value'],'interpretation':'Mathematical one-variable solution, not guidance, forecast or probability.'}
else:out['inverse_margin_shift']=None
out['inverse_margin_scan']=[{'delta':d/1000,'value':calc(dict(base,m=[m+d/1000 for m in base['m']]))['value']} for d in range(0,601,5)]
out['sensitivities']=sens
(P/'model.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:round(v['value'],4) for k,v in out['cases'].items()});print(out['inverse_margin_shift'])
