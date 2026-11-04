from pathlib import Path
import json,html
p=Path(__file__).parent;rows=json.loads((p/'history/history.json').read_text())['periods'];fields=['revenue','ebit','net_income_attributable','eps_diluted','cfo','capex','sbc','fcf_consolidated'];s='| Periodo | Ventas | EBIT | NI atribuible | EPS directo | CFO | PPE | SBC | CFO−PPE |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in rows:
 s+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.3f}' for k in fields)+' |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s);(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>FCX investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
