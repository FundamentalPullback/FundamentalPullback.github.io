"""BRO, 2026-11-07. Screen-grade deterministic FCFF research; not approval.
USD millions except per share. Run from any directory; no network dependencies.
"""
import json,csv,math,pathlib,copy
P=pathlib.Path(__file__).parent
PRICE=72.12
B={'debt_face':7822,'cash_reported':1099,'cash_surplus':0,'earnouts':326,'nci':18,'shares_cover':331.691829,'stock_comp_dilutive':1,'shares':332.691829,'fiduciary_cash_excluded':2442,'restricted_cash_excluded':271,'lease_liability_operating_not_deducted':336,'escrow_share_liability_not_deducted':270}
RF=.0484;ERP=.0441;BETA=.52;KD=.0555;TAX=.25
E=PRICE*B['shares_cover']; WD=B['debt_face']/(E+B['debt_face']);WACC=(RF+BETA*ERP)*(1-WD)+KD*(1-TAX)*WD
# No arbitrary risk premium. KD uses observed 2035 note coupon, not claimed market YTM.
H={
 'FY2023':dict(revenue=4257,fees=4199,investment=58,pretax=1146,interest=190,amortization=166,depreciation=40,net_income=871,eps=3.05,cfo=1010,capex=69,sbc=89,earnout_expense=21,disposal_loss=-143,escrow_gain=0,contingents=130),
 'FY2024':dict(revenue=4805,fees=4705,investment=100,pretax=1303,interest=193,amortization=178,depreciation=44,net_income=993,eps=3.46,cfo=1174,capex=82,sbc=101,earnout_expense=2,disposal_loss=-31,escrow_gain=0,contingents=166),
 'FY2025':dict(revenue=5902,fees=5763,investment=139,pretax=1371,interest=297,amortization=312,depreciation=55,net_income=1054,eps=3.16,cfo=1450,capex=68,sbc=93,earnout_expense=25,disposal_loss=2,escrow_gain=54,contingents=255),
 '9M2024':dict(revenue=3622,fees=3545,investment=77,pretax=1028,interest=147,amortization=131,depreciation=33,net_income=783,eps=2.73,cfo=813,capex=62,sbc=77,earnout_expense=-9,disposal_loss=-30,escrow_gain=0),
 '9M2025':dict(revenue=4295,fees=4183,investment=112,pretax=1050,interest=197,amortization=196,depreciation=37,net_income=790,eps=2.57,cfo=1006,capex=48,sbc=76,earnout_expense=18,disposal_loss=1,escrow_gain=-8,contingents=161),
 '9M2026':dict(revenue=5302,fees=5234,investment=68,pretax=1235,interest=299,amortization=337,depreciation=53,net_income=954,eps=2.57,cfo=1140,capex=77,sbc=72,earnout_expense=-7,disposal_loss=0,escrow_gain=83,contingents=262),
 'Q1_2026':dict(revenue=1901,fees=1880,investment=21,pretax=533,interest=99,amortization=116,depreciation=17,net_income=426,eps=1.06,cfo=262,capex=21,sbc=26,earnout_expense=5,disposal_loss=-1,escrow_gain=64,contingents=97),
 'Q2_2026':dict(revenue=1676,fees=1654,investment=22,pretax=383,interest=100,amortization=110,depreciation=18,net_income=288,eps=.84,cfo=346,capex=17,sbc=23,earnout_expense=-40,disposal_loss=1,escrow_gain=5,contingents=85),
 'Q3_2026':dict(revenue=1725,fees=1700,investment=25,pretax=320,interest=100,amortization=110,depreciation=18,net_income=240,eps=.67,cfo=532,capex=39,sbc=23,earnout_expense=27,disposal_loss=0,escrow_gain=14,contingents=80)}
def combine(a,b,c): return {k:a[k]+b[k]-c[k] for k in a if k in b and k in c}
H['TTM2026']=combine(H['FY2025'],H['9M2026'],H['9M2025']);H['TTM2025']=combine(H['FY2024'],H['9M2025'],H['9M2024'])
H['Q4_2025']={k:v-H['9M2025'][k] for k,v in H['FY2025'].items() if k in H['9M2025']};H['Q4_2025']['eps']=.59
for h in H.values():
 h['reported_ebit_including_other_income']=h['pretax']+h['interest'];h['reported_fcf']=h['cfo']-h['capex']
 h['economic_ebita_before_contingent_normalization']=h['pretax']+h['interest']-h['investment']-h['escrow_gain']+h['earnout_expense']+h['disposal_loss']+h['amortization']
 h['economic_margin_fees']=h['economic_ebita_before_contingent_normalization']/h['fees']
CORE=H['TTM2026']['fees']-H['TTM2026']['contingents']
C={
 'adverso':dict(organic=[-.02,0,.01,.02,.02],acq=.005,margin=[.28,.28,.285,.29,.29],contingent_share=.035,contingent_margin=.50,acq_price=6,g=.02,roic=.09,terminal_margin=.29),
 'central':dict(organic=[.02,.03,.035,.04,.04],acq=.01,margin=[.30,.303,.306,.309,.31],contingent_share=.04,contingent_margin=.60,acq_price=5.5,g=.025,roic=.12,terminal_margin=.31),
 'favorable':dict(organic=[.04,.05,.055,.06,.06],acq=.015,margin=[.31,.32,.325,.33,.33],contingent_share=.05,contingent_margin=.65,acq_price=5,g=.03,roic=.15,terminal_margin=.33)}
def value(c,wacc=WACC,g=None,shift=0,margin_shift=0,cash=0,shares=None):
 c=copy.deepcopy(c);g=c['g'] if g is None else g;assert wacc>g
 core=CORE;rows=[];last=None
 for y in range(1,11):
  f=max(0,(y-5)/5)
  organic=(c['organic'][min(y,5)-1]+shift)*(1-f)+g*f
  acquired=c['acq']*(1-f)
  margin=(c['margin'][min(y,5)-1]+margin_shift)*(1-f)+(c['terminal_margin']+margin_shift)*f
  prev=core;core=prev*(1+organic+acquired);cont=core*c['contingent_share']/(1-c['contingent_share']);rev=core+cont
  ebit=core*margin+cont*c['contingent_margin'];nopat=ebit*(1-TAX)
  dep=.01*rev;organic_wc=.15*max(0,prev*organic);acquisition=prev*acquired*c['acq_price'];organic_netcapex=.005*rev
  explicit_reinvest=organic_netcapex+organic_wc+acquisition
  stable_reinvest=nopat*g/c['roic']
  reinvest=(1-f)*(organic_netcapex+organic_wc)+acquisition+f*stable_reinvest
  # Smooth each component; at year10/terminal 80% net capex,20% NWC, no separate acquisition.
  netcapex=(1-f)*organic_netcapex+f*.8*stable_reinvest
  dwc=(1-f)*organic_wc+f*.2*stable_reinvest
  ma=acquisition
  capex=dep+netcapex;fcff=nopat+dep-capex-dwc-ma
  assert abs(fcff-(nopat-reinvest))<1e-8
  rows.append(dict(year=y,core=core,contingents=cont,revenue=rev,organic_growth=organic,acquired_growth=acquired,core_ebita_margin=margin,ebit_economic=ebit,tax=ebit*TAX,nopat=nopat,DA=dep,capex=capex,delta_wc=dwc,acquisition_reinvestment=ma,fcff=fcff,pv=fcff/(1+wacc)**y))
 r=rows[-1];rev11=r['revenue']*(1+g);n11=r['nopat']*(1+g);ri11=n11*g/c['roic'];d11=rev11*.01
 terminal=dict(revenue=rev11,nopat=n11,DA=d11,capex=d11+.8*ri11,delta_wc=.2*ri11,acquisition_reinvestment=0,fcff=n11-ri11,g=g,roic=c['roic'],reinvestment_rate=g/c['roic'])
 tv=terminal['fcff']/(wacc-g);pvtv=tv/(1+wacc)**10;ev=sum(r['pv'] for r in rows)+pvtv;equity=ev-B['debt_face']-B['earnouts']-B['nci']+cash
 return dict(price=equity/(shares or B['shares']),enterprise_value=ev,equity=equity,pv_explicit=sum(r['pv'] for r in rows),pv_terminal=pvtv,terminal_share=pvtv/ev,wacc=wacc,rows=rows,terminal=terminal)
def solve(param,target=PRICE):
 lo,hi=(-.08,.15) if param=='growth' else (-.15,.2)
 for _ in range(100):
  mid=(lo+hi)/2;v=value(C['central'],**({'shift':mid} if param=='growth' else {'margin_shift':mid}))['price']
  if v<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
R={'as_of':'2026-11-07','status':'screen-grade; not-decision-ready','bridge':B,'capital_cost':dict(rf=RF,rf_date='2026-11-05',erp=ERP,erp_date='2026-11-01',beta=BETA,kd=KD,kd_basis='2035 note coupon observed in Q3 filing; not current YTM',tax=TAX,equity_weight=1-WD,debt_weight=WD,ke=RF+BETA*ERP,wacc=WACC),'history':H,'cases':{k:value(v) for k,v in C.items()},'assumptions':C,'reverse':{'growth_parallel_shift':solve('growth'),'margin_parallel_shift':solve('margin')},'sensitivity':[dict(wacc=w,g=g,price=value(C['central'],wacc=w,g=g)['price']) for w in [WACC-.01,WACC-.005,WACC,WACC+.005,WACC+.01] for g in [.02,.025,.03]],'capital_sensitivity':{'all_cash_surplus':value(C['central'],cash=1099)['price'],'escrow_extra_4_4m_shares':value(C['central'],shares=B['shares']+4.4)['price']}}
R['checks']={'ten_years_each':all(len(v['rows'])==10 for v in R['cases'].values()),'fcff_component_identity':all(abs(x['fcff']-(x['nopat']+x['DA']-x['capex']-x['delta_wc']-x['acquisition_reinvestment']))<1e-8 for v in R['cases'].values() for x in v['rows']),'terminal_identity':all(abs(v['terminal']['fcff']-(v['terminal']['nopat']+v['terminal']['DA']-v['terminal']['capex']-v['terminal']['delta_wc']))<1e-8 for v in R['cases'].values()),'monotonic_scenarios':R['cases']['adverso']['price']<R['cases']['central']['price']<R['cases']['favorable']['price'],'four_quarter_revenue_sum':sum(H[k]['revenue'] for k in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])==H['TTM2026']['revenue'],'four_quarter_cfo_sum':sum(H[k]['cfo'] for k in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])==H['TTM2026']['cfo']}
# Independent audit diagnostics: do not replace unvalidated underwriting cases.
AUDIT_KD=.06183
AUDIT_WACC=(RF+BETA*ERP)*(1-WD)+AUDIT_KD*(1-TAX)*WD
R['audit_diagnostics']={'label':'Illustrative audit sensitivity; not revised base case',
 'issuer_curve_yield':{'kd':AUDIT_KD,'date':'2026-11-02','source':'https://www.aephel.com/research/bonds/US115236AM30','basis':'Delayed secondary curve-implied mark, not executable trade or current issuance quote','wacc':AUDIT_WACC,'case_prices':{k:value(v,wacc=AUDIT_WACC)['price'] for k,v in C.items()}},
 'producer_costs_9m2026':{'capitalized':30,'amortized':11,'net_capitalized':19,'basis':'Q3 10-Q Note 3; 15-year amortization. Not independently bridged to forecast working capital; no unsupported annualization.'},
 'earnout_tail':{'fair_value':326,'uncapped_fair_value':214,'capped_max_excluding_uncapped':369,'hypothetical_capped_max_increment':257,'central_price_if_capped_max_and_uncapped_fv':R['cases']['central']['price']-257/B['shares'],'basis':'369 minus (326 minus 214); diagnostic ignores timing and correlation, not expected liability.'}}
(P/'results.json').write_text(json.dumps(R,indent=2))
for k,v in R['cases'].items():
 with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=list(v['rows'][0]));w.writeheader();w.writerows(v['rows'])
(P/'run_log.json').write_text(json.dumps({'status':R['status'],'checks':R['checks'],'warnings':['Corporate free cash and insurance ring-fenced capital not fully disaggregated; all cash reserved, not claimed unavailable.','No current debt YTM; coupon proxy only.','Escrow inclusion in cover share count inferred, sensitivity supplied.','No pro forma TTM cash flow for full Accession perimeter.'],'publication':False},indent=2))
print(json.dumps({'prices':{k:v['price'] for k,v in R['cases'].items()},'wacc':WACC,'reverse':R['reverse'],'checks':R['checks'],'capital_sensitivity':R['capital_sensitivity']},indent=2))
