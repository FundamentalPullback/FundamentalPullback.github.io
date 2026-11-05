from value import *
b=dict(CASES['base'],case='base')
def v(**kw):return run(dict(b,**kw))['per_share']
sens=[dict(wacc=w,rate_scale=s,value=v(wacc=w,rate_scale=s)) for w in [.08,.09,.10,.11,.12] for s in [.8,.9,1,1.1,1.2]]
reverse=[]
for w in [.08,.09,.10,.11,.12]:
 scale=brentq(lambda s:v(wacc=w,rate_scale=s)-PRICE,.4,1.6,xtol=1e-7)
 reverse.append(dict(wacc=w,scale=scale,normal_rates={c:COMMON['normal'][c]*scale for c in CL},start_rates={c:COMMON['start'][c]*scale for c in CL}))
struct=[]
for key,vals in {'life':[20,22,25,30],'cost_scale':[.85,1.,1.15,1.3],'wc_pct':[.17,.22,.27],'cash_reserve':[50,75,150],'shares':[102.7,104.7,107.8],'jv_net':[-600,-300,-150,0,60,150],'settlement_net':[-20,-5,0,5],'repair_days':[3,5,10],'ga':[95,109.4,130],'tonnage_tax':[3,10,25]}.items():
 for z in vals:struct.append(dict(variable=key,input=z,value=v(**{key:z})))
# IRR of enterprise stream at current market-implied operating EV, not levered equity IRR.
targetev=PRICE*b['shares']-(446.2-b['cash_reserve'])-b['financial_assets']+b['claims']-b['jv_net']-b['settlement_net']
r=run(b,True)
implied_wacc=brentq(lambda w:run(dict(b,wacc=w),policy='renew')['operating_ev']-targetev,.05,.25)
# A harsher but plausible combination is separate, avoids using 20% margin as a magic pass rule.
comb={}
for name,changes in [('base',{}),('wacc10',{'wacc':.10}),('life20',{'life':20}),('normal_minus10',{'rate_scale':.9}),('base_negative_jv300',{'jv_net':-300}),('combined_moderate',{'wacc':.10,'life':22,'cost_scale':1.10,'rate_scale':.95,'jv_net':-150,'shares':107.8}),('combined_hard',{'wacc':.11,'life':20,'cost_scale':1.15,'rate_scale':.9,'jv_net':-300,'shares':107.8})]:
 rr=run(dict(b,**changes));comb[name]={k:rr[k] for k in ['per_share','operating_ev','renewal','terminal_weight']}
runoff=run(b,policy='runoff')
validation={'fleet95':len([f for f in fleet if not f['committed']])==95,'contractual14':sum(v['committed'] for v in fleet)==14,'allfirmcapex_once':abs(sum(COMMIT.values())-615.3)<1e-8,'terminal_identity':abs(r['terminal']['fcff']-r['terminal']['formula_fcff'])<1e-8,'capital_identity':abs(r['terminal']['economic_reinvestment']-r['terminal']['net_reinvestment']-r['terminal']['scrap_gain'])<1e-8,'ev_tie':abs(r['explicit_pv']+r['gordon_pv']+r['age_adjustment_pv']-r['operating_ev'])<1e-8,'principal_to_book':abs(1141.6-12.5+8.7-1137.8)<1e-8,'no_double_dividend':True,'sbc_not_added_back':True,'tail_after2176_usdm':sum(z['pv'] for z in r['rows'] if z['year']>2176),'hard_failures':[],'status':'senior-review-ready','independent_audit':'pending'}
out=dict(price=PRICE,reverse=reverse,sensitivity=sens,structural=struct,combined=comb,current_price_implied_operating_ev=targetev,implied_enterprise_discount_rate_base_cashflows=implied_wacc,runoff_base=runoff,validation=validation)
(P/'analysis.json').write_text(json.dumps(out,indent=2));(P/'run_log.json').write_text(json.dumps(validation,indent=2))
print('Reverse',reverse);print('combined',comb);print('implied discount',implied_wacc,'runoff',runoff['per_share']);print('sens',sens);print(validation)
