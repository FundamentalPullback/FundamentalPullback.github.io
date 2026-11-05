import pathlib,json,re,html,hashlib,zipfile,shutil
from openpyxl import load_workbook
P=pathlib.Path(__file__).parent
# Render markdown without third-party dependencies.
def inline(s):
 s=html.escape(s);s=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s);return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
def render(md):
 out=[];table=False;lis=False
 for line in md.splitlines():
  if line.startswith('|'):
   if not table:out.append('<table>');table=True
   if re.fullmatch(r'[| :\-]+',line):continue
   out.append('<tr>'+''.join('<td>'+inline(x.strip())+'</td>' for x in line.strip('|').split('|'))+'</tr>');continue
  if table:out.append('</table>');table=False
  if line.startswith('- '):
   if not lis:out.append('<ul>');lis=True
   out.append('<li>'+inline(line[2:])+'</li>');continue
  if lis:out.append('</ul>');lis=False
  if line.startswith('#'):
   n=len(line)-len(line.lstrip('#'));out.append(f'<h{n}>'+inline(line[n:].strip())+f'</h{n}>')
  elif line:out.append('<p>'+inline(line)+'</p>')
 return ''.join(out)
if __name__=='__main__':
 md=(P/'UNFI_research.md').read_text()
 replacements={'confórmulas':'con fórmulas','trescasos':'tres casos','fuenteaentrada':'fuente a entrada','matriztrimestral':'matriz trimestral','puentecontable':'puente contable','deproveedor':'de proveedor','declientes':'de clientes','deguía':'de guía','del4':'del 4','yterminal':'y terminal','yPython':'y Python','conel':'con el','yse':'y se','deseguridad':'de seguridad','caenbajo':'caen bajo','conmenor':'con menor','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocre ce':'o crece','ocrece':'o crece','variacióndebalance':'variación de balance','desdeagosto':'desde agosto','residualseguro':'residual seguro','caja sostenible':'caja sostenible','deoctubre':'de octubre','enYahoo':'en Yahoo','yriesgo':'y riesgo','sueEV':'su EV','suEV':'su EV','compauditado':'comp auditado','leasesen':'leases en','TextilUFI':'Textil UFI','textilUFI':'textil UFI','yestructura':'y estructura','noes':'no es','antes deaprobar':'antes de aprobar','antes deentrega':'antes de entrega','antes deapertura':'antes de apertura','despuésde':'después de','sinoperatingleases':'sin operating leases'}
 for a,b in replacements.items():md=md.replace(a,b)
 md=md.replace('1,31%→1,51%','1,28%→1,48%').replace('36,06 x','36,04 x').replace('18,23 x','18,22 x').replace('13,81–16,11 x','13,80–16,10 x').replace('14,87 x','14,86 x').replace('21,01–28,42 x','21,00–28,41 x').replace('24,16 x','24,15 x')
 md=md.replace('Método fin de año con balance FY 26; no fingimos un stub postagosto con cash flows no publicados. El corte de valoración es revisión del 5 nov anclada al último balance; sensibilidad de calendario debe considerarse si se pretende ejecutar.','Método de fin de año ajustado por el offset explícito a 4 de noviembre. El balance de agosto se mantiene como supuesto sin añadir un segundo stub de caja; no se certifica el balance actual.')
 md=md.replace('Esa limitación impide aprobación plena, no análisis DCF.','Esta limitación reduce la fuerza del contraste de múltiplos, pero no constituye por sí sola un veto al DCF.')
 md=re.sub(r'\bFY (\d{2})',r'FY\1',md);md=md.replace('A 104','A104');md=re.sub(r'\bQ ([1-4])',r'Q\1',md)
 (P/'UNFI_research.md').write_text(md)
 css='body{font:15px/1.5 Arial,sans-serif;color:#183247;margin:0 auto;max-width:1180px;padding:40px;background:#fafcfd}h1,h2{color:#12334b;line-height:1.2}h2{border-top:2px solid #cad5df;padding-top:20px;margin-top:30px}table{border-collapse:collapse;width:100%;font-size:10px;background:white}td{padding:4px;white-space:nowrap;border-bottom:1px solid #d4dee5}tr:first-child{background:#12334b;color:white;font-weight:bold}tr:first-child td{white-space:normal}a{color:#087f8c}p{margin:12px 0}@media print{body{padding:0;font-size:10pt}h2{break-after:avoid}tr{break-inside:avoid}table{font-size:7pt}td{padding:3px}}'
 (P/'UNFI_research.html').write_text('<!doctype html><meta charset="utf-8"><title>UNFI | Research</title><style>'+css+'</style>'+render(md))
