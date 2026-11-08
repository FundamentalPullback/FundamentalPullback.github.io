"""RBA evidence workbook in executable form. USD millions. No approved valuation.
python model.py writes historical reconciliations; dcf_fcff is gated until bridges resolve.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
fields=['gtv','service_revenue','inventory_revenue','revenue','ebit','net_income','common_income','da','cfo','ppe_additions','intangible_additions','disposals','sbc_cashflow','acquisition_cash']
rows={
 'FY2023':[13930.6,2732.5,947.1,3679.6,471.3,206,174.9,352.2,544,227.9,118.3,32.6,55.8,2778.6],
 'FY2024':[15904.8,3363.6,920.6,4284.2,761.2,412.8,372.7,444.4,932,167.4,109.5,2.6,62.4,8.6],
 'FY2025':[16201.9,3502.2,1088.5,4590.7,713.4,427.6,382.2,483.4,978.2,259,116.5,5.3,66,192.8],
 'H12024':[8181.5,1708.2,452.6,2160.8,400.8,218.4,197.8,218,462.1,73.9,56.2,1,35.1,0],
 'H12025':[8027,1739.7,554.9,2294.6,378.1,223,202.4,231.2,483.3,139.1,61.2,2.1,41.6,0],
 'H12026':[9013.6,1831.1,720.6,2551.7,442.3,279.2,256.6,257.1,365.8,129.6,54.3,3.3,33.5,331.1],
 '9M2025':[11920.8,2584.7,802.6,3387.3,536.4,318.2,283.1,355.9,723,190.3,91.2,4.4,64.4,163.6],
 'Q12026':[4340.9,897.7,336.9,1234.6,217.5,135.6,124.6,126.7,224.1,51.5,27.8,2.4,15.6,0],
}
d={k:dict(zip(fields,v)) for k,v in rows.items()}
def combine(a,b,c=None):return {k:round(a[k]+b[k]-(c[k] if c else 0),4) for k in fields}
def subtract(a,b):return {k:round(a[k]-b[k],4) for k in fields}
d['Q32025']=subtract(d['9M2025'],d['H12025'])
d['Q42025']=subtract(d['FY2025'],d['9M2025'])
d['Q22026']=subtract(d['H12026'],d['Q12026'])
d['TTM2026-06']=combine(d['FY2025'],d['H12026'],d['H12025'])
d['TTM2025-06']=combine(d['FY2024'],d['H12025'],d['H12024'])
for v in d.values():
 v['cash_fcf_before_disposals']=round(v['cfo']-v['ppe_additions']-v['intangible_additions'],4)
 v['cash_fcf_net_disposals']=round(v['cash_fcf_before_disposals']+v['disposals'],4)
 v['cash_after_acquisitions']=round(v['cash_fcf_before_disposals']-v['acquisition_cash'],4)
 v['ebit_margin']=v['ebit']/v['revenue']
 v['service_take_rate']=v['service_revenue']/v['gtv']
# FCFF is not CFO less capex: no attempt to relabel the historical cash proxies above.
def dcf_fcff(case):
 """5 explicit + 5 linear transition years, after operating leases; no free growth.
 Required inputs are independently supplied, NOT defaulted from the scanner.
 Transition reinvestment funds next-year incremental NOPAT / incremental ROIC.
 Explicit capex5 is cash PP&E only; software5 and finance_lease_additions5 exclude it.
 Acquisition and working-capital schedules must not overlap acquired balances.
 Year11 uses terminal growth and margin. No EV-to-common bridge is implemented.
 Tax rate and WACC must be internally consistent. SBC remains in EBIT.
 """
 if case.get('material_bridges_verified') is not True:raise ValueError('Material normalization/capital bridges unresolved; valuation withheld')
 rev=case['revenue0'];out=[]
 for y in range(1,11):
  if y<=5:
   g=case['growth5'][y-1];m=case['margin5'][y-1];rev*=1+g;n=rev*m*(1-case['tax']);
   reinv=case['capex5'][y-1]+case['software5'][y-1]+case['finance_lease_additions5'][y-1]+case['acquisitions5'][y-1]+case['nwc_change5'][y-1]-case['da5'][y-1]
  else:
   t=(y-5)/5;g=case['growth5'][-1]*(1-t)+case['terminal_g']*t;m=case['margin5'][-1]*(1-t)+case['terminal_margin']*t
   rev*=1+g;n=rev*m*(1-case['tax']);roic=case['roic5']*(1-t)+case['terminal_roic']*t
   tn=min(1,(y+1-5)/5);gn=case['growth5'][-1]*(1-tn)+case['terminal_g']*tn;mn=case['margin5'][-1]*(1-tn)+case['terminal_margin']*tn
   if roic<=0:raise ValueError('Positive incremental ROIC required')
   next_nopat=rev*(1+gn)*mn*(1-case['tax']);reinv=(next_nopat-n)/roic
  fcff=n-reinv;out.append(dict(year=y,revenue=rev,growth=g,margin=m,nopat=n,reinvestment=reinv,fcff=fcff,pv=fcff/(1+case['wacc'])**y))
 assert case['wacc']>case['terminal_g'] and case['terminal_roic']>case['terminal_g']
 n11=out[-1]['nopat']*(1+case['terminal_g']);fcff11=n11*(1-case['terminal_g']/case['terminal_roic']);tv=fcff11/(case['wacc']-case['terminal_g']);pvt=tv/(1+case['wacc'])**10
 ev=sum(x['pv'] for x in out)+pvt
 return dict(forecast=out,ev=ev,terminal_weight=pvt/ev,fcff11=fcff11)
if __name__=='__main__':
 cols=list(next(iter(d.values())))
 with (P/'historical_financials.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['period']+cols);w.writeheader();w.writerows(dict(period=k,**v) for k,v in d.items())
 t,p=d['TTM2026-06'],d['TTM2025-06']
 growth={k:t[k]/p[k]-1 for k in ['revenue','service_revenue','ebit','net_income','common_income','cfo','cash_fcf_before_disposals']}
 debt=[(18.5,.0534),(580,.052),(68.6,.0408),(902.5,.0516),(550,.0675),(800,.0775)]
 kd=sum(a*b for a,b in debt)/sum(a for a,b in debt)
 ke=.0484+.47*.0441
 results={'as_of':'2026-11-08','status':'partial_not_decision_ready','historical':d,'ttm_yoy':growth,'reference_price':93.52,'reference_price_time':'2026-11-06T16:00:00-05:00','scanner_last':93.52,'stage3_complete':False,'fair_value':None,'purchase_ceiling':None,'scenarios':None,'inverse_valuation':None,'capital_cost_diagnostics':{'beta_5y':.47,'beta_date':'2026-11-08','rf_DGS10':.0484,'rf_observation_date':'2026-11-05','erp':.0441,'erp_date':'2026-11-01','ke_CAPM':ke,'weighted_issuer_contractual_cost_of_debt_2026_06_30':kd,'warning':'No son WACC aprobado ni coste marginal de deuda al 6 noviembre. ERP y Treasury tienen fechas diferentes; beta atraviesa adquisición IAA.'},'fcff_model':'Uncalibrated EV-only architecture; finance-lease additions required; next-year incremental NOPAT funds transition growth. No EV-to-common bridge, scenarios or inverse implemented. Not run with invented normalized inputs','normalization_diagnostics':{'reported_ebit_ttm':777.6,'dst_reversal_h1_2026':11.2,'ebit_after_dst_only':766.4,'normalized_ebit_approved':None},'cash_definition_bridge':{'provider_fcf':611.2,'intangible_additions_omitted_by_provider':109.6,'consistent_cash_fcf':501.6,'normalized_fcff':None}}
 (P/'results.json').write_text(json.dumps(results,indent=2))
 checks={'revenue_components_all_periods':all(abs(v['revenue']-v['service_revenue']-v['inventory_revenue'])<.11 for v in d.values()),'four_quarters_sum_to_ttm':all(abs(sum(d[q][k] for q in ['Q32025','Q42025','Q12026','Q22026'])-t[k])<.11 for k in fields),'valuation_gate':False}
 try:dcf_fcff({})
 except ValueError:checks['valuation_gate']=True
 assert all(checks.values());(P/'self_check.json').write_text(json.dumps(checks,indent=2));print(json.dumps({'ttm':t,'growth':growth,'capital':results['capital_cost_diagnostics'],'checks':checks},indent=2))
