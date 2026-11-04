from pathlib import Path
import json
p=Path(__file__).resolve().parent
h=json.loads((p/'history/financial_history.json').read_text())
lines=['| Período | Ventas | EBIT operativo | NI Newmont | CFO | Capex caja | FCF simple |','|---|---:|---:|---:|---:|---:|---:|']
for period,row in h['periods'].items():
 vals=[row[k] for k in ['revenue','ebit_operating_reported_reconstructed','ni_parent','cfo','capex_cash','fcf_cfo_less_capex']]
 lines.append('| '+period+' | '+' | '.join(f'{v:,.0f}'.replace(',','.') for v in vals)+' |')
s=(p/'report_body.md').read_text().replace('{{HISTORY_TABLE}}','\n'.join(lines))
(p/'report.md').write_text(s)
