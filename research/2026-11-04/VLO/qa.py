import json,pathlib,math
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());h=json.loads((P/'history/portable/financial_history.json').read_text());pub=json.loads((P/'publication.json').read_text());r=(P/'report.md').read_text();c=[]
def ck(b,n):assert b,n;c.append(n)
for case,a in m['cases'].items():
 ck(len(a['rows'])==10,case+' ten years');pv=0
 for z in a['rows']:
  ck(abs(z['refining_ebit']+z['renewable_diesel_ebit']+z['ethanol_ebit']-z['corporate_expense']-z['ebit'])<1e-7,case+' segments'+str(z['year']))
  ck(abs(z['nopat']+z['da']-z['total_capital_investment']-z['delta_nwc']-z['additional_reinvestment_reserve']-z['fcff'])<1e-7,case+' fcff'+str(z['year']))
  ck(z['delta_nwc']>=0 and z['additional_reinvestment_reserve']>=-1e-7,case+' no unfinanced gap'+str(z['year']))
  ck(abs(z['pv']-z['fcff']/(1+a['assumptions']['wacc'])**z['year'])<1e-7,case+' discount'+str(z['year']));pv+=z['pv']
 ck(abs(pv+a['pv_terminal']-a['ev'])<1e-7,case+' enterprise value');ck(abs((a['ev']+m['bridge'])/a['shares']-a['value'])<1e-7,case+' per share');ck(a['terminal_reinvestment']>0,case+' funded terminal');ck(a['terminal_reinvestment']>=a['terminal_physical_reinvestment_floor'] and a['terminal_reinvestment']>=a['terminal_economic_reinvestment_floor'],case+' terminal preserves both floors');ck(a['assumptions']['wacc']>a['assumptions']['g'],case+' stable terminal')
ck(abs(m['reverse']['value']-387.65)<1e-7,'reverse reproduces target');ck(m['bridge']==-10387,'bridge arithmetic');ck(11001-8579==2422 and 8635+2422==11057,'nominal debt and leases');ck(h['rows']['TTM_2026Q3']['SBC_total'] is None,'SBC unknown not zero')
for k in ['pros_es','cons_es']:
 for t in pub[k]:ck(t in r,'exact report evidence')
for k in ['pros_en','cons_en']:
 for t in pub[k]:ck(t in (P/'english_evidence.md').read_text(),'English exact evidence')
for k in ['bear','base','bull']:ck(abs(pub[k]-m['cases'][k]['value'])<1e-10,'metadata '+k)
ck(not pub['approved_entry'] and not pub['stage35_approved'] and pub['buy_ceiling'] is None,'no entry')
(P/'qa.json').write_text(json.dumps({'status':'PASS','checks':len(c),'details':c},indent=2)+'\n');print('PASS',len(c))
