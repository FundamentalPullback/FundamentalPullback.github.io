"""Independent public bridge audit; no private source files or production imports."""
from decimal import Decimal as D
from pathlib import Path
import json, hashlib
p=Path(__file__).parent
r=json.loads((p/'results.json').read_text());checks=[]
def ck(name,actual,expected):
    assert abs(D(str(actual))-expected)<D('1e-9'),name
    checks.append({'name':name,'expected':str(expected),'pass':True})
old=D(5639)-(D(1697)-700)+150+625
ck('original claim identity',r['oldClaimsMillion'],old)
ck('maturity sum',sum(r['principalMaturities']),D(5696))
ck('pension net',r['netPensionPostRetire'],D(625)+42-253)
claims=[old,old+57,old+57+42,old+57+42+150,old+57+(414-625)+150]
for (name,row),claim in zip(r['cases'].items(),claims):
    delta=(old-claim)/291
    ck(name+' claims',row['claimsMillion'],claim)
    ck(name+' delta',row['valueDeltaPerShare'],delta)
    ck(name+' illustration',row['frozenValueIllustration'],D('156.87')+delta)
cap=D('22458.7')*(D('.06')-D('.055'))
ck('incremental year1 capex',r['oneYearExtraCapexMillion'],cap)
ck('single-year discounted capex per share',r['oneYearOnlyPVDeltaPerShare'],-cap/D('1.0975')/291)
assert not r['entryApproved'] and not r['fullDCFRefreshed']
checks.append({'name':'limited-scope flags','pass':True})
report=(p/'report.md').read_text()
import re
assert not re.search(r'Individual Cash|account identifier|número de cuenta', report, re.I)
checks.append({'name':'no known private account quantities/identifier','pass':True})
out={'status':'PASS','check_count':len(checks),'checks':checks,'scope':'Independent arithmetic and source/prose QA of bounded bridge and one-year capital sensitivity. Not full DCF audit.','source_review':['Nov9 SEC10K debt note principal5696 less57 issuance adjustments =5639; maturities and400 August2027 note verified.','Pension current42, noncurrent625, assets253 gives414 net including8 postretirement. Gross/net access assumptions disclosed.','Earn-out150 is acquisition-date estimated fair value, not fixed maximum or certified current liability; separate fromRNCI150.','SEC10K liquidity paragraph1084 explicitly guides fiscal2027 capital spending approximately6% of net sales.','Astrodyne remains pending; no duplicate1400 subtraction. Baird08:55EST confirmed; content not claimed verified.'],'prose_review':'PASS. Public report contains no private account quantities or identifiers, distinguishes frozen scenarios and illustrative claims from new valuation. No unsupported sale/entry instruction.','hashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['check.py','results.json','report.md','audit.py']}}
(p/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(checks))
