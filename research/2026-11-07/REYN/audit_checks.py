"""Independent audit of saved model outputs; rerun after model.py."""
import csv,json,math,pathlib
P=pathlib.Path(__file__).parent
x=json.loads((P/'results.json').read_text());checks={}
def eq(a,b):return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8)
for k,s in x['scenarios'].items():
 a=s['assumptions']; rows=s['rows']; prev=3799.; pv=0.; ok=True
 for t,r in enumerate(rows,1):
  g=(1+a['volume'][t-1])*(1+a['price_mix'][t-1])-1 if t<=5 else (1-(t-5)/5)*rows[4]['growth']+(t-5)/5*a['g']
  ok &= eq(r['revenue'],prev*(1+g)) and eq(r['nopat'],r['ebit']*.75)
  ok &= eq(r['delta_nwc'],.15*(r['revenue']-prev)) and eq(r['fcff'],r['nopat']+r['da']-r['capex']-r['delta_nwc'])
  pv+=r['fcff']/(1+a['wacc'])**t;prev=r['revenue']
 terminal=rows[-1]['nopat']*(1+a['g'])*(1-a['g']/a['roic'])
 ev=pv+terminal/(a['wacc']-a['g'])/(1+a['wacc'])**10
 equity=ev+a['acquisition_value']-1536-110-47-14-18.75
 checks[k+'_rows_fcff_growth']=bool(ok and len(rows)==10)
 checks[k+'_ev_equity']=eq(s['ev_standalone'],ev) and eq(s['value_per_share'],equity/211.8)
 z=s['terminal_components'];checks[k+'_terminal_components']=eq(z['fcff'],z['nopat']+z['da']-z['capex']-z['delta_nwc']) and eq(z['reinvestment']/z['nopat'],a['g']/a['roic'])
 data=list(csv.DictReader((P/f'forecast_{k}.csv').open())); checks[k+'_csv']=len(data)==10 and all(eq(float(rr[c]),r[c]) for rr,r in zip(data,rows) for c in rr)
f=x['financials']; columns=['revenue','ebit','net_income','da','cfo','capex','sbc']
y26=[2765,334,206,98,224,143,10];y25=[2687,316,184,100,240,124,18];y24=[2675,369,231,96,307,79,14]
checks['ttm_2026_primary_bridge']=all(eq(f['2026TTM'][c],f['2025'][c]+n-o) for c,n,o in zip(columns,y26,y25))
checks['ttm_2025_primary_bridge']=all(eq(f['2025TTM'][c],f['2024'][c]+n-o) for c,n,o in zip(columns,y25,y24))
checks['four_quarter_ttm_bridge']=all(eq(f['2026TTM'][c],sum(f[q][c] for q in ['2025Q4','2026Q1','2026Q2','2026Q3'])) for c in columns)
checks['capm']=eq(x['capm']['calculated_wacc'],.0771375)
checks['scenario_targets']=all(eq(x['scenarios'][k]['value_per_share'],v) for k,v in [('adverso',9.752932651046358),('central',21.616294489966823),('favorable',31.948441002065668)])
checks['normalized_cash_bridge']=eq(x['cash_bridge']['normalized_fcff'],344.353)
assert all(checks.values()),checks
(P/'audit_checks.json').write_text(json.dumps(checks,indent=2));print(f'{len(checks)} independent checks passed')
