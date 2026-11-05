from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());t=(p/'report.md').read_text()
r=dict(ticker='HRI',as_of='2026-11-04',research_cutoff=f['cutoff'],scanner_date='2026-11-04',scanner_price=f['scanner_price'],price=f['price_reference'],price_date=f['price_date'],certified_close=None,price_note='Scanner Last 158.41 versus StockAnalysis regular close 158.10. Distinct references, no single certified close.',research_status='Partial factual research; independently audited within this partial scope',bear=None,base=None,bull=None,buy_ceiling=None,owner_fcf=None,equity_bridge=None,bridge_certified=False,wacc_calibrated=False,approved_entry=False,stage35_approved=False,latestCompleted=False,decision_es='Observación: conciliar reposición de flota y desapalancamiento antes de valorar; no entrada.',decision_en='Watch: reconcile fleet replacement and deleveraging before valuation; no entry.',publication_note='Reported cash FCF is not owner cash. Fleet purchase payables, lease classification, H&E comparability and current capital remain to be reconciled. All valuation fields null; next earnings date unconfirmed.')
r['pros_es']=[];r['pros_en']=[];r['cons_es']=[];r['cons_en']=[]
for line in t.splitlines():
 for prefix,key in [('- ES favorable: ','pros_es'),('- EN favorable: ','pros_en'),('- ES riesgo: ','cons_es'),('- EN risk: ','cons_en')]:
  if line.startswith(prefix):r[key].append(line[len(prefix):])
(p/'publication.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
