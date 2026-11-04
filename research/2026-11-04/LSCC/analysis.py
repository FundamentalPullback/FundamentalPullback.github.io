from pathlib import Path
import json
p=Path(__file__).parent
f=json.loads((p/'facts/inputs.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text())
a={'ticker':'LSCC','units':'USD millions except per share','classification':'partial','bear':None,'base':None,'bull':None,'owner_fcf':None,'equity_bridge':None,'next_earnings_date':None}
a.update({'q3_revenue_growth':f['q3_revenue']/f['q3_prior_revenue']-1,'q3_fpga_growth':f['q3_fpga_revenue']/f['q3_prior_revenue']-1,'q3_gaap_margin':f['q3_ebit']/f['q3_revenue'],'nine_month_cfo_less_ppe':f['cfo9']-f['ppe9'],'nine_month_after_software':f['cfo9']-f['ppe9']-f['software9'],'nine_month_after_software_sbc':f['cfo9']-f['ppe9']-f['software9']-f['sbc9'],'nominal_net_debt_oct3':f['debt_principal']-f['cash'],'purchase_price_tie':f['stock_consideration']+f['cash_consideration']+f['purchase_payable']+f['ami_debt_retired'],'acquisition_cash_net':f['cash_consideration']+f['ami_debt_retired']-f['acquired_cash'],'historical_share_market_cap_proxy':f['price']*f['actual_shares_oct29'],'q3_unallocated_segment_cost':f['q3_fpga_segment_ebit']+f['q3_ami_segment_ebit']-f['q3_ebit']})
a['capital_note']='Nominal debt less cash is a balance-sheet diagnostic, not an integral distributable equity bridge. Shares at Oct29, price Nov4.'
(p/'analysis.json').write_text(json.dumps(a,indent=2)+'\n')
