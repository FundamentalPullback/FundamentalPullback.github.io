from pathlib import Path
from copy import deepcopy
import json,math
from model import CASES,run,SHARES,CLAIMS,PRICE,main
P=Path(__file__).parent
checks=[]
def ck(name,cond):checks.append({'test':name,'pass':bool(cond)})
def eq(name,a,b):ck(name,abs(a-b)<1e-6*max(1,abs(b)))
m=json.loads((P/'model_results.json').read_text());h=json.loads((P/'history/history.json').read_text());c=json.loads((P/'comps.json').read_text())
for x in json.loads((P/'history/checks.json').read_text()):checks.append(x)
for name,a in CASES.items():
 r=run(a);eq(name+' reproduction',r['value'],m['results'][name]['value']);ck(name+' ten years',len(r['rows'])==10);ck(name+' positive capex',all(x['capex_including_finance_asset_replacement']>0 for x in r['rows']));ck(name+' terminal discount spread',a['wacc']>a['g'])
 rev=22476
 for row in r['rows']:
  year=row['year'];eq(f'{name} year{year} revenue',row['revenue'],rev*(1+a['growth'][year-1]));rev=row['revenue'];eq(f'{name} year{year} EBIT',row['ebit'],rev*a['margins'][year-1]);eq(f'{name} year{year} tax',row['nopat'],(row['ebit']-row['other_cash_pre_tax'])*(1-a['tax']));eq(f'{name} year{year} FCFF',row['fcff'],row['nopat']+row['da']-row['capex_including_finance_asset_replacement']-row['delta_wc']);eq(f'{name} year{year} PV',row['pv_fcff'],row['fcff']/(1+a['wacc'])**year)
 eq(name+' terminal reinvest',r['terminal_reinvestment'],r['terminal_nopat']*a['g']/a['roic']);eq(name+' terminal FCFF',r['terminal_fcff'],r['terminal_nopat']-r['terminal_reinvestment']);eq(name+' EV',r['ev'],sum(x['pv_fcff']for x in r['rows'])+r['terminal_value']/(1+a['wacc'])**10);eq(name+' price',r['value'],(r['ev']-CLAIMS)/SHARES)
 for key,chg in [('wacc',.005),('tax',.01)]:
  z=deepcopy(a);z[key]+=chg;ck(name+' monotonic '+key,run(z)['value']<r['value'])
 eq(name+' more debt sensitivity',run(a,claims=CLAIMS+100)['value'],r['value']-100/SHARES)
 ck(name+' more shares lower value',run(a,shares=SHARES+5)['value']<r['value'])
for t,d in c['data'].items():
 eq(t+' marketcap',d['equity_value'],d['price']*d['shares']);eq(t+' EV',d['ev'],d['equity_value']+d['debt']+d['extra_finance_leases']+d['nci_book']-d['cash']);eq(t+' EBITDA',d['gaap_ebitda_after_sbc'],d['ebit']+d['da']);eq(t+' FCF',d['fcf_ex_sales'],d['cfo']-d['capex_all'])
ck('Q3 gross FCF not company cash flow',h['Q3_2026']['fcf_ex_asset_sales']==102 and h['Q3_2026']['issuer_fcf_incl_ppe_sales']==156)
ck('Current/prior TTM cash gap',h['TTM_2026_09']['trade_wc_cash']-h['TTM_2025_09']['trade_wc_cash']==-641)
ck('SBC annual sourced not stock plans',[h[f'FY{y}']['sbc_actual']for y in [2023,2024,2025]]==[219,223,213])
ck('quarter SBC flagged estimate',all(h[q]['sbc_actual'] is None for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026']))
ck('lease separate comparable NOV262',c['data']['NOV']['extra_finance_leases']==262)
ck('lease no duplicate WFRD',c['data']['WFRD']['extra_finance_leases']==0 and c['data']['WFRD']['debt']==1480)
(P/'validation.json').write_text(json.dumps({'count':len(checks),'failed':sum(not x['pass']for x in checks),'checks':checks},indent=2))
print('Validation',len(checks),'failed',sum(not x['pass']for x in checks))
assert all(x['pass']for x in checks)
