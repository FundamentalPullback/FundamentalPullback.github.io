"""OLLI FCFF, USD millions; Python standard library. Research only, 2026-11-07.
Run: python model.py. No network dependencies.
Historical sources and assumption provenance: sources.json and report.md.
"""
import json,csv,copy
from pathlib import Path
D=Path(__file__).resolve().parent
PRICE=90.40
# Issuer fiscal labels, not data-provider calendar-end labels.
fields=['sales','gross_profit','ebit','net_income','eps','cfo','capex','da','sbc','interest_net']
def row(v):return dict(zip(fields,v))
h={
'FY2023':row([2102.662,832.365,227.799,181.439,2.92,254.497,124.404,34.936,12.237,14.686]),
'FY2024':row([2271.705,914.452,249.503,199.762,3.23,227.454,120.554,43.958,19.445,16.311]),
'FY2025':row([2649.198,1072.944,297.665,240.596,3.89,296.539,101.879,55.236,13.060,18.719]),
'H12024':row([1087.193,428.389,117.256,95.324,1.54,84.059,65.154,19.733,6.801,8.229]),
'H12025':row([1256.323,508.369,133.160,108.870,1.76,109.414,53.156,26.261,6.524,9.322]),
'H12026':row([1400.233,598.129,178.032,141.854,2.34,153.625,68.783,29.826,7.129,11.108]),
'Q32025':row([613.619,253.654,55.414,46.172,.75,4.758,83.888-53.156,40.449-26.261,9.806-6.524,4.524]),
'Q42025':row([779.256,310.921,109.091,85.554,1.39,296.539-114.172,101.879-83.888,55.236-40.449,13.060-9.806,4.873]),
'Q12026':row([658.928,275.964,69.557,56.400,.92,45.501,25.474,14.934,3.401,4.966]),
'Q22026':row([741.305,322.165,108.475,85.454,1.42,108.124,68.783-25.474,29.826-14.934,3.728,6.142])}
for name,a,b,c in [('TTM2026','FY2025','H12026','H12025'),('TTM2025','FY2024','H12025','H12024')]:
 h[name]={k:h[a][k]+h[b][k]-h[c][k] for k in fields}
 h[name]['eps_method']='FY EPS plus current H1 EPS minus prior H1 EPS; quarterly-sum cross-check for current TTM; rounding differences possible'
for name,v in h.items():
 v.update(fcf=v['cfo']-v['capex'],op_margin=v['ebit']/v['sales'],gross_margin=v['gross_profit']/v['sales'],cash_conversion=(v['cfo']-v['capex'])/v['net_income'])
# 28.3 operating refund; 1.1 interest refund already inside net interest. SBC economic cost retained.
ttm=h['TTM2026'];ttm['normalized_ebit']=ttm['ebit']-28.3
ttm['normalized_fcff_cash_proxy']=ttm['fcf']-ttm['sbc']-ttm['interest_net']*.75-28.3*.75
BASE=2934.5 # FY26 published sales guidance midpoint used as rolling run-rate anchor, not actual NTM
BRIDGE={'cash':120.765,'short_investments':66.737,'long_investments':319.592,'operating_cash':BASE*.03,'finance_leases':2.229,'operating_leases_memo':723.417,'pension':0,'minority':0,'preferred':0,'shares_basic_aug1':59.549,'incremental_in_money':.139,'shares':59.688}
NET=BRIDGE['cash']+BRIDGE['short_investments']+BRIDGE['long_investments']-BRIDGE['operating_cash']-BRIDGE['finance_leases']
CASES={
'adverso':dict(growth=[.03,.05,.05,.04,.04],margin=[.099,.096,.095,.095,.095],terminal_margin=.095,wacc=.113,g=.02,roic=.14,growth_capex=.28,maint=.022),
'central':dict(growth=[.0564,.09,.08,.07,.06],margin=[.109,.111,.112,.112,.112],terminal_margin=.11,wacc=.102,g=.025,roic=.18,growth_capex=.22,maint=.02),
'favorable':dict(growth=[.10,.12,.11,.10,.09],margin=[.115,.12,.123,.125,.125],terminal_margin=.12,wacc=.095,g=.03,roic=.22,growth_capex=.20,maint=.02)}
def value(case,shares=BRIDGE['shares'],net=NET,operating_cash_rate=.03):
 c=copy.deepcopy(case); rev=BASE; rows=[]; c['operating_cash_rate']=operating_cash_rate
 for year in range(1,11):
  if year<=5:grow=c['growth'][year-1];margin=c['margin'][year-1]
  else:
   f=(year-5)/5;grow=c['growth'][-1]+(c['g']-c['growth'][-1])*f;margin=c['margin'][-1]+(c['terminal_margin']-c['margin'][-1])*f
  old=rev;rev*=1+grow;ebit=rev*margin;nopat=ebit*.75;da=rev*.021;dnwc=.15*(rev-old);dcash=operating_cash_rate*(rev-old)
  if year<=5:
   maint=rev*c['maint'];growth_capex=c['growth_capex']*(rev-old);capex=maint+growth_capex;reinv=capex-da+dnwc+dcash
   implied_roic=nopat*grow/reinv
   if year==5:roic5=implied_roic
  else:
   f=(year-5)/5;implied_roic=roic5+(c['roic']-roic5)*f;reinv=nopat*grow/implied_roic;capex=da+reinv-dnwc-dcash;maint=da;growth_capex=capex-maint
  fcff=nopat+da-capex-dnwc-dcash
  assert abs(fcff-(nopat-reinv))<1e-8
  assert growth_capex>=0 and capex>0 and reinv>0
  rows.append(dict(year=year,revenue=rev,growth=grow,margin=margin,ebit=ebit,nopat=nopat,da=da,maintenance_capex=maint,growth_capex=growth_capex,capex=capex,dNWC=dnwc,dOperatingCash=dcash,reinvestment=reinv,implied_incremental_roic=implied_roic,fcff=fcff,pv_fcff=fcff/(1+c['wacc'])**year))
 terminal_nopat=rev*(1+c['g'])*c['terminal_margin']*.75;terminal_reinv=terminal_nopat*c['g']/c['roic'];terminal_fcff=terminal_nopat-terminal_reinv;tv=terminal_fcff/(c['wacc']-c['g']);pv_tv=tv/(1+c['wacc'])**10;ev=sum(x['pv_fcff'] for x in rows)+pv_tv;equity=ev+net
 terminal_rev=rev*(1+c['g']);terminal_da=terminal_rev*.021;terminal_dnwc=(terminal_rev-rev)*.15;terminal_dcash=(terminal_rev-rev)*operating_cash_rate;terminal_capex=terminal_da+terminal_reinv-terminal_dnwc-terminal_dcash
 assert abs(terminal_fcff-(terminal_nopat+terminal_da-terminal_capex-terminal_dnwc-terminal_dcash))<1e-8
 return dict(terminal_physical={'revenue':terminal_rev,'da':terminal_da,'capex':terminal_capex,'dNWC':terminal_dnwc,'dOperatingCash':terminal_dcash},assumptions=c,rows=rows,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,terminal_fcff=terminal_fcff,terminal_value=tv,pv_terminal=pv_tv,ev=ev,equity=equity,net_bridge=net,shares=shares,value_per_share=equity/shares,upside=equity/shares/PRICE-1,terminal_weight=pv_tv/ev)
def solve(fn,target,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
def growth_value(g):
 c=copy.deepcopy(CASES['central']);c['growth']=[g]*5;return value(c)['value_per_share']
def margin_value(m):
 c=copy.deepcopy(CASES['central']);c['margin']=[m]*5;c['terminal_margin']=m;return value(c)['value_per_share']
r={'model_version':'OLLI-FCFF-20261107-v2','valuation_status':'exploratory_only_calibration_pending','canonical_valuation_approved':False,'asof':'2026-11-07','currency':'USD','units':'millions except share price and ratios','price':PRICE,'historical':h,'bridge':BRIDGE,'scenarios':{k:value(v) for k,v in CASES.items()}}
r['capital_cost']={'risk_free':.0486,'risk_free_source':'S13, 2026-11-06 10-year Treasury','erp':.0441,'erp_source':'S14, explicitly dated 2026-11-01','beta':1.10,'beta_type':'analyst assumption, not measured beta','capm':.0486+1.10*.0441,'execution_premium':.00489,'central_wacc':.102,'note':'ERP monthly observation is not synchronous with daily Treasury; paired source Treasury 5.29% sensitivity disclosed in audit.'}
r['inverse']={'constant_growth_first5':solve(growth_value,PRICE,.001,.4),'constant_margin_all10_and_terminal':solve(margin_value,PRICE,.05,.3),'note':'One-variable inverse holding other central assumptions fixed; growth includes capital needed.'}
r['sensitivity']=[{'wacc':w,'g':g,'value':value(dict(CASES['central'],wacc=w,g=g))['value_per_share']} for w in [.09,.10,.102,.11,.12] for g in [.02,.025,.03]]
r['bounded_proxies']={'all_antidilutive_shares_60_262':value(CASES['central'],shares=60.262)['value_per_share'],'cash_buffer_5pct':value(CASES['central'],net=NET-BASE*.02,operating_cash_rate=.05)['value_per_share'],'opening_cash_buffer_5pct_only':value(CASES['central'],net=NET-BASE*.02)['value_per_share'],'long_investments_haircut_2pct':value(CASES['central'],net=NET-319.592*.02)['value_per_share'],'post_august_buyback_60_5m_at_80':value(CASES['central'],net=NET-60.5,shares=BRIDGE['shares']-60.5/80)['value_per_share'],'cashflow_since_balance_plus75m':value(CASES['central'],net=NET+75)['value_per_share'],'maint_capex_plus_50bp':value(dict(CASES['central'],maint=.025))['value_per_share']}
# Historical market tests use only earnings known at respective release-date regular closes.
r['audit_sensitivities']={'label':'Illustrative audit sensitivity, not revised forecasts','beta_tests':[{'beta':b,'wacc':.0486+b*.0441+.00489,'value':value(dict(CASES['central'],wacc=.0486+b*.0441+.00489))['value_per_share']} for b in [.35,.75,1.1]],'erp_source_paired_riskfree_5_29pct':{'wacc':.1063,'value':value(dict(CASES['central'],wacc=.1063))['value_per_share']}}
r['matched_history']=[{'date':'2026-03-12','close':104.87,'eps_ttm':3.89,'pe':104.87/3.89,'period':'FY2025'}, {'date':'2026-06-03','close':79.74,'eps_ttm':3.89+.92-.77,'pe':79.74/(3.89+.92-.77),'period':'TTM Q12026'}, {'date':'2026-09-02','close':73.87,'eps_ttm':4.47,'pe':73.87/4.47,'period':'TTM Q22026'}, {'date':'2026-11-06','close':PRICE,'eps_ttm':4.47,'pe':PRICE/4.47,'period':'same TTM Q22026'}]
r['current_multiples']={'pe_reported':PRICE/4.47,'pe_normalized_tax25':PRICE/((ttm['ebit']-28.3+ttm['interest_net']-1.1)*.75/BRIDGE['shares']),'ev_ebit_normalized':(PRICE*BRIDGE['shares']-(NET+BRIDGE['operating_cash']))/ttm['normalized_ebit'],'fcf_yield':ttm['fcf']/(PRICE*BRIDGE['shares']),'economic_fcff_proxy_yield':ttm['normalized_fcff_cash_proxy']/(PRICE*BRIDGE['shares'])}
(D/'results.json').write_text(json.dumps(r,indent=2)+'\n')
for n,v in r['scenarios'].items():
 with (D/f'forecast_{n}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=v['rows'][0].keys());w.writeheader();w.writerows(v['rows'])
print(json.dumps({k:{x:v[x] for x in ['value_per_share','upside','terminal_weight']} for k,v in r['scenarios'].items()},indent=2));print(r['inverse']);print(r['current_multiples']);print(r['bounded_proxies'])
