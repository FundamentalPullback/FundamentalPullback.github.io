from pathlib import Path
import json,csv
r=Path(__file__).parent
a={'FY2023':dict(revenue=2581,ebit=287,net_income=178,da=119,cfo=316,capex=300,sbc=13),'FY2024':dict(revenue=2941,ebit=530,net_income=420,da=126,cfo=605,capex=183,sbc=20),'FY2025':dict(revenue=2708,ebit=209,net_income=146,da=145,cfo=382,capex=291,sbc=30),'9M2025':dict(revenue=2141,ebit=218,net_income=154,da=106,cfo=315,capex=216,sbc=24),'9M2026':dict(revenue=1929,ebit=95,net_income=76,da=115,cfo=214,capex=176,sbc=18),'H12026':dict(revenue=1239,ebit=66,net_income=53,da=77,cfo=102,capex=120,sbc=12),'Q22026':dict(revenue=664,ebit=31,net_income=26),'Q32026_direct':dict(revenue=691,ebit=29,net_income=23,da=38,cfo=112,capex=56,sbc=6)}
a['Q42025_derived']={k:a['FY2025'][k]-a['9M2025'][k] for k in a['FY2025']}
a['Q12026_derived']={k:a['H12026'][k]-a['Q22026'][k] for k in a['Q22026']}
a['Q32026_cumulative_difference']={k:a['9M2026'][k]-a['H12026'][k] for k in a['9M2026']}
a['TTM2026']={k:a['FY2025'][k]-a['9M2025'][k]+a['9M2026'][k] for k in a['FY2025']}
for d in a.values():
 if 'cfo'in d:d['cfo_less_capex']=d['cfo']-d['capex']
 d['ebit_margin_pct']=d['ebit']/d['revenue']*100
b=dict(price_reference=78.32,opportunity=80,shares_oct30_m=69.927181,market_cap_reference=78.32*69.927181,carrying_debt=349,cash=265,net_debt_carrying=349-265,operating_lease_liabilities=9+19,capex_unpaid_sep30=26,environmental_reserves=27,remaining_capex_implied=300-176,siding_q3_margin=119/473*100,siding_prior_q3_margin=117/443*100,ttm_simple_cash_after_sbc=30-24)
b['ev_simple_carrying_no_leases']=b['market_cap_reference']+b['net_debt_carrying'];b['ev_over_guidance_ebitda_low']=b['ev_simple_carrying_no_leases']/280;b['ev_over_guidance_ebitda_high']=b['ev_simple_carrying_no_leases']/270
checks={'ttm_formula':'FY2025 - 9M2025 + 9M2026','ttm_revenue_four_direct_quarters':sum(a[k]['revenue'] for k in ['Q42025_derived','Q12026_derived','Q22026','Q32026_direct']),'ttm_revenue_cumulative':a['TTM2026']['revenue'],'rounding_difference_revenue':1,'9m_simple_cash':38,'q3_simple_cash':56,'ttm_simple_cash':30,'no_valuation':True,'no_entry':True}
assert checks['ttm_revenue_four_direct_quarters']-checks['ttm_revenue_cumulative']==1
assert a['TTM2026']['cfo_less_capex']==30
(r/'calculations.json').write_text(json.dumps({'units':'USD millions except per-share price, ratios and shares explicitly in millions','actuals':a,'diagnostics':b,'checks':checks,'valuation':'unavailable','entryApproved':False},indent=2)+'\n')
keys=list(a['FY2025']);f=(r/'financials.csv').open('w');w=csv.writer(f);w.writerow(['period']+keys)
for p,x in a.items():w.writerow([p]+[x.get(k,'') for k in keys])
f.close();print(a['TTM2026']);print(b)
