import json,pathlib
P=pathlib.Path(__file__).parent
price=266.7778; shares=(84493627+270170)/1e6
rf=.0486;erp=.0441;beta=.46;shrunk=2/3*beta+1/3
w=rf+shrunk*erp
# Post-quarter repayment and deferred receipt modeled together, no certified current cash.
bridge={'cash_sep':184.538,'oct_debt_repayment':-150,'oct_deferred_gold_receipt':46.1,'operating_reserve_assumed':50*-1,'nominal_debt_after_repayment':0,'investments_carrying_value':233.875,'artmin_loan':70,'minority_interest':-45.807,'mount_milligan_deferred_liability_after_receipt':-(69.211+46.1),'warintza_committed_payment':-50}
net=sum(bridge.values())
def calc(g=.02,metal=1.,margin=.65,wacc=w,roic=.12,terminalg=.02,replacement=.18):
 rev=464.766*4*metal;pv=0;rows=[]
 for t in range(1,11):
  growth=g if t<=5 else g+(terminalg-g)*(t-5)/5
  newrev=rev*(1+growth);nopat=newrev*margin*.78;dda=newrev*.18
  # depletion replacement plus paid net growth. Replacement proxy is uncertain, not DDA-certified asset budget.
  repl=newrev*replacement;growthcap=max(0,newrev-rev)*margin*.78/roic
  reinv=repl+growthcap;fcff=nopat+dda-reinv
  rows.append({'year':2026+t,'revenue':newrev,'nopat':nopat,'dda':dda,'replacement_capital':repl,'growth_capital':growthcap,'fcff':fcff});pv+=fcff/(1+wacc)**t;rev=newrev
 nopat=rev*(1+terminalg)*margin*.78;dda=rev*(1+terminalg)*.18;replacementcap=rev*(1+terminalg)*replacement;growthcap=nopat*terminalg/roic
 tf=nopat+dda-replacementcap-growthcap;tv=tf/(wacc-terminalg);pvt=tv/(1+wacc)**10
 return {'value':(pv+pvt+net)/shares,'terminal_ev_fraction':pvt/(pv+pvt),'rows':rows,'terminal_fcff':tf,'terminal_reinvestment_net':replacementcap+growthcap-dda,'terminal_roic_effective':nopat*terminalg/(replacementcap+growthcap-dda) if replacementcap+growthcap-dda>0 else None}
cases={'bear':calc(g=0,metal=.8,margin=.60,wacc=w+.01,roic=.10,terminalg=.01,replacement=.22),'central':calc(),'favorable':calc(g=.035,metal=1.1,margin=.67,wacc=rf+beta*erp,roic=.15,terminalg=.02,replacement=.18)}
lo=.5;hi=2
for _ in range(100):
 mid=(lo+hi)/2
 if calc(metal=mid)['value']<price:lo=mid
 else:hi=mid
out={'price_scanner_reference':price,'shares_proxy':shares,'capital_cost':{'rf':rf,'erp':erp,'published_beta':beta,'shrunk_beta':shrunk,'wacc_working':w,'raw_beta_wacc':rf+beta*erp},'bridge':bridge,'net_bridge':net,'cases':cases,'metal_price_factor_inverse':(lo+hi)/2,'wacc_sensitivity':{str(x):calc(wacc=x)['value'] for x in [.06,.07,.08,.09]},'replacement_sensitivity':{str(x):calc(replacement=x)['value'] for x in [.12,.15,.18,.22]},'no_investments_loan_value':cases['central']['value']-(233.875+70)/shares,'checks':{'ten_years':len(cases['central']['rows'])==10,'wacc_above_g':w>.02,'terminal_reinvestment_identity':abs(cases['central']['terminal_roic_effective']-.12)<1e-8,'scenario_order':cases['bear']['value']<cases['central']['value']<cases['favorable']['value']}}
P.joinpath('calculations.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(w,net,shares,out['metal_price_factor_inverse']);print(out['wacc_sensitivity'],out['replacement_sensitivity'])
