"""CHKP public-source ten-year funded FCFF diagnostics. Conditional, not approved values."""
import json,csv,math
from pathlib import Path
P=Path(__file__).resolve().parent
# Primary annual 20-F, release quarter cash-flow presentation separately identified.
h={
 'FY2023':dict(revenue=2414.7,ebit=899.1,net=840.3,cfo=1037.9,sbc=145.3,capex=18.6,rd=368.9,da=47.4),
 'FY2024':dict(revenue=2565.,ebit=876.,net=845.7,cfo=1052.4,sbc=149.7,capex=24.2,rd=394.9,da=83.6),
 'FY2025':dict(revenue=2725.4,ebit=831.1,net=1056.9,cfo=1199.4,sbc=205.6,capex=26.6,rd=456.7,da=92.9)}
q=[dict(period='Q4_2025',revenue=744.9,ebit=232.9,net=304.5,cfo_release=310.4,sbc=56.4,capex=7.2,rd=124.3,da=17.8,grants=0.,diluted_average_shares=108.4),dict(period='Q1_2026',revenue=668.4,ebit=185.1,net=191.6,cfo_release=447.1,cfo_original_release=445.3,sbc=59.8,capex=9.4,rd=109.9,grants=27.,diluted_average_shares=106.1),dict(period='Q2_2026',revenue=673.6,ebit=185.1,net=193.8,cfo_release=169.6,sbc=55.9,capex=7.1,rd=112.,grants=28.,diluted_average_shares=103.5),dict(period='Q3_2026',revenue=669.8,ebit=177.2,net=185.2,cfo_release=264.3,sbc=54.8,capex=6.4,rd=122.1,grants=25.,diluted_average_shares=101.9)]
ttm26={k:sum(x[k] for x in q) for k in ['revenue','ebit','net','cfo_release','sbc','capex','rd','grants']};ttm26['da']=17.8+20.3+37.8;ttm26['capitalized_software']=3.6
# Comparable earnings-release quarters, never splice with annual audited CFO.
ttm25=dict(revenue=703.7+1980.5,ebit=254.3+598.2,net=257.5+752.4,cfo_release=249.+923.8,sbc=29.8+149.2,capex=6.5+19.4,rd=101.1+332.4,da=6.3+19.2+17.2+57.9,grants=0.,capitalized_software=0.)
price=144.17
basic_july=102.100634
awards_2025={'options':3.128875,'option_weighted_strike':139.35,'rsu_psu':3.054682}
# Explicit conservative stale-cohort proxy; not claimed current diluted shares.
shares=basic_july+awards_2025['rsu_psu']+awards_2025['options']*max(0,1-139.35/price)
cash=4122.9;reserve=500.;debt=2000.;legacy_tax_claim=391.6
bridge=cash-reserve-debt-legacy_tax_claim
spec={
 'adverso':dict(growth=[-.02,0,.01,.02,.02],margin=[.23,.225,.225,.23,.23],terminal_margin=.23,wacc=.095,g=.015,roic=.12,sales_capital=1.5,campus=100.),
 'central':dict(growth=[.025,.04,.05,.05,.04],margin=[.26,.27,.28,.285,.29],terminal_margin=.28,wacc=.085,g=.025,roic=.16,sales_capital=2.,campus=60.),
 'favorable':dict(growth=[.06,.08,.08,.07,.06],margin=[.29,.30,.31,.32,.33],terminal_margin=.32,wacc=.075,g=.03,roic=.20,sales_capital=2.5,campus=30.)}
def calc(s,write=False):
 rev=ttm26['revenue'];pv=0;rows=[];tax=.15;rr5=None
 for yr in range(1,11):
  if yr<=5:g=s['growth'][yr-1];m=s['margin'][yr-1]
  else:
   f=(yr-5)/5;g=s['growth'][-1]*(1-f)+s['g']*f;m=s['margin'][-1]*(1-f)+s['terminal_margin']*f
  old=rev;rev*=1+g;ebit=rev*m;nopat=ebit*(1-tax)
  da=rev*.027;maintenance_physical=rev*.012;software=rev*.002;intangible_replacement=rev*.014
  growth_capital=max(0,rev-old)/s['sales_capital'];nwc=max(0,rev-old)*.03
  raw_reinv=maintenance_physical+software+intangible_replacement+growth_capital+nwc-da
  if yr<=5:reinv=raw_reinv;rr5=reinv/nopat
  else:
   f=(yr-5)/5;reinv=nopat*(rr5*(1-f)+(s['g']/s['roic'])*f)
  reinv=max(raw_reinv,reinv) # Never let ROIC transition underfund explicit physical/growth components.
  supplemental_reinvestment=reinv-raw_reinv
  campus=s['campus'] if yr<=7 else 0.
  fcff=nopat-reinv-campus;disc=(1+s['wacc'])**yr;pv+=fcff/disc
  rows.append(dict(year=yr,revenue=rev,growth=g,ebit_margin=m,ebit=ebit,tax=tax,nopat=nopat,da=da,physical_replacement=maintenance_physical,software_capitalization=software,intangible_replacement=intangible_replacement,growth_capital=growth_capital,nwc_increase=nwc,raw_reinvestment=raw_reinv,funded_reinvestment_used=reinv,supplemental_reinvestment=supplemental_reinvestment,campus_capex=campus,fcff=fcff,pv_fcff=fcff/disc))
 r11=rev*(1+s['g']);n11=r11*s['terminal_margin']*(1-tax);terminal_physical_floor=r11*(.012+.002+.014-.027)+max(0,r11-rev)*(1/s['sales_capital']+.03);terminal_reinvest=max(terminal_physical_floor,n11*s['g']/s['roic']);fcff11=n11-terminal_reinvest;tv=fcff11/(s['wacc']-s['g']);pvtv=tv/(1+s['wacc'])**10;ev=pv+pvtv;equity=ev+bridge
 return dict(inputs=s,ev=ev,equity=equity,conditional_value_per_share=equity/shares,approved_value=None,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=n11,terminal_physical_floor=terminal_physical_floor,terminal_roic_effective=n11*s['g']/terminal_reinvest,terminal_reinvestment=terminal_reinvest,terminal_fcff=fcff11,rows=rows)
cases={k:calc(v) for k,v in spec.items()}
for k,c in cases.items():
 with (P/('forecast_'+k+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=list(c['rows'][0]));w.writeheader();w.writerows(c.pop('rows'))
lo,hi=-.05,.3
for _ in range(90):
 g=(lo+hi)/2;s=dict(spec['central']);s['growth']=[g]*5
 if calc(s)['conditional_value_per_share']<price:lo=g
 else:hi=g
sensitivity=[]
for w in [.075,.085,.095]:
 for g in [.015,.025,.03]:
  s=dict(spec['central'],wacc=w,g=g);sensitivity.append(dict(wacc=w,g=g,value=calc(s)['conditional_value_per_share']))
rf=.0486;erp=.0441;beta=.42;ke=rf+beta*erp
cap=price*basic_july;dw=debt/(cap+debt);new_kd=rf+.015 # analyst spread, NOT observed bond yield
wacc_mechanical=ke*(1-dw)+new_kd*(1-.15)*dw
r=dict(ticker='CHKP',as_of='2026-11-08',status='material_partial',stage3_complete=False,stage35_complete=False,entry_approved=False,approved_values=dict.fromkeys(cases),price=price,session='2026-11-06T16:00:00-05:00',method='10-year funded FCFF, USD nominal, end-year',historical_20f=h,quarters=q,ttm_release_basis={'2025':ttm25,'2026':ttm26},cfo_basis_bridge={'FY2025_release':1234.2,'marketable_security_amortization':-12.,'financing_fx':-22.8,'FY2025_20f':1199.4,'FY2024_release':1058.8,'marketable_security_amortization_2024':-6.4,'FY2024_20f':1052.4},normalization={'ttm_reported_ebit':ttm26['ebit'],'ttm_rd_grants':80.,'ttm_ex_grant_ebit':ttm26['ebit']-80.,'ttm_reported_margin':ttm26['ebit']/ttm26['revenue'],'ttm_ex_grant_margin':(ttm26['ebit']-80.)/ttm26['revenue'],'q3_ex_grant_ebit':177.2-25.,'ttm_cfo_release_less_capex_software_sbc':ttm26['cfo_release']-ttm26['capex']-3.6-ttm26['sbc'],'quarter_cfo_caveat':'Q1 original release 445.3 versus latest H1 616.7 minus Q2 169.6 = 447.1. Uses latest YTD-derived quarter; 1.8 revision/reclassification not explained in releases.', 'warning':'CFO diagnostic includes interest, cash timing and taxes; not FCFF. Grants legal program, not automatically one-time.'},equity_bridge={'cash_financial_assets_sep30':cash,'operating_reserve_analyst':reserve,'convert_principal':debt,'legacy_tax_claim_conservative':legacy_tax_claim,'net_adjustment':bridge,'leases_treated_operating_not_deducted_twice':True,'latest_exact_basic_found_july16':basic_july,'stale_dec2025_awards':awards_2025,'conditional_diluted_proxy':shares,'current_actual_diluted_unknown':True,'cap_call_value_added':0.,'new_buybacks_credited':False},cost_capital={'rf_nov6':rf,'erp_nov1':erp,'observed_beta_5y':beta,'mechanical_ke':ke,'debt_weight_proxy':dw,'new_debt_cost_proxy':new_kd,'spread_proxy_not_observed':.015,'mechanical_wacc':wacc_mechanical,'applied_wacc_scenarios':[.075,.085,.095],'israel_country_premium_january_context_only':.0207,'caveat':'Applied hurdle above low observed beta bridge; analyst judgment, not calibrated bottom-up cost. Zero coupon not zero economic funding cost. No mechanical full Israel CRP on all global sales.'},conditional_cases=cases,sensitivity=sensitivity,reverse_first_five_year_growth_other_central_inputs=(lo+hi)/2,share_sensitivity_base={str(n):(cases['central']['equity']/n) for n in [100,102,105.259924,108]},claim_sensitivity_base={'no_legacy_tax_deduction':(cases['central']['equity']+legacy_tax_claim)/shares,'no_reserve':(cases['central']['equity']+reserve)/shares},campus_sensitivity_per_extra_100m_total_pv=100/shares,blocked_approval=['Current point share/award rollforward not complete','Campus construction budget not disclosed; funded scenario range not evidence-calibrated','New margin/growth path and country-adjusted capital cost remain conditional','Margin recovery assumes operating leverage within stated expense ratios; economic support not complete'])
(P/'results.json').write_text(json.dumps(r,indent=2))
for name,data in [('historical',list(dict(period=k,**v) for k,v in h.items())),('quarters',q)]:
 fields=list(dict.fromkeys(k for row in data for k in row));f=(P/(name+'.csv')).open('w');w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data);f.close()
assert abs(ttm26['revenue']-(2725.4-1980.5+2011.8))<1e-8
assert abs(1234.2-12-22.8-1199.4)<1e-8
assert all(x['inputs']['wacc']>x['inputs']['g'] for x in cases.values())
assert all(x['terminal_reinvestment']>=x['terminal_physical_floor'] for x in cases.values())
for s in spec.values():
 z=calc(s);assert all(a['funded_reinvestment_used']+1e-9>=a['raw_reinvestment'] for a in z['rows'])
 assert abs(z['terminal_fcff']-z['rows'][-1]['fcff']*(1+s['g']))<1e-7
assert all(x['approved_value'] is None for x in cases.values())
(P/'self_check.json').write_text(json.dumps({'annual_cfo_bridge':True,'ttm_quarter_tie':True,'terminal_financed':True,'sbc_retained_in_ebit':True,'no_double_debt_convert':True,'approved_values_null':True,'independent_audit':False},indent=2))
print(json.dumps({k:{a:c[a] for a in ['conditional_value_per_share','terminal_weight','terminal_reinvestment']} for k,c in cases.items()},indent=2));print('reverse',r['reverse_first_five_year_growth_other_central_inputs'],'shares',shares,'wacc',wacc_mechanical)
