from pathlib import Path
import re,json,subprocess
P=Path(__file__).parent
def tidy(s):
 tokens=[]
 def protect(m):tokens.append(m.group());return '\x01'+chr(0xE000+len(tokens)-1)+'\x02'
 s=re.sub(r'https?://[^\s)>]+|\b(?:Stage3\.5|[qk]\d+(?:prev)?|A\d{3}|FY\d{2,4}|Q\d(?:FY\d+)?|[a-z]+_[a-z_]*\d+)\b',protect,s)
 s=re.sub(r'(?<=[A-Za-záéíóúñÁÉÍÓÚÑ])(?=\d)',' ',s)
 s=re.sub(r'(?<=\d)(?=[A-Za-záéíóúñÁÉÍÓÚÑ])',' ',s)
 s=re.sub(r'(?<=%)(?=[A-Za-záéíóúñÁÉÍÓÚÑ])',' ',s)
 s=re.sub(r'(?<=[a-z])(?=\$)',' ',s)
 for a,b in {'EBITTTM':'EBIT TTM','TTMseptiembre':'TTM septiembre','amortizaciónTTM':'amortización TTM','netoTTM':'neto TTM','ventasTTM':'ventas TTM','discontinuadasTTM':'discontinuadas TTM','menosSBC':'menos SBC','daKe':'da Ke','AOSprecio':'AOS precio'}.items():s=s.replace(a,b)
 # Protected financial-period tokens still need spaces from surrounding prose.
 s=re.sub(r'(?<=[A-Za-záéíóúñ])(?=\x01)',' ',s);s=re.sub(r'(?<=\x02)(?=[A-Za-záéíóúñ])',' ',s)
 s=re.sub(r'(\$[0-9.]+) m\b',r'\1m',s)
 for i,t in enumerate(tokens):s=s.replace('\x01'+chr(0xE000+i)+'\x02',t)
 return s
s=(P/'report.md').read_text();new=tidy(s)
assert re.findall(r'\d+(?:[.,]\d+)*',s)==re.findall(r'\d+(?:[.,]\d+)*',new)
(P/'report.md').write_text(new)
m=json.load(open(P/'publication.json'))
for k in ['pros_es','cons_es','pros_en','cons_en','decision_es','decision_en']:
 m[k]=[tidy(t) for t in m[k]] if isinstance(m[k],list) else tidy(m[k])
m['editorial_version']='v2, 2026-11-04 17:00 UTC; spacing only, same numerical model and research cutoff'
json.dump(m,open(P/'publication.json','w'),indent=2,ensure_ascii=False)
subprocess.run(['pandoc',str(P/'report.md'),'-s','-o',str(P/'report.html'),'--metadata','title=ZWS — revisión fundamental, edición tipográfica v2'],check=True)
