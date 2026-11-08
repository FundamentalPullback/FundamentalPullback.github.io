"""REYN FCFF, USD millions except per share. Analyst scenarios, not forecasts by issuer.
Run: python scanner_continuation/REYN/model.py. Sources and assumptions in report.md.
End-year discounting; rolling TTM starting 30 September 2026, priced 6 November.
"""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
PRICE=24.11; SHARES=211.8; R0=3799.; TAX=.25
# Principal, not amortized debt. Finance leases upper bound 14+33 (payments ignored).
BRIDGE={'term_principal':1536.,'OHA_revolver':110.,'finance_leases_upper_bound':47.,'postretirement':14.,'environmental_after_tax':25*(1-TAX),'minority':0.,'excess_cash':0.}
# Cash $25m is operating, not excess. OHA separately valued, not in standalone revenue.
CASES={
'adverso':dict(volume=[-.04,-.02,0,0,0],price_mix=[.02,.02,.015,.015,.015],margins=[.125,.12,.12,.122,.125],capex=[.052,.051,.05,.048,.047],wacc=.09,g=.01,roic=.09,terminal_margin=.125,acquisition_value=0.),
'central':dict(volume=[-.01,0,.005,.005,.005],price_mix=[.025,.02,.02,.02,.02],margins=[.14,.142,.145,.147,.15],capex=[.047,.046,.045,.044,.044],wacc=.08,g=.02,roic=.12,terminal_margin=.15,acquisition_value=110.),
'favorable':dict(volume=[0,.01,.015,.015,.015],price_mix=[.03,.025,.025,.025,.025],margins=[.145,.15,.155,.16,.16],capex=[.047,.046,.045,.045,.045],wacc=.075,g=.025,roic=.14,terminal_margin=.16,acquisition_value=165.)}
def dcf(c):
 assert c['wacc']>c['g']>=0 and c['roic']>c['g']
 r=R0;rows=[];prev_nopat=R0*(537/R0)*(1-TAX)
 for t in range(1,11):
  if t<=5:
   growth=(1+c['volume'][t-1])*(1+c['price_mix'][t-1])-1;m=c['margins'][t-1]
  else:
   a=(t-5)/5;growth=(1-a)*rows[4]['growth']+a*c['g'];m=(1-a)*c['margins'][-1]+a*c['terminal_margin']
  old=r;r*=1+growth;ebit=r*m;nopat=ebit*(1-TAX);da=r*.035;dnwc=.15*(r-old)
  if t<=5: capex=r*c['capex'][t-1]
  else:
   a=(t-5)/5;rr=(1-a)*rows[4]['reinvestment_rate']+a*c['g']/c['roic'];capex=da+nopat*rr-dnwc
  reinvest=capex-da+dnwc;fcff=nopat-reinvest;pv=fcff/(1+c['wacc'])**t
  rows.append(dict(year=t,revenue=r,growth=growth,ebit_margin=m,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=dnwc,reinvestment=reinvest,reinvestment_rate=reinvest/nopat,fcff=fcff,pv_fcff=pv));prev_nopat=nopat
 terminal_nopat=rows[-1]['nopat']*(1+c['g']);terminal_reinvest=terminal_nopat*c['g']/c['roic'];terminal_fcff=terminal_nopat-terminal_reinvest
 tv=terminal_fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev=sum(x['pv_fcff'] for x in rows)+pvtv
 deductions=sum(v for k,v in BRIDGE.items() if k!='excess_cash');equity=ev+c['acquisition_value']-deductions+BRIDGE['excess_cash']
 assert all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']-x['delta_nwc']))<1e-8 for x in rows)
 assert abs(rows[-1]['reinvestment_rate']-c['g']/c['roic'])<1e-8
 terminal_revenue=rows[-1]['revenue']*(1+c['g'])
 terminal_da=terminal_revenue*.035
 terminal_dnwc=.15*(terminal_revenue-rows[-1]['revenue'])
 terminal_capex=terminal_da+terminal_reinvest-terminal_dnwc
 assert abs(terminal_fcff-(terminal_nopat+terminal_da-terminal_capex-terminal_dnwc))<1e-8
 terminal_components=dict(year=11,revenue=terminal_revenue,ebit=terminal_revenue*c['terminal_margin'],nopat=terminal_nopat,da=terminal_da,capex=terminal_capex,delta_nwc=terminal_dnwc,reinvestment=terminal_reinvest,fcff=terminal_fcff)
 return dict(assumptions=c,rows=rows,terminal_components=terminal_components,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvest,terminal_fcff=terminal_fcff,terminal_value=tv,pv_terminal=pvtv,terminal_weight=pvtv/ev,ev_standalone=ev,bridge=BRIDGE,acquisition_value=c['acquisition_value'],equity=equity,value_per_share=equity/SHARES,upside=equity/SHARES/PRICE-1)
def solve(key):
 lo,hi=(-.03,.12) if key=='volume' else (.08,.25)
 for i in range(100):
  mid=(lo+hi)/2;c=copy.deepcopy(CASES['central'])
  if key=='volume':c['volume']=[mid]*5
  else:c['margins']=[mid]*5;c['terminal_margin']=mid
  if dcf(c)['value_per_share']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
out={'as_of':'2026-11-07','regular_close':PRICE,'shares':SHARES,'scenarios':{k:dcf(v) for k,v in CASES.items()},'reverse':{'constant_volume_first5_years':solve('volume'),'constant_ebit_margin_all_years':solve('margin')},'sensitivity':[]}
for w in [.07,.075,.08,.085,.09]:
 for g in [.01,.015,.02,.025,.03]:
  c=copy.deepcopy(CASES['central']);c.update(wacc=w,g=g);out['sensitivity'].append({'wacc':w,'g':g,'value':dcf(c)['value_per_share']})
# Data provenance: FYs 2025 10-K; Q1 2026 release; Q2 & Q3 2026 10-Qs; Q3 2025 release.
annual={'2023':[3756,512,298,1.42,124,644,104,14,210.0], '2024':[3695,549,352,1.67,129,489,120,19,210.4], '2025':[3721,492,301,1.43,135,477,161,21,210.4]}
quarters={'2025Q4':[1034,176,117,.56,35,237,37,3,210.4], '2026Q1':[877,98,59,.28,33,71,44,4,211.8], '2026Q2':[944,138,89,.42,32,102,57,4,211.8], '2026Q3':[944,98,58,.28,33,51,42,2,211.8]}
ttm={'2025TTM':[3707,496,305,None,133,422,165,23,210.3], '2026TTM':[3799,510,323,None,133,461,180,13,211.8]}
labels=['revenue','ebit','net_income','eps_reported','da','cfo','capex','sbc','diluted_shares']
financials={}
for period,vals in {**annual,**quarters,**ttm}.items():
 x=dict(zip(labels,vals));x.update(fcf=x['cfo']-x['capex'],fcf_per_share=(x['cfo']-x['capex'])/x['diluted_shares'],operating_margin=x['ebit']/x['revenue'],fcf_conversion=(x['cfo']-x['capex'])/x['net_income']);financials[period]=x
out['financials']=financials
out['cash_bridge']={'reported_ttm_cfo':461,'cash_capex':180,'reported_fcf':281,'subtract_sbc':13,'add_aftertax_net_interest':66,'cash_fcff_proxy':334,'reported_ebit':510,'environmental_reserve_addback':25,'ceo_transition_addback':2,'retained_strategic_and_other_costs':14,'normalized_ebit':537,'normalized_nopat':402.75,'da':133,'cash_capex':180,'normalized_delta_nwc_at_2pct_growth':.15*3799*.02,'normalized_fcff':402.75+133-180-.15*3799*.02}
# Audit diagnostics are not replacement forecasts. Additional capex stress is
# imposed only in years 1-10, leaving the terminal ROIC convention unchanged.
out['audit_diagnostics']={'label':'Illustrative audit sensitivity',
 'cash_capex_plus_9m_finance_lease_additions':180+33,
 'normalized_fcff_after_33_economic_capex_stress':344.353-33,
 'value_after_additional_33_capex_each_explicit_year':out['scenarios']['central']['value_per_share']-sum(33/1.08**t for t in range(1,11))/SHARES,
 'capex_stress_terminal_treatment':'No additional terminal stress; not a perpetual 33 cost scenario',
 'software':'No separately quantified material software capitalization found in FY25 or Q3 2026 disclosures; no zero-spend assertion or addback',
 'price_source':'https://stockanalysis.com/stocks/reyn/history/',
 'price_as_of':'2026-11-06T16:00:00-05:00',
 'price_verification':'Opened dated history row and timestamp on 2026-11-07; not an intraday/live quote'}
out['capm']={'rf':.0486,'raw_beta_secondary':.56,'analyst_beta':.80,'assumed_erp':.05,'prospective_kd':.057,'debt_weight':.25,'tax':TAX,'calculated_wacc':.75*(.0486+.80*.05)+.25*.057*(1-TAX),'selected_wacc':.08,'provenance':'Report C1-C5; RF secondary dated evidence, ERP/beta adjustment/weights analyst assumptions'}
(P/'results.json').write_text(json.dumps(out,indent=2))
for k,x in out['scenarios'].items():
 with (P/f'forecast_{k}.csv').open('w') as f:
  wr=csv.DictWriter(f,fieldnames=x['rows'][0]);wr.writeheader();wr.writerows(x['rows'])
(P/'run_log.json').write_text(json.dumps({'status':'senior-review-ready','model_type':'deterministic Python support, not banker formula workbook','checks':{'ten_years':all(len(x['rows'])==10 for x in out['scenarios'].values()),'fcff_identity':True,'terminal_reinvestment_identity':True,'no_future_share_buybacks':True},'bounded_proxies':['finance leases 47 upper bound','OHA value 0/110/165','cash excess zero','postretirement current component 1 carried from FY25'],'hard_failures':[]},indent=2))
print(json.dumps({k:{a:v for a,v in x.items() if a in ['value_per_share','terminal_weight','upside','ev_standalone','equity']} for k,x in out['scenarios'].items()},indent=2));print(out['reverse']);print(out['cash_bridge'])
