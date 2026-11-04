from pathlib import Path
import re,json
P=Path(__file__).parent;S=P/'sources'
def row(file,label):
 lines=(S/file).read_text().splitlines();line=next(l for l in lines if l.split(' | ')[0]==label)
 vals=[v.strip() for v in line.split('|')[1:]]
 return [float(v.replace(',','').replace('(','-').replace(')',''))/1000 for v in vals if re.match(r'^\(?[\d,]+(?:\.\d+)?\)?$',v)]
labels={'revenue':'Total revenue','ebit':'Income from operations','net_income':'Net income','cfo':'Net cash provided by operating activities','capex':'Purchases of property, plant and equipment','da':'Depreciation and amortization','sbc':'Stock-based compensation'}
def get(pl,cf,i,j):
 d={k:row(pl if k in ['revenue','ebit','net_income'] else cf,v)[i if k in ['revenue','ebit','net_income'] else j] for k,v in labels.items()};d['capex']=abs(d['capex']);return d
def add(a,b,sgn=1):return {k:a[k]+sgn*b[k] for k in labels}
def decorate(d,p):
 return dict(period=p,**d,fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'],ebit_margin=d['ebit']/d['revenue'])
fy=[get('k25_table_40.txt','k25_table_43.txt',i,i) for i in [2,1,0]]
nine26=get('q10_table_9.txt','q10_table_13.txt',2,0);nine25=get('q10_table_9.txt','q10_table_13.txt',3,1);nine24=get('priorq3_table_9.txt','priorq3_table_13.txt',3,1)
half26=get('q2_table_9.txt','q2_table_13.txt',2,0)
# Q1 cash table index differs inspect below
q1=get('q1_table_9.txt','q1_table_12.txt',0,0)
quarters=[add(fy[2],nine25,-1),q1,add(half26,q1,-1),add(nine26,half26,-1)]
ttm=[add(add(fy[1],nine25),nine24,-1),add(add(fy[2],nine26),nine25,-1)]
out=dict(units='USD millions',annual=[decorate(d,p) for d,p in zip(fy,['FY2023','FY2024','FY2025'])],quarters=[decorate(d,p) for d,p in zip(quarters,['Q42025','Q12026','Q22026','Q32026'])],ttm=[decorate(d,p) for d,p in zip(ttm,['TTM Sep2025','TTM Sep2026'])],source_tables='SEC 10K2025 plus 10Q Sep2025, Mar/Jun/Sep2026; quarterly flows derived from cumulative periods')
for group,values in [('annual',[3.82,3.85,4.06]),('quarters',[1.42,1.23,1.33,1.05]),('ttm',[3.88,5.03])]:
 for d,v in zip(out[group],values):d['diluted_eps']=v
out['eps_note']='Quarterly EPS from issuer; Q4 and TTM sum/difference approximations, not division by a single weighted share count.'
json.dump(out,open(P/'financials.json','w'),indent=2)
print(json.dumps(out,indent=2))
