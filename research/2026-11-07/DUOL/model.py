"""DUOL FCFF research model. USD millions except per-share. Run locally, no network.
Source facts are latest-as-filed SEC facts archived 2026-11-08, cut off Nov 6.
No SBC addback; current diluted shares; future SBC retained economically in EBIT.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
facts=json.load(open(P/'financial_inputs.json'))
T={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'OperatingIncomeLoss','ni':'NetIncomeLoss','cfo':'NetCashProvidedByUsedInOperatingActivities','da':'DepreciationDepletionAndAmortization','ppe':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','interest':'InterestIncomeOperating','tax':'IncomeTaxExpenseBenefit'}
provenance=[]
def get(tag,start,end,unit='USD'):
 a=[x for x in facts[tag]['units'][unit] if x.get('start')==start and x['end']==end and x['filed']<='2026-11-06' and x['form'] in ['10-K','10-Q']]
 if not a:return None
 x=sorted(a,key=lambda x:x['filed'])[-1];provenance.append({'tag':tag,**x});return x['val']/(1e6 if unit=='USD' else 1)
# cash software+intangibles manually tied to cash-flow/recast FCF tables, not accrual additions.
software={(2023,12):10.493,(2024,3):3.607,(2024,6):6.700,(2024,9):8.545,(2024,12):9.024,(2025,3):1.310,(2025,6):4.463,(2025,9):6.484,(2025,12):9.303,(2026,3):2.853,(2026,6):5.587,(2026,9):8.718}
def ytd(y,m):
 end=f'{y}-{m:02d}-'+('31' if m in (3,12) else '30');d={k:get(t,f'{y}-01-01',end) for k,t in T.items()};d['software']=software.get((y,m));return d
def sub(a,b):return {k:a[k]-b[k] if a[k] is not None and b[k] is not None else None for k in a}
def add(a,b):return {k:a[k]+b[k] if a[k] is not None and b[k] is not None else None for k in a}
def enrich(d):
 d['company_fcf']=d['cfo']-d['ppe']-d['software'];d['ebit_margin']=d['ebit']/d['revenue'];d['net_margin']=d['ni']/d['revenue'];d['fcf_after_sbc_check']=d['company_fcf']-d['sbc'];return d
history={f'FY{y}':enrich(ytd(y,12)) for y in (2023,2024,2025)}
for y,m in [(2025,9),(2025,12),(2026,3),(2026,6),(2026,9)]:
 q=ytd(y,m) if m==3 else sub(ytd(y,m),ytd(y,m-3));history[f'{y}Q{m//3}']=enrich(q)
for y in (2025,2026):history[f'TTM_{y}0930']=enrich(add(sub(ytd(y-1,12),ytd(y-1,9)),ytd(y,9)))
history['TTM_20260630']=enrich(add(sub(ytd(2025,12),ytd(2025,6)),ytd(2026,6)))
# Forward twelve-month base = latest TTM, not FY guidance treated as an actual.
BASE=history['TTM_20260930']['revenue'];M0=history['TTM_20260930']['ebit_margin'];SHARES=50.8;PRICE=160.42
LIQUID=1239.607+134.294+110.120;RESERVE=150.;NETCASH=LIQUID-RESERVE
RF=.0486;ERP=.0441;BETA=1.02;CAPM=RF+BETA*ERP
cases={
 'adverse':{'growth':[.08,.07,.06,.05,.04],'margins':[.09,.10,.11,.12,.13],'terminal_margin':.15,'g':.025,'roic':.15,'wacc':CAPM+.02,'da':.014,'ppe':.022,'software':.012,'acq':.005,'nwc_growth':0.},
 'central':{'growth':[.15,.15,.14,.12,.10],'margins':[.12,.14,.16,.18,.20],'terminal_margin':.22,'g':.03,'roic':.20,'wacc':CAPM,'da':.014,'ppe':.02,'software':.01,'acq':.005,'nwc_growth':-.10},
 'favorable':{'growth':[.22,.22,.20,.18,.16],'margins':[.14,.17,.20,.23,.25],'terminal_margin':.28,'g':.035,'roic':.25,'wacc':CAPM-.005,'da':.014,'ppe':.02,'software':.01,'acq':.005,'nwc_growth':-.15}}
def calc(c):
 rows=[];rev=BASE;pv=0
 for n in range(1,11):
  if n<=5:gr=c['growth'][n-1];margin=c['margins'][n-1]
  else:
   a=(n-5)/5;gr=c['growth'][-1]+a*(c['g']-c['growth'][-1]);margin=c['margins'][-1]+a*(c['terminal_margin']-c['margins'][-1])
  old=rev;rev*=1+gr;ebit=rev*margin;nopat=ebit*.76;da=rev*c['da'];ppe=rev*c['ppe'];sw=rev*c['software'];acq=rev*c['acq'];dnwc=(rev-old)*c['nwc_growth']
  raw_reinvest=ppe+sw+acq-da+dnwc
  # Fade explicit reinvestment to the sustainable g/ROIC framework, avoiding terminal cliff/free growth.
  target_reinvest=nopat*gr/c['roic'];a=max(0,(n-5)/5);reinvest=max(raw_reinvest,raw_reinvest*(1-a)+target_reinvest*a)
  fcff=nopat-reinvest;discounted=fcff/(1+c['wacc'])**n;pv+=discounted
  rows.append(dict(year=n,revenue=rev,growth=gr,margin=margin,ebit=ebit,nopat=nopat,da=da,ppe=ppe,software=sw,acquisitions=acq,delta_nwc=dnwc,raw_reinvestment=raw_reinvest,transition_reinvestment=reinvest,fcff=fcff,pv=discounted))
 terminal_nopat=rows[-1]['nopat']*(1+c['g']);terminal_growth_reinvestment=terminal_nopat*c['g']/c['roic'];terminal_rev=rev*(1+c['g']);terminal_physical_reinvestment=terminal_rev*(c['ppe']+c['software']+c['acq']-c['da'])+(terminal_rev-rev)*c['nwc_growth'];terminal_reinvestment=max(terminal_growth_reinvestment,terminal_physical_reinvestment);terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev=pv+pvtv
 return dict(value=(ev+NETCASH)/SHARES,enterprise_value=ev,netcash=NETCASH,shares=SHARES,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_growth_reinvestment=terminal_growth_reinvestment,terminal_physical_reinvestment=terminal_physical_reinvestment,terminal_fcff=terminal_fcff,rows=rows)
results={k:calc(v) for k,v in cases.items()}
sensitivity=[]
for w in [CAPM-.01,CAPM,CAPM+.01,CAPM+.02]:
 for g in [.02,.03,.04]:sensitivity.append({'wacc':w,'g':g,'value':calc({**cases['central'],'wacc':w,'g':g})['value']})
# Reverse with central growth, change entire EBIT trajectory proportionally; do not imply a unique expectation.
def reverse_growth_margin(growth):
 lo,hi=.2,4
 for _ in range(80):
  f=(lo+hi)/2;c={**cases['central'],'growth':growth,'margins':[x*f for x in cases['central']['margins']],'terminal_margin':cases['central']['terminal_margin']*f}
  if calc(c)['value']<PRICE:lo=f
  else:hi=f
 return {'growth_first5':growth,'margin_multiplier':f,'year1_margin':.12*f,'year5_margin':.20*f,'terminal_margin':.22*f,'value':calc(c)['value']}
reverse=[reverse_growth_margin(cases[k]['growth']) for k in cases]
# Audit exact accounting periods and FCFF mechanics.
assert abs(sum(history[q]['revenue'] for q in ['2025Q4','2026Q1','2026Q2','2026Q3'])-BASE)<1e-8
for k in ['revenue','ebit','ni','cfo','ppe','software','sbc']:
 assert abs(sum(history[q][k] for q in ['2025Q4','2026Q1','2026Q2','2026Q3'])-history['TTM_20260930'][k])<1e-8
for k,v in cases.items():
 assert v['wacc']>v['g'];assert results[k]['rows'][-1]['transition_reinvestment']+1e-8>=results[k]['rows'][-1]['nopat']*v['g']/v['roic'];assert all(row['transition_reinvestment']+1e-8>=row['raw_reinvestment'] for row in results[k]['rows']);assert results[k]['terminal_reinvestment']+1e-8>=results[k]['terminal_physical_reinvestment']
out={'asof':'2026-11-08','price':PRICE,'price_date':'2026-11-06 16:00 America/New_York','base_revenue':BASE,'capm':{'rf':RF,'beta':BETA,'erp':ERP,'wacc':CAPM,'debt_weight':0},'history':history,'cases':cases,'results':results,'sensitivity':sensitivity,'reverse':reverse,'scanner_mapping':{'raw_opm':.35875,'matching_20260630_net_margin':history['TTM_20260630']['net_margin'],'latest_operating_margin':history['TTM_20260930']['ebit_margin']}}
json.dump(out,open(P/'results.json','w'),indent=2);json.dump(provenance,open(P/'financial_input_provenance.json','w'),indent=2)
with open(P/'history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(history['FY2025']));w.writeheader();w.writerows({'period':p,**d} for p,d in history.items())
print(json.dumps({k:round(v['value'],2) for k,v in results.items()}));print(json.dumps(reverse,indent=2));print(json.dumps(history,indent=2))
# Additional transparent historical diagnostics. BS delta includes noncash/FX effects: not labeled cash-flow FCFF.
nwc_tags={'ar':('AccountsReceivableNetCurrent',1),'deferred_cost':('CapitalizedContractCostNetCurrent',1),'prepaid':('PrepaidExpenseAndOtherAssetsCurrent',1),'ap':('AccountsPayableCurrent',-1),'accrued':('AccruedLiabilitiesCurrent',-1),'deferred_revenue':('ContractWithCustomerLiabilityCurrent',-1)}
nwc={}
for end in ['2024-09-30','2025-09-30','2026-09-30']:
 d={k:get(tag,None,end)*sign for k,(tag,sign) in nwc_tags.items()};d['total']=sum(d.values());nwc[end]=d
out['historical_nwc']=nwc
for y in (2025,2026):
 h=history[f'TTM_{y}0930'];dn=nwc[f'{y}-09-30']['total']-nwc[f'{y-1}-09-30']['total'];h['balance_delta_nwc']=dn;h['normalized_fcff_bs_diagnostic']=h['ebit']*.76+h['da']-h['ppe']-h['software']-dn
# Exact nine-month cash-flow components from Q3 10-Q, note changes to prepaid/accrued include tax accounts.
wc9=17.362+20.771-3.525+.449+5.653+21.330+4.722
out['cash_bridge_9m2026']={'ni':103.783,'deferred_tax':23.727,'sbc':120.334,'da':12.718,'securities_accretion':-.983,'software_impairment':2.134,'working_capital_and_noncurrent':wc9,'cfo':328.475,'ppe':18.001,'software':8.718,'company_fcf':301.756,'normalized_ebit_tax_fcff_diagnostic':102.668*.76+12.718+wc9-18.001-8.718,'acquisition_cash':5.006}
assert abs(103.783+23.727+120.334+12.718-.983+2.134+wc9-328.475)<1e-8
out['multiples']={'market_cap_diluted':PRICE*SHARES,'ev_excess_cash':PRICE*SHARES-NETCASH,'ev_revenue':(PRICE*SHARES-NETCASH)/BASE,'ev_ebit':(PRICE*SHARES-NETCASH)/history['TTM_20260930']['ebit'],'company_fcf_yield':history['TTM_20260930']['company_fcf']/(PRICE*SHARES),'fcf_after_sbc_yield':history['TTM_20260930']['fcf_after_sbc_check']/(PRICE*SHARES)}
json.dump(out,open(P/'results.json','w'),indent=2);json.dump(provenance,open(P/'financial_input_provenance.json','w'),indent=2)

# Optional secondary-market EPS bridge. Q4 EPS absent from archived SEC quarter tags.
eps_quarters={'2024Q4':.28,'2025Q1':.72,'2025Q2':.91,'2025Q3':5.95,'2025Q4':.84,'2026Q1':.89,'2026Q2':.66,'2026Q3':.54}
out['eps_bridge_secondary']={'quarters':eps_quarters,'ttm_20250930_sum':sum(eps_quarters[q] for q in ['2024Q4','2025Q1','2025Q2','2025Q3']),'ttm_20260930_sum':sum(eps_quarters[q] for q in ['2025Q4','2026Q1','2026Q2','2026Q3']),'source':'Finviz and PromtFinance, archived eps_q4_secondary.json','caveat':'Sum of rounded quarterly per-share data. Q4 sourced from secondary providers; not issuer-published TTM EPS or annual-minus-nine-month EPS. Other providers show subtraction artifacts 0.31/0.94; those are not used.'}
json.dump(out,open(P/'results.json','w'),indent=2)
