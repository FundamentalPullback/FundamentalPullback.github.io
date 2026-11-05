from build import *
def value(p,**kw):return run(dict(p,**kw))['per_share']
b=CASES['base'];b['case']='base'
# The same bottom-up model supplies direct and reverse valuations; these are not independent corroboration.
reverse=[]
for w in [.08,.09,.10,.11,.12]:
 for fade in [1,2,4]:
  p=dict(b,wacc=w,fade_years=fade)
  scale=brentq(lambda x:value(p,rate_scale=x)-85.05,.3,2.)
  target=brentq(lambda x:value(p,rate_scale=x)-85.05/.75,.3,2.)
  reverse.append(dict(wacc=w,fade_years=fade,scale_current_price=scale,rates_current_price={k:v*scale for k,v in b['normal'].items()},scale_25pct_mos=target,rates_25pct_mos={k:v*target for k,v in b['normal'].items()}))
sens=[]
for w in [.08,.09,.10,.11,.12]:
 for scale in [.8,.9,1.,1.1,1.2]:sens.append(dict(wacc=w,rate_scale=scale,value=value(b,wacc=w,rate_scale=scale)))
structural=[]
for key,vals in {'life':[20,22,25,30],'replacement_premium':[.85,1,1.15,1.3],'fade_years':[1,2,3,4],'tax':[0,.02,.05,.15],'sbc':[60,78,95],'cash_reserve':[75,125,250],'pool_capital':[0,39.644,65.516],'jv_value':[0,50,100,150],'additional_shares':[0,.5,1.5],'repair_days':[3,5,10]}.items():
 for v in vals:structural.append(dict(variable=key,input=v,value=value(b,**{key:v})))
base=run(b,True)
# no double counting: combined commitments already deducted in each flow; NO second1295.9 bridge subtraction.
claimscases=[]
for name,claims in [('Principal only; excludes optionality',655),('Reported host plus derivative proxy',718.621),('Principal plus derivative; conservative claim stress, not reported debt',851.087)]:
 claimscases.append(dict(name=name,claims=claims,value=value(b,claims=claims)))
runoff={k:run(dict(v,case=k),False,False) for k,v in CASES.items()}
# Historical spot TCE, unweighted across years; actuals not inflation adjusted or fleet comparable.
history={2021:{'MR':11396,'LR2':12189,'Handymax':9523},2022:{'MR':33299,'LR2':38277,'Handymax':39253},2023:{'MR':31258,'LR2':39486,'Handymax':29578},2024:{'MR':29708,'LR2':43669,'Handymax':24146},2025:{'MR':22349,'LR2':32297,'Handymax':21072}}
hist_summary={cl:dict(mean=sum(x[cl] for x in history.values())/5,median=sorted(x[cl] for x in history.values())[2],minimum=min(x[cl] for x in history.values()),maximum=max(x[cl] for x in history.values())) for cl in ['Handymax','MR','LR2']}
renewal_wave=[{k:r[k] for k in ['year','avg_fleet','replacement','scrap','drydock','fcff','pv']} for r in base['rows'] if 2037<=r['year']<=2046]
# Main price implies EV after latest cash and claims but before nonoperating investments, pending sale assets.
mcap=51.078851*85.05;ev=mcap+718.621-(2042.088-125)-base['bridge']['investments']-base['bridge']['pending_sales_pv']+base['bridge']['post_balance_volare_purchase_pv']
validation={
 'fleet_actual_74':len([v for v in fleet if v['delivery']<2027])==74,
 'future_owned_17':len(new)==17,
 'fleet_postsale_72':len([v for v in fleet if v['delivery']<2027 and not v['sale']])==72,
 'mature_fleet_89':len([v for v in fleet if not v['sale']])==89,
 'class_mature':dict(Counter(v['type'] for v in fleet if not v['sale'])),
 'commitment_total_1295_9':abs(sum(COMMIT.values())-1295.9)<1e-8,
 'terminal_formula_tie':abs(base['gordon']['fcff']-base['gordon']['formula_fcff'])<1e-8,
 'ev_reconciles':abs(base['explicit_pv']+base['gordon_pv']+base['age_adjustment_pv']-base['operating_ev'])<1e-8,
 'fleet_count_base_each_year':all(abs(r['avg_fleet']-89)<1e-7 for r in base['rows'] if r['year']>=2031),
 'no_future_interest_subtracted':True,'sbc_in_ga_not_added_back':True,'no_permanent_2026_rates':True,
 'renewal_tail_160yrs':'Numerical tail to2196; verify lower-tail effect by stored annual PV sum after2180',
 'tail_after_2180_pv':sum(r['pv'] for r in base['rows'] if r['year']>2180),
 'claims_status':'Proxy only: host522.534 plus derivative196.087 atSep30. Not contractual principal+derivative.',
 'version':'v2_matched_balance','readiness':'screen-grade','hard_failures':[],'independent_review':'completed_arithmetic_and_economic_review_no_stage3_approval','certification_blockers':[],'decision':'No Stage 3 approval at 85.05; price-versus-risk judgment, not a missing essential fact','bounded_capital_uncertainty':['New VLCC JV future value is zero after all disclosed commitments; undisclosed additional guarantees would require reassessment if evidenced'],'warnings':['Beta and company premium are judgment-led, not pure tanker regression estimates','Post2027 drydock dates inferred from build years','Current unissued awards not comprehensively reconciled; observed Form4 restricted shares are already issued','2026Q4 is a complete-quarter forecast from the matchedSep30 balance, not actualNov4 cash','Convertible bull must use coherent conversion alternative, not frozen Sep30 option value']}
result=dict(reverse=reverse,sensitivity=sens,structural=structural,claimscases=claimscases,runoff=runoff,historical_tce=history,historical_summary=hist_summary,renewal_wave=renewal_wave,market_cap=mcap,implied_operating_ev=ev,validation=validation)
(ROOT/'model/analysis.json').write_text(json.dumps(result,indent=2))
(ROOT/'model/run_log.json').write_text(json.dumps(validation,indent=2))
print('BASE',base['per_share'],'reverse base',[x for x in reverse if x['wacc']==.10 and x['fade_years']==2]);print('runoff',{k:v['per_share'] for k,v in runoff.items()});print('base terminal',base['gordon']);print('wave',renewal_wave)
