"""Reproduce the public BSY calculation package without modifying delivered inputs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
OUTPUTS = ['metrics.json', 'annual.csv', 'quarters.csv', 'ttm.csv',
           'model_results.json', 'fcff_adverso.csv', 'fcff_central.csv', 'fcff_favorable.csv']
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
checks = []
with tempfile.TemporaryDirectory(prefix='bsy_reproduction_') as work:
    work = Path(work)
    for script in ['build_metrics.py', 'model_calc.py']:
        shutil.copy2(ROOT / script, work / script)
        run = subprocess.run([sys.executable, script], cwd=work, capture_output=True, text=True)
        if run.returncode != 0:
            raise RuntimeError('Calculation script failed: ' + script)
    for name in OUTPUTS:
        actual = digest(work / name)
        expected = digest(ROOT / name)
        checks.append({'check': 'Exact output reproduction: ' + name,
                       'pass': actual == expected, 'sha256': actual})
model = json.loads((ROOT / 'model_results.json').read_text())
for name, case in model['scenario'].items():
    for row in case['rows']:
        difference = row['nopat'] + row['da'] - row['effective_capex'] - row['delta_nwc'] - row['fcff']
        checks.append({'check': name + ' Y' + str(row['t']) + ' FCFF components',
                       'pass': abs(difference) < 1e-8})
quote = json.loads((ROOT / 'sources.json').read_text())['S13']
checks.append({'check': 'Historical quote timestamp and price',
               'pass': quote['price'] == model['spot'] and quote['trade_timestamp'] == model['as_of']})
result = {'status': 'pass' if all(x['pass'] for x in checks) else 'fail',
          'checks_passed': sum(x['pass'] for x in checks), 'checks_failed': sum(not x['pass'] for x in checks),
          'checks': checks, 'economic_changes': False,
          'scope': 'Reproducibility and formula identities, not a fresh independent valuation audit.',
          'visual_qa': 'Not performed; permitted publisher visual QA remains pending.'}
(ROOT / 'reproduction_result.json').write_text(json.dumps(result, indent=2))
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
if result['status'] != 'pass':
    raise SystemExit(1)
