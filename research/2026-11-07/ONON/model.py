"""ONON: diagnóstico reproducible, no valoración aprobada. Millones de CHF.
Fuentes: sources.json. Sin tasas/FX inventados ni precio objetivo.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
annual={
 '2023':dict(sales=1792.1,ebit=180.2,net_income=79.6,cfo=232.1,ppe=42.8,intangibles=4.4,sbc_cf=27.3,lease_principal=25.5,interest_paid=6.5),
 '2024':dict(sales=2318.3,ebit=211.6,net_income=242.3,cfo=510.6,ppe=60.5,intangibles=4.5,sbc_cf=57.5,lease_principal=51.3,interest_paid=15.3),
 '2025':dict(sales=3014.0,ebit=377.0,net_income=203.7,cfo=359.5,ppe=72.9,intangibles=5.7,sbc_cf=66.6,lease_principal=69.9,interest_paid=21.5),
 'H1_2025':dict(sales=1475.8,ebit=169.8,net_income=15.8,cfo=89.1,ppe=27.3,intangibles=2.2,sbc_cf=25.2,lease_principal=34.7,interest_paid=9.9),
 'H1_2026':dict(sales=1682.2,ebit=236.9,net_income=208.3,cfo=255.0,ppe=41.9,intangibles=5.3,sbc_cf=30.9,lease_principal=35.8,interest_paid=12.5)}
annual['TTM_Jun2026']={k:annual['2025'][k]+annual['H1_2026'][k]-annual['H1_2025'][k] for k in annual['2025']}
for d in annual.values():
 d['cfo_less_ppe_intangibles']=d['cfo']-d['ppe']-d['intangibles']
 d['cash_after_lease_principal_interest']=d['cfo_less_ppe_intangibles']-d['lease_principal']-d['interest_paid']
 d['ebit_margin']=d['ebit']/d['sales']
quarters={'Q3_2025':dict(sales=794.4,ebit=124.7,net_income=118.9),'Q4_2025':dict(sales=743.8,ebit=82.5,net_income=69.1),'Q1_2026':dict(sales=831.9,ebit=117.4,net_income=103.3),'Q2_2026':dict(sales=850.3,ebit=119.4,net_income=105.0)}
# H1/annual use independently rounded reported numbers: Q1+Q2 EBIT differs 0.1.
results={'status':'partial_pre_event','valuation_ready':False,'fair_value':None,'price_regular_close_usd':37.36,'price_date':'2026-11-06','scanner_last_usd':37.34,'annual_interim_ttm':annual,'last_four_quarters':quarters,'ttm_formula':'FY2025 + H1_2026 - H1_2025','share_equivalents_H1_diluted_m':(301548372+342005388/10)/1e6,'share_equivalents_Q2_diluted_m':(302099852+337842515/10)/1e6,'h1_ebit_growth':236.9/169.8-1,'h1_net_growth_from_rounded_amounts':208.3/15.8-1,'h1_net_growth_reported':12.215,'ttm_sbc_pnl':62.6+33.5-25.5,'security_type':'NYSE Class A ordinary share, not ADR','lease_FY2025_cashflow':69.9,'lease_FY2025_note_principal':65.9,'lease_difference_unreconciled':4.0,'h1_fx_swing':2.9-(-154.4),'q2_footwear_share':781.6/850.3,'q2_apparel_share':54.2/850.3,'h1_cash_lease_debt_proxy':1205.6-87.9-474.6,'notes':['Cash after lease principal and all financing interest is a descriptive levered cash metric, NOT FCFF.','CFO adds back SBC and includes interest received; raw FCF is not economic FCFF. TTM SBC cash-flow addback72.3 differs from P&L SBC70.6.', 'FY2025 lease cash-flow69.9 differs from note principal65.9; do not silently replace. Interest separately reported.', 'H1 net-income growth reported1221.5% differs from rounded-value arithmetic1218.35%; both explicitly labeled.','No capital-cost or FX input is silently set; DCF and inverse remain blocked.','Share equivalents use economic nominal-value ratio A:B=10:1; period weighted shares are not current fully diluted shares.']}
(P/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(annual['2023']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in annual.items())
print(json.dumps({k:v for k,v in results.items() if k not in ['annual_interim_ttm','last_four_quarters']},indent=2))
