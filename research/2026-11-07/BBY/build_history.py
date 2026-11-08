import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
fields={'revenue':'Revenue','ebit':'Operating income','ni':'Net earnings','da':'Depreciation and amortization','sbc':'Stock-based compensation','cfo':'Total cash provided by operating activities','capex':'Additions to property and equipment','restructuring':'Restructuring charges','impairment':'Goodwill and intangible asset impairments','inventory_cash':'Merchandise inventories','payable_cash':'Accounts payable'}
def row(file,label,last=False):
 a=[r for r in json.loads((P/'financial_source_inputs.json').read_text())[file] if r.startswith(label+' | ')]
 if not a:return [0]*4
 r=a[-1] if last else a[0]
 out=[]
 for v in r.split(' | ')[1:]:
  if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|-',v):out.append(0 if v=='-' else float(v.replace(',','').replace('(','-').replace(')','')))
 return out
annual={};files={}
for year,i in [(2026,0),(2025,1),(2024,2)]:
 annual[str(year)]={k:row('bby-20260131.htm.rows',v)[i] for k,v in fields.items() if k not in ['inventory_cash','payable_cash']};annual[str(year)]['capex']=abs(annual[str(year)]['capex'])
periods={}
for key,file,n in [('q326','bby-20251101.htm.rows',4),('q127','bby-20260502.htm.rows',2),('h127','bby-20260801.htm.rows',4)]:
 d={}
 for k,v in fields.items():
  if k in ['inventory_cash','payable_cash']:continue
  try:a=row(file,v)
  except IndexError:a=[0]*n
  # Income statements have quarter+prior then YTD+prior in Q2/Q3; cashflow first occurrence YTD only.
  idx=2 if n==4 and k in ['revenue','ebit','ni','restructuring','impairment'] else 0
  d[k]=[a[idx],a[idx+1]]
  if k=='capex':d[k]=list(map(abs,d[k]))
 periods[key]=d
quarters={}
for yr,idx in [(2026,0),(2025,1)]:
 f='bby-20251101.htm.rows';quarters['Q3FY'+str(yr)]={k:row(f,v)[idx] for k,v in fields.items() if k in ['revenue','ebit','ni','restructuring','impairment']}
 # cash Q3=9m minus6m
 f2='bby-20250802.htm.rows'
 for k in ['cfo','capex','da','sbc']:
  a=row(f,fields[k])[idx];b=row(f2,fields[k])[idx];quarters['Q3FY'+str(yr)][k]=abs(a-b) if k=='capex' else a-b
quarters['Q4FY2026']={k:annual['2026'][k]-periods['q326'][k][0] for k in annual['2026']}
quarters['Q1FY2027']={k:v[0] for k,v in periods['q127'].items()}
quarters['Q2FY2027']={k:v[0]-periods['q127'][k][0] for k,v in periods['h127'].items()}
ttm={}
for year,idx in [(2026,0),(2025,1)]:
 ttm[str(year)]={k:annual[str(year)][k]+v[idx]-row('bby-20250802.htm.rows',fields[k])[2+idx if k in ['revenue','ebit','ni','restructuring','impairment'] else idx] for k,v in periods['h127'].items() if k!='capex'}
 ttm[str(year)]['capex']=annual[str(year)]['capex']+periods['h127']['capex'][idx]-abs(row('bby-20250802.htm.rows',fields['capex'])[idx])
 # 2025 TTM =FY2025+H1FY26-H1FY25, not H1FY26 twice
 if idx==1:
  for k in ttm[str(year)]:
   a=row('bby-20250802.htm.rows',fields[k]);j=2 if k in ['revenue','ebit','ni','restructuring','impairment'] else 0
   ttm[str(year)][k]=annual[str(year)][k]+(abs(a[j])-abs(a[j+1]) if k=='capex' else a[j]-a[j+1])
 for key in ['cash_after_capex','cash_after_capex_sbc']:ttm[str(year)][key]=ttm[str(year)]['cfo']-ttm[str(year)]['capex']-(ttm[str(year)]['sbc'] if key.endswith('sbc') else 0)
h=dict(units='USD millions; fiscal year ends Jan/Feb',annual=annual,quarters=quarters,interims=periods,paired_ttm_august=ttm,method='Annual 10K comparative audited columns. Q4=FY-9M; Q2=H1-Q1. TTM=FY+currentH1-priorH1. No Q3FY27 actuals before Nov24.')
(P/'history.json').write_text(json.dumps(h,indent=2)+'\n');print(json.dumps(ttm,indent=2))
