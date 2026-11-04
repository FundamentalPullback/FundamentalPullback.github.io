"""Own NTAP FCFF, USD millions. SBC and R&D remain operating costs; no capitalized-R&D uplift."""
import json,csv,copy,pathlib,datetime
P=pathlib.Path(__file__).parent
PRICE=190.78; SHARES=200.0
ASOF=datetime.date(2026,11,4); FY27END=datetime.date(2027,4,30)
STUB_YEARS=(FY27END-ASOF).days/365.25
CAPITAL={'July31_cash_and_short_investments':3576.,'July31_principal_debt':2500.,'DataPelago_contingent_claim':106.,'October_dividend_estimate':102.,'operating_cash_reserve_assumption':600.,'JetStream_and_PEAKAIO_combined_reserve_assumption':200.,'other_Aug1_Nov3_net_cash_less_debt_and_claims_movement_assumption':0.,'restricted_cash_excluded':6.,'April_historical_tax_claim_reserve':46.}
BASE={'fy27_revenue':8100.,'fy27_margin':.248,'extra_week_revenue':65.,'growth':[.10,.08,.07,.06,.05,.045,.04,.035,.03,.03],'margins':[.255,.26,.265,.265,.26,.259,.258,.257,.256,.255],'wacc':.112,'g':.025,'tax':.24,'roic':.25,'capex_ratio':.033,'da_ratio':.023,'wc_ratio':.03,'post_July_acquisition_reserve':200.,'capital_movement':0.,'historical_tax_claim_reserve':46.}
SCENARIOS={'bear':dict(BASE,fy27_revenue=7975.,fy27_margin=.243,growth=[-.05,.02,.03,.03,.03,.025,.025,.02,.02,.02],margins=[.21,.215,.22,.225,.23,.23,.23,.23,.23,.23],wacc=.125,g=.02,tax=.25,roic=.18,capex_ratio=.035,post_July_acquisition_reserve=500.,capital_movement=-250.),'base':BASE,'bull':dict(BASE,fy27_revenue=8225.,fy27_margin=.253,growth=[.15,.13,.11,.09,.08,.07,.06,.05,.04,.035],margins=[.27,.28,.285,.29,.29,.288,.286,.284,.282,.28],wacc=.10,g=.03,tax=.23,roic=.35,capex_ratio=.03,post_July_acquisition_reserve=100.,capital_movement=250.)}
def capital(s,reserve=600):
 c=CAPITAL
 cash=c['July31_cash_and_short_investments']-c['October_dividend_estimate']-s['post_July_acquisition_reserve']+s['capital_movement']
 return {'liquid_equivalent_for_bridge_not_cash_balance':cash,'operating_reserve':reserve,'financial_debt':2500.,'contingent_claim':106.,'historical_tax_claim_reserve':s['historical_tax_claim_reserve'],'net_equity_adjustment':cash-reserve-2500-106-s['historical_tax_claim_reserve'],'unknown_net_cash_minus_debt_and_claims_movement':s['capital_movement'],'unknown_post_July_acquisition_reserve':s['post_July_acquisition_reserve']}
def calculate(s,stub_scale=1.,reserve=600,margin_shift=0.,growth_shift=0.):
 s=copy.deepcopy(s);w=s['wacc'];g=s['g'];tax=s['tax'];roic=s['roic']
 assert w>g and roic>g
 # Stub is run-rate allocation, not an issuer six-month forecast. Additional week already elapsed.
 revenue=s['fy27_revenue']-s['extra_week_revenue'];prior=revenue;priornopat=revenue*s['fy27_margin']*(1-tax)
 # Stub uses annual physical net investment; no prior-quarter earnings counted again.
 stub_nopat=priornopat;stub_net=max(revenue*(s['capex_ratio']-s['da_ratio']),max(0,stub_nopat-1663*(1-tax))/roic)
 stub_fcff=(stub_nopat-stub_net)*STUB_YEARS*stub_scale
 stub={'days':(FY27END-ASOF).days,'years':STUB_YEARS,'annualized_revenue':revenue,'annualized_NOPAT':stub_nopat,'annualized_net_investment':stub_net,'FCFF':stub_fcff,'PV':stub_fcff/(1+w)**STUB_YEARS,'FY26_normalized_EBIT_anchor':1663.,'annual_growth_funding':'positive delta NOPAT FY27 normalized run rate versus FY26, divided by ROIC'}
 rows=[]
 for i in range(10):
  growth=s['growth'][i]+growth_shift;revenue=prior*(1+growth);margin=s['margins'][i]+margin_shift;ebit=revenue*margin;nopat=ebit*(1-tax);da=revenue*s['da_ratio'];physicalcapex=revenue*s['capex_ratio'];wc=max(0,(revenue-prior)*s['wc_ratio'])
  # Literal positive change in NOPAT funds both volume and margin improvements; no free margin uplift.
  growth_net=max(0,nopat-priornopat)/roic
  physicalnet=physicalcapex-da+wc
  additional=max(0,growth_net-physicalnet);capex=physicalcapex+additional
  fcff=nopat+da-capex-wc;t=STUB_YEARS+i+1
  rows.append({'year':i+1,'fiscal_label':2028+i,'discount_years':t,'revenue':revenue,'growth':growth,'EBIT_margin':margin,'EBIT':ebit,'NOPAT':nopat,'DA':da,'physical_capex':physicalcapex,'working_capital_investment':wc,'positive_delta_NOPAT_over_ROIC':growth_net,'additional_growth_capex':additional,'total_capex':capex,'FCFF':fcff,'PV':fcff/(1+w)**t});prior=revenue;priornopat=nopat
 last=rows[-1];tn=last['NOPAT']*(1+g);td=last['DA']*(1+g);tc=last['physical_capex']*(1+g);tw=last['revenue']*g*s['wc_ratio'];net=max(tn*g/roic,tc-td+tw);tfc=tn-net;tv=tfc/(w-g);pvt=tv/(1+w)**last['discount_years'];pv=sum(x['PV']for x in rows)+stub['PV'];ev=pv+pvt;bridge=capital(s,reserve)
 return {'assumptions':s,'stub':stub,'rows':rows,'terminal_NOPAT':tn,'terminal_net_reinvestment':net,'terminal_FCFF':tfc,'terminal_value':tv,'PV_terminal':pvt,'PV_explicit_including_stub':pv,'terminal_weight':pvt/ev,'EV':ev,'capital_bridge_scenario_not_measured':bridge,'equity':ev+bridge['net_equity_adjustment'],'shares_diluted_proxy':SHARES,'value':(ev+bridge['net_equity_adjustment'])/SHARES}
def main():
 ke=.0495+1.51*.0441;debtweight=2500/(PRICE*SHARES+2500);wacc=ke*(1-debtweight)+.058*(1-.24)*debtweight
 m={'valuation_date':str(ASOF),'price_date':'2026-11-03','price':PRICE,'units':'USD millions except per share','capital_inputs':CAPITAL,'wacc_inputs':{'rf':.0495,'ERP':.0441,'beta_provider':1.51,'Ke':ke,'Kd_assumed':.058,'debt_weight_market_proxy':debtweight,'computed_wacc':wacc,'selected_base_discount_rate':.112},'scenarios':{k:calculate(v)for k,v in SCENARIOS.items()}}
 (P/'model_results.json').write_text(json.dumps(m,indent=2))
 rows=[dict(scenario=k,**r)for k,v in m['scenarios'].items()for r in v['rows']]
 with open(P/'ten_year_model.csv','w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print({k:round(v['value'],4)for k,v in m['scenarios'].items()})
if __name__=='__main__':main()
