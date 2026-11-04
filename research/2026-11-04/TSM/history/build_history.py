"""Reproduce TSM history. Manually transcribed primary statement inputs; units NTD million.
Annual inputs: SEC 2025 20-F F6-F13. Interim inputs: issuer financial statements pp4-8.
Missing fields remain None, never implicitly zero. Run python build_history.py.
"""
import json,pathlib
P=pathlib.Path(__file__).parent
keys='revenue ebit pretax_income tax_expense net_income net_income_parent eps_diluted cfo depreciation amortization capex_ppe capex_intangibles sbc interest_income finance_costs interest_received interest_paid lease_principal cash_rou_acquisitions'.split()
def row(values):
 assert len(values)==len(keys),(len(values),len(keys))
 return dict(zip(keys,values))
data={
'FY2023':row([2161735.8,921465.6,979316.5,128288.8,851027.7,851740.0,32.85,1241967.3,522932.7,9258.2,949816.8,5518.4,483.0,60293.9,11999.4,55887.2,17359.0,2854.3,None]),
'FY2024':row([2894307.7,1322053.0,1405840.0,248316.1,1157523.9,1158380.2,44.67,1826177.1,653610.5,9186.1,956006.5,8875.7,1242.7,87213.4,10495.4,76434.1,18751.2,2873.7,None]),
'FY2025':row([3809054.3,1936091.7,2041654.7,346529.8,1695124.9,1697604.0,65.47,2274975.6,679684.0,8412.4,1272410.5,10146.9,1246.1,105739.1,12370.4,98954.7,19128.8,3496.5,None]),
'9M2024':row([2025846.521,896340.137,957040.631,159077.760,797962.871,798587.976,30.80,1205971.785,485541.546,6876.767,594058.374,5827.476,735.748,62940.059,7972.185,57961.207,12804.370,2212.890,None]),
'9M2025':row([2762963.851,1371189.264,1449299.639,239318.192,1209981.447,1212138.637,46.75,1549466.838,519704.707,6279.555,915504.525,5594.917,1073.063,76231.655,9326.937,72794.719,13778.562,2612.337,None]),
'Q12026':row([1134103.440,658966.142,687799.687,114998.383,572801.304,572479.752,22.08,698976.265,163312.605,2137.832,350762.799,933.027,113.979,28862.263,2716.862,26745.717,2747.192,1328.422,None]),
'H12026':row([2404483.690,1425568.793,1550229.773,270647.546,1279582.227,1279041.690,49.32,1482341.242,359541.458,4447.147,846764.746,3876.352,237.026,58906.984,5801.911,52546.142,9889.408,2249.689,9441.034]),
'9M2026':row([3898727,2302014,2461269,418346,2042923,2042106,78.75,2402117,None,None,1289971,None,None,None,None,88095,14704,None,None]),
'Q32026':row([1494243,876445,911039,147698,763341,763064,29.43,919776,None,None,443206,None,None,None,None,35549,4815,None,None]),
}
# Preserve original inputs before derived measures.
(P/'source_inputs.json').write_text(json.dumps(data,indent=2)+'\n')
for r in data.values():
 r['da']=None if r['depreciation'] is None else round(r['depreciation']+r['amortization'],3)
data['9M2026']['da']=584192
data['Q32026']['da']=220204
# EPS sums/differences are approximate: rounded diluted EPS and weighted averages are not additive.
def combine(terms):
 out={}
 for k in data['FY2025']:
  vals=[data[p][k] for p,s in terms]
  out[k]=None if any(v is None for v in vals) else round(sum(data[p][k]*s for p,s in terms),3)
 return out
data['Q42025']=combine([('FY2025',1),('9M2025',-1)])
data['Q22026']=combine([('H12026',1),('Q12026',-1)])
# Use reported quarterly EPS rather than difference of rounded H1 EPS.
data['Q22026']['eps_diluted']=27.25
data['TTM2026Q3']=combine([('FY2025',1),('9M2025',-1),('9M2026',1)])
data['TTM2025Q3']=combine([('FY2024',1),('9M2024',-1),('9M2025',1)])
for r in data.values():
 r['fcf_ppe_only_reported_cfo']=round(r['cfo']-r['capex_ppe'],3)
 r['fcf_ppe_intangibles_reported_cfo']=None if r['capex_intangibles'] is None else round(r['cfo']-r['capex_ppe']-r['capex_intangibles'],3)
 r['cfo_after_interest_paid']=round(r['cfo']-r['interest_paid'],3)
 r['operating_margin']=r['ebit']/r['revenue']
 r['effective_tax_rate']=r['tax_expense']/r['pretax_income']
 r['eps_adr_ntd_approx']=round(5*r['eps_diluted'],3)
meta={'units':'NTD millions except diluted EPS NTD per ordinary share and ratios','adr_ratio':5,'periods':data,'last_four_quarters':['Q42025','Q12026','Q22026','Q32026'],'derivation':{'Q42025':'FY2025 - 9M2025','Q22026':'H12026 - Q12026, except directly reported quarterly diluted EPS','TTM2026Q3':'FY2025 - 9M2025 + 9M2026','TTM2025Q3':'FY2024 - 9M2024 + 9M2025'},'limitations':['Q32026 and 9M2026 condensed statements rounded to NTD millions; FY statements rounded to 0.1M; full interim statements converted from NTD thousands to millions. Derived values do not acquire extra source precision.','TTM diluted EPS is approximate arithmetic roll-forward, not recalculated weighted-average EPS. ADR NTD EPS uses rounded ordinary EPS x5; source exact ADR may differ. No USD conversion mixed into history.','Q32026 SBC, intangible capex, lease principal, gross interest income/finance costs and cash ROU acquisitions not separately disclosed in condensed release. Corresponding TTM fields null. Do not call PPE-only FCF total FCF or owner earnings.','CFO excludes interest paid (financing) and interest received (investing). Lease principal is financing; cash ROU acquisition is investing. Annual and Q1 cash ROU acquisitions not separately presented, hence null rather than zero.','Gross PPE capex not netted against government grants or US investment tax credits. Investing inflows do not increase CFO.']}
(P/'history.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({p:data[p] for p in ['TTM2026Q3','TTM2025Q3']},indent=2))
