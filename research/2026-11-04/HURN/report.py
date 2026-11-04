from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/history.json').read_text());cols=['period','revenue_gaap','revenue_rbr','ebit','ni','eps_diluted','cfo','capex_ppe','capex_software','sbc']
s='| Periodo | Ingresos GAAP | RBR | EBIT | NI | EPS diluido | CFO | PPE | Software | SBC |\n|'+'|'.join(['---']*len(cols))+'|\n'
for r in h['rows']:
 s+='| '+' | '.join('n/d' if r.get(k) is None else (f'{r[k]:,.3f}' if isinstance(r[k],(float,int)) else str(r[k])) for k in cols)+' |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s);(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>HURN — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
