"""Pre-event 8 Nov2026. USD millones. Consolidated FCFF after cash content funding."""
import json,csv
from pathlib import Path
P=Path(__file__).parent;SALES=98861;SHARES=1743;PRICE=116.75
S={'prudente':dict(sales1=101000,growth=.025,margin1=.145,margin10=.16,wacc=.105,g=.02,maintenance=.055,capital_per_growth=1.1,content_growth=.30,other_wc=.12,nci_multiple=20,claim_reserve=1200,tariff_reserve=150,investment_haircut=.40),'central':dict(sales1=104000,growth=.045,margin1=.16,margin10=.19,wacc=.095,g=.025,maintenance=.05,capital_per_growth=.90,content_growth=.25,other_wc=.10,nci_multiple=17,claim_reserve=600,tariff_reserve=100,investment_haircut=.20),'favorable':dict(sales1=107000,growth=.065,margin1=.175,margin10=.225,wacc=.085,g=.03,maintenance=.045,capital_per_growth=.75,content_growth=.20,other_wc=.08,nci_multiple=14,claim_reserve=300,tariff_reserve=50,investment_haircut=0)}
def calc(a,growth=None,wacc=None):
 a=a.copy();a['growth']=a['growth'] if growth is None else growth;a['wacc']=a['wacc'] if wacc is None else wacc
 pv=0;prev=SALES;rows=[]
 for y in range(1,11):
  growth_rate=a['growth'] if y<=5 else a['growth']+(a['g']-a['growth'])*(y-5)/5
  sales=a['sales1'] if y==1 else prev*(1+growth_rate);delta=sales-prev;m=a['margin1']+(a['margin10']-a['margin1'])*(y-1)/9
  # Margins retain content amortization/cash maintenance and SBC. No 53rd-week annual recurrence.
  ebit=sales*m-a['tariff_reserve']*(sales/SALES)
  # NFL deferred economics from2033; explicit economic renewal allowance, not asserted contractual cash payment.
  nfl=300*(sales/SALES) if y>=7 else 0
  nopat=ebit*.76;da=sales*.0555;physical=sales*a['maintenance']+delta*a['capital_per_growth'];intangible=sales*.0125;content_extra=delta*a['content_growth'];wc=delta*a['other_wc']
  fcff=nopat+da-physical-intangible-content_extra-wc-nfl;pv+=fcff/(1+a['wacc'])**y
  rows.append(dict(year=y,sales=sales,operating_margin=m,ebit=ebit,nopat=nopat,da=da,physical_capex=physical,intangible_replacement=intangible,extra_cash_content=content_extra,other_wc=wc,nfl_economic_renewal=nfl,net_reinvestment=physical+intangible+content_extra+wc+nfl-da,growth_rate=growth_rate,fcff=fcff));prev=sales
 sales=prev*(1+a['g']);delta=sales-prev;fcff=(sales*a['margin10']-a['tariff_reserve']*sales/SALES)*.76+sales*.0555-sales*(a['maintenance']+.0125)-delta*(a['capital_per_growth']+a['content_growth']+a['other_wc'])-300*sales/SALES
 tv=fcff/(a['wacc']-a['g']);ev=pv+tv/(1+a['wacc'])**10
 # All consolidated NCI cash flows are inside EV, so subtract earnings-capitalized claim, not just book.
 claims=dict(borrowings=46041,finance_leases_last_annual=162,pension_medical_gross_deficits_last_annual=1715,nci_value=max(6810,824*a['nci_multiple']),tax_uncertainty_last_annual=1133,litigation_other_reserve=a['claim_reserve'],operating_cash=SALES*.03,cash=-5185,nonoperating_investments=-7627*(1-a['investment_haircut']))
 net=sum(claims.values());equity=ev-net
 return dict(assumptions=a,rows=rows,terminal_fcff=fcff,enterprise_value=ev,net_claims=net,claims=claims,equity_value=equity,price=equity/SHARES,terminal_pv_weight=tv/(1+a['wacc'])**10/ev)
def main():
 r={k:calc(v) for k,v in S.items()};lo,hi=-.01,1.0
 for _ in range(100):
  m=(lo+hi)/2
  if calc(S['central'],growth=m)['price']<PRICE:lo=m
  else:hi=m
 root=(lo+hi)/2
 grid=[{'growth':i/1000,'price':calc(S['central'],growth=i/1000)['price']} for i in range(-10,1001)]
 r['inverse']={'growth_years2_to5':root if abs(calc(S['central'],growth=root)['price']-PRICE)<1e-6 else None,'price':PRICE,'other_assumptions':'central; growth fades years6-10 to2.5%','tested_range':[-.01,1.0],'grid_best':max(grid,key=lambda x:x['price']),'root_verified':abs(calc(S['central'],growth=root)['price']-PRICE)<1e-6}
 r['approval']={'approved_values':None,'approved_price':None,'entry_approved':False,'stage3_complete':False,'capital_calibration_validated':False}
 r['cost_capital']={'rf':.0486,'rf_date':'2026-11-06','erp':.0441,'erp_date':'2026-11-01','erp_source_rf':.0529,'beta_assumed':1.1,'kd_assumed':.055,'date_basis_mismatch':True}
 r['sensitivity']=[dict(wacc=w,growth=g,price=calc(S['central'],growth=g,wacc=w)['price']) for w in [.085,.095,.105] for g in [.025,.045,.065]]
 (P/'model_results.json').write_text(json.dumps(r,indent=2))
 for k in S:
  with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=r[k]['rows'][0]);w.writeheader();w.writerows(r[k]['rows'])
 print({k:r[k]['price'] for k in S});print(r['inverse'])
if __name__=='__main__':main()
