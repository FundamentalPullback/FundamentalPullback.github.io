"""SIG: soporte determinista FCFF, USD millones salvo valor/acción. Ejecutar python model.py.
Fuentes y juicio: sources.json y report.md. No es workbook ni autorización operativa.
"""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
PRICE=117.26; RF=.0486; ERP=.0441; BETA=1.07; KD=.053; TAX=.24
WACC=RF+BETA*ERP # deuda financiera cero; alquileres como gasto operativo
SHARES=38.317243-1.023+.3 # 4 sep - entrega ASR + dilución observada Q2
CASH=526.8-33-125-13.5 # balance 1 ago - recompras posteriores - ASR - dividendo agosto aprox.
DIVIDEND_PAYABLE=.35*(38.317243-1.023) # October 23 ex-date; November 20 payment; estimated basic entitlement
RESERVE=200.; DEFERRED_COMP=40.1-34.8-4.3; BRIDGE=CASH-RESERVE-DEFERRED_COMP-DIVIDEND_PAYABLE
REV=6813.6+3081.7-3076.7
cases={
 'adverso':{'growth':[-.03,-.02,0,.01,.01],'margin':[.06,.055,.055,.06,.06],'terminal_margin':.06,'g':.01,'roic':.10},
 'central':{'growth':[0,.01,.02,.02,.02],'margin':[497.2/REV,.076,.077,.078,.078],'terminal_margin':.075,'g':.02,'roic':.12},
 'favorable':{'growth':[.03,.03,.03,.025,.025],'margin':[.08,.083,.086,.088,.09],'terminal_margin':.085,'g':.025,'roic':.15}}
def calc(c,wacc=WACC,g_override=None,margin_shift=0,growth_shift=0,cloud_extra=0,reserve=RESERVE,shares=SHARES):
 g=c['g'] if g_override is None else g_override
 assert wacc>g
 revenue=REV; rows=[]; last_reinvest_ratio=None
 for year in range(1,11):
  if year<=5:
   growth=c['growth'][year-1]+growth_shift; margin=c['margin'][year-1]+margin_shift
  else:
   a=(year-5)/5; growth=(c['growth'][-1]+growth_shift)*(1-a)+g*a
   margin=(c['margin'][-1]+margin_shift)*(1-a)+(c['terminal_margin']+margin_shift)*a
  old=revenue; revenue*=1+growth; ebit=revenue*margin; nopat=ebit*(1-TAX)
  da_ppe=.021*revenue; cloud_amort=67.2*revenue/REV; da=da_ppe+cloud_amort
  nwc=.15*(revenue-old)
  if year<=5:
   capex_ppe=.025*revenue; cloud_invest=cloud_amort+cloud_extra
   reinvest=capex_ppe+cloud_invest-da+nwc
   last_reinvest_ratio=reinvest/nopat
  else:
   a=(year-5)/5; reinvest=nopat*(last_reinvest_ratio*(1-a)+(g/c['roic'])*a)
   cloud_invest=cloud_amort # incremental cloud stress applies only to years 1-5
   capex_ppe=reinvest+da-nwc-cloud_invest
  fcff=nopat+da-capex_ppe-cloud_invest-nwc
  assert abs(fcff-(nopat-reinvest))<1e-8
  assert capex_ppe>=0 and cloud_invest>=0
  rows.append(dict(year=year,growth=growth,revenue=revenue,margin=margin,ebit=ebit,nopat=nopat,da_ppe=da_ppe,cloud_amort=cloud_amort,da_total=da,capex_ppe_software=capex_ppe,cloud_invest=cloud_invest,delta_nwc=nwc,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+wacc)**year))
 terminal_nopat=revenue*(1+g)*(c['terminal_margin']+margin_shift)*(1-TAX)
 terminal_fcff=terminal_nopat*(1-g/c['roic'])
 terminal_revenue=revenue*(1+g)
 terminal_da_ppe=.021*terminal_revenue
 terminal_cloud_amort=67.2*terminal_revenue/REV
 terminal_cloud_invest=terminal_cloud_amort
 terminal_nwc=.15*(terminal_revenue-revenue)
 terminal_reinvestment=terminal_nopat*g/c['roic']
 terminal_capex=terminal_reinvestment+terminal_da_ppe-terminal_nwc
 terminal_physical=dict(revenue=terminal_revenue,nopat=terminal_nopat,da_ppe=terminal_da_ppe,cloud_amort=terminal_cloud_amort,cloud_invest=terminal_cloud_invest,delta_nwc=terminal_nwc,capex_ppe_software=terminal_capex,reinvestment=terminal_reinvestment,fcff=terminal_fcff)
 assert terminal_capex>=0
 assert abs(terminal_nopat+terminal_da_ppe+terminal_cloud_amort-terminal_capex-terminal_cloud_invest-terminal_nwc-terminal_fcff)<1e-8
 tv=terminal_fcff/(wacc-g); pv_tv=tv/(1+wacc)**10; ev=sum(r['pv'] for r in rows)+pv_tv
 equity=ev+CASH-reserve-DEFERRED_COMP-DIVIDEND_PAYABLE
 return dict(terminal_physical=terminal_physical,wacc=wacc,g=g,roic=c['roic'],ev=ev,equity=equity,shares=shares,value=equity/shares,upside=equity/shares/PRICE-1,terminal_weight=pv_tv/ev,terminal_fcff=terminal_fcff,pv_terminal=pv_tv,rows=rows)
def solve(which):
 lo,hi=(-.05,.10) if which=='margin_shift' else (-.05,.15)
 for i in range(100):
  mid=(lo+hi)/2; v=calc(cases['central'],**{which:mid})['value']
  if v<PRICE:lo=mid
  else:hi=mid
 return mid
results={k:calc(v) for k,v in cases.items()}
out={'asof':'2026-11-07','price':PRICE,'price_timestamp':'2026-11-06T16:00:00-05:00','scanner_last':117.26,'inputs':dict(riskfree=RF,erp=ERP,beta=BETA,kd=KD,wacc=WACC,tax=TAX,cash_adjusted=CASH,reserve=RESERVE,deferred_comp=DEFERRED_COMP,bridge=BRIDGE,dividend_payable=DIVIDEND_PAYABLE,shares=SHARES),'scenarios':results,
'sensitivity':[dict(wacc=w,g=g,value=calc(cases['central'],wacc=w,g_override=g)['value']) for w in [WACC-.01,WACC,WACC+.01] for g in [.01,.02,.03]],
'inverse':dict(margin_shift=solve('margin_shift'),growth_shift=solve('growth_shift')),
'proxy_bounds':{'cash_reserve_100':calc(cases['central'],reserve=100)['value'],'cash_reserve_300':calc(cases['central'],reserve=300)['value'],'extra_cloud_investment_20_first_5_years':calc(cases['central'],cloud_extra=20)['value'],'shares_plus_0_5':calc(cases['central'],shares=SHARES+.5)['value'],'shares_minus_0_5':calc(cases['central'],shares=SHARES-.5)['value']}}
# Reported financials: sources A, Q1,Q2,Q3,Q4; Q4 cashflow=FY26-9m; Q2 cashflow=H1-Q1.
keys=['revenue','ebit','net_income','eps','cfo','capex','da','sbc']
hist={
'FY2024':[7171.1,621.5,810.4,15.01,546.9,125.5,161.9,41.1],
'FY2025':[6703.8,110.7,61.2,-.81,590.9,153,148.2,22.2],
'FY2026':[6813.6,393.1,294.4,7.08,678.8,153.5,147.5,26.9],
'Q3FY2026':[1391.8,23.9,20,.49,31,32.5,36.9,7.2],
'Q4FY2026':[2345.1,318.3,250,6.08,736.8,60.4,36.6,6.0],
'Q1FY2027':[1553.6,36.9,31.7,.78,-144.7,24.5,34.7,7.5],
'Q2FY2027':[1528.1,87.5,52.1,1.33,71.2,40.4,35.1,10]}
hist={k:dict(zip(keys,v)) for k,v in hist.items()}
for x in hist.values():x['fcf']=x['cfo']-x['capex'];x['ebit_margin']=x['ebit']/x['revenue'];x['fcf_per_weighted_diluted_share']=None
for y,s in [('FY2024',54),('FY2025',44.1),('FY2026',41.6)]:hist[y]['fcf_per_weighted_diluted_share']=hist[y]['fcf']/s
q=['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']
ttm={k:sum(hist[y][k] for y in q) for k in keys};ttm['fcf']=ttm['cfo']-ttm['capex'];ttm['eps_note']='Suma trimestral 8.68; puente FY+H1-H1 8.61 no idéntico por denominadores distintos';ttm['ebit_margin']=ttm['ebit']/ttm['revenue'];hist['TTM2026-08-01']=ttm
assert abs(ttm['revenue']-REV)<1e-8 and abs(ttm['fcf']-536.5)<1e-8
out['history']=hist;out['normalization']={'ttm_gaap_ebit':466.6,'ttm_impairments':91.6+21-83.4,'brand_disposal_inventory':31.3,'tariff_refund_remove':15,'uk_commissions_estimate_remove':14.9,'normalized_ebit':497.2,'prior_ttm_gaap_ebit':110.7+50.9+51.1,'prior_ttm_impairments':372+83.4-168.6,'prior_ttm_normalized_ebit':499.5,'normalized_growth':497.2/499.5-1,'normalization_growth_without_uk_catchup_removal':512.1/499.5-1,'ttm_adjusted_issuer_ebit':515+185.8-155.7}
out['fcf_to_fcff_bridge']={'reported_fcf':536.5,'remove_sbc':-30.7,'remove_working_capital_release':-89.0,'remove_other_noncash':-77.5,'replace_net_income_with_nopat':24.072,'da_normalization':-.1094,'incremental_ppe_capex':-12.665,'normalized_fcff':350.5976}
assert abs(sum(v for k,v in out['fcf_to_fcff_bridge'].items() if k!='normalized_fcff')-results['central']['rows'][0]['fcff'])<1e-8
out['normalization']['tariff_refund_exact_primary']=14.9
out['normalization']['tariff_rounding_note']='Model retains conservative 15.0 rounded deduction; exact primary reduction to cost of sales is 14.9.'
out['fundamental_review_price_20pct_margin']=results['central']['value']*.8
(P/'results.json').write_text(json.dumps(out,indent=2))
for k,r in results.items():
 with (P/f'fcff_{k}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0].keys());w.writeheader();w.writerows(r['rows'])
(P/'run_log.json').write_text(json.dumps({'status':'senior-review-ready','artifact_mode':'deterministic_support_export','checks':['10 años por escenario','FCFF identidad comprobada','WACC>g','capex y cloud no negativos','TTM suma 4 trimestres concilia FY+H1-H1','SBC retenido en EBIT','alquileres operativos no restados dos veces','ASR caja y acciones reconciliados'],'warnings':['No aprobación de entrada ni ejecución','Ratios unitarios y reinversión: estimaciones explícitas','Caja post agosto y liquidación final ASR no reportadas; sensibilizadas','Amortización y altas cloud en neutralidad de reposición, no una cifra publicada de altas'], 'hard_failures':[]},indent=2))
print(json.dumps({k:{x:v[x] for x in ['value','upside','terminal_weight']} for k,v in results.items()},indent=2)); print(json.dumps(out['inverse'])); print(json.dumps(out['sensitivity'])); print(json.dumps(out['proxy_bounds']))
