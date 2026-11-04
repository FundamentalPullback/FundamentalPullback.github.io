import pathlib,json,math
P=pathlib.Path(__file__).parent;a=json.loads((P/'analysis.json').read_text());m=json.loads((P/'publication.json').read_text());h=json.loads((P/'history/normalized_history.json').read_text());d={r['period']:r for r in h['periods']};checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
f=a['fcf'];c=a['capital']
ck('H1 FCF',f['h1_cfo']-f['h1_cash_capex']==f['h1_reported_fcf'])
ck('H1 adjusted FCF',f['h1_reported_fcf']+f['h1_financing_receivables_addback']+f['h1_net_operating_lease_equipment_addback']==f['h1_adjusted_fcf'])
ck('Q2 FCF',f['q2_cfo']-f['q2_capex']==f['q2_reported_fcf'])
ck('Q2 adjusted FCF',f['q2_reported_fcf']+f['q2_finance_addback']+f['q2_lease_addback']==f['q2_adjusted_fcf'])
ck('Nominal debt',c['senior_notes']+c['legacy_notes']+c['actual_dfs_debt']+c['other_debt']==c['nominal_debt'])
ck('Core debt',c['senior_notes']+c['legacy_notes']-c['allocated_dfs_debt']==c['core_debt'])
ck('DFS allocation',c['actual_dfs_debt']+c['allocated_dfs_debt']==c['dfs_related_debt'])
ck('Book debt',c['nominal_debt']+c['carrying_adjustment']==c['book_debt'])
ck('DFS assets',c['financing_receivables']+c['operating_lease_equipment']==c['dfs_assets'])
ck('7 to 1 rounding',abs(c['dfs_assets']*7/8-c['dfs_related_debt'])<1)
for k in ['revenue','ebit','parent_net_income','cfo','da','sbc','cash_capex','financing_receivables_cash_use','isg_revenue','isg_ebit','csg_revenue','csg_ebit']:
 ck('TTM '+k,abs(d['FY2026'][k]+d['H1FY2027'][k]-d['H1FY2026'][k]-d['TTM'][k])<.001)
 ck('4Q '+k,abs(sum(d[q][k] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-d['TTM'][k])<.001)
ck('EPS sum',abs(sum(d[q]['gaap_diluted_eps'] for q in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-17.23)<.001)
ck('Valuations absent',all(v is None for v in a['valuation'].values()) and all(m[k] is None for k in ['bear','base','bull','buy_ceiling']))
ck('No entry',not m['approved_entry'] and not m['stage35_approved'])
r=(P/'report.md').read_text()
for line in m['pros_es']+m['cons_es']:ck('Exact report evidence '+line[:24],line in r)
p=a['peers'][0];ck('HPE definition',p['cfo']-p['cash_capex']+p['asset_sales']+p['fx_cash']==p['reported_fcf'])
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'checks passed')
