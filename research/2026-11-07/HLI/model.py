"""Support calculation, USD millions; not an approved valuation or entry level."""
import json,pathlib
P=pathlib.Path(__file__).parent
annual={
 'FY2024':dict(revenue=1914.404,CF=1106.826,FR=521.984,FVA=285.594,ebit=373.234,net_income=280.301,eps=4.11,cfo=328.458,capex=66.730,sbc=166.595,comp_accrual_change=-42.269),
 'FY2025':dict(revenue=2389.416,CF=1526.756,FR=544.478,FVA=318.182,ebit=502.567,net_income=399.711,eps=5.82,cfo=848.609,capex=39.699,sbc=168.443,comp_accrual_change=210.254),
 'FY2026':dict(revenue=2617.516,CF=1744.634,FR=528.655,FVA=344.227,ebit=527.019,net_income=425.697,eps=6.22,cfo=704.131,capex=22.312,sbc=201.304,comp_accrual_change=128.217)}
h1prev=dict(revenue=1088.566,CF=692.445,FR=248.990,FVA=147.131,ebit=225.409,net_income=182.489,cfo=224.711,capex=21.368,sbc=78.396,comp_accrual_change=-84.213)
h1old=dict(revenue=1264.801,CF=837.180,FR=262.019,FVA=165.602,ebit=241.141,net_income=209.314,cfo=193.416,capex=15.423,sbc=88.852,comp_accrual_change=-111.735)
h1new=dict(revenue=1203,CF=784,FR=237,FVA=182,ebit=232,net_income=187,cfo=-84,capex=18,sbc=87,comp_accrual_change=-308)
def ttm(a,b,c):return {k:a[k]-b[k]+c[k] for k in c}
cur=ttm(annual['FY2026'],h1old,h1new);prev=ttm(annual['FY2025'],h1prev,h1old)
quarters=[dict(period='Q3 FY2026',revenue=717.072,ebit=160.730,net_income=116.548,eps=1.70,cfo=411.098-193.416,capex=16.062-15.423,CF=473.688,FR=156.253,FVA=87.131),dict(period='Q4 FY2026',revenue=635.643,ebit=125.148,net_income=99.835,eps=1.47,cfo=704.131-411.098,capex=22.312-16.062,CF=433.766,FR=110.383,FVA=91.494),dict(period='Q1 FY2027',revenue=511,ebit=78,net_income=78,eps=1.15,cfo=-336,capex=6,CF=303,FR=119,FVA=89),dict(period='Q2 FY2027',revenue=692,ebit=154,net_income=109,eps=1.64,cfo=252,capex=12,CF=481,FR=118,FVA=93)]
for x in list(annual.values())+[cur,prev]+quarters:
 x['fcf_cfo_less_capex']=x['cfo']-x['capex'];x['operating_margin']=x['ebit']/x['revenue']
for x in list(annual.values())+[cur,prev]:x['fcf_less_sbc_diagnostic']=x['fcf_cfo_less_capex']-x['sbc']
history=dict(units='USD millions; EPS USD/share; FY ends March 31',annual=annual,quarters=quarters,ttm_sep2026=cur,ttm_sep2025=prev,rounding='FY2027 filing reports whole millions. Derived TTM and quarterly cash flows are approximate, not falsely precise.',source_files=['fy2026_10k','q2fy2026_10q','q3fy2026_10q','q1fy2027_10q','q2fy2027_10q'])
(P/'history.json').write_text(json.dumps(history,indent=2))
CASES={'bajista':dict(growth=[-.05,.02,.04],margin=.18,terminal_margin=.19,wacc=.112,terminal_growth=.025,roic=.25,terminal_roic=.15,reserve=800,claims=100), 'base':dict(growth=[.08,.04,.08],margin=.205,terminal_margin=.22,wacc=.0486+1.12*.0441,terminal_growth=.03,roic=.35,terminal_roic=.20,reserve=650,claims=75),'alcista':dict(growth=[.13,.07,.10],margin=.22,terminal_margin=.24,wacc=.09,terminal_growth=.035,roic=.45,terminal_roic=.25,reserve=500,claims=56.670)}
def dcf(c,wacc=None,tg=None,scale=1):
 c=c.copy();wacc=wacc or c['wacc'];tg=c['terminal_growth'] if tg is None else tg
 seg=[cur[k] for k in ['CF','FR','FVA']];rows=[];pv=0;old=sum(seg);previous_nopat=cur['ebit']*.72
 for y in range(1,11):
  fade=max(0,(y-5)/5);g=[((v*scale)*(1-fade)+tg*fade) for v in c['growth']];seg=[s*(1+v) for s,v in zip(seg,g)];rev=sum(seg)
  margin=c['margin']+(c['terminal_margin']-c['margin'])*(y-1)/9;nopat=rev*margin*.72
  roic=c['roic']+(c['terminal_roic']-c['roic'])*(y-1)/9
  # Contemporaneous annual convention: investment during t supports delta NOPAT_t;
  # both investment and operating cash are discounted at end t. No capital release on contraction.
  delta_nopat=nopat-previous_nopat;reinvest=max(0,delta_nopat)/roic;fcff=nopat-reinvest;pv+=fcff/(1+wacc)**y
  rows.append(dict(year=y,segments=seg.copy(),revenue=rev,margin=margin,nopat=nopat,incremental_roic=roic,previous_nopat=previous_nopat,incremental_nopat=delta_nopat,reinvestment=reinvest,fcff=fcff));old=rev;previous_nopat=nopat
 terminal_nopat=nopat*(1+tg);terminal_reinvestment=(terminal_nopat-nopat)/c['terminal_roic'];terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(wacc-tg);pvtv=tv/(1+wacc)**10;ev=pv+pvtv
 # Hypothetical bridge, not a verified total debt/earnout schedule.
 excess=max(0,888-c['reserve']);equity=ev+excess-111-c['claims'];shares=69.7
 return dict(value_per_share=equity/shares,enterprise_value=ev,equity_value=equity,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,excess_cash=excess,redeemable_nci=111,assumed_debt_and_earnouts=c['claims'],economic_shares=shares,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,rows=rows)
out={k:dcf(v) for k,v in CASES.items()}
sens=[dict(wacc=w,g=g,value=dcf(CASES['base'],w,g)['value_per_share']) for w in [.09,.10,.11] for g in [.025,.03,.035]]
lo,hi=0,5
for _ in range(100):
 mid=(lo+hi)/2
 if dcf(CASES['base'],scale=mid)['value_per_share']<145.86:lo=mid
 else:hi=mid
results=dict(posture='screen-grade',entry_approved=False,maximum_fundamental_price=None,price=145.86,scenarios=out,assumptions=CASES,sensitivity=sens,reverse_growth_multiplier=(lo+hi)/2,reverse_growth_first5=[g*(lo+hi)/2 for g in CASES['base']['growth']],caveats=['Economic bridge not reconciled: operating cash reserve, full acquisition liabilities and redeemable NCI valuation.','ROIC reinvestment and segment forecasts are analyst assumptions, not company guidance.','Economic shares use 69.4m outstanding A+B plus 0.3m RSUs; unvested restricted shares already included, not added again.','Recurring SBC stays in margins, not added back. No separate perpetual dilution charge; avoid double counting.','Rent remains operating expense; lease liabilities not subtracted again.','Tax 28% normalized, not quarter-specific SBC windfall.'])
(P/'model_results.json').write_text(json.dumps(results,indent=2))
checks={'incremental_investment_ties':all(abs(r['reinvestment']-max(0,r['nopat']-r['previous_nopat'])/r['incremental_roic'])<1e-8 for case in out.values() for r in case['rows']),'terminal_investment_ties':all(abs(out[k]['terminal_reinvestment']-(out[k]['terminal_nopat']-out[k]['rows'][-1]['nopat'])/v['terminal_roic'])<1e-8 for k,v in CASES.items()),'ttm_revenue_matches_quarters':abs(sum(x['revenue'] for x in quarters)-cur['revenue'])<.01,'ttm_cash_matches_quarters':abs(sum(x['cfo'] for x in quarters)-cur['cfo'])<.01,'wacc_above_terminal_growth':all(v['wacc']>v['terminal_growth'] for v in CASES.values()),'ordered_scenarios':out['bajista']['value_per_share']<out['base']['value_per_share']<out['alcista']['value_per_share']}
(P/'run_log.json').write_text(json.dumps(dict(artifact='deterministic support calculation',checks=checks,status='screen-grade',hard_failures=[],decision_blockers=results['caveats'][:2]),indent=2))
print({k:round(v['value_per_share'],2) for k,v in out.items()});print('TTM',cur,'prior',prev);print('reverse',results['reverse_growth_first5']);assert all(checks.values())
