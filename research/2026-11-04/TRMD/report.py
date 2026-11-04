from pathlib import Path
import json,html
p=Path(__file__).parent;h=json.loads((p/'history/normalized_history.json').read_text());a=json.loads((p/'analysis.json').read_text());f=json.loads((p/'facts/inputs.json').read_text())
cols=['revenue','tce_tanker','ebit','net_income','diluted_eps_usd','cfo','cash_tangible_investment','cash_intangible_investment','sbc_expense','cfo_less_all_cash_capex']
s='| Periodo | Ingresos | TCE tanker | EBIT | NI consolidado | EPS diluido | CFO | Tangibles cash | Intangibles cash | SBC gasto | CFO − capex |\n|'+'|'.join(['---']*11)+'|\n'
for period,r in h.items():s+='| '+period+' | '+' | '.join('n/d' if r.get(k) is None else f'{r[k]:,.2f}' for k in cols)+' |\n'
n='| Recorte de brokers a flota existente | NAV mecánico por acción tras dividendo |\n|---|---|\n'
for r in a['nav_sensitivity_not_fair_value']:n+=f"| {r['broker_fleet_haircut']:.0%} | {r['after_declared_dividend_nav_proxy']:.2f} USD |\n"
links=f['sources'].copy();links['peer_STNG']=json.loads((p/'comparables/inputs.json').read_text())['source']
sources='\n'.join('- ['+k+']('+v+')' for k,v in links.items())+'\n\nLos archivos history/sources.json y field_lineage.json aportan las fuentes primarias y la trazabilidad adicional de cada periodo.'
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',s).replace('{NAV_TABLE}',n).replace('{SOURCE_LIST}',sources)
(p/'report.md').write_text(t);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>TRMD — investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
