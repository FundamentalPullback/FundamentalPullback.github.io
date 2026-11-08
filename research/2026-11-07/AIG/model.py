"""Residual income / FCFE; USD millones. Capital regulatorio no equivale a patrimonio GAAP."""
from pathlib import Path
import json,csv
P=Path(__file__).parent
BOOK=38883-88 # September common book less disclosed October repurchases; no unreported earnings assumed.
SHARES=518.438878+4.261278 # October basic plus Q3 incremental diluted proxy.
PRICE=77.75
S={'prudente':dict(roe1=.075,roe10=.085,ke=.115,capital_growth=.03,g=.02,year1_additional_loss=1975,payout_cap=1400,hold_years=2),'central':dict(roe1=.09,roe10=.105,ke=.105,capital_growth=.035,g=.025,year1_additional_loss=300,payout_cap=2600,hold_years=0),'favorable':dict(roe1=.115,roe10=.13,ke=.095,capital_growth=.04,g=.03,year1_additional_loss=100,payout_cap=3200,hold_years=0)}
def calc(a,terminal_roe=None,ke=None):
 a=a.copy();a['roe10']=a['roe10'] if terminal_roe is None else terminal_roe;a['ke']=a['ke'] if ke is None else ke
 b=BOOK;pv=ri=0;rows=[]
 for y in range(1,11):
  roe=a['roe1']+(a['roe10']-a['roe1'])*(y-1)/9;income=b*roe-(a['year1_additional_loss'] if y==1 else 0)
  capital_growth=a['capital_growth']+(a['g']-a['capital_growth'])*min(max(y-5,0),5)/5
  required=b*capital_growth;available=max(0,income-required)
  cap=a['payout_cap']*(1+a['capital_growth'])**(y-1) if y<=3 else available
  distribution=0 if y<=a['hold_years'] else min(available,cap)
  end=b+income-distribution;residual=income-a['ke']*b
  pv+=distribution/(1+a['ke'])**y;ri+=residual/(1+a['ke'])**y
  rows.append(dict(year=y,opening_book=b,roe=roe,net_income=income,target_retained_capital=required,fcfe=distribution,actual_retention=income-distribution,ending_book=end,residual_income=residual,capital_growth_target=capital_growth,unfunded_target_capital=max(0,required-(income-distribution)),remittance_capacity_validated=False,approved_distribution=None));b=end
 terminal_income=b*a['roe10'];terminal_fcfe=terminal_income-b*a['g'];tv=terminal_fcfe/(a['ke']-a['g']);value=pv+tv/(1+a['ke'])**10
 ri_value=BOOK+ri+(a['roe10']-a['ke'])*b/(a['ke']-a['g'])/(1+a['ke'])**10
 assert abs(value-ri_value)<1e-7
 return dict(assumptions=a,rows=rows,terminal_fcfe=terminal_fcfe,equity_fcfe=value,equity_ri=ri_value,price=value/SHARES,terminal_pv_weight=tv/(1+a['ke'])**10/value)
def main():
 r={k:calc(a) for k,a in S.items()};lo,hi=.04,.25
 for _ in range(100):
  m=(lo+hi)/2
  if calc(S['central'],terminal_roe=m)['price']<PRICE:lo=m
  else:hi=m
 r['inverse']={'terminal_roe_with_linear_path':(lo+hi)/2,'price':PRICE,'other_assumptions':'central'}
 r['approval']={'approved_values':None,'approved_price':None,'entry_approved':False,'statutory_remittance_validated':False,'stress_capital_validated':False}
 r['cost_capital']={'rf':.0486,'rf_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','erp_source_rf':.0529,'beta_assumed':1.0,'mechanical_ke':.0927,'date_basis_mismatch':True}
 r['sensitivity']=[dict(ke=k,terminal_roe=q,price=calc(S['central'],terminal_roe=q,ke=k)['price']) for k in [.095,.105,.115] for q in [.085,.105,.125]]
 r['normalization']={'adjusted_ttm':4373,'gi_earned_ttm':24674,'illustrative_reserve_release_removed_pretax':24674*.021,'reported_cat_ttm':798,'normal_cat_budget_5pct':24674*.05,'recurring_restructuring_ttm_pretax':439+247-307,'additional_parent_income_reduction':25,'tax_rate':.24,'illustrative_normal_income':4373-(24674*.021+24674*.05-798+439+247-307)*.76-25}
 (P/'model_results.json').write_text(json.dumps(r,indent=2))
 for k in S:
  with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=r[k]['rows'][0]);w.writeheader();w.writerows(r[k]['rows'])
 print({k:r[k]['price'] for k in S});print(r['inverse']);print(r['normalization'])
if __name__=='__main__':main()
