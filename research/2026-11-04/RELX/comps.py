"""Public-source peer inputs and own calculations; millions in each row's currency.
Run with Python standard library. No external dependencies or private inputs.
"""
import csv,json,pathlib
P=pathlib.Path(__file__).parent
FX=1.1179/.83358
SOURCES={
 'relx_fy25':'https://www.sec.gov/Archives/edgar/data/929869/000110465926017277/relx-20251231xex15d2.htm',
 'relx_h126':'https://www.sec.gov/Archives/edgar/data/929869/000092986926000054/relx-20260723xex99d1.htm',
 'relx_price':'https://stockanalysis.com/stocks/relx/history/',
 'fx':'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html',
 'tri_q326':'https://investors.thomsonreuters.com/news-releases/news-release-details/thomson-reuters-reports-third-quarter-2026-results',
 'tri_recast':'https://investors.thomsonreuters.com/static-files/13453a61-1934-494a-b639-ed45a69dd0e8',
 'tri_fy25':'https://investors.thomsonreuters.com/static-files/d4676c84-359c-42c3-9f84-8c62552d49a2',
 'tri_price':'https://thomsonreuters.gcs-web.com/stock-information/stock-price-performance',
 'tri_price_crosscheck':'https://stockanalysis.com/stocks/tri/history/',
 'fds_fy26':'https://www.sec.gov/Archives/edgar/data/1013237/000162828026066391/fds-20260831.htm',
 'fds_release':'https://www.sec.gov/Archives/edgar/data/1013237/000162828026063888/fdsq42026earningsrelease.htm',
 'fds_price':'https://stockanalysis.com/stocks/fds/history/'
}
rows=[
 dict(ticker='RELX',currency='GBP',price_usd=39.40,usd_per_currency=FX,shares=1794.1,share_basis='H1 2026 diluted weighted average; ADR 1:1',balance_date='2026-06-30',period='TTM 2026-06-30',revenue=9720,ebit=3122,owner_cash=2256,owner_cash_status='Reconstructed after SBC, leases and minorities; includes JV cash dividends',net_debt_reported=8733,leases_in_reported_net_debt=119,nci=17,preferred=0),
 dict(ticker='TRI',currency='USD',price_usd=110.18,usd_per_currency=1,shares=434.017155,share_basis='Q3 2026 diluted weighted average',balance_date='2026-09-30',period='TTM 2026-09-30 continuing operations',revenue=1873+1975+1843+1833,ebit=453+571+498+402,owner_cash=2535-665-61-4-120,owner_cash_status='Continuing CFO-capex-lease principal-preferred dividends-SBC; SBC120 estimate (100-140 range)',net_debt_reported=2747,leases_in_reported_net_debt=228,nci=0,preferred=110),
 dict(ticker='FDS',currency='USD',price_usd=332.59,usd_per_currency=1,shares=35.572,share_basis='Q4 FY2026 diluted weighted average',balance_date='2026-08-31',period='FY ended 2026-08-31',revenue=2476.256,ebit=699.957,owner_cash=822.200-114.720-84.099,owner_cash_status='CFO-capex including software-SBC; operating lease cash already in CFO',net_debt_reported=1375-233.339,leases_in_reported_net_debt=0,nci=0,preferred=0)
]
for r in rows:
 r['price_local']=r['price_usd']/r['usd_per_currency']
 r['equity_proxy']=r['price_local']*r['shares']
 r['net_financial_debt_ex_leases']=r['net_debt_reported']-r['leases_in_reported_net_debt']
 r['ev']=r['equity_proxy']+r['net_financial_debt_ex_leases']+r['nci']+r['preferred']
 r['ev_issuer_debt_basis']=r['equity_proxy']+r['net_debt_reported']+r['nci']+r['preferred']
 r['ev_ebit']=r['ev']/r['ebit'];r['ev_revenue']=r['ev']/r['revenue'];r['p_owner_cash']=r['equity_proxy']/r['owner_cash']
 r['ev_ebit_issuer_debt_basis']=r['ev_issuer_debt_basis']/r['ebit'];r['ev_revenue_issuer_debt_basis']=r['ev_issuer_debt_basis']/r['revenue']
 r['ebit_margin']=r['ebit']/r['revenue']
out={'as_of':'2026-11-03 US regular close; research 2026-11-04','units':'Millions of row currency, except prices and multiples','fx_usd_per_gbp':FX,'peers':rows,'sources':SOURCES,'method':'Price times reported diluted weighted share proxy, not current exchange market cap. Headline EV excludes leases; issuer-debt EV shown separately. No pension, operating cash reserve or speculative transaction adjustment in peer EV. IFRS/GAAP EBIT lease differences remain. No peer-median target.','tri_sensitivity':{'sbc_estimate':120,'owner_cash_range':[1665,1705],'p_owner_cash_range':[rows[1]['equity_proxy']/1705,rows[1]['equity_proxy']/1665],'ebit_normalized':1846,'ev_normalized_ebit':rows[1]['ev']/1846},'fds_subsequent_revolver_borrowing':{'amount':90,'treatment':'Disclosed subsequent to August31 in FY26 10-K; not rolled into stale balance without matching cash/use bridge.'},'qa':{'shares_not_assumed_current':True,'currencies_matched':True,'price_targets_from_peer_medians':False}}
assert round(rows[1]['owner_cash'])==1685 and rows[1]['revenue']==7524 and rows[1]['ebit']==1924
assert abs(rows[2]['owner_cash']-623.381)<1e-6
(P/'peers.json').write_text(json.dumps(out,indent=2))
with (P/'peers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for r in rows:print(r['ticker'],{k:round(r[k],3) for k in ['ev','ev_ebit','ev_revenue','p_owner_cash','ev_ebit_issuer_debt_basis']})
