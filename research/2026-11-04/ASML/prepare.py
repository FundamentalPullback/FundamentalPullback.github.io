from pathlib import Path
import json
P=Path(__file__).parent;m=json.load(open(P/'model.json'));r=(P/'report.md').read_text()
pros=['Las ventas TTM aumentan 22,54 % y el EBIT 35,56 %, con mejora operativa que no depende de la revalorización Mistral.','La expansión de capacidad y las nuevas condiciones de precio pueden sostener crecimiento, aunque su ejecución y calendario no están garantizados.']
# Keep exact source passage capitalization.
pros=[r.split('**A favor:** ')[i].split('\n')[0] for i in [1,2]]
cons=[r.split('**En contra:** ')[i].split('\n')[0] for i in [1,2,3]]
pe=['TTM revenue rose 22.54% and operating EBIT 35.56%; the operating improvement does not depend on the Mistral revaluation.','Capacity expansion and new pricing terms can support growth, although execution and timing are not guaranteed.']
ce=['TTM FCF includes EUR 7,876.9m of aggregate asset and liability changes; it is not a certified recurring cash-flow rate.','The USD 1,552.14 close exceeds the USD 954.98 central case; the reverse model needs approximately 27.10% revenue growth in years 2–5 under the other base assumptions.','Current capital, strategic asset valuation, applicable rules and the next earnings date remain unresolved; there is no entry approval.']
pub=dict(ticker='ASML',as_of='2026-11-04',research_cutoff='2026-11-04 17:58 UTC',price=1552.14,price_timestamp='2026-11-03 16:00 America/New_York',base=round(m['cases']['base']['value'],2),bear=round(m['cases']['bear']['value'],2),bull=round(m['cases']['bull']['value'],2),research_status='Conditional research reconstruction; not integral Stage3. Independently audited for conditional research only.',decision_es='Esperar precio o evidencia; capital, normativa y calendario pendientes.',decision_en='Wait for price or evidence; capital, regulation and calendar remain open.',approved_entry=False,stage35_approved=False,buy_ceiling=None,pros_es=pros,cons_es=cons,pros_en=pe,cons_en=ce,publication_note='Preserve A033 historical reconstruction and original Oct 12 scanner 1765.96. No current scan fabricated; Nov 3 close 1552.14 separate. No portfolio or execution changes. Not latestCompleted/integral certification.')
json.dump(pub,open(P/'publication.json','w'),indent=2,ensure_ascii=False)
# Separate bilingual evidence appendix generated exactly from metadata.
a='\n## Appendix: English evidence summary\n\n'+'\n\n'.join(pe+ce)+'\n';(P/'english_evidence.md').write_text(a)
