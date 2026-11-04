import pathlib,json,math,csv,re
P=pathlib.Path(__file__).parent
from model import calculate,SCENARIOS,SHARES,PRICE,STUB_YEARS
m=json.load(open(P/'model_results.json'));s=json.load(open(P/'summary.json'));v=json.load(open(P/'valuation_checks.json'));report=(P/'report.md').read_text();checks=[]
def check(label,b):
 checks.append({'check':label,'pass':bool(b)})
def near(label,a,b):check(label,math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8))
for name,x in m['scenarios'].items():
 z=calculate(SCENARIOS[name]);near(name+' reproduction',x['value'],z['value']);near(name+' metadata',s[name],x['value']);check(name+' ten full years',len(x['rows'])==10);a=x['assumptions'];check(name+' wacc > g',a['wacc']>a['g']);check(name+' first year calendar',x['rows'][0]['discount_years']>1.48)
 for i,r in enumerate(x['rows']):
  tag=f'{name} year{i+1} '
  near(tag+' EBIT',r['EBIT'],r['revenue']*r['EBIT_margin']);near(tag+' NOPAT',r['NOPAT'],r['EBIT']*(1-a['tax']));near(tag+' FCFF',r['FCFF'],r['NOPAT']+r['DA']-r['total_capex']-r['working_capital_investment']);near(tag+' PV',r['PV'],r['FCFF']/(1+a['wacc'])**r['discount_years']);check(tag+' funded growth',r['total_capex']-r['DA']+r['working_capital_investment']+1e-8>=r['positive_delta_NOPAT_over_ROIC']);check(tag+' physical floor',r['total_capex']+1e-8>=r['physical_capex'])
  prior=x['stub']['annualized_NOPAT']if i==0 else x['rows'][i-1]['NOPAT'];near(tag+' literal deltaNOPAT',r['positive_delta_NOPAT_over_ROIC'],max(0,r['NOPAT']-prior)/a['roic'])
 last=x['rows'][-1];tn=last['NOPAT']*(1+a['g']);net=max(tn*a['g']/a['roic'],(last['physical_capex']-last['DA'])*(1+a['g'])+last['revenue']*a['g']*a['wc_ratio']);near(name+' terminal investment',x['terminal_net_reinvestment'],net);near(name+' TV',x['terminal_value'],(tn-net)/(a['wacc']-a['g']));near(name+' EV',x['EV'],sum(r['PV']for r in x['rows'])+x['stub']['PV']+x['PV_terminal']);near(name+' equity',x['equity'],x['EV']+x['capital_bridge_scenario_not_measured']['net_equity_adjustment']);near(name+' per share',x['value'],x['equity']/SHARES)
check('scenario ordering',s['bear']<s['base']<s['bull']);near('price immutable',s['lastClose'],190.78);check('scan distinct',s['scanDate']=='2026-10-29'and s['scanPrice']==215.36);check('provisional calendar',s['earningsDateConfirmed']is False and s['calendarGatePassed']is False);check('no unresolved comps placeholder','[COMPARABLES_PENDING]'not in report)
near('reverse growth reprices',calculate(dict(SCENARIOS['base']),growth_shift=v['reverse_growth_uniform_addition'])['value'],PRICE);near('reverse margin reprices',calculate(dict(SCENARIOS['base']),margin_shift=v['reverse_margin_uniform_addition'])['value'],PRICE)
for i,x in enumerate(json.load(open(P/'pros_cons.json'))):
 check(f'evidence{i}exact paragraph',x['evidence']in report.split('\n\n'));check(f'text{i}es length',len(x['text_es'])<=320);check(f'text{i}en length',len(x['text_en'])<=360)
h=list(csv.DictReader(open(P/'history/history.csv')));d={r['period']:r for r in h};t=d['TTM2026-07-31'];near('history gaapEBIT',float(t['operating_income']),1849);near('history normalizedEBIT',float(t['operating_income_ex_spot_gain']),1838);near('history FCF',float(t['fcf']),1650);near('history SBC retained',float(t['fcf_after_sbc']),1253)
for n in ['history/validation.json','comps/comps.json']:
 check('exists '+n,(P/n).exists())
hr=json.load(open(P/'history/validation.json'));check('history pass',hr['checks_failed']==0)
cp=json.load(open(P/'comps/comps.json'));check('two peers',len(cp['rows'])>=2)
out={'status':'PASS'if all(x['pass']for x in checks)else'FAIL','count':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks};(P/'qa.json').write_text(json.dumps(out,indent=2));print(out['status'],out['count'],out['failed']);assert not out['failed']
