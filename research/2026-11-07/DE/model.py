"""Screen-grade SOTP. USD millions; fully funded 10-year equipment FCFF + finance FCFE/RI.
Sources and analyst assumptions: model_citations.md. Never approved fair values.
"""
import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent
PRICE=671.65
SHARES=269.625412+0.9+0.000092 # actual Aug 2 + Q3 dilution, not weighted-average basic
BASE_SALES=41358
FIN_BOOK=6953
BRIDGE_ITEMS={'equipment_cash':6607,'equipment_marketable_securities':155,'receivable_from_finance':5364,'operating_cash_reserve':-3000,'equipment_debt_including_finance_leases':-9325,'unallocated_debt_principal_adjustment_proxy':-100,'equipment_pension_opeb_deficit_proxy':-1385,'tax_uncertain_incremental_proxy':-322,'redeemable_nci':-44,'nci_book_proxy':-7,'guarantees_accrued_proxy':-25,'august_dividend_payable_at_balance':-443,'november_ex_right_dividend':-269.625412*1.62,'uncollected_tariff_refund_after_tax':382*.2*.75}
BRIDGE=sum(BRIDGE_ITEMS.values())
SCENARIOS={
'adverso':dict(growth=[-.05,0,.03,.03,.03],margin1=.09,margin5=.115,marginT=.115,wacc=.10,g=.02,roic=.15,roicT=.15,maintenance=.033,growthcap=.22,nwc=.22,acq=.004,finance_roe=.09,finance_roeT=.09,finance_ke=.11,finance_growth=.02,finance_g=.02,finance_haircut=.10,loan_haircut=.10),
'central':dict(growth=[.06,.08,.07,.05,.04],margin1=.115,margin5=.16,marginT=.17,wacc=.09,g=.03,roic=.22,roicT=.20,maintenance=.03,growthcap=.18,nwc=.18,acq=.003,finance_roe=.125,finance_roeT=.125,finance_ke=.10,finance_growth=.04,finance_g=.03,finance_haircut=0,loan_haircut=0),
'favorable':dict(growth=[.10,.12,.10,.08,.06],margin1=.13,margin5=.19,marginT=.20,wacc=.08,g=.035,roic=.27,roicT=.24,maintenance=.029,growthcap=.17,nwc=.16,acq=.003,finance_roe=.15,finance_roeT=.14,finance_ke=.095,finance_growth=.05,finance_g=.035,finance_haircut=0,loan_haircut=0)}
def calc(s,override_growth=None,physical_only=False):
 sales=BASE_SALES;rows=[];pv=0
 for y in range(1,12):
  gr=(s['growth'][y-1] if override_growth is None else override_growth) if y<=5 else (s['growth'][-1] if override_growth is None else override_growth)+(s['g']-(s['growth'][-1] if override_growth is None else override_growth))*min(y-5,5)/5
  if y==11:gr=s['g']
  prev=sales;sales*=1+gr
  mar=s['margin1']+(s['margin5']-s['margin1'])*min(y-1,4)/4 if y<=5 else s['margin5']+(s['marginT']-s['margin5'])*min(y-5,5)/5
  nopat=sales*mar*.75;da=sales*.033
  maintenance=max(sales*s['maintenance'],1300*1.02**y)
  growth_capex=max(sales-prev,0)*s['growthcap'];acq=sales*s['acq'];capex=maintenance+growth_capex
  nwc=(sales-prev)*s['nwc']
  physical=capex+acq-da+nwc
  roic=s['roic']+(s['roicT']-s['roic'])*min(max(y-5,0),5)/5
  reinvest=max(physical,0) if physical_only else max(physical,nopat*max(gr,0)/roic)
  # Extra capital only if sales-growth/ROIC funding exceeds explicit physical/working-capital path.
  # No automatic capital charge on margin productivity already expensed in EBIT.
  fcff=nopat-reinvest
  row=dict(year=y,sales=sales,growth=gr,ebit_margin=mar,ebit=sales*mar,nopat=nopat,da=da,maintenance_capex=maintenance,growth_capex=growth_capex,acquisition_budget=acq,cash_capex=capex,delta_nwc=nwc,explicit_net_investment=physical,incremental_roic=roic,net_reinvestment=reinvest,other_capital=max(0,reinvest-physical),fcff=fcff)
  rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
 terminal=rows[-1]['fcff']/(s['wacc']-s['g']);pvt=terminal/(1+s['wacc'])**10;ev=pv+pvt
 # Financial equity: loan and lease assets, external and intercompany debt all remain within equity.
 book=FIN_BOOK*(1-s['finance_haircut']);opening=book;fr=[];pvf=0;pvr=0
 for y in range(1,12):
  growth=s['finance_growth']+(s['finance_g']-s['finance_growth'])*min(max(y-5,0),5)/5
  roe=s['finance_roe']+(s['finance_roeT']-s['finance_roe'])*min(max(y-5,0),5)/5
  ni=book*roe;retained=book*growth;div=ni-retained;ri=ni-book*s['finance_ke']
  fr.append(dict(year=y,opening_book=book,roe=roe,ni=ni,growth=growth,retained_capital=retained,distributable_fcfe=div,approved_distribution=None,remittance_capacity_validated=False,residual_income=ri,closing_book=book+retained))
  if y<=10:pvf+=div/(1+s['finance_ke'])**y;pvr+=ri/(1+s['finance_ke'])**y
  book+=retained
 fterm=fr[-1]['distributable_fcfe']/(s['finance_ke']-s['finance_g']);fpvt=fterm/(1+s['finance_ke'])**10;fvalue=pvf+fpvt
 rivalue=opening+pvr+fr[-1]['residual_income']/(s['finance_ke']-s['finance_g'])/(1+s['finance_ke'])**10
 assert abs(fvalue-rivalue)<1e-7
 bridge=BRIDGE-5364*s['loan_haircut'];equity=ev+fvalue+bridge
 return dict(value_per_share=equity/SHARES,equipment_ev=ev,equipment_explicit_pv=pv,equipment_terminal_pv=pvt,equipment_terminal_weight=pvt/ev,finance_equity_value=fvalue,finance_ri_check=rivalue,finance_terminal_weight=fpvt/fvalue,bridge=bridge,equity_value=equity,rows=rows,finance_rows=fr)
def main():
 out={k:calc(s) for k,s in SCENARIOS.items()}
 for k,v in out.items():
  for suffix,rows in [('equipment',v['rows']),('finance',v['finance_rows'])]:
   with open(P/f'forecast_{k}_{suffix}.csv','w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 sens=[]
 for w in [.08,.09,.10]:
  for g in [.02,.03,.035]:
   s=copy.deepcopy(SCENARIOS['central']);s.update(wacc=w,g=g);v=calc(s);sens.append(dict(wacc=w,g=g,value=v['value_per_share']))
 lo,hi=-.1,.8
 for _ in range(100):
  mid=(lo+hi)/2
  if calc(SCENARIOS['central'],mid)['value_per_share']<PRICE:lo=mid
  else:hi=mid
 capital_sensitivity=[]
 for reserve in [2000,3000,4000]:capital_sensitivity.append({'reserve':reserve,'base_value':out['central']['value_per_share']+(3000-reserve)/SHARES})
 ke=.0486+.9*.0441;dw=9425/(PRICE*SHARES+9425);kd=.0486+.0075
 result=dict(ticker='DE',as_of='2026-11-08',status='material_partial',quality='screen-grade',stage3_approved=False,stage3_5_approved=False,entry_approved=False,approved_fair_value=None,approved_buy_max=None,price=PRICE,price_date='2026-11-06',price_session='regular_close_16_EST',shares=SHARES,base_equipment_sales=BASE_SALES,finance_book=FIN_BOOK,bridge_items=BRIDGE_ITEMS,scenarios=out,physical_only_sensitivity={k:calc(v,physical_only=True)['value_per_share'] for k,v in SCENARIOS.items()},sensitivity=sens,reserve_sensitivity=capital_sensitivity,inverse_constant_first_five_growth=(lo+hi)/2,cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',erp_source_riskfree=.0529,parameter_dates_not_matched=True,observed_beta=.9,observed_ke=ke,analyst_kd=kd,industrial_debt_weight=dw,mechanical_wacc=ke*(1-dw)+kd*.75*dw,chosen_base_wacc=.09,finance_ke=.10),checks=dict(finance_ri_fcfe_equal=True,terminal_physical_floor=True,captive_debt_not_deducted=True,finance_dividends_not_in_equipment_fcff=True,expensed_rd_and_sbc_retained=True,negative_finance_fcfe_allowed=True,no_free_buybacks=True),gaps=['Post-August cash/share bridge and exact pension/tax allocation remain estimates.','Through-cycle equipment demand, margin and replacement capex not certified.','Finance capital target, remittance capacity and correlated dealer-credit stress not certified.','Current used-inventory and dealer-order metrics not established by the available primary financial evidence.'])
 result['approved_values']={'fair_value':None,'buy_max':None,'adverse':None,'central':None,'favorable':None}; (P/'model_results.json').write_text(json.dumps(result,indent=2)); (P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:{z:v[z] for z in ['value_per_share','equipment_ev','finance_equity_value','bridge','equipment_terminal_weight']} for k,v in out.items()},indent=2));print('inverse',result['inverse_constant_first_five_growth'],'wacc',result['cost_of_capital'])
if __name__=='__main__':main()
