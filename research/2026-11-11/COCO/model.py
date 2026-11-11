import json,csv,math,pathlib
P=pathlib.Path(__file__).parent
price=65.95
cases={
'bear':dict(revenues=[870,922,968,1007,1047,1089,1132,1177,1224,1273],margins=[.13,.135,.14,.14,.14,.14,.14,.14,.14,.14],tax=.26,nwc=.22,capex=.025,da=.008,wacc=.104925,g=.02,roic=.15,earnout=45),
'base':dict(revenues=[980,1117.2,1251.264,1376.3904,1486.5016,1590.5567,1685.9901,1770.2896,1841.1012,1896.3342],margins=[.165,.17,.175,.175,.175,.175,.175,.175,.175,.175],tax=.25,nwc=.18,capex=.02,da=.008,wacc=.0939,g=.025,roic=.20,earnout=70),
'bull':dict(revenues=[1050,1239,1437.24,1638.4536,1835.068,2018.575,2180.061,2310.865,2426.408,2523.464],margins=[.185,.195,.205,.21,.215,.215,.215,.215,.215,.215],tax=.23,nwc=.16,capex=.018,da=.008,wacc=.082875,g=.03,roic=.25,earnout=100)}
# Ten forward annual periods, not fiscal-year cash flows. Source date Sep30 plus only known October repurchase. Not precise current fair values.
base_rev=875 # analyst full-year economic perimeter reference: guide815 less approx40 Copra partial-year plus100 full-year
cash=151.995-7.614-19 # observed cash less disclosed repurchase less analyst operating reserve; unknown intervening cash excluded
shares=57.063861+2.195236+.878911 # basic Oct20 plus vested options, no proceeds, no unvested awards; conservative proxy not full dilution valuation

def calc(c, revenue_scale=1.,margin_shift=0.,wacc=None,g=None):
 w=wacc or c['wacc'];g=c['g'] if g is None else g;prior=base_rev;prior_nwc=base_rev*.18;rows=[];pv=0
 for i,(r,m) in enumerate(zip(c['revenues'],c['margins']),1):
  r*=revenue_scale;m+=margin_shift;ebit=r*m;nopat=ebit*(1-c['tax']);da=r*c['da'];cap=r*c['capex'];nwc=r*c['nwc'];delta=nwc-prior_nwc;fcff=nopat+da-cap-delta;v=fcff/(1+w)**i;pv+=v
  rows.append(dict(period=i,revenue=r,growth=r/prior-1,ebit_margin=m,ebit=ebit,tax=nopat*c['tax']/(1-c['tax']),nopat=nopat,da=da,capex=cap,nwc=nwc,delta_nwc=delta,fcff=fcff,pv=v));prior=r;prior_nwc=nwc
 terminal_nopat=rows[-1]['nopat']*(1+g);terminal_reinvestment=terminal_nopat*g/c['roic'];terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(w-g);pvtv=tv/(1+w)**10;ev=pv+pvtv
 # Liability replaced, not duplicated: scenario nominal earnout PV in approx 2.4 years. Not an inferred contractual payoff curve.
 earnpv=c['earnout']/(1+w)**2.4;equity=ev+cash-earnpv
 return dict(rows=rows,ev=ev,equity=equity,value=equity/shares,pv_forecast=pv,pv_terminal=pvtv,terminal_pct=pvtv/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,terminal_roic=c['roic'],cash_bridge=cash,shares=shares,earnout_pv=earnpv,wacc=w,g=g)
results={k:calc(v) for k,v in cases.items()}
# reverse growth: first-period revenue fixed at base980; apply a constant annual growth for remaining9 periods; same margin/capital mechanics as base
lo,hi=0,.6
for _ in range(100):
 x=(lo+hi)/2;c=dict(cases['base']);c['revenues']=[980*(1+x)**i for i in range(10)];v=calc(c)['value']
 if v<price:lo=x
 else:hi=x
reverse_growth=(lo+hi)/2
lo,hi=0,.6
for _ in range(100):
 x=(lo+hi)/2;c=dict(cases['base']);c['margins']=[x]*10;v=calc(c)['value']
 if v<price:lo=x
 else:hi=x
reverse_margin=(lo+hi)/2
sens=[dict(wacc=w,g=g,value=calc(cases['base'],wacc=w,g=g)['value']) for w in [.082875,.0939,.104925,.115] for g in [.02,.025,.03]]
summary={k:{x:y for x,y in v.items() if x!='rows'} for k,v in results.items()}
meta=dict(status='screen-grade; not canonical targets',price=price,price_date='2026-11-10 regular close',valuation_date='2026-11-11',unit='USD millions except per share',base_revenue_perimeter=base_rev,cases=cases,summary=summary,reverse_growth_years2to10=reverse_growth,reverse_constant_ebit_margin=reverse_margin,sensitivity=sens)
(P/'model_results.json').write_text(json.dumps(meta,indent=2))
for k,v in results.items():
 with (P/f'fcff_{k}.csv').open('w') as f:
  z=csv.DictWriter(f,fieldnames=v['rows'][0]);z.writeheader();z.writerows(v['rows'])
checks={'horizon_10':all(len(v['rows'])==10 for v in results.values()),'wacc_gt_g':all(v['wacc']>v['g'] for v in results.values()),'finite':all(math.isfinite(v['value']) for v in results.values()),'positive_terminal_reinvestment':all(v['terminal_reinvestment']>0 for v in results.values()),'forecast_nwc_increases_after_transition':all(all(b['nwc']>=a['nwc'] for a,b in zip(v['rows'],v['rows'][1:])) for v in results.values()),'sbc_treatment':'analyst margin assumption; not source-reconciled','earnout_single_bridge_check':all(abs(v['equity']-(v['ev']+cash-v['earnout_pv']))<1e-9 for v in results.values()),'mechanical_failures':[],'readiness_failures':['Unreconciled share and cash dates','Unverified margin SBC bridge','Terminal asset replacement not independently supported','Peer normalization incomplete'],'limitations':['Forward annual approximation, not fiscal/stub cash-flow timing','Cash since October21 not disclosed','Vested-option no-proceeds dilution proxy; unvested earned portions unresolved','Scenario earnings and reinvestment are analyst estimates; capacity economics not audited','Peer data unnormalized; not recommendation ready']}
(P/'run_log.json').write_text(json.dumps(checks,indent=2));print(json.dumps(dict(summary=summary,reverse_growth=reverse_growth,reverse_margin=reverse_margin),indent=2))
