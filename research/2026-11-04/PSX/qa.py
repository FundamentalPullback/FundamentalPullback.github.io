import json,math,re
from pathlib import Path
P=Path(__file__).resolve().parent;checks=[]
def ck(label,ok):
 checks.append({'check':label,'pass':bool(ok)});assert ok,label
j=lambda f:json.loads((P/f).read_text())
m=j('model/results.json');s=j('summary.json');report=(P/'report.md').read_text();i=j('model/inputs.json');c=j('capital_cycle/facts.json');h=j('history/financial_history.json')
for n in ['bear','base','bull']:ck(n+'summary',abs(m[n]['valuePerShare']-s[n])<1e-8)
for r in h:
 a=r['metrics'];ck(r['period']+'NI',abs(a['pretax_income']-a['tax_expense']-a['nci_income']-a['net_income_parent'])<1e-6)
 ck(r['period']+'FCF',abs(a['cfo']-a['capex_investments']-a['fcf_cfo_minus_capex'])<1e-6)
 ck(r['period']+'CFOwc',abs(a['cfo']-a['wc_cash_effect']-a['cfo_ex_wc'])<1e-6)
 ck(r['period']+'jvdiv',abs(a['equity_earnings']-a['undistributed_equity_earnings']-a['equity_distributions_in_cfo'])<1e-6)
for r in m['base']['rows']:
 ck(str(r['year'])+'table',f"{r['fcff']:,.2f}" in report)
ck('noEntry',s['stage35Approved']==False and s['calendarGatePassed']==False and s['technicalGatePassed']==False)
ck('newScanNotOld',s['scanDate']=='2026-11-03' and s['opportunity']==70 and s['originalAnalysisScanDate']=='2026-10-27')
ck('close',s['lastClose']==271.94 and s['lastCloseDate']=='2026-11-03')
ck('debt',c['balance']['debtCurrent']+c['balance']['debtNoncurrent']==18530)
ck('propel',c['legal']['propelAccruedSeptember']==947)
ck('quarterMarginBridge',6031+96+249+55+1166+1-161+15==7452)
ck('barrels',abs(196.088*365/92-777.9578260869565)<1e-8)
ck('reportIRS','https://www.irs.gov/credits-deductions/clean-fuel-production-credit' in report)
ck('noSubsidyRenewal',i['scenarios']['base']['renewableEbit2031Real2027']==0)
ck('reverse',abs(j('model/sensitivities.json')['reverse']['roots'][0]['value']-271.94)<1e-7)
ck('modelChecks',j('model/valuation_checks.json')['failed']==0)
if (P/'pros_cons.json').exists():
 pc=j('pros_cons.json')
 for side in ['pros','cons']:
  ck(side+'count',1<=len(pc[side])<=3)
  for ix,p in enumerate(pc[side]):
   ck(side+str(ix)+'evidence',p['evidence'] in report)
   ck(side+str(ix)+'esLength',len(p['es'])<=320)
   ck(side+str(ix)+'enLength',len(p['en'])<=360)
   if p.get('sourceUrl'):ck(side+str(ix)+'url',p['sourceUrl'] in report)
(P/'qa_results.json').write_text(json.dumps({'passed':len(checks),'failed':0,'scope':'Author arithmetic, scope, evidence and presentation checks; not independent source certification.','checks':checks},indent=2)+'\n')
print(len(checks),'package checks PASS')
