from pathlib import Path
import json,math
P=Path(__file__).parent;m=json.load(open(P/'model.json'));h=json.load(open(P/'financials.json'));pub=json.load(open(P/'publication.json'));r=(P/'report.md').read_text();checks=[]
def ck(name,ok):
 assert ok,name
 checks.append(name)
for name,v in m['cases'].items():
 w=v['assumptions']['wacc'];g=v['assumptions']['g'];ck(name+' rate',w>g)
 for row in v['rows']:
  ck(name+f" year{row['year']} FCFF",abs(row['fcff']-(row['nopat']+row['da']-row['capex']-row['delta_nwc']-row['additional_reinvestment_reserve']))<1e-6)
  ck(name+f" year{row['year']} floor",row['reinvestment']>=row['explicit_reinvestment']-1e-6 and row['reinvestment']>=row['economic_reinvestment']-1e-6)
 ck(name+' PV',abs(sum(x['pv_fcff'] for x in v['rows'])+v['pv_terminal']-v['ev_eur_m'])<1e-6)
 ck(name+' per share',abs(v['value']-(v['ev_eur_m']+v['assumptions']['net_bridge'])/v['assumptions']['shares']*v['assumptions']['fx'])<1e-8)
 ck(name+' published',pub[name if name!='base' else 'base']==round(v['value'],2))
for k in ['pros_es','pros_en','cons_es','cons_en']:
 for x in pub[k]:ck('exact '+x[:25],x in r)
ck('no entry',not pub['approved_entry'] and not pub['stage35_approved'] and pub['buy_ceiling'] is None)
ck('historical base',abs(m['historical_A033']['base']['value']-1120)<.5)
ck('history source',h==json.load(open(P/'history/extracts/core_history.json')))
for v in h.values():ck('FCF arithmetic',abs(v['fcf']-(v['cfo']-v['capex']))<1e-6)
ck('capital',abs(m['capital_bridge']['net_bridge']-2819.919543)<1e-5)
ck('post balance date',all(x['date']>'2026-09-27' for x in m['capital_bridge']['post_buyback_rows']))
ck('mistral outside EBIT','fuera del EBIT' in r)
ck('regulatory reservation','implementación BIS posterior' in r)
ck('calendar reservation','no está confirmada' in r)
(P/'qa.json').write_text(json.dumps(dict(passed=len(checks),checks=checks),indent=2));print('QA',len(checks))
