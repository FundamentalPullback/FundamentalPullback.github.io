"""Independent, read-only audit recomputation. No model import or network access."""
import json, pathlib, hashlib, math, re
P=pathlib.Path(__file__).resolve().parent
r=json.loads((P/'results.json').read_text());f=json.loads((P/'financial_inputs.json').read_text())
def recalc(c,floor=True):
 rev=r['base_revenue'];pv=0;rows=[]
 for n in range(1,11):
  a=max(0,(n-5)/5)
  gr=c['growth'][n-1] if n<=5 else c['growth'][-1]*(1-a)+c['g']*a
  margin=c['margins'][n-1] if n<=5 else c['margins'][-1]*(1-a)+c['terminal_margin']*a
  old=rev;rev*=1+gr;nopat=rev*margin*.76
  physical=rev*(c['ppe']+c['software']+c['acq']-c['da'])+(rev-old)*c['nwc_growth']
  reinvest=physical*(1-a)+nopat*gr/c['roic']*a
  if floor:reinvest=max(reinvest,physical)
  pv+=(nopat-reinvest)/(1+c['wacc'])**n
  rows.append((rev,nopat,reinvest,physical))
 nopat=rows[-1][1]*(1+c['g']);rev11=rev*(1+c['g'])
 physical=rev11*(c['ppe']+c['software']+c['acq']-c['da'])+(rev11-rev)*c['nwc_growth']
 terminal=nopat*c['g']/c['roic']
 if floor:terminal=max(terminal,physical)
 pvtv=(nopat-terminal)/(c['wacc']-c['g'])/(1+c['wacc'])**10
 return {'value':(pv+pvtv+1334.021)/50.8,'terminal_reinvestment':terminal,'terminal_physical_requirement':physical,'terminal_shortfall':max(0,physical-terminal),'year10_shortfall':max(0,rows[-1][3]-rows[-1][2])}
checks={}
for k,c in r['cases'].items():
 z=recalc(c);assert abs(z['value']-r['results'][k]['value'])<1e-9;checks[k]=z
for s in r['sensitivity']:
 assert abs(recalc({**r['cases']['central'],'wacc':s['wacc'],'g':s['g']})['value']-s['value'])<1e-9
for v in r['reverse']:
 c={**r['cases']['central'],'growth':v['growth_first5'],'margins':[x*v['margin_multiplier'] for x in r['cases']['central']['margins']],'terminal_margin':.22*v['margin_multiplier']}
 assert abs(recalc(c)['value']-160.42)<1e-8
for k in ['revenue','ebit','ni','cfo','ppe','software','sbc']:
 assert abs(sum(r['history'][q][k] for q in ['2025Q4','2026Q1','2026Q2','2026Q3'])-r['history']['TTM_20260930'][k])<1e-8
for v in json.loads((P/'financial_input_provenance.json').read_text()):
 tag=v['tag'];fact={k:x for k,x in v.items() if k!='tag'}
 assert any(fact in vals for vals in f[tag]['units'].values())
assert abs(r['scanner_mapping']['matching_20260630_net_margin']-.35875)<.000005
out={'corrected_values_reproduced':checks,'all_12_sensitivities_reproduced':True,'all_3_reverse_cases_reproduced':True,'last_four_quarters_tie':True,'all_public_input_provenance_matches':True,'illustrative_physical_floor_sensitivity':{k:recalc(c,True) for k,c in r['cases'].items()}}
print(json.dumps(out,indent=2))
