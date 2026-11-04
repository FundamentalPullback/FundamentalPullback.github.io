"""Reproduce derived history using only minimal inputs.json; no network/full source required."""
import json,pathlib,csv
P=pathlib.Path(__file__).parent
x=json.load(open(P/'inputs.json'));p=x['periods']
def diff(a,b):return {k:round(v-b.get(k),5) if v is not None and b.get(k) is not None else None for k,v in a.items()}
for k in ['da','sbc']:
 p['Q22026'][k]=round(p['H12026'][k]-p['Q12026'][k],5)
for d in p.values():
 if d['acquired_amortization'] is None and d['software_amortization'] is not None:d['acquired_amortization']=round(d['da']-d['depreciation']-d['software_amortization'],5)
p['Q42025']=diff(p['FY2025'],p['9M2025']);p['Q42025'].update(x['quarter4_reported']['Q42025'])
for k in ['cfo','ppe_capex','software_capex','acquisition_cash']:
 p['Q22026'][k]=round(p['H12026'][k]-p['Q12026'][k],5)
 p['Q32026'][k]=round(p['9M2026'][k]-p['H12026'][k],5)
for yy in [2025,2026]:
 fy=p[f'FY{yy-1}'];old=p[f'9M{yy-1}'];new=p[f'9M{yy}']
 d={k:round(fy[k]-old[k]+new[k],5) if all(v is not None for v in [fy[k],old[k],new[k]]) else None for k in fy}
 daysfy=366 if yy==2025 else 365;daysold=274 if yy==2025 else 273
 d['shares_diluted']=round((x['quarter4_reported'][f'Q4{yy-1}']['shares_diluted']*92+new['shares_diluted']*273)/365,5)
 d['eps_diluted']=round(x['quarter4_reported'][f'Q4{yy-1}']['eps_diluted']+new['eps_diluted'],2)
 p[f'TTM0920{str(yy)[-2:]}']=d
for name,d in p.items():
 d['capex_total']=round(d['ppe_capex']+d['software_capex'],5) if d['ppe_capex'] is not None and d['software_capex'] is not None else None
 d['fcf_strict']=round(d['cfo']-d['capex_total'],5) if d['cfo'] is not None and d['capex_total'] is not None else None
 d['fcf_after_sbc_diagnostic']=round(d['fcf_strict']-d['sbc'],5) if d['fcf_strict'] is not None else None
 d['ebit_margin']=d['ebit_gaap']/d['revenue'];d['fcf_margin']=d['fcf_strict']/d['revenue'] if d['fcf_strict'] is not None else None
 d['ebit_before_acquired_amort']=round(d['ebit_gaap']+d['acquired_amortization'],5) if d['acquired_amortization'] is not None else None
 d['net_margin']=d['net_income_parent']/d['revenue'];d['effective_tax_rate']=d['tax']/d['pretax']
 d['eps_ratio_diagnostic']=d['net_income_parent']/d['shares_diluted']
 if name in x['working_capital']:d['wc_cash_contribution']=round(sum(x['working_capital'][name].values()),5)
bs=x['balance_sheets']
for d in bs.values(): d['invested_capital_book_netdebt_equity']=round(d['equity_total']+d['debt_current']+d['debt_noncurrent']-d['cash_corporate'],5)
roic={}
for yy in [2023,2024,2025]:
 d=p[f'FY{yy}'];ic=(bs[str(yy)]['invested_capital_book_netdebt_equity']+bs[str(yy-1)]['invested_capital_book_netdebt_equity'])/2
 roic[str(yy)]={'average_invested_capital':ic,'nopat_at_25pct_tax':d['ebit_gaap']*.75,'roic_gaap_25pct_tax':d['ebit_gaap']*.75/ic,'roic_before_acquired_amort_25pct_tax':d['ebit_before_acquired_amort']*.75/ic}
bridges={}
for a,b in [('FY2023','FY2024'),('FY2024','FY2025'),('9M2025','9M2026'),('TTM092025','TTM092026')]:
 old,new=p[a],p[b]; revenue=old['ebit_gaap']*(new['revenue']/old['revenue']-1);margin=new['ebit_gaap']-old['ebit_gaap']-revenue
 bridges[b]={'comparison':a,'revenue_growth':new['revenue']/old['revenue']-1,'ebit_growth':new['ebit_gaap']/old['ebit_gaap']-1,'ebit_margin_change_bps':(new['ebit_margin']-old['ebit_margin'])*1e4,'ebit_growth_revenue_contribution_usdm':revenue,'ebit_growth_margin_contribution_usdm':margin,'net_income_growth':new['net_income_parent']/old['net_income_parent']-1,'shares_change':new['shares_diluted']/old['shares_diluted']-1,'eps_growth_ratio_based':new['eps_ratio_diagnostic']/old['eps_ratio_diagnostic']-1,'eps_growth_income_contribution':(new['net_income_parent']-old['net_income_parent'])/old['shares_diluted'],'eps_growth_buyback_contribution':new['net_income_parent']*(1/new['shares_diluted']-1/old['shares_diluted']),'cfo_growth':new['cfo']/old['cfo']-1,'fcf_growth':new['fcf_strict']/old['fcf_strict']-1}
 if 'wc_cash_contribution' in old and 'wc_cash_contribution' in new:bridges[b]['wc_cash_improvement']=new['wc_cash_contribution']-old['wc_cash_contribution']
notes=['All amounts USD millions except shares (millions), EPS ($) and ratios.','FY2023-25 financial statements audited; interim releases unaudited.','FCF strict = CFO - cash PP&E additions - capitalized software; acquisitions excluded and shown separately. FCF after SBC is an analytical owner-cost diagnostic, not GAAP cash flow or a claim that SBC cash was paid.','Q4 = FY minus 9M; Q2/Q3 cash flow = YTD differences. Q4 EPS and diluted shares directly from issuer quarterly financials, not annual minus YTD.','TTM flows = prior FY - prior 9M + current 9M. TTM EPS field is summed reported period EPS (rounded); TTM share count estimated by day weighting, so net-income/share EPS diagnostic can differ.','Acquired amortization interim = total D&A minus physical depreciation minus capitalized-software amortization. Q3/9M2026 developed-software split unavailable in release; acquired amortization remains null.','Invested capital = total equity including NCI + book debt - corporate cash. Goodwill/intangibles retained. Client funds never included as corporate cash/debt. No operating-cash reserve, lease capitalization or investment asset exclusion in this diagnostic.','ROIC uses normalized 25% tax, not variable reported effective taxes, and average beginning/end invested capital. Before-acquired-amort ROIC is supplemental, not GAAP.']
y={'periods':p,'balance_sheets':bs,'roic':roic,'growth_bridges':bridges,'working_capital':x['working_capital'],'notes':notes,'sources':x['sources']}
y['metric_status']={'Q42025':{'shares_diluted':'REPORTED Q4 diluted shares251.5m in issuer February5 quarterly financials','eps_diluted':'REPORTED Q4 diluted EPS0.77 in issuer February5 financials'},'TTM092025':{'shares_diluted':'ESTIMATED day-weighted proxy from reported Q42024 and9M2025 averages; NOT reported TTM shares','eps_diluted':'SUM of rounded reported period EPS; not a directly reported TTM EPS'},'TTM092026':{'shares_diluted':'ESTIMATED day-weighted proxy from reported Q42025 and9M2026 averages; NOT reported TTM shares','eps_diluted':'SUM of rounded reported period EPS; not a directly reported TTM EPS'}}
json.dump(y,open(P/'history.json','w'),indent=2)
sel=['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM092025','TTM092026']
with open(P/'history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period','shares_status','eps_status']+list(p['FY2025'].keys()),extrasaction='ignore');w.writeheader()
 for n in sel:w.writerow({'period':n,'shares_status':y.get('metric_status',{}).get(n,{}).get('shares_diluted','Reported weighted-average diluted shares'),'eps_status':y.get('metric_status',{}).get(n,{}).get('eps_diluted','Reported diluted EPS'),**p[n]})
print(json.dumps({'summary':{k:{f:p[k][f] for f in ['revenue','ebit_gaap','net_income_parent','eps_diluted','shares_diluted','cfo','capex_total','fcf_strict','fcf_after_sbc_diagnostic','da','acquired_amortization','software_amortization']} for k in sel},'roic':roic,'bridges':bridges},indent=2))
