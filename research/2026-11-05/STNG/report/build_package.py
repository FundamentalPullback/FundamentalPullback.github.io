from pathlib import Path
import json, hashlib, datetime, html
ROOT=Path(__file__).resolve().parent.parent
R=json.loads((ROOT/'model/results.json').read_text());A=json.loads((ROOT/'model/analysis.json').read_text());B=R['base'];G=B['gordon'];P=B['bridge']
Q3='https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/q32026earnings-exhibit991.htm'
AR='https://www.sec.gov/Archives/edgar/data/1483934/000148393426000021/stng-20251231.htm'
ledger=[
('S01','reported','Q3 2026 earnings release','2026-10-28',Q3,'Hull count, delivery windows, Q4 TCE coverage and days, operating costs, cash, shares, commitments; archived q3_table_00..18.'),
('S02','reported','FY2025 Form20-F','2025-12-31',AR,'25-year life, drydock intervals, taxes, management fees, restricted stock, historical pool/spot TCE; sources/2025_clean.txt and old 2025.html.'),
('S03','reported','Nov4 stock closing price','2026-11-04','https://stockanalysis.com/stocks/stng/history/','85.05USD close16:00EST, volume894555; old price.txt/html. ScannerLast85.1297 is a different snapshot.'),
('S04','reported','US Treasury daily yield curve','2026-11-04','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','10-year4.90%; sources/wacc_primary.json and wacc_find.json.'),
('S05','web_research','Damodaran implied ERP','2026-11-01','https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm','Adjusted payout implied ERP4.41%; different date than Treasury; not a guaranteed forward return.'),
('S06','web_research','Damodaran US industry betas','2026-01','https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html','Marine unlevered cash-corrected0.66; broad transportation0.71. Not pure-tanker matched beta.'),
('S07','reported','2031 convertible indenture','2026-04','https://www.sec.gov/Archives/edgar/data/1483934/000114036126014289/ef20070255_ex4-1.htm','605m principal;1.75%; initial9.9615 shares/$1000 in indenture; current10.0791 adjustment from Q3 S01. Settlement choices; no principal+derivative+full dilution double deduction.'),
('S08','reported','September insider equity award Form4','2026-09-28','https://scorpiotankers.gcs-web.com/static-files/aad420ec-b94c-4fe2-b98d-bec3d0bd83f8','240495 awarded common shares,873162 unvested shares; TableI, not additional derivative awards. sources/new_filings.json.'),
('S09','reported','July director Form4','2026-07-13','https://scorpiotankers.gcs-web.com/static-files/c32faddf-36dc-44a2-8cfb-4fb76bfde05a','15834 common shares include7500 described as RSUs; TableII empty. Do not mechanically add them to reported outstanding.'),
('S10','web_research','Volare quoted share price','2026-11-04','https://markets.ft.com/data/equities/tearsheet/summary?s=VLCC:OSL','Nov4 NOK164.60 search snapshot; 2.4mshares. Stockquote is indicative, not executable price; sources/capital_search.json.'),
('S11','reported','Norges Bank exchange rate','2026-11-04','https://www.norges-bank.no/en/topics/Statistics/exchange_rates/','USDNOK9.2278 search snapshot; Volare USD42.81m. Indicative mark, cost38.4m alternative.'),
('S12','reported','2022 annual report historical spot TCE','2022-12-31','https://www.sec.gov/Archives/edgar/data/1483934/000148393423000028/stng-20221231.htm','2021–22 pool/spot rates; old annual2022.txt/tables.'),
('S13','reported','2023 annual report historical spot TCE','2023-12-31','https://www.sec.gov/Archives/edgar/data/1483934/000148393424000025/stng-20231231.htm','2023 spot MR31258,LR239486,Handy29578; searched primary source and annual history.'),
('S14','reported','TORM audited research inputs','2026-11-04','https://investors.torm.com/financials/quarterly-results/default.aspx','Read-only peer inputs from trmd_completion_20261104; TTM EBIT ex sale gains788.3, principal+leases1150.3, unrestrictedcash446.2,102.7mperiodshares,37.62close. Not a TORM fair-value model.'),
('S15','analyst_estimate','Fleet valuation assumptions','2026-11-05','', 'model/assumptions.json: scenario TCE paths,2% inflation, drydock cycles, replacement prices/scrap, working cash, risk premia and taxes. Explicitly not company guidance.'),
('S16','derived','Deterministic fleet engine and reverse valuation','2026-11-05','', 'model/build.py, analyze.py, results.json, analysis.json. First five detailed2027–31, five transition2032–36, exact age-adjusted terminal tail. Independent arithmetic and economic review completed; no Stage 3 approval. See independent_audit.md.')]
D=[dict(id=i,label=l,source=s,date=d,url=u,usage=n) for i,l,s,d,u,n in ledger]
(ROOT/'sources/source_ledger.json').write_text(json.dumps(D,indent=2,ensure_ascii=False))
# Additional decision-focused sensitivities that do not change the engine.
extras={'current_price':85.05,'market_cap':51.078851*85.05,'base_value':B['per_share'],'bull_coherent_conversion':R['bull']['physical_conversion'],'cash_timing_v2':'Matched September30 balance with full Q4 forecast; October Volare purchase deducted separately. Oct26cash only crosscheck.','working_capital_50m_error_per_share':50/P['shares'],'claim_100m_error_per_share':100/P['shares'],'volare_cost_instead_of_mark_value':B['per_share']+(38.4-P['volare'])/P['shares'],'peer_simple_principal_ev':{'STNG':51.078851*85.05+655-2051.865,'TRMD':102.7*37.62+704.1},'peer_ev_ebit_ex_gains':{'STNG':(51.078851*85.05+655-2051.865)/601.88,'TRMD':(102.7*37.62+704.1)/788.3},'terminal_vintage_rollforward':G}
replacement_pv=sum(r['replacement']/(1+B['assumptions']['wacc'])**(r['period_mid']-(2026+307/365.25)) for r in B['rows'])
extras['future_replacement_payment_timing']={'replacement_capex_pv':replacement_pv,'one_year_earlier_value':B['per_share']-replacement_pv*.10/P['shares'],'one_point_five_years_earlier_value':B['per_share']-replacement_pv*((1.10)**1.5-1)/P['shares'],'assumption':'Only future discretionary replacement capex shifts earlier; deliveries and scrap unchanged. Current newbuild commitments retain reported timing.'}
(ROOT/'model/decision_sensitivities.json').write_text(json.dumps(extras,indent=2))
print('Source ledger and decision sensitivities saved.')
