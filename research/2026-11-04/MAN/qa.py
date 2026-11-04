from pathlib import Path
import json,math,re
P=Path(__file__).parent;checks=[]
def ck(v,s):
 assert v,s
 checks.append(s)
s=json.loads((P/'summary.json').read_text());r=json.loads((P/'model/results.json').read_text());i=json.loads((P/'model/inputs.json').read_text());t=(P/'report.md').read_text();h=json.loads((P/'history/ttm_comparison.json').read_text())[-1];se=json.loads((P/'model/sensitivities.json').read_text())
for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases']:ck(s[k] is None,'null '+k)
for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']:ck(s[k] is False,'false '+k)
for k in ['pros','cons']:
 for a in s[k]:
  ck(a['evidence'] in t,k+' contiguous evidence');ck(len(a['es'])<=320,k+' ES length');ck(len(a['en'])<=360,k+' EN length');ck(a['sourceUrl'] in t,k+' source')
ck(abs(h['cfo']-h['capex_including_software']-7.4)<1e-8,'TTM FCF');ck(abs(h['ebit']-28.3-274.9)<1e-8,'sale gain correction');ck(abs(i['anchorEbitBeforeAcquiredAmort']-302.9)<1e-8,'beforeamort anchor');ck(abs(i['physicalSoftwareDaRatio']*18923.7-54.6)<1e-8,'DA residual')
ck(i['bridge']['selectedOtherClaims']==0,'no double restructuring reserve');ck(i['bridge']['selectedOperatingCash']==233.1,'cash reserve explicit');ck(s['lastClose']==46.94 and s['scanPrice']==55.87,'dated prices separated');ck(s['nextEarningsConfirmed'] is None,'no guessed earnings');ck(not s['nextEvent']['isEarnings'],'conference not earnings')
for k,v in r.items():
 ck(v['totalFairValue'] is None,k+' total null');ck(len(v['rows'])==10,k+' ten years');ck(math.isfinite(v['economicResidualPerShareProxy']),k+' finite residual')
ck(r['bear']['conditionalPositivePrice'] is None,'deficit not price');ck(abs(se['inverse']['residualError'])<1e-8,'inverse residual');ck(abs(se['inverseEfficiencyAlternative']['residualError'])<1e-8,'alternative residual');ck(not se['inverse']['fundingCertified'],'no inverse financing assertion')
(P/'qa_results.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks))
