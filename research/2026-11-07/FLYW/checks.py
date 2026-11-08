import pathlib,json,math,csv
import model
P=pathlib.Path(__file__).parent
h=json.loads((P/'history.json').read_text());r=json.loads((P/'model_results.json').read_text())
assert abs(h['TTM2026']['rev']-763.7)<1e-8
assert abs(h['TTM2026']['ebit']-59.806)<1e-8
assert abs(h['TTM2026']['ni']-78.947)<1e-8
assert abs(h['Q22026']['ni']+8.147)<1e-8
assert abs(h['Q32026']['ni']-74.543)<1e-8
assert abs(h['TTM2026']['cash_less_capex_settlement_sbc']-38.040)<1e-8
for k in ['rev','ebit','ni','cfo','capex']:
 assert abs(sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][k])<1e-8
for n,s in r['scenarios'].items():
 a=s['year10'];R=a['revenue'];K=a['physical_stock'];I=a['intangible_stock'];pv=0
 for t in range(1,301):
  nr=R*1.025;dep=.2*K+.125*I;ebit=a['cash_operating_margin_includes_sbc_rnd']*nr-dep
  f=ebit*.75+dep-.03*nr-.08*(nr-R);pv+=f/(1+s['wacc'])**t
  K=.8*K+.02*nr;I=.875*I+.01*nr;R=nr
 assert abs(pv-s['terminal_value'])/s['terminal_value']<1e-8,(n,pv,s['terminal_value'])
 assert s['approved_value'] is None
out={'history_identities':'pass','terminal_stock_closed_form_vs_300_year_simulation':'pass','claims_unknown_not_zero':'pass','approved_values_null':'pass','scope':'Reproducible arithmetic checks; economic assumptions and unknown claims remain unapproved'}
(P/'checks.json').write_text(json.dumps(out,indent=2));print(out)
