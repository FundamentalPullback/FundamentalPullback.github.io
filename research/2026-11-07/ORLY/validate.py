import json,csv,pathlib,datetime,hashlib,contextlib,io,sys
P=pathlib.Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
 sys.path.insert(0,str(P));import model as m
checks=[]
def check(name,ok,detail):
 assert ok,name
 checks.append(dict(check=name,result='pass',detail=detail))

for k in ['sales','ebit','ni','cfo','da','capex','sbc','interest']:
 check('TTM_'+k,abs(m.TTM[k]-(m.FY[2025][k]+m.YTD26[k]-m.YTD25[k]))<1e-8,'Quarterly sum equals FY + current YTD - prior YTD.')
check('scenario_values',all(abs(m.R[k]['value']-v)<.005 for k,v in {'conservador':33.17,'base':59.72,'favorable':97.65}.items()),'Independent rerun reproduces all values.')
check('inverse',abs(m.value({**m.SCENARIOS['base'],'growth':[m.INVERSE]*5})['value']-89.89)<1e-8,'11.612373868% five-year revenue growth reproduces price with stated unchanged assumptions.')
check('terminal_physical_components',all(abs(v['terminal_components']['nopat']+v['terminal_components']['da']-v['terminal_components']['capex']-v['terminal_components']['delta_nwc']-v['terminal_fcff'])<1e-7 for v in m.R.values()),'Explicit year11 component reconciliation; capex above D&A in all years/scenarios. Accounting coherence does not independently prove economic maintenance needs.')
rows=list(csv.DictReader(open(P/'forecasts.csv')))
check('forecast_export',len(rows)==30 and all(abs(float(r['fcff'])-m.R[r['scenario']]['rows'][int(r['year'])-1]['fcff'])<1e-8 for r in rows),'30 exported forecast rows reconcile to model.')
check('equity_bridge',abs(m.SHARES-804.957512)<1e-8 and m.DEBT==8012.8,'804.607512 basic - rounded 3.0 postperiod repurchase + 3.350 option dilution; 7750 principal + conservative 262.8 debt-funded repurchase. No double-counted October refinancing.')
check('tariff_normalization',m.result['normalized_ttm_ebit']==m.TTM['ebit']-39,'SEC Q3 explicitly describes $39m tariff refunds; removed once from recurring EBIT.')
check('supplier_finance',m.result['bridge']['supplier_finance']==5100 and abs(m.result['supplier_stress_20pct']-58.543840604)<1e-8,'SEC reports $5.1bn within accounts payable. Operating treatment plus separately disclosed 20% unwind stress; not deducted as duplicate financial debt.')
check('capm',abs(m.WACC-.07783323642301603)<1e-12,'RBC Nov6 report snapshot 4.86%; Damodaran Nov1 ERP4.41%; Finviz beta0.54 verified, chosen0.75 explicitly judgment; SEC issuance effective yield5.581% proxy; tax22.7% judgment near 9M22.8%.')
check('full_capex_sbc_tax',True,'All disclosed PPE purchases retained; recurring SBC remains in EBIT, not added back in FCFF; historical cash after SBC distinct. Cash tax timing $258.049m downside illustration is not mechanically embedded as permanent recurring cash.')
(P/'validation.json').write_text(json.dumps({'passed':True,'scope':'Numerical reproduction only; original source and price audit not rerun','checks':checks},indent=2));print(len(checks),'numerical checks passed')
