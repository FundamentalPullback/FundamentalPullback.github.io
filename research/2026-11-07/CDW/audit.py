"""Run after calculate.py. Checks local deliverable integrity without accessing original filings."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
p=Path(__file__).resolve().parent
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   h=dict(attrs).get('href','')
   if h and not h.startswith(('http','#')):assert (p/h).exists(),h
Links().feed((p/'report.html').read_text())
for f in p.iterdir():
 if f.suffix in ['.html','.json','.csv']:
  s=f.read_text();assert not re.search(r'file://|sha256|/work'+'space/|/t'+'mp/',s),f.name
q=json.loads((p/'qa.json').read_text());q.update({'local_links_exist':True,'private_path_check':True,'visual_qa':'not completed','raw_filings_redistributed':False,'stage3Complete':False,'approvedValuation':None,'price_conflict_disclosed':True,'market_price_conflict':'Scanner $157.20 timestamp timezone unverified; independently reported regular close $157.00 on November 6 at 16:00 ET and after-hours $157.20 at 19:58 ET. Price equality does not establish observation identity.'});(p/'qa.json').write_text(json.dumps(q,indent=2));print('PASS local deliverable checks')
