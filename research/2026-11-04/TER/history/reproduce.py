#!/usr/bin/env python3
"""Offline, standard-library-only history rebuild from minimal source-mapped factual inputs."""
import csv,json,pathlib
P=pathlib.Path(__file__).resolve().parent
F=json.loads((P/'inputs.json').read_text())['facts']
metrics=sorted({f['metric'] for f in F if f['segment'] is None})
periods={}

def direct(name,source,start,end):
 d={}
 for f in F:
  if f['source_id']==source and f['start']==start and f['end']==end:
   key=f['metric']+(':'+f['segment'] if f['segment'] else '')
   d[key]={'value':f['value_usd_m'],'formula':'reported','fact_ids':[f['fact_id']]}
 periods[name]=d

def combine(name,terms):
 keys=set().union(*(periods[p] for p,s in terms));d={}
 for k in sorted(keys):
  if all(k in periods[p] for p,s in terms):
   d[k]={'value':round(sum(periods[p][k]['value']*s for p,s in terms),6),'formula':' '.join(('+' if s==1 else '-')+p for p,s in terms),'fact_ids':sum([periods[p][k]['fact_ids'] for p,s in terms],[])}
 periods[name]=d
for year in [2023,2024,2025]: direct('FY'+str(year),'fy',str(year)+'-01-01',str(year)+'-12-31')
for yr in [2025,2026]:
 ends={2025:['2025-03-30','2025-06-29','2025-09-28'],2026:['2026-03-29','2026-06-28','2026-09-27']}[yr]
 for n,end in enumerate(ends,1):direct(str(n*3)+'M'+str(yr),'q'+str(n),str(yr)+'-01-01',end)
 direct('Q1FY'+str(yr),'q1',str(yr)+'-01-01',ends[0])
 combine('Q2FY'+str(yr),[('6M'+str(yr),1),('3M'+str(yr),-1)])
 combine('Q3FY'+str(yr),[('9M'+str(yr),1),('6M'+str(yr),-1)])
 # Prefer directly reported standalone income-statement and segment facts; cash flows remain YTD differences.
 for n,start in [(2,{2025:'2025-03-31',2026:'2026-03-30'}[yr]),(3,{2025:'2025-06-30',2026:'2026-06-29'}[yr])]:
  direct('_direct','q'+str(n),start,ends[n-1]);periods['Q'+str(n)+'FY'+str(yr)].update(periods.pop('_direct'))
direct('9M2024','priorq3','2024-01-01','2024-09-29')
combine('Q4FY2024',[('FY2024',1),('9M2024',-1)])
combine('Q4FY2025',[('FY2025',1),('9M2025',-1)])
combine('TTM2026Q3',[('FY2025',1),('9M2026',1),('9M2025',-1)])
combine('TTM2025Q3',[('FY2024',1),('9M2025',1),('9M2024',-1)])

def calc(d,k,req,fn,formula):
 if all(x in d for x in req):d[k]={'value':round(fn(*(d[x]['value'] for x in req)),6),'formula':formula,'fact_ids':sum([d[x]['fact_ids'] for x in req],[])}
for name,d in periods.items():
 calc(d,'da',['depreciation','amortization_cf'],lambda a,b:a+b,'depreciation + amortization_cf')
 calc(d,'fcf',['cfo','capex'],lambda a,b:a-b,'cfo - capex')
 calc(d,'fcf_after_sbc_cf',['cfo','capex','sbc_cf'],lambda a,b,c:a-b-c,'cfo - capex - sbc_cf; economic cost proxy, not GAAP')
 calc(d,'ebitda',['ebit','da'],lambda a,b:a+b,'ebit + da; SBC remains an expense')
 calc(d,'ebit_margin_pct',['ebit','revenue'],lambda a,b:a/b*100,'100 * ebit / revenue')
 calc(d,'effective_tax_rate_pct',['income_tax','pretax_before_equity_method'],lambda a,b:a/b*100,'100 * income_tax / pretax_before_equity_method')
 calc(d,'ebit_before_restructuring_and_acquisition_amortization',['ebit','restructuring_other','acquisition_intangible_amortization'],lambda a,b,c:a+b+c,'ebit + restructuring_other + acquisition_intangible_amortization; sensitivity only, not assumed sustainable')
 for s in ['SemiconductorTest','ProductTest','Robotics']:
  calc(d,'segment_pretax_margin_pct:'+s,['segment_pretax_income:'+s,'segment_revenue:'+s],lambda a,b:a/b*100,'100 * segment pretax income / segment revenue; NOT operating margin')
rows=[]
for period,d in periods.items():
 for metric,v in sorted(d.items()):rows.append({'period':period,'metric':metric,'value':v['value'],'unit':'percent' if '_pct' in metric else 'USD million','formula':v['formula'],'fact_ids':'|'.join(v['fact_ids'])})
with (P/'normalized_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'normalized_history.json').write_text(json.dumps({'as_of':'2026-11-04','periods':periods},indent=2,sort_keys=True)+'\n')
checks=[]
for name,d in periods.items():
 if all('segment_revenue:'+s in d for s in ['SemiconductorTest','ProductTest','Robotics']):
  residual=d['revenue']['value']-sum(d['segment_revenue:'+s]['value'] for s in ['SemiconductorTest','ProductTest','Robotics'])
  checks.append({'check':name+' segment revenue tie-out','residual_usd_m':round(residual,6),'pass':abs(residual)<0.002})
 if all(x in d for x in ['pretax_before_equity_method','income_tax','equity_method_income','net_income','noncontrolling_income']):
  residual=d['pretax_before_equity_method']['value']-d['income_tax']['value']+d['equity_method_income']['value']-d['noncontrolling_income']['value']-d['net_income']['value']
  checks.append({'check':name+' pretax/tax/equity/NCI to NI','residual_usd_m':round(residual,6),'pass':abs(residual)<0.002})
for m in ['revenue','ebit','net_income','cfo','capex','sbc_cf','da']:
 residual=periods['TTM2026Q3'][m]['value']-sum(periods[p][m]['value'] for p in ['Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026'])
 checks.append({'check':'TTM2026Q3 four-quarter '+m,'residual_usd_m':round(residual,6),'pass':abs(residual)<0.002})
(P/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(str(len(rows))+' rows; '+str(len(checks))+' checks; failures='+str(sum(not x['pass'] for x in checks)))
for p in ['FY2023','FY2024','FY2025','Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026','TTM2026Q3','TTM2025Q3']:
 print(p,{k:periods[p].get(k,{}).get('value') for k in ['revenue','ebit','net_income','cfo','capex','da','sbc_cf','sbc_expense','fcf_after_sbc_cf']})
assert all(c['pass'] for c in checks)
wc=json.loads((P/'working_capital_inputs.json').read_text())
with (P/'working_capital.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(wc[0]));w.writeheader();w.writerows(wc)
