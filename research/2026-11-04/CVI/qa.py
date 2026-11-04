from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
s=json.loads((P/'summary.json').read_text());r=(P/'report.md').read_text();pc=json.loads((P/'pros_cons.json').read_text());checks=[]
def check(n,v):
 assert v,n
 checks.append({'check':n,'passed':True})
for k in ['fairValue','fairValueTotal','bear','base','bull']:check(k+'_null',s[k] is None)
for k in ['researchComplete','stage3Complete','stage35Approved','entryApproved','calendarGatePassed','technicalGatePassed']:check(k+'_false',s[k] is False)
check('no_unresolved_template','{{' not in r)
check('full_report',len(r.split())>3500)
for group in ['pros','cons']:
 check(group+'_count',1<=len(pc[group])<=3)
 for i,row in enumerate(pc[group]):
  check(group+str(i)+'_evidence',row['evidence'] in r.split('\n\n'))
  check(group+str(i)+'_es_length',len(row['es'])<=320)
  check(group+str(i)+'_en_length',len(row['en'])<=360)
check('no_internal_fs_paths','/workspace/' not in r)
check('scanner_distinct',s['scanPrice']==55.92 and s['lastClose']==48.6)
check('no_false_earnings',s['nextEarningsDate'] is None)
check('partial_scope','PARTIAL' in r and 'no es un precio negativo' in r)
check('roic_limit_disclosed','recuperación cíclica sobre capacidad existente' in r)
check('inventory_funding_open','financiación de inventario' in r)
check('sources_https',len(re.findall('https://',r))>=20)
check('history_qa',json.loads((P/'history/check_results.json').read_text()).get('status')=='PASS')
check('valuation_qa',json.loads((P/'model/valuation_checks.json').read_text())['passed'])
(P/'QA.json').write_text(json.dumps({'passed':True,'count':len(checks),'checks':checks},indent=2));print(len(checks),'package QA PASS')
