from pathlib import Path
import json,html
p=Path(__file__).parent;m=json.loads((p/'model.json').read_text());h=json.loads((p/'history/periods.json').read_text());s=(p/'report_body.md').read_text();fields=['revenue','ebit','net_income','eps_diluted','cfo','ppe_cash_purchases','sbc','da','fcf_cfo_less_ppe']
t='| Periodo | Ventas | EBIT | NI | EPS directo | CFO | PPE | SBC | D&A | CFO−PPE |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for r in h:t+='| '+r['period']+' | '+' | '.join('—' if r.get(k) is None else f'{r[k]:,.3f}' for k in fields)+' |\n'
s=s.replace('{HISTORY_TABLE}',t)
r={'BASE':m['cases']['base']['value_per_share'],'BEAR':m['cases']['bear']['value_per_share'],'BULL':m['cases']['bull']['value_per_share'],'TERMINAL_PCT':m['cases']['base']['terminal_share_pct'],'CAPACITY':m['sensitivities']['margin_on_installed_capacity_sales_growth_funding'],'CAPEX5':m['sensitivities']['terminal_capex_5pct'],'REVERSE_PP':m['reverse_margin_shift_roots'][0]*100}
for k,v in r.items():s=s.replace('{'+k+'}',f'{v:.2f}')
t='| Sensibilidad | USD/acción |\n|---|---:|\n'+'\n'.join('| '+k+' | '+f'{v:.4f}'+' |' for k,v in m['sensitivities'].items());s=s.replace('{SENSITIVITY_TABLE}',t)
c=json.loads((p/'comparables/outputs.json').read_text());t='| Empresa Q2 | Ventas | EBIT GAAP | EBIT tras ajustes específicos | Margen limitado |\n|---|---:|---:|---:|---:|\n'+'\n'.join(f"| {x['ticker']} | {x['revenue']:.3f} | {x['ebit']:.3f} | {x['ebit_ex_specific_items']:.3f} | {x['margin_ex_specific_items_pct']:.2f}% |"for x in c);s=s.replace('{COMPS_TABLE}',t)
(p/'report.md').write_text(s);(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>URBN investigación condicionada</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(s)+'</pre></body></html>')
