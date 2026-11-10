import json,csv,hashlib
from pathlib import Path
r=Path(__file__).parent
# USD millions. Original source columns: k25 FY25/FY24/FY23; q3 9M26/9M25; q2 H126/Q226.
a={
'FY2023':dict(revenue=13683,pretax=1087,net_income=921,net_interest=77,nonservice_pension_income=237,da=395,cfo_cont=1267,capex=402),
'FY2024':dict(revenue=13702,pretax=943,net_income=824,net_interest=97,nonservice_pension_income=263,da=382,cfo_cont=1015,capex=364),
'FY2025':dict(revenue=14799,pretax=1137,net_income=921,net_interest=126,nonservice_pension_income=266,da=401,cfo_cont=1313,capex=383),
'9M2025':dict(revenue=10624,pretax=858,net_income=686,net_interest=90,nonservice_pension_income=200,da=289,cfo_cont=613,capex=210),
'9M2026':dict(revenue=11273,pretax=893,net_income=738,net_interest=99,nonservice_pension_income=210,da=291,cfo_cont=613,capex=330),
'H12026':dict(revenue=7522,pretax=571,net_income=468,net_interest=67,nonservice_pension_income=140,da=190,cfo_cont=187,capex=228),
'Q22026':dict(revenue=3827,pretax=304,net_income=248,net_interest=33,nonservice_pension_income=70),
'Q32026':dict(revenue=3751,pretax=322,net_income=270,net_interest=32,nonservice_pension_income=70,da=101,cfo_cont=426,capex=102),
'Q32025':dict(revenue=3602,pretax=316,net_income=234,net_interest=30,nonservice_pension_income=67,da=97,cfo_cont=349,capex=76)}
a['Q42025_derived']={k:a['FY2025'][k]-a['9M2025'][k] for k in a['FY2025']}
a['Q12026_derived']={k:a['H12026'][k]-a['Q22026'][k] for k in a['Q22026']}
a['TTM2026_derived']={k:a['FY2025'][k]-a['9M2025'][k]+a['9M2026'][k] for k in a['FY2025']}
for x in a.values():
 x['pretax_plus_net_interest_ex_nonservice_pension_diagnostic']=x['pretax']+x['net_interest']-x['nonservice_pension_income']
 if 'cfo_cont'in x:x['cfo_cont_less_capex']=x['cfo_cont']-x['capex']
b={'scanner_price':85.41,'opportunity':80,'shares_oct16_m':169.399979,'manufacturing_debt_oct3':3465,'finance_debt_oct3':339,'manufacturing_cash_oct3':1610,'finance_cash_oct3':86,'operating_lease_liability_oct3':405,'finance_lease_in_manufacturing_debt':26,'nov4_notes_principal':350,'nov4_notes_coupon':0.055,'planned_refinanced_notes_principal':350,'planned_refinanced_coupon':0.0365}
b.update(market_cap_reference=b['scanner_price']*b['shares_oct16_m'],manufacturing_net_debt_oct3=3465-1610,consolidated_net_debt_oct3=3465+339-1610-86,annual_coupon_new=350*.055,annual_coupon_old=350*.0365,annual_coupon_increase_if_one_for_one=350*(.055-.0365),manufacturing_9m_simple_fcf=640-330,manufacturing_9m_company_cash=640-330+28+6,manufacturing_q3_company_cash=512-102+8,consolidated_9m_simple_fcf=613-330,consolidated_q3_simple_fcf=426-102)
b.update(guidance_gaap_pe_low=85.41/5.74,guidance_gaap_pe_high=85.41/5.64,guidance_adjusted_pe_low=85.41/6.65,guidance_adjusted_pe_high=85.41/6.55)
assert b['manufacturing_9m_company_cash']==344
assert b['manufacturing_q3_company_cash']==418
assert sum(a[x]['revenue'] for x in ['Q42025_derived','Q12026_derived','Q22026','Q32026'])==a['TTM2026_derived']['revenue']
assert sum(a[x]['pretax'] for x in ['Q42025_derived','Q12026_derived','Q22026','Q32026'])==a['TTM2026_derived']['pretax']
(r/'calculations.json').write_text(json.dumps({'units':'USD millions except per-share prices, ratios and shares noted','actuals_and_derivations':a,'diagnostics':b,'valuation':'unavailable','entryApproved':False},indent=2)+'\n')
keys=list(a['FY2025']);w=csv.writer((r/'financials.csv').open('w'));w.writerow(['period']+keys)
for p,x in a.items():w.writerow([p]+[x.get(k,'') for k in keys])
print(json.dumps(b,indent=2));print(a['TTM2026_derived'])
