import json
from pathlib import Path
p=Path(__file__).parent;h=json.loads((p/'history.json').read_text());n=json.loads((p/'normalization_inputs.json').read_text());a=n['acquiredAmortization'];current=a['FY2026']+a['H1FY27']-a['H1FY26'];prior=a['FY2025']+a['H1FY26']-a['H1FY25'];out={}
for per,am in [('TTM20260930',current),('TTM20250930',prior)]:
 r=h[per];out[per]={'gaapEbit':r['ebit'],'acquiredAmort':am,'ebitBeforeAcquiredAmort':r['ebit']+am,'remainingPhysicalSoftwareDa':r['da']-am,'cashTax':r['cashTax'],'fcfReported':r['fcf'],'cashTaxAt26pctReportedPretax':(r['netIncome']+r['tax'])*.26,'fcfTaxTimingIllustration':r['fcf']+r['cashTax']-(r['netIncome']+r['tax'])*.26}
out['FY2025IllustrativeOperatingNormalization']={'revenue':h['FY2025']['revenue']-113,'ebit':h['FY2025']['ebit']-113-115,'basis':'Remove claimed-cost release113 and insurance115; other costs retained. Both occur before the two SeptemberTTM windows; do not subtract them again from current/prior TTM.'}
assert current==61;assert prior==52
(p/'normalization.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
