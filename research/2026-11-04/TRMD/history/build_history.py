from pathlib import Path
import json,csv,hashlib
P=Path(__file__).parent
# USD million. Expenses/capex shown positive; gains/profit/CFO carry reported signs.
fields=['revenue','tce_tanker','ebit','da','net_income','net_income_parent','vessel_sale_gain','cfo','cash_tangible_investment','cash_intangible_investment','asset_sale_proceeds','restricted_cash_change','cfi']
data={
'9M2024':[1253.8,920.1,569.3,139.3,534.1,534.8,38.7,706.1,436.2,.9,112.3,24.9,-299.9],
'FY2023':[1520.4,1083.8,698.6,149.3,648.0,648.3,50.4,805.0,509.7,.6,166.4,-26.7,-370.6],
'FY2024':[1559.2,1134.8,658.8,192.0,611.5,612.5,51.3,826.8,582.4,1.1,130.6,10.8,-442.1],
'FY2025':[1339.5,909.7,356.3,214.5,286.0,285.3,19.0,498.9,308.5,1.8,143.8,13.9,-152.6],
'9M2025':[986.9,658.7,255.9,158.5,199.2,198.5,16.2,363.9,91.8,.8,128.6,8.9,44.9],
'9M2026':[1564.2,1150.9,709.1,181.5,659.8,659.8,18.4,719.9,311.3,2.0,75.6,2.9,-234.8],
'H12025':[644.3,422.2,157.0,105.4,121.6,120.9,14.9,244.4,55.7,.4,95.3,9.3,48.5],
'H12026':[1064.8,798.1,496.4,120.1,460.7,460.7,4.0,455.4,256.9,1.5,29.3,2.9,-226.2],
'Q12025':[329.1,214.0,82.3,53.3,62.9,62.3,9.4,83.1,27.8,.2,63.3,8.1,43.4],
'Q12026':[402.0,286.1,141.3,59.7,122.4,122.4,4.0,135.9,183.2,1.1,29.3,2.4,-152.6],
'Q22025':[315.2,208.2,74.6,52.2,58.7,58.6,5.4,161.4,None,None,None,None,5.1],
'Q22026':[662.8,512.0,355.1,60.5,338.3,338.3,0,319.5,None,None,None,None,-73.6],
'Q32025':[342.6,236.4,99.0,53.1,77.6,77.6,1.3,119.5,None,None,None,None,-3.6],
'Q32026':[499.4,352.8,212.7,61.4,199.1,199.1,14.4,264.5,None,None,None,None,-8.6]}
rows={p:dict(zip(fields,v)) for p,v in data.items()}
lineage={p:{f:('FY25_20F' if p.startswith('FY') else 'Q1_26' if p.startswith('Q1') else 'H1_26' if p.startswith(('Q2','H1')) else 'Q3_26') for f in fields} for p in rows}
def diff(out,a,b,only_missing=False):
 if out not in rows:rows[out]={};lineage[out]={}
 for f in fields:
  if only_missing and rows[out].get(f) is not None:continue
  rows[out][f]=round(rows[a][f]-rows[b][f],1);lineage[out][f]=f'{a}.{f} - {b}.{f}'
for y in [2025,2026]:
 diff(f'Q2{y}',f'H1{y}',f'Q1{y}',True);diff(f'Q3{y}',f'9M{y}',f'H1{y}',True)
diff('Q42025','FY2025','9M2025')
rows['TTM2026Q3']={f:round(rows['FY2025'][f]+rows['9M2026'][f]-rows['9M2025'][f],1) for f in fields}
lineage['TTM2026Q3']={f:f'FY2025.{f} + 9M2026.{f} - 9M2025.{f}' for f in fields}
rows['TTM2025Q3']={f:round(rows['FY2024'][f]+rows['9M2025'][f]-rows['9M2024'][f],1) for f in fields}
lineage['TTM2025Q3']={f:f'FY2024.{f} + 9M2025.{f} - 9M2024.{f}' for f in fields}
lineage['9M2024']={f:'Q3_25' for f in fields}
eps={'FY2023':[7.75,7.48],'FY2024':[6.54,6.36],'FY2025':[2.91,2.85],'Q12025':[.64,.62],'Q12026':[1.21,1.18],'Q22025':[.60,.58],'Q22026':[3.31,3.25],'Q32025':[.79,.77],'Q32026':[1.94,1.91],'H12025':[1.24,1.20],'H12026':[4.52,4.43],'9M2024':[5.77,5.61],'9M2025':[2.03,1.98],'9M2026':[6.46,6.34]}
sbceq={'FY2023':22.5,'FY2024':30.2,'FY2025':34.1,'9M2024':22.4,'9M2025':24.7,'9M2026':14.4,'H12025':14.0,'H12026':8.3,'Q12025':7.9,'Q12026':3.8}
for y in [2025,2026]:
 sbceq[f'Q2{y}']=round(sbceq[f'H1{y}']-sbceq[f'Q1{y}'],1);sbceq[f'Q3{y}']=round(sbceq[f'9M{y}']-sbceq[f'H1{y}'],1)
sbceq['Q42025']=9.4;sbceq['TTM2025Q3']=32.5;sbceq['TTM2026Q3']=23.8
for p,r in rows.items():
 r['basic_eps_usd'],r['diluted_eps_usd']=eps.get(p,[None,None])
 r['sbc_expense']= {'FY2023':23.0,'FY2024':30.3,'FY2025':34.1}.get(p)
 r['sbc_equity_movement']=sbceq.get(p)
 for f in ['basic_eps_usd','diluted_eps_usd']:lineage[p][f]='reported EPS from period income statement; derived-quarter/TTM EPS null, not summed'
 lineage[p]['sbc_expense']='FY25_20F staff costs note 5; interim expense not separately verified (null)'
 lineage[p]['sbc_equity_movement']='source period changes in equity statement; discrete quarters/TTM cumulative difference; not asserted identical to expense'
 r['ebitda']=round(r['ebit']+r['da'],1);r['ebit_ex_vessel_sale_gain']=round(r['ebit']-r['vessel_sale_gain'],1)
 r['cfo_less_all_cash_capex']=round(r['cfo']-r['cash_tangible_investment']-r['cash_intangible_investment'],1)
 r['issuer_fcf_cfo_plus_cfi']=round(r['cfo']+r['cfi'],1);r['owner_fcf']=None
 for f in ['ebitda','ebit_ex_vessel_sale_gain','cfo_less_all_cash_capex','issuer_fcf_cfo_plus_cfi']:lineage[p][f]='formula; see build_history.py'
 lineage[p]['owner_fcf']='unresolved maintenance/replacement vs growth capex; no cycle normalization'
(P/'numerical_inputs.json').write_text(json.dumps({'unit':'USD million','reported_inputs':data,'field_order':fields},indent=2))
(P/'normalized_history.json').write_text(json.dumps(rows,indent=2));(P/'field_lineage.json').write_text(json.dumps(lineage,indent=2))
with (P/'normalized_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(rows.values())).keys()));w.writeheader();w.writerows(dict(period=p,**r) for p,r in rows.items())
qa=[]
for p,r in rows.items():
 gap=round(r['cfi']-(-r['cash_tangible_investment']-r['cash_intangible_investment']+r['asset_sale_proceeds']+r['restricted_cash_change']),2)
 qa.append({'test':p+' investing bridge','gap_usdm':gap,'pass':abs(gap)<=.21})
for y in [2025,2026]:
 for f in fields:
  gap=round(sum(rows[f'Q{q}{y}'][f] for q in [1,2,3])-rows[f'9M{y}'][f],2)
  qa.append({'test':str(y)+' 3 quarters vs YTD '+f,'gap_usdm':gap,'pass':abs(gap)<=.21})
(P/'qa.json').write_text(json.dumps({'rounding_tolerance_usdm':.21,'tests':qa,'all_pass':all(x['pass'] for x in qa)},indent=2))
print(rows['TTM2026Q3']);print('all QA',all(x['pass'] for x in qa))
