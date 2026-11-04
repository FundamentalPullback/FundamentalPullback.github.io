import json,math
from pathlib import Path
from model import run,I
p=Path(__file__).parent;checks=[]
def ck(x,label):
 assert x,label
 checks.append(label)
for k,c in I['cases'].items():
 r=run(k);ck(len(r['rows'])==10,k+' ten years')
 for a in r['rows']:
  ck(abs(a['nopat']+a['physicalSoftwareDa']-a['impliedGrossCapex']-a['workingCapitalGrowth']-a['legacyWcFunding']-a['otherInvestment']-a['fcff'])<1e-8,k+str(a['year'])+' FCFF identity')
  ck(a['impliedGrossCapex']+1e-8>=a['grossCapexFloor'],k+str(a['year'])+' physical floor')
  ck(a['totalNetInvestment']+1e-8>=a['economicNetInvestment'],k+str(a['year'])+' economic floor')
 t=r['terminal'];ck(t['netInvestment']>=max(t['economicReinvestment'],t['physicalReinvestment'])-1e-8,k+' terminal floor');ck(c['discount']>c['terminalGrowth'],k+' convergence');ck(r['totalFairValue'] is None,k+' no total certification')
 for floor in [1,1.25,1.5,2]:
  a=run(k,{'capexDaFloor':floor})['terminal'];ck(a['netInvestment']>=a['physicalReinvestment']-1e-8,k+str(floor)+' stress terminal physical')
ck(run('bear')['conditionalPositivePrice'] is None,'negative residual is not share price')
ck(abs(I['anchorEbitBeforeAcquiredAmort']-(303.2-28.3+28))<1e-8,'partial operating anchor')
ck(abs(I['physicalSoftwareDaRatio']*18923.7-(82.6-28))<1e-8,'DA separation')
(p/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks))
