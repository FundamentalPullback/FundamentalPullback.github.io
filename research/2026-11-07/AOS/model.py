"""AOS analyst FCFF scenarios, USD millions. Standard library; no network needed.
Run in any folder: python model.py. Inputs are disclosed estimates, not consensus.
"""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
fields=['sales','gross','sga','restructuring','interest','pretax','net','da','sbc','cfo','capex']
def row(v):
 d=dict(zip(fields,v));d['ebit']=d['gross']-d['sga']-d['restructuring'];d['fcf']=d['cfo']-d['capex'];d['cash_after_sbc']=d['fcf']-d['sbc'];return d
h={
'FY2023':row([3852.8,1484.8,727.4,18.8,12,733.5,556.6,78.3,11.5,670.3,72.6]),
'FY2024':row([3818.1,1456.1,739.3,17.6,6.7,701,533.6,78.8,14.9,581.8,108]),
'FY2025':row([3830.2,1487.4,759.4,0,13.5,715.1,546.2,85.1,13.8,616.8,70.8]),
'9M2024':row([2905.7,1118,557.3,0,4.3,555.9,423.9,59.5,12.7,359.9,77.4]),
'9M2025':row([2917.7,1137,572.8,0,11.1,554.5,420.8,62.8,11.3,433.7,53.2]),
'9M2026':row([2890.4,1118.2,591.1,22.6,22.9,479.4,369.2,72.5,12.7,429.4,33.2]),
'Q1 2026':row([945.6,365.7,203.9,0,7.1,154.7,118,23.9,6.6,129.4,10.5]),
'6M2026':row([1949.9,753.5,401.6,22.6,15.2,312.7,242.9,48.5,9.3,253.8,20.5])}
def difference(a,b):return {k:round(a[k]-b[k],7) for k in a}
h['Q4 2025']=difference(h['FY2025'],h['9M2025']);h['Q2 2026']=difference(h['6M2026'],h['Q1 2026']);h['Q3 2026']=difference(h['9M2026'],h['6M2026'])
for year in [2025,2026]:h['TTM'+str(year)]={k:round(h['FY'+str(year-1)][k]+h['9M'+str(year)][k]-h['9M'+str(year-1)][k],7) for k in fields+['ebit','fcf','cash_after_sbc']}
capital={'price':64.55,'price_date':'2026-11-06','class_a':25.860239,'common':108.468717,'incremental_dilution':0.734055,'debt':673.1,'cash':234.5,'operating_cash_reserve':100,'additional_pension_reserve':7.5,'restructuring_cash_reserve':9.3}
capital['shares']=capital['class_a']+capital['common']+capital['incremental_dilution']
cases={'bear':dict(growth=.01,margin_start=.19,margin5=.185,margin10=.18,wacc=.1075,g=.02,roic=.12,china=240), 'base':dict(growth=.04,margin_start=.20,margin5=.21,margin10=.21,wacc=.0975,g=.025,roic=.16,china=320), 'bull':dict(growth=.06,margin_start=.205,margin5=.23,margin10=.225,wacc=.09,g=.03,roic=.20,china=400)}
def model(p,tax=.25,net_floor=.005,reserve=100,china=None,royalty=0):
 rev=3280.;nop=rev*p['margin_start']*(1-tax);rows=[];pv=0
 for y in range(1,11):
  growth=p['growth'] if y<=5 else p['growth']+(p['g']-p['growth'])*(y-5)/5
  margin=p['margin_start']+(p['margin5']-p['margin_start'])*y/5 if y<=5 else p['margin5']+(p['margin10']-p['margin5'])*(y-5)/5
  r=rev*(1+growth);n=r*margin*(1-tax);wc=max(0,r-rev)*.12
  # Fund BOTH incremental profit (growth and margin gains) and physical replenishment.
  reinv=max(max(0,n-nop)/p['roic'],r*net_floor+wc)
  da=r*.025;capex=da+reinv-wc;fcff=n+da-capex-wc;disc=fcff/(1+p['wacc'])**y;pv+=disc
  rows.append(dict(year=y,revenue=r,growth=growth,margin=margin,ebit=r*margin,nopat=n,da=da,capex=capex,dnwc=wc,net_reinvestment=reinv,fcff=fcff,pv=disc));rev=r;nop=n
 r=rev*(1+p['g']);n=r*p['margin10']*(1-tax);terminal_reinv=max(n*p['g']/p['roic'],r*net_floor+(r-rev)*.12)
 terminal_fcff=n-terminal_reinv;tv=terminal_fcff/(p['wacc']-p['g']);pvt=tv/(1+p['wacc'])**10;ev=pv+pvt
 # China is a separate gross business asset, debt stays deducted in full; cash is not counted twice.
 bridge=capital['cash']-reserve-capital['debt']-capital['additional_pension_reserve']-capital['restructuring_cash_reserve']+(p['china'] if china is None else china)+royalty
 eq=ev+bridge
 return dict(inputs=p,years=rows,terminal_fcff=terminal_fcff,terminal_reinvestment=terminal_reinv,terminal_value=tv,terminal_pv=pvt,terminal_weight=pvt/ev,ev=ev,equity_bridge=bridge,equity=eq,per_share=eq/capital['shares'])
out={k:model(v) for k,v in cases.items()}
sens=[]
for w in [.0875,.0925,.0975,.1025,.1075]:
 for g in [.015,.02,.025,.03]:sens.append(dict(wacc=w,g=g,value=model(dict(cases['base'],wacc=w,g=g))['per_share']))
lo,hi=-.05,.3
for i in range(90):
 mid=(lo+hi)/2;v=model(dict(cases['base'],growth=mid))['per_share']
 if v<capital['price']:lo=mid
 else:hi=mid
inverse=dict(first_five_year_growth=(lo+hi)/2,margin5=cases['base']['margin5'],margin10=cases['base']['margin10'],wacc=cases['base']['wacc'],g=cases['base']['g'],price_target=capital['price'])
qa={'history_quarters_tie':all(abs(sum(h[q][k] for q in ['Q4 2025','Q1 2026','Q2 2026','Q3 2026'])-h['TTM2026'][k])<1e-6 for k in fields),'fcff_tie':all(abs(r['fcff']-(r['nopat']+r['da']-r['capex']-r['dnwc']))<1e-7 for v in out.values() for r in v['years']),'capex_floor':all(r['capex']>=r['da'] for v in out.values() for r in v['years']),'wacc_gt_g':all(p['wacc']>p['g'] for p in cases.values()),'case_order':out['bear']['per_share']<out['base']['per_share']<out['bull']['per_share'],'status':'screen-grade conditional valuation; no approved entry','assumption_warnings':['China net proceeds/taxes/royalties and retained business cash flow not yet recast','tariff refund amount not quantified in reviewed primary text','WACC beta and ERP are assumptions, not a regression or consensus','Q4 standalone EPS not estimated by subtracting rounded annual EPS']}
other={'tax':[dict(tax=t,value=model(cases['base'],tax=t)['per_share']) for t in [.23,.25,.28]],'roic':[dict(roic=r,value=model(dict(cases['base'],roic=r))['per_share']) for r in [.12,.16,.20]],'physical_floor':[dict(floor=f,value=model(cases['base'],net_floor=f)['per_share']) for f in [0,.005,.01]],'china_total_asset':[dict(china=c,value=model(cases['base'],china=c)['per_share']) for c in [0,240,320,400,500]],'cash_reserve':[dict(reserve=r,value=model(cases['base'],reserve=r)['per_share']) for r in [50,100,150]]}
grid=[dict(growth=x/100,value=model(dict(cases['base'],growth=x/100))['per_share']) for x in range(0,21)]
qa['inverse_growth_monotonic_0_to_20']=all(grid[i+1]['value']>grid[i]['value'] for i in range(len(grid)-1))
qa['inverse_reprices']=abs(model(dict(cases['base'],growth=inverse['first_five_year_growth']))['per_share']-capital['price'])<1e-7
qa['public_source_ledger']='Only public URLs, titles, dates and purpose; no raw filings included.'
qa['visual_review']='Visual layout not independently certified.'
qa['china_geographic_reconciliation']='Unresolved: Q3 geography 139.8 vs 151.7 implies -7.84%, while management states -17% local; no invented FX explanation.'
qa['stage3Complete']=False
qa['entryApproved']=False
qa['approvedValuation']=None
qa['valuationScope']='conditional_research_only'
results=dict(inverse_growth_grid=grid,historical=h,capital=capital,cases=out,sensitivity=sens,inverse=inverse,other_sensitivity=other,qa=qa)
(ROOT/'model.json').write_text(json.dumps(results,indent=2))
(ROOT/'qa.json').write_text(json.dumps(qa,indent=2))
assert all(qa[k] for k in ['history_quarters_tie','fcff_tie','capex_floor','wacc_gt_g','case_order'])
print(json.dumps({'values':{k:round(v['per_share'],2) for k,v in out.items()},'inverse':inverse,'qa':qa},indent=2))
