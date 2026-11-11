"""September-perimeter sensitivity and required 37South contribution, not a combined-company DCF.
All amounts USD million; model preserves historical operating paths and varies explicitly selected capital assumptions.
"""
import json
from pathlib import Path
B=Path(__file__).parent
L=json.loads((B/'legacy/model_outputs.json').read_text());S=L['shares'];BR=L['net_bridge'];PRICE=157.58

def calc(path='central',mode='funded',rate=None,first_growth=None,margin_shift=0):
 c=L['cases'][path];W=c['wacc'] if rate is None else rate;G=c['g'];gs=c['growth'][:] if first_growth is None else [first_growth]*5;gs += [gs[-1]+(G-gs[-1])*i/5 for i in range(1,6)];ms=[v+margin_shift for v in c['margin']]+[c['margin'][-1]+margin_shift]*5;sales=881.242;oldnop=165.339*.75;rows=[]
 for y,(g,m) in enumerate(zip(gs,ms),1):
  prior=sales;sales*=1+g;n=sales*m*.75;wc=(sales-prior)*.15;ri=c['roic']+(c['terminal_roic']-c['roic'])*max(0,y-5)/5
  net=max(max(0,n-oldnop)/ri,wc) if mode=='funded' else wc
  cf=n-net;rows.append(dict(year=y,sales=sales,margin=m,nopat=n,net_investment=net,fcff=cf,pv=cf/(1+W)**y));oldnop=n
 tn=oldnop*(1+G);tw=sales*G*.15;ti=max(tn*G/c['terminal_roic'],tw) if mode=='funded' else tw;tf=tn-ti;pvterm=tf/(W-G)/(1+W)**10;ev=sum(r['pv'] for r in rows)+pvterm;val=(ev+BR)/S
 return dict(path=path,mode=mode,rate=W,terminal_growth=G,first_growth=first_growth,margin_shift=margin_shift,rows=rows,terminal_fcff=tf,terminal_pv=pvterm,terminal_fraction=pvterm/ev,ev=ev,net_bridge=BR,shares=S,value=val,required_net_deal_value=(PRICE-val)*S)

def inverse(mode,rate):
 lo=0;hi=.5
 for _ in range(100):
  mid=(lo+hi)/2
  if calc(mode=mode,rate=rate,first_growth=mid)['value']<PRICE:lo=mid
  else:hi=mid
 x=calc(mode=mode,rate=rate,first_growth=(lo+hi)/2)
 return dict(mode=mode,rate=rate,required_y1_5_growth=(lo+hi)/2,year10_sales=x['rows'][-1]['sales'],value=x['value'])
if __name__=='__main__':
 cases={k:calc(**v) for k,v in {'oldcentral':{},'oldfavorable':{'path':'favorable'},'oldadverse':{'path':'adverse'},'efficientcentral':{'mode':'efficient'},'efficientfavorable':{'path':'favorable','mode':'efficient'},'fundedcentral_obs':{'rate':.077142},'efficientcentral_obs':{'mode':'efficient','rate':.077142},'efficientfavorable_obs':{'path':'favorable','mode':'efficient','rate':.077142},'efficientcentral_939':{'mode':'efficient','rate':.0939},'efficientfavorable_939':{'path':'favorable','mode':'efficient','rate':.0939}}.items()}
 # Acquired operations value must cover consideration + incremental integration/claims + current quote gap.
 deals=[]
 for case in ['oldcentral','oldfavorable','efficientcentral','efficientfavorable']:
  gap=cases[case]['required_net_deal_value']
  for purchase in [0,25,50,100]:
   gross=gap+purchase
   deals.append(dict(case=case,hypothetical_purchase_cost=purchase,required_net_deal_value=gap,required_acquired_gross_value=gross,illustrative_perpetual_fcff_at_9pct_g25=gross*(.09-.025)))
 out=dict(price=PRICE,price_date='2026-11-10 16:00 EST',shares=S,net_bridge=BR,perimeter='September2026 excludes37South; no asserted currentcombinedintrinsicvalue',cases=cases,deals=deals,inverses=[inverse(m,r) for m,r in [('funded',.09),('efficient',.09),('efficient',.0939),('efficient',.077142)]],assumptions={'efficient':'Capex replaces all D&A; no netcashinvestment except15% incrementalrevenue workingcapital; no freefuture M&A. Generousbenchmark, not verifiedcapitalbudget.','deal':'Purchase numbers0/25/50/100 are illustrative, not estimates of terms. Deduct purchase once whetherfundedcashordebt; debtissuance not addedfreeequity. Ongoingcontribution incrementalaftertaxafterreinvestment.'})
 (B/'results.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(out['inverses'])
