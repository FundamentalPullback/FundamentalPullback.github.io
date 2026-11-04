from pathlib import Path
import re,json
P=Path(__file__).parent;S=P/'sources'
def row(file,label):
 line=next(l for l in (S/file).read_text().splitlines() if l.split(' | ')[0]==label)
 vals=[v.strip() for v in line.split('|')[1:]]
 return [0.0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')','')) for v in vals if v=='—' or re.match(r'^\(?[\d,]+(?:\.\d+)?\)?$',v)]
keys=['revenue','ebit','net_income','eps','cfo','capex','da','sbc']
def annual(i):
 pl='k25_table_37.txt';cf='k25_table_40.txt'
 return dict(revenue=row(pl,'Net revenues')[i],ebit=row(pl,'Operating income')[i],net_income=row(pl,'Net earnings attributable to Allegion plc')[i],eps=row(pl,'Diluted net earnings:')[i],cfo=row(cf,'Net cash provided by operating activities')[i],capex=abs(row(cf,'Capital expenditures')[i]),da=row(cf,'Depreciation and amortization')[i],sbc=row(cf,'Share-based compensation')[i])
def interim(k,i,j,sbcfile):
 pl=k+'_table_6.txt';cf=k+'_table_8.txt'
 return dict(revenue=row(pl,'Net revenues')[i],ebit=row(pl,'Operating income')[i],net_income=row(pl,'Net earnings')[i],eps=row(pl,'Diluted net earnings')[i],cfo=row(cf,'Net cash provided by operating activities')[j],capex=abs(row(cf,'Capital expenditures')[j]),da=row(cf,'Depreciation and amortization')[j],sbc=row(sbcfile,'Pre-tax expense')[i])
def plus(a,b,sign=1):return {k:a[k]+sign*b[k] for k in keys}
def finish(d,p):return dict(period=p,**d,fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'],ebit_margin=d['ebit']/d['revenue'])
fy=[annual(i) for i in [2,1,0]];n26=interim('q10',2,0,'q10_table_28.txt');n25=interim('q10',3,1,'q10_table_28.txt');n24=interim('priorq3',3,1,'priorq3_table_30.txt');h26=interim('q2',2,0,'q2_table_24.txt');q1=interim('q1',0,0,'q1_table_24.txt')
qs=[plus(fy[2],n25,-1),q1,plus(h26,q1,-1),plus(n26,h26,-1)];ttm=[plus(plus(fy[1],n25),n24,-1),plus(plus(fy[2],n26),n25,-1)]
f=dict(units='USD millions except EPS',annual=[finish(d,n) for d,n in zip(fy,['FY2023','FY2024','FY2025'])],quarters=[finish(d,n) for d,n in zip(qs,['Q42025','Q12026','Q22026','Q32026'])],ttm=[finish(d,n) for d,n in zip(ttm,['TTM Sep2025','TTM Sep2026'])],note='Q4, Q2/Q3 cash flows and TTM derived from cumulative reports. EPS sums/differences approximate whole-period weighted-share calculation. FY2023 net attributable540.4 versus total540.6; other periods no material minority interest.')
json.dump(f,open(P/'financials.json','w'),indent=2);print(json.dumps(f,indent=2))
