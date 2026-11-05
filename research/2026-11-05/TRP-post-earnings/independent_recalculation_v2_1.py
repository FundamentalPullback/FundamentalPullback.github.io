"""Independent reviewer implementation; does not import or execute the author model.
Input assumptions are copied from the immutable model_output.json under audit.
All values C$m except per-share USD; auditor stresses are NOT repaired forecasts.
"""
from pathlib import Path
from math import prod
import json, hashlib, datetime, csv
SOURCE=Path(__file__).resolve().parent
DEST=Path(__file__).parent
m=json.loads((SOURCE/'model_output.json').read_text())
checks=[]
def ck(label,a,b,tol=1e-7):
    checks.append({'check':label,'independent':a,'package':b,'difference':a-b,'pass':abs(a-b)<tol})

def value(p, reverse_growth=False):
    n=range(1,11)
    fade=[0]*5+[.2,.4,.6,.8,1.]
    growth=[(1-f)*p['rev_growth']+f*p['g'] for f in fade]
    sales=[15070*prod(1+x for x in growth[:t]) for t in n]
    earnings=[x*p['margin'] for x in sales]
    nopat=[x*(1-p['tax']) for x in earnings]
    depreciation=[x*p['da_ratio'] for x in sales]
    nwc=[.01*(sales[i]-(15070 if i==0 else sales[i-1])) for i in range(10)]
    capital=[]
    for i in range(10):
        if i<5:
            if reverse_growth:
                reference_sales=15070*(1.055)**(i+1)
                ref_wc=.01*(reference_sales-reference_sales/1.055)
                ref_net=p['capex'][i]-reference_sales*p['da_ratio']+ref_wc
                capital.append(depreciation[i]+ref_net*(sales[i]/reference_sales)*(growth[i]/.055)-nwc[i])
            else: capital.append(p['capex'][i])
        else:
            old_policy=capital[4]*sales[i]/sales[4]
            terminal_policy=depreciation[i]+nopat[i]*growth[i]/p['roic']-nwc[i]
            capital.append(old_policy*(1-fade[i])+terminal_policy*fade[i])
    investment=[capital[i]-depreciation[i]+nwc[i] for i in range(10)]
    cash=[nopat[i]-investment[i] for i in range(10)]
    dt=56/365
    pv_oper=sum(cash[i]/(1+p['wacc'])**(i+1+dt) for i in range(10))
    termcash=nopat[-1]*(1+p['g'])*(1-p['g']/p['roic'])
    tv=termcash/(p['wacc']-p['g'])
    pv_tv=tv/(1+p['wacc'])**(10+dt)
    jvg=[(1-f)*p['jv_growth']+f*p['g'] for f in fade]
    je=[p['jv_earn0']*prod(1+x for x in jvg[:t]) for t in n]
    jd=[p['jv_dist0']*prod(1+x for x in jvg[:t]) for t in n]
    jcash=[]
    for i in range(10):
        if i<5: jcash.append(jd[i]-p['jv_contrib'][i])
        else:
            old_cash=jd[i]-p['jv_contrib'][4]*je[i]/je[4]
            stable_cash=je[i]*(1-jvg[i]/p['roe'])
            jcash.append(old_cash*(1-fade[i])+stable_cash*fade[i])
    jtv=je[-1]*(1+p['g'])*(1-p['g']/p['roe'])/(p['ke']-p['g'])
    jpv=sum(jcash[i]/(1+p['ke'])**(i+1+dt) for i in range(10))
    jpv_tv=jtv/(1+p['ke'])**(10+dt)
    ev=pv_oper+pv_tv
    jval=jpv+jpv_tv
    claims=2780+3197+44418+12639+2255+218+84+76+41+933+904-(1249-500)
    equity=ev+jval+p['lease']-p['nci']-claims
    return {'core_ev':ev,'jv_equity_value':jval,'lease_value':p['lease'],'nci_value':p['nci'],'net_financial_claims':claims,'equity':equity,'value_usd':max(0,equity)/(1042*1.3961),'value_cad':max(0,equity)/1042,'core_terminal_weight':pv_tv/ev,'total_terminal_weight':(pv_tv+jpv_tv)/(ev+jval+p['lease']),'terminal_fcff':termcash,'core_terminal_value':tv,'jv_terminal_value':jtv,'rows':[{'year':2027+i,'revenue':sales[i],'ebit':earnings[i],'nopat':nopat[i],'da':depreciation[i],'capex':capital[i],'delta_wc':nwc[i],'net_reinvestment':investment[i],'fcff':cash[i],'jv_net_equity_cash':jcash[i]} for i in range(10)]}

values={}
for name,obj in m['scenarios'].items():
    r=value(obj['assumptions']);values[name]=r
    for k,v in r.items():
        if k!='rows':ck(name+'_'+k,v,obj[k])
    for i,row in enumerate(r['rows']):
        for k,v in row.items(): ck(f'{name}_{row["year"]}_{k}',v,obj['rows'][i][k])
for entry in m['sensitivity']:
    a=m['scenarios']['base']['assumptions'].copy();a.update(wacc=entry['wacc'],g=entry['g'])
    ck('sensitivity_'+str(entry['wacc'])+'_'+str(entry['g']),value(a)['value_usd'],entry['value_usd'])
roots={}
for key,lo,hi in [('wacc',.035,.12),('rev_growth',0,.3),('margin',.2,.8)]:
    a=m['scenarios']['base']['assumptions'].copy()
    def diff(x):
        a[key]=x
        return value(a,reverse_growth=True)['value_usd']-64.38
    flo=diff(lo)
    for _ in range(80):
        mid=(lo+hi)/2
        if diff(mid)*flo>0:lo=mid;flo=diff(lo)
        else:hi=mid
    roots[key]=(lo+hi)/2
    ck('reverse_'+key,roots[key],m['reverse'][key])
# Source-transcribed historical values, not author arrays. Annual P2 PDF19/20/137/154/155-157;
# Q3 P1 PDF56/59/61/66; Q1 P5 PDF53/58; Q2 P4 PDF57/62; 2025 P3 PDF60/67;
# P6 PDF58; P7 PDF53. The 2026 comparatives verify 2025 discontinued CFO.
source_annual=[(2023,13267,5097,2217,2.15,3.78,7268,1026,7958,142,4149),(2024,13771,7964,4199,4.05,3.73,7696,670,6181,50,4683-3137),(2025,15239,8036,3612,3.47,3.51,7346,-185,5270,16,1051)]
annual=[]
for z in source_annual:
    d=dict(zip(['year','revenue','segmented_ebit','common_net','eps','comp_eps','cfo_total','cfo_discontinued','core_capex','development','jv_contribution'],z));d['cfo_cont']=d['cfo_total']-d['cfo_discontinued'];d['cash_reinvestment']=d['core_capex']+d['development']+d['jv_contribution'];d['fcf_before_nci_preferred']=d['cfo_cont']-d['cash_reinvestment'];annual.append(d)
    old=next(x for x in m['annual'] if x['year']==d['year'])
    for k,v in d.items():ck('history_'+str(d['year'])+'_'+k,v,old[k])
source_quarters=[
 ('2024Q4',3577,1069,1.03,1.05,1094,7696-5612,670-724,6181-4541,50-41,1546-888),
 ('2025Q1',3623,978,.94,.95,983,1359,-56,1560,4,245),
 ('2025Q2',3744,862,.83,.82,848,2173,3,1109,6,264),
 ('2025Q3',3704,813,.78,.77,805,1920,12,1255,2,249),
 ('2025Q4',4168,959,.92,.98,1018,7346-5452,-185+41,5270-3924,16-12,1051-758),
 ('2026Q1',3861,899,.86,.99,1031,2603,168,1070,4,233),
 ('2026Q2',3957,987,.95,.94,984,2217,-2,889,5,229),
 ('2026Q3',4030,1026,.98,.94,983,1782,-122,1194,5,213)]
quarters=[]
for z in source_quarters:
    d=dict(zip(['quarter','revenue','common_net','eps','comp_eps','comp_common_net','cfo_total','cfo_discontinued','core_capex','development','jv_contribution'],z));d['cfo_cont']=d['cfo_total']-d['cfo_discontinued'];d['cash_reinvestment']=d['core_capex']+d['development']+d['jv_contribution'];d['fcf_before_nci_preferred']=d['cfo_cont']-d['cash_reinvestment'];quarters.append(d)
    old=next(x for x in m['quarters'] if x['quarter']==d['quarter'])
    for k,v in d.items():
        if k!='quarter':ck('history_'+d['quarter']+'_'+k,v,old[k])
periods={}
for name,qs in [('2025Q3',quarters[:4]),('2026Q3',quarters[4:])]:
    periods[name]={k:sum(q[k] for q in qs) for k in ['revenue','common_net','eps','comp_eps','comp_common_net','cfo_total','cfo_discontinued','cfo_cont','cash_reinvestment','fcf_before_nci_preferred']}
    for k,v in periods[name].items():ck('TTM_'+name+'_'+k,v,m['ttm'][name][k])
residual=8596-5485-(929+716-414)-(114+84-85)
ck('common_cash_residual',residual,m['ttm']['2026Q3']['common_cash_residual'])
# Additional V2 corrections checked separately from historical reported values.
for key,independent in {
'cgl_one_off_cash':199,
'cfo_cont_less_cgl_one_off':8596-199,
'fcf_before_nci_preferred_less_cgl_one_off':3111-199,
'common_cash_residual_less_cgl_one_off':1767-199,
'common_dividend_cash_coverage_less_cgl_one_off':(1767-199)/3597,
'third_party_settlement_cash_net_of_tax':78,
'common_cash_residual_illustrative_ex_cgl_plus_settlement':1767-199+78,
'illustrative_cash_coverage_ex_cgl_plus_settlement':(1767-199+78)/3597,
}.items(): ck('V2_'+key,independent,m['ttm']['2026Q3'][key])
ck('V2_dividends_payable',933,m['bridge']['declared_dividends_payable'])
ck('V2_accrued_interest',904,m['bridge']['accrued_interest_payable'])
fx=1.3961;shares=1042
illustrations={'unit_CAD1bn_USD_per_share':1000/(fx*shares),'NCI_30pct_USD_per_share':9773*.3/(fx*shares),'lease_15pct_USD_per_share':9366*.15/(fx*shares),'debt_fair_value_difference_USD_per_share':(60254-58471)/(fx*shares),'stub_250_USD_per_share':250/(fx*shares),'omitted_dividends_payable_USD_per_share':933/(fx*shares),'accrued_interest_USD_per_share':904/(fx*shares),'zero_NCI_base_USD':values['base']['value_usd']+9773/(fx*shares),'price_gap_equity_CADm':(64.38-values['base']['value_usd'])*fx*shares,'coverage_residual':residual/3597,'coverage_pre_NCI_pref':3111/3597,'growth_comparable_eps':3.85/3.59-1,'growth_comparable_income':4016/3730-1,'CFO_growth':8596/7631-1,'PE_comparable':64.38*fx/3.85,'dividend_yield':3.51/(64.38*fx),'core_anchor_sales_margin_vs_claim':15070*.425-6410}
# Public delivery: sources.json marks omitted PDFs as external provenance; only bundled sources are re-hashed here.
source_hashes=[]
for s in json.loads((SOURCE/'sources.json').read_text()):
    if 'local' in s and 'sha256' in s:
        actual=hashlib.sha256((SOURCE/s['local']).read_bytes()).hexdigest()
        source_hashes.append({'id':s['id'],'file':s['local'],'expected':s['sha256'],'actual':actual,'pass':actual==s['sha256']})
raw=json.loads((SOURCE/'price_history.json').read_text())['chart']['result'][0]
price_meta={'symbol':raw['meta']['symbol'],'currency':raw['meta']['currency'],'exchange':raw['meta']['fullExchangeName'],'raw_price':raw['meta']['regularMarketPrice'],'raw_price_time':datetime.datetime.fromtimestamp(raw['meta']['regularMarketTime'],datetime.timezone.utc).isoformat(),'analytical_price_64_38':'stated in sources.json; raw quote response not retained in this package'}
prices=json.loads((SOURCE/'daily_prices.json').read_text());daily=[r for r in prices if r['date'][:10]<='2026-11-04']
ema={}
for period in [20,50,200]:
    series=[]
    for p in daily:
        series.append(p['close'] if not series else series[-1]+2/(period+1)*(p['close']-series[-1]))
    ema[str(period)]={'last':series[-1],'ten_before':series[-11],'twenty_before':series[-21]}
tech={'last_date':daily[-1]['date'],'close':daily[-1]['close'],'high252':max(r['high'] for r in daily[-252:]),'avg_volume20':sum(r['volume'] for r in daily[-20:])/20,'ema':ema};tech['pullback']=1-tech['close']/tech['high252']
output={'method':'Independent reviewer script. No import or execution of author model.py. No modification to reviewed files.','scenario_summaries':{n:{k:v for k,v in r.items() if k!='rows'} for n,r in values.items()},'check_count':len(checks),'failed_checks':[x for x in checks if not x['pass']],'maximum_abs_difference':max(abs(x['difference']) for x in checks),'checks':checks,'source_hashes':source_hashes,'annual':annual,'quarters':quarters,'ttm':periods,'reverse':roots,'illustrative_audit_sensitivities':illustrations,'price_source':price_meta,'technicals':tech}
(DEST/'independent_recalculation_v2_1.json').write_text(json.dumps(output,indent=2))
print(json.dumps({k:output[k] for k in ['scenario_summaries','check_count','failed_checks','maximum_abs_difference','reverse','illustrative_audit_sensitivities','price_source','technicals']},indent=2))
