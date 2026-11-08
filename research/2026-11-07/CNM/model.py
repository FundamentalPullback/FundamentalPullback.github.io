"""CNM, USD million. Deterministic support calculation requested by research lead.
Run python model.py. No trades, publication or price-fitting assumptions.
Sources and rationale: report.md, sources.json. All forward values analyst estimates.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
PRICE=45.97; REV=7698.; TAX=.249
SHARES=184.192708+6.301342+(193.359334-186.639659-6.301342)
DEBT=2478.; CASH=312.-11.; OPERATING_CASH=.01*REV
CONTINGENT=12.; TAX_PARTNERSHIP_NET=55.-43.
RF=.0529; ERP=.0441; BETA=.91; KD=.06
KE=RF+BETA*ERP
E=PRICE*SHARES
WACC=KE*E/(E+DEBT)+KD*(1-TAX)*DEBT/(E+DEBT)
CASES={
 'adverso':{'growth':[-.02,0,.015,.02,.02],'margins':[.108,.108,.109,.110,.110],'terminal_margin':.105,'g':.02,'roic':.10,'nwc':.22,'capex':.009},
 'central':{'growth':[.025,.03,.035,.035,.03],'margins':[.116,.117,.118,.118,.118],'terminal_margin':.114,'g':.025,'roic':.13,'nwc':.19,'capex':.008},
 'favorable':{'growth':[.04,.05,.05,.045,.04],'margins':[.119,.122,.124,.125,.125],'terminal_margin':.12,'g':.03,'roic':.16,'nwc':.17,'capex':.008}}
def tra_net(w,n=15):
 # Paired tax savings and TRA payments; EBIT taxed at statutory rate, no tax shield in FCFF.
 # PROVISIONAL ILLUSTRATION ONLY: 685/85% is not proven FUTURE savings.
 # Filing says payments lag tax utilization by two fiscal years. Past-realized
 # savings must not be credited again; the required split is unavailable.
 gross=685/.85
 benefit=sum((gross/n)/(1+w)**t for t in range(1,n+1))
 claim=.85*benefit
 return benefit,claim

def calc(case='central',w=WACC,g=None,shift=0,marginshift=0):
 c=CASES[case];g=c['g'] if g is None else g;assert w>g
 rev=REV;rows=[];amort=[136,127.5,116,103,90] # proxy rolling next 12-month periods; anchored 10-Q note 5
 for y in range(1,11):
  fade=max(0,(y-5)/5)
  growth=c['growth'][y-1]+shift if y<=5 else (c['growth'][-1]+shift)*(1-fade)+g*fade
  preamort=(c['margins'][y-1] if y<=5 else c['margins'][-1]*(1-fade)+c['terminal_margin']*fade)+marginshift
  old=rev;rev*=1+growth
  a=amort[y-1] if y<=5 else amort[-1]*(1-fade)
  da=.005*rev+a
  ebit=rev*preamort-a # SBC and lease rent stay expensed; maintenance depreciation included
  nopat=ebit*(1-TAX); dnwc=(rev-old)*c['nwc']
  ordinary_capex=rev*c['capex']
  target_reinvestment=nopat*growth/c['roic']
  target_capex=da+target_reinvestment-dnwc
  capex=ordinary_capex*(1-fade)+target_capex*fade
  fcff=nopat+da-capex-dnwc
  rows.append(dict(year=y,growth=growth,revenue=rev,pre_acquisition_amort_margin=preamort,acquisition_amortization=a,ebit=ebit,tax=ebit*TAX,nopat=nopat,da=da,capex_including_software=capex,delta_nwc=dnwc,acquisition_spend=0,fcff=fcff,pv_fcff=fcff/(1+w)**y))
 terminal_rev=rev*(1+g);tnopat=terminal_rev*(c['terminal_margin']+marginshift)*(1-TAX)
 reinv=tnopat*g/c['roic'];tda=.005*terminal_rev;tdnwc=(terminal_rev-rev)*c['nwc'];tcapex=tda+reinv-tdnwc
 tfcff=tnopat+tda-tcapex-tdnwc;tv=tfcff/(w-g);pvtv=tv/(1+w)**10;ev=sum(r['pv_fcff'] for r in rows)+pvtv
 ta,tl=tra_net(w)
 equity=ev-DEBT+CASH-OPERATING_CASH-CONTINGENT-TAX_PARTNERSHIP_NET+ta-tl
 return dict(wacc=w,g=g,roic=c['roic'],ev=ev,equity=equity,value=equity/SHARES,upside=equity/SHARES/PRICE-1,pv_terminal_share=pvtv/ev,pv_explicit=sum(r['pv_fcff'] for r in rows),pv_terminal=pvtv,tra_gross_tax_benefit_pv=ta,tra_liability_pv=tl,tra_net_pv=ta-tl,terminal=dict(revenue=terminal_rev,nopat=tnopat,da=tda,capex=tcapex,delta_nwc=tdnwc,reinvestment=reinv,fcff=tfcff),rows=rows)
def inverse(var,other=0):
 lo,hi=(-.08,.20) if var=='growth' else (-.08,.12)
 for _ in range(100):
  mid=(lo+hi)/2;r=calc(shift=mid if var=='growth' else other,marginshift=mid if var=='margin' else other)
  if r['value']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
historical_fcff={'cfo':683,'capex':55,'reported_fcf':628,'ebit':742,'statutory_nopat':742*(1-TAX),'net_income_consolidated':479,'operating_da':184,'cashflow_da':193,'sbc':14,'deferred_tax':34,'other_cashflow_adjustments':-1,'delta_nwc_mechanical':36,'fcff':742*(1-TAX)+184-55-36}
assert abs(628+(742*(1-TAX)-479)-9-14-34+1-historical_fcff['fcff'])<1e-7
out={'historical_fcff_bridge':historical_fcff,'asof':'2026-11-07','price':PRICE,'price_time':'2026-11-06T16:00:00-05:00','units':'USD million, shares million, price USD','rf':RF,'erp':ERP,'beta':BETA,'cost_equity':KE,'cost_debt':KD,'wacc':WACC,'shares':SHARES,'bridge':{'debt':DEBT,'cash_after_disclosed_buyback':CASH,'retained_operating_cash':OPERATING_CASH,'contingent_consideration':CONTINGENT,'net_tax_partnership_claim':TAX_PARTNERSHIP_NET,'operating_leases':300,'operating_leases_subtracted':False,'nci_subtracted':False},'scenarios':{k:calc(k) for k in CASES},'sensitivity':[{'wacc':w,'g':g,'value':calc(w=w,g=g)['value']} for w in [WACC-.01,WACC,WACC+.01] for g in [.02,.025,.03]],'inverse':{'growth_shift_all_explicit_years':inverse('growth'),'margin_shift_all_years':inverse('margin'),'growth_shift_if_margins_50bp_higher':inverse('growth',.005)},'bounds':{'tra_net_per_share_by_schedule':{str(n):(lambda z:(z[0]-z[1])/SHARES)(tra_net(WACC,n)) for n in [10,15,20]},'remove_tra_net_value':calc()['value']-calc()['tra_net_pv']/SHARES,'extra_software_16_annual_10years_value_hit':sum(16/(1+WACC)**t for t in range(1,11))/SHARES,'full_tra_acceleration_without_tax_realization_stress_hit':(685+calc()['tra_net_pv'])/SHARES}}
# Audit safeguard: preserve pre-audit illustration for traceability, not fair value.
out['valuation_status']='partial_pending_TRA_realized_vs_future_bridge'
out['audited_fair_value']=None
out['portfolio_action_ready']=False
out['tra_evidence']={'reported_gross_obligation':685,'current_due_next_12_months':41,'remaining_noncurrent':644,'payment_lag_fiscal_years':2,'future_unrealized_benefits':None,'liability_for_benefits_already_realized':None,'source':'Q2 FY2026 10-Q Note 7 and MD&A Liquidity'}
# Illustrative audit sensitivity, NOT a corrected forecast: current 41 in year 1,
# remaining 644 equal installments in years 2-15, no future tax-benefit credit.
claim_pv=41/(1+WACC)+sum((644/14)/(1+WACC)**t for t in range(2,16))
out['audit_sensitivities']={'label':'Illustrative audit sensitivity, not audited fair value','gross_claim_schedule_pv':claim_pv,'assumed_schedule':'41 year 1; 644 uniformly years 2-15; no tax-benefit credit','no_future_benefit_values':{k:(v['equity']-v['tra_net_pv']-claim_pv)/SHARES for k,v in out['scenarios'].items()},'all_obligation_immediate_no_future_benefit_values':{k:(v['equity']-v['tra_net_pv']-685)/SHARES for k,v in out['scenarios'].items()}}
for v in out['scenarios'].values():
 v['valuation_status']='provisional_unverified_TRA_pairing'
 v['audited_fair_value']=None
out['inverse']['status']='conditional_on_unverified_TRA_pairing'
checks={'ten_years':all(len(x['rows'])==10 for x in out['scenarios'].values()),'fcff_identity':all(abs(r['fcff']-(r['nopat']+r['da']-r['capex_including_software']-r['delta_nwc']))<1e-7 for x in out['scenarios'].values() for r in x['rows']),'terminal_reinvestment':all(abs(x['terminal']['capex']+x['terminal']['delta_nwc']-x['terminal']['da']-x['terminal']['nopat']*x['g']/x['roic'])<1e-7 for x in out['scenarios'].values()),'ordered':out['scenarios']['adverso']['value']<out['scenarios']['central']['value']<out['scenarios']['favorable']['value'],'positive_capex':all(r['capex_including_software']>0 for x in out['scenarios'].values() for r in x['rows'])}
assert all(checks.values()),checks
(P/'results.json').write_text(json.dumps(out,indent=2));(P/'run_log.json').write_text(json.dumps({'artifact':'deterministic_support_calculation','status':'partial_pending_material_valuation_bridge','checks':checks,'hard_failures':['TRA future-benefit amount versus already-realized benefits is unresolved; original paired-TRA values are not audited fair values.'],'warnings':['Analyst scenarios, not forecasts guaranteed by management.','Debt cost uses July issuance rather than live bond yield.','TRA timing and software bounds disclosed.','Independent audit completed with material TRA blocker; no completed valuation or publication approval.']},indent=2))
for k,r in out['scenarios'].items():
 with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
print(json.dumps({k:{f:v[f] for f in ['value','upside','pv_terminal_share']} for k,v in out['scenarios'].items()},indent=2));print('WACC',WACC,'inverse',out['inverse'],'bounds',out['bounds'])
