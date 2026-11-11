import sys,pathlib,json,copy,math
P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent))
import model
res={}; ref=55.32; shares=113.029173
for n,s in model.CASES.items():
 r=model.run(s)
 # Source-anchored favorable endpoint, NOT simultaneously validated economic claims.
 # Full cash credit, reported fair debt rather than principal, omit provisional derivatives, NCI book, actual legal shares.
 favorable=(r['ev']-2773-2-31+340)/shares
 # Stress entire other current liabilities as additional claim: conservative overlap deliberately retained; not estimate.
 extra415=(r['equity']-415)/model.SHARES
 res[n]={'unfloored_original':r['unfloored_equity_residual_per_share'],'all_favorable_claims_diagnostic':favorable,'extra_claim_20_incremental_sensitivity':-20/model.SHARES,'extra_claim_415_deliberate_overcount_sensitivity':extra415,'ev':r['ev']}
# Fixed bridge; finite cash-flow saving, not altering terminal maintenance.
b=model.run(model.CASES['bull']);base=model.run(model.CASES['base'])
for n,r in [('bull',b),('base',base)]:
 res[n]['annual_investment_saving_years1_5_to_reference']=(ref*model.SHARES-r['equity'])/sum(1/(1+r['inputs']['wacc'])**i for i in range(1,6))
# economic contrast: repeat verified model with lower WACC, higher ROIC, margin lift, or capex reduction; not verified ranges
sens=[]
for key,changes in [('bull_wacc8_5',{'wacc':.085}),('bull_wacc9_5',{'wacc':.095}),('bull_capex_minus25bp',{'capex':.0355}),('bull_margin_plus25bp',{'m5':.0525,'m10':.0575}),('base_capex_minus50bp',{'capex':.034})]:
 s=copy.copy(model.CASES['bull' if key.startswith('bull') else 'base']);s.update(changes);r=model.run(s)
 sens.append({'test':key,'assumption_changes':changes,'unfloored_residual_per_share':r['unfloored_equity_residual_per_share']})
out={'claim_tests':res,'operating_sensitivity_not_evidence_verified':sens,'reference':ref,'factoring_20_is_flow_not_ending_balance':True,'canonical_fair_value':None,'canonical_entry':None}
(P/'materiality.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
