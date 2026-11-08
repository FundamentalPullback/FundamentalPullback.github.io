import pathlib,re,json,csv
P=pathlib.Path(__file__).parent
labels={'revenue':'Total revenue, net','ebit':['Operating income (loss)','Operating income','Operating loss'],'pretax':['Income (loss) before income taxes','Income before income taxes','Loss before income taxes'],'net':['Net income (loss)','Net income','Net loss'],'cfo':'Net cash provided by operating activities','capex':'Additions to property, equipment and software','sbc':'Stock-based compensation','warrants':'Commercial agreement warrant expense','da':'Depreciation and amortization','provision':'Provision for losses','loan_originations':'Purchases and origination of loans held for investment','loan_sales':'Proceeds from the sale of loans held for investment','loan_repayments':'Principal repayments and other loan servicing activity','capitalized_sbc':'Stock-based compensation included in capitalized internal-use software'}
def data(file):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[file];out={}
 for key,labs in labels.items():
  if isinstance(labs,str):labs=[labs]
  candidates=[r for r in rows if r.split(' | ')[0] in labs]
  if key in ['sbc']:
   candidates=[r for r in candidates if len([x for x in r.split(' | ')[1:] if x not in ['$','—','']])<=3]
  if key in ['net','sbc']:candidates=[r for r in candidates if '—' not in r]
  if not candidates: print(file,key,'MISSING');continue
  r=max(candidates,key=lambda r:sum(bool(re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?',c)) for c in r.split(' | ')[1:]));
  if key in ['revenue','ebit','pretax','net']:r=candidates[0]
  vals=[]
  for c in r.split(' | ')[1:]:
   if c=='—':vals.append(0.0)
   elif re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?',c): vals.append(float(c.replace(',','').replace('(','-').replace(')',''))/1000)
  out[key]=vals
 return out
annual=data('2026-08-27_afrm-20260630.htm.rows');h={}
for i,y in enumerate([2026,2025,2024]):h['FY'+str(y)]={k:v[i] for k,v in annual.items()}
for name,file in [('Q1FY27','2026-11-05_afrm-20260930.htm.rows'),('Q1FY26','2025-11-06_afrm-20250930.htm.rows'),('H1FY26','2026-02-05_afrm-20251231.htm.rows'),('9MFY26','2026-05-07_afrm-20260331.htm.rows')]:
 d=data(file);h[name]={k:v[0] for k,v in d.items()}
 # income statement first column is quarter, cash flow first is YTD; normalize to YTD via quarter income sum later
 if name=='H1FY26':h['Q2FY26']={k:v[0] for k,v in d.items()}
 if name=='9MFY26':h['Q3FY26']={k:v[0] for k,v in d.items()}
# Income statement YTD from second pair columns; extract four value rows (Q current/prior,YTD current/prior)
for name,file in [('H1FY26','2026-02-05_afrm-20251231.htm.rows'),('9MFY26','2026-05-07_afrm-20260331.htm.rows')]:
 d=data(file)
 for k in ['revenue','ebit','pretax','net']:h[name][k]=d[k][2]
for q,ytd,prior in [('Q2FY26','H1FY26','Q1FY26'),('Q3FY26','9MFY26','H1FY26')]:
 h[q]={k:h[ytd][k]-h[prior][k] for k in h[ytd]}
h['Q4FY26']={k:h['FY2026'][k]-h['9MFY26'][k] for k in h['FY2026']}
# paired TTM previous Q1 from current comparative
old=data('2025-11-06_afrm-20250930.htm.rows');h['Q1FY25']={k:v[1] for k,v in old.items()}
for name,fy,now,prev in [('TTM2026','FY2026','Q1FY27','Q1FY26'),('TTM2025','FY2025','Q1FY26','Q1FY25')]:h[name]={k:h[fy][k]+h[now][k]-h[prev][k] for k in h[fy]}
for row in h.values():
 row['cfo_less_capex']=row['cfo']+row['capex'];row['net_loan_investment']=row['loan_originations']+row['loan_sales']+row['loan_repayments']
(P/'history.json').write_text(json.dumps(h,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2026']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(json.dumps(h,indent=2))
