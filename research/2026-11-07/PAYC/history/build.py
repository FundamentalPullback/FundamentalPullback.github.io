from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;x=json.loads((P/'inputs.json').read_text())
MAP={'revenue':('income','Total revenues'),'recurring':('income','Recurring and other'),'float_interest':('income','Interest on funds held for clients'),'ebit':('income','Operating income'),'net_income':('income','Net income'),'tax':('income','Provision for income taxes'),'rnd_expense':('income','Research and development'),'cfo':('cash','Net cash provided by operating activities'),'ppe_cash':('cash','Purchases of property and equipment'),'da':('cash','Depreciation and amortization'),'sbc_expense':('cash','Stock-based compensation expense'),'tax_working_capital':('cash','Income taxes, net'),'contract_net_cf':('cash','Deferred contract costs')}
def period(src,inc,cf):
 d={}
 for k,(t,l) in MAP.items():d[k]=x[src][t][l]['values'][inc if t=='income' else cf]
 d['ppe_cash']=-d['ppe_cash'];return d
def combine(a,b,op=1):return {k:round(a[k]+op*b[k],4)for k in MAP}
h={f'FY{2025-i}':period('fy25',i,i)for i in range(3)}
h['9M2026']=period('q3',2,0);h['9M2025']=period('q3',3,1);h['9M2024']=period('q3prior',3,1)
h['Q42025']=combine(h['FY2025'],h['9M2025'],-1)
h['Q12026']=period('q1',0,0);h['H12026']=period('q2',2,0)
h['Q22026']=combine(h['H12026'],h['Q12026'],-1);h['Q32026']=combine(h['9M2026'],h['H12026'],-1)
h['TTM2026']=combine(combine(h['FY2025'],h['9M2026']),h['9M2025'],-1)
h['TTM2025']=combine(combine(h['FY2024'],h['9M2025']),h['9M2024'],-1)
for name,d in h.items():
 d['cfo_less_ppe']=round(d['cfo']-d['ppe_cash'],4)
 d['ebit_margin']=d['ebit']/d['revenue'];d['ebit_ex_known_2024_award_reversal']=round(d['ebit']-(117.5 if name in ['FY2024','9M2024']else 0),4)
 d['cfo_less_ppe_and_reported_sbc']=round(d['cfo_less_ppe']-d['sbc_expense'],4)
 d['basis']='Quarter/TTM additive flows derived from cumulative reported figures; 0.1m rounding differences possible. CFO less PPE excludes separately reported intangible purchases and is not normalized owner FCF.'
checks=[]
for name,d in h.items():
 checks += [abs(d['revenue']-d['recurring']-d['float_interest'])<=0.15,abs(d['cfo_less_ppe']-d['cfo']+d['ppe_cash'])<1e-6]
for k in MAP:checks.append(abs(sum(h[q][k]for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][k])<1e-6)
assert all(checks)
(P/'periods.json').write_text(json.dumps(h,indent=2)+'\n')
with (P/'history.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values()))));w.writeheader();w.writerows({'period':k,**v}for k,v in h.items())
(P/'qa.json').write_text(json.dumps({'checks':len(checks),'pass':all(checks),'known_rounding':'Derived Q1/Q2 net income may differ0.1 from individually reported figures; use additive source consistently.'},indent=2)+'\n')
print(json.dumps({k:h[k]for k in ['TTM2026','TTM2025']},indent=2))
