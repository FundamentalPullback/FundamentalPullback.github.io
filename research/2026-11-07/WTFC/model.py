import json,csv,pathlib,math
P=pathlib.Path(__file__).parent
j=lambda n,v:(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def csvout(n,rows):
 with (P/n).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# USD million except per-share; GAAP consolidated, calendar fiscal year.
annual=[]
for yr,rev,nii,ni,common,eps,shares,prov,assets,loans,dep,eq,sbc,cfo,ppe in [
(2023,2271.970,1837.864,622.626,594.662,9.58,62.087,114.390,56259.934,42131.831,45397.170,5399.526,33.5,744.376,46.406),
(2024,2450.860,1962.535,695.045,667.081,10.31,64.701,101.047,64879.668,48055.037,52512.349,6344.297,38.9,721.557,86.032),
(2025,2725.992,2224.052,823.844,774.154,11.40,67.894,95.553,71142.046,53105.101,57717.191,7258.715,42.0,910.348,49.951)]:
 annual.append(dict(period=str(yr),revenue=rev,net_interest_income=nii,net_income=ni,common_income=common,diluted_eps=eps,diluted_shares_m=shares,credit_provision=prov,assets=assets,loans=loans,deposits=dep,total_equity=eq,sbc=sbc,cfo=cfo,ppe=ppe,source='S2'))
q=[]
for per,rev,nii,ni,common,eps,shares,prov,nim in [('2025Q4',714.264,583.874,223.024,214.657,3.15,68.113,27.588,3.52),('2026Q1',713.166,579.024,227.388,219.021,3.22,68.097,29.594,3.54),('2026Q2',738.635,597.366,233.693,225.326,3.30,68.286,23.134,3.50),('2026Q3',757.877,621.604,239.054,230.687,3.37,68.378,25.879,3.49)]:
 q.append(dict(period=per,revenue=rev,net_interest_income=nii,net_income=ni,common_income=common,diluted_eps=eps,diluted_shares_m=shares,credit_provision=prov,gaap_nim_percent=nim,source='S1'))
ttm=[dict(period='TTM2025-09-30',revenue=2450.860+2011.728-1812.261,net_interest_income=1962.535+1640.178-1437.387,net_income=695.045+600.820-509.683,diluted_eps_sum=2.63+8.25,source='S2+S3'),dict(period='TTM2026-09-30',revenue=sum(x['revenue'] for x in q),net_interest_income=sum(x['net_interest_income'] for x in q),net_income=sum(x['net_income'] for x in q),diluted_eps_sum=sum(x['diluted_eps'] for x in q),source='S1')]
# TTM EPS is sum of disclosed quarterly EPS, not a reweighted annual denominator.
financials={'unit':'USD millions, except per share and ratios','annual':annual,'quarters':q,'ttm':ttm,'ttm_common_income':sum(x['common_income'] for x in q),'ttm_sbc':42+34.877-30.646,'ttm_cfo':910.348+1540.069-658.689,'ttm_ppe':49.951+58.667-26.921,'cashflow_not_bank_fcfe':True,'capital':{'date':'2026-09-30','common_equity':6864.546,'tangible_common_equity':5949.852,'preferred':425,'acquisition_intangibles':914.694,'common_shares_m':67.472459,'diluted_shares_q3_m':68.378,'book_per_share':101.74,'tbv_per_share':88.18,'aoci':-863.776,'aoci_june':-420.798,'cet1_ratio':.105,'tier1_ratio':.112,'total_capital_ratio':.125,'minimum_cet1_including_buffer':.07,'aoci_optout':True},'remittances_historical':{'date':'2025-12-31','subsidiary_dividends_2023_2024_2025':[360,475,600],'available_without_prior_approval':929.8,'parent_cash':281.521,'parent_interest_2025':41.911,'not_future_distributable_cash':True}}
j('financials.json',financials);csvout('historical_annual.csv',annual);csvout('historical_quarters.csv',q);csvout('historical_ttm.csv',ttm)
beta=.86;ke=.0529+beta*.0441
j('discount_evidence.json',{'observed_beta_5y_monthly':beta,'retrieved':'2026-11-08','source':'S6 Yahoo search-index observation; direct retrieval returned 429; regional Yahoo variant 0.89, window end not verified','paired_monthly':{'date':'2026-11-01','rf':.0529,'erp':.0441,'ke':ke},'mixed_daily_sensitivity':{'rf_date':'2026-11-06','rf':.0486,'erp_date':'2026-11-01','erp':.0441,'ke':.0486+beta*.0441},'approved_ke':None,'economic_ke_grid':[ke,.105,.12],'reason':'Observed CAPM is not a stress capital cost. Higher rates are explicit scenario assumptions, not reverse engineered to price.'})
# Residual income with clean-surplus assumption and equivalent DDM; not approved bank FCFE.
def ri(roe1,roet,ke,g=0.025,bgrowth=.05):
 b=101.74;value=b;pvdiv=0;rows=[]
 for t in range(1,6):
  roe=roe1+(roet-roe1)*(t-1)/4;eps=b*roe;retain=b*bgrowth;div=eps-retain;ri=(roe-ke)*b
  rows.append(dict(year=t,opening_book=b,roe=roe,eps=eps,retention=retain,hypothetical_distribution=div,residual_income=ri));value+=ri/(1+ke)**t;pvdiv+=div/(1+ke)**t;b+=retain
 terminal_ri=b*(roet-ke)/(ke-g);value+=terminal_ri/(1+ke)**5
 ddm=pvdiv+b*(roet-g)/(ke-g)/(1+ke)**5
 assert abs(value-ddm)<1e-8
 return dict(value=value,ddm_equivalent=ddm,rows=rows,terminal_ri_pv=terminal_ri/(1+ke)**5,terminal_roe=roet,ke=ke,g=g,book_growth=bgrowth)
scenarios={'adverso':ri(.10,.09,.12,.02,.03),'central':ri(.128,.12,.105),'favorable':ri(.14,.135,ke)}
# Diagnostic retained earnings are book growth, NOT validated RWA/CET1 requirement.
model={'ticker':'WTFC','status':'partial','method':'Residual income + clean-surplus DDM diagnostic','industrial_fcff_rejected':'Deposits and financial debt are operating funding; CFO minus PPE is not remittable common cash.','approved_values':{'bear':None,'base':None,'bull':None},'approved_entry':None,'scenarios_diagnostic_only':scenarios,'price':151.27,'price_date':'2026-11-06','starting_common_book':101.74,'no_price_calibration':True,'clean_surplus_warning':'Future AOCI, RWA migration, regulatory capital retention, bank-to-parent dividend constraints and share dilution not underwritten; no actionable valuation.'}
j('model.json',model)
sens=[dict(ke=k,terminal_roe=r,value=ri(.128,r,k)['value']) for k in [ke,.105,.12] for r in [.10,.12,.14]];csvout('diagnostic_sensitivity.csv',sens)
lo,hi=.01,.4
for _ in range(100):
 mid=(lo+hi)/2
 if ri(.128,mid,.105)['value']<151.27:lo=mid
 else:hi=mid
j('results.json',{'ticker':'WTFC','status':'partial','price':151.27,'price_date':'2026-11-06','opportunity':75,'stage3':'en_observacion_no_aprobada','approved_values':{'bear':None,'base':None,'bull':None},'entry':None,'diagnostic_values':{k:v['value'] for k,v in scenarios.items()},'implied_terminal_roe_diagnostic':mid,'implied_roe_backsolve_scope':'Year 1 ROE fixed at 12.8%; years 2-5 interpolate to the solved year-5/terminal ROE; Ke, book growth, terminal growth and opening book fixed.','pe_ttm':151.27/13.04,'price_book':151.27/101.74,'price_tbv':151.27/88.18,'ttm_growth':{k:ttm[1][k]/ttm[0][k]-1 for k in ['revenue','net_interest_income','net_income','diluted_eps_sum']}})
print(json.dumps(json.loads((P/'results.json').read_text()),indent=2))
