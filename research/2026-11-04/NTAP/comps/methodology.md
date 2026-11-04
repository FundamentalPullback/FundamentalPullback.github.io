# NTAP valuation comparables

As of **4 November 2026**, using the **3 November regular-session closes**. USD millions except prices and multiples. These are diluted-share EV proxies using the latest reported capital, not verified current enterprise values.

| Company | Close | EV proxy | TTM revenue | GAAP operating EBIT | Normalized operating EBIT | EV/revenue | EV/GAAP EBIT | EV/normalized EBIT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NetApp (NTAP) | $190.78 | 37,186 | 7,391 | 1,849 | 1,838 | 5.03x | 20.11x | 20.23x |
| Everpure (P) | $117.65 | 39,650 | 4,262 | 224 | 230 | 9.30x | 176.85x | 172.73x |
| Hewlett Packard Enterprise (HPE) | $53.10 | 90,815 | 41,871 | 2,602 | 2,862 | 2.17x | 34.90x | 31.73x |

## Interpretation

Everpure, formerly Pure Storage, is the closest listed operating comparison. Its current ticker is **P**, not PSTG. Its 5.4% normalized trailing margin and much faster expected revenue expansion make the very high EBIT multiple a weak valuation anchor for NetApp. HPE competes in enterprise storage, but storage was only 10.6% of its latest quarter's revenue. Its consolidated valuation is driven largely by servers, networking and financing. Neither supports directly transferring a multiple to NTAP. **No peer median or peer-derived price target is calculated.**

NTAP looks less expensive on trailing EBIT, but that does not establish undervaluation. Its margin, growth durability, reinvestment needs and post-July cash use must support its own DCF. The reported fiscal periods differ, including NTAP's 53-week TTM.

## Reproducible calculation and normalization

Run `python comps.py` in this folder. It reads `comps_inputs.json` and rebuilds `comps.json` and `comps.csv` offline. Every period input has source IDs; the JSON contains the source URLs and limitations.

TTM = latest fiscal year + current year-to-date − prior year-to-date. EBIT means **GAAP income from operations**, before non-operating gains/losses. All SBC, recurring R&D and intangible amortization remain expenses.

- **NTAP:** FY2026 + Q1FY2027 − Q1FY2026. Remove the $11m Spot contingent-consideration gain: 1,849 − 11 = 1,838. Retain $397m SBC and $75m restructuring. The provider's 1,924 figure includes a restructuring addback and is not GAAP EBIT.
- **P:** FY2026 + H1FY2027 − H1FY2026. Add only $5.335m specifically identified acquisition transaction expense: 224.210 + 5.335 = 229.545. Retain $549.863m SBC. FY2026 severance of $5.489m occurred in prior H1 and fully rolls out of this TTM, so no severance addback remains.
- **HPE:** FY2025 + 9MFY2026 − 9MFY2025. Primary normalization adds only $260m impairment: 2,602 + 260 = 2,862. Recurring cost programs and broad acquisition/disposition charges remain. A separate, more permissive sensitivity adds $211m cost programs, $638m acquisition/disposition charges and $2m transformation charges, producing 3,713. This reconciles to management's 5,767 non-GAAP EBIT less retained SBC of 795 and amortization of 1,259; it is not the primary measure.

## Capital bridge and stale-balance limits

EV proxy = close × latest quarterly diluted shares + financial debt + other claims + noncontrolling interests − cash − marketable investments. Operating leases are excluded consistently. No operating-cash reserve is deducted from available cash.

- **NTAP:** 200m shares; 3,576 cash/short investments; 2,500 debt principal; 106 acquisition contingent claim. July 31 capital is unchanged. October dividend and later acquisitions are not deducted here. PEAK:AIO closed November 2; its consideration is unestablished, as is the combined post-July cash impact of JetStream and PEAK:AIO. This differs intentionally from the companion DCF's cash reserves and equity adjustments. Actual August 28 common shares were 196.419005m.
- **P:** 345.587m diluted shares versus 333.227251m actual August 31 common shares. August 2 cash 385.694 plus marketable investments 622.197; no outstanding revolver borrowings. Immaterial, unquantified finance leases are omitted. The May 7 1touch purchase for 125.9 cash is already in the balance sheet. Later working-capital movements and repurchases are not estimated.
- **HPE:** 1,449m diluted shares = 1,336m quarterly basic weighted average + 76m mandatory convertible preferred, if-converted + 37m employee-plan dilution, treasury-stock method. Actual August 27 common shares were 1,327.464779m. **No preferred claim is added again.** July 31 cash is 6,216, investments 217, debt carrying value 20,244 and noncontrolling interests 62. Restricted cash is excluded; pension deficits are not valued here.

HPE's debt includes captive-finance funding, while operating earnings deduct financing costs. The supplemental pre-financing-cost ratio is also not a clean industrial storage multiple. The August 1 Telco Solutions sale is after the balance date. Announced consideration was up to 160, including 15 contingent on performance. The separate 0–160 gross-proceeds sensitivity is not an estimate of net cash proceeds and does not restate disposed EBIT. Subsequent dividends also prevent treating July capital as current. Juniper is included for the full current TTM; reported growth is not organic.

## Principal sources

- Everpure [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1474432/000147443226000027/pstg-20260201.htm), [Q2FY2027 10-Q](https://www.sec.gov/Archives/edgar/data/1474432/000147443226000088/pstg-20260802.htm), [Q1 reconciliation](https://investor.everpuredata.com/news-and-events/press-releases/press-release-details/2026/Everpure-Announces-First-Quarter-Fiscal-2027-Financial-Results/default.aspx), [ticker change](https://www.everpuredata.com/company/newsroom/press-releases/everpure-to-change-ticker-symbol.html), [September outlook](https://investor.everpuredata.com/news-and-events/press-releases/press-release-details/2026/Everpures-Expanding-Business-Model-Fuels-New-Long-Term-Outlook/default.aspx).
- HPE [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1645590/000164559025000130/hpe-20251031.htm), [Q3FY2026 10-Q](https://www.sec.gov/Archives/edgar/data/1645590/000164559026000080/hpe-20260731.htm), [Telco closing](https://www.hcltech.com/en-us/press-releases/hcltech-completes-acquisition-hpes-telco-solutions-business), [sale terms, note 2](https://www.hcltech.com/sites/default/files/document/open/quarter-results/2026-01/IFRS_Financials_Dec-25.pdf).
- NTAP [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1002047/000119312526259683/ntap-20260424.htm), [Q1FY2027 10-Q](https://www.sec.gov/Archives/edgar/data/1002047/000119312526380207/ntap-20260731.htm).
- NetApp [PEAK:AIO closing, November 2](https://investors.netapp.com/news/news-details/2026/NetApp-Completes-Acquisition-of-PEAKAIO-to-Accelerate-Zettabyte-scale-AI-Deployments/default.aspx).
- Dated close rows: [NTAP](https://stockanalysis.com/stocks/ntap/history/), [P](https://stockanalysis.com/stocks/p/history/), [HPE](https://stockanalysis.com/stocks/hpe/history/). Peer dated rows cross-checked against FT historical tables. Ignore live November 4 page headers and intraday rows.

QA: offline rebuild, all three TTM bridges, normalization arithmetic, HPE diluted-share components, positive denominators and independent CSV/JSON consistency checked. Complete source ledger is in the JSON files. Raw downloaded filings are not part of this deliverable.
