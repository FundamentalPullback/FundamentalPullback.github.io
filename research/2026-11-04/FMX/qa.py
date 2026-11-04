import json,math,pathlib,re,csv
P=pathlib.Path(__file__).parent;checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
def eq(n,a,b):ck(n,math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7))
s=json.load(open(P/'summary.json'));r=json.load(open(P/'model/results.json'));i=json.load(open(P/'model/inputs.json'));txt=(P/'report.md').read_text();pc=json.load(open(P/'pros_cons.json'))
for k in ['fairValue','bear','base','bull']:ck('full_value_unavailable.'+k,s[k] is None)
for k in ['stage3Complete','stage35Approved','entryApproved','calendarGatePassed','earningsDateConfirmed']:ck('no_gate.'+k,s[k] is False)
for key in ['pros','cons']:
 ck('1to3.'+key,1<=len(pc[key])<=3)
 for ix,z in enumerate(pc[key]):
  ck(f'evidence_exact.{key}.{ix}',z['evidence'] in txt);ck(f'evidence_contiguous_paragraph.{key}.{ix}','\n' not in z['evidence']);ck(f'es_length.{key}.{ix}',len(z['es'])<=320);ck(f'en_length.{key}.{ix}',len(z['en'])<=360);ck(f'url_in_report.{key}.{ix}',z['sourceUrl'] in txt)
for name,v in r.items():
 eq('summary_partial.'+name,s['partialIdentifiedAssetValuation'][name],v['partial_value_per_fmx_ads_usd']);ck('report_value.'+name,f"{v['partial_value_per_fmx_ads_usd']:,.2f}" in txt)
# Capital identities, avoiding wrong consolidation and future dividend double counts.
o=json.load(open(P/'ownership/ownership_minimal_inputs.json'));c=i['capital'];eq('ex_kof_cash',c['ex_kof_cash'],111063.060-46772.350);eq('net_pension_exKOF',c['pension_reserve'],11265.440-5719.002);eq('Spin_customer_claim',c['spin_customer_reserve'],4781.191+92.017);eq('kof_stake_ads',o['kof']['femsa_stake_ads_equivalent'],7936628152/80)
eq('KOF_normalized_rent_EBIT',i['anchors']['kof']['economic_ebit_after_rent_estimated'],44706.809-2462+1130-1535)
eq('exKOF_DA_proxy',i['anchors']['ex_kof']['da_total_estimated'],46031-14847.269-(15895-13837.995))
# Derive exKOF dividend and KOF cash reduction independently using public share rights.
fmx_div=(1968615615*3.202925+1417048500*2.669125)/1e6;kof_div=16806658096*.241875/1e6;kof_in=7936628152*.241875/1e6
eq('October_KOF_dividend',-c['known_post_september_kof_dividend'],kof_div);eq('October_exKOF_dividend',c['known_post_september_ex_kof_dividends_estimated'],kof_in-fmx_div)
for z in json.load(open(P/'history/validation_checks.json')):ck('history.'+z['check'],z['passed'])
v=json.load(open(P/'model/valuation_checks.json'));ck('all_model_checks',v['passed']==v['total'])
# Peer numerator and denominator arithmetic from own inputs.
a=json.load(open(P/'comps/atd_inputs.json'));ar=json.load(open(P/'comps/atd_results.json'));eq('ATD_legal_normalization',ar['normalized_ebit'],4727.8-260.9);eq('ATD_EVEBIT',ar['ev_normalized_ebit'],ar['ev_usdm']/ar['normalized_ebit']);w=json.load(open(P/'comps/walmex_inputs.json'));wr=json.load(open(P/'comps/walmex_results.json'));eq('Walmex_TTM_EBIT',wr['ttm']['ebit'],78494+54174.470-55176.765);eq('Walmex_EV',wr['ev'],50.04*17137.424318+5676.271+78343.7+3953.525-27064.984)
for source in s['sources'].values():ck('https.'+source,source.startswith('https://'))
# Every scenario/segment has ten published yearly rows and proper after-rent convention.
for name in r:
 for seg in ['ex_kof','kof']:
  rows=list(csv.DictReader(open(P/'model'/f'{name}_{seg}_10years.csv')));ck(f'10yrCSV.{name}.{seg}',len(rows)==10)
res={'passed':sum(z['pass'] for z in checks),'total':len(checks),'checks':checks,'scope':'Arithmetic, reporting identity and reproducibility checks, not investment or entry approval.'};(P/'qa_results.json').write_text(json.dumps(res,indent=2)+'\n');print(res['passed'],'/',res['total']);assert res['passed']==res['total'],[z for z in checks if not z['pass']]
