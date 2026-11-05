"""Offline frozen-input attribution, NOT a refreshed current fair value."""
from pathlib import Path
import json,itertools
P=Path(__file__).resolve().parent.parent
D=json.loads((P/'inputs/legacy_full_model.json').read_text())
E=json.loads((P/'inputs/event_inputs.json').read_text())
S,FX=D['shares'],D['fx']

def op(p,fade=True,capex_interpretation=None,margin_end=None,margin_year=5):
 sales=p['revenue'];rows=[]
 for k in range(1,11):
  growth=p['growth'] if k<=5 else p['growth']+(p['growth10']-p['growth'])*(k-5)/5
  prior=sales;sales*=1+growth
  target=p['margin5'] if margin_end is None else margin_end
  margin=p['margin0']+(target-p['margin0'])*min(k,margin_year)/margin_year
  nopat=sales*(margin-p['restruct'])*(1-p['tax'])+p.get('synergy',0)*min(k/3,1)*(1-p['tax'])
  capex,lease=p['capex'],p['lease_capex']
  # Mechanical first-three-MODEL-period sensitivity; not a calendar-perfect2027-29 forecast.
  if k<=3 and capex_interpretation:
   capex=E['capex_2027_2029'];lease=p['lease_capex'] if capex_interpretation=='excludes_leases' else 0
  reinv=sales*(capex+lease-p['da'])+(sales-prior)*p['nwc']
  terminal_required=nopat*growth/p['terminal_roic'];weight=(k-5)/5 if fade and k>5 else 0
  applied=reinv*(1-weight)+terminal_required*weight
  extra=p.get('extra_costs',{}).get(str(k),0)
  cash=nopat-applied-extra
  rows.append(dict(model_year=k,legacy_label_year=2026+k,revenue=sales,margin=margin,capex_rate=capex,lease_rate=lease,nopat=nopat,applied_net_reinvestment=applied,fcff=cash,pv=cash/(1+p['wacc'])**k))
 terminal=rows[-1]['nopat']*(1+p['tg'])*(1-p['tg']/p['terminal_roic'])/(p['wacc']-p['tg'])
 ev=sum(x['pv'] for x in rows)+terminal/(1+p['wacc'])**10
 return dict(ev=ev,rows=rows,terminal_value=terminal)

def direct(fade):
 p=D['direct']['base']['inputs'];r=op(p,fade)
 return (r['ev']-D['operating_claims']+D['nonoperating_assets'])/S*FX

def deal(fade=True,cost=4,capex=None,margin=None,margin_year=5):
 h=D['deal']['hpc']['inputs'];f=D['deal']['foods']['inputs'];delay=D['deal']['inputs']['close_years']
 ho=op(h,fade,capex,margin,margin_year);fo=op(f,fade)
 pre=op(D['direct']['base']['inputs'],fade)['rows'][0]['fcff']*delay/(1+h['wacc'])**delay
 value_eur=pre+ho['ev']/(1+h['wacc'])**delay+15.7/FX/(1+h['wacc'])**delay+.65*(fo['ev']-4.6871-15.7-.75)/FX/(1+f['wacc'])**delay-D['operating_claims']+D['nonoperating_assets']-cost/(1+h['wacc'])**delay
 return dict(mechanical_package_per_adr_usd=value_eur/S*FX,hpc=ho,foods=fo)

legacy={'direct_original':direct(False),'direct_fade':direct(True),'deal_original':deal(False)['mechanical_package_per_adr_usd'],'deal_fade':deal(True)['mechanical_package_per_adr_usd']}
checks=[dict(name='legacy deal reproduction',passed=abs(legacy['deal_original']-D['deal']['adr'])<1e-9),dict(name='legacy direct reproduction',passed=abs(legacy['direct_original']-D['direct']['base']['adr'])<1e-9)]
cases=[]
for cost,cap in itertools.product([4,5],[None,'excludes_leases','includes_leases']):
 r=deal(cost=cost,capex=cap)
 cases.append(dict(cost_reserve_eur_bn=cost,capex_interpretation=cap or 'legacy_unchanged',mechanical_package_per_adr_usd=r['mechanical_package_per_adr_usd'],delta_vs_frozen_fade=r['mechanical_package_per_adr_usd']-legacy['deal_fade']))
margin_cases=[]
for endpoint,year in itertools.product([.22,.225,.23],[5,10]):
 r=deal(cost=5,capex='excludes_leases',margin=endpoint,margin_year=year)
 margin_cases.append(dict(analyst_margin_endpoint=endpoint,model_year_reached=year,mechanical_package_per_adr_usd=r['mechanical_package_per_adr_usd']))
a,b=.15,.30
for _ in range(100):
 mid=(a+b)/2
 if deal(cost=5,capex='excludes_leases',margin=mid,margin_year=10)['mechanical_package_per_adr_usd']<E['price']:a=mid
 else:b=mid
reverse={'analyst_margin_endpoint_year10':(a+b)/2,'price':E['price'],'held_fixed':'5% initial revenue growth,7.5% HPC WACC,19% terminal ROIC,2.5% terminal growth; €5bn aggregate reserve;3.6% capex plus0.8% leases for first3 model periods; all other legacy inputs frozen','meaning':'Conditional reverse diagnostic, not a uniquely market-implied margin or management forecast.'}
annual=[]
sales=D['deal']['hpc']['inputs']['revenue']
for year in range(2027,2030):
 sales*=1+D['deal']['hpc']['inputs']['growth']
 annual.append(dict(calendar_label=year,illustrative_sales=sales,capex_at_legacy_3p2=sales*.032,capex_at_event_3p6=sales*.036,increment_if_comparable=sales*.004,legacy_recurring_restructuring=sales*.006))
checks.extend([dict(name='positive marginal cost reduces value',passed=cases[3]['mechanical_package_per_adr_usd']<cases[0]['mechanical_package_per_adr_usd']),dict(name='includes vs excludes lease bracket',passed=cases[5]['mechanical_package_per_adr_usd']>cases[3]['mechanical_package_per_adr_usd']>cases[4]['mechanical_package_per_adr_usd'])])
R={'scope':'Frozen-legacy attribution only; every mechanical package value is NOT current fair value, target or entry. Inputs date before event; no complete postevent capital/calendar reconciliation.','units':'EURbn except FoodsUSD, sharesbn and ADRUSD','fixed_fx':FX,'shares':S,'legacy':legacy,'cash_cost_capex_sensitivities':cases,'margin_sensitivities':margin_cases,'reverse_margin_diagnostic':reverse,'three_year_cash_illustration':annual,'price_change':{'prior_close':D['quote'],'new_close':E['price'],'return':E['price']/D['quote']-1},'checks':checks,'limitations':['First three post-close model periods are a timing proxy, not literal2027-29 calendar periods. Old0.67-year stub and postclose discounting retained solely for like-for-like attribution.','Capex reverts to old3.2% plus0.8% leases after3 periods; no management post2029 guidance inferred.','Aggregate€5bn reserve may overlap recurring restructuring and old€0.12/0.06bn stranded costs retained here. No€1.2bn or€0.5-0.6bn additional charge made.','No future acquisitions or acquired growth added; not management all-in cash allocation.','Current shares, FX, pension, NCI, nonoperating assets and MKC carveout have not been fully rebuilt.','Annual ongoing restructuring .6% is an analytical baseline, not event forecast.']}
(P/'model/results.json').write_text(json.dumps(R,indent=2,sort_keys=True)+'\n')
(P/'model/qa.json').write_text(json.dumps({'passed':all(x['passed']for x in checks),'checks':checks},indent=2,sort_keys=True)+'\n')
assert all(x['passed'] for x in checks)
print(json.dumps({'legacy':legacy,'cases':cases,'margin':margin_cases,'reverse':reverse,'checks':checks},indent=2))
