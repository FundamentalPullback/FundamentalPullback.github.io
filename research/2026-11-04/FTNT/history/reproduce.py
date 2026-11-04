#!/usr/bin/env python3
"""Reproduce Fortinet historical series offline, Python standard library only."""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
inp=json.loads((P/'inputs.json').read_text()); r=inp['reported']; out={}; lineage={}
inc=set(r['FY2025'])-set(r['YTD12026']); inc.add('net_income')
cf=set(r['YTD12026'])
def diff(a,b,keys):return {k:round(a[k]-b[k],6) for k in sorted(keys)}
for y in [2023,2024,2025]:out[f'FY{y}']=dict(r[f'FY{y}']);lineage[f'FY{y}']='Direct 2025 10-K comparative annual statements'
for y in [2025,2026]:
 for q in [1,2,3]:
  p=f'Q{q}{y}';out[p]=dict(r[p]); k=f'YTD{q}{y}'
  cash=dict(r[k]) if q==1 else diff(r[k],r[f'YTD{q-1}{y}'],cf)
  out[p].update(cash);lineage[p]=f'Income/EPS direct quarter; cash flow '+('direct Q1' if q==1 else f'{q*3}M less {(q-1)*3}M cumulative cash flow')
for y in [2024,2025]:
 p=f'Q4{y}';out[p]=diff(r[f'FY{y}'],r[f'YTD3{y}'],set(r[f'FY{y}'])-{'diluted_eps'})
 out[p]['diluted_eps']=r[p+'_direct']['diluted_eps'];lineage[p]='FY less 9M for additive flows; diluted EPS directly reported in Q4 2025 release, not subtraction'
for y in [2025,2026]:
 ps=[f'Q4{y-1}']+[f'Q{q}{y}' for q in [1,2,3]];p=f'TTM_September_{y}'
 out[p]={k:round(sum(out[q][k] for q in ps),6) for k in out[ps[0]]};lineage[p]='Sum of '+', '.join(ps)+'; EPS sum of rounded reported quarterly EPS (not standalone GAAP annual EPS)'
for p,d in out.items():
 d['capex']=-d.pop('ppe_cash_outflow');d['fcf_cfo_minus_capex']=round(d['cfo']-d['capex'],6)
 nonrec=inp['nonrecurring_cash_receipts'].get(p,0.)
 if p=='TTM_September_2025':nonrec=inp['nonrecurring_cash_receipts']['Q12025']
 if p=='TTM_September_2026':nonrec=inp['nonrecurring_cash_receipts']['Q32026']
 d['nonrecurring_cash_receipts_excluded']=nonrec
 d['fcf_company_definition']=round(d['fcf_cfo_minus_capex']-nonrec,6)
 d['fcf_less_sbc_sensitivity']=round(d['fcf_company_definition']-d['sbc_cf'],6)
 d['fcf_ex_deferred_revenue_sensitivity']=round(d['fcf_company_definition']-d['deferred_revenue_cash'],6)
 d['net_deferred_contract_cash_effect']=round(d['deferred_contract_cash']+d['deferred_contract_amortization'],6)
 for name,num,den in [('operating_margin','ebit','revenue'),('net_margin','net_income','revenue'),('fcf_margin','fcf_company_definition','revenue'),('cfo_to_ni','cfo','net_income'),('effective_tax_rate','income_tax','pretax_income'),('sbc_to_revenue','sbc_cf','revenue'),('deferred_revenue_to_cfo','deferred_revenue_cash','cfo')]:d[name]=round(d[num]/d[den],8)
 assert abs(d['product_revenue']+d['service_revenue']-d['revenue'])<.11
 assert abs(d['fcf_cfo_minus_capex']-d['cfo']+d['capex'])<.01
order=['FY2023','FY2024','FY2025','Q42024','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','TTM_September_2025','TTM_September_2026']
results={'units':inp['units'],'as_of':'2026-11-04','periods':{p:out[p] for p in order},'methodology':lineage,'sources':inp['sources']}
(P/'financial_history.json').write_text(json.dumps(results,indent=2)+'\n')
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(out['FY2025']));w.writeheader();w.writerows({'period':p,**out[p]} for p in order)
current=out['TTM_September_2026'];prior=out['TTM_September_2025'];comparison={k:{'current':current[k],'prior':prior[k],'change':round(current[k]-prior[k],6),'growth_pct':round(100*(current[k]/prior[k]-1),4) if prior[k] else None} for k in current}
(P/'ttm_comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
print('PASS: 3 annual, 8 quarterly, 2 TTM periods; reconciliations passed.')
for p in ['TTM_September_2025','TTM_September_2026']:print(p,{k:out[p][k] for k in ['revenue','ebit','net_income','diluted_eps','cfo','capex','fcf_company_definition','sbc_cf','deferred_revenue_cash']})
