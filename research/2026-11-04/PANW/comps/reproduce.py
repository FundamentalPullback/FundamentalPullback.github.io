#!/usr/bin/env python3
"""Offline operational comparisons; Python standard library only."""
import pathlib,json,csv
P=pathlib.Path(__file__).resolve().parent;i=json.loads((P/'inputs.json').read_text());r=i['reported'];out=[]
for p,d0 in r.items():
 if 'revenue' not in d0:continue
 d=dict(d0);company=p.split('_')[0];year=int(p[-4:]);quarter='Q' in p
 row={'period':p,'company':company,'period_start':f'{year}-07-01' if quarter and company!='PANW' else f'{year}-01-01' if company=='CHKP' else f'{year}-05-01' if quarter else f'{year-1}-08-01','period_end':f'{year}-07-31' if company=='PANW' else f'{year}-09-30','months':3 if quarter else 9 if company=='CHKP' else 12,'revenue':d['revenue'],'ebit':d['ebit'],'cfo':d['cfo']}
 if company=='CHKP':
  spend=-sum(d[k] for k in ['ppe_signed','prepaid_lease_signed','software_signed']);sbc=d['sbc_cf'];adj=d['acquisition_cost_addback'];companyfcf=d['adjusted_fcf_reported']
 elif company=='PANW':
  spend=d['capital_spend'];sbc=r[f'PANW_FY{year}']['sbc_cf']-(r[f'PANW_9MFY{year}']['sbc_cf'] if quarter else 0);adj=sum(d[k] for k in ['hq_capex_addback','corporate_asset_addback','acquisition_cost_addback','litigation_cash_addback']);companyfcf=d['adjusted_fcf_reported']
 else:
  spend=d['capital_spend'];sbc=d['sbc_cf'];adj=-d['nonrecurring_receipt_excluded'];companyfcf=d['company_fcf_reported']
 fcf=round(d['cfo']-spend,6);assert abs(fcf-d['fcf_reported'])<.01,p;assert abs(fcf+adj-companyfcf)<.01,p
 row.update(capital_spend_deducted=round(spend,6),sbc_cf=round(sbc,6),fcf_before_company_adjustments=fcf,company_adjustment=round(adj,6),company_fcf=companyfcf,gaap_operating_margin=round(d['ebit']/d['revenue'],8),sbc_cf_to_revenue=round(sbc/d['revenue'],8),fcf_before_adjustments_margin=round(fcf/d['revenue'],8),company_fcf_margin=round(companyfcf/d['revenue'],8),fcf_before_adjustments_less_sbc_sensitivity=round(fcf-sbc,6))
 out.append(row)
(P/'operating_comparables.json').write_text(json.dumps({'as_of':i['as_of'],'units':i['units'],'comparability':'Descriptive only; different fiscal periods, acquisitions, grants and FCF definitions. No peer multiples or DCF.','periods':out,'sources':i['sources']},indent=2)+'\n')
with (P/'operating_comparables.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
(P/'checks.json').write_text(json.dumps({'status':'PASS','tests':['Every disclosed FCF reconciles to CFO less stated capital spending','Every company FCF reconciles to explicit adjustments','PANW quarter cash-flow SBC derived from annual less nine months, distinct from SBC-related operating charges'],'records':len(out)},indent=2)+'\n')
for d in out:
 if d['months']==3 and d['period'].endswith('2026'):print(d)
