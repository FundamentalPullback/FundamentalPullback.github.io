"""Independent row-based repricing; no import or execution of production model."""
import json, math
from pathlib import Path
B=Path(__file__).resolve().parents[1]
L=json.loads((B/'legacy_inputs.json').read_text()); O=json.loads((B/'results.json').read_text()); checks=[]
def ck(label,a,b):
 assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7),(label,a,b)
 checks.append(label)
shares=592.5887; claims=16997-1076-125+409+750+6
E=68.60*590.5887; we=E/(E+16997)
rates={name:we*(.0498+.0441*beta)+(1-we)*.06*.77 for name,beta in [('observed_beta',.36),('normalized_beta',1)]}
ck('claims',claims,L['netclaims']);ck('equity weight',we,O['weights']['equity']);ck('debt weight',1-we,O['weights']['debt']);ck('market equity',E,O['market_equity'])
for k,v in rates.items():ck(k,v,O['rates'][k])
for path,data in L['results'].items():
 c=L['case_assumptions'][path]
 for row in data['rows']:
  ck(f'{path} NOPAT {row["year"]}',row['revenue']*row['margin']*(1-row['tax_rate']),row['NOPAT'])
  ck(f'{path} FCFF {row["year"]}',row['NOPAT']+row['DA']-row['cash_capex']-row['new_finance_leases']-row['delta_WC'],row['FCFF'])
 ck(path+' funded terminal',data['rows'][-1]['revenue']*(1+c['g'])*c['terminalmargin']*(1-c['tax'])*(1-c['g']/c['roic']),data['terminal_FCFF'])
def calc(path,r,capex=0,legal=0,t=0):
 c=L['case_assumptions'][path]; d=L['results'][path]; g=c['g']
 flows=[x['NOPAT']+x['DA']-x['cash_capex']-x['new_finance_leases']-x['delta_WC']-capex for x in d['rows']]
 terminal=d['rows'][-1]['revenue']*(1+g)*c['terminalmargin']*(1-c['tax'])*(1-g/c['roic'])-capex*(1+g)
 pvterminal=terminal/(r-g)/(1+r)**10
 ev=sum(f/(1+r)**(i+1) for i,f in enumerate(flows))+pvterminal
 lp=legal/(1+r)**t;eq=ev-claims-lp
 return dict(value=eq/shares,ev=ev,equity=eq,terminal_fcff=terminal,terminal_pv=pvterminal,terminal_fraction=pvterminal/ev,extra_claim_pv=lp,incremental_claim_capacity_at_quote=eq-68.60*shares)
case_args={'legacy_adverse':('bear',.09),'legacy_base':('base',.08),'legacy_favorable':('bull',.075),'base_observed':('base',rates['observed_beta']),'base_normalized':('base',rates['normalized_beta']),'base_hurdle9':('base',.09),'base_normalized_capex300':('base',rates['normalized_beta'],300),'base_observed_capex300':('base',rates['observed_beta'],300)}
values={}
for name,args in case_args.items():
 v=calc(*args);values[name]=v
 for k,x in v.items():ck(name+' '+k,x,O['cases'][name][k])
for name,path in [('legacy_adverse','bear'),('legacy_base','base'),('legacy_favorable','bull')]:ck(name+' original price',values[name]['value'],L['results'][path]['price'])
legal={}
for tag,r in [('observed',rates['observed_beta']),('normalized',rates['normalized_beta']),('old8',.08)]:
 for claim in [0,600,3000,9300]:legal[f'{tag}_claim{claim}']=calc('base',r,legal=claim)
legal['claim3000_year3']=calc('base',rates['normalized_beta'],legal=3000,t=3)
for name,v in legal.items():
 for k,x in v.items():ck(name+' '+k,x,O['legal_sensitivity'][name][k])
# Risk increments reduce equity linearly; discount-rate sensitivity is strictly decreasing here.
grid=[calc('base',.04+i*.0001)['value'] for i in range(1101)]
assert all(a>b for a,b in zip(grid,grid[1:]))
output=dict(status='PASS',comparisons=len(checks),cases=8,legal_sensitivity_count=13,original_tieouts=3,monotonic_rate_intervals=1100,rates=rates,weighted_recent_coupon=(650*.058+850*.062)/1500,market_equity=E,equity_weight=we,values=values,legal_sensitivities=legal,limitations=['Independent arithmetic audit of preserved assumptions, not certification of new earnings or balances.','Legal amounts are hypothetical present values; no probability or liability determination.'])
(B/'audit/output.json').write_text(json.dumps(output,indent=2));print(json.dumps({k:output[k] for k in ['status','comparisons','rates','weighted_recent_coupon']}))
