import pathlib,json
p=pathlib.Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());o={}
for k,r in x.items():
 o[k]={**r,'ebit_margin_pct':100*r['ebit']/r['revenue'],'cfo_less_ppe':r['cfo']-r['ppe'],'capex_share_cfo_pct':100*r['ppe']/r['cfo']}
 if k=='MRVL':o[k]['cash_after_license_and_sbc_sensitivity']=r['cfo']-r['ppe']-r['license_purchases']-r['license_payments']-r['sbc']
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
