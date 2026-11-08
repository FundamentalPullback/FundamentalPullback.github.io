"""UNP standalone FCFF illustration only. Not merger-inclusive fair value or Stage3 approval.
Run python model.py. USD millions except per share.
"""
from pathlib import Path
import json,csv
P=Path(__file__).parent
REV=26363; EBIT=10565; PRICE=290.16; SH=594.5; DEBT=30324
CASH=2211+875; MINCASH=1500; NONOP=2000 # TTX book-value proxy only, pending valuation
RF=.0486; ERP=.0441; BETA=.85; KE=RF+BETA*ERP
E=PRICE*SH; DMARKET=22800; KD=.0575; TAX=.24
WACC=KE*E/(E+DMARKET)+KD*(1-TAX)*DMARKET/(E+DMARKET)
ENV={1:65,2:209/4,3:209/4,4:209/4,5:209/4} # gross legacy settlement assumption; no tax benefit presumed

def value(g1=.045,m5=.415,m10=.40,capex=.145,wacc=WACC,gt=.025,roic=.15):
 revenue=REV;pv=0;rows=[]
 for t in range(1,11):
  trans=max(0,(t-5)/5);g=g1+(gt-g1)*trans
  prev=revenue;revenue*=1+g
  margin=EBIT/REV+(m5-EBIT/REV)*t/5 if t<=5 else m5+(m10-m5)*trans
  da_ratio=.097; nwc=.05*(revenue-prev); nopat=revenue*margin*(1-TAX)
  fcff=nopat+revenue*da_ratio-revenue*capex-nwc
  pv+=fcff/(1+wacc)**t
  rows.append(dict(year=t,revenue=revenue,growth=g,ebit_margin=margin,nopat=nopat,DA=revenue*da_ratio,capex=revenue*capex,delta_wc=nwc,fcff=fcff))
 term_nopat=rows[-1]['nopat']*(1+gt);term_reinvest=term_nopat*gt/roic;term_reinvest=max(term_reinvest,rows[-1]['revenue']*(1+gt)*(capex-.097)+.05*rows[-1]['revenue']*gt);term_fcff=term_nopat-term_reinvest
 tv=term_fcff/(wacc-gt);pv_tv=tv/(1+wacc)**10;ev=pv+pv_tv;eq=ev-DEBT+CASH-MINCASH+NONOP-sum(c/(1+KE)**t for t,c in ENV.items())
 return dict(value=eq/SH,upside=eq/SH/PRICE-1,EV=ev,equity=eq,terminal_share=pv_tv/ev,terminal_fcff=term_fcff,terminal_reinvestment=term_reinvest,terminal_ROIC=roic,wacc=wacc,g1=g1,m5=m5,m10=m10,capex_ratio=capex,gt=gt,rows=rows)
cases={'adverso':value(.02,.38,.37,.16,.09,.02,.12),'central':value(),'favorable':value(.065,.44,.43,.14,.0725,.03,.18)}
def inv(wacc=WACC,m=.415):
 lo,hi=-.1,.3
 for _ in range(100):
  x=(lo+hi)/2
  if value(g1=x,m5=m,wacc=wacc)['value']<PRICE:lo=x
  else:hi=x
 return (lo+hi)/2
sens=[dict(wacc=w,g_terminal=g,value=value(wacc=w,gt=g)['value']) for w in [.0725,.08,.0875,.095] for g in [.02,.025,.03]]
annual=[('2023',24119,9082,6379,10.45,2318,8379,3606,107,610.2),('2024',24250,9713,6747,11.09,2398,9346,3452,118,608.6),('2025',24510,9846,7138,11.98,2465,9290,3791,142,595.9)]
quarters=[('2025Q4',6085,2401,1848,3.11,624),('2026Q1',6217,2458,1701,2.87,633),('2026Q2',6864,2763,1993,3.36,638),('2026Q3',7197,2943,2076,3.49,643)]
assert sum(x[1] for x in quarters)==REV;assert sum(x[2] for x in quarters)==EBIT
for fn,head,rows in [('financials_annual.csv',['period','revenue','EBIT','net_income','EPS_diluted','DA','CFO','cash_capex','SBC','diluted_shares'],annual),('financials_quarterly.csv',['period','revenue','EBIT','net_income','EPS_diluted','DA'],quarters)]:
 with (P/fn).open('w') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
# Transaction constants; final dated formula replaces initial metadata below.
new_shares=225;new_cash=225*88.82
r={'status':'partial_standalone_only_not_approved','as_of':'2026-11-08','regular_close':PRICE,'close_date':'2026-11-06','close_time':'16:00 America/New_York','scanner_last':290.16,'rf':RF,'erp':ERP,'beta_5Y_monthly':BETA,'ke':KE,'kd_assumption':KD,'tax_assumption':TAX,'wacc_derived':WACC,'market_equity':E,'market_debt_for_weights':DMARKET,'debt_claim_deducted':DEBT,'gross_cash_short_investments':CASH,'minimum_operating_cash_assumption':MINCASH,'TTX_book_proxy_nonoperating':NONOP,'cases':cases,'inverse_growth_same_model':inv(),'sensitivity':sens,'TTM':{'revenue':REV,'EBIT':EBIT,'net_income':7618,'DA':2538,'CFO':10527,'cash_capex':3833,'levered_CFO_less_capex':6694,'SBC':130,'normalized_start_FCFF':EBIT*(1-TAX)+2538-3833-100},'merger':{'new_UNP_shares_estimate':new_shares,'cash_per_NSC':88.82,'cash_consideration_from_share_estimate':new_cash,'proforma_share_floor':SH+new_shares,'old_holders_ownership':SH/(SH+new_shares),'new_shares_as_percent_old':new_shares/SH,'break_fee_conditional':2500,'break_fee_per_old_diluted_share':2500/SH,'cash_plus_market_value_new_shares':new_shares*PRICE+new_cash,'NSC_equity_plus_net_synergies_less_costs_needed_for_combined_290_16':(SH+new_shares)*PRICE-cases['central']['equity']+new_cash,'formula':'Combined equity = UNP standalone equity + NSC standalone equity + PV(net synergies) - cash consideration - transaction/integration costs; divide by old diluted shares + new shares. NSC equity already subtracts NSC debt. Cash financed with new debt or existing cash is deducted once, not twice.','missing':['NSC standalone equity and debt/contingencies','financing amount/cost and future accumulated cash through actual close','net synergy/integration capex and regulatory remedies','conversion awards and final share count']},'QA':{'TTM_quarters_tie':True,'no_operating_lease_double_deduction':True,'SBC_kept_in_operating_margin':True,'no_free_buybacks':True,'not_merger_inclusive':True}}
(P/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:{a:v[a] for a in ['value','upside','terminal_share']} for k,v in cases.items()},indent=2));print('wacc',WACC,'inverse',inv(),'merger required equity+synergies lesscost',new_shares*PRICE+new_cash)

# Conditional transaction overlay. NSC equity is modeled independently; not a market quote.
# No probabilities or approved merger fair value claimed. Dated closing bridge below.
def nsc_value(g=.04,margin=.355,wacc=.085,gt=.025):
 rev=12963; pv=0; rows=[]
 for t in range(1,11):
  growth=g+(gt-g)*max(0,(t-5)/5);old=rev;rev*=1+growth
  m=4088/12963+(margin-4088/12963)*min(t/5,1)
  fcff=rev*m*.76+rev*.11-rev*.175-.05*(rev-old)
  pv+=fcff/(1+wacc)**t;rows.append({'year':t,'revenue':rev,'margin':m,'fcff':fcff})
 tn=rev*(1+gt)*margin*.76
 reinvest=max(tn*gt/.13,rev*(1+gt)*(.175-.11)+.05*rev*gt)
 terminal=(tn-reinvest)/(wacc-gt)/(1+wacc)**10
 claims=373+277+125+534 # incident, unfunded pension, OPEB, Conrail advances (pension/OPEB FY25 proxies; Conrail confirmed Sept30 2026)
 equity=pv+terminal-16613+1598-750-claims
 return {'equity':equity,'EV':pv+terminal,'claims':claims,'terminal_share':terminal/(pv+terminal),'rows':rows,'assumptions':{'g':g,'margin':margin,'wacc':wacc,'capex_ratio':.175,'DA_ratio':.11,'terminal_ROIC':.13,'nonop_asset_addition':0}}
ns=nsc_value()
def combo(realization=1,close=1,integration=3000,remedy=0):
 # t=0 2026-11-08, close at t=1 (2027-11-08) or t=3 (2029-11-08).
 # Pre-close debt held constant: maturities refinanced, no repurchases. Cash earns zero.
 # Dividends are assumptions, not additional FCFF expenses. Existing interest proxies explicit.
 u=cases['central'];n=ns;wu=WACC;wn=.085;ke_close=KE
 def remaining_ev(v,w):
  return v['EV']*(1+w)**close-sum(row['fcff']*(1+w)**(close-row['year']) for row in v['rows'] if row['year']<=close)
 cu=CASH;cn=1598;pre=[];pv_div=0
 for t in range(1,close+1):
  uf=u['rows'][t-1]['fcff'];nf=n['rows'][t-1]['fcff']
  du=3312;dn=1215 # UNP nine-month 2484 annualized; NSC illustrative 5.40*225
  ui=1270*.76;ni=782*.76;env=ENV.get(t,0)
  cu+=uf-ui-du-env;cn+=nf-ni-dn
  pv_div+=du/(1+KE)**t
  pre.append({'year':t,'UNP_FCFF':uf,'NSC_FCFF':nf,'UNP_after_tax_interest':ui,'NSC_after_tax_interest':ni,'UNP_distribution':du,'NSC_distribution':dn,'UNP_legacy_environment_payment':env,'UNP_cash_end':cu,'NSC_cash_end':cn,'UNP_debt_end':DEBT,'NSC_debt_end':16613})
 # Only UNP surplus cash funds acquisition at closing. Target cash remains on balance sheet.
 used=min(new_cash,max(0,cu-MINCASH));newdebt=new_cash-used
 postcash=cu+cn-used;postdebt=DEBT+16613+newdebt
 sy=0;flows=[];w=.085
 for j in range(1,31):
  ramp=min(j/3,1);eb=2750*realization*ramp
  cf=eb*.66-(2100+integration)/3*(j<=3)-remedy*ramp
  sy+=cf/(1+w)**j;flows.append({'year_after_close':j,'net_synergy_cash':cf})
 sy+=(2750*realization*.66-remedy)/w/(1+w)**30
 env_remaining=sum(c/(1+KE)**(t-close) for t,c in ENV.items() if t>close)
 eu=remaining_ev(u,wu);en=remaining_ev(n,wn)
 # NSC booked claim basket held unchanged until closing (no estimated payments counted twice).
 equity=eu+en+sy-postdebt+postcash-MINCASH-750+NONOP-n['claims']-env_remaining
 current=pv_div/SH+equity/(SH+new_shares)/(1+ke_close)**close
 return {'current_old_share_value':current,'close_year':close,'close_date_assumption':f'{2026+close}-11-08','preclose_distributions_PV':pv_div,'preclose_distribution_PV_per_old_share':pv_div/SH,'closing_equity':equity,'closing_value_per_combined_share':equity/(SH+new_shares),'remaining_UNP_EV_at_close':eu,'remaining_NSC_EV_at_close':en,'net_synergy_value_at_close':sy,'cash_purchase_at_close':new_cash,'UNP_cash_used_at_close':used,'new_debt_at_close':newdebt,'postclose_gross_debt':postdebt,'postclose_gross_cash':postcash,'remaining_UNP_environment_PV_at_close':env_remaining,'NSC_claims_at_close_assumption':n['claims'],'postclose_share_count':SH+new_shares,'old_holder_ownership_at_close':SH/(SH+new_shares),'equity_discount_to_today':ke_close,'realization':realization,'integration_cash_assumption':integration,'annual_remedy_cost_assumption':remedy,'preclose_roll':pre,'flows_after_close':flows}
r['NSC']=ns
r['merger']['conditional_outcomes']={'close_full_claim':combo(),'close_half_synergies_remedies':combo(.5,1,4000,200),'delay_two_years':combo(1,3,4000),'failure_no_fee':{'old_share_value':cases['central']['value']},'failure_fee_triggered':{'old_share_value':cases['central']['value']-2500/(1+KE)/SH}}
r['merger']['illustrative_funding']={'cash_payment':new_cash,'inherited_UNP_debt':30324,'inherited_NSC_debt':16613,'new_debt_range_assumption':[14000,18000],'gross_proforma_debt_range':[60937,64937],'interest_rate_range_assumption':[.055,.065],'annual_new_interest_range':[770,1170],'after_tax_interest_range':[585.2,889.2],'extra_cash_needed_range':[1984.5,5984.5],'current_UNP_cash_above_floor':1586,'note':'Funding capacity illustration, not committed debt or forecast. NSC cash is not assumed available before closing. NSC debt already deducted in target equity; cash purchase deducted once. Interest is shown diagnostically, not also subtracted from FCFF.'}
r['merger']['missing']=['Final financing terms, commitments, award conversion and issued shares','Integration cash spend and regulatory remedies, retention of synergy claims','NSC contingent losses beyond booked reserves; September pension reconciliation; Conrail confirmed September 30','Acquisition tax basis and purchase accounting; cost of capital after financing']
r['QA']['conditional_merger_overlay']=True
r['status']='partial_standalone_and_conditional_merger_not_approved'
(P/'results.json').write_text(json.dumps(r,indent=2))
print('NSC equity',ns['equity']); print('conditional merger', {k:v.get('current_old_share_value',v.get('old_share_value')) for k,v in r['merger']['conditional_outcomes'].items()})

r['environmental_claim_bridge']={'reserve':274,'current':65,'gross_cash_schedule_assumption':ENV,'tax_benefit_assumed':0,'FCFF_treatment':'Base operating margins retain ordinary environmental costs; no separately identifiable legacy settlement is in projected capex or delta WC. Deduct scheduled legacy payments outside FCFF. Overlap sensitivity removes this deduction to bound unidentified embedded settlements.','PV_deduction':sum(c/(1+KE)**t for t,c in ENV.items()),'per_share_zero_overlap':sum(c/(1+KE)**t for t,c in ENV.items())/SH,'per_share_full_overlap':0,'gross_immediate_upper_deduction':274/SH}
r['merger']['formula']='At dated close: remaining operating EVs + synergy value - rolled debt incl new financing + rolled cash after purchase - minimum cash + nonoperating proxy - remaining legacy claims. Current old-share payoff = PV(old-holder preclose distributions)/old shares + PV(closing equity/postclose diluted shares). No immediate dilution of preclose dividends.'
r['merger'].pop('NSC_equity_plus_net_synergies_less_costs_needed_for_combined_290_16',None)
r['merger'].pop('illustrative_funding',None)
r['QA']['terminal_physical_capex_floor']=True
r['QA']['dated_closing_bridge']=True
r['QA']['environment_settlements_not_in_operating_WC']=True
(P/'results.json').write_text(json.dumps(r,indent=2))
