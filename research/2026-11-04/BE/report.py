from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/history.json').read_text());columns=['period','revenue','ebit_gaap','ni_attributable','eps_diluted','cfo','capex_ppe','sbc_cashflow','da','fcf_ppe']
s='| Periodo | Ingresos | EBIT | NI atribuible | EPS diluido | CFO | PPE | SBC | D&A | CFO−PPE |\n|'+'|'.join(['---']*len(columns))+'|\n'
for r in h['rows']:
 s+='| '+' | '.join(('n/d' if r.get(k) is None else str(r.get(k))) if not isinstance(r.get(k),(int,float)) else f'{r[k]:,.3f}' for k in columns)+' |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s)
(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>BE — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
