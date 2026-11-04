from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/history.json').read_text());m=json.loads((p/'model.json').read_text());cols=['period','revenue','ebit','ni','eps_diluted','cfo','capex_ppe','da','sbc','fcf_ppe']
s='| Periodo | Ventas | EBIT | NI | EPS | CFO | PPE | D&A | SBC | CFO−PPE |\n|'+'|'.join(['---']*len(cols))+'|\n'
for r in h['rows']:s+='| '+' | '.join('n/d' if r.get(k) is None else (f'{r[k]:,.3f}' if isinstance(r[k],(float,int)) else str(r[k])) for k in cols)+' |\n'
v='| Escenario | EV operativo | Puente | Patrimonio | USD/acción |\n|---|---:|---:|---:|---:|\n'
for k,x in m['cases'].items():v+=f"| {k} | {x['ev']:,.3f} | {x['bridge']:,.3f} | {x['equity']:,.3f} | {x['value_per_share']:.4f} |\n"
v+='\n| Sensibilidad central | USD/acción |\n|---|---:|\n'
labels={'capex_plus_1pp':'Capex pagado +1 punto de ventas','margin_minus_1pp':'Márgenes −1 punto todos los años','margin_plus_1pp':'Márgenes +1 punto todos los años','tax_26pct':'Impuesto 26 %','no_postquarter_buyback_reserve':'Sin reserva de recompras posteriores','no_lease_guarantee_stress':'Sin estrés de garantías'}
for k,x in m['sensitivities'].items():v+=f'| {labels[k]} | {x:.4f} |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{MODEL_RESULTS}',v);(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>EAT — FCFF condicionado</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
