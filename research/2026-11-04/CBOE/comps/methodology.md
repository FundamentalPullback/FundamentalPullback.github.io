# CME and ICE peer screen for CBOE

**Valuation freeze:** 4 November 2026. Prices are the 3 November 2026 regular-session closes. Financial denominators run through 30 September 2026. USD millions except prices, EPS, and multiples. This is a reproducible screening comparison, not a median-based CBOE price target, and not a bank valuation.

## Read first

| Peer | Close | TTM net revenue | TTM GAAP EBIT | EBIT margin | EV / GAAP EBIT | EV / net revenue | GAAP P/E* |
|---|---:|---:|---:|---:|---:|---:|---:|
| CME | $304.06 | $6,972.3m | $4,577.8m | 65.66% | 24.10x | 15.82x | 24.92x |
| ICE | $170.93 | $10,912.0m | $5,703.0m | 52.26% | 20.83x | 10.88x | 23.29x |

*P/E uses the FY-plus-YTD-minus-prior-YTD reported diluted EPS approximation, not net income divided by the current quarter's share count. Both GAAP P/Es contain nonoperating investment gains and should not be read as normalized multiples. Mechanical EBITDA, share-count and prefunding sensitivities are in comps.json and comps.csv.

CME is the closer derivatives-market peer. ICE's data and mortgage platforms, different acquisition history, much higher financing leverage and pending MarketAxess acquisition make it a secondary peer. These two companies cannot establish a fair CBOE target multiple by themselves. A premium or discount requires CBOE-specific growth, index-option economics, capital needs and competitive evidence. No consensus forecasts or forward multiples are claimed.

## Reproduce and audit

Run `python comps.py` in this directory. Standard-library Python only; no network calls. **Only comps.py and comps_inputs.json are required. No full filings, private source directory, or prior output files are needed.** Output is comps.json, comps.csv and qa.json. The default public/offline mode performs 49 checks, including net-revenue bridges, equal clearing asset/liability exclusions, no fabricated exact-date capitalization, source URLs, and recorded provenance-hash formatting.

For another output directory, use `python comps.py --output-dir /path/to/output`. Default inputs remain beside the script. Every source has an exact URL. Period inputs and capitalization fields cite source IDs in comps_inputs.json. Previously recorded source SHA-256 hashes are input provenance metadata and are copied into comps.json; their presence does not assert that the original documents were reopened during reproduction. The public package deliberately does not redistribute full filings.

Optional private source verification is available with `python comps.py --verify-private-sources /path/to/private/source/archive --output-dir /path/to/private-check-output`. This explicitly requested mode also checks the archived filenames against the recorded hashes. It is never a prerequisite for default calculation, and it does not fetch anything. Missing private sources fail only this optional mode. Public offline QA is distinct from document availability or an independent forensic audit of issuer accounting.

**Packaging regression check:** copied only the comps directory into an isolated temporary directory with no sibling sources directory, removed generated outputs, and reran the script. JSON, CSV and public QA reproduced byte-for-byte. Numerical inputs and peer valuations are unchanged by this packaging fix.

## Denominator policy

- TTM = FY2025 + nine months 2026 minus nine months 2025. No annualization of Q3 and no mix of FY2025 and Q3-only denominators.
- CME revenue is reported GAAP revenue, already reflecting its applicable transaction-fee presentation. ICE revenue deducts both Section 31 fees and cash liquidity/routing/clearing payments from gross revenues. The ICE arithmetic is checked for all three TTM building blocks.
- Main EBIT is reported GAAP operating income. **No normalization adjustments are made.** SBC, acquired-intangible amortization, restructuring, legal costs and recurring acquisition/integration activity remain expenses. This is deliberately more conservative than management's adjusted EBIT.
- D&A is separately recorded. Supplemental mechanical EBITDA = GAAP EBIT + all reported D&A. For ICE, acquired amortization comes from the release reconciliation and other D&A is the residual from total D&A; those components sum back to the GAAP statement. This presentation does not relabel amortization addbacks as EBIT or cash earnings.
- Normalized EBIT equals GAAP EBIT. If the parent adds a specific, evidenced CBOE one-off, present that adjustment explicitly and do not compare management-adjusted CBOE EBIT against an unlabeled GAAP peer denominator.
- Net revenue and EBIT are not perfectly fee-only: ICE includes net interest income and fees on certain clearing collateral in OTC/Other; CME puts investment/clearing-collateral income below operating income. ICE does not quantify the necessary standalone reclassification in this packet. That residual mismatch is a limitation, not an invented adjustment.
- Neither EBIT multiple is a fully isolated fee-business enterprise multiple. Strategic investments contribute equity value, while their equity-method/fair-value results are outside EBIT. No book value is silently substituted for fair value to remove them. A fee-business FCFF valuation would require a separate investment and regulatory-capital bridge.

## Capital and share-count policy

Primary EV = closing price × Q3 diluted weighted-average shares + carrying debt + finance lease liabilities + book noncontrolling interests + redeemable noncontrolling interests − unrestricted cash + reserved pass-through fees. Operating lease debt is not added because EBIT includes rent. This convention is explicitly labeled as a screening EV, not actual market capitalization or a debt-at-fair-value takeover valuation.

**CME**

- $155,179.7m of performance-bond/guaranty cash and the identical liabilities are excluded entirely. They are not corporate debt and do not support shareholder cash distributions.
- Only $2,198.5m of reported non-restricted corporate cash is netted. The release's approximately $2.4bn headline includes $225m deposited with FICC in other current assets; that $225m is **not** netted.
- Other restricted cash of $3.5m is not netted. $131m of marketable securities is also conservatively excluded: the annual filing explains that non-qualified compensation-plan assets have offsetting obligations. No unverified securities surplus is treated as distributable.
- Debt is $3,425.1m carrying value plus $44.0m of finance-lease liabilities. No preferred-equity amount is added after the preferred conversion.
- DCO and DCM requirements include capital equivalent to at least one year's projected operating expense and qualifying liquidity equivalent to at least six months. The filing says the company is compliant. A full legal-entity excess-capital calculation is unavailable here. The cash offset is an accounting convention, not a claim that every dollar can be paid out.

**ICE**

- Exclude $113,274m of client margin/guaranty cash and the matching liabilities, plus $2,811m of invested deposits/delivery/unsettled-margin assets and matching liabilities.
- Reported unrestricted cash is $936m. Reserve the $94m Section 31 payable because the 10-Q says collections enter cash before remittance. Net $842m against debt rather than treating the pass-through amount as shareholder cash.
- Exclude all $4,486m of non-client restricted cash and $1,141m of restricted investments from the primary cash offset. Own guaranty-fund/SITG and regulatory resources remain invested, not distributable excess cash.
- ICE separately holds approximately $3.7bn of restricted MarketAxess debt proceeds. The sensitivity subtracts **only that identified acquisition-prefunding amount** from primary EV. It is a matching financing-asset sensitivity, not a release of regulatory capital or a cash distribution. The source is rounded to $0.1bn, so the sensitivity is approximate. It lowers EV/EBIT from 20.83x to approximately 20.18x. The primary EV retains the gross debt because the cash is restricted.
- Debt is $23,304m carrying value. Add $48m book NCI and $30m redeemable NCI to match consolidated EBIT. Book NCI is a proxy, not a fair-value appraisal. No finance lease amount is separately identified in this packet.
- The $2.0bn MarketAxess term loan was undrawn at September 30 and is not added as existing debt. Strategic equity/equity-method investments of $2,994m book value are not netted from EV because book value is not fair value.

**Shares and date mismatch**

- Primary market caps are explicitly **price × Q3 diluted weighted-average share proxies**: 358.641m CME shares and 563m ICE shares. They are not actual market caps on November 3.
- Also show capitalization using the filing cover's dated actual outstanding counts: CME 357.930746m Class A plus 0.003138m Class B on October 14; ICE 558.858412m on October 26. Combining those counts with November 3 price is still a dated-count estimate, not a verified November 3 actual capitalization. The exact-date market-cap field remains null.
- Balance-sheet cash/debt remain September 30 amounts. Post-quarter cash generation, repurchases, dividends and security issuance between that date and November 3 are not rolled forward without evidence. Buyback authorizations are not assumed executed.

## Earnings and post-balance-sheet events

- CME FY2025 includes a $306.1m OSTTRA disposal gain in investment income. The TTM ends September 2026, so the gain remains in TTM net income. It is outside EBIT. No tax-adjusted P/E is fabricated.
- CME's 4.584m preferred shares converted on March 5, 2026. Q3 diluted shares and the October 14 cover count already reflect the conversion. Earlier-period EPS allocation is retained as reported.
- ICE YTD2026 includes $452m investment fair-value gains versus $35m in YTD2025. P/E is therefore not an underlying earnings metric. Investment gains are outside GAAP EBIT.
- ICE's roughly $6.0bn equity-value/$167-per-share MarketAxess agreement remains pending. HSR early termination occurred October 21, 2026. **MarketAxess shareholders approved the merger October 29**, as confirmed in the target's later 8-K. Expected closing is Q1 2027, subject to remaining conditions and regulatory approvals. Do not call shareholder approval pending or treat the deal as completed.
- September debt already contains acquisition prefunding, but the TTM operating denominator excludes MarketAxess. No synergy, purchase accounting or pro forma earnings are added. The optional prefunding sensitivity does not solve all future deal-related comparability differences.
- No additional completed material capital event was established by the targeted public-source review through November 4. This is not a claim that no event occurred; September capitalization remains stale by design.

## Sources

- [CME Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1156375/000115637526000068/cme-20260930.htm): statements; cover share count; cash, clearing, lease and regulatory-resource disclosures.
- [CME Q3 2026 release](https://www.sec.gov/Archives/edgar/data/1156375/000115637526000065/exhibit9919302026.htm): latest results, FICC cash deposit and preferred conversion.
- [CME FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1156375/000115637526000009/cme-20251231.htm): annual TTM base, OSTTRA gain and deferred-compensation investments.
- [ICE Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1571949/000157194926000015/ice-20260930.htm): statements, margin balances, financing and corporate investments.
- [ICE Q3 2026 release](https://www.sec.gov/Archives/edgar/data/1571949/000110465926119880/tm2628301d1_ex99-1.htm) and [FY2025 release](https://www.sec.gov/Archives/edgar/data/1571949/000110465926010646/tm264989d1_ex99-1.htm): annual/YTD statements and acquired-amortization reconciliation.
- [MarketAxess October 29 vote 8-K](https://www.sec.gov/Archives/edgar/data/1278021/000119312526437772/mktx-20261029.htm): shareholder approval and remaining deal conditions.
- [CME price history](https://stockanalysis.com/stocks/cme/history/) corroborated by [ChartExchange CME](https://chartexchange.com/symbol/nasdaq-cme/historical/); [ICE price history](https://chartexchange.com/symbol/nyse-ice/historical) corroborated by a [Yahoo history search snapshot](https://finance.yahoo.com/quote/ICE/history/). Price feeds are secondary; financials are primary SEC/issuer evidence. A later Yahoo full-page open returned rate limiting, so no successful full-page fetch is claimed.
