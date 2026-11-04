from pathlib import Path
import json
P=Path(__file__).parent;m=json.load(open(P/'model.json'));h=json.load(open(P/'financials.json'));pub=json.load(open(P/'publication.json'));r=(P/'report.md').read_text();checks=[]
def ck(n,x):
 assert x,n
 checks.append(n)
for name,v in m['cases'].items():
 ck(name+' rate',v['assumptions']['wacc']>v['assumptions']['g'])
 for a in v['rows']:
  ck(name+str(a['year'])+' cash reconciliation',abs(a['fcff']-(a['nopat']+a['da']-a['capex']-a['delta_nwc']-a['additional_reinvestment_reserve']))<1e-7)
  ck(name+str(a['year'])+' funded growth',a['reinvestment']>=max(a['explicit_reinvestment'],a['economic_reinvestment'])-1e-7)
 ck(name+' PV',abs(sum(a['pv_fcff'] for a in v['rows'])+v['pv_terminal']-v['ev'])<1e-7)
 ck(name+' equity',abs((v['ev']+v['assumptions']['net'])/v['assumptions']['shares']-v['value'])<1e-8)
 ck(name+' published value',pub[name]==round(v['value'],2))
for k in ['pros_es','pros_en','cons_es','cons_en']:
 for x in pub[k]:ck('exact evidence '+x[:20],x in r)
for p,v in h.items():
 ck(p+' FCF',abs(v['owner_fcf']-(v['cfo']-v['capex']-v['sbc']))<1e-8)
ck('TTM income',h['TTM2026']['net_income']==2459+2273-1849)
ck('TTM revenue',h['TTM2026']['revenue']==7718+6287-5829)
ck('prior EPS direct release',h['Q42024']['eps_basic']==2.18)
ck('no entry',pub['stage35_approved']==False and pub['approved_entry']==False and pub['buy_ceiling'] is None)
ck('SPGI owner unavailable',json.load(open(P/'peers.json'))['peers'][1]['owner_fcf_yield'] is None)
ck('bridge',m['capital_bridge']['net']==-7086)
ck('gain outside EBIT','fuera de EBIT' in r)
json.dump(dict(passed=len(checks),checks=checks),open(P/'qa.json','w'),indent=2);print(len(checks),'QA passed')
