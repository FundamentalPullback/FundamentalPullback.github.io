"""Reproducible bank-equity model. Reconstructed inputs revalidated; not original file bytes."""
from pathlib import Path
import json,csv
P=Path(__file__).parent
price=85.76; bv=52.91
fields=['period','revenue','nii','expense','provision','net_income','common_income','eps','cfo','sbc','roe','rotce','cet1']
raw=[['FY2023',82597,52375,55562,5399,19142,17982,4.83,40358,1122,11.,13.1,11.43],['FY2024',82296,47676,54598,4334,19722,18606,5.37,3035,1281,11.4,13.4,11.07],['FY2025',83699,47484,54842,3658,21338,20285,6.26,-19001,1476,12.4,14.6,10.61],['Q4 2025',21292,12331,13726,1040,5361,5114,1.62,4121,238,12.3,14.5,10.61],['Q1 2026',21446,12096,14330,1135,5253,5000,1.60,9143,715,12.2,14.5,10.3],['Q2 2026',22622,12317,13661,914,6407,6160,2.,15918-9143,318,15.,17.7,10.3],['Q3 2026',21870,12517,13743,1029,5951,5703,1.87,24785-15918,270,13.8,16.3,10.03]]
rows=[dict(zip(fields,r)) for r in raw];annual=rows[:3];qs=rows[3:]
keys=['revenue','nii','expense','provision','net_income','common_income','eps','cfo','sbc']
current={k:sum(q[k] for q in qs) for k in keys}
prior=dict(revenue=20378+62407,nii=11836+35153,expense=13900+41116,provision=1095+2618,net_income=5079+15977,common_income=4801+15171,eps=None,cfo=3035-(-5869)+(-23122),sbc=1281-1066+1238)
# Estimated TTM EPS from common income / day-weighted quarterly diluted shares, not sums of EPS.
current['eps']=current['common_income']/sum(x*d for x,d in zip([3159.0,3117.7,3074.6,3051.5],[92,90,91,92]))*365
prior['eps']=prior['common_income']/sum(x*d for x,d in zip([3360.7,3321.6,3267.0,3223.5],[92,90,91,92]))*365
current['period']='TTM Sep2026';prior['period']='TTM Sep2025'
rows += [prior,current]
for x in rows:
 x['ptpp']=x['revenue']-x['expense'];x['efficiency_ratio']=100*x['expense']/x['revenue'];x['net_margin']=100*x['net_income']/x['revenue']
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields+['ptpp','efficiency_ratio','net_margin']);w.writeheader();w.writerows(rows)
scenarios={'adverse':dict(ke=.13,g=.02,returns=[.08,.09,.10,.105,.11,.11,.11,.11,.11,.11],growth=[.01]*5+[.02]*5,terminal_roe=.11),'base':dict(ke=.115,g=.03,returns=[.13,.1325,.135,.1375,.14,.138,.136,.134,.132,.13],growth=[.04]*5+[.038,.036,.034,.032,.03],terminal_roe=.13),'favorable':dict(ke=.10,g=.035,returns=[.15,.155,.16,.165,.17,.166,.162,.158,.154,.15],growth=[.05]*5+[.047,.044,.041,.038,.035],terminal_roe=.15)}
def value(s,b=bv):
 start=b;pv=0;ri=0;out=[]
 for t,(r,g) in enumerate(zip(s['returns'],s['growth']),1):
  earn=b*r;ret=b*g;div=earn-ret;res=earn-s['ke']*b;end=b+ret;df=(1+s['ke'])**t
  out.append(dict(year=t,beginning_book=b,return_on_beginning_equity=r,book_growth=g,earnings=earn,retention=ret,potential_payout=div,ending_book=end,pv_payout=div/df,residual_income=res));pv+=div/df;ri+=res/df;b=end
 terminal=b*(s['terminal_roe']-s['g'])/(s['ke']-s['g']);tvr=b*(s['terminal_roe']-s['ke'])/(s['ke']-s['g']);pvterminal=terminal/(1+s['ke'])**10
 result=dict(value=pv+pvterminal,distribution_pv=pv,pv_terminal=pvterminal,terminal_weight=pvterminal/(pv+pvterminal),residual_income_value=start+ri+tvr/(1+s['ke'])**10,margin_of_safety=(pv+pvterminal-price)/(pv+pvterminal),assumptions=s,years=out)
 assert abs(result['value']-result['residual_income_value'])<1e-8
 return result
models={k:value(v) for k,v in scenarios.items()};sens=[]
for ke in [.105,.115,.125]:
 for terminal_roe in [.12,.13,.14]:
  s=dict(scenarios['base'],ke=ke,terminal_roe=terminal_roe,returns=scenarios['base']['returns'][:5]+[.14+(terminal_roe-.14)*i/5 for i in range(1,6)])
  sens.append(dict(ke=ke,terminal_roe=terminal_roe,value=value(s)['value']))
reverse=[]
for ke in [.105,.115,.125]:
 lo=0;hi=.4
 for _ in range(100):
  mid=(lo+hi)/2;s=dict(scenarios['base'],ke=ke,returns=[mid]*10,terminal_roe=mid)
  if value(s)['value']<price:lo=mid
  else:hi=mid
 reverse.append(dict(ke=ke,required_constant_return=(lo+hi)/2))
calc=dict(price=price,price_status='scanner export Nov10 2026 19:15:33 timezone unspecified; not verified regular close',book_value=bv,tangible_book=44.46,ttm=current,prior_ttm=prior,growth={k:current[k]/prior[k]-1 for k in keys if prior[k]>0},multiples=dict(pe=price/current['eps'],pb=price/bv,ptbv=price/44.46,dividend_runrate_yield=2/price),models=models,sensitivity=sens,reverse=reverse,approved_fair_value=None,approved_max_price=None,htm_sensitivity=dict(pretax_unrecognized_loss=43228,assumed_tax=.21,per_share_aftertax_loss=43228*.79/3001.6,adjusted_bv=bv-43228*.79/3001.6,base_value_after_full_mark=value(scenarios['base'],bv-43228*.79/3001.6)['value']))
(P/'calculations.json').write_text(json.dumps(calc,indent=2))
assert abs(models['base']['value']-64.31317902196248)<1e-8
assert abs(models['adverse']['value']-40.85142238228296)<1e-8
assert abs(models['favorable']['value']-100.52619388767991)<1e-8
assert current['cfo']==28906 and prior['cfo']==-14218
assert abs(current['eps']-7.087803853085263)<1e-9
assert abs(prior['eps']-6.06477239278881)<1e-9
assert calc['approved_fair_value'] is None and calc['approved_max_price'] is None
print('PASS calculated output reconciliation, payout/residual-income tieout, TTM aggregation, null approval fields')
print(json.dumps({k:v for k,v in calc.items() if k!='models'},indent=2));print({k:v['value'] for k,v in models.items()})
