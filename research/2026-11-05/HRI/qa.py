import json, math, hashlib, csv
from pathlib import Path
from model import run,I
P=Path(__file__).parent
R=json.loads((P/'results.json').read_text());checks=[]
def check(name,condition):
 checks.append({'check':name,'pass':bool(condition)})
for k,v in R.items():
 if k=='reverse':continue
 c=v['assumptions'];rows=v['rows']
 check(k+' 10 annual periods',len(rows)==10)
 check(k+' WACC exceeds terminal growth',c['wacc']>c['terminal_g'])
 check(k+' positive terminal reinvestment below NOPAT',0<c['terminal_g']/c['terminal_roic']<1)
 check(k+' PV ties EV',abs(v['enterprise_value']-sum(x['pv_fcff'] for x in rows)-v['pv_terminal'])<1e-8)
 check(k+' enterprise equity bridge ties',abs(v['equity_raw']-(v['enterprise_value']-v['bridge']))<1e-8)
 check(k+' claims paid once and cash buffer bounded',0<=c['operating_cash_buffer']<=I['cash'])
 check(k+' equity limited to zero',v['value_per_share']>=0)
 for z in rows:
  check(k+f" year{z['year']} FCFF identity",abs(z['fcff']-(z['economic_ebit']*(1-z['unlevered_cash_tax_rate'])-z['modeled_growth_reinvestment']))<1e-8)
  check(k+f" year{z['year']} net maintenance bridge",abs(z['economic_da']-z['fleet_gross_replacement']+z['fleet_disposal_proceeds']-z['other_net_maintenance'])<1e-8)
  check(k+f" year{z['year']} capex remains positive",z['economic_da']+z['modeled_growth_reinvestment']-z['delta_nwc']>0)
 check(k+' five year explicit fade',rows[4]['terminal_transition_weight']==0 and rows[-1]['terminal_transition_weight']==1)
rev=R['reverse'];check('reverse WACC ties price',abs(run('base',{'wacc':rev['base_break_even_wacc']})['value_per_share']-I['price'])<1e-6)
check('reverse holding life ties price',abs(run('base',{'holding_life':rev['base_break_even_holding_life']})['value_per_share']-I['price'])<1e-6)
check('reverse margin ties price',abs(rev['uniform_margin_result']['value_per_share']-I['price'])<1e-6)
check('raising WACC lowers raw equity',run('base',{'wacc':.11})['equity_raw']<run('base',{'wacc':.09})['equity_raw'])
check('lower residual lowers raw equity',run('base',{'residual_fraction':.30})['equity_raw']<run('base',{'residual_fraction':.40})['equity_raw'])
check('shorter holding life lowers raw equity',run('base',{'holding_life':7})['equity_raw']<run('base',{'holding_life':9})['equity_raw'])
result={'status':'screen-grade','independent_audit':'pending; checks are builder QA only','hard_failures':sum(not x['pass'] for x in checks),'checks':checks,'warnings':['Economic depreciation is a replacement-cost analytical measure, not GAAP D&A or a certified tax basis.','Maintenance life, residual and replacement-cost premium are estimated; cohort disclosure unavailable.','WACC calibrated to approximate peer beta and last verified Treasury, not observed HRI beta or spot debt yield.','September capital bridge has estimated accrued interest, operating cash, existing dilution and historical contingent claims.','No subsequent-period capital roll-forward, technical entry or verified next earnings date.','Residual equity close to zero is a funding gap, not precise price target or insolvency forecast.','Five-year transition to 12% terminal incremental ROIC adds capital beyond fleet-only economics; alternative is supplied.','Forecasts are annual prospective normalized periods, not a completed calendar quarterly budget.']}
(P/'QA.json').write_text(json.dumps(result,indent=2));print('Checks',len(checks),'failures',result['hard_failures'])
assert not result['hard_failures']
