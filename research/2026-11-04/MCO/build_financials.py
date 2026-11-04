from pathlib import Path
import json
P=Path(__file__).parent;T=json.load(open(P/'sources/numeric_tables.json'))
def row(t,l,occ=0):
 rr=[r['values'] for r in T[t] if r['label'].replace('’',"'")==l];assert rr,(t,l);return rr[occ]
def v(t,l,col,occ=0):return row(t,l,occ)[col]
keys=dict(revenue='Revenue',ebit='Operating income',net_income="Net income attributable to Moody's",da='Depreciation and amortization',tax='Provision for income taxes',pretax='Income before provision for income taxes',restructuring='Restructuring',eps_basic='Basic',eps_diluted='Diluted')
def read(ist,ic,cf,cc):
 d={k:v(ist,l,ic) for k,l in keys.items()};d.update(cfo=v(cf,'Net cash provided by operating activities',cc),capex=-v(cf,'Capital additions',cc),sbc=v(cf,'Stock-based compensation',cc));return d
h={}
for yr,c in [(2025,0),(2024,1),(2023,2)]:h[f'FY{yr}']=read('k25_81',c,'k25_84',c)
for yr,c in [(2026,0),(2025,1)]:h[f'Q1{yr}']=read('q1_13',c,'q1_17',c)
for yr,c in [(2026,0),(2025,1)]:
 d=read('q2_12',c,'q2_16',c)
 for k in ['cfo','capex','sbc']:d[k]-=h[f'Q1{yr}'][k]
 h[f'Q2{yr}']=d
for yr,c in [(2026,0),(2025,1)]:
 d=read('q3_12',c,'q3_16',c)
 for k in ['cfo','capex','sbc']:d[k]-=h[f'Q1{yr}'][k]+h[f'Q2{yr}'][k]
 h[f'Q3{yr}']=d
for yr,c in [(2025,0),(2024,1)]:
 ytd=read('q3prev_13',c+2,'q3prev_17',c);h[f'Q4{yr}']={k:round(h[f'FY{yr}'][k]-ytd[k],6) for k in ytd}
for yr,c in [(2025,0),(2024,1)]:
 for k,l in [('eps_basic','Basic'),('eps_diluted','Diluted')]:h[f'Q4{yr}'][k]=v('q4release_29',l,c)
for yr in [2025,2026]:
 ps=[f'Q4{yr-1}']+[f'Q{i}{yr}' for i in [1,2,3]];h[f'TTM{yr}']={k:round(sum(h[p][k] for p in ps),6) for k in h[ps[0]]}
for d in h.values():d['fcf']=round(d['cfo']-d['capex'],6);d['owner_fcf']=round(d['fcf']-d['sbc'],6)
json.dump(h,open(P/'financials.json','w'),indent=2);print(json.dumps(h,indent=2))
