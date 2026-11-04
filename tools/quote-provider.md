# TradingView symbol maps and publication refresh

These tools prepare public listing-identity maps for the stock-profile quote widgets. They do not publish, upload, create credentials, or retrieve prices.

## Installation

Place `refresh-tradingview-symbols.py` in the repository's `tools/` directory. It is self-contained: Python standard library plus installed Node.js, with no other tool files, raw source files or credentials required. By default it treats the parent of `tools/` as the website root; it also recognizes a repository containing `site/data/manifest.js`.

Refresh before each authorized publication:

    python tools/refresh-tradingview-symbols.py

Dry-run with fresh official downloads and no output writes:

    python tools/refresh-tradingview-symbols.py --dry-run

Explicit paths:

    python tools/refresh-tradingview-symbols.py --site-root path/to/site --out-dir path/to/review/data

The default output is the resolved website's `data/` directory. Optional `--audit-output path/to/audit.json` writes full identity provenance and unsupported/excluded rows. `--source-dir path/to/fixtures` uses explicit local Nasdaq directory snapshots instead of downloads for testing only.

## Output and integration

- `tradingview-symbols.js` sets `window.FP_TRADINGVIEW_SYMBOLS`, `window.FP_TRADINGVIEW_UNAVAILABLE`, and `window.FP_TRADINGVIEW_SYMBOL_METADATA`.
- `tradingview-directory.js` sets `window.FP_TRADINGVIEW_DIRECTORY` for future profiles already present in the directory snapshot.
- Current profiles have an exchange-qualified string or explicit `null`; unavailable reasons are provided separately.

Use an exact current-profile lookup, then an exact full-directory lookup. Do not strip class punctuation, replace dots with hyphens, guess an exchange, or substitute foreign ordinary stock for an ADR. An absent/null identity should show “Quote unavailable: symbol needs verification.” Unknown future profiles are warnings, not build failures; valid mappings remain available. Never retain a formerly valid but now unverified mapping as though it were current.

Source downloads are stored only in a temporary directory, then removed. Both source files must pass header, row-completeness, count and creation-trailer validation. Every generated JS file is staged and syntax checked before any output replacement. Each final output file is replaced atomically. Invalid sources or invalid generated syntax leave prior outputs untouched.

## Coverage and limitations

Current review build: 523/523 profiles mapped, 11,537 full-directory entries including seven dated OTC overrides. 506 rows are explicitly unsupported and 1,240 test/obvious exotic issues excluded. Some true common shares have terse directory descriptions without a security type; these are in the unsupported review list unless already part of the current profile universe. This is intentionally not a promise of universal coverage.

Verified venue conventions: directory Q → NASDAQ, N → NYSE, P/A → AMEX, Z → CBOE. Dotted classes are preserved exactly (e.g. NYSE:BRK.B and NYSE:HEI.A). Unknown directory code F remains unsupported. CBOE is CBOE:CBOE on TradingView, not Google's BATS namespace. Dated exceptions: OTC:HTHIY, OTC:IDEXY, OTC:LKNCY, OTC:LSEGY, OTC:MRAAY, OTC:OBICY, OTC:PRNDY, verified on official TradingView pages on 2026-11-04.

Refresh at publication because static directories cannot anticipate new listings or venue transfers. Newly added profiles already present in the snapshot need no manual map edit. New OTC tickers require exact provider identity verification or a licensed reference service; the seven-symbol exception list is not whole-OTC coverage.

Identity mapping does not prove that a security is permitted in a third-party widget. Preserve TradingView's unavailable state for unsupported symbols. Retain widget attribution. These are delayed human-readable display widgets, not a quote API, a promise of consolidated real time, or a documented official-close feed.

Primary references:
- https://www.nasdaqtrader.com/Trader.aspx?id=SymbolDirDefs
- https://www.tradingview.com/symbols/NYSE-BRK.B/
- https://www.tradingview.com/symbols/NYSE-HEI.A/
- https://www.tradingview.com/symbols/AMEX-SPY/
- https://www.tradingview.com/symbols/AMEX-ACU/
- https://www.tradingview.com/symbols/CBOE-AAAU/
- https://www.tradingview.com/symbols/CBOE-CBOE/
- https://www.tradingview.com/symbols/OTC-OBICY/
- https://www.tradingview.com/widget-docs/faq/data/


## Site publication and quote behavior

Run `python3 tools/prepare-publication.py` after adding approved scanner/research sources and before publication. This is the single preparation entry point for symbol refresh, existing regression checks, quote checks and a new manifest version. There was no repository scanner-ingestion or automatic-publish workflow to modify. The authorized publisher must call this command on each release; adding a checklist does not itself create a scheduled backend. No credentials or CI permissions were added.

The browser loads both mapping files through `manifest.files`, using the current publication version as the cache key. Each profile checks the exact current-profile mapping first (including an explicit unavailable value), then the broad directory for a newly added ticker. Only the visible profile mounts a widget; the Refresh button reloads that widget and checks for a newer publication; the browser does not open hundreds of quotes or scrape price data. A new already-listed ticker normally needs no hand edit. Newly listed/transferred symbols are picked up when the publication refresh sees them. Unknown exchanges or security classes are never guessed. The seven individually checked OTC ADRs are not a promise of arbitrary OTC coverage.

TradingView hosts and refreshes its official Symbol Info widget. Public exchange data can be delayed or unavailable. Its visible quote, currency, market status, time and delay indicator remain provider data. The widget is not used to populate certified previous-close fields, valuations, scanner prices, holdings or account calculations. No interval is promised beyond the provider's behavior, no real-time entitlement is claimed, and provider failure cannot produce a fabricated value. A direct provider link remains available if the script is blocked; unknown identities show an explicit unavailable message. The provider may show its own Invalid Symbol state even for a directory identity.

Official sources: https://www.tradingview.com/widget-docs/faq/data/ , https://www.tradingview.com/widget-docs/faq/general/ , https://www.tradingview.com/widget-docs/tutorials/iframe/build-page/widget-integration/ , https://www.tradingview.com/widget-docs/markets/north-america/ . Keep the widget attribution and branding. Do not export or republish its quotes outside the widget.

The historical close field is intentionally independent. Only a documented regular-session close with its source/session date fills it. The account's existing Google Sheets feed is unchanged. Google Finance documentation says quotes can be delayed up to 20 minutes; its redistribution terms do not grant a general public quote API. This release does not expand that feed or change sheet sharing.
