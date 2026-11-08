"""Independent executable FBIN tie-out and FCFF controls; USD millions."""
import json,math,hashlib
from pathlib import Path
import model as m
P=Path(__file__).parent
checks=[]
def close(a,b,label,tol=1e-7):
 assert abs(a-b)<tol,(label,a,b)
 checks.append(label)
r=json.loads((P/'model_results.json').read_text())
for name in m.SC:
 v=m.value(name)
 close(v['value'],r['scenarios'][name]['value'],name+' recomputed value')
 for row in v['rows']:
  close(row['fcff'],row['nopat']+row['da']-row['capex_including_software']-row['delta_nwc'],name+f" FCFF year{row['year']}")
  assert row['capex_including_software']>0
 t=v['terminal'];close(t['fcff'],t['nopat']+t['da']-t['capex']-t['delta_nwc'],name+' terminal physical identity')
 close(t['fcff'],v['rows'][-1]['fcff']*(1+v['g']),name+' terminal continuity')
 assert v['wacc']>v['g']
 close(v['equity'],v['ev']-2318.7+230.9-100-33.4+m.SC[name]['proceeds']-m.SC[name]['exit_costs'],name+' equity bridge')
stress=m.value(software_extra=10);t=stress['terminal'];close(t['fcff'],t['nopat']+t['da']-t['capex']-t['delta_nwc'],'software stress terminal physical identity')
close(m.bondvalue(m.KD),2004.2,'aggregate debt market PV')
close(m.value(margin_shift=r['reverse']['required_margin_shift'])['value'],48.08,'inverse margin')
close(m.value(growth_extra=r['reverse']['required_growth_extra'])['value'],48.08,'inverse growth')
for k,annual,current,prior in [('revenue',4463.2,3278.9,3385.7),('ebit',516.1,111.7,394.4),('net_income',298.8,51.6,222.4),('cfo',478.6,430.6,270.4),('capex',111.8,59.7,87.3),('da',194.4,121.2,151.5)]:
 if k=='ebit':
  close(annual+current-prior-r['ttm'][k],.1,'TTM EBIT disclosed rounding residual0.1')
 else:
  close(r['ttm'][k],annual+current-prior,'TTM source bridge '+k)
close(1.14-.28-.14,.72,'Q3 EPS normalization')
close(554.6-121.5-4.3-14,414.8,'cash economic normalization')
close(233.3+306.6+44.2-134-4.8,445.3,'EBIT economic normalization')
out={'status':'passed','checks':checks,'check_count':len(checks),'illustrative_audit_sensitivities':{'remove_proceeds_per_share':145/m.SHARES,'additional_exit_cash100_per_share':100/m.SHARES,'one_year_delay_loss_removal55_per_share':55*.75/(1+m.WACC)/m.SHARES},'hashes':{x:hashlib.sha256((P/x).read_bytes()).hexdigest() for x in ['model.py','model_results.json','report.md','source_ledger.json','status.json']}}
(P/'audit_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'check_count':len(checks),'stresses':out['illustrative_audit_sensitivities']},indent=2))
