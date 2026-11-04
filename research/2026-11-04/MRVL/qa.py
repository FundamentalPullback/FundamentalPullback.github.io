import pathlib,json
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());m=json.loads((P/'publication.json').read_text());h=a['history'];checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
for k in ['revenue','gaap_ebit','net_income_parent','cfo','da_total','sbc','capex_ppe','technology_license_purchases','technology_license_obligation_payments']:
 ck('4Q TTM '+k,abs(sum(h[q][k] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-h['TTM'][k])<.001)
for k,r in h.items():
 ck(k+' D&A',abs(r['da_total']-r['da_ex_acquired_intangibles']-r['acquired_intangible_amortization'])<.001)
 ck(k+' cash proxy',abs(r['cfo']-r['capex_ppe']-r['technology_license_purchases']-r['technology_license_obligation_payments']-r['sbc']-r['owner_cash_after_sbc_proxy'])<.001)
c=a['capital_aug1'];ck('Debt nominal-book',abs(c['nominal_debt']-c['book_debt']-c['unamortized_debt_cost'])<.001)
ck('EPS direct sum',abs(sum(h[q]['eps_diluted'] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-3.03)<.001)
ck('Common allocation difference',abs(h['TTM']['net_income_common_annual_ytd_bridge']-h['TTM']['net_income_common_sum_quarter_allocations']-2.1)<.001)
ck('Exchange arithmetic',abs(a['merger_arithmetic']['stock_consideration_per_lite_at_reference']-773.865)<.001)
ck('Prelim range',a['merger_arithmetic']['q3_prelim_low']==3087 and a['merger_arithmetic']['q3_prelim_high']==3213)
ck('No valuation',all(x is None for x in a['valuation'].values()) and all(m[k] is None for k in ['bear','base','bull','buy_ceiling']))
ck('No approval',not m['approved_entry'] and not m['stage35_approved'])
ck('No confirmed earnings',a['merger_arithmetic']['latest_earnings_date_confirmed'] is None)
p=a['avgo_comparison'];ck('AVGO cash',p['cfo']-p['ppe']==p['reported_fcf'])
l=a['lite_target_context'];ck('LITE cash',abs(l['CFO']-l['cash_capex']-l['derived_CFO_less_capex'])<.001)
r=(P/'report.md').read_text()
for x in m['pros_es']+m['cons_es']:ck('Exact evidence '+x[:24],x in r)
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'checks passed')
