"""DHI conditional research model. USD millions, shares millions. NOT a certified valuation.
Ex-financial-services operating FCFF, separate financial-services residual income.
Land/development/rental investment is in total reinvestment, not additional capex.
See report.md for unresolved perimeter and minority calibration.
"""
from pathlib import Path
import json,csv
P=Path(__file__).parent
PRICE=152.28
SHARES=271.435610+0.9 # outstanding at Sep30 plus Q4 incremental diluted shares; no free buybacks
RF=.0486; BETA=1.37; ERP=.0441; KE=RF+BETA*ERP
KD=RF+.01 # assumed current credit spread, NOT an observed bond yield
TAX=.255; WACC=.9*KE+.1*KD*(1-TAX)
R0=33043.4-817.3
# Conservatively book-valued NCI; market proxy shown separately, not exact consolidated NCI.
DEBT=6053.9-1372-600
CASH=2060.4-248-600-500 # excludes financial subsidiary, October maturity, operating reserve
NCI=604.7
FIN_EQUITY=3251.4-1913.8
SCENARIOS={
 'adverso':dict(revenue1=28500,growth=[-.03,.01,.02,.025],margins=[.085,.08,.09,.095,.10],terminal_margin=.095,g=.02,roic=.10,sc=1.25,wacc=WACC+.01,fin_roe=.10),
 'central':dict(revenue1=30200,growth=[.02,.04,.04,.04],margins=[.095,.10,.11,.12,.125],terminal_margin=.115,g=.025,roic=.12,sc=1.5,wacc=WACC,fin_roe=.12),
 'favorable':dict(revenue1=31200,growth=[.05,.06,.06,.05],margins=[.105,.115,.13,.14,.145],terminal_margin=.135,g=.03,roic=.15,sc=1.75,wacc=WACC-.005,fin_roe=.15)}
def fin_value(roe_end=.12,ke=KE,g=.025):
 b=FIN_EQUITY; value=b; rows=[]
 roe0=258.1*(1-TAX)/b
 for year in range(1,11):
  roe=roe0+(roe_end-roe0)*year/10
  ni=b*roe; residual=ni-ke*b; retention=b*g; dividend=ni-retention
  rows.append(dict(year=year,beginning_equity=b,roe=roe,net_income=ni,residual_income=residual,retention=retention,dividend=dividend))
  value+=residual/(1+ke)**year;b+=retention
 terminal_residual=b*(roe_end-ke)
 value+=terminal_residual/(ke-g)/(1+ke)**10
 return value,rows

def model(s,margin_shift=0,wacc=None,g=None):
 s=dict(s); wacc=s['wacc'] if wacc is None else wacc;g=s['g'] if g is None else g
 terminal_margin=s['terminal_margin']+margin_shift
 terminal_sc=s['roic']/(terminal_margin*(1-TAX))
 rows=[]; previous=R0;ev=0
 for y in range(1,11):
  if y==1:r=s['revenue1'];gr=r/previous-1
  elif y<=5:gr=s['growth'][y-2];r=previous*(1+gr)
  else:gr=s['growth'][-1]+(g-s['growth'][-1])*(y-5)/5;r=previous*(1+gr)
  margin=s['margins'][y-1]+margin_shift if y<=5 else s['margins'][-1]+margin_shift+(terminal_margin-s['margins'][-1]-margin_shift)*(y-5)/5
  sc=s['sc'] if y<=5 else s['sc']+(terminal_sc-s['sc'])*(y-5)/5
  ebit=r*margin;nopat=ebit*(1-TAX)
  total_reinvestment=(r-previous)/sc
  if total_reinvestment<0:total_reinvestment*=.25 # avoid full inventory release during slowdown
  da=r*.0035;capex=r*.0055
  delta_operating_working_capital=total_reinvestment-(capex-da)
  fcff=nopat+da-capex-delta_operating_working_capital
  pv=fcff/(1+wacc)**y;ev+=pv
  rows.append(dict(year=2026+y,revenue=r,growth=gr,ebit_margin=margin,ebit=ebit,tax=ebit*TAX,nopat=nopat,da=da,capex_including_software=capex,delta_operating_wc_including_land=delta_operating_working_capital,total_reinvestment=total_reinvestment,incremental_sales_capital=sc,fcff=fcff,pv=pv))
  previous=r
 terminal_nopat=r*(1+g)*terminal_margin*(1-TAX)
 terminal_reinvestment=terminal_nopat*g/s['roic'];terminal_fcff=terminal_nopat-terminal_reinvestment
 terminal_value=terminal_fcff/(wacc-g);pvterminal=terminal_value/(1+wacc)**10;ev+=pvterminal
 fin,finrows=fin_value(s['fin_roe'])
 eq=ev-DEBT+CASH-NCI+fin;per=eq/SHARES
 return dict(wacc=wacc,terminal_growth=g,terminal_roic=s['roic'],terminal_margin=terminal_margin,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,pv_terminal=pvterminal,terminal_weight=pvterminal/ev,operating_ev=ev,financial_services_equity=fin,operating_debt=DEBT,excess_cash=CASH,nci=NCI,equity_value=eq,diluted_shares=SHARES,value_per_share=per,upside=per/PRICE-1,forecast=rows,financial_forecast=finrows)
def solve_shift(s):
 lo,hi=-.05,.3
 for _ in range(100):
  mid=(lo+hi)/2
  if model(s,margin_shift=mid)['value_per_share']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
results={'status':'partial_conditional_not_approved','as_of':'2026-11-07','price':PRICE,'price_timestamp':'2026-11-06T16:00:00-05:00','scanner_last':152.28,'rf':RF,'beta':BETA,'erp':ERP,'ke':KE,'assumed_credit_spread':.01,'kd':KD,'wacc':WACC,'scenarios':{k:model(s) for k,s in SCENARIOS.items()}}
results['audit_controls']={'canonical_approved_value':None,'stage3_complete':False,'entry_approved':False,'publication_allowed':False,'valuation_ready':False,'bridge_complete':False,'unsettled_repurchase_obligation_millions':34.6,'unsettled_repurchase_treatment':'Unresolved; not separately deducted in provisional bridge. Confirm liability classification and settlement to avoid omission or double count.','capex_wc_identity':'Capex and D&A allocation does not independently affect FCFF when total reinvestment is fixed.','financial_profit_standalone_certified':False}
results['inverse']={k:{'parallel_margin_shift':solve_shift(s),'terminal_margin_required':s['terminal_margin']+solve_shift(s)} for k,s in SCENARIOS.items()}
results['sensitivity']=[{'wacc':w,'g':g,'price':model(SCENARIOS['central'],wacc=w,g=g)['value_per_share']} for w in [.09,.10,.11,.12] for g in [.015,.025,.035]]
results['crosscheck']={'book_value_per_share':85.14,'price_to_book':PRICE/85.14,'reported_roe':.122,'perpetual_justified_pb':(.122-.025)/(KE-.025),'implied_sustainable_roe':.025+(PRICE/85.14)*(KE-.025),'pe_ttm':PRICE/10.11,'forestar_market_nci_proxy':51.02*23.70*.38,'nci_book_used':NCI}
results['cash_diagnostics']={'cfo':3507.2,'capex':160.4,'cfo_minus_capex':3346.8,'less_sbc':134,'after_sbc':3212.8,'less_acquisitions':124.1,'after_acquisitions':3088.7,'q4_cfo':3507.2-880.8,'q4_share_annual_cfo':(3507.2-880.8)/3507.2,'inventory_operating_cash_movement':146.3+21.2-23.8,'wc_total':146.3+21.2-23.8-421-3.5+256.6,'nonfinancial_ebit_proxy':33043.4-25682.7-3748.6-(817.3-640.3)+182.5,'financial_pretax':258.1}
for k,r in results['scenarios'].items():
 with (P/f'forecast_{k}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['forecast'][0].keys());w.writeheader();w.writerows(r['forecast'])
 assert len(r['forecast'])==10 and r['wacc']>r['terminal_growth']
 for row in r['forecast']:assert abs(row['fcff']-(row['nopat']+row['da']-row['capex_including_software']-row['delta_operating_wc_including_land']))<1e-8
(P/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:{j:r[j] for j in ['value_per_share','upside','terminal_weight']} for k,r in results['scenarios'].items()},indent=2));print('Inverse',results['inverse']);print('Cross',results['crosscheck'])
