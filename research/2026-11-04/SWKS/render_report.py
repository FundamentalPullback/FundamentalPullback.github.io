from pathlib import Path
import html,re,json
P=Path(__file__).parent
s=(P/'report.md').read_text();lines=s.splitlines();body=[];table=False;ul=False;ol=False

def inline(t):
 t=html.escape(t);t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t);t=re.sub(r'\[([^\]]+)\]\((https?[^)]+)\)',r'<a href="\2">\1</a>',t);return t
for line in lines:
 if line.startswith('|'):
  if not table:body.append('<div class="table-wrap"><table>');table=True;first=True
  if re.match(r'^\|[-| ]+\|$',line):continue
  cells=line.strip('|').split('|');tag='th' if first else 'td';body.append('<tr>'+''.join(f'<{tag}>{inline(x.strip())}</{tag}>' for x in cells)+'</tr>');first=False;continue
 if table:body.append('</table></div>');table=False
 if not line.strip():continue
 if line.startswith('# '):body.append('<h1>'+inline(line[2:])+'</h1>');continue
 if line.startswith('## '):body.append('<h2>'+inline(line[3:])+'</h2>');continue
 if line.startswith('### '):body.append('<h3>'+inline(line[4:])+'</h3>');continue
 if line.startswith('- '):body.append('<p class="list">• '+inline(line[2:])+'</p>');continue
 body.append('<p>'+inline(line)+'</p>')
if table:body.append('</table></div>')
H=json.load(open(P/'history/history.json'));annual=[r for r in H if r['period'].startswith('FY')]
svg=['<svg role="img" aria-label="Ventas y EBIT GAAP independientes de FY2023 a FY2026, en millones USD" viewBox="0 0 840 260">']
for i,r in enumerate(annual):
 x=70+i*195;h=r['revenue']/5000*160;he=r['ebitGAAP']/5000*160
 svg += [f'<rect x="{x}" y="{210-h}" width="58" height="{h}" fill="#1f5770" rx="3"/>',f'<rect x="{x+66}" y="{210-he}" width="35" height="{he}" fill="#c38a37" rx="2"/>',f'<text x="{x+46}" y="235" text-anchor="middle">{r["period"]}</text>',f'<text x="{x+29}" y="{200-h}" text-anchor="middle">{r["revenue"]:,.0f}</text>']
svg+=['<rect x="550" y="6" width="12" height="12" fill="#1f5770"/><text x="580" y="17">Ventas</text><rect x="660" y="6" width="12" height="12" fill="#c38a37"/><text x="680" y="17">EBIT GAAP</text></svg>']
chart='<section class="chart"><h2>El legado pierde rentabilidad</h2>'+''.join(svg)+'<p class="caption">Skyworks independiente. No incluye Qorvo. Fuentes: 10-K FY25 y resultados FY26 citados en el informe.</p></section>'
content='\n'.join(body);mark=content.find('<h2>Scanner');content=content[:mark]+chart+content[mark:]
css='''body{margin:0;background:#eef2f4;color:#172c38;font:16px/1.62 system-ui,-apple-system,Arial,sans-serif}main{max-width:1060px;margin:36px auto;background:#fff;padding:54px 66px;box-shadow:0 5px 35px #1020300c}.eyebrow{font-size:12px;letter-spacing:2px;color:#476a7b;text-transform:uppercase}.flag{display:inline-block;padding:8px 13px;background:#fff3da;color:#6c4a14;font-size:13px;border-radius:4px}h1{font-size:40px;line-height:1.18;letter-spacing:-1.2px;margin:22px 0 24px;max-width:940px}h2{font-size:24px;line-height:1.3;margin:48px 0 16px;padding-top:16px;border-top:1px solid #dce5e9}h3{font-size:19px;margin-top:30px}p{margin:12px 0}a{color:#195b80;text-underline-offset:3px}strong{font-weight:700}.table-wrap{overflow-x:auto;margin:22px 0;border:1px solid #dbe5e9;border-radius:6px}table{width:100%;border-collapse:collapse;font-size:13px;line-height:1.45}th{background:#173e50;color:white;text-align:left;white-space:normal}th,td{padding:11px 12px;border-bottom:1px solid #dbe5e9}tr:nth-child(even){background:#f3f7f8}td:first-child{font-weight:600}td{vertical-align:top}svg{width:100%;height:auto;background:#f8fafb;border-radius:6px}svg text{font:13px Arial;fill:#23414e}.caption{font-size:12px;color:#647985}.list{padding-left:16px}.footer{margin-top:44px;padding-top:22px;border-top:1px solid #dce5e9;color:#647985;font-size:12px}@media(max-width:700px){main{margin:0;padding:28px 22px}h1{font-size:30px}table{font-size:12px}th,td{padding:8px}}@media print{body{background:white}main{margin:0;box-shadow:none;padding:18px}h2{break-after:avoid}tr{break-inside:avoid}a{color:#173e50}}'''
(P/'report.html').write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SWKS | Qorvo, capital y caja pendientes</title><style>'+css+'</style></head><body><main><div class="eyebrow">Fundamental Pullback · Investigación del 4 noviembre 2026</div><span class="flag">En observación · Sin valoración total ni entrada</span>'+content+'<div class="footer">Análisis de escenarios, no garantía de rentabilidad. Datos y supuestos claramente separados. El modelo combinado sigue condicionado a la conciliación de capital y caja.</div></main></body></html>')
