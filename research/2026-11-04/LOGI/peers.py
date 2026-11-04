from pathlib import Path
import json,re
P=Path(__file__).parent
from build_financials import row,inc,cf
f=json.load(open(P/'financials.json'));a=f['annual'][-1];q=inc('q1_table_4.txt',2);c=cf('q1_table_7.txt',2)
l={k:a[k]+q[0][k]-q[1][k] for k in ['revenue','ebit','net_income']}
for k in c[0]:l[k]=a[k]+c[0][k]-c[1][k]
l.update(price=92.85,shares=145.038)
def nums(file,label,last=False):
 rows=[]
 for line in (P/'sources'/file).read_text().splitlines():
  if line.split('|')[0].strip()!=label:continue
  vals=[]
  for v in line.split('|')[1:]:
   v=v.strip().replace(',','')
   if v=='—':vals.append(0.)
   elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',v):vals.append(float(v.strip('()'))*(-1 if v.startswith('(') else 1)/1000)
  if vals:rows.append(vals)
 return rows[-1 if last else 0]
r=nums('crsr_k_table_20.txt','Net revenue')[0]+nums('crsr_q_table_7.txt','Net revenue')[2]-nums('crsr_q_table_7.txt','Net revenue')[3]
label='Net income (loss) attributable to common stockholders of Corsair Gaming, Inc.'
n=nums('crsr_k_table_20.txt',label)[0]+nums('crsr_q_table_7.txt',label)[2]-nums('crsr_q_table_7.txt',label)[3]
x=dict(revenue=r,net_income=n,price=12.31,shares=nums('crsr_q_table_7.txt','Diluted',True)[0])
for k,label in {'cfo':'Net cash provided by operating activities','capex':'Purchase of property and equipment','sbc':'Stock-based compensation'}.items():
 av=nums('crsr_k_table_24.txt',label)[0];qv=nums('crsr_q_table_14.txt',label);x[k]=(abs(av)+abs(qv[0])-abs(qv[1])) if k=='capex' else av+qv[0]-qv[1]
for d in [l,x]:
 d['market_cap_proxy']=d['price']*d['shares'];d['pe_common']=d['market_cap_proxy']/d['net_income'];d['fcf']=d['cfo']-d['capex'];d['fcf_less_sbc']=d['fcf']-d['sbc'];d['p_consolidated_fcf']=d['market_cap_proxy']/d['fcf'];d['p_consolidated_fcf_less_sbc']=d['market_cap_proxy']/d['fcf_less_sbc']
out=dict(period='TTM June30 2026 for both; prices November3 regular close; June quarterly diluted shares proxy for both, not actual current market cap.',LOGI=l,CRSR=x,limitations='Corsair much smaller, gaming/PC components mix, tariff refunds and NCI participating securities affect comparability. P/E uses income attributable to common. Consolidated cash ratios are reference metrics, not fully allocated common-owner cash; no sector median or target multiple. Q3 Corsair due Nov5 after close, June data will soon be stale.')
json.dump(out,open(P/'peers.json','w'),indent=2);print(json.dumps(out,indent=2))
