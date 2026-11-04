# MPC comparison inputs, 4 November 2026

Use `python calculate_mpc.py` to reproduce `outputs.json`. Sources and field mapping are in `inputs.json`. Full downloaded SEC filings are kept only in `../../sources/mpc/`.

## Valuation result and interpretation

MPC trades near **7.17x trailing GAAP operating EBIT**, using consolidated debt/cash and market-valued public MPLX ownership. This is a screening multiple, not normalized earning power. Refining is highly cyclical and 2026 earnings are exceptionally elevated. Do not infer cheapness from this multiple or a peak-cycle P/E. A business-mix/through-cycle comparison remains necessary versus PSX.

The approximate MPLX minority market value is **$21.045bn** from September's rounded 366m public units times the verified November 3 $57.50 close. MPC consolidates MPLX through control of its general partner. Thus consolidated EBIT and debt require the public MPLX equity interest in EV; simply using MPC equity plus consolidated net debt understates EV. It yields an invalid 6.21x comparison.

The 366m public/647m MPC unit counts are rounded financial-statement figures. MPC owns about 64%. Exact total units are available but exact current public units were not established. October 29 total units are 181,824 below September 30. This is immaterial to a two-decimal screening multiple, but the NCI value must remain approximate.

MPLX also reports $224m subsidiary NCI at book value. Adding that as an explicitly labeled proxy moves the multiple to 7.18x. Do not add MPC's full $6.643bn book NCI on top of the MPLX public market value: that double counts. Residual MPC subsidiary minorities and their market values have not been independently reconciled. Therefore label the 7.17x figure as excluding other NCI, or 7.18x as including only the known MPLX subsidiary book proxy.

## Comparability controls

- Use gross principal/finance-lease debt ($33.492bn) or balance-sheet carrying debt ($33.022bn) consistently across peers. The $470m difference is financing costs and discounts. Carrying net debt after cash and short-term investments is $19.413bn; principal-based net debt is $19.883bn.
- Finance leases ($645m) already sit in debt. Operating leases ($1.432bn) are excluded from this EV convention. Do not add them to one peer alone.
- Current shares are October 29 cover shares, with September 30 balance-sheet debt/cash. Subsequent repurchases can create timing mismatch. The stale 638m vendor share count is rejected.
- November 3 closing MPC price $427.34 is verified in Investing.com and ChartExchange daily histories; MPLX $57.50 is verified on issuer IR. Do not mix November 4 intraday prices into the comparison.
- TTM = FY25 + 9M26 − 9M25; no annualization of Q3 alone. Operating income includes equity-method income and is not a pure operating-assets EBIT measure. Keep that convention consistent with PSX and VLO; do not subtract affiliate investment value without also excluding affiliate earnings.
- Announced November 2 divestiture of St. Paul Park/Mandan plus related assets: $4.2bn headline proceeds, not yet closed. Do not net those proceeds against September debt or remove earnings as if closed. MPLX's $750m component is within the consolidated announcement, not incremental to $4.2bn.
- SPR return obligations are a separate sensitivity, not included in ordinary reported debt. Investigate consistently across refiner peers before making a debt-like adjustment.

## Evidence status

Primary SEC filings and issuer releases support financials and ownership; issuer IR supports MPLX price. MPC closing-price evidence is market-data fallback, not issuer evidence. The local source archive contains MPC and MPLX Q3 filings. FY25 release was verified through web retrieval and is linked in inputs; no claim is made that a local FY25 copy exists.
