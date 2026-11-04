import copy,json,math
from pathlib import Path
from model import I,SC,value
P=Path(__file__).parent;b=value(SC['base']);rows=[]
def put(label,inp=None,sc=None):
 r=value(sc or SC['base'],inp or I);rows.append({'case':label,'partial_value_usd':r['partial_value_per_fmx_ads_usd'],'hybrid_kof_mark_usd':r['hybrid_kof_market_mark_usd_per_fmx_ads']})
for amt in [0,10000,20000,30899.215,50000]:
 j=copy.deepcopy(I);j['capital']['imperial_brady_value_in_main']=amt;put(f'Unpriced investments illustrative MXNm {amt}; not independently verified FV',j)
for reserve in [0,4873.208,7000]:
 j=copy.deepcopy(I);j['capital']['spin_customer_reserve']=reserve;put(f'Spin mapping reserve MXNm {reserve}',j)
for csh in [5000,15000,25000]:
 j=copy.deepcopy(I);j['capital']['operating_cash_reserve']=csh;put(f'ExKOF operating cash reserve MXNm {csh}',j)
for reserve in [0,10000,20000]:
 j=copy.deepcopy(I);j['capital']['kof_operating_cash_reserve']=reserve;put(f'KOF operating cash reserve MXNm {reserve}',j)
for nci in [9255.132,15000,25000]:
 j=copy.deepcopy(I);j['capital']['kof_nci_reserve']=nci;put(f'KOF subsidiary NCI reserve MXNm {nci}',j)
for nci in [0,1000,3000]:
 j=copy.deepcopy(I);j['capital']['ex_kof_nci_reserve']=nci;put(f'ExKOF minority reserve MXNm {nci}',j)
for claim in [0,2618.794,6391.794]:
 j=copy.deepcopy(I);j['capital']['other_claims_reserve']=claim;put(f'ExKOF long-term tax plus possible claims reserve MXNm {claim}',j)
for residual in [-10000,0,10000]:
 j=copy.deepcopy(I);j['capital']['unknown_post_september_net_capital_change']=residual;put(f'Unobserved post-September net capital change MXNm {residual}',j)
for bottle in [0,2057.005,4000]:
 j=copy.deepcopy(I);delta=I['anchors']['ex_kof']['bottle_adjustment_estimated']-bottle;j['anchors']['ex_kof']['economic_ebit_after_rent_estimated']+=delta;s=copy.deepcopy(SC['base']);s['ex_kof']['margin']=[x+delta/j['anchors']['ex_kof']['revenue'] for x in s['ex_kof']['margin']];put(f'TTM KOF bottle adjustment MXNm {bottle}; margins shifted consistently',j,s)
for tax in [.30,.33,.36]:
 s=copy.deepcopy(SC['base']);s['ex_kof']['tax']=tax;put(f'ExKOF normalized economic tax {tax}',sc=s)
for capex in [.0297,.032,.038]:
 s=copy.deepcopy(SC['base']);s['ex_kof']['capex_ratio']=capex;put(f'ExKOF gross physical capex floor {capex}',sc=s)
for roic in [.12,.18,.25]:
 s=copy.deepcopy(SC['base']);s['ex_kof']['roic']=roic;put(f'ExKOF marginal ROIC {roic}',sc=s)
for fx in [17,18.59701225512121,21]:
 j=copy.deepcopy(I);j['fx']=fx;put(f'Valuation spot MXN per USD {fx}; cash flows unchanged',j)
for insurance in [2332,2462,2592]:
 j=copy.deepcopy(I);delta=I['anchors']['kof']['insurance_gain_adjustment_estimated']-insurance;j['anchors']['kof']['economic_ebit_after_rent_estimated']+=delta;s=copy.deepcopy(SC['base']);s['kof']['margin']=[x+delta/j['anchors']['kof']['revenue'] for x in s['kof']['margin']];put(f'KOF insurance proxy MXNm {insurance}',j,s)
for rent_delta in [-100,100]:
 j=copy.deepcopy(I);s=copy.deepcopy(SC['base'])
 # Additional KOF rent means less exKOF rent; total group rent unchanged.
 for seg,sign in [('kof',-1),('ex_kof',1)]:
  delta=sign*rent_delta;j['anchors'][seg]['economic_ebit_after_rent_estimated']+=delta;s[seg]['margin']=[x+delta/j['anchors'][seg]['revenue'] for x in s[seg]['margin']]
 put(f'KOF cash rent allocation delta MXNm {rent_delta}',j,s)
for ratio in [.022,.024229435,.027]:
 j=copy.deepcopy(I);s=copy.deepcopy(SC['base']);a=j['anchors']['ex_kof'];delta=a['revenue']*(a['physical_da_ratio']-ratio);a['physical_da_ratio']=ratio;a['economic_ebit_after_rent_estimated']+=delta;s['ex_kof']['margin']=[x+delta/a['revenue'] for x in s['ex_kof']['margin']];put(f'ExKOF physical DA ratio {ratio}; EBIT and addback consistent',j,s)
# Additional unclassified long-term cash investment, charged conservatively to exKOF capex floor.
s=copy.deepcopy(SC['base']);s['ex_kof']['capex_ratio']+=733.769/I['anchors']['ex_kof']['revenue'];put('All consolidated other long-term cash investment charged to exKOF floor, proxy',sc=s)
# Pure stub omission with discount dates unchanged, separate from a shortened annual convention.
stub=(b['ex_kof']['stub_pv']+b['kof']['stub_pv']*I['kof_fraction'])/(I['fx']*I['ads_m'])
rows.append({'case':'Omit estimated 58-day stub, same discount dates','partial_value_usd':b['partial_value_per_fmx_ads_usd']-stub,'hybrid_kof_mark_usd':b['hybrid_kof_market_mark_usd_per_fmx_ads']-b['ex_kof']['stub_pv']/(I['fx']*I['ads_m'])})
# Bottler renewal dependence: mechanical cash-flow haircut, no invented country probability.
for haircut in [.20,.50]:
 pv_at_risk=sum(x['pv_fcff'] for x in b['kof']['rows'] if x['year']>=2028)+b['kof']['pv_terminal'];loss=pv_at_risk*haircut*I['kof_fraction']/(I['fx']*I['ads_m']);rows.append({'case':f'KOF renewal stress: cash flow haircut {haircut} from2028 incl terminal; no salvage or restructuring benefit','partial_value_usd':b['partial_value_per_fmx_ads_usd']-loss,'hybrid_kof_mark_usd':None})
rows.append({'case':'KOF zero terminal after2036; ten-year cash flows unchanged, not a legal expiry forecast','partial_value_usd':b['partial_value_per_fmx_ads_usd']-b['kof']['pv_terminal']*I['kof_fraction']/(I['fx']*I['ads_m']),'hybrid_kof_mark_usd':None})
grid=[]
for shift in [-.02,-.01,0,.01,.02]:
 for g in [.035,.045,.055]:
  s=copy.deepcopy(SC['base'])
  for seg in s:s[seg]['wacc_usd']+=shift;s[seg]['g']=g
  z=value(s);grid.append({'usd_wacc_parallel_shift':shift,'terminal_mxn_growth':g,'partial_value_usd':z['partial_value_per_fmx_ads_usd']})
def solve(fn,target,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
# Reverse retail margins with KOF at the observed market price, avoiding need to accept our KOF DCF.
def margin_value(delta):
 s=copy.deepcopy(SC['base']);s['ex_kof']['margin']=[m+delta for m in s['ex_kof']['margin']];return value(s)['hybrid_kof_market_mark_usd_per_fmx_ads']
d=solve(margin_value,I['price'],0,.30)
den=I['ads_m']*I['fx'];reverse={'price':I['price'],'ex_kof_parallel_margin_uplift_required_with_kof_at_market':d,'required_year1_margin':SC['base']['ex_kof']['margin'][0]+d,'required_terminal_margin':SC['base']['ex_kof']['margin'][-1]+d,'reproduced_price':margin_value(d),'unpriced_asset_value_required_mxnm_own_kof_dcf':(I['price']-b['partial_value_per_fmx_ads_usd'])*den,'unpriced_asset_value_required_mxnm_kof_market_mark':(I['price']-b['hybrid_kof_market_mark_usd_per_fmx_ads'])*den,'warning':'Inverse calculations are conditions, not forecasts or verified investment values; tax/realization costs ignored for the unpriced-asset residual.'}
# Exact currency equivalence: MXN FCFF at FX-drift-adjusted discount = annually translated USD cashflows at USD discount.
currency_checks=[]
for seg in ['ex_kof','kof']:
 for row in b[seg]['rows']:
  t=row['discount_years'];usd=row['fcff']/(I['fx']*(1+I['rates']['annual_mxn_depreciation_assumed'])**t)/(1+SC['base'][seg]['wacc_usd'])**t;expected=row['pv_fcff']/I['fx'];currency_checks.append({'segment':seg,'year':row['year'],'usd_pv':usd,'mxn_pv_converted':expected,'pass':math.isclose(usd,expected,rel_tol=1e-12)})
(P/'sensitivities.json').write_text(json.dumps({'one_way':rows,'wacc_growth_grid':grid,'inverse':reverse,'currency_equivalence_checks':currency_checks},indent=2)+'\n');print(reverse)
