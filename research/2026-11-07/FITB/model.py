"""USD millones. RI/FCFE bancario condicional, no FCFF ni objetivo aprobado."""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
K=['nii_gaap','fees','provision','opex','net_income','common_income','cfo','sbc']
raw={'FY2023':[5827,2881,515,5205,2349,2212,4509,169],'FY2024':[5630,2849,530,5033,2314,2155,2824,164],'FY2025':[5982,3035,662,5144,2522,2376,4514,163],'9M2024':[4192,2117,351,3807,1694,1573,2925,133],'9M2025':[4453,2224,544,3835,1791,1677,3585,135],'9M2026':[6420,2962,479,6553,1832,1719,2525,226],'Q1_2026':[1934,895,227,2395,165,128,-1106,145],'Q2_2026':[2215,1059,129,2109,801,763,2796,43],'Q3_2026':[2271,1008,122,2049,866,828,835,38]}
h={p:dict(zip(K,v)) for p,v in raw.items()}
def diff(a,b):return {k:h[a][k]-h[b][k] if h[a][k] is not None and h[b][k] is not None else None for k in K}
h['Q4_2025']=diff('FY2025','9M2025')
for y in [2025,2026]:
 h['TTM_Sep'+str(y)]={k:h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] if all(h[p][k] is not None for p in ['FY'+str(y-1),'9M'+str(y),'9M'+str(y-1)]) else None for k in K}
for x in h.values():x['revenue_gaap']=x['nii_gaap']+x['fees'];x['ppnr_gaap']=x['revenue_gaap']-x['opex']
# Final 10-Q supersedes preliminary release. End-Sep book, current diluted-share proxy.
book=33296-2182; cet1=25001; rwa=249257; shares=917.102971; price=53.04
# No AOCI addback; no debt/cash enterprise bridge. All earnings after preferred dividends and SBC.
def case(roe,ke,growth,terminal_roe,gt=.025,target=.105,initial_loss=0,credit_loss_year1=0):
 b=book-initial_loss;c=cet1-initial_loss; r=rwa; pv=0; pvri=0; rows=[]; b0=b
 for t in range(1,11):
  g=growth if t<=5 else growth+(gt-growth)*(t-5)/5
  rt=roe if t<=5 else roe+(terminal_roe-roe)*(t-5)/5
  earn=rt*b-(credit_loss_year1 if t==1 else 0)
  rn=r*(1+g); need=max(g*b,target*rn-c,0)
  dist=max(0,earn-need);ret=earn-dist
  bn=b+ret;cn=c+ret
  ri=earn-ke*b
  pv+=dist/(1+ke)**t;pvri+=ri/(1+ke)**t
  rows.append(dict(year=t,roe=rt,rwa_growth=g,opening_common_equity=b,common_earnings=earn,retained=ret,fcfe_distributable=dist,approved_distribution=None,distribution_requires_remittance_validation=True,closing_common_equity=bn,cet1=cn,rwa=rn,cet1_ratio=cn/rn,residual_income=ri,target_shortfall=max(0,target*rn-cn)))
  b,c,r=bn,cn,rn
 # terminal retains gt*book, enough for unchanged CET1/rwa under equal growth
 tv=b*(terminal_roe-gt)/(ke-gt);tvr=b*(terminal_roe-ke)/(ke-gt)
 value=pv+tv/(1+ke)**10; rivalue=b0+pvri+tvr/(1+ke)**10
 assert abs(value-rivalue)<1e-7
 assert all(x['fcfe_distributable']>=0 for x in rows)
 return dict(price=value/shares,roe=roe,ke=ke,growth=growth,terminal_roe=terminal_roe,terminal_growth=gt,target_cet1=target,initial_loss=initial_loss,credit_loss_year1=credit_loss_year1,terminal_share=tv/(1+ke)**10/value,ri_fcfe_tieout=value-rivalue,terminal_distribution=b*(terminal_roe-gt),terminal_retention=b*gt,terminal_cet1_ratio=c/r,approved_value=None,rows=rows)
cases={'prudente':case(.095,.1175,.02,.095,gt=.02,target=.11,initial_loss=1039*.78+76,credit_loss_year1=180272*.01*.78),'intermedio':case(.12,.1075,.04,.115),'expansivo':case(.14,.0975,.05,.13)}
lo,hi=.01,.4
for _ in range(100):
 m=(lo+hi)/2;x=case(m,.1075,.04,m)
 if x['price']<price:lo=m
 else:hi=m
inverse=case((lo+hi)/2,.1075,.04,(lo+hi)/2)
# Q3 normalized run-rate is a bridge, not four actual quarters.
runrate=828*4+171*4+14*4-57*4*.78-(.005-.0031)*179244*.78-20*4*.78
res=dict(as_of='2026-11-08',method='RI y FCFE bancario: sensibilidad condicional de perímetro combinado, no valoración aprobada',approved_values=None,approved_price=None,entry_approved=False,history=h,quote={'price':price,'date':'2026-11-06','session':'NYSE regular close 16:00 EST','quality':'secundaria corroborada; interfaz IR sin cierre recuperable','scanner_last':53.45,'scanner_date':'2026-11-05'},capital={'common_equity':book,'tangible_common_equity':19940,'aoci':-4938,'cet1':cet1,'rwa':rwa,'cet1_ratio':cet1/rwa,'scb':.032,'buffered_minimum':.077,'proposed_rules_estimate':.092,'shares_diluted_proxy':shares,'shares_basic_oct31':903.645765,'htm_unrecognized_loss_pretax':1039},normalization={'q3_common_annualized':828*4,'remove_merger_aftertax_annualized':171*4,'remove_tech_impairment_annualized':14*4,'retain_interchange_legal_costs':True,'remove_purchase_accretion_pretax_annualized':57*4,'raise_credit_cost_to_50bp_from_31bp':(.005-.0031)*179244,'remove_pension_benefit_pretax_annualized':80,'illustrative_common_income':runrate,'illustrative_roe':runrate/book,'caution':'no forecast; merger expense relief annualized mechanically, no added synergies; credit/PPA/pension adjustments explicit'},cost_of_equity={'rf_10y_2026_11_06':.0486,'erp_2026_11_01':.0441,'erp_source_riskfree':.0529,'parameter_dates_not_matched':True,'beta_assumed':1.2,'calculated_ke':.0486+1.2*.0441,'scenario_ke':[.0975,.1075,.1175],'beta_not_regression_estimate':True},conditional_cases=cases,inverse_constant_roe=inverse,pro_forma={'source':'10-Q Note 4, unaudited no synergies','Q3_2026':{'nii':2254,'fees':1018,'common_income':991},'Q3_2025':{'nii':2136,'fees':1058,'common_income':769},'9M2026':{'nii':6590,'fees':3084,'common_income':2656},'9M2025':{'nii':6310,'fees':3021,'common_income':1275}},quality_flags=['TTM reported mixes legacy Q4 and 8 months Comerica; not combined pro forma TTM','Q1+Q2+Q3 provision 478 vs 9M479: reported rounding difference retained','CFO not shareholder FCFE','No recurring SBC addback','Forward OCI held constant; model capital simplification not regulatory approval','Bank-specific remittance capacity amount unverified; 24 month parent liquidity is not payout authorization','Conference Nov6 held; no primary slides/text recovered yet; current market quote not primary-certified'])
(P/'results.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values())).keys()));w.writeheader();w.writerows({'period':p,**v} for p,v in h.items())
print(json.dumps({'cases':{k:v['price'] for k,v in cases.items()},'inverse_roe':inverse['roe'],'runrate_roe':runrate/book,'ttms':{k:v for k,v in h.items() if k.startswith('TTM')}},indent=2))
