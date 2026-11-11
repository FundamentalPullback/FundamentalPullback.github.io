"""Independent algebra, no production function imports; reads saved expectations only."""
import json, math
from pathlib import Path
B=Path(__file__).resolve().parents[1]; O=json.loads((B/'results.json').read_text()); L=json.loads((B/'legacy/model_outputs.json').read_text()); checks=[]
S=28.563652+.121037; bridge=67.928-30-12-9.343
P={'central':([.08,.08,.08,.07,.06],[.20,.205,.21,.215,.22],.025,.20,.18),'adverse':([0,.03,.04,.04,.04],[.18,.18,.185,.185,.185],.02,.15,.15),'favorable':([.12,.12,.11,.10,.09],[.21,.22,.23,.235,.24],.03,.25,.20)}
# Explicit legacy scenario inputs are used as data, not computed outputs.
for k,c in L['cases'].items(): P[k]=(c['growth'],c['margin'],c['g'],c['roic'],c['terminal_roic'])
def ck(label,a,b):
 ok=math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7); checks.append({'label':label,'actual':a,'expected':b,'pass':ok}); assert ok,(label,a,b)
def value(path,mode,rate,flat=None):
 gs,ms,g,ri,tr=P[path]; gs=list(gs) if flat is None else [flat for _ in range(5)]
 rev=881.242; prev=165.339*.75; rows=[]
 for n in range(10):
  grow=gs[n] if n<5 else (gs[4]*(9-n)+g*(n-4))/5
  mar=ms[min(n,4)]; nxt=rev*(1+grow); nop=.75*mar*nxt; wc=.15*(nxt-rev)
  rr=ri if n<5 else (ri*(9-n)+tr*(n-4))/5
  capital=wc if mode=='efficient' else max(wc,(nop-prev)/rr,0)
  cash=nop-capital; rows.append(dict(sales=nxt,nopat=nop,net_investment=capital,fcff=cash,pv=cash*(1+rate)**(-n-1)))
  rev=nxt;prev=nop
 terminal_nop=prev*(1+g); funding=.15*rev*g
 if mode!='efficient':funding=max(funding,terminal_nop*g/tr)
 tf=terminal_nop-funding; tp=tf/(rate-g)*(1+rate)**-10; ev=sum(x['pv'] for x in rows)+tp
 return {'rows':rows,'terminal_fcff':tf,'terminal_pv':tp,'ev':ev,'terminal_fraction':tp/ev,'value':(ev+bridge)/S,'required_net_deal_value':157.58*S-ev-bridge}
ck('shares',S,O['shares']);ck('bridge',bridge,O['net_bridge']);ck('observed KE',.0498+.0441*.62,.077142)
vals={}
for name,c in O['cases'].items():
 x=value(c['path'],c['mode'],c['rate']);vals[name]=x['value']
 for key in ['value','ev','terminal_fcff','terminal_pv','terminal_fraction','required_net_deal_value']:ck(name+'.'+key,x[key],c[key])
 for i,(a,b) in enumerate(zip(x['rows'],c['rows'])):
  for key in a:ck(f'{name}.{i+1}.{key}',a[key],b[key])
for path in ['central','favorable','adverse']:
 for key,new in [('price','value'),('ev','ev'),('terminal_fcff','terminal_fcff'),('pv_terminal','terminal_pv')]:ck('legacy.'+path+'.'+key,O['cases']['old'+path][new],L['summary'][path][key])
for i,d in enumerate(O['deals']):
 gap=157.58*S-(vals[d['case']]*S); gross=gap+d['hypothetical_purchase_cost']
 for key,v in [('required_net_deal_value',gap),('required_acquired_gross_value',gross),('illustrative_perpetual_fcff_at_9pct_g25',gross*.065)]:ck('deal'+str(i)+key,v,d[key])
scans=[]
for i,d in enumerate(O['inverses']):
 f=lambda g:value('central',d['mode'],d['rate'],g)['value']; vs=[f(j/2000) for j in range(1001)]
 assert all(b>a for a,b in zip(vs,vs[1:]));assert vs[0]<157.58<vs[-1]
 lo=0.;hi=.5
 for _ in range(80):
  mid=(lo+hi)/2
  if f(mid)>157.58:hi=mid
  else:lo=mid
 root=(lo+hi)/2;x=value('central',d['mode'],d['rate'],root)
 ck('inverse'+str(i)+'.root',root,d['required_y1_5_growth']);ck('inverse'+str(i)+'.value',x['value'],157.58);ck('inverse'+str(i)+'.sales',x['rows'][-1]['sales'],d['year10_sales']);scans.append({'mode':d['mode'],'rate':d['rate'],'intervals':1000,'strictly_increasing':True,'root':root})
out={'status':'PASS','comparisons':len(checks),'cases':10,'deal_scenarios':16,'inverses':4,'legacy_paths':3,'monotonic_intervals':4000,'values':vals,'inverse_scans':scans,'checks':checks};(B/'audit/output.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='checks'})
