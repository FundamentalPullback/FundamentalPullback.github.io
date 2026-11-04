from pathlib import Path
import json,html
p=Path(__file__).parent;rows=json.loads((p/'history/history.json').read_text())['rows'];fields=['revenue_continuing','operating_income_continuing','net_income_continuing','eps_diluted_continuing','cfo_continuing','capex_ppe_continuing','sbc_continuing','fcf_continuing_strict']
s='| Periodo | Ventas | EBIT | NI continuado | EPS directo | CFO continuado | Capex PPE | SBC | CFO−PPE |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in rows:
 if r.get('kind') not in ['FY','Q','quarter','TTM']:continue
 s+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.3f}' for k in fields)+' |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{PEERS}',(p/'comparables/notes.md').read_text());(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>NVT investigación parcial</title><style>body{max-width:1100px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
