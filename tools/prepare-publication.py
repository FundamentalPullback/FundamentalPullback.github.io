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
    subprocess.run([sys.executable, str(ROOT / 'tools/refresh-tradingview-symbols.py'),
                    '--site-root', str(ROOT)], check=True)
    for test in ('test-stock-profiles.cjs', 'test-stock-cards.cjs', 'test-stock-quotes.cjs', 'test-stock-navigation.cjs', 'test-stock-status.cjs', 'test-research-workspace.cjs', 'test-stock-scan-filter.cjs', 'test-floating-navigation.cjs'):
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
