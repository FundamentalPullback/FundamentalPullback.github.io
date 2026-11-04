from pathlib import Path
import json,math
p=Path(__file__).resolve().parent
s=json.loads((p/'summary.json').read_text());r=(p/'report.md').read_text();a=json.loads((p/'analysis/results.json').read_text());h=json.loads((p/'history/financial_history.json').read_text())
checks=[]
def check(v,label):
 assert v,label
 checks.append(label)
for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases']:check(s[k] is None,k+' null')
for k in ['entryApproved','stage3Complete','stage35Approved','latestCompletedEligible']:check(s[k] is False,k+' false')
for side in ['pros','cons']:
 check(1<=len(s[side])<=3,side+' count')
 for i,x in enumerate(s[side]):
  check(x['evidence'] in r,side+str(i)+' exact evidence')
  check(len(x['textEs'])<=320,side+str(i)+' ES length')
  check(len(x['textEn'])<=360,side+str(i)+' EN length')
check(s['latestClose']==118.15 and s['scanPrice']==116.5,'price separation')
check(s['scanStage2Current'] is None,'no inherited Stage2')
check(s['nextEvent']['date'] is None,'calendar unconfirmed')
check(a['priceOnlyScenarios']['higher']['grossRevenueChange']==1397.5,'gross sensitivity1397.5')
check(a['tenYearDcf'] is None and a['inverseDcf'] is None,'no invented valuation')
check(h['periods']['TTM2026-09']['fcf_cfo_less_capex']==10074,'TTM FCF')
check(h['periods']['TTM2026-09']['sbc_expense'] is None,'SBC gap')
check('118,2 Moz' in r and '21 Moz' in r,'reserve perimeter explicit')
check('no se publica un DCF' in r,'methodology gap explicit')
check('HOLD' not in r,'report no internal coordination')
(p/'qa_results.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n')
print(str(len(checks))+' package checks PASS')
