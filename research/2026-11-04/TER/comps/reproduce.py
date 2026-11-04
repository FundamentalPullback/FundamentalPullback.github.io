"""Offline peer screen. Python3 standard library, no network. Run from any cwd."""
import json,csv
from pathlib import Path
p=Path(__file__).parent
j=json.load(open(p/'inputs.json')); out={}; checks=[]
for ticker,a in j['peers'].items():
 periods=a['periods']; c=a['capital']
 if ticker=='TER':
  t=dict(periods['TTM']);t['sbc']=t.pop('sbc_cf')
 else:
  first,old,new=('FY2025','H12025','H12026') if ticker=='6857' else ('FY2025','9M2025','9M2026')
  t={k:round(periods[first][k]-periods[old][k]+periods[new][k],6) for k in periods[first]}
  if ticker=='6857':t['capex']=t['capex_ppe']+t['capex_intangibles']
 t['fcf']=t['cfo']-t['capex'];t['fcf_after_sbc_proxy']=t['fcf']-t['sbc']
 t['operating_margin_pct']=100*t['ebit']/t['revenue']; t['fcf_margin_pct']=100*t['fcf']/t['revenue'];t['sbc_pct_revenue']=100*t['sbc']/t['revenue']
 t['fcf_conversion_to_ebit_pct']=100*t['fcf']/t['ebit'] if t['ebit']>0 else None
 if ticker=='6857':t['fcf_after_lease_principal']=t['fcf']-t['lease_principal'];t['fcf_after_lease_and_sbc_proxy']=t['fcf_after_lease_principal']-t['sbc']
 shares=c.get('shares',c.get('shares_sep30'));cash=c['cash_and_liquid_investments']
 if ticker=='6857':shares=shares-c['oct_repurchase_shares']+c['oct_restricted_shares_issued'];cash-=c['oct_repurchase_cost']
 mcap=shares*c['price'];ev=mcap+c['debt_face']-cash
 v={'shares_used':shares,'market_cap':mcap,'cash_used':cash,'face_debt':c['debt_face'],'screen_ev':ev,'ev_revenue':ev/t['revenue'],'ev_ebit':ev/t['ebit'] if t['ebit']>0 else None,'fcf_yield_pct':100*t['fcf']/mcap,'fcf_after_sbc_yield_pct':100*t['fcf_after_sbc_proxy']/mcap}
 if ticker=='6857':
  v['screen_ev_including_ifrs_leases']=ev+c['lease_liabilities'];v['ev_ebit_including_ifrs_leases']=(ev+c['lease_liabilities'])/t['ebit']
  v['investment_book_subtraction_sensitivity_ev']=ev-c['investment_securities_book'];v['investment_book_subtraction_sensitivity_ev_ebit']=(ev-c['investment_securities_book'])/t['ebit']
  checks.append({'check':'Advantest convertible out of money at selected close','passed':c['price']<c['conversion_price']})
 if ticker=='TER':
  stake=c['technoprobe_shares']*c['technoprobe_price_eur']*c['usd_per_eur']
  industrial=ev-stake+c['pension_liability']+c['redeemable_nci_book']
  v.update({'technoprobe_mark':stake,'industrial_ev_with_book_nci':industrial,'industrial_ev_revenue':industrial/t['revenue'],'industrial_ev_ebit':industrial/t['ebit']})
 if ticker=='COHU':
  underlying=c['convert_principal']*c['convert_shares_per_1000']/1000
  strike=1000/c['convert_shares_per_1000']; gross=max(0,underlying*c['price']-c['convert_principal']); offset=underlying*max(0,min(c['price'],c['capped_call_cap'])-strike)
  v.update({'convert_underlying_shares':underlying,'convert_gross_intrinsic':gross,'capped_call_intrinsic_offset':offset,'convert_net_intrinsic':gross-offset,'ev_with_net_intrinsic_sensitivity':ev+gross-offset,'ev_revenue_net_intrinsic_sensitivity':(ev+gross-offset)/t['revenue'],'ev_revenue_gross_intrinsic_sensitivity':(ev+gross)/t['revenue']})
  checks.append({'check':'Cohu negative EBIT gives null multiple, not negative valuation','passed':t['ebit']<0 and v['ev_ebit'] is None})
 checks += [{'check':ticker+' FCF identity','passed':abs(t['fcf']-(t['cfo']-t['capex']))<1e-8},{'check':ticker+' positive revenue','passed':t['revenue']>0}]
 out[ticker]={'currency':a['currency'],'period':a['period'],'accounting':a['accounting'],'role':a['role'],'ttm':t,'valuation_screen':v,'limitations':a['limitations'],'sources':a['sources']}
(p/'results.json').write_text(json.dumps({'as_of':j['as_of'],'posture':'screening-only, no peer-median target','peers':out},indent=2)+'\n')
checks.append({'check':'Advantest TTM revenue independently expected1447077','passed':out['6857']['ttm']['revenue']==1447077})
checks.append({'check':'Cohu TTM EBIT independently expected-13.552','passed':abs(out['COHU']['ttm']['ebit']+13.552)<1e-8})
(p/'checks.json').write_text(json.dumps({'passed':all(x['passed'] for x in checks),'checks':checks},indent=2)+'\n')
rows=[]
for k,r in out.items():
 t=r['ttm'];v=r['valuation_screen'];rows.append({'ticker':k,'currency':r['currency'],'period':r['period'],'revenue':t['revenue'],'ebit':t['ebit'],'operating_margin_pct':t['operating_margin_pct'],'cfo':t['cfo'],'capex':t['capex'],'fcf':t['fcf'],'sbc':t['sbc'],'fcf_after_sbc_proxy':t['fcf_after_sbc_proxy'],'ev_revenue_screen':v['ev_revenue'],'ev_ebit_screen':v['ev_ebit'],'fcf_yield_pct':v['fcf_yield_pct']})
with (p/'comparison.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2));assert all(x['passed'] for x in checks)
