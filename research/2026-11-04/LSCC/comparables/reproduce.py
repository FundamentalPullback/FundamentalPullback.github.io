from pathlib import Path
import json
p=Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());a=x['AMD_Embedded'];m=x['MCHP'];o={'amd_embedded_growth':a['revenue']/a['prior_revenue']-1,'amd_segment_margin_not_gaap':a['segment_operating_income']/a['revenue'],'mchp_gaap_margin':m['gaap_operating_income']/m['revenue'],'mchp_adjusted_margin_not_gaap':m['adjusted_operating_income']/m['revenue']};(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
