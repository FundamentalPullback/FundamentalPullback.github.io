"""Independent arithmetic checker; does not import or execute decision/model.py.
Base/recovery uses preserved A186 FCFF and terminal rows directly.
Reverse checks use independent explicit forecast reconstruction from inputs.
"""
import json, math
from pathlib import Path
P=Path(__file__).resolve().parent
old=json.loads((P.parent.parent/'prior/model_results.json').read_text())
new=json.loads((P.parent/'results.json').read_text())
shares=old['shares']; debt=old['debt']; equity=192.96*shares
cash=old['cash']-old['regulated_cash']-old['operating_cash']
rates={}; checks=[]
for beta,label in [(0.9,'observed_beta'),(1.,'normalized_beta')]:
    ke=.0498+beta*.0441
    w=(equity*ke+debt*.0625*(1-.25))/(equity+debt)
    rates[str(beta)]=w
    for case in ['base','recovery']:
        c=old['cases'][case]; g=c['inputs']['g']
        pv=sum(row['fcff']*math.exp(-row['year']*math.log1p(w)) for row in c['forecast'])
        terminal_pv=c['terminal_fcff']/(w-g)*math.exp(-10*math.log1p(w))
        ev=pv+terminal_pv
        value=(ev+cash-old['net_claims'])/shares
        expected=new['cases'][label+'_'+case]['value']
        checks.append(dict(label=label,case=case,wacc=w,pv_explicit=pv,pv_terminal=terminal_pv,value=value,expected=expected,error=value-expected))
# Independent cash-flow expression: NOPAT + D&A - capex - WC;
# blend with ROIC-based reinvestment after year5. Does not use new model rows.
reverse=[]
for answer in new['reverse']:
    c=old['cases']['base']['inputs']; revenue=7460.3; pv=0
    w=rates[str(float(answer['beta']))]
    for year in range(1,11):
        growth=answer['growth'] if year<=5 else answer['growth']+(c['g']-answer['growth'])*(year-5)/5
        previous=revenue; revenue=previous*(1+growth)
        margin=c['startmargin']+(answer['margin']-c['startmargin'])*min(1,(year-1)/4)
        amort=c['ppa_opening']*([.35,.27,.18,.10,.06,.04][year-1] if year<=6 else 0)
        profit=(revenue*margin-amort)*(1-c['tax'])
        cash_before_terminal_blend=profit+revenue*c['maintenance_da']+amort-revenue*c['investment']-(revenue-previous)*c['wc']
        terminal_style_cash=profit*(1-growth/c['roic'])
        blend=max(0,(year-5)/5)
        fcff=cash_before_terminal_blend*(1-blend)+terminal_style_cash*blend
        pv+=fcff/(1+w)**year
    terminal=revenue*(1+c['g'])*answer['margin']*(1-c['tax'])*(1-c['g']/c['roic'])
    value=(pv+terminal/(w-c['g'])/(1+w)**10+cash-old['net_claims'])/shares
    reverse.append(dict(beta=answer['beta'],margin=answer['margin'],growth=answer['growth'],independent_value=value,error_from_price=value-192.96))
assert all(abs(x['error'])<1e-8 for x in checks)
assert all(abs(x['error_from_price'])<1e-8 for x in reverse)
result=dict(method='Preserved A186 FCFF repriced, plus separately reconstructed reverse cash flows. No model import.',rates=rates,base_recovery_checks=checks,reverse_checks=reverse,passed=True)
(P/'independent_check_output.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
