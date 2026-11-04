"""Read-only final artifact validation. Does not rewrite model, report or publication."""
from pathlib import Path
import json
P=Path(__file__).parent
m=json.loads((P/'model.json').read_text());p=json.loads((P/'publication.json').read_text());h=(P/'WDAY_20261104.html').read_text()
assert abs(m['cases']['central']['value_per_share']-151.34476629)<1e-7
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for s in p[k]:assert s in h,(k,s)
assert all(len(c['rows'])==10 for c in m['cases'].values())
print('Final consistency PASS. Visual review and independent model audit remain separate.')
