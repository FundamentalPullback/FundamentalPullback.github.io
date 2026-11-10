from pathlib import Path
import json,csv
P=Path(__file__).parent
cols=['revenue','ebit','net_income_parent','depreciation','cfo','cash_capex','sbc']
raw={'H1FY2025':[5580.7,-287.8,-322.0,220.8,1872.3,703.1,41.0],'FY2024':[9961.8,3169.7,1727.4,427.9,2780.0,1269.1,63.6],'FY2025':[10208.7,354.9,-81.4,445.7,3152.2,1214.1,72.2],'FY2026':[9139.0,2721.4,1686.7,418.7,2669.0,875.0,67.7],'H1FY2026':[4996.0,1587.8,982.1,207.9,1489.3,410.1,32.1],'H1FY2027':[5065.7,1650.3,1219.6,194.4,1478.6,354.1,34.9],'9MFY2026':[7218.8,2279.8,1484.9,306.9,2106.2,656.1,48.0],'Q1FY2027':[2432.7,845.3,653.8,97.6,661.8,177.2,15.0]}
a={k:dict(zip(cols,v)) for k,v in raw.items()}
def sub(x,y):return {k:round(a[x][k]-a[y][k],4) for k in cols}
a['Q3FY2026']=sub('9MFY2026','H1FY2026');a['Q4FY2026']=sub('FY2026','9MFY2026');a['Q2FY2027']=sub('H1FY2027','Q1FY2027');a['TTM20260831']={k:round(a['FY2026'][k]-a['H1FY2026'][k]+a['H1FY2027'][k],4) for k in cols}
a['TTM20250831']={k:round(a['FY2025'][k]-a['H1FY2025'][k]+a['H1FY2026'][k],4) for k in cols}
for v in a.values():v['simple_fcf']=round(v['cfo']-v['cash_capex'],4)
checks={k:round(sum(a[p][k] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-a['TTM20260831'][k],6) for k in cols};assert all(v==0 for v in checks.values())
d={'currency':'USD millions','raw':raw,'columns':cols,'periods':a,'ttm_quarter_reconciliation':checks,'diagnostics':{'h1_cfo_growth_pct':(1478.6/1489.3-1)*100,'h1_simple_fcf_growth_pct':((1478.6-354.1)/(1489.3-410.1)-1)*100,'q2_ebit_growth_pct':(805/874-1)*100,'q2_net_income_growth_pct':(565.8/466-1)*100,'debt_carrying_august':116.5+1103+9096.2,'net_debt_simple_august':116.5+1103+9096.2-98.5,'ttm_simple_fcf_less_sbc':a['TTM20260831']['simple_fcf']-a['TTM20260831']['sbc'],'illustrative_market_cap':145.9*(169198487+25733)/1e6,'guide_pe_gaap_low':145.9/12.55,'guide_pe_gaap_high':145.9/11.85,'guide_pe_adjusted_low':145.9/11.9,'guide_pe_adjusted_high':145.9/11.2},'limitations':['Depreciation is not D&A; amortization separate in segment disclosures.','Historical scope includes divested wine businesses; no synthetic pro forma organic history.','Simple FCF already includes interest and taxes; not FCFF.','Post-August debt rollover, repurchases and SpikedAde not modeled as current balance.']}
(P/'calculations.json').write_text(json.dumps(d,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+cols+['simple_fcf']);w.writeheader();w.writerows(dict(period=p,**v) for p,v in a.items())
print(json.dumps(d['diagnostics'],indent=2))
