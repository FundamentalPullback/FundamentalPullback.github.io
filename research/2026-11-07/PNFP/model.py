import json
from pathlib import Path
p=Path(__file__).parent
price=100.64; book=91.52; tbv=61.86
rwa=10321/.1002 # estimate from rounded CET1 ratio, not reported exact RWA
rows=[]
for ke in [.0486+1.03*.0441,.10,.11,.12]:
 for g in [.02,.03,.04]:
  rows.append(dict(ke=ke,g=g,required_sustainable_ROE=g+price/book*(ke-g),method="Steady-state clean-surplus reverse RI; not fair value"))
capital=[]
for growth in [.06,.10,.12]:
 for target in [.1002,.1025,.105,.11]:
  required=rwa*(1+growth)*target-10321
  capital.append(dict(rwa_growth=growth,target_CET1=target,required_retention_m=required,earnings_common_runrate_m=1456,mechanical_residual_m=1456-required,warning="Not remittable FCFE: ignores AOCI shifts, deductions, conversion costs, subsidiary restrictions; no existing excess released"))
out=dict(price=price,book=book,tbv=tbv,price_to_book=price/book,price_to_tbv=price/tbv,estimated_rwa_m=rwa,reverse_RI=rows,capital_retention_diagnostics=capital,fair_value=None,standalone_dcf=None)
(p/"model.json").write_text(json.dumps(out,indent=2)+"\n")
assert all(r['required_sustainable_ROE']>r['ke'] for r in rows)
assert out['fair_value'] is None
print(json.dumps(out,indent=2))
