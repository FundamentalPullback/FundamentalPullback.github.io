import pathlib,json
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());m=json.loads((P/'publication.json').read_text());h=a['history']['periods'];checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
for k,r in h.items():
 ck(k+' FCF',abs(r['cfo']-r['ppe_cash']-r['capitalized_software_cash']-r['issuer_fcf'])<.01)
 ck(k+' SBC proxy',abs(r['issuer_fcf']-r['sbc_expensed']-r['fcf_less_expensed_sbc'])<.01)
q=a['q3_usdm'];ck('Adjusted EBIT',abs(q['ebit_gaap']+q['sbc_expensed']+q['acquired_amortization']+q['equity_payroll_tax_expense']+q['ma_expense']-q['ebit_adjusted'])<.001)
ck('Net income bridge',abs(q['ebit_gaap']+q['net_other_income']-q['tax']-q['net_income'])<.001)
ck('Q3 FCF',abs(q['cfo']-q['ppe']-q['software_cash']-q['issuer_fcf'])<.001)
ck('Q3 expensed SBC proxy',abs(q['fcf_less_expensed_sbc']-13.453)<.001)
ck('Capitalized SBC unknown',q['sbc_capitalized'] is None)
ck('No valuation',all(x is None for x in a['valuation'].values()) and all(m[k] is None for k in ['bear','base','bull','buy_ceiling']))
ck('No entry',not m['approved_entry'] and not m['stage35_approved'])
ck('Price pre-event',a['price_is_pre_earnings'] and a['price_date']=='2026-11-03')
p=a['peers'][0];ck('DT adjusted FCF',abs(p['cfo']-p['ppe']-p['software_cash']+p['cash_adjustment']-p['adjusted_fcf'])<.001)
ck('Latest complete footnotes older',a['latest_10q_identified']=='2026-06-30')
r=(P/'report.md').read_text()
for x in m['pros_es']+m['cons_es']:ck('Exact evidence '+x[:25],x in r)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'history_note':'Separate 52 source checks preserve five immaterial direct-quarter/cumulative presentation differences; not asserted exact.'},indent=2)+'\n');print(len(checks),'checks passed')
