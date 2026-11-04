#!/usr/bin/env python3
"""Offline rebuild; Python standard library only. USD million, EPS USD/share."""
import json,csv,copy,pathlib
P=pathlib.Path(__file__).resolve().parent
raw=json.loads((P/'numerical_inputs.json').read_text());d=copy.deepcopy(raw);lin=json.loads((P/'input_lineage.json').read_text());checks=[]
def check(name,a,b):checks.append({'check':name,'actual':a,'expected':b,'pass':abs(a-b)<0.00001})
def derive(period,terms,fields=None):
 d.setdefault(period,{});lin.setdefault(period,{})
 if fields is None:fields=sorted(set.union(*(set(d[p]) for p,_ in terms))-{'eps_diluted'})
 for m in fields:
  if m in d[period]:
   if all(d[p].get(m) is not None for p,_ in terms):check(period+'.'+m+' reported vs cumulative',d[period][m],sum(d[p][m]*s for p,s in terms))
   continue
  val=sum(d[p][m]*s for p,s in terms) if all(d[p].get(m) is not None for p,_ in terms) else None
  d[period][m]=val;lin[period][m]={'formula':' + '.join(f'{s} * {p}.{m}' for p,s in terms),'status':'derived' if val is not None else 'unavailable input'}
for y in [2025,2026]:
 derive('Q2'+str(y),[('H1'+str(y),1),('Q1'+str(y),-1)])
 derive('Q3'+str(y),[('9M'+str(y),1),('H1'+str(y),-1)])
derive('Q42025',[('FY2025',1),('9M2025',-1)])
derive('TTM2026Q3',[('FY2025',1),('9M2026',1),('9M2025',-1)])
derive('TTM2025Q3',[('FY2024',1),('9M2025',1),('9M2024',-1)])
for m,v in d.pop('9M2025_check').items():check('Q3 2025 release vs Q3 2026 filing '+m,v,d['9M2025'][m])
lin.pop('9M2025_check')
metrics=sorted(set.union(*(set(v) for v in d.values())))
for p,row in d.items():
 for m in metrics:
  if m not in row:row[m]=None;lin[p][m]={'status':'not established; EPS not summed across changing denominators' if m=='eps_diluted' else 'not established'}
 for m,formula,value in [('fcf_cfo_less_capex','cfo - capex_including_software',row['cfo']-row['capex_including_software']),('ebit_margin','ebit_gaap / revenue',row['ebit_gaap']/row['revenue']),('ebitda_mechanical','ebit_gaap + da',row['ebit_gaap']+row['da']),('fas_cas_total_adjustment','fas_cas_operating_adjustment + nonservice_pension_income_signed',row['fas_cas_operating_adjustment']+row['nonservice_pension_income_signed'])]:row[m]=value;lin[p][m]={'formula':formula,'status':'derived'}
 row['owner_fcf']=None;lin[p]['owner_fcf']={'status':'not established: no sustainable working-capital, maintenance capex or program cash-loss normalization'}
 check(p+' EBIT reconciliation',row['ebit_gaap'],sum(row[x] for x in ['segment_profit_nongaap','fas_cas_operating_adjustment','intangible_amort_signed','impairment_signed','other_unallocated_signed']))
 check(p+' NI reconciliation',row['net_income'],row['pretax_income']+row['income_tax_signed'])
for m in ['revenue','ebit_gaap','net_income','cfo','capex_including_software','da','sbc']:
 check('TTM26 equals latest 4Q '+m,d['TTM2026Q3'][m],sum(d[p][m] for p in ['Q42025','Q12026','Q22026','Q32026']))
order=['FY2023','FY2024','FY2025','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','9M2024','H12025','9M2025','H12026','9M2026','TTM2025Q3','TTM2026Q3']; d={p:d[p] for p in order}
(P/'normalized_history.json').write_text(json.dumps({'units':'USD million except EPS USD/share and margins decimal','as_of':'2026-11-04','periods':d},indent=2)+'\n')
with (P/'normalized_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(d.values()))));w.writeheader();w.writerows({'period':p,**v} for p,v in d.items())
(P/'field_lineage.json').write_text(json.dumps(lin,indent=2)+'\n');(P/'qa.json').write_text(json.dumps({'all_pass':all(c['pass'] for c in checks),'checks':checks},indent=2)+'\n')
assert all(c['pass'] for c in checks),[c for c in checks if not c['pass']]
print(f'{len(d)} periods; {len(checks)} QA checks passed')
