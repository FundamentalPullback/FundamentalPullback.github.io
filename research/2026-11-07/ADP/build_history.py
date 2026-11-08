import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
labels={'revenue':'TOTAL REVENUES','client_interest':'Interest on funds held for clients','net_income':'NET EARNINGS','pbt':'EARNINGS BEFORE INCOME TAXES','interest_expense':'Interest expense','rd':'Research and development','sga':'Selling, general, and administrative expenses'}
cf={'cfo':'Net cash flows provided by operating activities','da':'Depreciation and amortization','contract_amort':'Amortization of deferred contract costs','sbc':'Stock-based compensation expense','contract_spend':'Increase in deferred contract costs','capex':'Capital expenditures','intangible_spend':'Additions to intangibles'}
def nums(line):
 a=[]
 for x in line.split(' | ')[1:]:
  x=x.strip().replace(',','')
  if re.fullmatch(r'\(?-?\d+(\.\d+)?\)?',x):a.append(float(x.strip('()'))*(-1 if '(' in x else 1))
  elif x=='—':a.append(0.)
 return a
def parse(date):
 s=json.loads((P/'financial_source_inputs.json').read_text())[date];inc=s.split('Cash Flows from Operating Activities:')[0];cash=s.split('Cash Flows from Operating Activities:')[-1]
 if date=='20260630':inc=inc.split('Years ended June 30, | 2026 | 2025 | 2024')[1]
 def find(text,label):return nums(next(l for l in text.splitlines() if l.startswith(label+' | ')))
 return {k:find(inc,v) for k,v in labels.items()}|{k:find(cash,v) for k,v in cf.items()}
r=parse('20260630');annual={str(y):{k:v[i] for k,v in r.items()} for i,y in enumerate([2026,2025,2024])}
q={};cumulative={}
for date in ['20240930','20241231','20250331','20250930','20251231','20260331','20260930']:
 z=parse(date);cumulative[date]={k:v[0 if k in cf or len(v)==2 else 2] for k,v in z.items()};q[date]={k:v[0] for k,v in z.items()}
for yr in [2025,2026]:
 for mo,prev in [('1231',f'{yr-1}0930'),('0331',f'{yr-1}1231')]:
  date=f'{yr-1}1231' if mo=='1231' else f'{yr}0331'
  for k in cf:q[date][k]=cumulative[date][k]-cumulative[prev][k]
 q[f'{yr}0630']={k:annual[str(yr)][k]-cumulative[f'{yr}0331'][k] for k in labels|cf}
ttm={str(yr):{k:annual[str(yr)][k]+q[f'{yr}0930'][k]-q[f'{yr-1}0930'][k] for k in labels|cf} for yr in [2025,2026]}
for block in [annual,q,ttm]:
 for v in block.values():v['cash_after_physical_software_sbc']=v['cfo']+v['capex']+v['intangible_spend']-v['sbc']
(P/'history.json').write_text(json.dumps({'units':'USD millions; fiscal year ends June30; investment outflows negative','annual':annual,'quarters':q,'paired_ttm_september':ttm},indent=2)+'\n')
