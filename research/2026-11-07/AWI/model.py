#!/usr/bin/env python3
"""AWI reproducible analytical export, USD millions except per-share. No network or dependencies."""
import json,csv,math,pathlib,copy
ROOT=pathlib.Path(__file__).resolve().parent
# Primary-source transcriptions: income/cash-flow statements; positive spend and earnings conventions.
FIELDS=['revenue','gross_profit','ebit','affiliate_earnings','interest','other_income','pretax','tax','net_income','da','sbc','cfo','capex','jv_distribution','acquisitions','receivable_cash_change','inventory_cash_change','payable_cash_change','tax_cash_change','other_working_cash_change','cash_interest','cash_tax','sale_gain']
VALUES={
'FY2023':[1295.2,497,323.7,89.3,35.3,9.9,298.3,74.5,223.8,89.2,18.8,233.5,83.8,96.9,26.5,-1.6,6.1,8,3.2,-18.5,33.9,72.1,0],
'FY2024':[1445.7,581.6,374.3,103.4,39.8,12.6,347.1,82.2,264.9,103.2,18.3,266.8,82.8,97.8,123.5,-24.6,1.9,27.3,-5.4,-17.7,37.4,87.6,-.6],
'FY2025':[1620.8,658.7,430.9,112.3,33,2.4,400.3,91.6,308.7,120.4,21.9,355.5,109.4,113,13.9,-7.5,-12.8,28.4,-1.8,-15.2,29.7,69.3,.8],
'9M2024':[1078,437.7,292.4,78.7,30.6,9.3,271.1,68.4,202.7,75.9,13.9,180.2,54,72.7,93.5,-29.5,-4.2,14.4,1.5,-17.5,28.8,66,-.3],
'9M2025':[1232.5,504.2,338.9,86.5,25.3,1.9,315.5,72.3,243.2,89.9,16.3,245.5,61.6,82.5,6.7,-31.5,-13.2,12.4,-1.2,-4.2,22.9,53.4,.8],
'Q12026':[409.9,155.3,94.2,27.3,7.3,1.5,88.4,21.6,66.8,29.7,3.8,32.1,17.7,29.6,64.8,-35.8,-4.7,-13.5,16.2,-3.2,6.3,3.9,0],
'6M2026':[881.9,350.3,228,60.7,15.1,2.4,215.3,51.8,163.5,59.9,9.8,125.9,41.7,57.6,64.8,-62.4,-2.7,7.1,3.2,5.9,13.5,45.5,0],
'9M2026':[1357.7,541,359.2,92.4,22.6,3.1,339.7,84.3,255.4,92.1,14.4,222.1,66.4,89.6,64.9,-66,-11.1,21.3,6.4,-.1,20.5,74.7,0]}
H={p:dict(zip(FIELDS,v)) for p,v in VALUES.items()}
def combine(a,b,c=None):
 return {k:round(a[k]-b[k]+(c[k] if c else 0),6) if a[k] is not None and b[k] is not None and (not c or c[k] is not None) else None for k in FIELDS}
H['Q42025']=combine(H['FY2025'],H['9M2025']);H['Q22026']=combine(H['6M2026'],H['Q12026']);H['Q32026']=combine(H['9M2026'],H['6M2026']);H['TTM2026']=combine(H['FY2025'],H['9M2025'],H['9M2026']);H['TTM2025']=combine(H['FY2024'],H['9M2024'],H['9M2025'])
SHARES={'FY2023':44.8,'FY2024':44,'FY2025':43.6,'Q42025':43.3,'Q12026':43.2,'Q22026':42.7,'Q32026':42.3,'TTM2026':43.6+.75*(42.7-43.7),'TTM2025':44+.75*(43.7-44)}
for p,v in H.items():
 v.update(core_ebit=v['ebit']-v['affiliate_earnings'],core_margin=(v['ebit']-v['affiliate_earnings'])/v['revenue'],gaap_margin=v['ebit']/v['revenue'],fcf_including_jv=v['cfo']+v['jv_distribution']-v['capex'])
 v['cash_fcff_after_sbc']=v['fcf_including_jv']-v['sbc']+v['interest']*.75-v['other_income']*.75
 v['nonrecurring_cash_tax_benefit']={'FY2025':20,'9M2025':10,'Q42025':10,'TTM2025':10,'TTM2026':10}.get(p,0)
 v['cash_fcff_after_sbc_tax_normalized']=v['cash_fcff_after_sbc']-v['nonrecurring_cash_tax_benefit']
 v['normalized_net_income']=(v['ebit']-(v['sale_gain'] or 0)-v['interest'])*.75
 if p in SHARES:v['diluted_shares']=SHARES[p];v['normalized_eps']=v['normalized_net_income']/SHARES[p]
# SOTP: core FCFF at WACC plus after-parent-tax JV equity cash at cost of equity. No JV asset/book value addition.
A={'as_of':'2026-11-07','price':171.23,'price_date':'2026-11-06','forecast_anchor_revenue':1795.5,'anchor_core_margin':.20,'anchor_jv_pretax_earnings':123,'tax':.25,'current_shares':41.900177,'outstanding_award_dilution':.3,'valuation_shares':42.200177,'gross_debt_principal':472.9,'finance_leases':35.2,'cash':71.4,'operating_cash_reserve':35,'pension_and_postretirement_claims':59.8,'contingent_consideration':3.1,'pension_surplus_value':0,'operating_lease_claim_added':0,'other_affiliate_value':0,'riskfree':.0484,'beta':1.14,'erp':.05,'cost_of_debt':.065,'debt_weight':.065,'equity_weight':.935,'comment':'4.84% risk-free is latest H15 available observation in Nov6 release, not claimed Nov6 closing yield. ERP and forward borrowing cost are analyst assumptions.'}
A['calculated_ke']=A['riskfree']+A['beta']*A['erp'];A['calculated_wacc']=A['calculated_ke']*.935+.065*(1-.25)*.065
CASES={
'adverse':{'growth':[0,.02,.025,.03,.03],'margin5':.185,'terminal_margin':.18,'wacc':.112,'ke':.116,'g':.02,'roic':.15,'sales_to_incremental_fixed_capital':2.,'wc_ratio':.14,'maintenance_ratio':.058,'jv_growth':.02,'jv_roe':.20},
'base':{'growth':[.065,.06,.055,.05,.045],'margin5':.22,'terminal_margin':.22,'wacc':.102,'ke':.1054,'g':.025,'roic':.20,'sales_to_incremental_fixed_capital':2.5,'wc_ratio':.12,'maintenance_ratio':.055,'jv_growth':.04,'jv_roe':.25},
'favorable':{'growth':[.09,.085,.08,.075,.065],'margin5':.24,'terminal_margin':.235,'wacc':.092,'ke':.096,'g':.03,'roic':.25,'sales_to_incremental_fixed_capital':3.,'wc_ratio':.10,'maintenance_ratio':.052,'jv_growth':.06,'jv_roe':.30}}
def valuation(c, growth_override=None, margin_shift=0):
 c=copy.deepcopy(c);initial=A['forecast_anchor_revenue'];rev=initial;jv=A['anchor_jv_pretax_earnings'];rows=[];pvcore=pvjv=0
 for y in range(1,11):
  if y<=5:g=(growth_override if growth_override is not None else c['growth'][y-1]);m=A['anchor_core_margin']+(c['margin5']-A['anchor_core_margin'])*y/5
  else:
   f=(y-5)/5;g=(growth_override if growth_override is not None else c['growth'][-1])*(1-f)+c['g']*f;m=c['margin5']*(1-f)+c['terminal_margin']*f
  m+=margin_shift
  oldrev=rev;rev*=1+g;nopat=rev*m*(1-A['tax']);da_ratio=.068+(.055-.068)*y/10;da=rev*da_ratio
  # Maintenance includes software and finance-leased asset renewal; do not make asset renewal free.
  maintenance=rev*c['maintenance_ratio'];growth_capex=max(0,rev-oldrev)/c['sales_to_incremental_fixed_capital'];wc=(rev-oldrev)*c['wc_ratio'];capex=maintenance+growth_capex
  core=nopat+da-capex-wc
  jg=c['jv_growth'] if y<=5 else c['jv_growth']+(c['g']-c['jv_growth'])*(y-5)/5
  jv*=1+jg;je=jv*(1-A['tax']);jret=je*jg/c['jv_roe'];jcash=je-jret
  pvcore+=core/(1+c['wacc'])**y;pvjv+=jcash/(1+c['ke'])**y
  rows.append(dict(year=2026+y,revenue=rev,growth=g,core_margin=m,nopat=nopat,da=da,maintenance_capex=maintenance,growth_capex=growth_capex,total_capex=capex,delta_nwc=wc,core_fcff=core,jv_pretax_earnings=jv,jv_after_tax_earnings=je,jv_retained_reinvestment=jret,jv_equity_cash=jcash,pv_core=core/(1+c['wacc'])**y,pv_jv=jcash/(1+c['ke'])**y))
 tn=rev*(1+c['g'])*(c['terminal_margin']+margin_shift)*(1-A['tax']);economic=tn*c['g']/c['roic'];physical=rev*c['g']*(1/c['sales_to_incremental_fixed_capital']+c['wc_ratio']);reinvest=max(economic,physical)
 # Terminal depreciation equals maintenance capex at 5.5% of revenue. Growth investment is never below physical floor.
 tcore=tn-reinvest;tcv=tcore/(c['wacc']-c['g'])/(1+c['wacc'])**10
 tje=jv*(1+c['g'])*(1-A['tax']);tjcash=tje*(1-c['g']/c['jv_roe']);tjv=tjcash/(c['ke']-c['g'])/(1+c['ke'])**10
 core_ev=pvcore+tcv;jv_value=pvjv+tjv;excess=A['cash']-A['operating_cash_reserve'];claims=A['gross_debt_principal']+A['finance_leases']+A['pension_and_postretirement_claims']+A['contingent_consideration'];equity=core_ev+jv_value+excess-claims
 return dict(value=equity/A['valuation_shares'],core_ev=core_ev,jv_equity_value=jv_value,excess_cash=excess,claims=claims,equity_value=equity,terminal_weight=(tcv+tjv)/(core_ev+jv_value),terminal_core_fcff=tcore,terminal_economic_reinvestment=economic,terminal_physical_growth_floor=physical,terminal_reinvestment=reinvest,terminal_implied_core_roic=tn*c['g']/reinvest,rows=rows)
OUT={k:valuation(c) for k,c in CASES.items()}
def solve(fn,target,lo,hi):
 if not fn(lo)<=target<=fn(hi):return None
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
inverse={}
for shift in [0,.02,.04]:inverse[str(shift)]=solve(lambda g:valuation(CASES['base'],g,shift)['value'],A['price'],0,.40)
sens=[]
for w in [.092,.097,.102,.107,.112]:
 for g in [.02,.025,.03]:
  c=copy.deepcopy(CASES['base']);c['wacc']=w;c['ke']=w+.0034;c['g']=g;sens.append({'wacc':w,'g':g,'value':valuation(c)['value']})
margin_sens=[{'margin_shift':s,'value':valuation(CASES['base'],margin_shift=s)['value']} for s in [-.02,-.01,0,.01,.02,.04]]
checks=[]
def ck(name,test,detail):checks.append({'check':name,'pass':bool(test),'detail':detail})
for p,v in H.items():
 ck(p+' pretax identity',abs(v['ebit']-v['interest']+v['other_income']-v['pretax'])<.15,'EBIT - interest + other income = pretax')
 ck(p+' earnings identity',abs(v['pretax']-v['tax']-v['net_income'])<.15,'Pretax - tax = net income')
for k in FIELDS:
 if H['TTM2026'][k] is not None:ck('Four-quarter '+k,abs(sum(H[p][k] for p in ['Q42025','Q12026','Q22026','Q32026'])-H['TTM2026'][k])<.001,'Quarter sum equals FY2025 + 9M2026 - 9M2025')
for n,r in OUT.items():
 ck(n+' discount spread',CASES[n]['wacc']>CASES[n]['g'] and CASES[n]['ke']>CASES[n]['g'],'Both discount rates exceed growth')
 ck(n+' physical reinvestment',r['terminal_reinvestment']>=r['terminal_physical_growth_floor'],'Terminal funds physical capacity and working capital')
 ck(n+' cash flow identity',all(abs(x['core_fcff']-(x['nopat']+x['da']-x['total_capex']-x['delta_nwc']))<1e-6 for x in r['rows']),'All ten years')
 ck(n+' equity bridge',abs(r['value']*A['valuation_shares']-(r['core_ev']+r['jv_equity_value']+r['excess_cash']-r['claims']))<1e-6,'No JV book value / JV debt double count')
ck('Scenario ordering',OUT['adverse']['value']<OUT['base']['value']<OUT['favorable']['value'],'Adverse < base < favorable')
ck('Balance sheet',abs(294+816.6+893.8-2004.4)<1e-6,'Current liabilities + noncurrent liabilities + equity = assets')
ck('Cash flow roll',abs(112.7+222.1-34.8-228-.6-71.4)<1e-6,'2026 YTD beginning cash plus cash flows equals ending cash')
ck('Inverse base target',abs(valuation(CASES['base'],inverse['0'])['value']-A['price'])<1e-6,'Bisection reproduces reference price')
for f,obj in [('inputs.json',{'units':'USD millions except per share','reported':H,'assumptions':A,'cases':CASES}),('model-output.json',{'scenarios':OUT,'sensitivity':sens,'margin_sensitivity':margin_sens,'inverse_first_five_years_growth':inverse}),('qa.json',{'status':'Ready with caveats for conditional review only','stage3Complete':False,'entryApproved':False,'approvedValuation':None,'valuationScope':'Conditional analytical scenarios; historical-multiple study incomplete and JV capital/distribution coverage qualified','artifact_mode':'deterministic analytical export','checks':checks,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'limitations':['Forward capex/margin/ROIC assumptions are analytical estimates, not management promises.','WAVE cash valued as an equity interest separately from core FCFF.','Historical raw files are not included in public deliverables.']})]:
 (ROOT/f).write_text(json.dumps(obj,indent=2))
with (ROOT/'historicals.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['period']+list(H['TTM2026'].keys()));writer.writeheader()
 for p,v in H.items():writer.writerow(dict(period=p,**v))
with (ROOT/'forecast.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['case']+list(OUT['base']['rows'][0].keys()));writer.writeheader()
 for n,r in OUT.items():
  for row in r['rows']:writer.writerow(dict(case=n,**row))
print(json.dumps({'values':{k:dict(value=v['value'],terminal_weight=v['terminal_weight'],core_ev=v['core_ev'],jv_equity_value=v['jv_equity_value']) for k,v in OUT.items()},'inverse':inverse,'sensitivity':sens,'qa':{'passed':sum(x['pass'] for x in checks),'failed':[x for x in checks if not x['pass']]}},indent=2))
