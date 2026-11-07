"""BCO standalone diagnostic, NOT valuation of announced combined company.
USD millions except per-share values. Analyst estimates explicitly separated.
Run: python model.py. No third-party dependencies. Five explicit + five transition.
"""
import json
from pathlib import Path
PRICE=110.25
SHARES=41.5 # Q3 diluted average, proxy not exact fully diluted future count
# Nominal debt adds unamortized costs to reported carrying value; finance leases included.
BRIDGE={'nominal_debt':4155.1+6.1+7.6,'corporate_cash':1423.4,'operating_cash_reserve_estimate':150,'nci_book_proxy':84.7,'pension_and_other_retirement_book_proxy':147.2+117.7}
DEDUCTION=BRIDGE['nominal_debt']-BRIDGE['corporate_cash']+BRIDGE['operating_cash_reserve_estimate']+BRIDGE['nci_book_proxy']+BRIDGE['pension_and_other_retirement_book_proxy']
BASE={'revenue':5532.0,'growth':.04,'margin_start':.115,'margin_end':.125,'tax':.30,'roic_initial':.12,'roic_terminal':.10,'g_terminal':.02,'wacc':.093}
def value(**overrides):
 p=BASE|overrides;rev=p['revenue'];rows=[]
 for y in range(1,11):
  t=max(0,(y-5)/5);g=p['growth']*(1-t)+p['g_terminal']*t
  roic=p['roic_initial']*(1-t)+p['roic_terminal']*t
  margin=p['margin_start']+(p['margin_end']-p['margin_start'])*min(1,(y-1)/4)
  rev*=1+g;nopat=rev*margin*(1-p['tax']);reinvest=nopat*g/roic
  fcff=nopat-reinvest;pv=fcff/(1+p['wacc'])**y
  rows.append(dict(year=y,revenue=rev,growth=g,margin=margin,nopat=nopat,roic=roic,reinvestment=reinvest,fcff=fcff,pv=pv))
 terminal_nopat=rows[-1]['nopat']*(1+p['g_terminal'])
 terminal_fcff=terminal_nopat*(1-p['g_terminal']/p['roic_terminal'])
 terminal_pv=terminal_fcff/(p['wacc']-p['g_terminal'])/(1+p['wacc'])**10
 ev=sum(x['pv'] for x in rows)+terminal_pv
 return dict(assumptions=p,rows=rows,terminal_fcff=terminal_fcff,terminal_pv=terminal_pv,terminal_share=terminal_pv/ev,ev=ev,equity=ev-DEDUCTION,per_share=(ev-DEDUCTION)/SHARES)
def inverse(field,lo,hi):
 if (value(**{field:lo})['per_share']-PRICE)*(value(**{field:hi})['per_share']-PRICE)>0:return None
 for _ in range(120):
  mid=(lo+hi)/2;v=value(**{field:mid})['per_share']
  if (v<PRICE)==(field!='wacc'):lo=mid
  else:hi=mid
 return (lo+hi)/2
cases={'adverso':value(growth=.01,margin_start=.095,margin_end=.10,wacc=.105,roic_initial=.10,roic_terminal=.09,g_terminal=.015),'central':value(),'favorable':value(growth=.06,margin_start=.13,margin_end=.14,wacc=.08,roic_initial=.16,roic_terminal=.12,g_terminal=.025)}
result={'status':'screen-grade','scope':'BCO standalone only; not a target or combined-company fair value','as_of':'2026-11-07','regular_close':PRICE,'scanner_last':109.8,'shares_proxy':SHARES,'bridge':BRIDGE,'net_deduction':DEDUCTION,'cases':cases,'sensitivity':[dict(wacc=w,g_terminal=g,per_share=value(wacc=w,g_terminal=g)['per_share']) for w in [.07,.08,.093,.105] for g in [.015,.02,.025]],'reverse_standalone_only':{'growth_first5_to_match_close':inverse('growth',0,.12),'wacc_to_match_close':inverse('wacc',.04,.16)},'cost_of_capital':{'risk_free_reported':.0486,'published_beta':.93,'analyst_beta':1.3,'erp_estimate':.055,'debt_cost_estimate':.075,'debt_weight_estimate':.4,'tax':.3,'illustrative_capm_wacc':(.0486+1.3*.055)*.6+.075*.7*.4},'checks':{'wacc_above_g':all(c['assumptions']['wacc']>c['assumptions']['g_terminal'] for c in cases.values()),'ten_year_rows':all(len(c['rows'])==10 for c in cases.values()),'no_acquisition_synergies_or_financing':True},'missing':['NCR Atleos latest normalized FCFF and pro forma capital structure','NoteMachine/TestLink UK disposal proceeds and removed FCFF','Current fully diluted combined share count and purchase accounting','Quarterly homogeneous historical bridge and pension economic net obligation']}
if __name__=='__main__':
 Path(__file__).with_name('model_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:round(v['per_share'],2) for k,v in cases.items()}));print(result['reverse_standalone_only']);print('bridge',DEDUCTION,'TV',cases['central']['terminal_share'])
