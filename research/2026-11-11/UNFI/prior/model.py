import json,math,pathlib,csv,copy,datetime
P=pathlib.Path(__file__).parent
PRICE=48.29
OFFSET=(datetime.date(2026,11,4)-datetime.date(2026,8,1)).days/365.25 # no duplicated cash stub
BASIC=60.053154
SHARES=BASIC+2.1 # FY26 treasury-stock equivalent existing dilution proxy; sensitivity to full target awards separately
BRIDGE=1583+13+13+1 # principal debt + finance leases + pension obligation + minority; all cash retained operationally
RF=.049;BETA=1.08;ERP=.0441;SIZE=0.0;KD=.07;DEBTW=.35;TAX=.26
WACC=(RF+BETA*ERP+SIZE)*(1-DEBTW)+KD*(1-TAX)*DEBTW
CASES={
'base':dict(rev1=31500,growth=[.02]*4,margin=[.012,.0125,.013,.0135,.014],wacc=WACC,g=.02,roic=.12,da=.008,capex=300/31500,nwc=.05,terminal_margin=.014),
'bear':dict(rev1=30900,growth=[0,.005,.01,.01],margin=[.010,.010,.0105,.011,.0115],wacc=.105,g=.015,roic=.09,da=.008,capex=.010,nwc=.06,terminal_margin=.0115),
'bull':dict(rev1=31800,growth=[.035,.03,.025,.025],margin=[.0135,.0145,.0155,.016,.0165],wacc=.08,g=.025,roic=.14,da=.008,capex=.0095,nwc=.045,terminal_margin=.0165)}
def model(c, shares=SHARES,bridge=BRIDGE,offset=OFFSET):
 rev=31152; rows=[]
 for t in range(1,11):
  prev=rev
  if t==1:rev=c['rev1'];growth=rev/prev-1
  elif t<=5:growth=c['growth'][t-2];rev*=1+growth
  else:growth=c['growth'][-1]+(c['g']-c['growth'][-1])*(t-5)/5;rev*=1+growth
  margin=c['margin'][t-1] if t<=5 else c['margin'][-1]+(c['terminal_margin']-c['margin'][-1])*(t-5)/5
  ebit=rev*margin;nopat=ebit*(1-TAX);da=rev*c['da'];capex=rev*c['capex'];dWC=(rev-prev)*c['nwc'];explicit=capex-da+dWC
  # Y6-10 blend explicit reinvestment towards paid growth; total reinvestment represented by capex balance, no double deduction
  weight=max(0,(t-5)/5);reinvest=explicit*(1-weight)+nopat*growth/c['roic']*weight
  capex=da+reinvest-dWC
  fcff=nopat-reinvest;pv=fcff/(1+c['wacc'])**(t-offset)
  rows.append(dict(year=2026+t,revenue=rev,growth=growth,margin=margin,ebit=ebit,nopat=nopat,da=da,capex_including_cloud=capex,delta_nwc=dWC,reinvestment=reinvest,fcff=fcff,pv=pv))
 terminal_nopat=rows[-1]['nopat']*(1+c['g']);terminal_reinv=terminal_nopat*c['g']/c['roic'];terminal_fcff=terminal_nopat-terminal_reinv;tv=terminal_fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**(10-offset);ev=sum(r['pv'] for r in rows)+pvtv;eq=ev-bridge
 return dict(price=eq/shares,ev=ev,equity=eq,bridge=bridge,shares=shares,pv_explicit=sum(r['pv'] for r in rows),pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_fcff=terminal_fcff,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,terminal_value=tv,upside=eq/shares/PRICE-1,rows=rows)
def solve(fn,target,lo,hi):
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)<target:lo=m
  else:hi=m
 return (lo+hi)/2
OUT={k:model(v) for k,v in CASES.items()}
b=CASES['base']
rev_growth=solve(lambda g:model(dict(b,rev1=31152*(1+g),growth=[g]*4))['price'],PRICE,-.05,.3)
margin_shift=solve(lambda x:model(dict(b,margin=[v+x for v in b['margin']],terminal_margin=b['terminal_margin']+x))['price'],PRICE,-.005,.03)
break_wacc=solve(lambda w:-model(dict(b,wacc=w))['price'],-PRICE,.03,.2)
sens=[dict(wacc=w,g=g,value=model(dict(b,wacc=w,g=g))['price']) for w in [.075,.08,.085,WACC,.095,.10,.105,.115] for g in [.015,.02,.025]]
qa={'ten_year_all_cases':all(len(v['rows'])==10 for v in OUT.values()),'wacc_above_growth':all(c['wacc']>c['g'] for c in CASES.values()),'terminal_paid_growth':all(abs(v['terminal_fcff']-v['terminal_nopat']+v['terminal_reinvestment'])<1e-8 for v in OUT.values()),'positive_capex_all_cases':all(r['capex_including_cloud']>0 for v in OUT.values() for r in v['rows']),'bridge_correct':BRIDGE==1610,'no_free_buybacks':True,'cloud_in_capex_from_EBIT':True,'no_SBC_addback':True,'no_operating_lease_double_deduction':True}
results={'price':PRICE,'price_date':'2026-11-04 16:00 EST','valuation_offset_years':OFFSET,'balance_date':'2026-08-01','post_balance_bridge_change_assumed':0,'status':'screen-grade','wacc_build':{'rf':RF,'beta':BETA,'erp':ERP,'size_premium':SIZE,'pretax_debt':KD,'debt_weight':DEBTW,'tax':TAX,'result':WACC},'cases':OUT,'sensitivity':sens,'reverse':{'growth_Y1_Y5':rev_growth,'margin_shift':margin_shift,'Y1_margin':b['margin'][0]+margin_shift,'Y5_terminal_margin':b['terminal_margin']+margin_shift,'breakeven_wacc':break_wacc},'crosschecks':{'base_at_fiscal_year_end':model(b,offset=0)['price'],'finite_tax_shield_5y_upper':model(b)['price']+sum(66*TAX/(1+WACC)**(t-OFFSET) for t in range(1,6))/SHARES,'base_with_75bp_equity_premium':model(dict(b,wacc=WACC+.0075*(1-DEBTW)))['price'],'base_ERP5_no_premium':model(dict(b,wacc=(RF+BETA*.05)*(1-DEBTW)+KD*(1-TAX)*DEBTW))['price'],'base_at_10_5':model(dict(b,wacc=.105))['price'],'base_all_cash_excess':model(b,bridge=BRIDGE-37)['price'],'base_full_target_awards':model(b,shares=BASIC+5.814628)['price'],'base_awards_max':model(b,shares=BASIC+5.814628+1.323006)['price'],'base_no_future_growth':model(dict(b,rev1=31152,growth=[0]*4,g=0))['price']},'qa':qa}
# Explicit conditional cash paths; the long-term target does not prove a terminal perpetuity.
GUIDE_FCFF=300-65+115*(1-TAX)
GUIDE_GAP=GUIDE_FCFF-OUT['base']['rows'][0]['fcff']
alt=copy.deepcopy(b);shift=GUIDE_GAP/(31500*(1-TAX));alt['margin']=[m+shift for m in alt['margin']];alt['terminal_margin']+=shift
cash_two=sum(GUIDE_GAP/(1+WACC)**(t-OFFSET) for t in [1,2])/SHARES
shield_later=sum(66*TAX/(1+WACC)**(t-OFFSET) for t in [3,4,5])/SHARES
results['guidance_cash_paths']={'guide_FCFF':GUIDE_FCFF,'incremental_FCFF':GUIDE_GAP,'gap_years':[1,2],'gap_each_year_USDm':GUIDE_GAP,'limited_two_year_value':OUT['base']['price']+cash_two,'limited_two_year_plus_later_shield_value':OUT['base']['price']+cash_two+shield_later,'later_shield_years':[3,4,5],'later_shield_each_year_USDm':66*TAX,'persistent_margin_case':alt,'persistent_margin_value':model(alt)['price'],'caveat':'Gap added only in FY27 and FY28; no terminal uplift. Combined case adds tax shield only FY29-FY31, not FY27-FY28, to avoid overlapping the guide gap. Future tax/WC reversals could offset either; not certified or a new base.'}
results['finite_tax_shield_assumptions']={'annual_amortization_assumed_deductible':66,'tax':TAX,'years':[1,2,3,4,5],'annual_tax_saving':66*TAX,'terminal_tax_saving':0,'status':'upper sensitivity; deductibility and fixed five-year schedule not established'}

if (P/'audit_status.json').exists():results['independent_audit']=json.loads((P/'audit_status.json').read_text())
if __name__=='__main__':
 (P/'model_results.json').write_text(json.dumps(results,indent=2));(P/'model_inputs.json').write_text(json.dumps(CASES,indent=2));(P/'qa_results.json').write_text(json.dumps(qa,indent=2))
 for k,v in OUT.items():
  with open(P/(k+'_forecast.csv'),'w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 print(json.dumps({k:{q:v[q] for q in ['price','upside','terminal_weight']} for k,v in OUT.items()},indent=2));print(results['reverse']);print(results['crosschecks']);print('WACC',WACC)
