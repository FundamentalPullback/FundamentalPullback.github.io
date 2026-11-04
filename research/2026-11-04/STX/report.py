import pathlib,json,html
P=pathlib.Path(__file__).parent;H=json.loads((P/'history/financial_history.json').read_text());M=json.loads((P/'model.json').read_text());s='| Periodo | Semanas | Ventas | EBIT GAAP | NI | EPS | CFO | Capex | FCF | SBC |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in H:
 if r['period']=='Q1FY2025':continue
 s+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.2f}' for k in ['weeks','revenue','ebit','net_income','eps_diluted','cfo','capex','fcf','sbc'])+' |\n'
t='| Sensibilidad central | USD/acción |\n|---|---:|\n'
for k,v in M['sensitivities'].items():t+='| '+k+' | '+f'{v:,.2f}'+' |\n'
r=(P/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{SENSITIVITY_TABLE}',t).replace('{PEERS}',(P/'comparables/notes.md').read_text());(P/'report.md').write_text(r);(P/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>STX escenarios condicionados</title><style>body{max-width:1100px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(r)+'</pre></body></html>')
