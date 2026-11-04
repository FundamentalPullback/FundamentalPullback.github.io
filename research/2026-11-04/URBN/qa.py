from pathlib import Path
import json,math
p=Path(__file__).parent;m=json.loads((p/'model.json').read_text());h=json.loads((p/'history/periods.json').read_text());r=json.loads((p/'publication.json').read_text());checks=[]
def ck(n,v):assert v,n;checks.append(n)
def close(a,b):return abs(a-b)<1e-8
h=next(x for x in h if x['period']=='TTM2026-07-31')
for k,v in [('revenue',6474.380),('ebit',731.440),('cfo',715.886),('ppe_cash_purchases',420.675),('sbc',31.154)]:ck('anchor '+k,close(h[k],v))
for k,c in m['cases'].items():
 ck(k+' bridge',close(c['bridge'],786.134));ck(k+' equity',close((c['ev']+c['bridge'])/c['shares'],c['value_per_share']))
 for y in c['rows']:
  ck(k+str(y['year'])+' identity',close(y['fcff'],y['nopat']+y['da']-y['capex']-y['delta_nwc']-y['additional_reinvestment_reserve']))
  ck(k+str(y['year'])+' physical',y['reinvestment']+1e-8>=y['physical_reinvestment']);ck(k+str(y['year'])+' economic',y['reinvestment']+1e-8>=y['economic_reinvestment']);ck(k+str(y['year'])+' nonnegative reserve',y['additional_reinvestment_reserve']>=-1e-8)
 t=c['terminal'];ck(k+' terminal floor',t['reinvestment']>=max(t['physical_reinvestment'],t['economic_reinvestment']));ck(k+' terminal identity',close(t['fcff'],t['nopat']-t['reinvestment']));ck(k+' ev',close(c['ev'],sum(y['pv_fcff'] for y in c['rows'])+t['pv']))
for k in ['owner_fcf','equity_bridge','buy_ceiling']:ck(k+' null',r[k] is None)
for k in ['latestCompleted','approved_entry','stage35_approved']:ck(k+' false',r[k] is False)
ck('reverse bracketed root',len(m['reverse_margin_shift_roots'])==1)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for v in r[k]:ck(k+' exact passage '+v[:20],v in (p/'report.md').read_text())
ck('no macros','{BASE}' not in (p/'report.md').read_text())
(p/'qa.json').write_text(json.dumps(dict(status='PASS',count=len(checks),checks=checks),indent=2)+'\n');print(len(checks),'PASS')

from model import calc,CASES
c=dict(CASES['base']);d=m['reverse_margin_shift_roots'][0];c.update(m1=c['m1']+d,m5=c['m5']+d,mt=c['mt']+d);assert abs(calc(c)['value_per_share']-91.78)<1e-8
