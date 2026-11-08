"""Controlled deterministic diagnostic, USD millions. Not an approved valuation."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# Primary SEC statement extraction, source IDs in source_manifest.json.
keys=['revenue','ebit','net_income','cfo','da','ppe','software','sbc']
h={}
for y,v in {2023:[2748.377,279.841,307.568,705.513,91.323,12.950,26.958,284.558],2024:[2808.332,380.208,303.281,752.469,108.074,14.208,29.290,282.847],2025:[2883.501,266.210,162.982,693.414,101.845,15.386,39.278,244.745]}.items():h['FY'+str(y)]={**dict(zip(keys,v)),'basis':'as-reported group; includes disposed businesses until sale','source':'FY25'}
a25=dict(zip(keys,[2001.865,136.813,52.247,376.290,76.951,14.120,31.308,181.390]))
a24=dict(zip(keys,[1956.170,225.076,173.375,437.510,81.672,10.174,22.860,214.692]))
h['Q4_2025']={k:h['FY2025'][k]-a25[k] for k in keys};h['Q4_2025'].update(basis='Etsy plus Depop; derived FY25 less 9M25',source='FY25+Q325')
for period,v in {'Q1_2026':[631.277,119.846,104.662,102.536,15.315,1.484,8.378,52.963],'Q2_2026':[668.313,125.268,114.339,268.441-102.536,30.544-15.315,2.718-1.484,14.915-8.378,104.147-52.963],'Q3_2026':[692.469,111.433,113.637,511.293-268.441,46.603-30.544,4.122-2.718,19.994-14.915,149.852-104.147]}.items():h[period]={**dict(zip(keys,v)),'basis':'continuing Etsy only','source':period[:2]+'26'}
h['TTM_2025_09']={k:h['FY2024'][k]+a25[k]-a24[k] for k in keys};h['TTM_2025_09'].update(basis='as reported group, changing perimeter',source='FY25+Q325')
# Total historic operating perimeter reconstructs discontinued Depop revenue/operating loss.
h['TTM_2026_09']={'revenue':2883.501-2001.865+1992.059+138.586,'ebit':266.210-136.813+356.547-294.677,'net_income':162.982-52.247+876.547,'cfo':598.110,'da':None,'ppe':5.519,'software':35.466,'sbc':None,'basis':'total historic operating perimeter; NOT comparable Etsy-only','source':'FY25+Q325+Q326 note2'}
for v in h.values():
 v['ebit_margin']=v['ebit']/v['revenue']
 v['fcf']=v['cfo']-v['ppe']-v['software'] if v['ppe'] is not None else 557.125
 v['fcf_less_sbc_check']=v['fcf']-v['sbc'] if v['sbc'] is not None else None
# Forecast begins FY27; FY26 starting GMS = 9M actual + Q4 guidance midpoint, take = derived.
gms0=7689.975+3490
rev0=1992.059+3490*.256
equity_market=86.205886*89.93; debt=2350
rf=.0486; beta=1.78; erp=.0441 # Damodaran November 1 2026 trailing-12-month adjusted payout; unadjusted UST basis
kd=.0686; tax=.24
wacc=(rf+beta*erp)*equity_market/(equity_market+debt)+kd*(1-tax)*debt/(equity_market+debt)
# Operating lease expense retained in EBIT, not separately debt deducted. Finance lease claim deducted.
cash=2065.658+245.043+150.392-648.6-200 # operational cash reserve analyst estimate
financelease=96.4 # rounded current+long term, diagnostic
shares=87.914+6.812+(1.517-1.102) # September dated bridge; 9M exercised options removed, no proceeds credit; forfeitures/new grants unverified
netclaims=debt+financelease-cash
cases={'adverse':dict(growth=.00,margin=.16,wacc=wacc+.015,g=.015,roic=.12), 'central':dict(growth=.06,margin=.22,wacc=wacc,g=.025,roic=.20),'favorable':dict(growth=.10,margin=.26,wacc=wacc-.01,g=.03,roic=.25)}
def calc(c,margin_override=None):
 gm=gms0; prior_rev=rev0; rows=[]; pv=0
 for y in range(1,11):
  gr=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  gm*=1+gr;take=.258 if y<=5 else .258
  rev=gm*take; margin=.20+(c['margin']-.20)*min(y/5,1) if margin_override is None else margin_override
  ebit=rev*margin;nopat=ebit*(1-tax);da=.018*rev
  # Growth funding: economic reinvestment paid via net capex, plus 1% incremental revenue WC.
  nwc=max(0,rev-prior_rev)*.01
  reinvest=max(0,rev-prior_rev)*margin*(1-tax)/c['roic']
  capex=da+max(0,reinvest-nwc);fcff=nopat+da-capex-nwc
  pv+=fcff/(1+c['wacc'])**y
  rows.append(dict(year=2026+y,gms=gm,take_rate=take,revenue=rev,ebit_margin=margin,ebit=ebit,tax=tax,nopat=nopat,da=da,capex_including_software=capex,delta_nwc=nwc,fcff=fcff));prior_rev=rev
 terminal=rows[-1]['nopat']*(1+c['g'])*(1-c['g']/c['roic'])/(c['wacc']-c['g']);pvt=terminal/(1+c['wacc'])**10;ev=pv+pvt
 # if-converted treatment switches entire claim, never subtract debt and include converted shares.
 value=(ev-netclaims)/shares;convert=False
 if value>85.79:
  value=(ev-netclaims+700)/(shares+700/85.79);convert=True
 return dict(value=value,ev=ev,netclaims=netclaims,shares=shares+(700/85.79 if convert else 0),convert2025=convert,pv_fcff=pv,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_reinvestment_rate=c['g']/c['roic'],rows=rows,assumptions=c)
r={k:calc(v) for k,v in cases.items()}
lo,hi=.01,.70
for _ in range(70):
 mid=(lo+hi)/2
 if calc(cases['central'],mid)['value']<89.93:lo=mid
 else:hi=mid
out=dict(asof='2026-11-08',price=89.93,price_date='2026-11-06 16:00 America/New_York',readiness='screen-grade',valuationReady=False,entryApproved=False,history=h,comparable_etsy_only_ttm=None,forecast_base=dict(gms=gms0,revenue=rev0),capm=dict(rf=rf,beta=beta,erp=erp,kd=kd,tax=tax,wacc=wacc),bridge=dict(cash_after_maturity_and_reserve=cash,debt=debt,financelease=financelease,shares=shares),cases=r,reverse_constant_margin=(lo+hi)/2,sensitivity=[dict(wacc=w,g=g,value=calc({**cases['central'],'wacc':w,'g':g})['value']) for w in [.09,.105,.12,.135] for g in [.015,.025,.03]])
assert abs(sum(h[q]['revenue'] for q in ['Q1_2026','Q2_2026','Q3_2026'])-1992.059)<1e-8
assert abs(sum(h[q]['cfo'] for q in ['Q1_2026','Q2_2026','Q3_2026'])-511.293)<1e-8
assert all(c['assumptions']['wacc']>c['assumptions']['g'] for c in r.values())
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'history.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=['period']+list(h['FY2023']));wr.writeheader()
 for p,v in h.items():wr.writerow({'period':p,**v})
print(json.dumps({k:round(v['value'],2) for k,v in r.items()}));print('WACC',wacc,'Reverse margin',(lo+hi)/2)
