from pathlib import Path
import json,csv,re
P=Path(__file__).resolve().parents[1];S=P/'sources_private';H=P/'history'
labels=['Organic revenue growth rate','Adjusted EBITDAC','Adjusted net income','Adjusted diluted earnings per share']
inputs=json.load(open(H/'kpi_inputs.json'));rows=inputs['rows'];sources=inputs['sources']
out={}
for label in labels:
 a=rows['ryan-20251231.html'][label];out[label]={'FY2025':a[0],'FY2024':a[1],'FY2023':a[2]}
 for q,end in [(1,'0331'),(2,'0630'),(3,'0930')]:
  a=rows[f'ryan-2026{end}.html'][label]
  # Summary has change columns: 2026,2025,$change,%change,2026YTD,2025YTD,$change,%change; ratios/EPS no changes.
  if label in ['Adjusted EBITDAC','Adjusted net income']:
   out[label][f'Q{q} 2026']=a[0]/1000;out[label][f'2026YTD{q}']=a[4]/1000 if len(a)>4 else a[0]/1000
  else:out[label][f'Q{q} 2026']=a[0]
 if label in ['Adjusted EBITDAC','Adjusted net income']:
  for y in [2023,2024,2025]:out[label][f'FY{y}']/=1000
  prior9=rows['ryan-20260930.html'][label][5]/1000
  out[label]['Q4 2025']=out[label]['FY2025']-prior9
  out[label]['TTM Q3 2026']=out[label]['Q4 2025']+out[label]['2026YTD3']
  # 2025 Q3 filing comparison with current/prior9 for priorTTM
  a=rows['ryan-20250930.html'][label]
  out[label]['TTM Q3 2025']=out[label]['FY2024']+a[4]/1000-a[5]/1000
out['Organic revenue growth rate']['Q4 2025']=inputs['q4_organic']
out['Adjusted diluted earnings per share']['Q4 2025']=inputs['q4_adjusted_eps']
(H/'reported_kpis.json').write_text(json.dumps({'values':out,'source_table_index':sources,'notes':'Adjusted EBITDAC/net income in USD millions; EPS USD; organic growth percent. Q4=FY−9M; TTM=FYprior+9Mcurrent−9Mprior. Do not sum quarterly EPS or organic percentages.'},indent=2))
print(json.dumps(out,indent=2))
