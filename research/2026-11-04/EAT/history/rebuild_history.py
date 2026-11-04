from pathlib import Path
import json,csv
p=Path(__file__).parent;data=json.loads((p/'numeric_inputs.json').read_text());d={x['period']:{'period':x['period'],'start':x['start'],'end':x['end'],**x['values']} for x in data['periods']};keys=list(data['periods'][0]['values']);checks=[]
def sub(n,a,b):
 d[n]={'period':n,'basis':'derived '+a+' minus '+b}
 for k in keys:d[n][k]=None if k=='eps_diluted' or d[a][k] is None or d[b][k] is None else d[a][k]-d[b][k]
for fy in [2025,2026]:
 sub('Q2FY'+str(fy),'H1FY'+str(fy),'Q1FY'+str(fy));sub('Q3FY'+str(fy),'9MFY'+str(fy),'H1FY'+str(fy));sub('Q4FY'+str(fy),'FY'+str(fy),'9MFY'+str(fy))
for fy in [2025,2026]:
 n='TTMSeptember'+str(fy);d[n]={'period':n,'basis':'FY plus latest Q1 minus prior Q1; 52 weeks'}
 for k in keys:d[n][k]=None if k=='eps_diluted' or any(d[a][k] is None for a in ['FY'+str(fy),'Q1FY'+str(fy+1),'Q1FY'+str(fy)]) else d['FY'+str(fy)][k]+d['Q1FY'+str(fy+1)][k]-d['Q1FY'+str(fy)][k]
for n,x in data['direct_quarter_eps'].items():d[n]['eps_diluted']=x['val']
order=['FY2024','FY2025','FY2026']+[f'Q{q}FY{y}' for y in [2025,2026] for q in [2,3,4]]+['Q1FY2026','Q1FY2027','TTMSeptember2025','TTMSeptember2026']
rows=[d[x] for x in order]
for r in rows:
 r['fcf_ppe']=r['cfo']-r['capex_ppe'];r['cash_after_sbc_proxy']=r['fcf_ppe']-r['sbc'];r['owner_fcf']=None
 for k in ['revenue','ebit','ni','cfo','capex_ppe','da','sbc']:assert r[k] is not None,(r['period'],k)
 checks.append({'period':r['period'],'fcf_identity':abs(r['cfo']-r['capex_ppe']-r['fcf_ppe'])<1e-8})
(p/'history.json').write_text(json.dumps({'units':'USD millions except EPS; derived quarterly and TTM EPS null','rows':rows},indent=2)+'\n');(p/'qa.json').write_text(json.dumps(checks,indent=2)+'\n')
with (p/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+keys+['fcf_ppe','cash_after_sbc_proxy','owner_fcf'],extrasaction='ignore');w.writeheader();w.writerows(rows)
print('History',len(rows),'periods all basic identities pass');print(rows[-1])
