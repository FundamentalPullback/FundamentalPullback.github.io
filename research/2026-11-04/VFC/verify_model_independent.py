"""Second implementation of VFC FCFF arithmetic, independent of model.py.
Run from any directory: python verify_model_independent.py.
Read model_results.json, recompute all scenarios and reverse solutions, save checks.
"""
from pathlib import Path
import json,copy,hashlib
P=Path(__file__).parent
s=json.loads((P/'model_results.json').read_text())
R0=s['retained_ttm_revenue'];N=s['economic_share_denominator'];C=s['claims'];PRICE=s['quote']['price']
claims=sum(v for k,v in C.items() if k!='cash')-C['cash']
def calc(p,netclaims=claims,shares=N,midyear=False,sustain=True):
    rev=R0; flows=[]; periods=[]
    for t,(growth,margin) in enumerate(zip(p['growth'],p['margin']),1):
        previous=rev;rev=previous*(1+growth);delta=rev-previous
        tax_default=p['tax'] if isinstance(p['tax'],list) else [p['tax']]*10
        tax=p.get('tax_path',tax_default)[t-1]
        profit=rev*margin*(1-tax)
        depreciation=rev*p['da_ratio']
        delta_wc=delta*p['wc_ratio']+(p['year1_extra_wc'] if t==1 else 0)
        tangible_growth=max(0,max(delta,0)/p['sc']-max(delta*p['wc_ratio'],0))
        net_inv_initial=(p['maintenance']-1)*depreciation+tangible_growth+delta_wc
        transition=max(0,(t-7)/3) if sustain else 0
        mature_net=delta_wc+transition*max(0,profit*max(growth,0)/p['roic']-delta_wc)
        net_inv=max(net_inv_initial,mature_net)
        fcff=profit-net_inv;pv=fcff/(1+p['wacc'])**(t-(.5 if midyear else 0))
        flows.append(fcff);periods.append(dict(year=t,revenue=rev,nopat=profit,net_reinvestment=net_inv,fcff=fcff,pv_fcff=pv,capex=net_inv-delta_wc+depreciation))
    last_tax=p['tax'][-1] if isinstance(p['tax'],list) else p['tax']
    terminal_nopat=rev*(1+p['g'])*p['margin'][-1]*(1-p.get('terminal_tax',last_tax))
    terminal_ni=terminal_nopat*p['g']/p['roic'];terminal_fcff=terminal_nopat-terminal_ni
    terminal=terminal_fcff/(p['wacc']-p['g'])
    # Conventional simple midyear adjustment to explicit flows only, terminal still year 10.
    pv_terminal=terminal/(1+p['wacc'])**10
    ev=sum(x['pv_fcff'] for x in periods)+pv_terminal
    return dict(years=periods,enterprise_value=ev,unfloored_equity=ev-netclaims,per_share=max(0,ev-netclaims)/shares,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_ni,terminal_fcff=terminal_fcff,terminal_ev=terminal,pv_terminal=pv_terminal,terminal_share=pv_terminal/ev,cagr=(rev/R0)**.1-1)

checks=[]
cases={**s['scenarios'],'constructive':s['constructive_tax_margin_path'],'joint_alternative':s['plausible_joint_alternative']}
for name,stored in cases.items():
 z=calc(stored['params'])
 for key in ['enterprise_value','per_share','terminal_nopat','terminal_reinvestment','terminal_fcff','terminal_ev','pv_terminal','terminal_share']:
  checks.append({'test':name+'/'+key,'error':z[key]-stored[key],'pass':abs(z[key]-stored[key])<1e-8})
 for row,old in zip(z['years'],stored['years']):
  for key in ['revenue','nopat','fcff','pv_fcff']:
   checks.append({'test':name+'/Y'+str(row['year'])+'/'+key,'error':row[key]-old[key],'pass':abs(row[key]-old[key])<1e-8})
p=s['scenarios']['central']['params']
for r in s['reverse_joint']:
 z=copy.deepcopy(p);z['growth']=[g+r['growth_shift'] for g in z['growth']];z['margin']=[m+(r['year10_margin']-p['margin'][-1])*min(1,i/3) for i,m in enumerate(z['margin'])];z['wacc']=r['wacc'];v=calc(z)['per_share']
 checks.append({'test':'reverse/'+str(r['wacc'])+'/'+str(r['year10_margin']),'error':v-PRICE,'pass':abs(v-PRICE)<1e-8})
z=copy.deepcopy(s['constructive_tax_margin_path']['params']);z['growth']=[s['reverse_constructive']['revenue_cagr']]*10;v=calc(z)['per_share'];checks.append({'test':'reverse/constructive','error':v-PRICE,'pass':abs(v-PRICE)<1e-8})
for name,tax in [('flat28pct',.28),('partial25pct',[.28,.27,.26]+[.25]*7),('reach23pct',[.28,.26,.24]+[.23]*7)]:
 v=calc(dict(p,tax=tax))['per_share'];target=next(x['value'] for x in s['tax_sensitivities'] if x['case']==name);checks.append({'test':'tax/'+name,'error':v-target,'pass':abs(v-target)<1e-8})
out={'source_model_sha256':hashlib.sha256((P/'model_results.json').read_bytes()).hexdigest(),'checks':checks,'all_pass':all(x['pass'] for x in checks)}
(P/'independent_checks.json').write_text(json.dumps(out,indent=2))
assert out['all_pass'];print(str(len(checks))+' independent arithmetic checks passed')
