from pathlib import Path
import sys,copy,json,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import model
out={'source_cutoff_utc':'2026-11-04T15:04:07Z','original_model_sha256':hashlib.sha256((P/'model.py').read_bytes()).hexdigest(),'reference_price':model.PRICE,'not_new_guidance':'150m is qualitative capex reference at current growth, not FY2027 formal guidance','cases':{}}
for name,fl in [('central_unchanged',None),('150m_floor_years1_2',[150,150,0,0,0,0,0,0,0,0]),('150m_floor_years1_3',[150,150,150,0,0,0,0,0,0,0]),('150m_floor_all_years',[150]*10)]:
 p=copy.deepcopy(model.SCENARIOS['central'])
 if fl:p['capex_floor']=fl
 r=model.project(p);out['cases'][name]={k:r[k] for k in ['per_share','enterprise_value','enterprise_fixed_exit_irr','equity_distribution_proxy_irr']};out['cases'][name]['cash_capex']=[x['capex_total'] for x in r['years']]
b=model.project(model.SCENARIOS['central'])
for n in [2,3,10]:
 extra=[max(0,150-y['capex_total']) if y['year']<=n else 0 for y in b['years']]
 pv=sum(x/(1+b['params']['wacc'])**(i+1) for i,x in enumerate(extra))
 e=model.equity_value(b['enterprise_value']-pv)
 out['cases']['150m_floor_no_extra_capacity_'+str(n)+'years']={'extra_cash_capex':extra,'pv_extra_capex':pv,'per_share':e['per_share'],'interpretation':'Conservative cost overlay: no credit for additional capacity or displaced future capex; not a new fully integrated operating scenario.'}
(P/'post_call/call_sensitivities.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
