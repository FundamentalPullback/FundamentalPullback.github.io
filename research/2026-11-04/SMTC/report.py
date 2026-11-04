import pathlib,json,html
p=pathlib.Path(__file__).parent;rows=json.loads((p/'history/financial_history.json').read_text())['periods'];fields=['revenue','ebit','net_income','eps_diluted','cfo','capex_ppe','capex_intangibles','fcf_ppe','sbc_cf'];s='| Periodo | Ventas | EBIT GAAP | NI | EPS diluido | CFO | PPE | Intangibles pagados | CFO−PPE | SBC en flujos |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in rows:
 if r['period'].startswith(('H1','9M')):continue
 s+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.3f}' for k in fields)+' |\n'
s+='\nEPS trimestral directo; EPS TTM es suma de cuatro cifras directas, no EPS calculado con un denominador común. TTM de flujos: anual menos semestre comparable más semestre actual. NI FY24 difiere en 0,001 del beneficio consolidado por participaciones no dominantes; no se oculta.\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{PEERS}',(p/'comparables/notes.md').read_text());(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>SMTC investigación parcial</title><style>body{max-width:1100px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
