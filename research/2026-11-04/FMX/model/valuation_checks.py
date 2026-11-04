import json,math
from pathlib import Path
from model import I,SC,value
P=Path(__file__).parent;checks=[]
def ck(label,cond):checks.append({'check':label,'pass':bool(cond)})
def eq(label,a,b):ck(label,math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8))
R={s:value(v) for s,v in SC.items()}
for scenario,v in R.items():
 for seg in ['ex_kof','kof']:
  z=v[seg];s=SC[scenario][seg];ck(f'{scenario}.{seg}.wacc>g',z['wacc_mxn']>s['g']);ck(f'{scenario}.{seg}.10years',len(z['rows'])==10)
  eq(f'{scenario}.{seg}.PVsum',z['enterprise_value'],sum(r['pv_fcff'] for r in z['rows'])+z['stub_pv']+z['pv_terminal'])
  for r in z['rows']:
   stem=f'{scenario}.{seg}.{r["year"]}'
   eq(stem+'.EBIT',r['ebit_after_rent'],r['revenue']*r['margin']);eq(stem+'.NOPAT',r['nopat'],r['ebit_after_rent']*(1-r['tax_rate']));eq(stem+'.FCFF',r['fcff'],r['nopat']-r['net_reinvestment_selected']);eq(stem+'.DCF',r['pv_fcff'],r['fcff']/(1+z['wacc_mxn'])**r['discount_years']);ck(stem+'.funded_growth',r['net_reinvestment_selected']+1e-8>=r['positive_delta_nopat_roic_reinvestment']);ck(stem+'.funded_floor',r['net_reinvestment_selected']+1e-8>=r['net_physical_reinvestment_floor']+r['working_capital_floor'])
  eq(f'{scenario}.{seg}.TV',z['terminal_value'],z['terminal_fcff']/(z['wacc_mxn']-s['g']));ck(f'{scenario}.{seg}.terminal_funded',z['terminal_reinvestment']>0)
 eq(scenario+'.ownership',v['femsa_owned_kof_value'],v['kof_equity_common']*I['kof_fraction']);eq(scenario+'.ADS',v['partial_value_per_fmx_ads_usd'],v['identified_equity_value']/I['fx']/I['ads_m']);ck(scenario+'.rent_lease_not_deducted_twice',abs(v['ex_kof_capital_bridge'])<50000)
ck('scenario_monotonic',R['bear']['partial_value_per_fmx_ads_usd']<R['base']['partial_value_per_fmx_ads_usd']<R['bull']['partial_value_per_fmx_ads_usd'])
eq('ADS_rights',I['ads_m'],(1968615615+1417048500*5/6)/1e7)
eq('KOFstake_exact',I['kof_fraction'],7936628152/16806658096)
sens=json.load(open(P/'sensitivities.json'))
for c in sens['currency_equivalence_checks']:ck(f'currency.{c["segment"]}.{c["year"]}',c['pass'])
eq('reverse_price',sens['inverse']['reproduced_price'],I['price'])
# Independent closed form terminal and explicit discounting via a recurrence rather than model's power expression.
for sc,v in R.items():
 for seg in ['ex_kof','kof']:
  z=v[seg];pv=0;factor=(1+z['wacc_mxn'])**(-z['stub_days']/365)
  for row in z['rows']:factor/=1+z['wacc_mxn'];pv+=row['fcff']*factor
  eq(f'independent_discount.{sc}.{seg}',pv+z['stub_pv']+z['terminal_fcff']/(z['wacc_mxn']-z['g_mxn'])*factor,z['enterprise_value'])
(P/'valuation_checks.json').write_text(json.dumps({'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks},indent=2)+'\n');print(sum(c['pass'] for c in checks),'/',len(checks));assert all(c['pass'] for c in checks)
