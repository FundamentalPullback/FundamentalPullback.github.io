# HD independent audit | 7 November 2026

**Verdict: Ready with caveats for completed conditional research review only.** No entry approval; no publication or trading.

Valuation unchanged: adverse $127.85, central $211.78, favorable $341.51 against independently checked $343.47 regular close. The favorable case barely reaches price; central gap remains material. Upcoming November 17 results are not treated as published.

## Findings and fixes

**HD-A01 · medium · Not comparable without bridge**
Prior TTM is 53 weeks against 52 current and different acquisition perimeter; recurring EBIT -5.85% was mislabeled comparable.
Labeled reported-period comparison; added equal-26-week H1 normalized EBIT -4.73%, still not organic.

**HD-A02 · medium · Source contradiction**
Source ledger reported November ERP but noted canonical September snapshot; report did not disclose conflict.
Independently read November 1 4.41% at exact query-bearing NYU URL and archived; disclosed stale canonical snapshot and mixed monthly ERP/daily Treasury dates.

**HD-A03 · low · Formula/control defect**
CFO proxy subtracts EBIT refund 685 but cash received 730; 45 inventory timing not separately shown.
Retained earnings-normalized proxy 15742.63 and added inventory cash timing -45 to 15697.63; actual tax timing remains unavailable.

**HD-A04 · low · Formula/control defect**
Report claimed sensitivity mesh in CSV, but CSVs contain only forecasts/history.
Corrected location to results.json.

**HD-A05 · medium · Unsupported assumption**
Forward D&A replacement, incremental ROIC, working-capital intensity and debt spread are analyst assumptions, not externally verified forecasts.
Retained transparent assumptions and sensitivities; no investment-entry readiness implied.

## Source tie-out and controls

**3 annual years** (FY2025 annual report)
Sales, EBIT, earnings, CFO, capex, SBC and total D&A tie; FY2024 53-week caveat retained.

**4 quarters / TTM** (Q3 FY2025 results; Q4 FY2025 results; Q1 FY2026 results; Q2 FY2026 filing)
Quarter summation and FY2025 + H1 2026 - H1 2025 identities pass for all nine historical metrics. Current TTM sales 169176, EBIT 21022, cash FCF 15099.

**Tariff adjustment** (Q2 FY2026 filing)
685 earnings benefit excluded once; 730 cash receipts and 45 inventory effect now distinct. No unsupported removal of actual cost pressures.

**Acquisitions** (FY2025 annual report; Q2 FY2026 filing)
SRS 18028; GMS 5081 plus separately assumed/repaid 354; Mingledorff about 1100 closed. Existing debt reflects historical financing. TTM is not pro forma; +2% sales sensitivity bounds omitted maturity, not a factual run rate.

**Equity bridge** (Q2 FY2026 filing balance sheet, lease, supplier finance and EPS notes; annual employee plans)
Debt 52896 includes finance leases 3094 once. Operating leases 9671 remain operating cost. Supplier finance 542 remains WC. Cash 2085 with 2000 operating reserve. No identified material minority or separately disclosed defined-benefit deficit; zero is evidence-limited, not certification of all contingent claims.

**Reinvestment / SBC** (model.py dcf; FY2025 annual report)
Economic capex exceeds cash history; software amortization 3-7 years. SBC stays economic expense and is not added to forward FCFF. Generic total-D&A replacement is conservative proxy, not asset-by-asset engineering proof.

**FCFF / terminal / inverse** (model.py; validate.py; forecasts)
Ten years = five explicit plus five fade. FCFF, terminal physical capex, terminal g/ROIC, PV, equity bridge and both inverse equations independently reproduce.

**Price / event / CAPM** (dated market source verification; dated CAPM source verification; dated Treasury source verification)
343.47 regular close November 6 confirmed; Nov17 09:00 ET official event remains future. Treasury 10Y 4.86%, November ERP4.41%, beta0.95 verified with stated as-of caveats; debt spread90bp assumed.

## Judgment and remaining limits
The package supports observation, not an approved entry. No material missing acquisition payment, debt double-count or broken valuation identity was found. Mechanical consistency does not validate future recovery or reinvestment productivity. The DCF is a conditional scenario model, not a precision fair-value estimate. Negative normalized H1 EBIT on equal-length periods corroborates the deterioration diagnosis without misrepresenting the 53/52-week TTM comparison.

Source links remain in sources.json; prior source verification is summarized in audit.json. Audit.json preserves the issue log, source ledger and financial caveats.
