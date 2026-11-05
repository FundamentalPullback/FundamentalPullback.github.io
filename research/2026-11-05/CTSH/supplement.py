from value import *
from pathlib import Path
import json,csv,hashlib
s=json.loads((P/'sensitivity.json').read_text())
moderate=dict(organic_growth=.02,margins=[m-.005 for m in I['cases']['base']['margins']],terminal_margin=.155,acquisition_multiple=3.5,tax=.27,capex_pct=.018)
beta1w=(I['risk_free']+I['erp'])*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw
s['combined_risk_tests']={f'{label}':value(overrides={**moderate,**over})['per_share']for label,over in {
 'moderate_wacc9':{'wacc':.09},'moderate_beta1':{'wacc':beta1w},'moderate_beta1_plus5DSO':{'wacc':beta1w,'dso_cash_stress_2027':308},'moderate_same_month_Rf5_29':{'wacc':(.0529+beta*I['erp'])*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw}}.items()}
s['additional_checks']={'without_economic_Q4_stub':value()['per_share']-value()['pv_stub']/value()['shares'],'cash_conversion_FCFF_2027_before_new_MA':value()['rows'][0]['fcff']+value()['rows'][0]['acquisition_cash'],'historical_cash_enterprise_proxy_TTM':2143.36,'beta1_wacc':beta1w,'ERP_month_Rf_sensitivity_wacc':(.0529+beta*I['erp'])*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw}
# Conservative persistent cash-conversion drag, as a sensitivity not presumed perpetual DSO growth.
z=value();pvdrag=sum((300 if r['t']<=5 else 300*(10-r['t'])/5)/(1+z['wacc'])**r['discount_time']for r in z['rows'])
s['additional_checks']['extra_cash_drag_300_per_year_first5_then_fade_value']=z['per_share']-pvdrag/z['shares']
def legacy(w):
 R=22095;pv=0
 for t in range(1,11):
  prev=R;g=[.045,.045,.04,.035,.03][t-1]if t<=5 else .03+(.025-.03)*(t-5)/5;m=[.154,.157,.16,.16,.16][t-1]if t<=5 else .16;R*=1+g;nopat=R*m*.75;reinv=R*(.055-.026)+(R-prev)*.15
  if t>5:f=(t-5)/5;reinv=(1-f)*reinv+f*nopat*.025/.15
  pv+=(nopat-reinv)/(1+w)**t
 return pv+R*1.025*.16*.75*(1-.025/.15)/(w-.025)/(1+w)**10
old=(legacy(.10)-500)/450;rate=(legacy(wacc)-500)/450;new_ev_no_stub=z['enterprise_value']-z['pv_stub'];changed_ops=(new_ev_no_stub-500)/450;stub=(z['enterprise_value']-500)/450
s['migration_bridge']=[{'step':'Approximate A120 narrative reconstruction','value':old},{'step':'Same old operating assumptions, only WACC8.51757%','value':rate},{'step':'New growth/cohorts/tax/reinvestment/terminal and timed acquisition cash, no Q4stub; old capital/share bridge','value':changed_ops},{'step':'Add estimated economic Q4stub','value':stub},{'step':'New pension/earnout/capital-return reserve and current diluted denominator','value':z['per_share']}]
for n in range(1,len(s['migration_bridge'])):s['migration_bridge'][n]['change']=s['migration_bridge'][n]['value']-s['migration_bridge'][n-1]['value']
(P/'sensitivity.json').write_text(json.dumps(s,indent=2))
print(json.dumps({k:s[k]for k in ['combined_risk_tests','additional_checks','migration_bridge']},indent=2))
