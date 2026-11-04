#!/usr/bin/env python3
"""CBOE fee-business FCFF; USD millions. Own assumptions, not issuer guidance."""
import json,csv,copy,math
from pathlib import Path
P=Path(__file__).resolve().parent
COMMON=dict(anchor_net_revenue=709.3*4,anchor_margin=.65,shares=104.7,price=344.28,stub_days=57,days_year=365,cash=2663.1,foreign_cash_excluded=429.7,debt=1450,tax_claim=28.3,known_oct_buyback=8.1,domestic_reserve=500,capital_residual=0,canada_proceeds=0,retained_canada=True,capex_ratio=.036,working_capital_ratio=.03,regulatory_retention_ratio=.06,license_tail_years=15)
SCENARIOS={
'bear':dict(growth=[-.05,0,.02,.03,.03,.03,.025,.025,.02,.02],margins=[.60,.59,.59,.60,.60,.60,.60,.60,.59,.59],tax=.29,wacc=.095,g=.02,roic=.20,license_haircut=.40,domestic_reserve=650,capital_residual=-150),
'base':dict(growth=[.08,.07,.06,.05,.05,.045,.04,.035,.03,.03],margins=[.65,.655,.66,.66,.66,.66,.655,.65,.65,.65],tax=.28,wacc=.075,g=.025,roic=.30,license_haircut=.10),
'bull':dict(growth=[.12,.10,.09,.08,.07,.06,.05,.045,.04,.035],margins=[.66,.67,.68,.69,.69,.69,.685,.68,.68,.68],tax=.27,wacc=.0675,g=.03,roic=.40,license_haircut=0,domestic_reserve=400,capital_residual=150)}
def calc(name='base',overrides=None):
 c={**COMMON,**SCENARIOS[name],**(overrides or {})}; assert c['wacc']>c['g'] and c['roic']>c['g']
 rev=c['anchor_net_revenue']; prev_nopat=rev*c['anchor_margin']*(1-c['tax']); stub=c['stub_days']/c['days_year']
 # Stub uses a current run-rate, no invented Q4 guidance. Maintenance/growth reserve 3% of revenue is an assumption.
 stub_fcff=(prev_nopat-rev*.03)*stub; pv_stub=stub_fcff/(1+c['wacc'])**stub
 rows=[]
 for i,(growth,margin) in enumerate(zip(c['growth'],c['margins'])):
  prior_rev=rev; rev*=1+growth; ebit=rev*margin; nopat=ebit*(1-c['tax'])
  da_ratio=.041+(.03-.041)*i/9; da=rev*da_ratio; capex=rev*c['capex_ratio']
  delta_rev=max(0,rev-prior_rev); wc=delta_rev*c['working_capital_ratio']; reg=delta_rev*c['regulatory_retention_ratio']
  physical_net=capex-da+wc+reg; growth_net=max(0,nopat-prev_nopat)/c['roic']; reinvest=max(0,physical_net,growth_net)
  other=max(0,reinvest-physical_net); fcff=nopat-reinvest; t=i+1+stub; pv=fcff/(1+c['wacc'])**t
  rows.append(dict(year=2027+i,growth=growth,net_revenue=rev,margin=margin,ebit=ebit,tax=c['tax'],nopat=nopat,da=da,capex=capex,working_capital_investment=wc,regulatory_retention=reg,physical_net_investment=physical_net,growth_net_investment=growth_net,other_economic_investment=other,total_net_investment=reinvest,fcff=fcff,discount_years=t,pv=pv))
  prev_nopat=nopat
 next_nopat=rows[-1]['nopat']*(1+c['g']); terminal_reinvest=next_nopat*c['g']/c['roic']; terminal_fcff=next_nopat-terminal_reinvest
 tv_unadjusted=terminal_fcff/(c['wacc']-c['g']); tail_factor=1-c['license_haircut']*((1+c['g'])/(1+c['wacc']))**c['license_tail_years']; tv=tv_unadjusted*tail_factor
 pv_tv=tv/(1+c['wacc'])**rows[-1]['discount_years']; ev=pv_stub+sum(r['pv'] for r in rows)+pv_tv
 bridge=c['cash']-c['foreign_cash_excluded']-c['domestic_reserve']-c['debt']-c['tax_claim']-c['known_oct_buyback']+c['capital_residual']+c['canada_proceeds']; equity=ev+bridge
 return dict(scenario=name,assumptions=c,stub_fcff=stub_fcff,pv_stub=pv_stub,rows=rows,next_nopat=next_nopat,terminal_reinvestment=terminal_reinvest,terminal_fcff=terminal_fcff,terminal_value_no_license_adjustment=tv_unadjusted,license_tail_factor=tail_factor,terminal_value=tv,pv_terminal=pv_tv,terminal_ev_share=pv_tv/ev,ev=ev,bridge=bridge,equity=equity,value=equity/c['shares'],upside=equity/c['shares']/c['price']-1)
def solve(kind,target=COMMON['price']):
 lo,hi=(-.10,.30) if kind=='growth' else (-.40,.50)
 def f(x):
  o={'growth':[v+x for v in SCENARIOS['base']['growth']]} if kind=='growth' else {'margins':[v+x for v in SCENARIOS['base']['margins']]}
  return calc(overrides=o)
 if not f(lo)['value']<=target<=f(hi)['value']: return {'kind':kind,'solution':None,'bracket':[f(lo)['value'],f(hi)['value']]}
 for _ in range(100):
  mid=(lo+hi)/2
  if f(mid)['value']<target:lo=mid
  else:hi=mid
 r=f((lo+hi)/2)
 return dict(kind=kind,additive_change=(lo+hi)/2,value=r['value'],year10_revenue=r['rows'][-1]['net_revenue'],year10_margin=r['rows'][-1]['margin'])
def run():
 results={n:calc(n) for n in SCENARIOS}
 cap=COMMON['price']*COMMON['shares']; wd=1450/(cap+1450); ke=.0495+.41*.0441 # beta times ERP
 calc_wacc=(1-wd)*ke+wd*.05*(1-.28)
 sens={}
 for w in [.065,.0675,.07,.075,.08,.085,.095]:
  for g in [.015,.02,.025,.03]:sens[f'wacc_{w:.4f}_g_{g:.4f}']=calc(overrides={'wacc':w,'g':g})['value']
 special={
 'monthly_erp_risk_free_consistent':calc(overrides={'wacc':(1-wd)*(.0529+.41*.0441)+wd*.05*.72})['value'],
 'provider_capm_wacc':calc(overrides={'wacc':calc_wacc})['value'],
 'no_renewal_haircut':calc(overrides={'license_haircut':0})['value'],
 'post2051_cash_loss_40pct':calc(overrides={'license_haircut':.40})['value'],
 'post2051_cash_loss_100pct':calc(overrides={'license_haircut':1})['value'],
 'foreign_cash_available_without_tax':calc(overrides={'foreign_cash_excluded':0})['value'],
 'domestic_reserve_800':calc(overrides={'domestic_reserve':800})['value'],
 'additional_claim_100':calc(overrides={'capital_residual':-100})['value'],
 'fiscal_year_grid_no_stub':calc(overrides={'stub_days':0})['value'],
 'same_calendar_omit_stub':calc()['value']-calc()['pv_stub']/COMMON['shares'],
 'investments_at_book_39_1':calc(overrides={'capital_residual':39.1})['value'],
 'canada_remove_2pct_revenue_add_100_proceeds':calc(overrides={'anchor_net_revenue':COMMON['anchor_net_revenue']*.98,'canada_proceeds':100})['value'],
 'canada_remove_3pct_revenue_add_100_proceeds':calc(overrides={'anchor_net_revenue':COMMON['anchor_net_revenue']*.97,'canada_proceeds':100})['value'],
 'royalty_net_revenue_reduction_2pct':calc(overrides={'anchor_net_revenue':COMMON['anchor_net_revenue']*.98})['value'],
 'recurring_cost_margin_minus_05pp':calc(overrides={'margins':[v-.005 for v in SCENARIOS['base']['margins']]})['value'],
 'shares_plus_04m':calc(overrides={'shares':105.1})['value'],
 'roic_20pct':calc(overrides={'roic':.20})['value'],
 'tax_30pct':calc(overrides={'tax':.30})['value'],
 'beta_036_capm':calc(overrides={'wacc':(1-wd)*(.0495+.36*.0441)+wd*.05*.72})['value']}
 out={'as_of':'2026-11-04','price_date':'2026-11-03','currency':'USD','units':'USD millions except per-share values','results':results,'wacc_audit':{'risk_free':.0495,'erp':.0441,'beta':.41,'cost_equity':ke,'debt_weight':wd,'cost_debt_assumed':.05,'tax':.28,'calculated_wacc':calc_wacc,'selected_wacc':.075,'discretionary_buffer_bps':(.075-calc_wacc)*1e4},'sensitivity_grid':sens,'special_sensitivities':special,'inverse':[solve('growth'),solve('margin')]}
 (P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 with (P/'projection.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['scenario']+list(results['base']['rows'][0]));w.writeheader()
  for name,r in results.items():w.writerows(dict(scenario=name,**x) for x in r['rows'])
 print(json.dumps({'values':{n:r['value'] for n,r in results.items()},'wacc':out['wacc_audit'],'inverse':out['inverse'],'sensitivity':special},indent=2))
if __name__=='__main__':run()
