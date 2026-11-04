from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/normalized_history.json').read_text())['periods'];f=json.loads((p/'facts/inputs.json').read_text())
cols=['revenue','ebit_gaap','net_income','eps_diluted','cfo','capex_including_software','sbc','da','fas_cas_operating_adjustment','fcf_cfo_less_capex']
s='| Periodo | Ingresos | EBIT GAAP | NI | EPS diluido | CFO | Capex incl. software | SBC | D&A | FAS/CAS operativo | FCF mecánico |\n|'+'|'.join(['---']*11)+'|\n'
for period,r in h.items():s+='| '+period+' | '+' | '.join('n/d' if r.get(k) is None else f'{r[k]:,.2f}' for k in cols)+' |\n'
links=f['sources'];sources='\n'.join('- ['+k+']('+v+')' for k,v in links.items())+'\n\nLa historia y los extractos numéricos aportan fuentes adicionales en history/sources.json y trazabilidad por campo.'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{SOURCE_LIST}',sources)
(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>LMT — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
