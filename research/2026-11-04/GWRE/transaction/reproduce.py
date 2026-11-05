from pathlib import Path
import json
p=Path(__file__).parent;i=json.loads((p/'facts.json').read_text());rows=[]
for earnout in [0,200,400]:
 for fees in [0,25,50]:
  dcash=i['committedTermLoan']-i['baseCashConsideration']-earnout-fees;ddebt=i['committedTermLoan'];net=dcash-ddebt;assert net==-i['baseCashConsideration']-earnout-fees
  rows.append({'selectedEarnout':earnout,'selectedFees':fees,'cashDelta':dcash,'debtDelta':ddebt,'netCapitalDeltaBeforeTargetValue':net,'targetValue':None,'isTotalFairValue':False})
(p/'funding_cases.json').write_text(json.dumps(rows,indent=2)+'\n')
