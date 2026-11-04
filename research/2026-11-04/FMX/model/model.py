import json,csv,math,copy
from pathlib import Path
P=Path(__file__).resolve().parent;I=json.load(open(P/'inputs.json'))
SC={
'bear':{'ex_kof':{'growth':[.04,.04,.04,.035,.035,.035,.035,.035,.035,.035],'margin':[.040,.039,.038,.037,.036,.036,.036,.036,.036,.036],'tax':.35,'roic':.13,'capex_ratio':.036,'wacc_usd':.13,'g':.035},'kof':{'growth':[.04]*10,'margin':[.14,.138,.136,.134,.132,.132,.132,.132,.132,.132],'tax':.32,'roic':.15,'capex_ratio':.07,'wacc_usd':.12,'g':.035}},
'base':{'ex_kof':{'growth':[.08,.07,.06,.06,.055,.05,.05,.05,.05,.05],'margin':[.042,.044,.046,.047,.048,.048,.048,.0475,.047,.047],'tax':.33,'roic':.18,'capex_ratio':.032,'wacc_usd':.11,'g':.045},'kof':{'growth':[.07,.07,.06,.06,.055,.05,.05,.05,.05,.05],'margin':[.146,.148,.15,.151,.152,.152,.151,.150,.149,.148],'tax':.30,'roic':.20,'capex_ratio':.065,'wacc_usd':.105,'g':.045}},
'bull':{'ex_kof':{'growth':[.10,.10,.09,.08,.07,.065,.06,.055,.055,.055],'margin':[.045,.049,.053,.056,.058,.058,.0575,.057,.056,.055],'tax':.31,'roic':.23,'capex_ratio':.030,'wacc_usd':.095,'g':.05},'kof':{'growth':[.09,.09,.08,.07,.065,.06,.055,.055,.055,.055],'margin':[.15,.154,.158,.160,.162,.162,.161,.160,.159,.158],'tax':.29,'roic':.24,'capex_ratio':.06,'wacc_usd':.095,'g':.05}}
}
# Shift all projected KOF margins by the explicitly estimated nonrecurring insurance contribution.
for _s in SC.values():
 _s['kof']['margin']=[m-I['anchors']['kof']['insurance_gain_adjustment_estimated']/I['anchors']['kof']['revenue'] for m in _s['kof']['margin']]
def segment(name,s,inp=I):
 a=inp['anchors'][name];rev=a['revenue'];nprev=a['economic_ebit_after_rent_estimated']*(1-s['tax']);w=(1+s['wacc_usd'])*(1+inp['rates']['annual_mxn_depreciation_assumed'])-1;rows=[]
 da_ratio=a['physical_da_ratio'];stub_days=58;stub_fraction=stub_days/365
 # TTM maintenance floor only for short pre-2027 stub, no forecast seasonal release.
 stub_cf=(nprev-max(0,a['capex_cash']-rev*da_ratio))*stub_fraction
 pv=stub_cf/(1+w)**(stub_fraction/2)
 for t,(g,margin) in enumerate(zip(s['growth'],s['margin']),1):
  prevrev=rev;rev*=1+g;ebit=rev*margin;n=ebit*(1-s['tax']);da=rev*da_ratio;physical=max(0,rev*s['capex_ratio']-da);wc=max(0,rev-prevrev)*.02;ri=max(0,n-nprev)/s['roic'];reinvest=max(ri,physical+wc);fcf=n-reinvest;dt=t+stub_fraction;v=fcf/(1+w)**dt;pv+=v;rows.append({'year':2026+t,'revenue':rev,'growth':g,'ebit_after_rent':ebit,'margin':margin,'tax_rate':s['tax'],'nopat':n,'physical_da':da,'gross_physical_capex_floor':rev*s['capex_ratio'],'net_physical_reinvestment_floor':physical,'working_capital_floor':wc,'positive_delta_nopat_roic_reinvestment':ri,'net_reinvestment_selected':reinvest,'fcff':fcf,'discount_years':dt,'pv_fcff':v});nprev=n
 g=s['g'];rt=rev*(1+g);nt=rt*s['margin'][-1]*(1-s['tax']);rit=nt*g/s['roic'];pt=max(0,rt*(s['capex_ratio']-da_ratio));wt=(rt-rev)*.02;reinv=max(rit,pt+wt);ft=nt-reinv;tv=ft/(w-g);pvt=tv/(1+w)**(10+stub_fraction)
 return {'rows':rows,'wacc_mxn':w,'g_mxn':g,'g_usd_equivalent':(1+g)/(1+inp['rates']['annual_mxn_depreciation_assumed'])-1,'stub_days':stub_days,'stub_fcff_estimated':stub_cf,'stub_pv':stub_cf/(1+w)**(stub_fraction/2),'pv_cashflows_including_stub':pv,'terminal_nopat':nt,'terminal_reinvestment':reinv,'terminal_fcff':ft,'terminal_value':tv,'pv_terminal':pvt,'enterprise_value':pv+pvt,'terminal_share':pvt/(pv+pvt)}
def value(sc,inp=I):
 c=inp['capital'];x=segment('ex_kof',sc['ex_kof'],inp);k=segment('kof',sc['kof'],inp)
 xb=c['ex_kof_cash']+c['ex_kof_investments']-c['ex_kof_financial_debt_estimated']-c['spin_customer_reserve']-c['operating_cash_reserve']-c['pension_reserve']-c['other_claims_reserve']-c['ex_kof_nci_reserve']+c['known_post_september_ex_kof_dividends_estimated']+c['unknown_post_september_net_capital_change']
 kb=c['kof_cash']-c['kof_financial_debt']-c['kof_derivative_reserve']-c['kof_nci_reserve']-c['kof_operating_cash_reserve']-c['kof_pension_reserve']+c['known_post_september_kof_dividend'];ke=k['enterprise_value']+kb;xe=x['enterprise_value']+xb;eq=xe+ke*inp['kof_fraction']+c['imperial_brady_value_in_main'];den=inp['fx']*inp['ads_m'];marked=xe+inp['kof_price']*inp['kof_ads_m']*inp['fx']*inp['kof_fraction']+c['imperial_brady_value_in_main']
 return {'ex_kof':x,'kof':k,'ex_kof_capital_bridge':xb,'kof_capital_bridge':kb,'ex_kof_equity_identified':xe,'kof_equity_common':ke,'kof_standalone_value_per_ads_usd':ke/inp['fx']/inp['kof_ads_m'],'femsa_owned_kof_value':ke*inp['kof_fraction'],'identified_equity_value':eq,'partial_value_per_fmx_ads_usd':eq/den,'nominal_equal_shares_sensitivity':eq/inp['fx']/inp['ads_nominal_m'],'hybrid_kof_market_mark_usd_per_fmx_ads':marked/den,'upside_vs_price_not_recommendation':eq/den/inp['price']-1,'excluded_imperial_value':True}
def write():
 out={s:value(v) for s,v in SC.items()};(P/'scenarios.json').write_text(json.dumps(SC,indent=2)+'\n');(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for n,z in out.items():
  for seg in ['ex_kof','kof']:
   rows=z[seg]['rows'];f=open(P/f'{n}_{seg}_10years.csv','w');w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);f.close()
 print({s:round(z['partial_value_per_fmx_ads_usd'],4) for s,z in out.items()})
if __name__=='__main__':write()
