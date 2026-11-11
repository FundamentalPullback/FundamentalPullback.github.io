#!/usr/bin/env python3
"""Refresh quote identities and validate an already prepared site publication.

Does not ingest scanner data, publish, authenticate, change holdings, or fetch
quote prices. Run after adding approved scanner/research data to the site.
"""
import datetime
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

def main():
    subprocess.run([sys.executable, str(ROOT / 'tools/test-close-batch.py')], check=True)
    # Fail before quote refresh/tests if canonical Sheet reconciliation is absent.
    subprocess.run([sys.executable, str(ROOT / "tools/stage35-publication.py"),
                    "validate", "--site-root", str(ROOT)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools/test-stage35-publication.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / 'tools/refresh-tradingview-symbols.py'),
                    '--site-root', str(ROOT)], check=True)
    subprocess.run(['node', str(ROOT / 'tools/build-stock-balance.cjs')], check=True)
    for test in ('test-alphabet-refresh.cjs', 'test-alphabet-issuer.cjs', 'test-stock-profiles.cjs', 'test-stock-cards.cjs', 'test-stock-balance.cjs', 'test-stock-quotes.cjs', 'test-stock-charts.cjs', 'test-stock-navigation.cjs', 'test-stock-status.cjs', 'test-research-workspace.cjs', 'test-stock-scan-filter.cjs', 'test-floating-navigation.cjs', 'test-stage4-nov4.cjs', 'test-management-calendar.cjs', 'test-scanner-import-note.cjs', 'test-scanner-nov4.cjs', 'test-scanner-nov5.cjs', 'test-scanner-nov6.cjs', 'test-scanner-research-links.cjs', 'test-hrb-partial-sale.cjs', 'run-sales-nov9-historical.cjs', 'test-account-close-current.cjs', 'test-scanner-nov9.cjs', 'test-scanner-nov10.cjs', 'test-research-fa-nov11.cjs', 'test-research-wfc-nov11.cjs', 'test-research-batch90-nov11.cjs', 'test-research-gnxpi-nov11.cjs', 'test-research-you-nov11.cjs', 'test-research-brogxounfi-nov11.cjs', 'test-research-br-nov11.cjs', 'test-research-fa-decision-nov11.cjs', 'test-research-hrb-decision-nov11.cjs', 'test-research-chdn-decision-nov11.cjs', 'test-research-ul-decision-nov11.cjs', 'test-research-htht-refresh-nov11.cjs', 'test-research-ryan-decision-nov11.cjs', 'test-research-tost-decision-nov11.cjs', 'test-research-cpri-decision-nov11.cjs', 'test-research-bmi-decision-nov11.cjs', 'test-research-kr-decision-nov11.cjs', 'test-research-pypl-decision-nov11.cjs', 'test-research-fox-decision-nov11.cjs', 'test-research-bah-decision-nov11.cjs', 'test-research-rgld-decision-nov11.cjs', 'test-research-epam-decision-nov11.cjs', 'test-research-hasi-decision-nov11.cjs', 'test-research-aeo-decision-nov11.cjs', 'test-library-manifest-race.cjs', 'test-research-spgi-decision-nov11.cjs', 'test-research-hri-decision-nov11.cjs', 'run-stage4-nov9-historical.cjs', 'test-stage4-nov10.cjs'):
        subprocess.run(['node', str(ROOT / 'tools' / test)], check=True)
    path = ROOT / 'data/manifest.js'
    prefix = 'window.FP_MANIFEST='
    content = path.read_text()
    if not content.startswith(prefix):
        raise ValueError('Unexpected manifest format')
    manifest = json.loads(content[len(prefix):].strip().rstrip(';'))
    for name in ('data/tradingview-symbols.js', 'data/tradingview-directory.js'):
        if name not in manifest['files']:
            raise ValueError('Missing quote map in manifest.files: ' + name)
    manifest['generated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    temporary = path.with_suffix('.js.tmp')
    temporary.write_text(prefix + json.dumps(manifest, separators=(',', ':')) + ';\n')
    temporary.replace(path)
    print('Prepared and validated. Review changes, publish through the existing authorized path, and verify the live deployment.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('Publication preparation stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)

