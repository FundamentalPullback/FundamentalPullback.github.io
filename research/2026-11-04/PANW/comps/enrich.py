#!/usr/bin/env python3
"""Offline quarterly peer lens; no external dependencies or downloads."""
import json,pathlib,csv,hashlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(P/'reproduce.py')],check=True,capture_output=True)
i=json.loads((P/'inputs.json').read_text()); a=json.loads((P/'operating_comparables.json').read_text()); checks=json.loads((P/'checks.json').read_text());rows=[]
for ticker in ['PANW','FTNT','CHKP']:
 current=next(x for x in a['periods'] if x['company']==ticker and x['months']==3 and x['period'].endswith('2026'))
 prior=next(x for x in a['periods'] if x['company']==ticker and x['months']==3 and x['period'].endswith('2025'))
 r=dict(current)
 r.update(comparison_period=prior['period'],reported_revenue_growth_yoy=current['revenue']/prior['revenue']-1,gaap_ebit_growth_yoy=current['ebit']/prior['ebit']-1,cfo_growth_yoy=current['cfo']/prior['cfo']-1,cfo_margin=current['cfo']/current['revenue'],cash_flow_sbc_ratio_prior=prior['sbc_cf_to_revenue'],base_fcf_less_sbc_margin_sensitivity=(current['fcf_before_adjustments_less_sbc_sensitivity']/current['revenue']))
 rows.append(r)
assert rows[0]['period_start']=='2026-05-01' and rows[0]['period_end']=='2026-07-31'
assert all(r['period_end']=='2026-09-30' for r in rows[1:])
assert rows[0]['sbc_cf']==460 and rows[0]['sbc_cf']!=i['reported']['PANW_Q4FY2026']['sbc_related_operating_charges']
assert all(abs(r['fcf_before_company_adjustments']-r['cfo']+r['capital_spend_deducted'])<.0001 for r in rows)
assert rows[0]['company_adjustment']==35 and rows[1]['company_adjustment']==-17
out={'as_of':'2026-11-04','units':'USD millions; ratios decimal','scope':'Descriptive quarterly operating comparison, not a peer valuation or normalized organic-growth ranking','sbc_policy':'GAAP EBIT retains SBC. FCF less cash-flow SBC is a separate sensitivity only; do not subtract SBC again from a model whose EBIT already retains SBC.','valuation_status':'Not established: no consistent November 3 price, contemporaneous basic shares, EV bridge and TTM denominator set for all three companies in reused comparison sources.','periods':rows,'sources':i['sources']}
(P/'latest_quarter_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'latest_quarter_comparison.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
checks['tests']+=['PANW quarter May-July; peers July-September; not calendar aligned','PANW cash-flow SBC 460 distinguished from operating SBC-related charge 487','PANW +35 and FTNT -17 FCF adjustments retain opposite signs','Latest-quarter base FCF independently checked against CFO and spending']
checks['latest_quarter_records']=len(rows)
checks['limitations']=['Checks test arithmetic and period labels, not source authenticity or economic normalization','Peer valuation not certified','PANW separate quarterly software cash spending not disclosed in reviewed schedules','No pro-forma acquisition or organic growth bridge']
(P/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(P/'manifest.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(P))+'\n' for p in sorted(P.rglob('*')) if p.is_file() and p.name!='manifest.sha256'))
print(json.dumps(checks,indent=2))
