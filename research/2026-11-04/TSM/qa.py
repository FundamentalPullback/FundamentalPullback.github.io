import json,pathlib,math
P=pathlib.Path(__file__).parent;d=json.loads((P/'analysis.json').read_text());h=json.loads((P/'history/history.json').read_text());pub=json.loads((P/'publication.json').read_text());r=(P/'report.md').read_text();checks=[]
def ck(x,n):assert x,n;checks.append(n)
for k in ['base','bear','bull','owner_fcf_ttm','fully_reconciled_equity_bridge','quarterly_earnings_date']:ck(d[k] is None,k+' explicitly null')
for k in ['base','bear','bull','buy_ceiling']:ck(pub[k] is None,'publication '+k)
for k in ['pros_es','cons_es']:
 for s in pub[k]:ck(s in r,'exact evidence: '+s[:60])
for k in ['pros_en','cons_en']:
 for s in pub[k]:ck(s in (P/'english_evidence.md').read_text(),'English evidence')
for k in ['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2026Q3','TTM2025Q3']:
 a=h['periods'][k];ck(abs(a['cfo']-a['capex_ppe']-a['fcf_ppe_only_reported_cfo'])<.01,k+' gross spread');ck(abs(a['ebit']/a['revenue']-a['operating_margin'])<1e-10,k+' margin')
for k in ['capex_intangibles','sbc','lease_principal']:ck(h['periods']['TTM2026Q3'][k] is None,k+' not zero')
ck(d['current_bank_noncurrent_debt'] is None,'no guessed bank debt')
ck(d['current_capital']['cash']+d['current_capital']['current_marketable_instruments']==4016979,'cash instruments')
ck(not pub['approved_entry'] and not pub['stage35_approved'],'no entry')
ck(d['diagnostics']['adr_equivalent_weighted_millions']==5186.4,'ADR factor')
ck(d['price_usd']==404.8 and d['scanner_price']==431,'price dates separate')
(P/'qa.json').write_text(json.dumps({'status':'PASS','checks':len(checks),'details':checks},indent=2)+'\n');print('PASS',len(checks))
