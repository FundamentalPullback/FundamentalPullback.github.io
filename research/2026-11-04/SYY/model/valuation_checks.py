import json,math
from pathlib import Path
from model import run,INPUT
P=Path(__file__).resolve().parent;out=json.loads((P/'results.json').read_text());checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
def eq(n,a,b):ck(n,math.isclose(a,b,abs_tol=1e-7,rel_tol=1e-10))
for c,r in out.items():
 for who in ['syy','jrd']:
  a=INPUT['scenarios'][c][who];b=INPUT['businesses'][who];prev=b['revenueAnchor'];pn=b['ebitAnchor']*(1-b['tax']);ck(c+who+' length',len(r[who]['rows'])==10)
  for z,row in enumerate(r[who]['rows']):
   n=c+who+str(z);eq(n+'revenue',row['revenue'],prev*(1+a['growth'][z]));eq(n+'nopat',row['nopat'],row['ebitAfterSbcBeforeAcquiredAmort']*(1-b['tax']));eq(n+'cash identity',row['fcff'],row['nopat']+row['daPhysical']-row['grossCapitalSpending']-row['wcInvestment']-row['otherGrowthInvestment']);ck(n+'fund margin growth',row['netReinvestment']+1e-8>=max(row['nopat']-pn,0)/a['roic']);ck(n+'physical floor',row['grossCapitalSpending']>=row['daPhysical']);eq(n+'pv',row['pv'],row['fcff']/(1+a['wacc'])**(z+1));prev=row['revenue'];pn=row['nopat']
  ck(c+who+' wacc>g',a['wacc']>a['g']);eq(c+who+' terminal funding',r[who]['terminalFcff'],r[who]['terminalNopat']-r[who]['terminalNetReinvestment']);eq(c+who+' EV',r[who]['enterpriseValue'],r[who]['explicitPv']+r[who]['terminalPv'])
 eq(c+'closing shares',r['conditionalImmediateCloseShares'],585.5)
 eq(c+'close per share',r['conditionalImmediateCloseValuePerShare'],r['conditionalImmediateCloseEquity']/585.5)
 ck(c+'no current total',r['totalCurrentFairValue'] is None)
 eq(c+'failure fee differential',r['standaloneBeforeFailureCosts']-r['conditionalFailureValuePerShare'],r['conditionalRegulatoryFailureCosts']/494)
 # Acquired business and consideration each counted once. Seller shares excluded from failure.
 z=run(c,{'transaction.economicCashFreeDebtFreeBase':22600});eq(c+'purchase price sensitivity',r['conditionalImmediateCloseValuePerShare']-z['conditionalImmediateCloseValuePerShare'],1000/585.5);eq(c+'failure not cash purchase',r['conditionalFailureValuePerShare'],z['conditionalFailureValuePerShare'])
comp=run('base',{'businesses.jrd.additionalAnnualCompPreTax':45});plain=run('base');
for a,b in zip(plain['jrd']['rows'],comp['jrd']['rows']):eq(str(a['period'])+' extra retention cash tax',a['nopat']-b['nopat'],45*(1-.275))
eq('retention not failure liability',plain['conditionalFailureValuePerShare'],comp['conditionalFailureValuePerShare'])
s=json.loads((P/'sensitivities.json').read_text());ck('inverse monotonic',s['conditionalCloseReverse']['monotonic'])
for k in s['conditionalCloseReverse']['roots']:eq('inverse target',k['closeValue'],74.11)
result={'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks};(P/'valuation_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],'checks',result['failed'],'failed');assert not result['failed']
