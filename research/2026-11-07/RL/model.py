import json, pathlib, math, hashlib
P=pathlib.Path(__file__).parent
annual={'FY24':{'revenue':6631.4,'ebit':756.4,'net_income':646.3,'cfo':1069.7,'capex':164.8,'da':229,'sbc':99.5},'FY25':{'revenue':7079,'ebit':932.1,'net_income':742.9,'cfo':1235.1,'capex':216.2,'da':219.6,'sbc':107.9},'FY26':{'revenue':8114.5,'ebit':1179.2,'net_income':941.1,'cfo':1154.2,'capex':408.1,'da':233,'sbc':111}}
h1prior={'revenue':3238.2,'ebit':387.4,'net_income':316.5,'cfo':374.5,'capex':75.1,'da':110.3,'sbc':60}
h1old={'revenue':3729.8,'ebit':519.3,'net_income':427.9,'cfo':229.3,'capex':281.1,'da':112.5,'sbc':61.8}
h1new={'revenue':4153.1,'ebit':706.1,'net_income':558.8,'cfo':618.2,'capex':114.2,'da':119.3,'sbc':64.3}
ttm={k:annual['FY26'][k]-h1old[k]+h1new[k] for k in h1old}
prior={k:annual['FY25'][k]-h1prior[k]+h1old[k] for k in h1old}
for x in list(annual.values())+[ttm,prior]:x['fcf_cfo_less_capex']=round(x['cfo']-x['capex'],3)
quarter=[{'period':'Q3FY26','revenue':2406,'ebit':471.3,'net_income':361.6,'cfo':1008.9-229.3,'capex':356.7-281.1}, {'period':'Q4FY26','revenue':1978.7,'ebit':188.6,'net_income':151.6,'cfo':1154.2-1008.9,'capex':408.1-356.7}, {'period':'Q1FY27','revenue':1959.8,'ebit':342.4,'net_income':262.2,'cfo':339.3,'capex':53.4}, {'period':'Q2FY27','revenue':2193.3,'ebit':363.7,'net_income':296.6,'cfo':618.2-339.3,'capex':114.2-53.4}]
# Analyst FCFF scenarios, subject to independent audit. All projected cash-flow drivers are analyst assumptions, not guidance.
# Operating leases stay in EBIT/cash expenses, not debt. Finance leases deducted once as debt.
# Cash reserve is explicit sensitivity, not verified excess cash.
bridge={'cash_and_st_investments':1821.8,'operating_cash_reserve_assumption':600,'senior_debt_face':1250,'finance_lease_debt':222.6,'diluted_shares_assumption':60.9}
netbridge=1821.8-600-1250-222.6
cases={'adverse':{'growth':[.02,.02,.03,.03,.03,.028,.026,.024,.022,.02],'margin_end':.145,'wacc':.113,'g':.02,'roic':.12,'capex':.046},'central':{'growth':[.07,.06,.05,.05,.04,.037,.034,.031,.028,.025],'margin_end':.175,'wacc':.103,'g':.025,'roic':.15,'capex':.041},'favorable':{'growth':[.10,.09,.08,.07,.06,.054,.048,.042,.036,.03],'margin_end':.20,'wacc':.093,'g':.03,'roic':.20,'capex':.041}}
def value(c,scale=1,w=None,g=None):
 w=c['wacc'] if w is None else w;g=c['g'] if g is None else g
 r=ttm['revenue'];rows=[];pv=0
 for y,gr in enumerate(c['growth'],1):
  old=r;r*=1+gr*scale;m=.154+(c['margin_end']-.154)*min(y/5,1)
  ebit=r*m;nopat=ebit*.78;da=r*.028;dnwc=(r-old)*.10
  initial_reinvestment=r*(c['capex']-.028)+dnwc
  actual_growth=gr*scale
  growth_funded_reinvestment=nopat*actual_growth/c['roic']
  transition=max(0,(y-5)/5)
  reinvestment=initial_reinvestment*(1-transition)+growth_funded_reinvestment*transition
  capex=reinvestment+da-dnwc
  f=nopat+da-capex-dnwc;v=f/(1+w)**y;pv+=v
  rows.append(dict(year=y,revenue=r,revenue_growth=actual_growth,reinvestment=reinvestment,growth_funded_reinvestment=growth_funded_reinvestment,transition_weight=transition,margin=m,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=dnwc,fcff=f,pv=v))
 terminal_nopat=rows[-1]['nopat']*(1+g);reinvest=terminal_nopat*g/c['roic'];tf=terminal_nopat-reinvest;tv=tf/(w-g);ptv=tv/(1+w)**10;ev=pv+ptv
 return {'years':rows,'terminal_nopat':terminal_nopat,'terminal_reinvestment':reinvest,'terminal_fcff':tf,'pv_terminal':ptv,'terminal_weight':ptv/ev,'ev':ev,'equity_bridge':netbridge,'value_per_share':(ev+netbridge)/60.9}
models={k:value(v) for k,v in cases.items()}
lo,hi=0,6
for i in range(100):
 mid=(lo+hi)/2
 if value(cases['central'],mid)['value_per_share']<376.56:lo=mid
 else:hi=mid
inverse_model=value(cases['central'],(lo+hi)/2)
inverse={'target_price':376.56,'growth_multiplier':(lo+hi)/2,'first_year_growth':cases['central']['growth'][0]*(lo+hi)/2,'cagr_10yr':(value(cases['central'],(lo+hi)/2)['years'][-1]['revenue']/ttm['revenue'])**.1-1,'year10_growth':inverse_model['years'][-1]['revenue_growth'],'year10_reinvestment':inverse_model['years'][-1]['reinvestment'],'terminal_growth':cases['central']['g'],'years':inverse_model['years'],'note':'Same model, margins/reinvestment/discount fixed; not independent evidence or unique market expectation.'}
sens=[{'wacc':w,'g':g,'value':value(cases['central'],w=w,g=g)['value_per_share']} for w in [.093,.103,.113] for g in [.02,.025,.03]]
checks={}
checks['quarters_revenue_ttm']=abs(sum(q['revenue'] for q in quarter)-ttm['revenue'])<.01
checks['quarters_ebit_ttm']=abs(sum(q['ebit'] for q in quarter)-ttm['ebit'])<.01
checks['quarters_cfo_ttm']=abs(sum(q['cfo'] for q in quarter)-ttm['cfo'])<.01
checks['quarters_capex_ttm']=abs(sum(q['capex'] for q in quarter)-ttm['capex'])<.01
checks['q2_adjusted_ebit']=abs(363.7-82.3+63.2-344.6)<.001
checks['q2_adjusted_ni']=abs(296.6-19.1+5.2-282.7)<.001
checks['terminal_funded']=all(abs(z['terminal_reinvestment']-z['terminal_nopat']*cases[k]['g']/cases[k]['roic'])<.01 for k,z in models.items())
checks['wacc_above_g']=all(c['wacc']>c['g'] for c in cases.values())
checks['transition_funds_actual_growth']=all(abs(r['reinvestment']-((r['revenue']*(cases[k]['capex']-.028)+r['delta_nwc'])*(1-r['transition_weight'])+r['nopat']*r['revenue_growth']/cases[k]['roic']*r['transition_weight']))<1e-6 for k,v in models.items() for r in v['years'])
checks['inverse_year10_funds_actual_growth']=abs(inverse_model['years'][-1]['reinvestment']-inverse_model['years'][-1]['nopat']*inverse_model['years'][-1]['revenue_growth']/cases['central']['roic'])<1e-6
checks['inverse_matches_target']=abs(inverse_model['value_per_share']-376.56)<1e-6
checks['fcff_reinvestment_identity']=all(abs(r['fcff']-(r['nopat']-r['reinvestment']))<1e-6 for v in list(models.values())+[inverse_model] for r in v['years'])
assert all(checks.values()),checks
out={'status':'audited_provisional_partial','approved_for_publication':True,'publication_scope':'provisional_research_only','stage3_complete':False,'entry_approved':False,'currency':'USD','financial_units':'millions','as_of':'2026-11-07','annual':annual,'quarters':quarter,'ttm':ttm,'prior_ttm':prior,'bridge':bridge,'exploratory_assumptions':cases,'exploratory_models':models,'inverse_exploratory':inverse,'sensitivity_exploratory':sens,'qa':checks}
(P/'inputs_and_model.json').write_text(json.dumps(out,indent=2));(P/'qa.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'ttm':ttm,'prior':prior,'cases':{k:round(v['value_per_share'],2) for k,v in models.items()},'inverse':inverse,'sensitivity':sens},indent=2))
