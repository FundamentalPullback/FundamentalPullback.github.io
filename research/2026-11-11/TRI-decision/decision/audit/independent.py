import json, pathlib, hashlib
p=pathlib.Path(__file__).resolve().parents[1]
mfile=p.parent/'site/research/2026-11-04/TRI/model.json'
if not mfile.exists(): mfile=p.parents[2]/'2026-11-04/TRI/model.json'
m=json.loads(mfile.read_text());r=json.loads((p/'results.json').read_text());a=m['base_assumptions'];checks=[]
def chk(n,x,y,t=1e-8):
 checks.append({'name':n,'computed':x,'reference':y,'pass':abs(x-y)<t})
roy=83
for _ in range(10):roy*=.95
terminalcore=(m['base']['rows'][-1]['rev']-roy)*1.03
termroy=roy*.95
ratio=.325*(1-.21)*(1-.03/.25)
chk('terminal legacy full FCFF',(terminalcore+termroy)*ratio,m['base']['terminal_fcff'])
loss=termroy*ratio/(.085-.03)*pow(1.085,-10)
chk('year10royalty',roy,r['royalty_year10'])
chk('terminalFCFF royalty',termroy*ratio,r['legacy_terminal_FCFF_royalty_component'])
chk('PVloss',loss,r['no_renewal_terminal_only_PV_reduction_m'])
chk('per share loss',loss/435,r['per_share_reduction'])
chk('central sensitivity',m['base']['value']-loss/435,r['central_after_terminal_only_sensitivity'])
cf=m['expected_return'];cash=cf['cash_to_common_m'][:];cash[-1]+=cf['terminal_equity_m']
def solve(price):
 rate=.07
 for _ in range(25):
  f=sum(v/(1+rate)**i for i,v in enumerate(cash,1))-price*435
  df=-sum(i*v/(1+rate)**(i+1) for i,v in enumerate(cash,1))
  rate-=f/df
 return rate
chk('IRR current independentNewton',solve(108.41),r['legacy_illustrative_IRR_at_current_close'])
chk('IRR prior tieout',solve(109.78),cf['at_price'])
chk('SBC growth',22/84,r['continuing_SBC_growth'])
chk('cross perimeter arithmetic not certified',111-84+106,r['cross_perimeter_TTM_arithmetic_NOT_verified'])
assert all(v>0 for v in cash)
assert all(c['pass'] for c in checks)
out={'status':'PASS','count':len(checks),'checks':checks,'model_sha256':hashlib.sha256(mfile.read_bytes()).hexdigest(),'review':['No production calculator imported. Independent iterative royalty and Newton IRR calculations.','Terminal deletion is the component embedded in old blended aggregate Gordon terminal. It is NOT full contractual runoff valuation; renewal and retained costs remain uncertain.','Ten-year initial term from Oct1 2026 not exact model fiscalyear clock; terminal-only stress deliberately does not adjust earlier rows.','SBC133 is mixed-perimeter arithmetic, not actual continuing/combined TTM. No extra SBC deduction in forecast EBIT.','IRR freezes historical terminal equity and dated claims; not expected realized investment return.']}
(p/'audit.json').write_text(json.dumps(out,indent=2));(p/'audit/output.json').write_text(json.dumps(out,indent=2));print(out['status'],out['count'])
