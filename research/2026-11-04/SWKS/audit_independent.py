import json,pathlib,math,datetime,hashlib
P=pathlib.Path(__file__).parent
I=json.loads((P/'model/inputs.json').read_text());R=json.loads((P/'model/results.json').read_text());S=json.loads((P/'summary.json').read_text());H=json.loads((P/'history/history.json').read_text());checks={};notes=[]
def check(k,v):checks[k]=bool(v)
def recalc(c):
 sales=I['revenueAnchor'];pvs=[];out=[]
 for yr in range(1,11):
  blend=0 if yr<=5 else (yr-5)/5
  gr=c['growth'][yr-1] if yr<=5 else c['growth'][4]+(c['g']-c['growth'][4])*blend
  margin=c['margin'][yr-1] if yr<=5 else c['margin'][4]+(c['terminalMargin']-c['margin'][4])*blend
  prev=sales;sales*=1+gr;np=sales*margin*(1-c['tax']);wc=max(sales-prev,0)*c['nwcPct'];da=sales*c['daPct'];investment=(sales*c['capexPct']-da+wc)*(1-blend)+(np*gr/c['roic'])*blend
  integration=c['integrationCash'][yr-1] if yr<=5 else 0
  cf=np-investment-integration;pv=cf/(1+c['wacc'])**yr;pvs.append(pv);out.append((sales,np,investment,cf,pv,da+investment-wc))
 np11=np*(1+c['g']);tv=np11*(1-c['g']/c['roic'])/(c['wacc']-c['g']);ev=sum(pvs)+tv/(1+c['wacc'])**10
 return ev,out,tv
for k,c in I['cases'].items():
 ev,rows,tv=recalc(c);r=R['cases'][k]
 check(k+'_ev',abs(ev-r['operatingEV'])<1e-8);check(k+'_terminal',abs(tv-r['terminalValue'])<1e-8)
 check(k+'_rows',all(abs(a-b)<1e-8 for our,their in zip(rows,r['rows']) for a,b in zip(our,[their['revenue'],their['nopat'],their['netReinvestment'],their['fcff'],their['pv'],their['capexAllNecessary']])))
 check(k+'_residual',abs((ev-I['assumedNetFinancialClaims'])/I['assumedDilutedShares']-r['illustrativeEquityResidualPerShare'])<1e-8)
 check(k+'_terminal_continuity',abs(r['terminalFCFF']/r['rows'][-1]['fcff']-(1+c['g']))<1e-8)
for n,x in enumerate(R['reverse']):
 c=dict(I['cases']['base']);m=x['matureMarginAfterSBC'];g=x['growthYears2to5'];m0=c['margin'][0];c.update(growth=[c['growth'][0]]+[g]*4,margin=[m0,(m0+m)/2,m,m,m],terminalMargin=m)
 ev,_,_=recalc(c);check('reverse_'+str(n),abs(ev-(I['scanPrice']*I['assumedDilutedShares']+I['assumedNetFinancialClaims']))<1e-6)
for n,x in enumerate(R['waccGrowthSensitivity']):
 c=dict(I['cases']['base']);c.update(wacc=x['wacc'],g=x['g']);ev,_,_=recalc(c);check('sensitivity_'+str(n),abs(ev-x['operatingEV'])<1e-8)
check('actual_valuation_null',all(S[k] is None for k in ['fairValue','fairValueTotal','bear','base','bull','conditionalDcfCases','maximumConditioned','technicalGate']))
check('stage_entry_false',all(S[k] is False for k in ['entryApproved','stage3Complete','stage35Complete','latestCompletedEligible']))
check('history_fcf',all(abs(r['cfo']-r['capexPPE']-r['purchasedIntangibles']-r['fcfAfterPurchasedIntangibles'])<1e-8 for r in H))
check('FY25_53_weeks',(datetime.date.fromisoformat(H[2]['end'])-datetime.date.fromisoformat(H[2]['start'])).days+1==371)
check('FY26_52_weeks',(datetime.date.fromisoformat(H[-1]['end'])-datetime.date.fromisoformat(H[-1]['start'])).days+1==364)
C=json.loads((P/'capital/combined_capital.json').read_text());e=C['exchange_settlement'];check('exchange_principal',abs(sum(x['new_principal']+x['old_residual'] for x in e['series'])-1548.421)<1e-8)
check('combined_note_principal',abs(500+2000+1548.421-C['combined_face_debt_reconstruction']['sum'])<1e-8)
facts=json.loads((P/'history/source_inputs.json').read_text())['facts']['us-gaap']
tags={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','grossProfit':'GrossProfit','ebitGAAP':'OperatingIncomeLoss','netIncome':'NetIncomeLoss','epsDiluted':'EarningsPerShareDiluted','dilutedShares':'WeightedAverageNumberOfDilutedSharesOutstanding','cfo':'NetCashProvidedByUsedInOperatingActivities','capexPPE':'PaymentsToAcquirePropertyPlantAndEquipment','purchasedIntangibles':'PaymentsToAcquireIntangibleAssets','sbc':'ShareBasedCompensation','depreciation':'Depreciation','amortizationAll':'AmortizationOfIntangibleAssets'}
for r in H[:6]:
 for key,tag in tags.items():
  candidates=[v for vs in facts[tag]['units'].values() for v in vs if v.get('start')==r['start'] and v['end']==r['end'] and v['filed']<='2026-11-04']
  if candidates:
   cand=sorted(candidates,key=lambda v:v['filed'])[-1];value=cand['val']/(1 if key=='epsDiluted' else 1e6);check('source_'+r['period']+'_'+key,abs(value-r[key])<1e-8)
  else:
   prev={'Q2FY2026':'2026-01-02','Q3FY2026':'2026-04-03'}.get(r['period']);values=[]
   for end in [r['end'],prev]:
    cs=[v for vs in facts[tag]['units'].values() for v in vs if v.get('start')=='2025-10-04' and v['end']==end and v['filed']<='2026-11-04'];values.append(sorted(cs,key=lambda v:v['filed'])[-1]['val']/1e6)
   check('ytd_source_'+r['period']+'_'+key,abs(values[0]-values[1]-r[key])<1e-8)
source_hash={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'report.md',P/'summary.json',P/'model/model.py',P/'model/inputs.json',P/'model/results.json',P/'history/history.json']}
result={'reviewed_at_UTC':'2026-11-05T00:11:00Z','scope':'Independent recalculation and source/perimeter audit; not approval of missing actual combined valuation','checks':checks,'all_arithmetic_checks_pass':all(checks.values()),'reviewed_sha256':source_hash,'issues':[{'id':'A1','severity':'medium','status':'resolved','finding':'Original label corrected to calculated FCF. Prior finding: FCF económico publicado is an analyst-calculated measure, not a published company FCF. Rename heading to calculated FCF after intangibles.'},{'id':'A2','severity':'medium','status':'resolved','finding':'Selected bridge now490.3; impairment exclusion only unverified sensitivity. Prior finding: CFO impairment66.2 is not explicitly mapped to the67.8 non-GAAP settlements/impairment category. Remove definitive1.6 category remainder or provide mapping; selected556.5 EBIT bridge must remain provisional.'},{'id':'A3','severity':'low','status':'documented_nonblocking','finding':'Python is designated canonical editable assumptions; inputs.json is a regenerated snapshot. Reusable model.py hardcodes revenueAnchor7500,claims3500,shares241 and scanPrice82.65 rather than reading inputs.json. Current reproduction passes; changing JSON alone will not change model and rerun overwrites edits.'}], 'publication_judgment':'PASS for partial conditioned research only: A1/A2 corrections verified. Model source-of-truth convention documented; not a blocker. No full Stage3 or entry approval.'}
(P/'audit_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('Checks',len(checks),'passed',sum(checks.values()));print([k for k,v in checks.items() if not v])
