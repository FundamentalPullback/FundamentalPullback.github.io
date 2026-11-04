import pathlib,json,html
P=pathlib.Path(__file__).parent;m=json.loads((P/'model.json').read_text());h=json.loads((P/'history/history.json').read_text())['periods']
t='| Periodo | Ingresos | EBIT | NI common | EPS | CFO | Software | Activos | FCF | SBC CF |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
for k in ['FY2023','FY2024','FY2025','Q42024','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','TTM_Q32025','TTM_Q32026']:
 r=dict(h[k]);r.setdefault('eps_diluted',r.get('eps_diluted_sum_reported_quarters'));vals=[r.get(x) for x in ['revenue','ebit','ni_common','eps_diluted','cfo','software_cash','capex_cash','fcf_cfo_less_cash_capex_and_software','sbc_cfo']];t+='| '+k+' | '+' | '.join('—' if v is None else f'{v if j==3 else v/1000:,.3f}' for j,v in enumerate(vals))+' |\n'
ct='| Caso | Crecimiento años1–5 | Años6–10 | Márgenes años1–10 | Tasa | g | ROI | Impuesto |\n|---|---|---|---|---:|---:|---:|---:|\n'
for k,c in m['scenarios'].items():ct+='| '+k+' | '+', '.join(f'{100*x:g}%' for x in c['g'][:5])+' | '+', '.join(f'{100*x:g}%' for x in c['g'][5:])+' | '+', '.join(f'{100*x:g}%' for x in c['m'])+' | '+' | '.join(f'{100*c[x]:g}%' for x in ['w','tg','roic','tax'])+' |\n'
vt='| Caso | EV | Puente | PV terminal/EV | Valor/acción |\n|---|---:|---:|---:|---:|\n'
for k,r in m['cases'].items():vt+=f"| {k} | {r['ev']:.3f} | {r['bridge']:.4f} | {100*r['terminal_share']:.2f}% | {r['value']:.5f} |\n"
st='\n'.join(f'- {k}: {v:.5f} USD.' for k,v in m['sensitivities'].items())
s=(P/'report_body.md').read_text().replace('{HISTORY_TABLE}',t).replace('{SCENARIO_TABLE}',ct).replace('{VALUATION_TABLE}',vt).replace('{SENSITIVITIES}',st).replace('{PEERS}',(P/'comparables/notes.md').read_text());(P/'report.md').write_text(s);(P/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>TWLO investigación condicionada</title><style>body{max-width:1050px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(s)+'</pre></body></html>')
