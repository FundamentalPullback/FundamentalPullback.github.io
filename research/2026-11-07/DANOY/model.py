"""Danone: EUR millions. Semiannual financial TTM; sales-only quarters. No current approved valuation."""
import pathlib,json,csv
P=pathlib.Path(__file__).parent
A={2023:dict(revenue=27619,ebit=2042,recurring_ebit=3481,ni_group=881,ni_total=953,cfo=3442,capex=847,da_impairment=1611,sbc=61,wc_cash=277),2024:dict(revenue=27376,ebit=3379,recurring_ebit=3558,ni_group=2021,ni_total=2100,cfo=3831,capex=923,da_impairment=1168,sbc=71,wc_cash=534),2025:dict(revenue=27283,ebit=2940,recurring_ebit=3665,ni_group=1825,ni_total=1887,cfo=3779,capex=1055,da_impairment=1355,sbc=109,wc_cash=276)}
H={2024:dict(revenue=13757,ebit=1814,recurring_ebit=1746,ni_group=1219,ni_total=1259,cfo=1504,capex=319,da_impairment=552,sbc=45,wc_cash=-92),2025:dict(revenue=13737,ebit=1573,recurring_ebit=1811,ni_group=1040,ni_total=1074,cfo=1519,capex=373,da_impairment=641,sbc=75,wc_cash=-230),2026:dict(revenue=13936,ebit=1693,recurring_ebit=1854,ni_group=1175,ni_total=1235,cfo=1258,capex=414,da_impairment=538,sbc=69,wc_cash=-567)}
T={y:{k:A[y-1][k]+H[y][k]-H[y-1][k] for k in A[y-1]} for y in [2025,2026]}
for d in [*A.values(),*H.values(),*T.values()]:d.update(cfo_less_capex=d['cfo']-d['capex'],reported_margin=d['ebit']/d['revenue'],recurring_margin=d['recurring_ebit']/d['revenue'])
# Company IAS29 restates earlier quarters at each new measurement date. Do not sum vintages silently.
Q={'2025Q4_sales_residual':dict(revenue=27283-20578,basis='FY2025 minus 9M2025 comparison; indicative mixed IAS29 dates'), '2026Q1_as_reexpressed_Sep':dict(revenue=6721), '2026Q2_as_reexpressed_Sep':dict(revenue=7221),'2026Q3':dict(revenue=7233)}
for d in Q.values():d.update(ebit=None,cfo=None,capex=None)
fx=1.1165;price=14.99;ratio=.2;shares=643.109091;ordinary_equivalent=price/(fx*ratio);rev=T[2026]['revenue']
# Hypothesis stress only: no current roll-forward, no Huel price fabricated, no NCI assigned zero fair value.
bridge=dict(net_debt_june=8975,lease_debt_already_in_net_debt=902,minority_puts_already_in_net_debt=418,hybrid_equity_senior_to_common=1000,retirement_other_longterm_benefits_proxy=760,operating_cash_reserve_assumption=.02*rev,huel_purchase_price_primary=None,other_post_june_balance_changes=None,non_put_nci_fair_value=None,equity_accounted_investment_value=None)
netclaims=8975+1000+760+.02*rev;hurdle=ordinary_equivalent*shares+netclaims
pars={'prudente':dict(growth=.02,wacc=.08,gt=.02,roic=.10,capex=.052,nwc_incremental=.08),'intermedio':dict(growth=.04,wacc=.07,gt=.025,roic=.12,capex=.048,nwc_incremental=.05),'expansivo':dict(growth=.05,wacc=.06,gt=.025,roic=.15,capex=.046,nwc_incremental=.04)}
def test(p,m):
 r=rev;pv=0;rows=[];ratio5=None
 for y in range(1,11):
  g=p['growth'] if y<=5 else p['growth']+(p['gt']-p['growth'])*(y-5)/5
  new=r*(1+g);dnwc=(new-r)*p['nwc_incremental'];r=new;ebit=r*m;nopat=ebit*.72;da=r*.038;capex=r*p['capex'];raw_reinvestment=capex-da+dnwc
  if y<=5:reinvest=raw_reinvestment;ratio5=reinvest/nopat
  else:
   f=(y-5)/5;reinvest=max(raw_reinvestment,nopat*(ratio5*(1-f)+(p['gt']/p['roic'])*f))
  supplemental_reinvestment=reinvest-raw_reinvestment
  fcff=nopat-reinvest;disc=(1+p['wacc'])**y;pv+=fcff/disc
  rows.append(dict(year=y,revenue=r,margin=m,ebit=ebit,tax=.28,nopat=nopat,da_assumed=da,capex_including_new_lease_assets=capex,incremental_nwc=dnwc,raw_reinvestment=raw_reinvestment,supplemental_reinvestment=supplemental_reinvestment,reinvestment=reinvest,fcff=fcff,pv=fcff/disc))
 tn=rows[-1]['nopat']*(1+p['gt']);terminal_physical_floor=r*(1+p['gt'])*(p['capex']-.038)+r*p['gt']*p['nwc_incremental'];ri=max(terminal_physical_floor,tn*p['gt']/p['roic']);tfcf=tn-ri;pvt=tfcf/(p['wacc']-p['gt'])/(1+p['wacc'])**10
 return dict(parameters=p,required_constant_margin=m,rows=rows,terminal_nopat=tn,terminal_physical_floor=terminal_physical_floor,terminal_roic_effective=tn*p['gt']/ri,terminal_reinvestment=ri,terminal_fcff=tfcf,enterprise_hurdle=pv+pvt,terminal_weight=pvt/(pv+pvt))
inv={}
for name,p in pars.items():
 lo,hi=.01,.4
 for _ in range(100):
  mid=(lo+hi)/2
  if test(p,mid)['enterprise_hurdle']<hurdle:lo=mid
  else:hi=mid
 inv[name]=test(p,(lo+hi)/2)
O=dict(ticker='DANOY',as_of='2026-11-08',status='partial_perimeter_and_claims_bridge',research_eligible=True,research_threshold=65,opportunity=80,stage3_completed=False,stage35_approved=False,approved_values=None,approved_price=None,valuation_cases=None,price=dict(regular_close=price,date='2026-11-06',market='OTCQX end-of-day; not NYSE closing auction',scanner_last=15.39,scanner_date='2026-11-05'),adr=dict(ordinary_per_adr=ratio,usd_per_eur=fx,fx_date='2026-11-06 ECB reference not synchronous executable close',ordinary_eur_equivalent=ordinary_equivalent,issued_shares_june_m=683.337177,outstanding_ex_treasury_june_m=642.115656,weighted_diluted_h1_m=shares,denominator_status='dated June proxy, not Nov6 certified shares'),annual=A,half_year=H,paired_ttm_june=T,quarters_sales_only=Q,sales_9m_2026=21176,sales_9m_2025=20578,sales_ttm_sep_indicative=27283+21176-20578,sales_ttm_warning='Sales-only arithmetic, mixed IAS29 vintages and perimeter. Do not pair with June EBIT as same-period margin.',bridge=bridge,dated_known_claims_proxy=netclaims,enterprise_hurdle_conditional=hurdle,inverse_tests=inv,capital_cost=dict(currency='EUR',risk_free=.0322,risk_free_status='Nov6 primary Bundesbank current 10-year federal bond CSV:3.22%; stale secondary3.27 rejected',erp=.0441,erp_date='2026-11-01 Damodaran',beta_assumed=.8,global_country_risk_buffer_assumed=.005,ke_assumed=.0322+.8*.0441+.005,debt_cost_proxy=.04418,debt_cost_source='Sep2026 nine-year EUR issue coupon, not current yield',wacc_scenarios=[.08,.07,.06]),claim_sensitivity=dict(eur_1bn_per_adr=1000/shares*.2*fx,interpretation='Each additional EUR1bn net claim reduces conditional ADR equity by this amount, all else equal'),unresolved=['Current bridge after Huel closing and Argentina deconsolidation; purchase price primary not disclosed in retrieved sources','Fair value of non-put NCI versus puts already in debt; equity-accounted investments excluded from consolidated FCFF must be valued separately','Current lease asset reinvestment and normalized impairment-free D&A not fully reconciled','Latest shares and contingent claims roll-forward; June proxy only','Full current-perimeter DCF and valuation cases withheld; inverse tests not fair-value approval'])
(P/'results.json').write_text(json.dumps(O,indent=2,ensure_ascii=False))
fields=['revenue','ebit','recurring_ebit','ni_group','cfo','capex','cfo_less_capex','da_impairment','sbc','wc_cash']
with (P/'financial_history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period']+fields)
 for n,d in [(f'FY{k}',v) for k,v in A.items()]+[(f'H1_{k}',v) for k,v in H.items()]+[(f'TTM_Jun{k}',v) for k,v in T.items()]+list(Q.items()):w.writerow([n]+[d.get(k) for k in fields])
assert all(abs(v['enterprise_hurdle']-hurdle)<1e-6 for v in inv.values())
assert all(r['reinvestment']>0 for v in inv.values() for r in v['rows'])
assert all(d['ebit'] is None and d['cfo'] is None for d in Q.values())
print(json.dumps({'ttm':T,'ordinary_equivalent':ordinary_equivalent,'hurdle':hurdle,'inverses':{k:(v['required_constant_margin'],v['terminal_weight']) for k,v in inv.items()}},indent=2))

assert all(a['reinvestment']+1e-9>=a['raw_reinvestment'] for z in inv.values() for a in z['rows'])
assert all(abs(z['terminal_fcff']-z['rows'][-1]['fcff']*(1+z['parameters']['gt']))<1e-7 for z in inv.values())
