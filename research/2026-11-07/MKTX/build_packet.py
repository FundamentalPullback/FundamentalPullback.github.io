import json,pathlib,datetime,math
p=pathlib.Path(__file__).parent
sources=[
('S1','MarketAxess Q3 2026 results','2026-10-23','https://investor.marketaxess.com/news/news-details/2026/MarketAxess-Reports-Third-Quarter-2026-Financial-Results/default.aspx','Quarterly financials, declared dividend and withdrawn guidance.'),
('S2','ICE acquisition announcement','2026-07-30','https://ir.theice.com/press/news-details/2026/Intercontinental-Exchange-to-Acquire-MarketAxess-Creating-a-Premier-Fixed-Income-Marketplace/default.aspx','Cash consideration and original expected closing timeline.'),
('S3','ICE Q3 results','2026-10-29','https://s2.q4cdn.com/154085107/files/content_files/3Q26-Earnings-Press-Release_Final.pdf','Page 5: HSR satisfaction, Q1 2027 expectation and remaining conditions.'),
('S4','MarketAxess vote 8-K','2026-10-29','https://www.sec.gov/Archives/edgar/data/1278021/000119312526437772/mktx-20261029.htm','Shareholder approval and voting results.'),
('S5','Definitive merger proxy','2026-09-18','https://www.sec.gov/Archives/edgar/data/1278021/000119312526395678/d171374ddefm14a.htm','Outside date and conditional termination fees.'),
('S6','Merger agreement included with ICE SEC filing','2026-07-30','https://www.sec.gov/Archives/edgar/data/1571949/000119312526324914/d116245ddefa14a.htm','Sections 7.1–7.5 and 8.2: closing conditions, no financing condition and termination rights.'),
('S7','MarketAxess latest 10-Q','2026-11-06','https://www.sec.gov/Archives/edgar/data/1278021/000119312526450679/mktx-20260930.htm','Latest quarterly filing; subsequent merger-vote disclosure. Full financial review is outside this bounded update.'),
('L1','Prior published MKTX reports','2026-11-07',None,'Prior ordinary-entry classification in reports A128 (2 November) and A122 (30 October).'),
('L2','Nov6 scanner export','2026-11-06','https://fundamentalpullback.github.io/data/scan-4552.js','6 November scanner reference price $165.59, QP100 and Opportunity100; not an independently verified exchange closing price.')]
json.dump([dict(zip(['id','title','published','url','purpose'],s)) for s in sources],open(p/'sources.json','w'),indent=2)
price=165.59;offer=167;div=.78
out={'ticker':'MKTX','asOf':'2026-11-07','priceDate':'2026-11-06','price':price,'cashConsideration':offer,'considerationIsFairValue':False,'grossSpreadUSD':offer-price,'grossSpreadPct':100*(offer/price-1),'conditionalOneDeclaredDividendGrossReturnPct':100*((offer+div)/price-1),'assignedProbability':None,'standaloneFairValue':None,'entryApproved':False,'newShares':0,'timingScenarios':[]}
for day in ['2027-01-31','2027-03-31','2027-06-30','2027-07-29']:
 d=(datetime.date.fromisoformat(day)-datetime.date(2026,11,6)).days
 out['timingScenarios'].append({'illustrativeCloseDate':day,'calendarDays':d,'noDividendAnnualizedConditionalPct':100*((offer/price)**(365/d)-1),'withOneDividendAnnualizedConditionalPct':100*(((offer+div)/price)**(365/d)-1)})
out['limitations']='Conditional mechanical returns, not expected returns; no close probability, timing forecast, taxes, fees, funding, slippage, or reinvestment assumed. Dividend receipt requires actual entitlement; further dividends are not assumed. No break price estimated.'
json.dump(out,open(p/'derived_event_math.json','w'),indent=2)
assert math.isclose(out['grossSpreadUSD'],1.41,abs_tol=1e-8)
assert all(x['calendarDays']>0 for x in out['timingScenarios'])
assert out['standaloneFairValue'] is None and not out['entryApproved']
(p/'qa.json').write_text(json.dumps({'arithmetic':'PASS','sourceChronology':'PASS: Oct29 vote supersedes Oct23 approval-pending wording; Q1 replaces H1 expectation','existingResearch':'PASS: refresh not initiation','eventVersusFundamental':'PASS: offer not fair value; no probability or entry','fullStage3':'NOT COMPLETED; deliberately bounded event refresh','publicWhitelist':['report.md','sources.json','derived_event_math.json','build_packet.py','qa.json','summary.json','manifest.json']},indent=2))
print(json.dumps(out,indent=2))
