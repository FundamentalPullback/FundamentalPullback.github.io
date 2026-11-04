#!/usr/bin/env python3
"""Build TradingView identity maps from official Nasdaq directories, never prices.

Place in repo/tools/. Default --site-root is the parent of tools/; a repository
containing site/data/ is also recognized. Default output is the site's data/.
Run --dry-run to validate downloads and profile coverage without writing maps.
New unknown profiles remain explicitly unavailable; no exchange is guessed.
"""
import argparse
import collections
import csv
import datetime as dt
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

SOURCE_URLS = {
    name: 'https://www.nasdaqtrader.com/dynamic/SymDir/' + name
    for name in ('nasdaqlisted.txt', 'otherlisted.txt')
}
VENUES = {'Q': 'NASDAQ', 'N': 'NYSE', 'P': 'AMEX', 'A': 'AMEX', 'Z': 'CBOE'}
# Individually verified provider ADR pages, 2026-11-04. Not general OTC coverage.
OTC_OVERRIDES = {
    ticker: {'symbol': 'OTC:' + ticker,
             'sourceUrl': 'https://www.tradingview.com/symbols/OTC-' + ticker + '/',
             'verifiedAt': '2026-11-04'}
    for ticker in ('HTHIY', 'IDEXY', 'LKNCY', 'LSEGY', 'MRAAY', 'OBICY', 'PRNDY')
}
EXCLUDED = re.compile(
    r'\b(?:preferred|preference)\s+(?:stock|shares?|units?|securities)\b'
    r'|\bwarrants?\b|\bRights(?:$|,|\s+(?:each|to purchase))'
    r'|\b(?:notes?|bonds?|debentures?)\b(?=\s+(?:due|20\d{2}))'
    r'|\bETN\b|\bunits?[, ]+each\b|\d+\.?\d*\s*%|\bdue 20\d{2}\b', re.I)
ORDINARY = re.compile(
    r'\b(common|ordinary|depositary|depository|ADR|ADS|shares? of beneficial'
    r'|capital stock|voting shares?|non-voting shares?|equity shares?'
    r'|common units|units of beneficial|registry shares?)\b', re.I)
SAFE_SYMBOL = re.compile(r'^[A-Z0-9]+(?:\.[A-Z])?$')

# Existing profile engine is the authority for the current profile universe.
PROFILE_NODE = r'''
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.resolve(process.argv[1]);
const c = {}; c.window = c; vm.createContext(c);
function run(relative) {
  const filename = path.resolve(root, relative);
  if (!filename.startsWith(root + path.sep)) throw Error('Manifest path escapes site root');
  vm.runInContext(fs.readFileSync(filename, 'utf8'), c, {filename, timeout: 15000});
}
run('data/manifest.js');
const manifest = c.FP_MANIFEST;
if (!manifest || !Array.isArray(manifest.files) || !Array.isArray(manifest.libraryFiles))
  throw Error('Expected current site manifest files and libraryFiles');
for (const file of [...new Set([...manifest.files, ...manifest.libraryFiles])]) run(file);
if (fs.existsSync(path.join(root, 'data/names.js'))) run('data/names.js');
run('data/stock-profiles.js');
function convert(rows, suppliedHeader) {
  rows = rows || [];
  const header = suppliedHeader || rows[0] || [];
  const start = suppliedHeader ? 0 : 1;
  const ix = (name) => header.findIndex(x => String(x).trim().toLowerCase() === name);
  const ti = ix('ticker'), ci = ix('empresa');
  if (rows.length && ti < 0) throw Error('Missing Ticker header');
  return rows.slice(start).map(r => ({ticker:r[ti], company:ci < 0 ? '' : r[ci], date:r[0]}));
}
const f = c.FP || {};
const profiles = c.FP_PROFILE_ENGINE.build({
  scans:convert(f.scan, f.scanHead), decisions:convert(f.dec),
  operations:convert(f.ops), management:convert(f.ges),
  reports:(c.FP_LIB || {}).reports || [], names:c.FP_NAMES || {}
}).map(p => ({ticker:p.ticker, company:p.company}));
if (!profiles.length) throw Error('No stock profiles derived');
process.stdout.write(JSON.stringify({publication:manifest.generated, profiles}));
'''


def parse_directory(text, name):
    lines = text.strip().splitlines()
    required = {'Test Issue', 'Security Name', 'ETF'} | (
        {'Symbol'} if name == 'nasdaqlisted.txt'
        else {'Exchange', 'CQS Symbol', 'ACT Symbol', 'NASDAQ Symbol'})
    if (len(lines) < 1000 or not required <= set(lines[0].split('|'))
            or not lines[-1].startswith('File Creation Time:')):
        raise ValueError(name + ': invalid header, count or creation-time trailer')
    rows = list(csv.DictReader(io.StringIO('\n'.join(lines[:-1])), delimiter='|'))
    if any(any(r.get(k) is None for k in required) for r in rows):
        raise ValueError(name + ': incomplete directory row')
    return rows, lines[-1].split('|')[0]


def load_sources(source_dir):
    parsed = {}
    # No raw directory snapshot is written into the repository.
    with tempfile.TemporaryDirectory(prefix='tradingview-directory-') as tmp:
        for name, url in SOURCE_URLS.items():
            if source_dir:
                text = (source_dir / name).read_text(encoding='utf-8-sig')
            else:
                request = urllib.request.Request(url, headers={
                    'User-Agent': 'StockProfileSymbolMapper/1.0'})
                with urllib.request.urlopen(request, timeout=60) as response:
                    if response.status != 200:
                        raise ValueError(name + ': unexpected HTTP status')
                    text = response.read().decode('utf-8-sig')
                (pathlib.Path(tmp) / name).write_text(text, encoding='utf-8')
            parsed[name] = parse_directory(text, name)
    return parsed


def derive_profiles(site_root):
    result = subprocess.run(['node', '-e', PROFILE_NODE, str(site_root)],
                            check=True, text=True, capture_output=True, timeout=120)
    data = json.loads(result.stdout)
    tickers = [p['ticker'] for p in data['profiles']]
    if len(tickers) != len(set(tickers)):
        raise ValueError('Profile engine returned duplicate tickers')
    return data


def build_maps(parsed, profile_data):
    profile_keys = {p['ticker'] for p in profile_data['profiles']}
    mapping, records, reasons = {}, {}, {}
    unsupported, excluded, seen, ambiguous = [], [], set(), set()
    for name, (rows, _) in parsed.items():
        for row in rows:
            symbol = row.get('Symbol') or row['CQS Symbol']
            aliases = [symbol] if name == 'nasdaqlisted.txt' else list(dict.fromkeys(
                [symbol, row['ACT Symbol'], row['NASDAQ Symbol']]))
            seen.update(aliases)
            base = {'symbol': symbol, 'securityName': row['Security Name'], 'sourceFile': name}
            code = 'Q' if name == 'nasdaqlisted.txt' else row['Exchange']
            base['listingExchangeCode'] = code
            reason = None
            is_profile = any(alias in profile_keys for alias in aliases)
            if row['Test Issue'] != 'N':
                reason = 'test-issue'
            elif row['ETF'] == 'Y':
                kind = 'ETF'
            elif EXCLUDED.search(row['Security Name']):
                reason = 'preferred-warrant-right-debt-or-composite-unit'
            elif ORDINARY.search(row['Security Name']):
                kind = 'common-ordinary-ADR-or-beneficial-interest'
            elif is_profile:
                kind = 'existing-profile-directory-identity-type-unspecified'
            else:
                reason = 'security-type-not-explicit-in-directory-name'
            if reason is None and code not in VENUES:
                reason = 'unverified-provider-venue-code'
            if reason is None and not SAFE_SYMBOL.fullmatch(symbol):
                reason = 'unverified-provider-symbol-syntax'
            if reason:
                target = excluded if reason in ('test-issue', 'preferred-warrant-right-debt-or-composite-unit') else unsupported
                target.append(dict(base, reason=reason))
                for alias in aliases:
                    reasons[alias] = reason
                continue
            qualified = VENUES[code] + ':' + symbol
            records[symbol] = dict(base, type=kind, tradingviewSymbol=qualified,
                                  widgetAvailabilityVerified=False)
            for alias in aliases:
                if not SAFE_SYMBOL.fullmatch(alias):
                    continue
                if alias in mapping and mapping[alias] != qualified:
                    ambiguous.add(alias)
                else:
                    mapping[alias] = qualified
    for alias in ambiguous:
        mapping.pop(alias, None)
        reasons[alias] = 'ambiguous-exact-directory-alias'
        unsupported.append({'symbol': alias, 'reason': reasons[alias]})
    for ticker, override in OTC_OVERRIDES.items():
        if ticker not in seen:
            mapping[ticker] = override['symbol']
            records[ticker] = dict(override, type='verified-OTC-ADR', widgetAvailabilityVerified=False)
    current = {ticker: mapping.get(ticker) for ticker in sorted(profile_keys)}
    missing = {ticker: reasons.get(ticker, 'not-in-official-directory-or-verified-exceptions')
               for ticker, symbol in current.items() if symbol is None}
    metadata = {
        'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(),
        'profilePublication': profile_data.get('publication'),
        'directoryCreationTimes': {n: stamp for n, (_, stamp) in parsed.items()},
        'sourceUrls': list(SOURCE_URLS.values()), 'profileCount': len(current),
        'mappedProfileCount': len(current) - len(missing),
        'directoryAliasCount': len(mapping), 'securityCount': len(records),
        'unsupportedCount': len(unsupported), 'excludedCount': len(excluded),
        'unavailableProfiles': missing,
        'notes': [
            'Identity mapping is not proof of third-party widget availability.',
            'No prices are collected, copied or exported.',
            'Exact dotted classes are preserved; unknown venues and syntax are not guessed.',
            'Refresh at publication for new listings or listing transfers.',
            'Dated OTC exceptions are not general OTC coverage.',
            'Missing profiles are null and must remain explicitly unavailable.'
        ]
    }
    return current, dict(sorted(mapping.items())), metadata, {
        'metadata': metadata, 'records': records, 'unsupported': unsupported, 'excluded': excluded}


def atomic_writes(contents):
    """Stage and validate every file before replacing any live output."""
    staged = []
    try:
        for destination, text in contents.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=destination.parent,
                                             prefix='.' + destination.name + '.', suffix='.js',
                                             delete=False) as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
                temporary = pathlib.Path(handle.name)
            staged.append((temporary, destination))
            if destination.suffix == '.js':
                subprocess.run(['node', '--check', str(temporary)], check=True,
                               capture_output=True, text=True, timeout=30)
            else:
                json.loads(text)
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-root', type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parent.parent)
    parser.add_argument('--out-dir', type=pathlib.Path,
                        help='Default: the resolved website data/ directory')
    parser.add_argument('--dry-run', action='store_true', help='Validate only; write no maps')
    parser.add_argument('--source-dir', type=pathlib.Path,
                        help='Use explicit local directory fixtures instead of fresh downloads (testing only)')
    parser.add_argument('--audit-output', type=pathlib.Path,
                        help='Optional full provenance/unsupported/excluded JSON output')
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    if not (site_root / 'data/manifest.js').is_file() and (site_root / 'site/data/manifest.js').is_file():
        site_root = site_root / 'site'
    if not (site_root / 'data/manifest.js').is_file():
        raise ValueError('No data/manifest.js under the selected site root')
    out = args.out_dir.resolve() if args.out_dir else site_root / 'data'
    profile_data = derive_profiles(site_root)
    parsed = load_sources(args.source_dir.resolve() if args.source_dir else None)
    current, directory, metadata, audit = build_maps(parsed, profile_data)
    metadata['sourceMode'] = 'local-fixtures' if args.source_dir else 'fresh-official-downloads'
    metadata['dryRun'] = args.dry_run
    compact = lambda obj: json.dumps(obj, ensure_ascii=True, separators=(',', ':'))
    contents = {
        out / 'tradingview-symbols.js':
            '/* Exact profile listing identities. Null means unavailable. No prices. */\n'
            + 'window.FP_TRADINGVIEW_SYMBOLS=' + compact(current) + ';\n'
            + 'window.FP_TRADINGVIEW_UNAVAILABLE=' + compact(metadata['unavailableProfiles']) + ';\n'
            + 'window.FP_TRADINGVIEW_SYMBOL_METADATA=' + compact(metadata) + ';\n',
        out / 'tradingview-directory.js':
            '/* Official-directory identity lookup for future profiles. No prices. */\n'
            + 'window.FP_TRADINGVIEW_DIRECTORY=' + compact(directory) + ';\n'
    }
    if args.audit_output:
        contents[args.audit_output.resolve()] = json.dumps(audit, indent=2) + '\n'
    # Validate complete in-memory output before writes. Missing profiles are valid
    # explicit unavailable states, not permission to preserve a stale quote link.
    if not current or not directory or len(directory) < 1000:
        raise ValueError('Empty or unexpectedly small generated map')
    if any(value is not None and ':' not in value for value in current.values()):
        raise ValueError('Invalid exchange-qualified profile symbol')
    if not args.dry_run:
        atomic_writes(contents)
    print(json.dumps(metadata, indent=2))
    if metadata['unavailableProfiles']:
        print('WARNING: Explicitly unavailable profiles: ' + ', '.join(metadata['unavailableProfiles']),
              file=sys.stderr)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Symbol map refresh failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
