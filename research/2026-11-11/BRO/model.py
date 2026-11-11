"""Incremental BRO research model. USD millions. No network, no approved value.
Run python model.py. Assumptions deliberately conditional; see report.md.
"""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
OLD=json.loads((P/'sources/results.json').read_text())
C=OLD['assumptions']; B=OLD['bridge']; CORE=6458.; TAX=.25; PRICE=71.89
W=OLD['capital_cost']['wacc'] # unchanged risk rate for like-for-like economic test ONLY
CONTRACT_NET=28.; FEES=6814.
def value(case='central',w=W,replacement=0.,shift=0.,cash=0.,shares=B['shares'],g_override=None,contract_net=CONTRACT_NET):
 c=C[case];g=c['g'] if g_override is None else g_override
 assert w>g
 core=CORE;rows=[]
 for y in range(1,11):
  f=max(0,(y-5)/5);org=(c['organic'][min(y,5)-1]+shift)*(1-f)+g*f
  acq=c['acq']*(1-f);margin=c['margin'][min(y,5)-1]*(1-f)+c['terminal_margin']*f
  prev=core;new_acquired_runrate=prev*acq;core=prev*(1+org)+new_acquired_runrate
  recognized_core=core-.5*new_acquired_runrate # midyear acquisition recognition, no full year free
  cont=recognized_core*c['contingent_share']/(1-c['contingent_share']);rev=recognized_core+cont
  # Acquisition amortization excluded, SBC and ordinary producer/integration expense retained.
  # replacement is ONLY incremental deductible expense beyond costs already in margin.
  incremental_replacement=rev*replacement
  ebita=recognized_core*margin+cont*c['contingent_margin']-incremental_replacement;nopat=ebita*(1-TAX)
  contract=contract_net*rev/FEES # proxy for net cash reinvestment, NOT proven cash from disclosure
  base_netcapex=.005*rev;base_wc=.15*max(0,prev*org) # explicitly excludes contract-cost assets
  acquisition=prev*acq*c['acq_price'] # full enterprise consideration, no free bought growth
  stable=nopat*g/c['roic'];stable_residual=max(0,stable-contract)
  # contract costs explicitly allocated WITHIN terminal total growth reinvestment, not twice.
  netcapex=(1-f)*base_netcapex+f*.8*stable_residual
  wc=(1-f)*base_wc+f*.2*stable_residual
  dep=.01*rev;capex=dep+netcapex
  fcff=nopat+dep-capex-wc-contract-acquisition
  rows.append(dict(year=y,organic=org,acquired_growth=acq,core_runrate=core,core=recognized_core,contingents=cont,revenue=rev,core_margin=margin,incremental_replacement=incremental_replacement,ebita=ebita,cash_tax_proxy=ebita*TAX,nopat=nopat,dep=dep,capex=capex,other_wc=wc,contract_reinvestment=contract,acquisition_reinvestment=acquisition,fcff=fcff,pv=(fcff+acquisition)/(1+w)**y-acquisition/(1+w)**(y-.5)))
 last=rows[-1];n11=last['nopat']*(1+g);contract11=last['contract_reinvestment']*(1+g);ri11=max(n11*g/c['roic'],contract11)
 terminal_fcff=n11-ri11;pvtv=terminal_fcff/(w-g)/(1+w)**10;ev=sum(r['pv'] for r in rows)+pvtv
 equity=ev-B['debt_face']-B['earnouts']-B['nci']+cash
 return dict(price=equity/shares,wacc=w,ev=ev,equity=equity,terminal_share=pvtv/ev,terminal_fcff=terminal_fcff,terminal_reinvestment=ri11,rows=rows)
def solve(fn,lo,hi,target=PRICE,increasing=True):
 a,b=fn(lo),fn(hi)
 if not min(a,b)<=target<=max(a,b):return None
 for _ in range(100):
  m=(lo+hi)/2
  if (fn(m)<target)==increasing:lo=m
  else:hi=m
 return (lo+hi)/2
cases={k:value(k) for k in C}
result={'as_of':'2026-11-11','status':'conditional research; not decision ready','canonical_intrinsic_value':None,'maximum_buy_price':None,'approved_purchase':False,'scanner_price':PRICE,'price_is_certified_regular_close':False,'unchanged_reference_wacc':W,'cases':cases,
'reverse':{'organic_shift_zero_incremental_replacement':solve(lambda x:value(shift=x)['price'],-.08,.15),'incremental_replacement_revenue_fraction_at_price':solve(lambda x:value(replacement=x)['price'],0,.1,increasing=False),'break_even_wacc':solve(lambda x:value(w=x)['price'],.04,.12,increasing=False)},
'sensitivity':[dict(wacc=w,replacement=repl,price=value(w=w,replacement=repl)['price']) for w in [W,W+.005,W+.01] for repl in [0,.005,.01,.02]],
'capital_diagnostics':{'september_market_debt_estimate':6520+772,'old_estimate':6520+726,'difference':46,'nominal_debt':7822,'total_debt_carrying':7759,'all_reported_cash_surplus_value':value(cash=1099)['price'],'extra_escrow_shares_value':value(shares=B['shares']+4.4)['price']},
'first_year_liquidity_diagnostic':{k:{'fcff':v['rows'][0]['fcff'],'less_interest_without_tax_shield':374,'less_principal':413,'less_contingent_contractual_amount':208,'less_other_liabilities':35,'less_declared_dividend_only':60,'residual_before_other_distributions':v['rows'][0]['fcff']-374-413-208-35-60} for k,v in cases.items()},
'assumptions':{'replacement_default':0,'replacement_default_means':'conditional existing expense is sufficient, NOT proven zero economic replacement','contract_cash_proxy':28,'contract_cash_proxy_means':'A524 TTM net deferred acquisition25 + fulfillment3; payables movement unresolved','tax':TAX,'tax_shields_included':False,'acquisition_timing':'midyear purchase price and half first-year acquired revenue; full runrate retained for following year', 'terminal_contract_costs':'allocated inside g/ROIC budget','SBC':'not added back; current unvested dilution unresolved; no recurring future dilution on top of retained expense'},'inherited_assumptions':C}
result['checks']={'ten_years':all(len(v['rows'])==10 for v in cases.values()),'fcff_identity':all(abs(r['fcff']-(r['nopat']+r['dep']-r['capex']-r['other_wc']-r['contract_reinvestment']-r['acquisition_reinvestment']))<1e-8 for v in cases.values() for r in v['rows']),'monotonic_cases':cases['adverso']['price']<cases['central']['price']<cases['favorable']['price'],'terminal_smooth':all(abs(v['terminal_fcff']-v['rows'][-1]['fcff']*(1+C[k]['g']))<1e-8 for k,v in cases.items()),'canonical_null':result['canonical_intrinsic_value'] is None}
(P/'results.json').write_text(json.dumps(result,indent=2))
for k,v in cases.items():
 with (P/f'forecast_{k}.csv').open('w') as f:
  out=csv.DictWriter(f,fieldnames=list(v['rows'][0]));out.writeheader();out.writerows(v['rows'])
print(json.dumps({k:v for k,v in result.items() if k in ['reverse','sensitivity','checks','first_year_liquidity_diagnostic']},indent=2));print({k:round(v['price'],2) for k,v in cases.items()})
