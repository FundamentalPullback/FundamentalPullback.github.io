import pathlib,re,json,csv
P=pathlib.Path(__file__).parent
def rows(glob):return json.loads((P/'financial_source_inputs.json').read_text())[glob]['rows']
def vals(rr,label,minv=0):
 for line in rr:
  if line.split(' | ')[0] in label:
   a=[]
   for x in line.split(' | ')[1:]:
    if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',x):
     a.append(0. if x=='—' else float(x.replace(',','').replace('(','-').replace(')','')))
   if a and max(abs(x) for x in a)>=minv:return a
 raise ValueError(label)
labels={'rev':['Revenue'],'ebit':['Income (loss) from operations','Income from operations','(Loss) income from operations'],'ni':['Net income (loss)','Net income','Net (loss) income'],'da':['Depreciation and amortization'],'sbc':['Stock-based compensation expense'],'cfo':['Net cash provided by operating activities','Net cash used in operating activities','Net cash provided by (used in) operating activities'],'software':['Capitalization of internally developed software'],'ppe':['Purchases of property and equipment']}
fy=rows('2026-02*.rows');q3=rows('2026-11*.rows');q1=rows('2026-05*.rows');q2=rows('2026-08*.rows');prev=rows('2025-11*.rows')
hist={}
for yr,i in [(2025,0),(2024,1),(2023,2)]:hist[str(yr)]={k:vals(fy,l,1000 if k not in ['ppe','software'] else 0)[i]/1000 for k,l in labels.items()}
for per,rr,col in [('9M2026',q3,2),('9M2025',q3,3),('9M2024',prev,3),('Q12026',q1,0),('H12026',q2,2)]:
 hist[per]={k:vals(rr,l,1000 if k not in ['ppe','software'] else 0)[col if k in ['rev','ebit','ni'] else (1 if per in ['9M2025','9M2024'] else 0)]/1000 for k,l in labels.items()}
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:hist[per]={k:hist[a][k]-hist[b][k] for k in labels}
for yr in [2025,2026]:hist['TTM'+str(yr)]={k:hist[str(yr-1)][k]+hist['9M'+str(yr)][k]-hist['9M'+str(yr-1)][k] for k in labels}
# Changes from operating cash-flow statement, not simple balance deltas (FX/acquisition differ).
settles={'2025':-63.716+91.838,'2024':23.335+7.361,'2023':-53.151+82.301,'9M2026':-1.542+27.167,'9M2025':-42.686+83.343,'9M2024':-16.383+82.884}
for yr in [2025,2026]:settles['TTM'+str(yr)]=settles[str(yr-1)]+settles['9M'+str(yr)]-settles['9M'+str(yr-1)]
for per,r in hist.items():
 r['capex']=-(r['software']+r['ppe']);r['reported_cfo_less_capex']=r['cfo']-r['capex']
 r['settlement_flow']=settles.get(per)
 r['cash_less_capex_settlement']=r['reported_cfo_less_capex']-settles[per] if per in settles else None
 r['cash_less_capex_settlement_sbc']=r['cash_less_capex_settlement']-r['sbc'] if per in settles else None
(P/'history.json').write_text(json.dumps(hist,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(hist.values()))));w.writeheader()
 for per,r in hist.items():w.writerow({'period':per}|r)
print(json.dumps(hist,indent=2))
