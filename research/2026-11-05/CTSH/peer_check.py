from pathlib import Path
import json
P=Path(__file__).parent
# Selected public market observations; do not use mixed-definition provider EBIT/EV as a target.
o={'as_of':'2026-11-04 regular close','purpose':'P/E cross-check only; not a mechanical target and not a homogeneous EV/EBIT screen','peers':[
 {'ticker':'CTSH','close':65.78,'eps_ttm':5.48,'eps_basis':'Sum four published diluted quarterly GAAP EPS:1.34+1.39+1.36+1.39. Includes current restructuring and India reversal; historic weighted-share denominators differ.','pe':65.78/5.48,'url':'https://stockanalysis.com/stocks/ctsh/history/'},
 {'ticker':'ACN','close':264.27,'eps_ttm':13.56,'eps_basis':'FY2026 GAAP diluted EPS, year endedAugust31; primary Oct1release. Restructuring included.','pe':264.27/13.56,'url':'https://www.sec.gov/Archives/edgar/data/1467373/000146737326000037/q4fy26earnings8-kexhibit.htm'},
 {'ticker':'INFY','close':12.24,'eps_ttm':.83,'eps_basis':'Provider TTM roundedUSD ADR EPS; IFRS and differentquarter/source conventions. Not individually rebuilt allfourquarters.','pe':12.24/.83,'url':'https://stockanalysis.com/stocks/infy/statistics/'}],
 'primary_context':{
 'ACN':'FY2026 revenue74.18bn,+5%localcurrency; GAAPmargin15.4%,adjusted15.8%; FY2027revenueguide3–6%LC. More diversified consulting mix and stronger apparent growth; not a mandatory multiple forCTSH.',
 'INFY':'Q2FY2027 revenue5.145bn,+1.5%CC; margin21%; FYguideCCgrowth1–2%,margin20–22%. Highermargin but lowergrowth/currentpricingpressure; not proofsectorAIupsidesafe.'},
 'quality_warning':'Provider operating-income fields do not match issuer GAAP definitions (e.g.CTSH3.58bn vs3442mGAAP); total debt includes lease treatment. INFYprovider marketcap also lags Nov4close. Therefore no providerEV/EBIT or pooledmultiple is used. All displayedPE recomputed usingNov4regularclose.'}
(P/'peer_check.json').write_text(json.dumps(o,indent=2))
