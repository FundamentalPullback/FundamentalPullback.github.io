import json,csv,math,pathlib,subprocess,sys,hashlib
p=pathlib.Path(__file__).parent
subprocess.run([sys.executable,str(p/'model.py')],check=True,capture_output=True)
r=json.loads((p/'results.json').read_text());h=r['history'];b=r['bridge'];cc=r['capital_cost'];checks={}
checks['history_revenue_ttm']=h['TTM2026']['revenue']==5902+5302-4295==6909
checks['history_cfo_ttm']=h['TTM2026']['cfo']==1450+1140-1006==1584
checks['history_fcf_ttm']=h['TTM2026']['reported_fcf']==1487
checks['three_years_four_quarters']=all(k in h for k in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026'])
checks['normalization']=h['TTM2026']['economic_ebita_before_contingent_normalization']==2169 and h['9M2026']['escrow_gain']==83 and h['9M2026']['earnout_expense']==-7
checks['debt_face_tie']=b['debt_face']==6650+759+413==7759+16+47
checks['capital_boundaries']=b['cash_surplus']==0 and b['fiduciary_cash_excluded']==2442 and b['restricted_cash_excluded']==271 and b['lease_liability_operating_not_deducted']==336
checks['wacc']=math.isclose(cc['wacc'],(cc['rf']+cc['beta']*cc['erp'])*cc['equity_weight']+cc['kd']*(1-cc['tax'])*cc['debt_weight'])
for name,c in r['cases'].items():
 rows=list(csv.DictReader((p/('forecast_'+name+'.csv')).open()));w=c['wacc'];t=c['terminal'];ev=sum(float(x['fcff'])/(1+w)**int(x['year']) for x in rows)+t['fcff']/(w-t['g'])/(1+w)**10
 checks[name+'_identity']=len(rows)==10 and all(math.isclose(float(x['fcff']),float(x['nopat'])+float(x['DA'])-float(x['capex'])-float(x['delta_wc'])-float(x['acquisition_reinvestment'])) for x in rows)
 checks[name+'_ev_to_price']=math.isclose((ev-b['debt_face']-b['earnouts']-b['nci'])/b['shares'],c['price'])
 checks[name+'_terminal']=math.isclose(t['fcff'],t['nopat']*(1-t['g']/t['roic'])) and t['g']<w and t['acquisition_reinvestment']==0
s=json.loads((p/'status.json').read_text());checks['approval_gate']=s['kind']=='partial' and s['maximumFundamentalPrice'] is None and s['signal'] is None and not s['entryApproved'] and s['approvedQuantity']==0
checks['audit_status_persists']=s['independentAudit']=='completed_not_decision_ready'
checks['csv_and_results_source_consistency']=all(r['checks'].values())
(p/'audit_checks.json').write_text(json.dumps(checks,indent=2));assert all(checks.values()),checks
print(json.dumps({'checks_passed':len(checks),'diagnostic':r['audit_diagnostics']['issuer_curve_yield']},indent=2))
