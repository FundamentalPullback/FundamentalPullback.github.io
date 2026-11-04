"""RHI own cyclical FCFF, USD millions. Pre-unquantified litigation; no entry approval."""
import pathlib,json,csv,copy
P=pathlib.Path(__file__).parent
PRICE=43.73;SHARES=102.351225;CASH=321.291;CASH_RESERVE=150.0;DEBT=0
# FY2026 projection = reported9M + nominal midpoint Q4 guidance. Not a reported FY.
REVENUE=3995.841+1335;NORMAL_EBIT=139.815+1335*.04
BASE={'growth':[.05,.05,.04,.035,.03],'margin':[.05,.06,.065,.07,.07],'terminal_margin':.065,'tax':.33,'wacc':.105,'g':.025,'roic':.18,'terminal_roic':.15,'da':.013,'ppe_cloud_capex':.014,'acquisition_budget':.002,'wc':.15}
SCENARIOS={'bear':{'growth':[0,.02,.02,.02,.02],'margin':[.03,.035,.04,.04,.04],'terminal_margin':.035,'tax':.35,'wacc':.115,'g':.02,'roic':.12,'terminal_roic':.12,'da':.013,'ppe_cloud_capex':.015,'acquisition_budget':.002,'wc':.18},'base':BASE,'bull':{'growth':[.08,.08,.07,.06,.05],'margin':[.06,.075,.085,.09,.09],'terminal_margin':.085,'tax':.30,'wacc':.095,'g':.03,'roic':.23,'terminal_roic':.20,'da':.013,'ppe_cloud_capex':.014,'acquisition_budget':.002,'wc':.13}}
# Guidance-bound Q4 operating stub excludes unproven seasonal WC release.
STUB={'q4_revenue':1335,'margin':.04,'tax':.32,'da':(5298.220*.013)/4,'ppe_cloud_capex':17.5,'incremental_wc':5.0,'remaining_fraction':57/92,'discount_years':57/365}
def calculate(s,claims=0,reserve=CASH_RESERVE,shares=SHARES,charge_margin_growth=False,include_stub=True,time_offset=57/365,margin_cost=0):
 s=copy.deepcopy(s);r=REVENUE;previous_nopat=NORMAL_EBIT*(1-s['tax']);rows=[];ev=0
 for y in range(1,11):
  g=s['growth'][y-1]if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*(y-5)/5
  margin=s['margin'][y-1]if y<=5 else s['margin'][-1]+(s['terminal_margin']-s['margin'][-1])*(y-5)/5
  old=r;r*=1+g;ebit=r*(margin-margin_cost);nopat=ebit*(1-s['tax']);da=r*s['da'];cap=r*s['ppe_cloud_capex'];acq=r*s['acquisition_budget'];wc=max(0,r-old)*s['wc'];floor=max(0,cap+acq+wc-da)
  growth_charge=max(0,nopat-previous_nopat)/s['roic']if charge_margin_growth else nopat*max(0,g)/s['roic']
  reinvest=max(floor,growth_charge);fcff=nopat-reinvest;pv=fcff/(1+s['wacc'])**(y+time_offset);ev+=pv
  rows.append({'year':2026+y,'revenue':r,'growth':g,'normalized_ebit_margin':margin-margin_cost,'normalized_ebit':ebit,'nopat':nopat,'ordinary_da':da,'ppe_cloud_capex':cap,'acquisition_budget':acq,'working_capital':wc,'net_reinvestment_floor':floor,'economic_growth_reinvestment':growth_charge,'reinvestment':reinvest,'fcff':fcff,'pv':pv});previous_nopat=nopat
 tr=r*(1+s['g']);tn=tr*(s['terminal_margin']-margin_cost)*(1-s['tax']);tf=max(0,tr*(s['ppe_cloud_capex']+s['acquisition_budget']-s['da'])+r*s['g']*s['wc']);tre=max(tf,tn*s['g']/s['terminal_roic']);tfc=tn-tre;tv=tfc/(s['wacc']-s['g']);pt=tv/(1+s['wacc'])**(10+time_offset);ev+=pt
 stub_full=STUB['q4_revenue']*STUB['margin']*(1-STUB['tax'])+STUB['da']-STUB['ppe_cloud_capex']-STUB['incremental_wc'];stub_value=stub_full*STUB['remaining_fraction']/(1+s['wacc'])**STUB['discount_years']if include_stub else 0;ev+=stub_value
 excess_cash=max(0,CASH-reserve);eq=ev+excess_cash-DEBT-claims
 return {'assumptions':s,'rows':rows,'terminal_nopat':tn,'terminal_reinvestment_floor':tf,'terminal_reinvestment':tre,'terminal_fcff':tfc,'terminal_value':tv,'pv_terminal':pt,'terminal_share_of_ev':pt/ev,'stub_full_q4_proxy':stub_full,'stub_pv':stub_value,'enterprise_value':ev,'corporate_cash':CASH,'operating_cash_reserve':reserve,'excess_cash':excess_cash,'financial_debt':DEBT,'additional_claims_stress_not_estimated_legal_liability':claims,'equity_value_before_unquantified_contingency':eq,'shares':shares,'value':eq/shares,'charge_margin_growth':charge_margin_growth,'time_offset':time_offset}
def main():
 out={'valuation_date':'2026-11-04 valuation date; price reference close2026-11-03; balance2026-09-30','units':'USD millions; shares millions','fy2026_projected_revenue':REVENUE,'fy2026_projected_normalized_ebit':NORMAL_EBIT,'stub_assumptions':STUB,'scenarios':{k:calculate(v)for k,v in SCENARIOS.items()},'sensitivity':[{'wacc':w,'g':g,'value':calculate(dict(BASE,wacc=w,g=g))['value']}for w in [.085,.095,.105,.115,.125]for g in [.02,.025,.03]]}
 (P/'model_results.json').write_text(json.dumps(out,indent=2));rows=[dict(scenario=k,**r)for k,v in out['scenarios'].items()for r in v['rows']]
 with(P/'ten_year_model.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print({k:round(v['value'],2)for k,v in out['scenarios'].items()})
if __name__=='__main__':main()
