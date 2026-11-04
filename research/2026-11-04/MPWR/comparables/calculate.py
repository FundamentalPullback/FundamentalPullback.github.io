import pathlib,json
p=pathlib.Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());o={}
for k,r in x.items():o[k]={**r,'ebit_margin_pct':100*r['ebit']/r['revenue'],'cfo_less_ppe':r['cfo']-r['capex'],'cfo_less_ppe_sbc_sensitivity':r['cfo']-r['capex']-r['sbc']}
r=x['TXN'];o['TXN']['ttm_cfo_less_ppe']=r['ttm_cfo']-r['ttm_capex'];o['TXN']['ttm_no_CHIPS_sensitivity']=r['ttm_cfo']-r['ttm_capex']-r['ttm_ITC_in_CFO'];o['TXN']['ttm_company_fcf_reconcile']=r['ttm_cfo']-r['ttm_capex']+r['ttm_chips_proceeds']
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
