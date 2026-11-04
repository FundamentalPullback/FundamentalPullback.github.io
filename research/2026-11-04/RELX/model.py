"""RELX own research model. GBP millions; no entry approval. Python standard library."""
import json,csv,pathlib,copy
P=pathlib.Path(__file__).parent
FX=1.1179/.83358
START_REVENUE=9720; START_CASH_EBIT=3365
CAPITAL={'net_debt':8733,'pension_liabilities':149,'nci_book_proxy':17,'diluted_shares':1794.1,'balance_date':'2026-06-30','share_period':'H1 2026 weighted diluted'}
SCENARIOS={
'bear':{'growth':[.025,.03,.03,.025,.025],'margin':[.335,.335,.335,.335,.335],'tax':.25,'wacc':.095,'g':.02,'roic':.13,'terminal_roic':.13,'ordinary_da':.053,'capital_software_lease':.065,'prepublication':.012,'acquisitions':.022,'working_capital':.10},
'base':{'growth':[.055,.055,.05,.045,.04],'margin':[.35,.355,.36,.365,.365],'tax':.23,'wacc':.085,'g':.025,'roic':.18,'terminal_roic':.18,'ordinary_da':.053,'capital_software_lease':.062,'prepublication':.012,'acquisitions':.019,'working_capital':.08},
'bull':{'growth':[.075,.075,.07,.065,.055],'margin':[.36,.37,.38,.385,.39],'tax':.22,'wacc':.075,'g':.03,'roic':.23,'terminal_roic':.23,'ordinary_da':.053,'capital_software_lease':.06,'prepublication':.0115,'acquisitions':.018,'working_capital':.06}}
def calculate(s,fx=FX,extra_claims=0,shares=None,time_offset=0,extra_replacement=0):
 s=copy.deepcopy(s);r=START_REVENUE;prev=START_CASH_EBIT*(1-s['tax']);rows=[];ev=0
 for y in range(1,11):
  gr=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*(y-5)/5
  margin=s['margin'][y-1]if y<=5 else s['margin'][-1]
  prior=r;r*=1+gr;cash_ebit=r*margin;nopat=cash_ebit*(1-s['tax']);da=r*s['ordinary_da'];cap=r*s['capital_software_lease'];prepub=r*s['prepublication'];acq=r*s['acquisitions'];wc=(r-prior)*s['working_capital'];floor=cap+prepub+acq+wc-da
  growth_reinvest=max(0,nopat-prev)/s['roic']; reinvest=max(floor,growth_reinvest)+r*extra_replacement;fcff=nopat-reinvest;pv=fcff/(1+s['wacc'])**(y+time_offset);ev+=pv
  rows.append({'year':y,'growth':gr,'revenue':r,'cash_ebit_margin':margin,'cash_ebit_before_acquired_amortization':cash_ebit,'nopat':nopat,'ordinary_da':da,'ppe_software_lease_replacement':cap,'prepublication_cash':prepub,'acquisition_budget':acq,'incremental_working_capital':wc,'net_reinvestment_floor':floor,'positive_nopat_growth_reinvestment':growth_reinvest,'reinvestment':reinvest,'fcff':fcff,'pv':pv});prev=nopat
 terminal_revenue=r*(1+s['g']);terminal_nopat=nopat*(1+s['g']);terminal_floor=terminal_revenue*(s['capital_software_lease']+s['prepublication']+s['acquisitions']-s['ordinary_da'])+r*s['g']*s['working_capital'];terminal_reinvest=max(terminal_floor,terminal_nopat*s['g']/s['terminal_roic'])+terminal_revenue*extra_replacement
 terminal_fcff=terminal_nopat-terminal_reinvest;terminal_value=terminal_fcff/(s['wacc']-s['g']);pv_terminal=terminal_value/(1+s['wacc'])**(10+time_offset);ev+=pv_terminal;claims=CAPITAL['net_debt']+CAPITAL['pension_liabilities']+CAPITAL['nci_book_proxy']+extra_claims;denom=shares or CAPITAL['diluted_shares'];equity=ev-claims
 return {'assumptions':s,'rows':rows,'terminal_nopat':terminal_nopat,'terminal_reinvestment_floor':terminal_floor,'terminal_reinvestment':terminal_reinvest,'terminal_fcff':terminal_fcff,'terminal_value':terminal_value,'pv_terminal':pv_terminal,'terminal_weight':pv_terminal/ev,'enterprise_value':ev,'claims':claims,'equity_value':equity,'shares':denom,'gbp_per_share':equity/denom,'usd_per_adr':equity/denom*fx,'fx_usd_per_gbp':fx,'time_offset':time_offset}
def reconstruct_a111():
 r=9720;ev=0;rows=[]
 for y in range(1,11):
  g=[.06,.06,.055,.05,.045][y-1]if y<=5 else .045+(.025-.045)*(y-5)/5;m=[.323,.328,.333,.338,.34][y-1]if y<=5 else .34
  old=r;r*=1+g;n=r*m*.77;fc=n+r*.074-r*.081-(r-old)*.08;ev+=fc/1.08**y;rows.append(fc)
 tv=n*1.025*(1-.025/.15)/(.08-.025);ev+=tv/1.08**10
 return {'usd_per_adr':(ev-8899)/1794.1*1.332807,'published_rounded':29.59,'rows':rows,'note':'Reconstruction of published narrative, original executable not located. Rounds to published base; not proof of original file identity.'}
def main():
 out={'units':'GBP millions except per share; USD ADR conversion at ECB November3','capital':CAPITAL,'a111_reconstruction':reconstruct_a111(),'scenarios':{k:calculate(s)for k,s in SCENARIOS.items()}}
 out['sensitivity']=[{'wacc':w,'g':g,'value':calculate(dict(SCENARIOS['base'],wacc=w,g=g))['usd_per_adr']}for w in [.075,.08,.085,.09,.095]for g in [.02,.025,.03]]
 (P/'model_results.json').write_text(json.dumps(out,indent=2));rows=[dict(scenario=k,**r)for k,v in out['scenarios'].items()for r in v['rows']]
 with(P/'ten_year_model.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print({k:round(v['usd_per_adr'],2)for k,v in out['scenarios'].items()})
if __name__=='__main__':main()
