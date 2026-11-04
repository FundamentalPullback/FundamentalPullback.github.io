import urllib.request,concurrent.futures,pathlib,json,lxml.html
base=pathlib.Path(__file__).parent
src={
'FY2024_RELEASE':'https://www.vfc.com/news/press-release/1834/vf-corporation-reports-fourth-quarter-revenue-and-earnings',
'FY2026_10K':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000030/vfc-20260328.htm',
'Q2FY2027_10Q':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000135/vfc-20260926.htm',
'Q1FY2027_10Q':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000114/vfc-20260627.htm',
'Q3FY2026_10Q':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000011/vfc-20251227.htm',
'Q2FY2026_10Q':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-25-000060/vfc-20250927.htm',
'Q2FY2025_10Q':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-24-000030/vfc-20240928.htm',
'DICKIES_RECAST':'https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-25-000066/vfcex992supplementalfininf.htm',
'Q3FY2026_RELEASE':'https://www.vfc.com/investors/news-events-presentations/press-releases/detail/1863/vf-corporation-progressed-on-transformation-in-its-third',
'FY2026_RELEASE':'https://www.vfc.com/investors/news-events-presentations/press-releases/detail/1866/vf-corporation-returns-to-revenue-growth-for-the-full-year',
'Q2FY2027_RELEASE':'https://www.vfc.com/investors/news-events-presentations/press-releases/detail/1872/vf-corporation-exceeds-guidance-in-second-quarter-fiscal'
}
(base/'sources.json').write_text(json.dumps(src,indent=2))
def fetch(k,u):
 p=base/'raw'/f'{k}.html'
 if not p.exists():p.write_bytes(urllib.request.urlopen(u).read())
 tree=lxml.html.fromstring(p.read_bytes())
 for e in tree.xpath('//script|//style'):e.drop_tree()
 # readable lines with table cells one line
 lines=[]
 for e in tree.xpath('//p|//tr|//div[not(div) and not(table) and not(p)]'):
  if e.tag=='tr':txt=' | '.join(' '.join(x.text_content().split()) for x in e.xpath('./td|./th'))
  elif e.xpath('ancestor::table'):continue
  else:txt=' '.join(e.text_content().split())
  if txt:lines.append(txt)
 (base/'raw'/f'{k}.txt').write_text('\n'.join(lines))
 # tables detailed, stripped symbol columns preserved
 tabs=[]
 for i,t in enumerate(tree.xpath('//table')):
  rows=[[' '.join(c.text_content().split()) for c in tr.xpath('./td|./th')] for tr in t.xpath('./tr|./tbody/tr')]
  tabs.append({'table':i,'rows':rows})
 (base/'raw'/f'{k}_tables.json').write_text(json.dumps(tabs,indent=2))
 return k,len(p.read_bytes()),len(tabs)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for result in ex.map(lambda kv:fetch(*kv),src.items()):print(result)
