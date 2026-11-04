"""Rebuild NTAP historical schedules from minimal, sourced facts. Standard library only."""
import csv,json,pathlib,copy,datetime
P=pathlib.Path(__file__).resolve().parent

def main():
 x=json.loads((P/'inputs.json').read_text()); rows={r['period']:copy.deepcopy(r) for r in x['reported_periods']}; defs=x['metric_definitions']; metrics=list(defs)
 def get(p,k):return rows[p]['metrics'].get(k)
 def calc(p,k,terms,formula,unit='USD million',note=None):
  ins=[get(a,b) for a,b,c in terms]
  if any(v is None for v in ins):rows[p]['metrics'][k]=None;return
  rows[p]['metrics'][k]={'value':round(sum(v['value']*c for v,(a,b,c) in zip(ins,terms)),10),'unit':unit,'evidence_label':'derived_calculation','formula':formula,'input_refs':[f'{a}.{b}' for a,b,c in terms],'source_ids':sorted(set(s for v in ins for s in ([v['source_id']] if v.get('source_id') else v.get('source_ids',[]))))}
  if note:rows[p]['metrics'][k]['note']=note
 def ratio(p,k,a,b,mult=1,unit='ratio'):
  av=get(p,a);bv=get(p,b)
  if not av or not bv or bv['value']==0:rows[p]['metrics'][k]=None;return
  rows[p]['metrics'][k]={'value':round(mult*av['value']/bv['value'],10),'unit':unit,'evidence_label':'derived_calculation','formula':f'{a}/{b}'+(f'*{mult}' if mult!=1 else ''),'input_refs':[f'{p}.{a}',f'{p}.{b}'],'source_ids':sorted(set(s for v in [av,bv] for s in ([v['source_id']] if v.get('source_id') else v.get('source_ids',[]))))}
 # Exact quarter amounts from year-to-date differences; EPS and weighted share counts never differenced.
 for year in ['2025','2026']:
  for q,hi,lo in [('2',f'H1FY{year}',f'Q1FY{year}'),('3',f'9MFY{year}',f'H1FY{year}'),('4',f'FY{year}',f'9MFY{year}')]:
   p=f'Q{q}FY{year}'
   for k in metrics:
    if k.startswith('eps_') or k.startswith('shares_'):continue
    if get(p,k) is None:calc(p,k,[(hi,k,1),(lo,k,-1)],f'{hi}.{k} - {lo}.{k}')
 # TTM flow values sum four quarters with FY plus/minus Q1 retained as independent validation.
 for p,start,end,qs in [('TTM2026-07-31','2025-07-26','2026-07-31',['Q2FY2026','Q3FY2026','Q4FY2026','Q1FY2027']),('TTM2025-07-25','2024-07-27','2025-07-25',['Q2FY2025','Q3FY2025','Q4FY2025','Q1FY2026'])]:
  weeks=sum(rows[q]['weeks'] for q in qs);rows[p]={'period':p,'start':start,'end':end,'type':'ttm','weeks':weeks,'quarters':qs,'metrics':{},'comparison_note':'53 weeks versus 52 in prior TTM; no equal-week earnings or cash-flow adjustment.' if weeks==53 else '52-week prior TTM.'}
  for k in metrics:
   if k.startswith('shares_'):
    calc(p,k,[(q,k,rows[q]['weeks']/weeks) for q in qs],'Time-weighted average of directly reported quarterly weighted shares','million shares','Approximation because source quarterly weighted shares are rounded to whole millions; not a directly filed TTM share count.')
   elif k.startswith('eps_'):
    calc(p,k+'_sum_of_reported_quarters',[(q,k,1) for q in qs],'Sum of directly reported quarterly EPS','USD/share','A four-quarter EPS sum, not annual EPS plus/minus rounded quarterly EPS and not a directly filed TTM EPS.')
   else:calc(p,k,[(q,k,1) for q in qs],' + '.join(f'{q}.{k}' for q in qs))
 # Conservative cash and margin metrics. No removal of R&D, SBC, ongoing restructuring or routine amortization.
 for p,r in rows.items():
  calc(p,'fcf',[(p,'cfo',1),(p,'capex_outflow',-1)],'CFO - cash purchases of property and equipment')
  calc(p,'fcf_after_sbc',[(p,'fcf',1),(p,'sbc',-1)],'FCF - stock-based compensation','USD million','Analyst economic dilution-cost proxy, not GAAP cash flow. SBC remains in GAAP earnings; not double-subtracted from earnings.')
  calc(p,'fcf_after_sbc_and_reported_acquisition_cash',[(p,'fcf_after_sbc',1),(p,'acquisition_net_cash_paid',-1)],'FCF - SBC - net cash paid for business acquisitions','USD million','Only shown when acquisition cash explicitly disclosed; not a standard operating FCF measure. Contingent purchase obligation remains separate.')
  calc(p,'capex_less_da',[(p,'capex_outflow',1),(p,'depreciation_amortization',-1)],'Cash capex - total depreciation and amortization','USD million','Diagnostic only; acquired intangible amortization included in D&A; not pure maintenance-versus-growth capex.')
  for k,a,b in [('gross_margin','gross_profit','revenue'),('operating_margin','operating_income','revenue'),('net_margin','net_income','revenue'),('fcf_margin','fcf','revenue'),('fcf_after_sbc_margin','fcf_after_sbc','revenue'),('rd_pct_sales','research_development','revenue'),('sbc_pct_sales','sbc','revenue'),('effective_tax_rate','income_tax_expense','pretax_income'),('cfo_net_income','cfo','net_income'),('fcf_net_income','fcf','net_income')]:ratio(p,k,a,b)
  if r['type']=='ttm':ratio(p,'eps_diluted_from_rounded_income_shares','net_income','shares_diluted_m',unit='USD/share')
  if p in x['management_reconciliations']:
   m=x['management_reconciliations'][p];r['management_non_gaap']={**m,'treatment':'Audit comparison only; do not use as conservative earnings without separately accepting recurring-cost exclusions.'}
 # Remove ONLY the individually documented $11m Spot contingent consideration gain. Recurring costs remain intact.
 for p in ['FY2026','Q4FY2026','TTM2026-07-31']:
  op=get(p,'operating_income');rows[p]['metrics']['operating_income_ex_spot_gain']={'value':op['value']-11,'unit':'USD million','evidence_label':'analyst_adjusted','formula':'GAAP operating income - 11','input_refs':[p+'.operating_income','documentary_notes.spot-contingent'],'source_ids':sorted(set(([op['source_id']] if op.get('source_id') else op.get('source_ids',[]))+['0001193125-26-259683'])),'note':'Subtract gross disclosed Spot contingent consideration gain, retain $1m other asset loss and all SBC, R&D, restructuring and amortization. No undisclosed tax effect guessed.'}
  ratio(p,'operating_margin_ex_spot_gain','operating_income_ex_spot_gain','revenue')
 # Cash-only sensitivity removing a FINAL historical tax payment, never presented as base FCF.
 for p in ['FY2026','Q2FY2026','TTM2026-07-31']:
  v=get(p,'fcf_after_sbc');rows[p]['metrics']['fcf_after_sbc_ex_final_transition_tax_sensitivity']={'value':v['value']+179,'unit':'USD million','evidence_label':'analyst_adjusted','formula':'FCF after SBC + 179 final transition tax payment','source_ids':['0001193125-26-259683'],'note':'Optional cash timing sensitivity. Does not adjust working capital, ordinary cash tax, or the 53rd week; base metrics retain actual cash payments.'}
 for b in x['balance_sheets']:
  v=lambda k:b['metrics'][k]['value'] if b['metrics'].get(k) else None
  b['calculated']={'cash_and_short_term_investments':v('cash')+v('short_term_investments'),'net_cash_using_carrying_debt':v('cash')+v('short_term_investments')-v('debt_carrying'),'working_capital':v('current_assets')-v('current_liabilities')}
  if b['period']=='Q1FY2027':b['additional_acquisition_obligation']={'amount':106,'unit':'USD million','classification':'Accrued contingent purchase consideration; debt-like acquisition obligation for valuation bridge, not ordinary operating working capital.','source_id':'0001193125-26-380207','cash_already_paid':False}
 outputorder=['FY2024','FY2025','FY2026','Q1FY2025','Q2FY2025','Q3FY2025','Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026','Q4FY2026','Q1FY2027','TTM2025-07-25','TTM2026-07-31']
 growth={}
 for cur,prev in [('FY2025','FY2024'),('FY2026','FY2025'),('Q1FY2027','Q1FY2026'),('TTM2026-07-31','TTM2025-07-25')]:
  growth[cur+'_vs_'+prev]={k:(get(cur,k)['value']/get(prev,k)['value']-1) if get(cur,k) and get(prev,k) and get(prev,k)['value'] else None for k in ['revenue','gross_profit','operating_income','net_income','cfo','capex_outflow','fcf','fcf_after_sbc','research_development','sbc','shares_diluted_m']}
 out={'entity':x['entity'],'ticker':x['ticker'],'as_of':x['as_of'],'unit':'USD million except EPS/share counts and ratios','coverage':'Three full fiscal years; nine quarters including latest four; current and prior TTM; four balance sheets. TTM uses exact period dates and 53/52-week caveat.','methodology':{'base':'Reported GAAP; recurring restructuring, SBC, R&D and normal amortization retained.','fcf':'CFO less all cash PP&E capex, including capitalized internal-use software within PP&E.','economic_cash':'FCF less SBC; analyst proxy, not GAAP and not issuer non-GAAP.','normalization':'Only documented Spot gain removed in named operating-income sensitivity; no unsupported tax allocation or exact net-income normalization.','eps':'Published period EPS and shares direct. Q4 shares/EPS from earnings release. TTM EPS sum and time-weighted diluted shares explicitly approximate/derived.','missing':'Absent data remains null; no invented zeros. No observed separate internal-use software additions or cloud capex series.','sources':'Minimal facts plus official URLs in inputs.json. Raw filings excluded from public package.'},'sources':x['sources'],'periods':[rows[k] for k in outputorder],'balance_sheets':x['balance_sheets'],'growth':growth,'documentary_notes':x['documentary_notes'],'conflicts':x['conflicts']}
 (P/'history.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 allmetrics=list(dict.fromkeys(k for r in out['periods'] for k in r['metrics']))
 with (P/'history.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['period','start','end','type','weeks']+allmetrics);w.writeheader()
  for r in out['periods']:w.writerow({**{k:r[k] for k in ['period','start','end','type','weeks']},**{k:v['value'] if v else '' for k,v in r['metrics'].items()}})
 # Long form is auditable companion; rows with missing data deliberately visible.
 with (P/'financials_long.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['entity','period','start','end','metric','value','unit','evidence_label','source_ids','source_urls','formula','note']);w.writeheader()
  for r in out['periods']:
   for k,v in r['metrics'].items():
    src=([v['source_id']] if v and v.get('source_id') else v.get('source_ids',[]) if v else [])
    w.writerow({'entity':'NTAP','period':r['period'],'start':r['start'],'end':r['end'],'metric':k,'value':v['value'] if v else '', 'unit':v.get('unit','') if v else '', 'evidence_label':v.get('evidence_label') if v else 'missing_required_source','source_ids':';'.join(src),'source_urls':';'.join(x['sources'][s]['url'] for s in src),'formula':v.get('formula','') if v else '', 'note':v.get('note','') if v else 'Not separately disclosed or not safely reconstructable.'})
 print('Rebuilt history.json, history.csv, financials_long.csv')
 print(json.dumps(growth,indent=2))
if __name__=='__main__':main()
