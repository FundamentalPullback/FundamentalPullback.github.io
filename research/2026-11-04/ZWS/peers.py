from pathlib import Path
import json
from build_financials import row
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));z=dict(f['ttm'][-1]);z.update(price=44.12,shares=168.105)
a={}
for key,label in [('revenue','Net sales'),('net_income','Net Earnings')]:
 av=row('aos_k_table_21.txt',label,3);q=row('aos_q_table_7.txt',label,4);a[key]=av[0]+q[2]-q[3]
for key,kl,ql in [('cfo','Cash Provided by Operating Activities','Cash Provided by Operating Activities'),('capex','Capital expenditures','Capital expenditures'),('sbc','Stock based compensation expense','Share-based compensation expense')]:
 av=row('aos_k_table_23.txt',kl,3);q=row('aos_q_table_10.txt',ql,2);a[key]=(abs(av[0])+abs(q[0])-abs(q[1])) if key=='capex' else av[0]+q[0]-q[1]
a.update(price=63.84,shares=row('aos_q_table_18.txt','Denominator for diluted earnings per share',4)[0]/1e6)
a['fcf']=a['cfo']-a['capex'];a['fcf_less_sbc']=a['fcf']-a['sbc']
for d in [z,a]:
 d['equity_proxy']=d['price']*d['shares'];d['pe']=d['equity_proxy']/d['net_income'];d['p_fcf']=d['equity_proxy']/d['fcf'];d['p_fcf_less_sbc']=d['equity_proxy']/d['fcf_less_sbc']
z['tariff_normalized_cash_proxy']=z['fcf_less_sbc']-40.4;z['p_tariff_normalized_cash_proxy']=z['equity_proxy']/z['tariff_normalized_cash_proxy']
out=dict(period='Both TTM September2026, USD, USGAAP; Nov3 regular close; Q3 diluted shares proxy, not actual spot share counts.',ZWS=z,AOS=a,limitations='AOS China81% sale announcedOct27 not closed inSeptember and futureQ4 discontinued reclassification expected: no proforma proceeds or earnings strip performed. ZWS net income continuing, consolidated CFO contains undisaggregated discontinued cash; AOS reported includesChina. Reported metrics not economically normalized identically. Tariff refund cash normalization shown separately only forZWS. Peer contrast, no target multiple.')
json.dump(out,open(P/'peers.json','w'),indent=2);print(json.dumps(out,indent=2))
