"""VMC FCFF, USD millions; dated 2026-11-07. Controlled support calculation.
Sources and analyst assumptions described in report.md. No orders/publication.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
PRICE=282.72; SHARES=128.344422+0.4
RF=.0486; ERP=.0441; BETA=.99; KD=.05692; TAX=.225
DEBT=4440.1+315+8.6 # face debt, commercial paper and finance leases
EQUITY=PRICE*128.344422
WACC=(RF+BETA*ERP)*EQUITY/(EQUITY+DEBT)+KD*(1-TAX)*DEBT/(EQUITY+DEBT)
# No operating lease debt: rents remain operating costs. Present ARO deducted once.
BRIDGE=dict(debt=DEBT,aro=496.1,environment=51.2,pension_postretirement=71.8,nci=24.6,excess_cash=0,disposal_receivable=150/(1+KD)**(13/12))
NETCLAIMS=sum(BRIDGE[k] for k in ['debt','aro','environment','pension_postretirement','nci'])-BRIDGE['disposal_receivable']
BASE=dict(tons=227.6,asp=22.61,cost=11.16,aggregate_revenue=6103.1,asphalt_revenue=1227.7,concrete_revenue=369.6,asphalt_gp=167.2,concrete_gp=32,agg_da=610-18.7,other_da=714.3-610-(22.8-15.2),sag=550.2,other_cost=57.9-8.6-9.4-1.3)
# Concrete uses four times Q3 residual operations; broad perimeter sensitivity below.
BASE['revenue']=BASE['aggregate_revenue']+BASE['asphalt_revenue']+BASE['concrete_revenue']
CASES={
'adverso':dict(vol=[-.03,0,.01,.01,.01],price=[.04,.025,.025,.025,.025],cost=[.05,.03,.025,.025,.025],terminal_g=.025,roic=.08,turnover=.55),
'central':dict(vol=[.01,.02,.02,.02,.02],price=[.06,.04,.04,.04,.04],cost=[.035,.03,.03,.03,.03],terminal_g=.03,roic=.10,turnover=.65),
'favorable':dict(vol=[.03,.03,.03,.03,.03],price=[.08,.05,.05,.05,.05],cost=[.025,.025,.025,.025,.025],terminal_g=.035,roic=.12,turnover=.80)}
def value(case='central',wacc=WACC,g=None,price_shift=0,extra_capex=0,claims=NETCLAIMS,concrete_scale=1):
 c=CASES[case];g=c['terminal_g'] if g is None else g
 assert wacc>g
 b=BASE; tons=b['tons'];asp=b['asp'];cost=b['cost'];freight=b['aggregate_revenue']-tons*asp
 asphalt=b['asphalt_revenue'];concrete=b['concrete_revenue']*concrete_scale; agp=b['asphalt_gp'];cgp=b['concrete_gp']*concrete_scale
 dda=b['agg_da']+b['other_da'];sag=b['sag'];other=b['other_cost'];prev_rev=b['revenue']+b['concrete_revenue']*(concrete_scale-1)
 rows=[];pv=0
 for y in range(1,11):
  t=max(0,(y-5)/5)
  v=c['vol'][min(y,5)-1]*(1-t)+.01*t
  p=(c['price'][min(y,5)-1]+price_shift)*(1-t)+((1+g)/1.01-1)*t
  co=c['cost'][min(y,5)-1]*(1-t)+((1+g)/1.01-1)*t
  growth=(1+v)*(1+p)-1
  tons*=1+v;asp*=1+p;cost*=1+co
  freight*=1+growth;asphalt*=1+growth;concrete*=1+growth;agp*=1+growth;cgp*=1+growth
  # DDA includes depletion/mineral-rights renewal and finance-lease depreciation; excludes ARO accretion.
  dda*=1+growth;sag*=1+(0.03*(1-t)+g*t);other*=1+g
  rev=tons*asp+freight+asphalt+concrete
  # Base aggregate cash gross profit is tons*(ASP-cost); pass-through freight no profit.
  ebit=tons*(asp-cost)+agp+cgp-dda*(b['agg_da']/(b['agg_da']+b['other_da']))-sag-other
  nopat=ebit*(1-TAX);drev=rev-prev_rev;dnwc=.12*drev
  # Economic reinvestment for growth, incremental reclamation/reserve development charge.
  reinvest=drev/c['turnover']+20*(1+g)**y+extra_capex
  # Fade total reinvestment to sustainable NOPAT*g/ROIC, not a second deduction.
  reinvest=reinvest*(1-t)+(nopat*g/c['roic']+extra_capex)*t
  capex=dda+reinvest-dnwc
  fcff=nopat+dda-capex-dnwc
  assert capex>0 and abs(fcff-(nopat-reinvest))<1e-7
  pvfcff=fcff/(1+wacc)**y;pv+=pvfcff
  rows.append(dict(year=y,stage='explicit' if y<=5 else 'transition',tons=tons,asp=asp,cost_per_ton=cost,revenue=rev,ebit=ebit,nopat=nopat,dda=dda,capex=capex,dnwc=dnwc,net_reinvestment=reinvest,fcff=fcff,pv_fcff=pvfcff))
  prev_rev=rev
 n=rows[-1]['nopat']*(1+g);term_reinv=n*g/c['roic']+extra_capex;terminal_fcff=n-term_reinv;tv=terminal_fcff/(wacc-g);pvtv=tv/(1+wacc)**10;ev=pv+pvtv
 terminal_components=dict(revenue=rows[-1]['revenue']*(1+g),dda=rows[-1]['dda']*(1+g),dnwc=.12*rows[-1]['revenue']*g)
 terminal_components['capex']=terminal_components['dda']+term_reinv-terminal_components['dnwc']
 terminal_components['fcff_identity']=n+terminal_components['dda']-terminal_components['capex']-terminal_components['dnwc']
 assert abs(terminal_components['fcff_identity']-terminal_fcff)<1e-7
 return dict(terminal_components=terminal_components,price=(ev-claims)/SHARES,ev=ev,equity=ev-claims,wacc=wacc,g=g,roic=c['roic'],terminal_weight=pvtv/ev,terminal_nopat=n,terminal_reinvestment=term_reinv,terminal_fcff=terminal_fcff,rows=rows)
def solve_price_shift():
 lo,hi=-.02,.20
 for _ in range(90):
  mid=(lo+hi)/2
  if value(price_shift=mid)['price']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
if __name__=='__main__':
 results={k:value(k) for k in CASES}
 for k,r in results.items():
  with (P/f'forecast_{k}.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
 summaries={k:{a:b for a,b in r.items() if a!='rows'} for k,r in results.items()}
 out=dict(as_of='2026-11-07',price=PRICE,shares=SHARES,wacc_components=dict(riskfree=RF,erp=ERP,beta=BETA,kd=KD,tax=TAX,equity=EQUITY,debt=DEBT),bridge=BRIDGE,net_claims=NETCLAIMS,base=BASE,cases=summaries,inverse_price_shift=solve_price_shift(),sensitivity=[dict(wacc=w,g=g,value=value(wacc=w,g=g)['price']) for w in [.075,.085,WACC,.095,.105] for g in [.02,.025,.03,.035]],proxies=dict(debt_cost_plus100bp_price=value(wacc=WACC+.01*(1-TAX)*DEBT/(EQUITY+DEBT))['price'],reserve_extra50_price=value(extra_capex=50)['price'],concrete_minus25pct_price=value(concrete_scale=.75)['price'],concrete_plus25pct_price=value(concrete_scale=1.25)['price'],all_cash_excess_price=value(claims=NETCLAIMS-106.6)['price'],mexico_tax_loss_price=value(claims=NETCLAIMS+35)['price'],debt_market_value_price=value(claims=NETCLAIMS-(4440.1-3624.5))['price']),checks=dict(ten_years=all(len(r['rows'])==10 for r in results.values()),five_explicit_five_transition=all([x['stage'] for x in r['rows']]==['explicit']*5+['transition']*5 for r in results.values()),fcff_identity=all(abs(x['fcff']-(x['nopat']+x['dda']-x['capex']-x['dnwc']))<1e-7 for r in results.values() for x in r['rows']),terminal_g_less_wacc=all(r['g']<r['wacc'] for r in results.values()),terminal_reinvestment_not_free=all(r['terminal_reinvestment']>0 for r in results.values())))
 out['alternative_assumptions']={'favorable_wacc_7_5pct':value('favorable',wacc=.075)['price']}
 original=CASES['central'].copy()
 CASES['central']['turnover']=1.30
 out['alternative_assumptions']['turnover_1_3']=value()['price']
 CASES['central']['roic']=.14
 out['alternative_assumptions']['turnover_1_3_roic_14pct']=value()['price']
 CASES['central']=original
 out['cash_bridge']={'ttm_cfo':1514.0,'ttm_cash_capex':732.8,'cfo_less_capex':781.2,'ttm_net_interest':239.7-13.4+160-174.2,'ttm_sbc':46.5,'observed_fcff_proxy':781.2+(239.7-13.4+160-174.2)*(1-TAX)-46.5}
 (P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['cases','inverse_price_shift','proxies']},indent=2))
