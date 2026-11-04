"""Offline exKOF EBIT/revenue/gross cash capex comparison. Source facts retained separately."""
import pathlib,json
P=pathlib.Path(__file__).parent;K={}
for x in json.loads((P/'kof_comparison_source_facts.json').read_text()):K.setdefault(x['period'],{})[x['metric']]=x['value']
for per,e in [('FY2024',40141),('FY2025',42937),('9M2024',28037),('9M2025',29234),('9M2026',31574)]:K[per]['ebit_management']=e
# EBIT sources: FEMSA IR FY2025 pp14/22, Q3FY2025 p20, Q3FY2026 p22 (KOF segment).
F=json.loads((P/'history_wide.json').read_text());out={}
for per,fy,now,old in [('TTM2025','FY2024','9M2025','9M2024'),('TTM2026','FY2025','9M2026','9M2025')]:
 kv={m:K[fy][m]+K[now][m]-K[old][m] for m in K[fy]};fv=F[per+'_BMV'];ex={m:fv[m]-kv[m] for m in kv};ex['cash_capex_ppe_intangibles']=ex['cash_ppe']+ex['cash_intangibles'];out[per]={'femsa_consolidated':{m:fv[m] for m in kv},'kof_standalone':kv,'ex_kof_subtraction_basis':ex,'note':'Gross cash investment before insurance and disposals; no leases. EBIT management matched basis. ExKOF includes consolidation/elimination residual.'}
out['growth']={m:out['TTM2026']['ex_kof_subtraction_basis'][m]/out['TTM2025']['ex_kof_subtraction_basis'][m]-1 for m in out['TTM2026']['ex_kof_subtraction_basis']}
(P/'ex_kof_operating_comparison.json').write_text(json.dumps(out,indent=2))
