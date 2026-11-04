# VFC Stage 3 — 4 November 2026

Start with VFC_full_stage3_2026-11-04.md. All amounts are USD millions unless explicitly marked otherwise.

1. Run `python model.py` to reproduce the ten-year FCFF scenarios, joint sensitivities, reverse valuation and claims bridge. No network access or third-party Python package is required.
2. Run `python verify_model_independent.py` for the second formula implementation and 256 arithmetic tests. It does not import model.py.
3. Run `python build_comps.py` to reproduce the peer arithmetic from dated primary inputs and the supplied peer source indexes.
4. Historical CSV/JSON data contain the source references and formulas. Full source originals are linked in history/Source_Index and operating/source_manifest. Historical extraction scripts need the original HTML sources fetched into history/raw; source table indexes are preserved. Public issuer/SEC sources may change availability.

Exact retained Dickies cash and historical tariff/vendor timing are not disclosed by the issuer. Missing fields remain null. Reported continuing cash, retained P&L, symmetric normalization identities and forward assumptions are kept distinct.

The archive excludes the full licensed call transcript and third-party article bodies. Read the linked original sources. All prices use the November 3 regular close, separately from scanner after-hours data. This package contains research, not an order or trade authorization.
