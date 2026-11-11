from pathlib import Path
import json
p=Path(__file__).parent
shares=291;old=5417;fv=156.87
cases={
'old_book_bridge':old,
'principal_only':old+5696-5639,
'principal_and_gross_current_pension':old+57+42,
'principal_current_pension_plus_earnout_proxy':old+57+42+150,
'principal_net_pension_plus_earnout_proxy':old+57+(414-625)+150,
}
r={'modelStatus':'Bounded sensitivities to frozen rounded Oct29 valuation, NOT fullDCFrefresh','referenceClose':217.76,'referenceSession':'2026-11-10 16:00 EST','sharesMillionFrozen':shares,'oldCentralRounded':fv,'oldClaimsMillion':old,'cases':{k:{'claimsMillion':v,'valueDeltaPerShare':-(v-old)/shares,'frozenValueIllustration':fv-(v-old)/shares} for k,v in cases.items()},'capexFY27percentGuidance':6,'oldYear1CapexPercent':5.5,'oldYear1RevenueMillion':22458.7,'oneYearExtraCapexMillion':22458.7*.005,'oneYearOnlyPVDeltaPerShare':-22458.7*.005/1.0975/shares,'pensionLongTerm':625,'pensionCurrent':42,'pensionAssets':253,'netPensionPostRetire':625+42-253,'principalMaturities':[502,571,627,350,650,2996],'earnoutAcquisitionDateFairValueProxy':150,'entryApproved':False,'fullDCFRefreshed':False}
assert sum(r['principalMaturities'])==5696
assert r['netPensionPostRetire']==414
assert 5639-(1697-700)+150+625==old
(p/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
