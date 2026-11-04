from pathlib import Path
import html
p=Path(__file__).parent
s=(p/'history/ledger.md').read_text();table=s[s.index('| Period'):s.index('## Comparability')]
t=(p/'report_body.md').read_text().replace('{HISTORY_TABLE}',table)
(p/'report.md').write_text(t)
(p/'report.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>LSCC investigación parcial</title><style>body{max-width:1200px;margin:30px auto;padding:20px;font:16px/1.55 system-ui;color:#173047}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><body><pre>'+html.escape(t)+'</pre></body></html>')
