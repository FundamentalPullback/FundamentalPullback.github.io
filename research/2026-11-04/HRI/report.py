from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/history.json').read_text());f=json.loads((p/'facts/inputs.json').read_text())
cols=['sales','operating_ebit','net_income','eps_diluted','cfo','rental_gross_capex','rental_disposal_proceeds','nonrental_capex','rental_da','other_da','sbc','fcf_after_net_capex']
s='| Periodo | Ingresos | EBIT | NI | EPS diluido | CFO | Capex flota pagado | Ventas flota cobradas | Otro capex | DA flota | Otra DA | SBC | CFO menos capex más disposiciones |\n|'+'|'.join(['---']*13)+'|\n'
for period,r in h['periods'].items():s+='| '+period+' | '+' | '.join('n/d' if r.get(k,{}).get('value') is None else f"{r[k]['value']:,.2f}" for k in cols)+' |\n'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{SOURCE_LIST}','\n'.join('- ['+k+']('+v+')' for k,v in f['sources'].items()))
(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>HRI — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
