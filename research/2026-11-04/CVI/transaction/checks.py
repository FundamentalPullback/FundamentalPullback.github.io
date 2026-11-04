#!/usr/bin/env python3
import csv,json,pathlib,math
p=pathlib.Path(__file__).resolve().parent
f=json.loads((p/'facts.json').read_text()); rs=list(csv.DictReader((p/'target_financials.csv').open())); d={r['period']:r for r in rs}
checks=[]
def check(name,ok):
 assert ok,name
 checks.append({'check':name,'passed':bool(ok)})
def n(r,k): return float(r[k])
for r in rs:
 check(r['period']+' EBIT',n(r,'operating_ebit')==n(r,'pretax_income_no_allocated_debt_interest')-n(r,'other_income_including_equity'))
 check(r['period']+' SRE normalization',n(r,'operating_ebit_ex_sre')==n(r,'operating_ebit')-n(r,'sre_credit'))
 check(r['period']+' gross capex cash bridge',n(r,'cfo_minus_gross_capex')==n(r,'cfo')-n(r,'gross_capex_including_intangibles'))
 check(r['period']+' EBITDA',n(r,'ebitda_historical_policy')==n(r,'pretax_income_no_allocated_debt_interest')+n(r,'da'))
for k in ['sales','other_income_including_equity','pretax_income_no_allocated_debt_interest','operating_ebit','da','sre_credit','cfo','gross_capex_including_intangibles','turnaround_expense_reclassified_to_capitalization','ebitda_cvi_policy_before_purchase_accounting']:
 check('TTM '+k,n(d['TTM2026-09'],k)==n(d['FY2025'],k)+n(d['9M2026'],k)-n(d['9M2025'],k))
check('CVI-policy EBITDA release tie',n(d['TTM2026-09'],'ebitda_cvi_policy_before_purchase_accounting')==1158)
check('offering gross threshold',f['offering']['gross_derived']>=500)
check('secondary excluded',f['offering']['secondary_shares']==0)
check('PIPE final unresolved',f['trafigura']['final_shares'] is None)
check('8K cash bridge',1278+3970-4969-183==96)
check('preliminary prospectus cash bridge',1278+3943-4969-183==69)
check('8K debt bridge',1769+2675-183==4261)
check('no full filings in public package',not list(p.glob('*.htm')) and not list(p.glob('*.html')))
check('public offering discount exception',f['trafigura']['public_offering_exception']['discount']<=.15)
check('public offering size exception',f['trafigura']['public_offering_exception']['gross_including_full_option']<=750)
result={'status':'PASS','checks':checks,'notes':['Offline mathematical/consistency checks only; source truth requires reading linked primary documents.','Do not assume pre-closing funding commitment is a post-closing cash reserve.','All future financing and dilution remain conditional.']}
(p/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','check_count':len(checks)}))
