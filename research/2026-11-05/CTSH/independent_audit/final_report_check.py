from pathlib import Path
import json,hashlib,re,sys
from html.parser import HTMLParser
O=Path(__file__).parent;P=Path(sys.argv[1]) if len(sys.argv)>1 else O/'model_snapshot'
class TextOnly(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d)
h=TextOnly();h.feed((P/'report.html').read_text());htmltext=' '.join(h.parts);report=(P/'report.md').read_text()
q=json.loads((P/'QA.json').read_text());v=json.loads((P/'source_review/validation_checks.json').read_text());r=json.loads((O/'independent_results.json').read_text());run=json.loads((P/'run_log.json').read_text());s=json.loads((P/'sensitivity.json').read_text())
checks={
'independent_264_checks':r['all_numerical_checks_pass'] and r['numerical_check_count']==264,
'author_156_checks':q['count']==156 and q['failures']==0,
'primary_source_23_checks':len(v)==23 and all(x['status']=='PASS' for x in v),
'nine_step_run_log_pass':run['all_steps_passed'] and len(run['steps'])==9 and all(x['exit_code']==0 for x in run['steps']),
'regular_close_65_78':'65,78' in report,
'core_values_present':all(x in report and x in htmltext for x in ['79,34','51,76','109,12','84,95']),
'combined_risk_disclosed':all(x in report and x in htmltext for x in ['64,83','63,58']),
'stub_economics_exact':abs(s['additional_checks']['without_economic_Q4_stub']-(r['base']['value']-r['base']['pv_stub']/448.830425))<1e-7 and '77,51' in report,
'dyflex_terms_repaired':'210m' in report and 'DyFlex' in report,
'earnings_timing_repaired':'8:30 de la mañana' in report and 'antes de la apertura' in report and 'después del cierre' not in report,
'obsolete_trigger_removed':'66,10' not in report,
'current_resistance_not_overridden':'66,77' in report and 'La vía C queda suspendida' in report,
'prospective_A_labeled_not_validated':'Vía A' in report and 'no un patrón estadísticamente validado' in report,
'prior20_excludes_signal':'excluyendo la sesión de señal' in report,
 'technical_price_max_65_25':'máximo técnico propuesto 65,25' in report,
'expiration_unambiguous':'última sesión admisible de señal es el 9 noviembre' in report and 'caducan al cierre del 10 noviembre' in report,
'stage35_not_approved':'No hay Stage 3.5 aprobado' in report,
'P_cash_not_verified':'no verificados' in report,
'not_formula_workbook':'No es un libro Excel' in report,
'legacy_preserved':bool(re.search(r'Se conserva A\s*120',report))
}
financials=json.loads((P/'source_review/financials.json').read_text())
periods=['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026']
expected=[3.99,3.68,5.31,1.62,.42,.98,2.06]
ratios=[financials[k]['strict_fcf']/financials[k]['shares_diluted'] for k in periods]
checks['new_FCF_per_share_paragraph']=all(round(a,2)==b for a,b in zip(ratios,expected)) and round(2363/448.830425,2)==5.26 and '3,99/3,68/5,31' in report and '1,62/0,42/0,98/2,06' in report and 'equivale a 5,26 USD' in report and 'no es una serie histórica perfectamente comparable' in report
publication=json.loads((P/'publication_record.json').read_text())
checks['publication_metadata_consistent']=publication['stage3_decision']=='approved_conditional_reasonable_price' and publication['entry_approved'] is False and publication['stage35_approved'] is False and publication['trade_order_authorized'] is False and publication['robust_undervaluation_claim'] is False and publication['technical_plan']['signal_seen'] is False and publication['technical_plan']['quantity'] is None
assert all(checks.values()),checks
files=['value.py','model/inputs.json','results.json','beta_estimate.json','technical.json','sensitivity.json','QA.json','source_review/validation_checks.json','source_review/source_review.md','report.md','report.html','reproduce_all.py','run_log.json','source_review/financials.json','publication_record.json']
hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files}
out={'status':'PASS_FOR_CONDITIONAL_ANALYTICAL_RELEASE','date_utc':'2026-11-05','report_checks':checks,'report_check_count':len(checks),'all_report_checks_pass':all(checks.values()),'scope':'Core economics, source corrections, report/HTML numerical and claim tie-out, prospective setup coherence. Not a trade or Stage3.5 approval.','final_values':{k:r[k]['value'] for k in ['base','bear','bull','owned_business_crosscheck']},'snapshot_hashes':hashes,'limitations':['Stage3 classification is conditional reasonable price, not robust cheapness','No portfolio P, cash, orders, actual signal or executable quantity verified','Technical setup is prospective analyst judgment, not empirically validated','Report footer changes require updated hash but do not by themselves change analytical conclusions']}
(O/'final_report_audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'status':out['status'],'report_checks':len(checks),'all_pass':all(checks.values()),'report_hashes':{f:hashes[f] for f in ['report.md','report.html']}},indent=2))
