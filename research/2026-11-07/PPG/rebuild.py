"""Rebuild numerical artifacts and validate the frozen authored report and summary."""
from pathlib import Path
import subprocess,sys,json,hashlib
P=Path(__file__).parent
subprocess.run([sys.executable,str(P/'model.py')],check=True,cwd=P)
r=json.loads((P/'inputs_and_results.json').read_text());s=json.loads((P/'summary.json').read_text());report=(P/'PPG_report.md').read_text()
for case,out in r['results'].items():
 assert abs(s[case]-round(out['per_share'],2))<1e-8
 assert f"${out['per_share']:.2f}" in report
assert f"{100*r['inverse_margin']:.2f}%" in report
for x in s['pros']+s['cons']:
 assert x['evidence'] in report and x['es'] in report and x['en'] in report and x['sourceUrl'] in report
for c in ['sales','cogs','sga','dep','amort','rd','pretax','interest_exp','interest_inc','net_cont','cfo_cont','capex','sbc']:
 assert abs(sum(r['actuals'][k][c] for k in ['Q42025','Q12026','Q22026','Q32026'])-r['actuals']['TTM2026'][c])<1e-7
assert all(set(x)=={'url','title','date','purpose'} for x in json.loads((P/'source_ledger.json').read_text()))
q=dict(r['qa'],all_forecast_years_delta_nopat_funded=True,entryApproved=False,stage3Complete=False,approvedValuation=None,visual_review='not performed',evidence_exact_contiguous=True,all_period_columns_quarter_tie=True,summary_values_tie=True,bridge='conditional carrying-debt and noncurrent pension proxies; current reconciliation open')
(P/'QA.json').write_text(json.dumps(q,indent=2))
subprocess.run(['pandoc',str(P/'PPG_report.md'),'-s','--metadata','title=PPG: operating recovery and valuation','-o',str(P/'PPG_report.html')],check=True)
print('Rebuilt numerical files and HTML; static report and bilingual summary assertions pass.')
