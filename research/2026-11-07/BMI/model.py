"""BMI research-only FCFF v1, 2026-11-07. USD millions except per-share. No external dependencies."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# All actuals transcribed from issuer releases/2025 annual report; see source ledger.
fields=['sales','gross_profit','ebit','net_income','eps','cfo','capex','da','sbc','diluted_shares']
rows={
'FY2023':[703.592,276.438,118.049,92.598,3.14,110.117,12.003,28.110,5.188,29.456],
'FY2024':[826.558,329.184,157.936,124.942,4.23,155.034,12.818,32.185,6.182,29.533543],
'FY2025':[916.663,382.070,183.421,141.634,4.79,183.698,14.026,34.584,9.190,29.569496],
'Q4_2024':[205.182,82.760,39.223,30.717,1.04,52.067,4.669,8.068,1.587,29.559950],
'Q4_2025':[220.706,92.987,43.049,33.575,1.14,54.801,4.033,8.800,2.745,29.542816],
'Q1_2026':[202.277,84.327,35.171,27.335,.93,33.893,4.427,9.055,2.168,29.365170],
'Q2_2026':[222.321,90.773,39.377,29.720,1.02,26.711,4.839,9.855,3.179,29.141991],
'Q3_2026':[235.938,98.849,47.742,35.903,1.24,43.274,2.992,10.191,2.474,28.871187],
'9M_2025':[695.957,289.083,140.372,108.059,3.65,128.897,9.993,25.784,6.445,29.577619]}
d={k:dict(zip(fields,v)) for k,v in rows.items()}
for name,parts in [('TTM_20260930',['Q4_2025','Q1_2026','Q2_2026','Q3_2026']),('TTM_20250930',['Q4_2024','9M_2025'])]:
 d[name]={f:sum(d[p][f] for p in parts) for f in fields if f!='diluted_shares'}
 d[name]['diluted_shares']=sum(d[p]['diluted_shares']*(3 if p=='9M_2025' else 1) for p in parts)/4
for v in d.values():
 v.update(fcf_cfo_less_ppe=v['cfo']-v['capex'],nopat_25pct=v['ebit']*.75,operating_margin=v['ebit']/v['sales'],gross_margin=v['gross_profit']/v['sales'],net_margin=v['net_income']/v['sales'])
 v['fcf_less_sbc']=v['fcf_cfo_less_ppe']-v['sbc'];v['fcf_per_diluted_share']=v['fcf_cfo_less_ppe']/v['diluted_shares'];v['normalized_operating_eps']=v['nopat_25pct']/v['diluted_shares']
with (P/'historical.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(d.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in d.items())
shares=28.563652+.121037
bridge={'cash':67.928,'operating_cash_reserve':30.,'funded_debt':0.,'udlive_earnout_fair_value':12.,'legacy_benefit_reserve':9.343}
netbridge=bridge['cash']-sum(v for k,v in bridge.items() if k!='cash')
cases={
'adverse':dict(growth=[0,.03,.04,.04,.04],margin=[.18,.18,.185,.185,.185],wacc=.105,g=.02,roic=.15,terminal_roic=.15),
'central':dict(growth=[.08,.08,.08,.07,.06],margin=[.20,.205,.21,.215,.22],wacc=.09,g=.025,roic=.20,terminal_roic=.18),
'favorable':dict(growth=[.12,.12,.11,.10,.09],margin=[.21,.22,.23,.235,.24],wacc=.085,g=.03,roic=.25,terminal_roic=.20)}
def run(case,first_growth=None,wacc=None,g=None,margin_shift=0, replacement_floor_multiple=1.0):
 c=cases[case];gs=list(c['growth']) if first_growth is None else [first_growth]*5
 ms=[v+margin_shift for v in c['margin']];W=c['wacc'] if wacc is None else wacc;G=c['g'] if g is None else g
 assert W>G and replacement_floor_multiple>=1
 gs += [gs[-1]+(G-gs[-1])*i/5 for i in range(1,6)];ms += [ms[-1]]*5
 sales=d['TTM_20260930']['sales'];oldnop=d['TTM_20260930']['nopat_25pct'];out=[]
 for year,(gr,m) in enumerate(zip(gs,ms),1):
  oldsales=sales;sales*=1+gr;ebit=sales*m;nop=ebit*.75
  ri=c['roic']+(c['terminal_roic']-c['roic'])*max(0,year-5)/5
  reinv=max(0,nop-oldnop)/ri;da=sales*.043;dnwc=(sales-oldsales)*.15
  unfloored_invest=da+reinv-dnwc;floor=da*replacement_floor_multiple;invest=max(unfloored_invest,floor);floor_topup=invest-unfloored_invest;fcff=nop+da-invest-dnwc
  assert invest>=floor and abs(fcff-(nop-reinv-floor_topup))<1e-8
  out.append(dict(case=case,year=year,sales=sales,growth=gr,ebit_margin=m,ebit=ebit,nopat=nop,da=da,total_cash_investment=invest,replacement_floor=floor,replacement_topup=floor_topup,replacement_headroom=invest-floor,delta_nwc=dnwc,net_reinvestment=reinv,incremental_roic=ri,fcff=fcff,pv=fcff/(1+W)**year));oldnop=nop
 termnop=oldnop*(1+G);termreinv=termnop*G/c['terminal_roic'];termda=sales*(1+G)*.043;termdnwc=sales*G*.15;term_unfloored=termda+termreinv-termdnwc;termfloor=termda*replacement_floor_multiple;terminvest=max(term_unfloored,termfloor);termtopup=terminvest-term_unfloored;termfcff=termnop+termda-terminvest-termdnwc;assert terminvest>=termfloor;tv=termfcff/(W-G);pvtv=tv/(1+W)**10;ev=sum(r['pv'] for r in out)+pvtv
 return {'price':(ev+netbridge)/shares,'ev':ev,'pv_explicit':ev-pvtv,'pv_terminal':pvtv,'terminal_weight':pvtv/ev,'terminal_fcff':termfcff,'terminal_da':termda,'terminal_cash_investment':terminvest,'terminal_delta_nwc':termdnwc,'terminal_replacement_floor':termfloor,'terminal_floor_topup':termtopup,'explicit_floor_topup':sum(r['replacement_topup'] for r in out),'terminal_reinvestment':termreinv,'year10_sales':sales,'year10_nopat':oldnop,'wacc':W,'g':G},out
summary={}; forecasts=[]
for name in cases:
 summary[name],o=run(name);forecasts+=o
with (P/'forecast.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(forecasts[0]));w.writeheader();w.writerows(forecasts)
sens=[dict(wacc=w,g=g,**{k:v for k,v in run('central',wacc=w,g=g)[0].items() if k not in ['wacc','g']}) for w in [.08,.09,.10,.11] for g in [.02,.025,.03]]
inverse=[]
for w,shift in [(.09,0),(.09,.02),(.08,0),(.10,0)]:
 target=158.18
 grid=[(g,run('central',first_growth=g,wacc=w,margin_shift=shift)[0]['price']) for g in [i*.5/1000 for i in range(1001)]]
 monotonic=all(grid[i+1][1]>=grid[i][1]-1e-10 for i in range(1000))
 crossings=[i for i in range(1000) if grid[i][1]<=target<=grid[i+1][1]]
 bracketed=grid[0][1]<=target<=grid[-1][1]
 assert monotonic and bracketed and len(crossings)==1
 idx=crossings[0];lo,hi=grid[idx][0],grid[idx+1][0];original_bracket=[lo,hi]
 for _ in range(100):
  mid=(lo+hi)/2
  if run('central',first_growth=mid,wacc=w,margin_shift=shift)[0]['price']<target:lo=mid
  else:hi=mid
 s,_=run('central',first_growth=mid,wacc=w,margin_shift=shift);residual=s['price']-target
 assert abs(residual)<1e-7
 inverse.append(dict(wacc=w,year5_margin=.22+shift,required_y1_5_sales_growth=mid,year10_sales=s['year10_sales'],price=s['price'],residual=residual,scan_intervals=1000,scan_domain=[0,.5],scan_endpoint_prices=[grid[0][1],grid[-1][1]],monotonic_non_decreasing=monotonic,number_of_brackets=len(crossings),bracket=original_bracket,bracket_prices=[grid[idx][1],grid[idx+1][1]],final_bracket=[lo,hi]))
floor_stress=[]
for name in cases:
 for mult in [1.,1.25,1.5,2.]:
  v,rows=run(name,replacement_floor_multiple=mult)
  floor_stress.append(dict(case=name,replacement_floor_multiple=mult,price=v['price'],explicit_topup=v['explicit_floor_topup'],terminal_topup=v['terminal_floor_topup'],minimum_explicit_headroom=min(r['replacement_headroom'] for r in rows),terminal_headroom=v['terminal_cash_investment']-v['terminal_replacement_floor']))

result=dict(perimeter='September 2026 financial perimeter and historical capital bridge, excludes completed 37South acquisition announced 2026-11-03; NOT current combined BMI value',current_combined_value=None,version='BMI-FCFF-20261107-v1.1-QA-provisional',replacement_floor_stress=floor_stress,cases=cases,summary=summary,capital_bridge=bridge,net_bridge=netbridge,shares=shares,sensitivity=sens,inverse=inverse,historical=d)
(P/'model_outputs.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['summary','inverse','net_bridge']},indent=2))
assert abs(d['TTM_20260930']['sales']-881.242)<1e-6
assert abs(d['TTM_20260930']['ebit']-165.339)<1e-6
