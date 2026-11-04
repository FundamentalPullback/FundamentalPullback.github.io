# CRM / WDAY comparison for NOW research

Cutoff: 4 November 2026; prices strictly 3 November regular close. USD millions, shares millions. Research screen, not a current fully normalized acquisition-perimeter valuation. No peer median or implied NOW price target is warranted.

## Reproducible results
Run `python build_comps.py` in this directory. Only Python standard library and inputs.json are needed; full filings are excluded from this portable folder. outputs.json is generated rather than pasted. Source URLs in sources.json; statement tie-outs below.

| Peer | Price | Cover shares and date | TTM GAAP EBIT | Acquired amortization | EBIT before acquired amortization | EV July balance screen | EV/GAAP EBIT | EV/EBIT before acquired amortization |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| CRM | 222.20 | 823; Aug 20 | 8,735 | 1,995 | 10,730 | 211,600.60 | 24.22x | 19.72x |
| WDAY | 197.94 | 241; Aug 25 | 1,085 | 134 | 1,219 | 47,300.54 | 43.59x | 38.80x |

Cover shares are approximate actual shares outstanding, not current diluted ownership. WDAY includes both A and B. Q2 diluted weighted-average share sensitivity: CRM 821 gives 24.17x/19.68x; WDAY 246.307 gives 44.56x/39.66x. Different measurement bases must not be mixed silently. Repurchases, issuances and CRM ASR final settlement make November shares uncertain; final ASR settlement was expected in October, not verified here. A quarterly diluted average is not intrinsically conservative.

## Definition and source tie-out
TTM through July 2026 = FY January 2026 + H1 July 2026 − H1 July 2025. Both latest interim statements contain prior H1 comparatives. GAAP operating income is EBIT, excluding investment gains and financing interest. SBC, restructuring and all other operating costs remain expensed in BOTH multiples. Only specifically acquired-intangible amortization is added back in the second denominator, not all D&A and not deferred-commission amortization. It is not issuer non-GAAP operating income and does not claim acquisitions are costless.

- CRM FY 10-K statements: EBIT 8,331; acquired-amortization cost of revenue 692 plus sales/marketing 995 = 1,687. H1 10-Q: EBIT 4,678/4,274; acquired amortization 478+605=1,083 / 312+463=775. TTM EBIT 8,735; amortization 1,995. Revenue FY 41,525 +22,478−20,065=43,938.
- WDAY FY 10-K statements and Note 7: EBIT 721; acquired amortization 106. H1 10-Q statements and Note 7: EBIT 651/287; amortization 70/42. TTM EBIT 1,085; amortization 134. Revenue 9,552+5,191−4,588=10,155. Annual bridge avoids adding separately rounded quarterly numbers.
- CRM July 10-Q debt note: principal 39,500 (carrying value 39,288). Cash 8,310 + marketable 3,093. Finance lease liability 633 is outside debt and is ADDED. Strategic investments of 11,324 are NOT cash equivalents and are not subtracted.
- WDAY July 10-Q: principal 3,000 (carrying 2,989); cash 661 + marketable 2,742. No separate finance-lease amount identified: zero addition is an explicitly limited screen assumption, not verified absence.

EV = price × cover shares + debt principal + finance leases − cash − marketable securities. Principal rather than amortized carrying debt avoids treating issuance discounts as free equity value. We deduct all reported financial cash, with no assumed operating reserve; an operating reserve would raise EV. No independent non-controlling interest or preferred claim was identified in these statements.

## US GAAP lease treatment
Do not mechanically add operating lease liabilities to these EVs: operating lease expense is already inside GAAP EBIT. CRM operating leases 2,455 and WDAY 783 are excluded under this rent-expensed convention. Finance leases differ: CRM 633 is debt-like, with depreciation remaining in EBIT and lease interest below it. If comparing to an IFRS 16 issuer or a rent-adjusted multiple, normalize BOTH numerator and denominator. Uncommenced commitments are not existing financing debt.

## Current-period limitations that affect use
1. CRM completed Contentful September 1 and Fin September 10, verified on issuer releases. July 10-Q agreed cash considerations were approximately 1,500 and 3,600. Final consideration adjustments, target cash/debt and incremental TTM earnings are not in the July statements. Adding 5,100 cash cost only gives 24.81x /20.20x, but is strictly a gross-payment sensitivity, NOT normalized combined valuation. No operating cash flow since July is assumed. Prior Informatica/Qualified acquisitions also make reported TTM a partial-consolidation perimeter.
2. CRM Braze remained an agreement in the reviewed October 20 release, with ~$5.66bn enterprise value and expected FY2028 close. Do not deduct that EV as if a closed equity cash payment. The issuer M&A page also lists Listen Labs, Loops, Rune and Cresta agreements; this screen does not assert a complete November acquisition ledger or financial bridge.
3. WDAY October 23 financing: new principal 2,500 and approximate net proceeds 2,470 add 30 to EV, producing 43.62x/38.83x on cover shares. Refinancing 1,000 old principal does not create another cash benefit. This is a financing-only bridge, not a November balance sheet. October C1.ai agreement economics and closing status were not fully resolved; combined-company valuation remains uncertified.
4. Both peers have July TTM vs NOW's later quarter. WDAY's next results are Nov 24; CRM quarterly-results page still shows Q2 FY2027 as latest. No November 4 intraday quote or unreported October quarter actual is used.

## Read-through
CRM and WDAY are secondary enterprise-application SaaS references, not substitutes for NOW: different product mix, growth, GAAP margins, acquired assets and SBC/reinvestment burden. Their sizeable multiple dispersion remains even when acquired amortization is isolated. These observations can challenge a NOW premium but do not justify a two-stock median target. Next underwriting step is the post-acquisition balance/share-count and earnings reconciliation, especially CRM Q3 disclosures, then match the periods and definitions to NOW.

## Primary links
- [CRM July 10-Q](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm), [CRM FY 10-K](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm), [CRM closing quote](https://investor.salesforce.com/stock-info/).
- [WDAY July 10-Q](https://www.sec.gov/Archives/edgar/data/1327811/000132781126000044/wday-20260731.htm), [WDAY FY 10-K](https://www.sec.gov/Archives/edgar/data/1327811/000132781126000014/wday-20260131.htm), [WDAY quote](https://investor.workday.com/home/default.aspx).
- [Contentful completion note](https://www.salesforce.com/news/stories/salesforce-signs-definitive-agreement-to-acquire-contentful/), [Fin completion](https://www.salesforce.com/news/press-releases/2026/09/10/salesforce-completes-acquisition-of-fin/), [Braze agreement](https://investors.braze.com/news/news-details/2026/Salesforce-Signs-Definitive-Agreement-to-Acquire-Braze/default.aspx).
- [WDAY October financing completion](https://www.sec.gov/Archives/edgar/data/1327811/000110465926118496/tm2626731d6_8k.htm), [C1 agreement](https://www.sec.gov/Archives/edgar/data/1327811/000132781126000051/wday-20261012.htm).
