import json, math, pathlib, datetime
P=pathlib.Path(__file__).parent
PRICE=15.79; FX=1.1165; SHARES=252.392562
# EUR millions. Controlled support calculation, not a certified workbook.
CLAIMS=10662+1000+1040+216+355+80+592+16.3725
cases={
'adverso':dict(growth=[-.04,0,.01,.015,.02,.02,.02,.02,.02,.02],margins=[.23,.23,.235,.24,.24,.24,.24,.24,.24,.24],wacc=.095,g=.015,roic=.09,age=.03),
'central':dict(growth=[-.02,.04,.05,.035,.03,.028,.026,.024,.022,.02],margins=[.245,.25,.26,.267,.27,.27,.27,.27,.27,.27],wacc=.080,g=.02,roic=.12,age=.025),
'favorable':dict(growth=[0,.055,.06,.045,.04,.036,.032,.028,.024,.02],margins=[.25,.265,.275,.285,.29,.29,.29,.29,.29,.29],wacc=.071,g=.025,roic=.14,age=.025)}
STUB=(datetime.date(2027,6,30)-datetime.date(2026,11,8)).days/365
def calc(c,offset=0,tax=.25):
 rev=9404; rows=[]; pv=0
 for i,(gr,mar) in enumerate(zip(c['growth'],c['margins']),1):
  old=rev; rev*=1+gr; ebit=rev*(mar+offset); nopat=ebit*(1-tax); da=rev*.044
  cashcapex=rev*.048; leasecapex=rev*(144/9404); ageing=rev*c['age']; otherwc=max(0,rev-old)*.09
  reinv=cashcapex+leasecapex+ageing+otherwc-da
  if i>5:
   fade=(i-5)/5
   target_reinv=nopat*c['g']/c['roic']
   target_age=rev*.754*c['g']; target_wc=rev*.09*c['g']
   reinv=(1-fade)*reinv+fade*target_reinv
   ageing=(1-fade)*ageing+fade*target_age; otherwc=(1-fade)*otherwc+fade*target_wc
   cashcapex=da+reinv-leasecapex-ageing-otherwc
  fcff=nopat-reinv; time=STUB+i-1; forward_fcff=fcff*(STUB if i==1 else 1); dcf=forward_fcff/(1+c['wacc'])**time;pv+=dcf
  rows.append(dict(year=2026+i,revenue=rev,margin=mar+offset,EBIT=ebit,NOPAT=nopat,DA=da,cash_capex=cashcapex,lease_replacement_capex=leasecapex,ageing_investment=ageing,other_delta_wc=otherwc,net_reinvestment=reinv,FCFF=fcff,remaining_FCFF=forward_fcff,discount_years=time,PV=dcf))
 tn=rows[-1]['NOPAT']*(1+c['g']); tri=tn*c['g']/c['roic']; tf=tn-tri; tv=tf/(c['wacc']-c['g']); tp=tv/(1+c['wacc'])**(STUB+9); ev=pv+tp; eq=ev-CLAIMS
 terminal_ageing=rev*(1+c['g'])*.754*c['g']; terminal_other_wc=rev*(1+c['g'])*.09*c['g']; terminal_net_fixed=tri-terminal_ageing-terminal_other_wc
 return dict(years=rows,terminal_ageing_investment=terminal_ageing,terminal_other_delta_wc=terminal_other_wc,terminal_net_fixed_investment=terminal_net_fixed,terminal_NOPAT=tn,terminal_reinvestment=tri,terminal_FCFF=tf,terminal_value=tv,PV_terminal=tp,EV=ev,claims=CLAIMS,equity=eq,eur_per_ordinary=eq/SHARES,usd_per_ADR=eq/SHARES*FX/5,terminal_weight=tp/ev,upside=eq/SHARES*FX/5/PRICE-1)
out={k:calc(c) for k,c in cases.items()}
lo=-.2;hi=.2
for _ in range(100):
 mid=(lo+hi)/2
 if calc(cases['central'],mid)['usd_per_ADR']<PRICE:lo=mid
 else:hi=mid
reverse=calc(cases['central'],mid)
vol=[191363,545070,149338,237368,735017,179649,1139948,346095,240842,1161983,507238,697581,276418,385311,392318,738438,287847,274608,1567073,1939754]
sensitivity=[]
for w in [.071,.080,.095]:
 for g in [.015,.02,.025]:
  c=dict(cases['central'],wacc=w,g=g);sensitivity.append(dict(wacc=w,g=g,value=calc(c)['usd_per_ADR']))
result=dict(asof='2026-11-08',status='screen-grade',decision='Observación; Stage 3 parcial; sin entrada',price=PRICE,price_date='2026-11-06',currency='EUR million except per-share',FX=FX,shares_m=SHARES,adr_per_ordinary=5,claims_bridge={'june_net_debt_including_leases':10662,'retained_operating_cash_assumption':1000,'minority_book_proxy':1040,'pension_and_employee_benefit_liabilities_no_surplus_credit':216,'other_risk_provisions':355,'restructuring_provision_past_events':80,'july_dividend_paid_after_balance_date':592,'hybrid_face_less_estimated_net_proceeds':16.3725,'total':CLAIMS,'hybrid_note':'October mechanical net debt 9178.3725 + hybrid claim1500 =10678.3725 before tender premiums and intervening cash flows; July dividend592 additionally recognized. No fictitious deleveraging.'},scenarios=out,assumptions=cases,sensitivity=sensitivity,tax_sensitivity={str(t):calc(cases['central'],tax=t)['usd_per_ADR'] for t in [.243,.25,.28]},stub_years=STUB,reverse=dict(margin_offset=mid,margin_year1=reverse['years'][0]['margin'],margin_year10=reverse['years'][-1]['margin'],value=reverse['usd_per_ADR']),avg20_volume=sum(vol)/20,stage35={'approved':False,'ceiling':None,'stop':None,'shares':0},gaps=['July-November operating cash/net debt rollforward not published in Q1 sales release; hybrid estimated net proceeds sourced in final terms; tender cash consideration/premium not quantified in completion release','Delhi ED litigation: issuer note6.4 explicitly unable to quantify exposure or probability','Minority fair value uses book proxy; exact October diluted option/performance-share count not published in voting-rights notice','Current senior debt market yield and geographic country premium remain scenario estimates; sourced Bund, sector beta and ERP are dated','Maintenance/growth/ROU D&A impairment split not fully separated; actual ROU additions/cash payments obtained','EMA200 slope and consistent complete technical series'])
(P/'results.json').write_text(json.dumps(result,indent=2))
(P/'run_log.json').write_text(json.dumps({'artifact':'controlled_support_calculation','status':'screen-grade','checks':{'wacc_gt_g':all(c['wacc']>c['g'] for c in cases.values()),'positive_terminal_reinvestment':all(r['terminal_reinvestment']>0 for r in out.values()),'scenario_ordered':out['adverso']['usd_per_ADR']<out['central']['usd_per_ADR']<out['favorable']['usd_per_ADR'],'reverse_tie':abs(reverse['usd_per_ADR']-PRICE)<1e-8,'positive_cash_capex':all(y['cash_capex']>0 for r in out.values() for y in r['years']),'positive_terminal_physical_investment':all(r['terminal_net_fixed_investment']>0 for r in out.values()),'ten_years_each':all(len(r['years'])==10 for r in out.values()),'future_stub_only':all(abs(r['years'][0]['remaining_FCFF']-r['years'][0]['FCFF']*STUB)<1e-8 for r in out.values()),'fcff_identity':all(abs(y['FCFF']-(y['NOPAT']+y['DA']-y['cash_capex']-y['lease_replacement_capex']-y['ageing_investment']-y['other_delta_wc']))<1e-7 for r in out.values() for y in r['years'])},'warnings':result['gaps']},indent=2))
print(json.dumps({k:{a:v[a] for a in ['usd_per_ADR','terminal_weight','upside']} for k,v in out.items()},indent=2));print(result['reverse']);print(result['avg20_volume'])
