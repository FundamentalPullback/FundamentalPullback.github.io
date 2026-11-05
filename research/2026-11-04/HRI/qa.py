from pathlib import Path
import json,math
p=Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());f=json.loads((p/'facts/inputs.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text());c=json.loads((p/'comparables/outputs.json').read_text());r=(p/'report.md').read_text();checks=[]
def ck(n,v):
 assert v,n
 checks.append(n)
for k in ['q3','q3_prior','ytd','ytd_prior']:
 z=f[k];b=a[k];ck(k+' ebit',b['ebit']==z['pretax']+z['interest_net']+z['other_expense_net']);ck(k+' margin',math.isclose(b['margin'],b['ebit']/z['revenue']));ck(k+' limited normalization',b['limited_ebit_ex_transaction_disposal_impairment']==b['ebit']+z['transaction']+z.get('held_for_sale_loss',0))
for k in ['ytd','ytd_prior']:
 z=f[k];b=a[k];ck(k+' published fcf',b['fcf_issuer']==z['fcf_published']);ck(k+' fcfSBC',b['fcf_less_sbc_proxy']==b['fcf_issuer']-z['sbc']);ck(k+' supplier sensitivity',b['illustrative_cash_fcf_less_fleet_ap_increase']==b['fcf_issuer']-(z['fleet_ap_end']-z['fleet_ap_start']))
ck('nominal debt',a['capital']['nominal_debt_incl_finance_leases']==8080);ck('carrying tieout',8080-f['capital']['unamortized_debt_cost']==f['capital']['debt_carrying']);ck('subtotal not bridge',a['capital']['nominal_debt_financing_less_cash']==8113 and a['equity_bridge'] is None);ck('leases separate',a['capital']['operating_leases']==1502);ck('liquidity not cash',a['capital']['liquidity_cash_plus_abl']==2100);ck('rate stress',math.isclose(a['capital']['one_pct_rate_stress_annual_pretax'],32.44));ck('op balance cash',a['ytd_operating_assets_liabilities_cash_change']==-166)
for k in ['bear','base','bull','owner_fcf','equity_bridge']:
 ck(k+' null',a[k] is None and m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+' false',a[k] is False and m[k] is False)
ck('price discrepancy',m['certified_close'] is None and m['price']!=m['scanner_price']);ck('calendar unknown',f['next_earnings'] is None);ck('no target multiple',c['multiple_target'] is None)
for key in ['pros_es','pros_en','cons_es','cons_en']:
 ck(key+' exists',bool(m[key]))
 for t in m[key]:ck(key+' exact excerpt',t in r)
for period in ['FY2023','FY2024','FY2025','2025Q4','2026Q1','2026Q2','2026Q3','TTM2025Q3','TTM2026Q3']:ck('history '+period,period in h['periods'])
ck('TTM EBIT',h['periods']['TTM2026Q3']['operating_ebit']['value']==653);ck('TTM FCF',h['periods']['TTM2026Q3']['fcf_after_net_capex']['value']==299);ck('TTM EPS null',h['periods']['TTM2026Q3']['eps_diluted']['value'] is None)
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'QA passed')
