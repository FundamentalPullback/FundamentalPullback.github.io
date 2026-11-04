"""Reconstruct A119 SPSC printed assumptions and reconcile to new model. Prior report is preserved, not silently overwritten."""
from pathlib import Path
import json
from model import model,BASE
P=Path(__file__).parent
def old_model(shares=36.6,growth=[.06,.06,.055,.05,.04],margins=[.17,.18,.19,.20,.20],terminal_margin=.20,roic=.25):
 rev=787.9;pv=0;ratio5=None
 for i in range(1,11):
  a=max(0,(i-5)/5);g=growth[i-1] if i<=5 else growth[-1]*(1-a)+.025*a;mar=margins[i-1] if i<=5 else margins[-1]*(1-a)+terminal_margin*a;prev=rev;rev*=1+g;n=rev*mar*.75
  if i<=5:reinv=(rev-prev)*.10;ratio5=reinv/n
  else:reinv=n*(ratio5*(1-a)+(.025/roic)*a)
  pv+=(n-reinv)/(1.1**i)
 terminal_nopat=rev*1.025*terminal_margin*.75
 ev=pv+terminal_nopat*(1-.025/roic)/(.10-.025)/(1.1**10)
 return (ev+133.501)/shares
steps=[('A119 reconstructed; same Q3 information set',old_model()),('Replace annual guidance diluted average36.6 with Q3 diluted36.209',old_model(shares=36.209)),('Replace initial growth assumptions only',old_model(shares=36.209,growth=BASE['growth'])),('Replace operating margin basis/path and terminal margin only',old_model(shares=36.209,growth=BASE['growth'],margins=BASE['cash_margin'],terminal_margin=.23)),('Change terminal ROIC25% to20%',old_model(shares=36.209,growth=BASE['growth'],margins=BASE['cash_margin'],terminal_margin=.23,roic=.20)),('Replace reinvestment with explicit capex/working capital/ROIC funding and transition',model(BASE)['value'])]
out=[];prev=None
for label,v in steps:out.append({'step':label,'value':v,'change':None if prev is None else v-prev});prev=v
(P/'migration_bridge.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
assert abs(out[0]['value']-49.73)<.005
assert abs(out[-1]['value']-52.88941934089687)<1e-8
