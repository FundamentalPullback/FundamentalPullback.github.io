"""Validate rebuilt history against source inputs and independent public release checks."""
import csv,json,pathlib,math,datetime
P=pathlib.Path(__file__).resolve().parent;x=json.loads((P/'inputs.json').read_text());h=json.loads((P/'history.json').read_text());R={r['period']:r for r in h['periods']};I={r['period']:r for r in x['reported_periods']};checks=[]
def v(p,k):
 d=R[p]['metrics'].get(k);return None if d is None else d['value']
def ck(area,p,name,observed,expected,tolerance=1e-8,notes=''):
 passed=(observed==expected) if isinstance(expected,(bool,str)) else observed is not None and abs(observed-expected)<=tolerance
 checks.append({'check_id':f'C{len(checks)+1:03}','area':area,'period':p,'test':name,'observed':observed,'expected':expected,'variance':observed-expected if isinstance(observed,(int,float)) and not isinstance(observed,bool) and isinstance(expected,(int,float)) else None,'result':'PASS' if passed else 'FAIL','notes':notes})
for p,r in R.items():
 ck('periods',p,'Exact dates tie to stated fiscal weeks',(datetime.date.fromisoformat(r['end'])-datetime.date.fromisoformat(r['start'])).days+1,r['weeks']*7)
 for a,b,c,label in [('revenue','cost_of_revenue','gross_profit','Revenue less cost = gross profit'),('gross_profit','operating_expenses','operating_income','Gross profit less opex = EBIT'),('pretax_income','income_tax_expense','net_income','Pretax less tax = net income'),('cfo','capex_outflow','fcf','CFO less all capex = FCF'),('fcf','sbc','fcf_after_sbc','FCF less SBC = economic cash')]:ck('statement_tieout',p,label,v(p,a)-v(p,b),v(p,c))
 if v(p,'ppe_depreciation_amortization') is not None and v(p,'intangible_amortization') is not None:
  ck('da_split',p,'Total D&A = PP&E D&A + acquired intangibles',v(p,'ppe_depreciation_amortization')+v(p,'intangible_amortization'),v(p,'depreciation_amortization'))
 if r['type']!='ttm':
  for basis in ['basic','diluted']:
   ni,shares,eps=v(p,'net_income'),v(p,'shares_'+basis+'_m'),v(p,'eps_'+basis)
   lo=(ni-.5)/(shares+.5);hi=(ni+.5)/(shares-.5)
   ck('shares_eps',p,basis+' EPS consistent with source rounding intervals',bool((eps+.005)>=lo and (eps-.005)<=hi),True,notes='Income and weighted shares rounded to $m/m shares; EPS to cents. Not backsolved.')
   orig=I[p]['metrics'].get('eps_'+basis)
   ck('shares_eps',p,basis+' EPS is direct original input',eps,orig['value'])
   ck('shares_eps',p,basis+' share count is direct original input',shares,I[p]['metrics']['shares_'+basis+'_m']['value'])
 for k,m in r['metrics'].items():
  if m:
   src=[m['source_id']] if m.get('source_id') else m.get('source_ids',[])
   ck('provenance',p,k+' has existing source identifiers',bool(src and all(s in x['sources'] for s in src)),True)
for y in ['2025','2026']:
 for k in ['revenue','cost_of_revenue','gross_profit','operating_income','net_income','pretax_income','income_tax_expense','research_development','cfo','capex_outflow','sbc','depreciation_amortization','restructuring_charge','fcf','fcf_after_sbc']:
  ck('annual_quarter_tieout','FY'+y,k+' annual = sum four quarters',sum(v(f'Q{q}FY{y}',k) for q in range(1,5)),v('FY'+y,k))
for p,annual,new,old in [('TTM2026-07-31','FY2026','Q1FY2027','Q1FY2026'),('TTM2025-07-25','FY2025','Q1FY2026','Q1FY2025')]:
 for k in ['revenue','operating_income','net_income','cfo','capex_outflow','sbc','research_development','depreciation_amortization','restructuring_charge','fcf','fcf_after_sbc']:
  ck('ttm_independent_tieout',p,k+' sum of quarters = FY + new Q1 - old Q1',v(p,k),v(annual,k)+v(new,k)-v(old,k))
for p,m in x['management_reconciliations'].items():ck('management_bridge',p,'GAAP NI + all issuer adjustments = issuer non-GAAP NI',v(p,'net_income')+sum(m['signed_adjustments_to_net_income'].values()),m['non_gaap_net_income'])
for p,d in x['manual_crosschecks'].items():
 for k,value in d.items():
  if k!='source_id':ck('independent_release',p,k+' ties direct release row',v(p,k),value)
for b in h['balance_sheets']:
 m=b['metrics'];v2=lambda k:m[k]['value'];p=b['period']
 ck('balance_sheet',p,'Assets = liabilities + equity',v2('total_assets'),v2('total_liabilities')+v2('equity'))
 ck('balance_sheet',p,'Carrying debt = current + noncurrent',v2('debt_carrying'),v2('current_debt')+v2('noncurrent_debt'))
for p in ['FY2026','Q4FY2026','TTM2026-07-31']:ck('normalization',p,'Only gross $11m Spot gain removed; all recurring expenses retained',v(p,'operating_income_ex_spot_gain'),v(p,'operating_income')-11)
ck('ttm','TTM2026-07-31','GAAP EBIT is 1849, not restructuring-adjusted 1924',v('TTM2026-07-31','operating_income'),1849)
ck('ttm','TTM2026-07-31','Current TTM weeks',R['TTM2026-07-31']['weeks'],53)
ck('ttm','TTM2025-07-25','Prior TTM weeks',R['TTM2025-07-25']['weeks'],52)
ck('cash','TTM2026-07-31','Reported FCF',v('TTM2026-07-31','fcf'),1650)
ck('cash','TTM2025-07-25','Reported prior FCF',v('TTM2025-07-25','fcf'),1658)
ck('acquisition','Q1FY2027','Net acquisition cash = cash consideration - cash acquired',87-9,v('Q1FY2027','acquisition_net_cash_paid'))
ck('acquisition','Q1FY2027','Purchase price = upfront + contingent',87+106,193)
ck('acquisition','Q1FY2027','Contingent obligation stays explicit',h['balance_sheets'][-1]['additional_acquisition_obligation']['amount'],106)
failed=[c for c in checks if c['result']=='FAIL']
qa=[
{'id':'QA-WEEKS','severity':'high','status':'disclosed','issue':'53-week current TTM versus 52 prior. Q1FY2027 14 weeks. Management extra-week estimates rounded; no exact GAAP/CFO equal-week series.','treatment':'Load reported actuals. Use separate labeled revenue sensitivity only.'},
{'id':'QA-SBC','severity':'high','status':'controlled','issue':'Issuer non-GAAP excludes recurring SBC and recurring restructuring.','treatment':'Core stays GAAP; FCF after SBC is separate economic cash proxy. No automatic non-GAAP substitution.'},
{'id':'QA-SOFTWARE','severity':'medium','status':'open_disclosure_limit','issue':'Internal-use software and cloud capex additions not separately disclosed.','treatment':'Retain full PP&E capex; no invented zero, no second software capex deduction.'},
{'id':'QA-ACQ','severity':'high','status':'disclosed','issue':'DataPelago $106m contingent consideration is accrued, unpaid and outside $78m net cash purchase. Subsequent JetStream not captured in July balance.','treatment':'Separate acquisition obligation; not ordinary working capital. No November cash certification.'},
{'id':'QA-EPS','severity':'medium','status':'controlled','issue':'Quarter/annual EPS and shares direct, but TTM weighted shares built from rounded quarterly data and EPS is sum of quarters.','treatment':'TTM figures labeled derived; never infer direct Q4 share count or use annual EPS subtraction.'},
{'id':'QA-TAX','severity':'medium','status':'disclosed','issue':'FY2025 14.2% tax rate affected by discrete tax items; final transition-tax payment in Q2FY2026.','treatment':'No low historical tax extrapolation; retain cash payment in base. Show $179m timing sensitivity separately.'},
{'id':'QA-TAG','severity':'low','status':'resolved','issue':'Companyfacts mislabels a $287m nine-month cash-tax figure as H1FY2025.','treatment':'Direct filing tables confirm H1 $222m and 9M $287m. Conflict preserved in inputs.'},
{'id':'QA-DISPOSAL','severity':'medium','status':'disclosed','issue':'Spot sold March2025; FY2024/25 segment comparison includes disposed operations. No full comparable organic historical series.','treatment':'Reported financial history loadable; do not call organic/recast.'}]
report={'status':'PASS' if not failed else 'FAIL','checks_total':len(checks),'checks_passed':len(checks)-len(failed),'checks_failed':len(failed),'failed_checks':failed,'qa_flags':qa,'scope':'Historical arithmetic/provenance/normalization checks only. Not approval of valuation, price, entry or event calendar.','checks':checks}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
with (P/'validation_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
(P/'qa_flags.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','checks_total','checks_passed','checks_failed','failed_checks']},indent=2))
raise SystemExit(bool(failed))
