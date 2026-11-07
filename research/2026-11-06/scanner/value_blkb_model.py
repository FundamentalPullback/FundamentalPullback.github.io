import json
from pathlib import Path
# Preliminary FCFF cross-check, not a completed Stage 3 valuation. USD millions.
R0=1159.634
DEBT=1046.494
EXCESS_CASH=0
SHARES=45.7
cases={
 'adverse':dict(growth=.02,margin0=.19,margin5=.19,wacc=.105,tg=.02,roic=.12,tax=.25,capex=.058,da_start=.072,da_end=.058,wc=.05),
 'central':dict(growth=.04,margin0=.205,margin5=.22,wacc=.095,tg=.025,roic=.15,tax=.245,capex=.055,da_start=.072,da_end=.058,wc=.00),
 'favorable':dict(growth=.055,margin0=.215,margin5=.24,wacc=.085,tg=.03,roic=.18,tax=.245,capex=.055,da_start=.072,da_end=.058,wc=.00)
}
def value(p):
 rows=[];r=R0
 for y in range(1,11):
  g=p['growth'] if y<=5 else p['growth']+(p['tg']-p['growth'])*(y-5)/5
  oldr=r;r*=1+g
  margin=p['margin0']+(p['margin5']-p['margin0'])*min(y-1,4)/4
  da=r*(p['da_start']+(p['da_end']-p['da_start'])*(y-1)/9)
  capex=r*p['capex'];nwc=(r-oldr)*p['wc'];nopat=r*margin*(1-p['tax'])
  fcf=nopat+da-capex-nwc
  rows.append(dict(year=y,revenue=r,margin=margin,ebit=r*margin,nopat=nopat,da=da,capex=capex,nwc=nwc,fcff=fcf,pv=fcf/(1+p['wacc'])**y))
 terminalnopat=rows[-1]['nopat']*(1+p['tg'])
 terminalreinv=terminalnopat*p['tg']/p['roic']
 terminalfcf=terminalnopat-terminalreinv
 tv=terminalfcf/(p['wacc']-p['tg'])/(1+p['wacc'])**10
 ev=sum(x['pv'] for x in rows)+tv
 return dict(assumptions=p,rows=rows,enterprise_value=ev,terminal_weight=tv/ev,equity_value=ev-DEBT+EXCESS_CASH,value_per_share=(ev-DEBT+EXCESS_CASH)/SHARES,terminal_fcff=terminalfcf,terminal_reinvestment=terminalreinv)
res={k:value(v) for k,v in cases.items()}
res['central']['interpretation']='Central operating assumptions discounted at a conservative discretionary 9.5%; retained as a sensitivity case, not an adopted base valuation or calibrated required return.'
res['sensitivity']=[dict(wacc=w,tg=g,value=value(cases['central']|{'wacc':w,'tg':g})['value_per_share']) for w in [.085,.095,.105] for g in [.02,.025,.03]]
res['discount_sensitivity_same_operations']=[dict(wacc=w,value=value(cases['central']|{'wacc':w})['value_per_share']) for w in [.07,.075,.08,.085,.09,.095]]
lo,hi=.04,.20
for _ in range(100):
 mid=(lo+hi)/2
 if value(cases['central']|{'wacc':mid})['value_per_share']>54.12: lo=mid
 else: hi=mid
reverse_wacc=(lo+hi)/2
rf=.0486; beta=1.03; assumed_erp=.045; observed_debt_rate=.0563; tax=.245
market_equity=44.978875*54.12
debt_weight=DEBT/(DEBT+market_equity)
cost_equity=rf+beta*assumed_erp
illustrative_wacc=cost_equity*(1-debt_weight)+observed_debt_rate*(1-tax)*debt_weight
res['discount_rate_review']={
 'reverse_wacc_at_54_12':reverse_wacc,
 'reverse_residual':value(cases['central']|{'wacc':reverse_wacc})['value_per_share']-54.12,
 'risk_free':rf,'beta':beta,'assumed_erp':assumed_erp,'observed_debt_rate':observed_debt_rate,'tax':tax,
 'market_equity_basic':market_equity,'debt_weight':debt_weight,'cost_equity':cost_equity,
 'illustrative_wacc':illustrative_wacc,
 'illustrative_value':value(cases['central']|{'wacc':illustrative_wacc}),
 'conclusion':'At $54.12, valuation is plausible at a reasonable illustrative WACC around 8%. The original 9.5% case is a conservative discount scenario, not an adopted base or evidence of economic rejection. The reverse WACC is a numerical implication of this model, not a validated decision threshold. These are present-value sensitivities, not future share-price targets. Calibration remains preliminary.',
 'limitations':['ERP is an analyst assumption, not a verified current implied premium.','Observed debt cost is an average book borrowing rate, not current marginal funding cost.','Capital weights use reference share price $54.12 times current basic shares and book gross debt; these price-dependent current weights may not be suitable steady-state weights after deleveraging.','Beta estimates are source- and window-dependent.','No new Stage 3 or entry approval.'],
 'sources':{
  'risk_free':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve',
  'beta':'https://stockanalysis.com/stocks/blkb/',
  'debt_rate_shares':'https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm'
 }
}
assert abs(res['discount_rate_review']['reverse_residual'])<1e-7
assert all(a['value']>b['value'] for a,b in zip(res['discount_sensitivity_same_operations'],res['discount_sensitivity_same_operations'][1:]))
res['anchor']={'revenue':R0,'debt':DEBT,'excess_cash':EXCESS_CASH,'shares':SHARES,'price':54.12}
res['definitions']='FCFF = EBIT*(1-tax)+D&A-capex-deltaNWC; SBC retained in EBIT. No future buybacks. Cash reserve is all corporate cash. D&A includes noncash acquisition amortization and fades; capitalized software is included in capex. Terminal reinvestment is NOPAT*g/ROIC. Annual growth assumed primarily from pricing/productivity; no annual ROIC floor imposed. This is an assumption-sensitive screening model, not full Stage 3.'
Path('scanner_nov6/value_blkb_model.json').write_text(json.dumps(res,indent=2))
for k in cases:print(k,res[k]['value_per_share'],res[k]['terminal_weight'],res[k]['rows'][0]['fcff'])
print('sensitivity',res['sensitivity'])
