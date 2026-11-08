"""Diagnostic only: finite Tucuma 2021 engineering schedule, NOT current project/equity NAV."""
import pathlib,json,csv,re
p=pathlib.Path(__file__).parent
a=json.loads((p/'tucuma_engineering_inputs.json').read_text())['table22_2']
labels=['Cu Payable','Ore Sent to Mill','Mine Operating Costs','Mill Processing','Mill Maintenance','Dry Stack Tailings','Operational Support','G&A','Haulage (plant to port)','Stuffing & port fees','Sea freight','TC & RC','Sustaining Capital']
rows=[];out={};params={'adverso':(4.5,1.55,1.40,.12),'central':(5.5,1.40,1.25,.10),'favorable':(6.5,1.25,1.15,.085)}
# Constant-dollar scenario treated as a real sensitivity, not calibrated 2026 purchasing power; taxes conservative 34% positive EBITDA, no fictional shield.
for case,(cu,opfactor,capfactor,r) in params.items():
 pv=0
 for year in range(2027,2037):
  i=year-2022;pay=a['Cu Payable'][i];rev=pay*cu
  costs=sum(a[k][i] for k in labels[2:12])*opfactor
  royalty=.02*rev
  # Preserve higher old sustaining years; floor scales physical throughput, not commodity revenue.
  cap=max(a['Sustaining Capital'][i]*capfactor,35*a['Ore Sent to Mill'][i]/4000)
  tax=max(0,rev-costs-royalty)*.34
  closure=24*capfactor if year==2036 else 0
  salvage=7 if year==2036 else 0
  cf=rev-costs-royalty-tax-cap-closure+salvage;disc=(1+r)**(year-2026);pv+=cf/disc
  rows.append(dict(case=case,year=year,payable_copper_mlb=pay,revenue=rev,cash_costs=costs,royalty=royalty,tax_no_shield=tax,capex=cap,closure=closure,salvage=salvage,fcf=cf,pv=cf/disc))
 out[case]={'copper_usd_lb':cu,'old_cost_multiplier':opfactor,'old_capex_multiplier':capfactor,'real_discount':r,'conditional_project_diagnostic_usdm':pv,'economic_ownership':.996,'conditional_attributable_subtotal':pv*.996}
(p/'finite_results.json').write_text(json.dumps({'scope':'Historical engineering schedule sensitivity, January 1 2027. NOT current Tucuma NAV or ERO fair value; old mine sequence conflicts with current guidance. No perpetual terminal.','approved_value':None,'approved_entry':None,'cases':out},indent=2));w=csv.DictWriter((p/'finite_schedule.csv').open('w'),fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(p/'tucuma_engineering_inputs.json').write_text(json.dumps({'years':list(range(2022,2037)),'table22_2':a},indent=2));print(json.dumps(out,indent=2))
