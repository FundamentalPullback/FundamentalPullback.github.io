# Operating comparables verified November 4, 2026

Run `python reproduce_comps.py` using only the Python standard library. Inputs and original source URLs/SHA-256 are in source_numeric_subset.json; key primary financial tables are copied into source_excerpts.json. Full HTML is outside this portable subset in ../full_filings/. Financial figures below are USD millions. No forecasts, price multiples or valuation are provided.

## Quarter comparison
- NVIDIA Q2FY2027, ended July 26, 2026: revenue 96,221; GAAP operating income 63,734; CFO 24,077; cash purchases of PPE and intangible assets 2,677; associated financing principal 59; company-defined FCF 21,341; SBC 2,027. EBIT margin 66.24%, FCF margin 22.18%. Mechanical FCF less SBC 19,314.
- Broadcom Q3FY2026, ended August 2, 2026: revenue 29,591; GAAP operating income 15,955; CFO 14,197; PPE purchases 532; company-defined FCF 13,665; SBC 2,019. EBIT margin 53.92%, FCF margin 46.18%. Mechanical FCF less SBC 11,646.
- AMD Q3FY2026, ended September 26, 2026: revenue 13,377; GAAP operating income 2,832; continuing CFO 1,202; PPE purchases 648; continuing FCF 554; SBC 523. EBIT margin 21.17%, FCF margin 4.14%. Mechanical FCF less SBC 31. These cashflow numbers derive nine months less six months, not simply the nine-month reported totals.

## Period alignment and cash volatility
These are different latest reported quarters, not contemporaneous calendar quarters and not trailing twelve months. NVIDIA ends roughly nine weeks before AMD and Broadcom roughly eight weeks before AMD. NVIDIA FY2027 is largely calendar 2026; never align its FY label directly to AMD/Broadcom FY2027. Inputs include prior-year corresponding quarters and NVDA six-month/AVGO nine-month data to expose cashflow timing; those YTD windows must not be compared as equal durations or annualized blindly.

NVIDIA first-half CFO 74,421 and FCF 69,895 contrast with Q2 CFO 24,077/FCF21,341. Q2 receivables alone consumed 22,346, inventory 5,784 and prepaid/other assets 5,497, partly offset by liabilities. AMD Q3 working-capital use was 3,357. A quarter's FCF margin is not a sustainable normalized cash margin.

NVIDIA release retains direct six-month revenue 177,837 versus the 177,836 sum of displayed quarterly revenue 96,221+81,615; preserve the primary reported totals rather than force consistency by altering a number.

## Definitions and business perimeter
NVIDIA capex is explicitly PPE **and intangible assets**, and its FCF also deducts financing principal for those assets. Dropping the 59 principal would overstate Q2 FCF. The disclosed line does not provide a separate software-only cash outlay. NVIDIA Q2 D&A is 1,127; Note 4 separately gives intangible amortization 237, so do not add this 237 again to reported D&A. Acquisition-related amortization is not identical to total intangible amortization. Groq-related payment 2,944 appears in financing cashflow, outside the company's FCF formula; note the disclosed non-exclusive-license context rather than treating it as ordinary PPE capex or assuming FCF captures every strategic economic outlay. Equity purchases 15,822 and investment gains 7,771 are also separate from recurring operating capital expenditure. GAAP net income benefits from investment gains while GAAP EBIT does not.

Broadcom capex line is PPE purchases, with no separate capitalized-software spend identified in the reviewed release/10-Q. Do not assume software cost is zero or add an unsupported number. Cashflow D&A for Q3 is depreciation 171 plus amortization of intangible and right-of-use assets 2,042, total 2,213; acquired intangible amortization within the operating-income reconciliation is 2,006 and is already within this broader expense family. Do not double count. Purchases of investments are not capex. Prior-year Q3 included a 163 gain from sale of business and 300 investing proceeds; neither is a reason to change GAAP EBIT or classify the sale proceeds as FCF.

Broadcom includes infrastructure software revenue 8,752, approximately 29.58% of consolidated revenue, plus semiconductor revenue 20,839. This material software mix and acquisition amortization mean it is not a pure accelerator-chip peer. Its segment operating incomes (12,770 semiconductors and 7,325 software) exclude 4,140 unallocated adjustments, including SBC and acquired amortization; their 20,095 sum is not consolidated GAAP EBIT 15,955.

NVIDIA combines accelerated computing, networking, graphics and associated software. Its Compute & Networking reporting segment revenue 88,299 is not identical to the approximately 89,000 Data Center market-platform revenue. Do not mix market-platform and reportable-segment definitions, or label all NVIDIA revenue GPU sales. NVIDIA segment OI also excludes certain corporate costs and SBC and must not be substituted for GAAP consolidated EBIT.

AMD retained ZT design in continuing operations but disposed of ZT manufacturing, which remains excluded from the CFO comparison. AMD client/gaming/embedded mix is materially different from NVIDIA's or Broadcom's. No organic-perimeter reconstruction is claimed for undisclosed small acquisitions.

## SBC and adjusted-measure trap
NVIDIA explicitly changed its non-GAAP convention starting Q1FY2027: it **no longer excludes SBC**, and recast the historical non-GAAP comparisons shown. AMD/Broadcom adjusted operating income ordinarily excludes SBC. Thus cross-company non-GAAP margin comparisons without harmonizing SBC are invalid. This file uses GAAP EBIT and separately displays SBC. FCF less SBC is a mechanical diagnostic, not a fully normalized owner-earnings figure; it does not settle dilution, customer warrants, tax benefits, acquisitions or future reinvestment needs.

## Primary source locations
NVIDIA release (August 26, 2026): https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx
NVIDIA 10-Q: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm
NVIDIA issuer-hosted PDF locator: https://investor.nvidia.com/files/doc_financials/2027/NVDA-2027-Q2-10Q-Final-including-exhibits.pdf
Broadcom release (September 2, 2026): https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial
Broadcom 10-Q: https://www.sec.gov/Archives/edgar/data/1730168/000173016826000080/avgo-20260802.htm
AMD sources and broader history are in ../history/.
