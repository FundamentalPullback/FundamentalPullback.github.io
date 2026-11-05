from pathlib import Path
import json
from html.parser import HTMLParser
P=Path(__file__).parent;S=json.loads((P/'summary.json').read_text());A=json.loads((P/'analysis.json').read_text());N=json.loads((P/'normalization_qa.json').read_text());R=(P/'report.md').read_text();H=(P/'report.html').read_text()
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append(tag)
p=Tags();p.feed(H)
checks={'normalized_math':N['passed'],'current_value_fields_null':all(S[k] is None for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases','ownerFCF','certifiedEquityBridge','scenarioEconomicsOnly']),'no_entry_completion':all(S[k] is False for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']),'no_earnings_date_invented':S['nextEarningsConfirmed'] is None and not S['nextEvent']['isEarnings'],'legacy_analysis_null':all(A[k] is None for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge']),'credit_disclosed':'4.393' in R and '370' in R,'cash_sensitivity_not_owner_fcf':'Ninguna cifra es owner FCF normalizado' in R,'issuer_source_discrepancy':'1.833' in R and '1.883' in R,'ownership_denominators':'49,55%' in R and '48,6%' in R,'quarterly_eps_not_derived':'No se fabrica EPS Q4 o TTM' in R,'pending_notes_not_booked':'no se agregan a deuda o caja' in R,'no_unverified_contract_reconciliation':'No se ha conciliado' in R,'html_structure':p.tags.count('h1')==1 and p.tags.count('table')==1 and p.tags.count('tr')==10 and p.tags.count('th')==8 and p.tags.count('td')==72,'html_selfcontained':'<script'not in H,'sufficient_depth':len(R.split())>2800}
(P/'qa.json').write_text(json.dumps({'passed':all(checks.values()),'checks':checks},indent=2,sort_keys=True)+'\n');assert all(checks.values()),checks;print('QA',checks)
