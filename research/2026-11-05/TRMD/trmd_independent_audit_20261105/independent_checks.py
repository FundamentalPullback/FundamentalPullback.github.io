from pathlib import Path
import json,math,hashlib
P=Path(__file__).resolve().parent;M=P.parent/'trmd_valuation_20261105/model'
A=json.loads((M/'assumptions.json').read_text());R=json.loads((M/'results.json').read_text());F=json.loads((M/'fleet.json').read_text())
COST={'MR':48.6,'LR1':60.,'LR2':75.};DOCK={'MR':1.5,'LR1':1.8,'LR2':2.2};OPEX={'MR':7680,'LR1':7401,'LR2':8752};BASE=2026.75;VAL=2026+307/365
# Primary note10 Sept30 fiscal bands, independently spread into calendar years for audit.
commit={2026:49.175,2027:167.85,2028:113.175,2029:174.975,2030:68.875,2031:41.25}
checks=[]
def check(name,got,expected,tol=1e-7):
 ok=abs(got-expected)<=tol if isinstance(expected,(float,int)) else got==expected
 checks.append(dict(name=name,got=got,expected=expected,tolerance=tol,pass_=ok))

def rebuild(p,renewal,last):
 fs=[dict(type=v['type'],built=v['built_year']+.5,start=BASE,committed=False) for v in F]
 for year,count in [(2027,4),(2028,2),(2029,6),(2030,2)]:
  fs.extend(dict(type='MR',built=year+.5,start=year+.5,committed=True) for _ in range(count))
 ys={y:dict(tce=0.,opex=0.,dock=0.,replace=0.,scrap=0.,days=0.) for y in range(2026,last+1)}
 inflate=lambda t:(1+p['inflation'])**(t-2026)
 for v in fs:
  cl=v['type'];birth=v['built'];first=True
  while birth<last+1:
   starts=max(v['start'],birth) if first else birth;ends=birth+p['life'];events=[birth+n for n in [5,10,15]+list(range(17,p['life'],2))]
   for y in range(max(2026,math.floor(starts)),min(last+1,math.ceil(ends))):
    lo=max(BASE if y==2026 else y,starts);hi=min(y+1,ends)
    if lo>=hi:continue
    dur=hi-lo;mid=(hi+lo)/2;active=365*dur;ds=[d for d in events if lo<=d<hi];rd=max(0,active-p['repair_days']*dur-p['dock_days']*len(ds))
    if y<=2031:rate=p['start'][cl]+(p['detailed_end'][cl]-p['start'][cl])*(y-2027)/4
    else:rate=p['detailed_end'][cl]+(p['normal'][cl]-p['detailed_end'][cl])*min(1,(y-2031)/5)
    ys[y]['tce']+=rate*p['rate_scale']*inflate(y+.5)*rd/1e6
    ys[y]['opex']+=OPEX[cl]*inflate(mid)*(1+p['age_opex']*max(0,mid-birth-15))*active/1e6
    ys[y]['dock']+=sum(DOCK[cl]*(1.25 if d-birth>=15 else 1)*inflate(d)*p['cost_scale'] for d in ds)
    ys[y]['days']+=active
   if 2026<=int(ends)<=last:ys[int(ends)]['scrap']+=COST[cl]*p['scrap']*inflate(ends)
   if not renewal[cl]:break
   for when,fraction in [(ends-2,.2),(ends-1,.2),(ends,.6)]:
    if BASE<=when and int(when)<=last:ys[int(when)]['replace']+=COST[cl]*p['cost_scale']*inflate(ends)*fraction
   birth=ends;first=False
 old_wc=300.5+p['cash_reserve'];out=[]
 for y,d in ys.items():
  dur=.25 if y==2026 else 1;mid=(BASE+y+1)/2 if y==2026 else y+.5;n=d['days']/365/dur
  full=95+sum(v['committed'] and v['start']<=mid for v in fs);ratio=min(1,n/max(1,full))
  admin=(p['ga']+p['incremental_ga']*max(0,full-95))*inflate(mid)*dur*ratio
  other=p['other_gross']*inflate(mid)*dur*ratio
  tax=p['tonnage_tax']*inflate(mid)*dur*n/95
  maintother=p['other_capex']*inflate(mid)*dur*ratio
  rev=p['q4_tce'] if y==2026 else d['tce'];earn=p['q4_ebitda'] if y==2026 else rev-d['opex']-admin+other
  dock=p['q4_drydock'] if y==2026 else d['dock']
  wc=rev/dur*p['wc_pct']+p['cash_reserve']*n/95*inflate(y+1)
  rt=0
  for c in COST:
   final=max(v['built']+p['life'] for v in fs if v['type']==c)
   if not renewal[c] and y<=final<y+1:rt+=45.2*sum(v['type']==c for v in F)/95
  cf=earn-tax-dock-d['replace']+d['scrap']-commit.get(y,0)-(wc-old_wc)-rt-maintother
  out.append(dict(year=y,fcff=cf,pv=cf/(1+p['wacc'])**(mid-VAL),nwc=wc,retirement_tax=rt))
  old_wc=wc
 ev=sum(r['pv'] for r in out);eq=ev+446.2-p['cash_reserve']+p['financial_assets']-p['claims']+p['jv_net']+p['settlement_net']
 return ev,eq/p['shares'],out

check('95 existing hulls',len(F),95);check('MR source count',sum(v['type']=='MR' for v in F),64);check('LR1 source count',sum(v['type']=='LR1' for v in F),9);check('LR2 source count',sum(v['type']=='LR2' for v in F),22);check('Remaining commitments paid exactly once',sum(commit.values()),615.3)
independent={}
for case,r in R.items():
 p=A[case];ev,v,rows=rebuild(p,r['renewal'],max(x['year'] for x in r['rows']))
 check(case+' independently rebuilt EV',ev,r['operating_ev'],1e-6);check(case+' independently rebuilt per share',v,r['per_share'],1e-7)
 for x,y in zip(rows,r['rows']):
  check(f'{case} {x["year"]} independent cashflow',x['fcff'],y['fcff'],1e-6)
  check(f'{case} {x["year"]} independent WC',x['nwc'],y['nwc'],1e-7)
 check(case+' equity bridge',r['operating_ev']+r['bridge']['cash_excess']+25.7-1150.3+p['jv_net']+p['settlement_net'],r['equity'])
 check(case+' published price anchor',r['upside'],r['per_share']/37.64-1)
 if r['terminal']['roic'] is not None:
  t=r['terminal'];check(case+' terminal NOPAT reinvestment identity',t['economic_nopat']*(1-t['g']/t['roic']),t['fcff'],1e-7)
  check(case+' terminal capital return identity',t['economic_nopat']/t['capital_prior'],t['roic'])
  check(case+' explicit tail reconciles decomposition',r['gordon_pv']+r['age_adjustment_pv'],r['tail_pv'])
 check(case+' runoff tax at most whole historical claim',sum(x['runoff_tax'] for x in r['rows'])<=45.20000001,True)
 independent[case]=dict(operating_ev=ev,per_share=v,renewal=r['renewal'])
out={'as_of':'2026-11-05','scope':'Independent rebuild of fleet cashflows, not import/call of author engine. Source/capital/decision judgment separate. Workbook not yet reviewed.','model_hashes':{f:hashlib.sha256((M/f).read_bytes()).hexdigest() for f in ['value.py','assumptions.json','results.json','fleet.json']},'independent_results':independent,'checks':checks,'passed':sum(c['pass_'] for c in checks),'failed':sum(not c['pass_'] for c in checks)}
(P/'checks.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['independent_results','passed','failed']},indent=2))
if out['failed']:
 print([x for x in checks if not x['pass_']][:12]);raise SystemExit(1)
