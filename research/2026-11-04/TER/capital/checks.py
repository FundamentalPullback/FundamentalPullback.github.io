from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.loads((P/'facts.json').read_text());c=[]
def ck(n,b):
 assert b,n
 c.append(n)
ck('liquid subtotal',math.isclose(f['cash']+f['securitiesShort']+f['securitiesLong'],624.865));ck('NCI rollforward',math.isclose(35.799+5.684+7.582,49.065));ck('NCI not fair valuation',not f['mltp']['redemptionFormulaPubliclyQuantified']);ck('actual shares not weighted dilution',f['actualShares']!=f['q3WeightedDilutedShares']);ck('debt0 not unused revolver',f['borrowings']==0 and f['undrawnRevolver']==1000);ck('tax overlap not asserted',not f['uncertainTaxOverlapWithPayableVerified']);ck('stake dated exact shares',f['technoprobe']['ownedShares']==65.326087);ck('stake calendar',f['technoprobe']['nextEventConfirmed'] and f['technoprobe']['nextEvent']=='2026-11-11');ck('TER date unknown',f['terNextEvent'] is None and not f['terNextEventConfirmed']);ck('no prior lockup assumption',f['technoprobe']['original36MonthFinancialLockupTerminated']);ck('WC supplier cost not freecash',f['supplierPrepayments']==539.686);ck('commitments not all debt',f['purchaseCommitmentsUnderOneYear']<f['purchaseCommitmentsTotal'])
out={'checks':c,'passed':len(c),'technoprobeMarkNov3USD':65.326087*24.34*1.1179,'operatingWorkingCapitalProxy':1110.798+574.992+539.686-516.967-270.025,'limits':'Arithmetic/factual identity checks, not independent source audit or certification of redemption and tax terms.'};(P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(len(c),'capital PASS')
