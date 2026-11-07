import json,pathlib
p=pathlib.Path(__file__).parent
sources=[
('calendar','Recruit Holdings IR events','2026-11-07','https://recruit-holdings.com/en/ir/events/','Confirm Nov 11 earnings'),
('q1','Q1 FY2026 IFRS earnings release','2026-08-07','https://recruit-holdings.com/en/ir/library/upload/Recruit_202703Q1_earnings_en.html','Q1 statements, cash, capital, guidance'),
('summary','FY2026 Q1 Financial Results Summary','2026-08-07','https://recruit-holdings.com/en/ir/library/upload/Recruit_202703Q1_summary_en.html','Segment growth and monetization'),
('call','FY2026 Q1 earnings call transcript (page heading says FY2027)','2026-08-07','https://recruit-holdings.com/en/ir/library/upload/Recruit_202703Q1_call-transcript_en.html','Management commentary and antitrust risk'),
('annual','FY2025 IFRS earnings release','2026-05-15','https://recruit-holdings.com/en/ir/library/upload/Recruit_202603Q4_earnings_en.html','Prior full-year baseline and perimeter'),
('buyback','Status of Share Repurchases','2026-11-02','https://recruit-holdings.com/en/newsroom/20261102_0001/','Executed purchases versus authority'),
('extension','Repurchase period extension','2026-10-14','https://recruit-holdings.com/en/newsroom/20261014_0001/','Repurchase end date'),
('adr','Deutsche Bank Recruit ADR directory','2026-11-07','https://adr.db.com/drwebrebrand/dr-universe/dr_details.html?identifier=10994','Ratio, identifiers, unsponsored OTC, sector'),
('actions','Citi Recruit corporate actions','2026-11-02','https://depositaryreceipts.citi.com/adr/notices/pgm_dispCA.aspx?cusip=75629J101&pageId=15&subpageID=112','Ratio cross-check; empty notice list not exhaustive assurance'),
('ordinary','FT Recruit historical prices','2026-11-06','https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=6098%3ATYO','JPY ordinary close'),
('fx','Bank of Japan Foreign Exchange Rates','2026-11-06','https://www.boj.or.jp/en/statistics/market/forex/fxdaily/fxlist/fx261106.pdf','17:00 JST spot range'),
('quote','Yahoo Finance RCRUY quote','2026-11-06','https://finance.yahoo.com/quote/RCRUY/','USD close and conflicting volume'),
('volume','Deutsche Bank Recruit ADR trading data','2026-11-06','https://adr.db.com/drwebrebrand/dr-universe/dr_details.html?identifier=10994','November 6 volume 2,057,647; conflicts with Yahoo'),
('release_time','Recruit Holdings Investor Relations','2026-11-07','https://recruit-holdings.com/en/ir/','November 11 results at 15:30 JST'),
('call_time','Recruit Holdings Earnings Results Call Webcast','2026-11-07','https://recruit-holdings.com/en/ir/events/live/','November 11 call at 16:30 JST'),
('restructuring','HR Technology Workforce Reduction','2025-07-11','https://recruit-holdings.com/en/newsroom/20250711_0001/','Historical cost restructuring context'),
('perimeter','Changes in Group Governance Structure','2024-09-09','https://recruit-holdings.com/en/newsroom/20240909_0001/','Japan HR Solutions transfer')]
(p/'sources.json').write_text(json.dumps([dict(id=i,title=t,date=d,url=u,purpose=r) for i,t,d,u,r in sources],indent=2))
x={'as_of':'2026-11-07','status':'bounded_pre_earnings_preparation_not_approved','currency':'JPY','financial_units':'billions unless shares or EPS','event':'2026-11-11T15:30:00+09:00','adrs_per_ordinary':5,'price_adr_usd':22.01,'price_date':'2026-11-06','ordinary_jpy':17000,'fx_jpy_per_usd_tokyo_1700_mid':157.95,'q1_FY2026':{'revenue':1045.3,'operating_income':255.4,'net_income_parent':202.618,'cfo':203.657,'ppe_purchase':1.779,'intangible_purchase':13.119,'lease_principal':10.660,'sbc_expense':20.540,'cash_equivalents':853.046,'borrowings':.658,'lease_liabilities':178.169,'retirement_liability':60.004,'issued_shares':1472504149,'treasury_including_trust':80332780,'weighted_basic_shares':1392734530},'FY2025':{'revenue':3697.3,'operating_income':630.5,'net_income_parent':496.9,'basic_eps':349.78},'guidance_Aug7_FY2026':{'revenue':4230,'operating_income':945,'net_income_parent':755,'basic_eps':543,'sbc':78.9},'buybacks_through_Oct31':{'shares':16384200,'jpy':178135923900,'authority_jpy':350000000000},'volume_20_sessions':None,'bid_ask_spread':None,'valuation':None,'price_target':None}
a=x['q1_FY2026'];derived={'cfo_less_ppe_and_intangibles':round(a['cfo']-a['ppe_purchase']-a['intangible_purchase'],3),'cash_after_lease_principal':round(a['cfo']-a['ppe_purchase']-a['intangible_purchase']-a['lease_principal'],3),'illustrative_after_SBC_charge':round(a['cfo']-a['ppe_purchase']-a['intangible_purchase']-a['lease_principal']-a['sbc_expense'],3),'cash_less_borrowings_not_excess_cash':round(a['cash_equivalents']-a['borrowings'],3),'ordinary_excluding_treasury_including_trust':a['issued_shares']-a['treasury_including_trust'],'non_synchronous_ADR_parity_usd':17000/157.95/5,'non_synchronous_ADR_difference_percent':(22.01/(17000/157.95/5)-1)*100,'ordinary_forward_PE_guidance':17000/543}
(p/'inputs.json').write_text(json.dumps(x,indent=2));(p/'derived.json').write_text(json.dumps(derived,indent=2))
assert derived['cfo_less_ppe_and_intangibles']==188.759
assert derived['cash_after_lease_principal']==178.099
assert x['valuation'] is None and x['volume_20_sessions'] is None
assert derived['ordinary_excluding_treasury_including_trust']==1392171369
(p/'qa.json').write_text(json.dumps({'status':'PASS for bounded preparation only','tests':['Cash arithmetic ties','ADR uses division by five','No target or approval','20-day volume unknown not passed','All source entries public URLs'],'limitations':['No complete three-year/four-quarter/TTM review','No full corporate-action-history assurance','No executable parity comparison','No remote publication performed']},indent=2))

# Public packaging includes only original research and derived inputs.
import zipfile
paragraphs=(p/'report.md').read_text().split('\n\n')
selectors={'pros':['HR Technology Q1','Q1 FY2026 ended','Executed buybacks'],'cons':['Management attributes','Liquidity is unresolved','Cash equivalents were','The ADR close was']}
mapping={k:[q for q in paragraphs if any(q.startswith(a) for a in v)] for k,v in selectors.items()}
(p/'pros_cons_evidence.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False))
files=['report.md','summary_en.txt','summary_es.txt','inputs.json','derived.json','sources.json','qa.json','pros_cons_evidence.json','build_package.py']
manifest={'title':'Recruit Holdings bounded pre-earnings research','as_of':'2026-11-07','status':'Pending; not approved','contents':files,'scope':'Original analysis, public source references and reproducible calculations; no full filings or source caches'}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(p/'rcruy_pre_earnings_20261107.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in files+['manifest.json']:
        content=(p/name).read_bytes()
        z.writestr(name,content)
