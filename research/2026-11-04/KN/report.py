from pathlib import Path
import json,html
p=Path(__file__).parent;m=json.loads((p/'model.json').read_text());h=json.loads((p/'history/history.json').read_text())['rows'];s=(p/'report_body.md').read_text();fields=['revenue','ebit','ni_continuing','eps_continuing_diluted','cfo_consolidated','cfo_continuing_nongaap','capex_continuing_nongaap','sbc_continuing','fcf_continuing_company']
t='| Periodo | Ventas | EBIT | NI continuado | EPS directo | CFO consolidado | CFO continuado | Capex continuado | SBC | FCF continuado |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in h:
 t+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.3f}' for k in fields)+' |\n'
t+='\nEPS TTM calculado como suma de trimestres directos: continuado 0,87 / total 0,82 para septiembre 2026; continuado 0,42 / total 0,48 para septiembre 2025. No son EPS TTM publicados.\n'
s=s.replace('{HISTORY_TABLE}',t)
r={'BASE':m['cases']['base']['value_per_share'],'BEAR':m['cases']['bear']['value_per_share'],'BULL':m['cases']['bull']['value_per_share'],'SYNTIANT':m['sensitivities']['include_syntiant_at_carrying_not_fair_value'],'TERMINAL_PCT':m['cases']['base']['terminal_share_pct'],'CAPACITY':m['sensitivities']['margin_on_installed_capacity_sales_growth_funding'],'CAPEX6':m['sensitivities']['capex_6pct'],'REVERSE_MAX':m['reverse_scan_max']}
for k,v in r.items():s=s.replace('{'+k+'}',f'{v:.2f}')
t='| Sensibilidad | USD/acción |\n|---|---:|\n'+'\n'.join('| '+k+' | '+f'{v:.4f}'+' |' for k,v in m['sensitivities'].items());s=s.replace('{SENSITIVITY_TABLE}',t)
(p/'report.md').write_text(s);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>KN investigación condicionada</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(s)+'</pre></body></html>')
