import pathlib,re,json,csv
p=pathlib.Path(__file__).parent
def rows(n):return json.loads((p/'financial_source_inputs.json').read_text())[n]
def numbers(s):
 # Separate closing parentheses in issuer tables are joined before parsing.
 a=s.replace(' | )',')').split(' | ')
 return [0 if x in ['—','-'] else float(x.replace(',','').replace('(','-').replace(')',''))/1000 for x in a[1:] if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—|-',x)]
def get(r,label,n):
 for s in r:
  if s.split(' | ')[0].replace('\u200b','').strip()==label:
   a=numbers(s)
   if len(a)>=n:return a[-n:]
 raise ValueError(label)
L={'revenue':'Total net revenues','ebit':'Operating income','net_parent':'Net income attributable to the Company’s ordinary shareholders','cfo':'Net cash provided by operating activities','sbc':'Share-based compensation expenses'}
fy=rows('2026-03-27_lk-20251231x20f.htm.rows');r3=rows('release.htm.rows');r2=rows('tm2621683d1_ex99-1.htm.rows');r1=rows('tm2612798d1_ex99-1.htm.rows');h={}
for y,c in [(2023,0),(2024,1),(2025,2)]:h[str(y)]={k:get(fy,l,4)[c] for k,l in L.items()};h[str(y)]['cash_capex']=-get(fy,'Purchases of property and equipment',4)[c]
for per,r,c,n in [('9M2026',r3,4,6),('9M2025',r3,3,6),('H12026',r2,4,6),('Q12026',r1,1,3)]:h[per]={k:get(r,l,n)[c] for k,l in L.items()};h[per]['cash_capex']=None
# Restated comparison from issuer Q3 2025 release, page9 & cash-flow page.
h['9M2024']={'revenue':24861.537,'ebit':2562.311,'net_parent':None,'cfo':2600.897,'sbc':268.188,'cash_capex':None}
t=json.loads((p/'financial_source_inputs.json').read_text())['prior_release_net_income_excerpt'];ls=t.splitlines()
for i,s in enumerate(ls):
 if s.startswith('Net income attributable to the Company’s') and i+1<len(ls):
  ns=re.findall(r'\(?[\d,]+\)?',ls[i+1])
  if len(ns)==6:h['9M2024']['net_parent']=float(ns[3].replace(',',''))/1000;break
assert h['9M2024']['net_parent'] is not None
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:h[per]={k:h[a][k]-h[b][k] for k in L};h[per]['cash_capex']=None
for y in [2025,2026]:h['TTM'+str(y)]={k:h[str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in L};h['TTM'+str(y)]['cash_capex']=None
(p/'history.json').write_text(json.dumps(h,indent=2))
with (p/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['2025']));w.writeheader()
 for k,v in h.items():w.writerow({'period':k}|v)
print(json.dumps(h,indent=2))
