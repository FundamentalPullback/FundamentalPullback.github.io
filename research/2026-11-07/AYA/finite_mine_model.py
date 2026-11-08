"""Finite source reconstruction and conditional sensitivities, NOT approved equity fair value."""
from pathlib import Path
import json,csv
p=Path(__file__).parent
# Source: Boumadine 2026 PEA Table22-3, PDF page331/printed311. USD million.
years=list(range(-1,19));cf=[-162,-301,640,448,532,868,450,284,126,159,307,443,192,182,205,234,91,7,-4,-4]
rev=[0,0,1006,818,932,1301,866,833,568,611,864,1006,519,523,504,470,173,0,0,0]
cost=[0,0,259,302,332,346,346,353,340,340,354,308,229,232,218,182,64,0,0,0]
cap=[162,301,30,36,34,45,43,41,43,38,43,41,40,42,23,0,0,4,4,4]
roy=[0,0,30,25,28,39,26,25,17,18,26,30,16,16,15,14,5,0,0,0]
mt=[0,0,1,1,1,1,1,1,1,1,2,1,1,1,1,0,0,0,0,0]
fee=[0,0,28,23,26,36,24,23,16,17,24,28,14,14,14,13,5,0,0,0]
tax=[0,0,47,8,6,2,0,129,41,56,134,184,41,51,43,40,14,-11,0,0]
rows=[]
for i,y in enumerate(years):
 rebuilt=rev[i]-cost[i]-roy[i]-mt[i]-fee[i]-tax[i]-cap[i]
 rows.append(dict(year=y,revenue=rev[i],opex=cost[i],royalties=roy[i],mining_tax=mt[i],technical_fee=fee[i],income_tax_VAT=tax[i],capex=cap[i],reported_aftertax_cf=cf[i],rebuilt_aftertax_cf=rebuilt,residual=cf[i]-rebuilt,rebuilt_excluding_technical_fee_and_mining_tax=rebuilt+fee[i]+mt[i],residual_excluding_technical_fee_and_mining_tax=cf[i]-rebuilt-fee[i]-mt[i]))
with open(p/'boumadine_source_reconciliation.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def value(rate,delay=0,stress=0):
 # sensitivity takes stated aftertax CF, conservatively charges additional cost with no assumed tax shield.
 return sum((cf[i]-stress*(cost[i]+cap[i]))/(1+rate)**(max(0,y-.5)+delay) for i,y in enumerate(years))
# Zgounder: actual annual physical schedule, NOT smoothed Gordon perpetuity. 2027-2036 starts after2026.
zs=[6.2,6.3,6.4,6.3,6.4,6.2,6.1,6,5.9,4.0]
zops=[122.5,120.1,116.3,125.9,99.8,92.8,68.8,68.9,70.6,58.7]
zcap=[12.30,5.14,10.62,.68,.08,7.08,.24,3.08,2.04,2.04]
scenarios={};allrows=[]
for name,metal,r,costfactor,capfactor in [('prudente',35,.14,1.25,1.50),('central',45,.12,1.10,1.20),('favorable',55,.10,1,1)]:
 pv=0
 for i in range(10):
  # existing cost includes royalty at $28; incremental 3% royalty follows assumed metal price.
  royalty_extra=zs[i]*(metal-28)*.03;cashcost=zops[i]*costfactor+royalty_extra
  revenue=zs[i]*metal;tax=max(revenue-cashcost,0)*.35
  # no depletion tax shield assumed; no reserve expansion credits or exploration spend assumed to extend life.
  cashflow=revenue-cashcost-tax-zcap[i]*capfactor;discounted=cashflow/(1+r)**(i+.5);pv+=discounted
  allrows.append(dict(scenario=name,year=2027+i,silver_moz=zs[i],silver_price=metal,revenue=revenue,cash_cost=cashcost,cash_tax_no_depletion_shield=tax,sustaining_and_closure_capex=zcap[i]*capfactor,project_cashflow=cashflow,pv=discounted))
 scenarios[name]=dict(zgounder_conditional_project_value_at_2027_start=pv,discount_rate=r,silver_price=metal,no_terminal_value=True,no_equity_value=True,postclosure_monitoring_unquantified=True,constant_dollar_rate_sensitivity=True)
with open(p/'zgounder_finite_scenarios.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
b=dict(reported_npv5=3537,rounded_reported_cf_midyear_npv5=value(.05),reported_initial_capex_total_column=446,initial_capex_sum=sum(cap[:2]),reported_sustaining_total_column=340,sustaining_capex_sum=sum(cap[2:]),reported_total_capex=970,capex_sum=sum(cap),reported_aftertax_total=4694,aftertax_cf_sum=sum(cf),rebuilt_aftertax_cf_sum=sum(x['rebuilt_aftertax_cf'] for x in rows),residual_sum=sum(x['residual'] for x in rows),detailed_capital_table_initial=463,detailed_capital_table_sustaining=507,detailed_capital_table_total=970,annual_technical_fee_sum=sum(fee),annual_mining_tax_sum=sum(mt),residual_excluding_fee_and_mining_tax=sum(x['residual_excluding_technical_fee_and_mining_tax'] for x in rows),reported_mine_life_years=14.4,ownership=.85,sensitivity_only=[dict(rate=r,delay_years=d,cost_capex_stress=s,project_value_100pct=value(r,d,s),arithmetic_85pct=value(r,d,s)*.85) for r,d,s in [(.14,3,.3),(.12,2,.15),(.10,1,0)]],not_a_validated_dcf=True,not_equity_value=True)
r=dict(boumadine=b,zgounder=scenarios,total_company_value=None,per_share_value=None,approved_values=None,reason='Boumadine presentation totals and treatment of technical assistance/mining tax require reconciliation; detailed capital table supports463+507=970. This does not prove the source economic model erroneous. Financing/date/tax/offtake assumptions remain unverified. Zgounder sensitivities omit depletion shield, quantified postclosure monitoring and full corporate bridge.')
(p/'finite_model_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
