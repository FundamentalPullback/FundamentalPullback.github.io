from pathlib import Path
import json
P=Path(__file__).parent
rows=[dict(ticker='CL',price=95.62,shares_m=794.920513,cash=1527,debt=7716,revenue=21285,ebit_reported=3161,ebit_norm_low=4080,ebit_norm_high=4503,cfo=4366,capex=577,sbc=169,period='2026-09-30'),dict(ticker='GIS',price=34.08,shares_m=534.687144,cash=433.1,debt=13615.6,revenue=18296.6,ebit_reported=-206.4,ebit_norm_low=2563.2,ebit_norm_high=2734.3,cfo=2067,capex=520.9,sbc=86.1,period='2026-08-30, 53 weeks'),dict(ticker='CHWY',price=22.05,shares_m=401.927249,cash=612.2,debt=600,revenue=13068.7,ebit_reported=328.2,ebit_norm_low=328.2,ebit_norm_high=328.2,cfo=717.2,capex=149.1,sbc=297.9,period='2026-08-02')]
for r in rows:
 r['nci_book_proxy']={'CL':352.0,'GIS':13.4,'CHWY':0.0}[r['ticker']]
 r['marketcap']=r['price']*r['shares_m'];r['ev_before_other_claims']=r['marketcap']+r['debt']-r['cash'];r['ev_nci_book_proxy']=r['ev_before_other_claims']+r['nci_book_proxy'];r['ev_sales']=r['ev_nci_book_proxy']/r['revenue'];r['ev_ebit_low']=r['ev_nci_book_proxy']/r['ebit_norm_high'];r['ev_ebit_high']=r['ev_nci_book_proxy']/r['ebit_norm_low'];r['cash_fcf']=r['cfo']-r['capex'];r['cash_fcf_less_sbc']=r['cash_fcf']-r['sbc'];r['pcf_after_sbc']=r['marketcap']/r['cash_fcf_less_sbc'];r['yield_after_sbc']=r['cash_fcf_less_sbc']/r['marketcap']
(P/'comps.json').write_text(json.dumps({'price_date':'2026-11-03 regular close','rows':rows,'limitations':'Approximate equity/debt EV including explicitly labeled NCI book proxies (market values unknown), before currently unquantified CHWY finance leases and employee award dilution, actual common snapshots dated. No operating lease adjustment; rent remains expense. Peer note required.'},indent=2))
for r in rows:print(r)
