"""Retrieve selected primary evidence into memory; save only derived tables and short contiguous extracts, never full filings."""
import json,urllib.request,pathlib,re
from lxml import html
P=pathlib.Path(__file__).resolve().parent
ledger=json.loads((P/'source_ledger.json').read_text());out=[]
selectors={
'EPAM 2025 Form 10-K':['Revenues','Income from operations','Net income','Depreciation and amortization expense','Stock-based compensation expense','Net cash provided by operating activities','Purchases of property and equipment','Diluted'],
'EPAM Q3 2026 Form 10-Q':['Common Stock, par value $0.001 per share','Revenues','Income from operations','Net income','Net cash provided by operating activities','Purchases of property and equipment','Contract assets included','Contract liabilities included','Contingent consideration liabilities as of September 30, 2026'],
'EPAM Q2 2026 Form 10-Q':['Revenues','Income from operations','Net cash provided by (used in) operating activities','Purchases of property and equipment'],
'EPAM Q1 2026 Form 10-Q':['Revenues','Income from operations','Net cash provided by (used in) operating activities','Purchases of property and equipment'],
'EPAM Q3 2025 Form 10-Q':['Revenues','Income from operations','Net cash provided by operating activities','Purchases of property and equipment'],
'EPAM Q4 and FY2025 earnings release':['Revenues','Income from operations','Revenue growth as reported','Inorganic revenue','Foreign exchange rates','Revenue growth on an organic constant currency basis'],
}
for s in ledger:
 if s['title'] not in selectors:continue
 raw=urllib.request.urlopen(urllib.request.Request(s['url'],headers={'User-Agent':'Investment research analyst contact research@example.org'})).read()
 t=html.fromstring(raw); rows=[]
 for tr in t.xpath('//tr'):
  cells=[' '.join(x.text_content().split()) for x in tr.xpath('./td')]; line=' | '.join(cells)
  if cells and any(cells[0].startswith(p) for p in selectors[s['title']]):
   # Numeric financial facts and their unchanged contiguous row labels, not narrative reproduction.
   if len(line)<700 and line not in rows:rows.append(line)
 out.append({'source_url':s['url'],'source_title':s['title'],'source_date':s['date'],'table_context':'Columns retain source order. Consult linked filing table headers; annual 2025/2024/2023, quarterly 2026/2025 and YTD 2026/2025 unless noted.','financial_rows':rows})
(P/'primary_financial_evidence.json').write_text(json.dumps(out,indent=2))
print('Saved selected primary financial evidence from',len(out),'sources')
