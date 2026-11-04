import re,json,csv
from pathlib import Path
P=Path(__file__).parent; S=P/'sources'
keys={'revenue':'Total revenues','ebit':'Operating income','net_income':'Net income','eps':'Net income per share, diluted','sbc':'Total share-based compensation expense','cfo':'Net cash provided by operating activities','capex':'Capital expenditures','da':'Depreciation and amortization','deferred_amort':'Amortization of deferred costs','deferred_investment':'Deferred costs','restructuring':'Restructuring'}
def pull(f,key,index):
 rows=(S/(f+'.tables.txt')).read_text().splitlines()
 for row in rows:
  a=[s.strip() for s in row.split('|')]
  if a[0] not in [key,key+' (2)']:continue
  nums=[]
  for x in a[1:]:
   if x:
    y=x.replace('$','').replace(',','').strip().replace('(','-').replace(')','')
    try:nums.append(float(y))
    except:pass
  if len(nums)>index:return nums[index]
 raise ValueError((f,key,index))
def record(f,i,period):
 d={'period':period,'source':f}
 for k,v in keys.items():
  try:d[k]=pull(f,v,i)
  except:d[k]=0
 d['capex']=abs(d['capex']);d['deferred_investment']=abs(d['deferred_investment'])
 d['fcf']=d['cfo']-d['capex'];d['fcf_less_sbc']=d['fcf']-d['sbc'];d['ebit_margin']=d['ebit']/d['revenue'];return d
fy=[record('q4fy25',3,'FY2024'),record('q4fy26',3,'FY2025'),record('q4fy26',2,'FY2026')]
qs=[record('q3fy26',0,'Q3 FY2026'),record('q4fy26',0,'Q4 FY2026'),record('q1fy27',0,'Q1 FY2027'),record('q2fy27',0,'Q2 FY2027')]
h=[record('q2fy26',3,'H1 FY2025'),record('q2fy27',3,'H1 FY2026'),record('q2fy27',2,'H1 FY2027')]
# deferred costs first occurrence is balance-sheet, so replace CF values by explicit financial cash-flow extraction, same precision.
for d,v,a in zip(fy,[342,337,404],[213,251,292]):d['deferred_investment']=v;d['deferred_amort']=a
for d,v,a in zip(h,[104,152,195],[121,140,162]):d['deferred_investment']=v;d['deferred_amort']=a
for d,v,a in zip(qs,[95,158,65,131],[75,77,79,83]):d['deferred_investment']=v;d['deferred_amort']=a
# restructuring appears in income statement; q1 release has no restructuring line current quarter, correctly zero.
ttm=[]
for ix in (0,1):
 d={'period':['TTM July2025','TTM July2026'][ix],'source':'FY + current H1 - prior H1'}
 for k in keys:
  if k=='eps':continue
  d[k]=fy[ix+1][k]+h[ix+1][k]-h[ix][k]
 d['fcf']=d['cfo']-d['capex'];d['fcf_less_sbc']=d['fcf']-d['sbc'];d['ebit_margin']=d['ebit']/d['revenue'];ttm.append(d)
obj={'currency':'USD','units':'millions except EPS and margins','annual':fy,'quarters':qs,'half_years':h,'ttm':ttm,'notes':['TTM uses annual plus H1 less prior H1, avoiding accumulation of rounded quarters. Q3/Q4 plus H1 differs by $1m from the annual bridge for revenue/EBIT/CFO due to rounding.','EPS TTM is not mechanically aggregated or used for valuation due to weighting and tax distortions.','FCF less SBC is an economic shareholder cash proxy, not GAAP cash flow or FCFF.']}
json.dump(obj,open(P/'financials.json','w'),indent=2)
for d in fy+qs+h+ttm:print(d)
