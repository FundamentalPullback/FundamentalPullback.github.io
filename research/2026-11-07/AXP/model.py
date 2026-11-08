import json, pathlib, math
P=pathlib.Path(__file__).parent
facts=json.loads((P/'financial_inputs.json').read_text())
def fact(tag,start,end):
 vals=[x for a in facts[tag]['units'].values() for x in a if x.get('start')==start and x['end']==end and x['filed']<='2026-11-08']
 v=sorted(vals,key=lambda x:x['filed'])[-1]
 return v['val']/(1 if 'PerShare' in tag else 1e6)
tags={'revenue':'RevenuesNetOfInterestExpense','net_income':'NetIncomeLoss','eps':'EarningsPerShareDiluted','cfo':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation'}
history={}
for k,t in tags.items():
 a24=fact(t,'2024-01-01','2024-12-31');a25=fact(t,'2025-01-01','2025-12-31')
 y24=fact(t,'2024-01-01','2024-09-30');y25=fact(t,'2025-01-01','2025-09-30');y26=fact(t,'2026-01-01','2026-09-30')
 q1=fact(t,'2026-01-01','2026-03-31');h1=fact(t,'2026-01-01','2026-06-30')
 history[k]={'FY2023':fact(t,'2023-01-01','2023-12-31'),'FY2024':a24,'FY2025':a25,'9M2024':y24,'9M2025':y25,'9M2026':y26,'Q42025_derived':a25-y25,'Q12026':q1,'Q22026_derived':h1-q1,'Q32026_derived':y26-h1,'TTM2025':a24-y24+y25,'TTM2026':a25-y25+y26}
# Banking exception documented in report: FCFE = common earnings - increase in required common book.
# All amounts USD millions, shares millions. No cash add-on, deposit or debt deduction.
accounting_common_book=35797-1584
book=35797-1600; shares=674; price=320.99
pretax=13795-10705+12380
normalized=(pretax-(982-336)-426)*.77-(1600*.06450+62*4/3)
# Current Series E coupon: 6.450% on liquidation preference 1600, issued Aug12 2026.
# Participating awards annualized from 9M 62; exclude 16 redemption.
# Accounting common book is34213; conservative liquidation-adjusted book34197 is model basis.
# Additional credit normalization 30bp on latest 9M average balances; no reserve releases projected.
credit_extra=.003*227121
seed=normalized
ke=.0529+1.08*.0441

def value(growth=.08,roe_terminal=.25,ke=ke,shock=0,terminal_g=.035):
 b=book; income=seed*(1+shock); pv=0; ri_pv=0; rows=[]
 for y in range(1,11):
  gb=growth if y<=5 else growth+(terminal_g-growth)*(y-5)/5
  if y<=5: income*=1+growth
  else:
   roe0=seed*(1+shock)/book*(1+growth)
   income=b*(roe0+(roe_terminal-roe0)*(y-5)/5)
  reinvest=b*gb; fcfe=income-reinvest; ri=income-ke*b
  rows.append(dict(year=y,book_open=b,common_earnings=income,roe=income/b,book_growth=gb,reinvestment=reinvest,fcfe=fcfe,residual_income=ri))
  pv+=fcfe/(1+ke)**y; ri_pv+=ri/(1+ke)**y;b+=reinvest
 terminal_income=b*roe_terminal; terminal_fcfe=terminal_income-b*terminal_g
 tv=terminal_fcfe/(ke-terminal_g); tvri=(terminal_income-ke*b)/(ke-terminal_g)
 v=(pv+tv/(1+ke)**10)/shares
 rival=(book+ri_pv+tvri/(1+ke)**10)/shares
 assert abs(v-rival)<1e-8
 return {'value':v,'return_to_value':v/price-1,'ke':ke,'growth_first5':growth,'roe_terminal':roe_terminal,'terminal_g':terminal_g,'shock':shock,'terminal_share':tv/(1+ke)**10/(v*shares),'ri_crosscheck':rival,'rows':rows}
cases={'bajista':value(.04,.20,ke+.01,-.18,.025),'central':value(),'favorable':value(.11,.30,ke-.005,0,.04)}
lo,hi=-.05,.30
for _ in range(100):
 mid=(lo+hi)/2
 if value(mid)['value']<price:lo=mid
 else:hi=mid
out={'asof':'2026-11-08','price':price,'price_session':'2026-11-06 regular close 16:00 America/New_York','history':history,'common_book':book,'common_book_basis':'liquidation_adjusted','accounting_common_book':accounting_common_book,'claims_annual':{'preferred':1600*.0645,'participating_awards':62*4/3,'total':1600*.0645+62*4/3},'capital_returns_9m':{'common_dividends_declared':1938,'common_repurchases_equity':5505,'total_declared_common_returns':7443,'common_dividends_prior':1719,'total_dividends_paid_cash_including_preferred':1916,'repurchases_other_cash':5805},'diluted_shares':shares,'pretax_ttm':pretax,'normalized_common_earnings_before_credit':normalized,'credit_extra_pretax_sensitivity_only':credit_extra,'seed_common_earnings':seed,'ke_basis':{'riskfree_paired':.0529,'erp':.0441,'beta':1.08,'current_treasury':.0486,'paired_ke':ke,'current_rf_ke_sensitivity':.0486+1.08*.0441},'credit_30bp_sensitivity_value':value(shock=-credit_extra*.77/seed)['value'],'cases':cases,'inverse_growth_first5':(lo+hi)/2,'sensitivity':[{'ke':k,'roe_terminal':r,'value':value(roe_terminal=r,ke=k)['value']} for k in [.096228,.100528,.11,.12] for r in [.20,.25,.30]],'status':'partial_conditional_research_not_entry','researchCompleted':False,'valuationApproved':False}
(P/'results.json').write_text(json.dumps(out,indent=2)); print(json.dumps({k:v for k,v in out.items() if k not in ['cases','history','sensitivity']},indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(history)
