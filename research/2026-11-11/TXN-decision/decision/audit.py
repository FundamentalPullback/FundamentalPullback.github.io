"""Independent, self-contained arithmetic/prose QA; no production import or private inputs."""
from decimal import Decimal as D
from pathlib import Path
import json, hashlib
p=Path(__file__).resolve().parent
r=json.loads((p/'results.json').read_text()); checks=[]
def ck(name,got,want):
    ok=abs(D(str(got))-D(str(want)))<D('0.00000001')
    checks.append({'name':name,'pass':ok}); assert ok,name
price=D('300.52'); shares=D('921')
coupon=sum(D('500')*D(x) for x in ['.05','.0535','.055','.0575'])
for k,v in {'price':price,'old_share_proxy_m':shares,'new_notes_face_m':2000,'net_proceeds_approx_m':1987,'annual_coupon_m':coupon,'coupon_rate_face':coupon/D(2000),'issuance_net_debt_delta_approx_m':D(2000)-D(1987),'issuance_cost_per_old_share_proxy':D(13)/shares,'target_q3_revenue_m':251,'target_q3_gaap_ebit_m':8,'target_q3_adjusted_ebit_m':40,'target_gaap_margin':D(8)/D(251),'target_adjusted_margin':D(40)/D(251),'target_adjustment_gap_m':32,'illustrative_bridge_after_offering_only_m':D(5413)+13,'illustrative_value_after_offering_cost_only':D('124.53')-D(13)/shares}.items(): ck(k,r[k],v)
for key,value in [('bear','87.62'),('base','124.53'),('bull','184.06')]:
    ck('legacy_'+key,r['historic_standalone'][key],value)
    ck('comparison_'+key,r['old_value_comparison'][key],D(value)/price-1)
assert r['combined_valuation'] is None and r['entry_approved'] is False
s=(p/'report.md').read_text()
for text in ['d166196d424b5.htm','silicon-labs-reports-third-quarter-2026-results','no valoración integrada actual','no otra deducción del FCFF','no deuda ya desembolsada']:
    assert text in s,text
for private in ['DEV42RG8','Individual Cash','108k','30.8615']:
    assert private not in s,private
out={'status':'PASS','arithmetic_checks':len(checks),'checks':checks,'scope':'Independent Decimal arithmetic plus source/prose review; not a combined-company DCF audit.','source_review':{'notes':'Nov9 issuance verified; four $500m tranches, $108m annual coupons. Final prospectus net proceeds approximately $1987m after expenses; $1989.640m before expenses.','acquisition':'Pending all-cash $231/share, approximately $7.5bn enterprise value. Expected H1 2027 is conditional, not completed. $5bn facility undrawn as of September30 only.','target':'Nov10 Q3 release: revenue251, GAAP EBIT8, adjusted40; no annualization.','market':'Nov10 regular close300.52 at16EST; premarket excluded.'},'limitations':['$13m face-minus-net includes issuance discount and expenses; approximate financing-only effect, not certified November balance.','$0.0141 per share uses frozen921m proxy, not current diluted share count.','Old124.53 and184.06 remain dated standalone values; generous historical366.03 countercase retained.','Coupons not subtracted again from FCFF; conditional redemption premium not unconditional liability.','Acquisition synergies remain management forecast, not included free in a valuation.'],'privacy_review':'No account identifiers, screenshots, positions or quantities found in public report.','hashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['report.md','check.py','results.json']}}
(p/'audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(checks),'arithmetic checks; source/prose/privacy review passed')
