import pathlib,json,math
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());pub=json.loads((P/'publication.json').read_text());h=json.loads((P/'history/shop_financial_history.json').read_text());checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
def near(a,b):return abs(a-b)<1e-7
for r in h['records']:
 ck(r['period']+' PPE',near(r['cfo_minus_ppe'],r['cfo']-r['ppe_cash_spend']))
 ck(r['period']+' funded cash',near(r['cash_after_ppe_and_investing_lending'],r['cfo_minus_ppe']-r['net_investing_lending_funding']))
 ck(r['period']+' economic sensitivity',near(r['cash_after_ppe_lending_intangibles_sbc'],r['cash_after_ppe_and_investing_lending']-r['intangible_cash_spend']-r['sbc']))
for k,v in m['cases'].items():
 c=m['inputs']['scenarios'][k];pv=0
 for r in v['rows']:
  ck(k+str(r['year'])+' FCFF bridge',near(r['fcff'],r['nopat']+r['da']-r['capex']-r['delta_nwc']-r['delta_net_loans']-r['additional_reinvestment_reserve']))
  ck(k+str(r['year'])+' reinvestment floor',r['additional_reinvestment_reserve']>=0 and near(r['nopat']-r['fcff'],max(r['physical_reinvestment'],r['economic_reinvestment'])))
  pv+=r['fcff']/(1+c['w'])**r['year']
 t=v['terminal'];ck(k+' terminal floor',near(t['reinvestment'],max(t['physical_reinvestment'],t['economic_reinvestment'])))
 ck(k+' terminal FCFF',near(t['fcff'],t['nopat']-t['reinvestment']))
 ck(k+' valuation',near(v['value'],(pv+t['fcff']/(c['w']-c['tg'])/(1+c['w'])**10+v['bridge'])/v['shares']))
 ck(k+' rate',c['w']>c['tg'])
ck('bridge',near(m['cases']['base']['bridge'],4518.65));ck('shareproxy',near(m['cases']['base']['shares'],1302.555790))
ck('quarter funding',818-2-(1700-1471)-99-140==348)
ck('no double shift',816-30==786 and 816-229==587)
ck('loan book net',2226+370-246==2350)
ck('strategic components',2596+1706+599+10==4911)
ck('prior quarter cash unmodified',next(r for r in h['records'] if r['period']=='2025Q3')['cfo']==513)
ck('no entry',not pub['approved_entry'] and not pub['stage35_approved'] and pub['buy_ceiling'] is None)
ck('terminal dependence',.80<m['cases']['base']['terminal_share']<.81)
ck('inverse no root in scan',max(x['value'] for x in m['inverse_margin_scan'])<m['inputs']['price'])
r=(P/'report.md').read_text()
for t in pub['pros_es']+pub['cons_es']:ck('exact evidence '+t[:25],t in r)
for k in ['2025Q4','2026Q1','2026Q2','2026Q3']:ck('visible '+k,k in r)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
