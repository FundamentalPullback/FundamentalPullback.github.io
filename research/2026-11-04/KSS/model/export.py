from pathlib import Path
import csv,json
p=Path(__file__).resolve().parent
r=json.loads((p/'results.json').read_text())
for name,x in r.items():
 with (p/(name+'_10years.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(x['rows'][0]));w.writeheader();w.writerows(x['rows'])
