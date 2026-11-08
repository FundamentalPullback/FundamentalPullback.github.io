"""SLDE: puente histórico y diagnósticos; no emite valoración aprobada. USD millones."""
import json,csv,pathlib
D=pathlib.Path(__file__).parent
annual={2023:dict(gwp=874.726,npe=441.412,revenue=468.530,net_income=87.371,cfo=442.999,capex=8.677,source='S1'),2024:dict(gwp=1333.864,npe=792.439,revenue=846.814,net_income=201.125,cfo=553.886,capex=10.088,source='S2'),2025:dict(gwp=1795.516,npe=1079.528,revenue=1155.901,net_income=443.958,cfo=797.432,capex=2.857,source='S2')}
ytd={2024:dict(gwp=939.257,npe=567.843,revenue=608.361,net_income=126.032,cfo=395.481,capex=9.318),2025:dict(gwp=1177.027,npe=752.954,revenue=808.894,net_income=273.572,cfo=375.702,capex=2.314),2026:dict(gwp=1429.382,npe=1059.864,revenue=1137.150,net_income=412.607,cfo=547.039,capex=7.405)}
q={ '2025Q4':{k:annual[2025][k]-ytd[2025][k] for k in ytd[2025]},'2026Q1':dict(gwp=414.792,npe=365.883,revenue=389.283,net_income=139.527,eps_diluted=1.02),'2026Q2':dict(gwp=508.014,npe=360.635,revenue=386.817,net_income=134.850,eps_diluted=1.06),'2026Q3':dict(gwp=506.576,npe=333.346,revenue=361.051,net_income=138.230,eps_diluted=1.09)}
q['2026Q1'].update(cfo=289.488,capex=.679)
q['2026Q2'].update(cfo=590.011-289.488,capex=1.094-.679)
q['2026Q3'].update(cfo=547.039-590.011,capex=7.405-1.094)
ttm={y:{k:annual[y-1][k]+ytd[y][k]-ytd[y-1][k] for k in ytd[y]} for y in [2025,2026]}
for y in ttm:ttm[y]['cfo_less_capex_not_fcfe']=ttm[y]['cfo']-ttm[y]['capex']
book=1302.663;shares=117.320564;px=25.94;bps=book/shares
# RI perpetuo = BV + BV*(ROE-Ke)/(Ke-g). Solo prueba de expectativas, no valoración.
sens=[]
for ke in [.12,.14,.16]:
 for roe in [.15,.25,.35]:
  g=.03;v=bps*(roe-g)/(ke-g);sens.append(dict(ke_assumed=ke,roe_assumed=roe,g_assumed=g,diagnostic_value=v,upside=v/px-1))
# Un dividendo no crea valor: base postdividendo + cobro = base previa, sin demás movimientos.
div=1.57;postbook=book-div*shares
out=dict(ticker='SLDE',as_of='2026-11-08',research_status='material_partial',stage3_completed=False,stage35_approved=False,approved_values=None,approved_price=None,price=dict(regular_close=px,date='2026-11-06',session='16:00 America/New_York',scanner_last=25.58,scanner_session='after_hours 19:30 America/New_York',sources=['S8','S9']),annual=annual,quarters=q,ytd=ytd,ttm=ttm,ttm_growth={k:ttm[2026][k]/ttm[2025][k]-1 for k in ytd[2026]},book=book,shares_period_end=shares,book_per_share=bps,price_book=px/bps,special_plus_regular_dividend=div,proforma_book_after_announced_dividends=postbook,diagnostic_sensitivity=sens,reverse_roe=[dict(ke_assumed=ke,g_assumed=.03,required_roe=.03+(px/bps)*(ke-.03)) for ke in [.12,.14,.16]],q3_quality=dict(reported_net_income=138.230,pretax=161.746,favorable_reserve_development=18,net_at_assumed_25pct_tax_ex_reserve_release=(161.746-18)*.75,warning='No es beneficio sostenible: mantiene siniestros observados y no carga catastrófica esperada'),cat_stress=dict(first_event_modeled_retention=166.8,second_event_modeled_retention=150,combined_arithmetic_not_probability=316.8,after_tax_at_assumed_25pct=316.8*.75,as_pct_gaap_equity=316.8*.75/book,warning='No es límite de pérdida contractual ni estrés regulatorio completo; no sumar de nuevo como cat load a un caso que ya lo incorpore.'),ke_current=None,sustainable_roe=None,regulatory_distribution_capacity=None)
out['latest_reported_basic_shares_m']=117.248652
out['latest_shares_date']='2026-10-29'
out['book_denominator_date']='2026-09-30'
out['dividend_proforma_basis']='September shares held constant; actual November record-date shares not yet known'
out['scanner_pullback_diagnostic']={'high_assumed':29.145,'afterhours_pct':100*(1-25.58/29.145),'regular_close_pct':100*(1-25.94/29.145),'afterhours_component':50,'regular_component':40,'conditional_score_if_other_points_unchanged':75,'technical_score_revalidated':False}
out['regulatory_capital_evidence']={'sic_surplus':503.095,'sic_minimum_surplus':79.534,'arithmetic_excess_not_distributable':503.095-79.534,'ssic_reported_surplus':48.373,'ssic_capital_stock':1.5,'rbc_above_company_action_level':True,'rbc_ratio_disclosed':None,'holding_remittance_capacity':None}
assert abs(sum(v['cfo'] for v in q.values())-ttm[2026]['cfo'])<1e-8
assert abs(sum(v['capex'] for v in q.values())-ttm[2026]['capex'])<1e-8
(D/'results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
with (D/'financial_history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period','gwp_usdm','npe_usdm','revenue_usdm','net_income_usdm','cfo_usdm','capex_usdm','basis'])
 for p,a in [(str(y),v) for y,v in annual.items()]+list(q.items())+[(f'TTM_Sep_{y}',v) for y,v in ttm.items()]:w.writerow([p]+[round(a[k],6) if k in a else '' for k in ['gwp','npe','revenue','net_income','cfo','capex']]+['Annual audited / quarterly unaudited / Q4=FY-9M / TTM=FY+9M-9M prior'])
assert abs(sum(v['net_income'] for v in q.values())-ttm[2026]['net_income'])<.002
assert abs(sum(v['revenue'] for v in q.values())-ttm[2026]['revenue'])<.002
assert all(x['ke_assumed']>x['g_assumed'] for x in sens)
assert out['approved_values'] is None
print(json.dumps({k:out[k] for k in ['ttm','ttm_growth','book_per_share','price_book','reverse_roe','q3_quality']},indent=2))
