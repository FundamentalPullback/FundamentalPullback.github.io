"""Offline, Python standard library only. Rebuild normalized history from minimal inputs.json.
All monetary inputs/output USD millions; shares millions; EPS USD/share.
No valuation or adjusted earnings. Null means unavailable, never zero assumed.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'inputs.json').read_text()); I=D['periods']; out={}
flow=[k for k in D['metrics'] if k not in ['eps_basic','eps_diluted','shares_basic','shares_diluted']]
def combine(label,terms,end,weeks):
 r={'period':label,'end':end,'weeks':weeks,'derivation':terms}
 for k in D['metrics']:
  if k.startswith('eps_'):r[k]=None;continue
  vals=[(I[x].get(k),w) for x,w in terms.items()]
  r[k]=sum(v*w for v,w in vals) if all(v is not None for v,w in vals) else None
  if k.startswith('shares_'):
   weights={x:w*I[x]['weeks']/weeks for x,w in terms.items()}
   r[k]=sum(I[x][k]*w for x,w in weights.items()) if all(I[x].get(k) is not None for x in weights) else None
 for k in ['eps_basic','eps_diluted']:
  share=r[k.replace('eps','shares')]
  r[k]=r['net_income']/share if share and r['net_income'] is not None else None
 return r
for k in ['FY2023','FY2024','FY2025','FY2026Q1','FY2026Q2','FY2026Q3']:
 out[k]=dict(I[k],period=k,derivation='direct reported')
out['FY2025Q4']=combine('FY2025Q4',{'FY2025':1,'9M2025':-1},'2025-12-27',13)
# Q2 and Q3 CF only available YTD: subtract exact YTD values, never divide by quarters.
for q,now,prior in [('FY2026Q2','6M2026','FY2026Q1'),('FY2026Q3','9M2026','6M2026')]:
 for metric in D['cash_flow_metrics']:
  a,b=I[now].get(metric),I[prior].get(metric)
  out[q][metric]=a-b if a is not None and b is not None else None
 out[q]['cash_flow_derivation']=now+' minus '+prior
out['TTM2026Q3']=combine('TTM2026Q3',{'FY2025':1,'9M2025':-1,'9M2026':1},'2026-09-26',52)
out['TTM2025Q3']=combine('TTM2025Q3',{'FY2024':1,'9M2024':-1,'9M2025':1},'2025-09-27',52)
for r in out.values():
 for label,num,den in [('gross_margin','gross_profit','revenue'),('operating_margin','operating_income','revenue'),('net_margin','net_income','revenue'),('effective_tax_rate','tax_expense','pretax_income'),('sbc_to_revenue','sbc_expense','revenue')]:
  r[label]=r.get(num)/r[den] if r.get(num) is not None and r.get(den) else None
 a,b=r.get('cfo'),r.get('gross_capex');r['fcf_cfo_minus_gross_capex']=a-b if a is not None and b is not None else None
 r['fcf_margin']=r['fcf_cfo_minus_gross_capex']/r['revenue'] if r['fcf_cfo_minus_gross_capex'] is not None and r.get('revenue') else None
 bs=D['balance_sheets'].get(r['end'],{})
 r.update(bs)
 if all(bs.get(k) is not None for k in ['accounts_receivable','inventory','accounts_payable']):r['trade_working_capital']=bs['accounts_receivable']+bs['inventory']-bs['accounts_payable']
 for seg in ['probe_cards','systems']:
  if r.get(seg+'_revenue') and r.get(seg+'_gross_profit') is not None:r[seg+'_gross_margin']=r[seg+'_gross_profit']/r[seg+'_revenue']
rows=[out[k] for k in ['FY2023','FY2024','FY2025','FY2025Q4','FY2026Q1','FY2026Q2','FY2026Q3','TTM2025Q3','TTM2026Q3']]
(P/'normalized.json').write_text(json.dumps({'units':D['units'],'notes':D['notes'],'periods':rows},indent=2)+'\n')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (P/'normalized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
comparisons={}
for metric in D['metrics']+['fcf_cfo_minus_gross_capex','gross_margin','operating_margin','trade_working_capital']:
 a,b=out['TTM2026Q3'].get(metric),out['TTM2025Q3'].get(metric)
 comparisons[metric]={'current':a,'prior':b,'change':a-b if a is not None and b is not None else None,'growth':a/b-1 if a is not None and b else None}
(P/'ttm_comparison.json').write_text(json.dumps(comparisons,indent=2)+'\n')
# Exact financial statement arithmetic, subject to thousands rounding.
for r in rows:
 assert abs(r['revenue']-r['cost_of_revenue']-r['gross_profit'])<.003,r['period']
 assert abs(r['pretax_income']-r['tax_expense']+r.get('equity_method_income',0)-r['net_income'])<.003,r['period']
print('Reproduced',len(rows),'periods; revenue/COGS/GP and pretax/tax/net income checks passed.')
