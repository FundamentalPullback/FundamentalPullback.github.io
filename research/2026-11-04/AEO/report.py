from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/history.json').read_text());f=json.loads((p/'facts/inputs.json').read_text())
cols=['revenue','ebit','net_income','net_income_parent','eps_diluted','cfo','capex','sbc','da_cashflow','fcf_reported_proxy']
s='| Periodo | Ingresos | EBIT | NI consolidado | NI AEO | EPS diluido | CFO | Capex | SBC | D&A cashflow | CFO − capex |\n|'+'|'.join(['---']*11)+'|\n'
for period,r in h.items():s+='| '+period+' | '+' | '.join('n/d' if r.get(k) is None else f'{r[k]:,.3f}' for k in cols)+' |\n'
links=f['sources'].copy()
for r in json.loads((p/'comparables/inputs.json').read_text()):links['peer_'+r['ticker']]=r['source']
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{SOURCE_LIST}','\n'.join('- ['+k+']('+v+')' for k,v in links.items()))
(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>AEO — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
