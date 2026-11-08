"""Funded clean-surplus RI and FCFE cross-check; USD millions. Conditional assumptions."""
from pathlib import Path
import json,csv
P=Path(__file__).parent;BOOK=16182;SHARES=155.1;PRICE=185.48
PREMIUM=10180;EQPORT=13145;NON_EQ_INCOME=(731+31-14)*4/3;RESIDUAL=-136
S={'prudente':dict(cr=1.00,equity_total_return=.03,tax=.21,ke=.117,growth=.035,terminal_g=.025,shock=987+EQPORT*.20*.79+18925*.064*.79,hold_years=2),'central':dict(cr=.96,equity_total_return=.06,tax=.20,ke=.106,growth=.05,terminal_g=.03,shock=0,hold_years=0),'favorable':dict(cr=.92,equity_total_return=.08,tax=.19,ke=.097,growth=.065,terminal_g=.035,shock=0,hold_years=0)}
def calc(a,equity_return=None):
 a=a.copy()
 if equity_return is not None:a['equity_total_return']=equity_return
 components=dict(underwriting=PREMIUM*(1-a['cr']),non_equity_recurring_investment_income=NON_EQ_INCOME,equity_total_return=EQPORT*a['equity_total_return'],life_corporate_interest_residual=RESIDUAL)
 roe=sum(components.values())*(1-a['tax'])/BOOK;b0=BOOK-a['shock'];b=b0;pvri=pvcf=0;rows=[]
 for y in range(1,11):
  ni=b*roe;target_growth=a['growth']+(a['terminal_g']-a['growth'])*min(max(y-5,0),5)/5;growth=roe if y<=a['hold_years'] else target_growth;retained=b*growth;fcfe=ni-retained;ri=ni-a['ke']*b
  rows.append(dict(year=y,opening_equity=b,roe=roe,net_income=ni,retained_capital=retained,fcfe=fcfe,residual_income=ri,closing_equity=b+retained,target_capital=b*target_growth,unfunded_target_capital=max(0,b*target_growth-retained),approved_distribution=None,statutory_remittance_validated=False,cash_realization_validated=False));pvri+=ri/(1+a['ke'])**y;pvcf+=fcfe/(1+a['ke'])**y;b+=retained
 tvri=(roe-a['ke'])*b/(a['ke']-a['terminal_g']);tvcf=(roe-a['terminal_g'])*b/(a['ke']-a['terminal_g']);value=b0+pvri+tvri/(1+a['ke'])**10;cross=pvcf+tvcf/(1+a['ke'])**10
 assert abs(value-cross)<1e-7 and all(x['fcfe']>=0 for x in rows)
 return dict(assumptions=a,earnings_components_on_current_capital=components,normalized_roe=roe,initial_book_after_stress=b0,rows=rows,ri_equity=value,fcfe_equity=cross,price=value/SHARES,terminal_fcfe=(roe-a['terminal_g'])*b)
def main():
 r={k:calc(v) for k,v in S.items()};lo,hi=0,.30
 for _ in range(100):
  m=(lo+hi)/2
  if calc(S['central'],m)['price']<PRICE:lo=m
  else:hi=m
 r['inverse']={'equity_portfolio_annual_total_return':(lo+hi)/2,'implied_normalized_roe':calc(S['central'],(lo+hi)/2)['normalized_roe'],'other_assumptions':'central','price':PRICE}
 r['approval']={'approved_values':None,'approved_price':None,'entry_approved':False,'statutory_capital_validated':False,'remittance_validated':False}
 r['cost_capital']={'rf':.0486,'rf_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','erp_source_rf':.0529,'beta_assumed_central':1.1,'date_basis_mismatch':True}
 r['sensitivity']=[dict(ke=ke,equity_return=er,price=calc(dict(S['central'],ke=ke),er)['price']) for ke in [.097,.106,.117] for er in [.03,.06,.08]]
 (P/'model_results.json').write_text(json.dumps(r,indent=2))
 for k in S:
  with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=r[k]['rows'][0]);w.writeheader();w.writerows(r[k]['rows'])
 print({k:(r[k]['price'],r[k]['normalized_roe']) for k in S});print(r['inverse'])
if __name__=='__main__':main()
