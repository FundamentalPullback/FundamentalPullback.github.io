# Compact peer evidence sheet

Cutoff: November 4, 2026, 06:46 UTC. All financial evidence was public before the cutoff; collection finished later that morning. No FRPT Q3 result, valuation multiple, trade, or recommendation is included. Amounts are USD millions except common shares and quoted price.

| Raw trailing input | CL | GIS | CHWY |
|---|---:|---:|---:|
| Period end | September 30, 2026 | August 30, 2026 | August 2, 2026 |
| Revenue | 21,285.0 | 18,296.6 | 13,068.7 |
| GAAP operating profit | 3,161.0 | -206.4 | 328.2 |
| SBC | 169.0 | 86.1 | 297.9 |
| D&A | 643.0 | 556.3 | 143.9 |
| CFO | 4,366.0 | 2,067.0 | 717.2 |
| Cash capex, positive outflow | 577.0 | 520.9 | 149.1 |
| Latest cash and equivalents | 1,527.0 | 433.1 | 611.0 |
| Latest debt, carrying value | 7,716.0 | 13,615.6 | 591.7 |
| Actual common shares | 794,920,513 | 534,687,144 | 401,927,249 |
| Common-share observation | September 30, 2026 | September 16, 2026 | September 2, 2026 |
| November 3 regular close, USD | 95.62 | 34.08 | 22.05 |

Cash/debt dates equal each trailing period end. CHWY gross debt principal is $600.0m; carrying value deducts issuance costs. GIS has another $30.7m cash held for sale, not included in the main cash row. CHWY has $1.2m marketable securities separately. Operating leases are separately described in issuer reports, not mixed into the debt row. No date-mismatched market value or multiple has been calculated.

## Interpretation controls

- **CL:** consolidated consumer-staples comparator only. Hill’s trailing sales $4,790m and reported segment profit $1,102m are not a standalone enterprise valuation or fully burdened EBIT. Consolidated trailing GAAP profit retains $919m impairment. The issuer operating-profit bridge is preserved separately: its endpoint implies $4,503m after adjustments, with a $1m rounding residual versus summed component adjustments. Ordinary SBC and amortization remain costs. Restructuring has real cash consequences.
- **GIS:** consolidated branded-food comparator only. North America Pet trailing sales $2,616.1m and reported segment profit $485.4m include more than Blue Buffalo and fresh food. The mechanical trailing period has **53 weeks**. GAAP EBIT is negative because FY26 impairment/held-for-sale losses remain while the earlier divestiture gain rolls out. Do not compute an apparently meaningful raw GAAP EV/EBIT multiple. The issuer operating-profit bridge is preserved for judgment, not automatically adopted. Ordinary SBC and amortization remain costs.
- **CHWY:** retailer/channel reference only. Producer gross margin and capital requirements are not comparable. SBC is shown excluding associated payroll taxes, which remain ordinary expenses. A new term loan means historical zero-debt shortcuts are wrong. Acquisitions affect growth, mix and capital employed.
- TTM is FY + latest YTD − prior matching YTD for CL/CHWY, and FY + latest quarter − prior matching quarter for GIS. Issuer reports preserve all legs. No pro-forma acquisitions, dispositions or 53-week adjustments were invented. Capex is not assumed entirely maintenance.

## Primary financial sources

CL: [Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/21665/000002166526000048/cl-20260930.htm), [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/21665/000002166526000006/cl-20251231.htm), [October 30 release](https://investor.colgatepalmolive.com/news-releases/news-release-details/colgate-palmolive-announces-3rd-quarter-2026-results).

GIS: [FY2026 10-K, July 1](https://www.sec.gov/Archives/edgar/data/40704/000162828026046466/gis-20260531.htm), [Q1 FY2027 10-Q, September 23](https://www.sec.gov/Archives/edgar/data/40704/000162828026063201/gis-20260830.htm).

CHWY: [Q2 FY2026 10-Q, September 9](https://www.sec.gov/Archives/edgar/data/1766502/000162828026061018/chwy-20260802.htm), [FY2025 10-K, March 25](https://www.sec.gov/Archives/edgar/data/1766502/000176650226000034/chwy-20260201.htm).

## Dated market-price sources

Regular close on November 3, 2026, 4:00 PM EST: [CL daily history](https://stockanalysis.com/stocks/cl/history/), [GIS daily history](https://stockanalysis.com/stocks/gis/history/), [CHWY daily history](https://stockanalysis.com/stocks/chwy/history/). These pages credit S&P Global Market Intelligence. Exact OHLC rows, quote times and source URLs are preserved in `quotes.json`. Ignore conflicting intraday/after-hours observations. Prices are third-party market evidence; financial inputs above are issuer/SEC evidence.

## Packet map

- `peer_evidence.json`: compact structured summary and source pointers.
- `cl/report.md`, `cl/facts.json`, `cl/normalization_addendum.md`, `cl/adjustments.json`.
- `gis/report.md`, `gis/facts.json`, `gis/operating_profit_bridge.md`.
- `chwy/report.md`, `chwy/facts.json`.
- Full raw SEC/issuer sources and readable table/text extracts are retained in issuer directories or `sources/`.
