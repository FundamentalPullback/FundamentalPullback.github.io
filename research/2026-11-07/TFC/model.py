import json,pathlib
p=pathlib.Path(__file__).parent
B=46.78; P=49.38
out={'method':'Residual income sobre patrimonio común; excepción bancaria documentada antes de calcular','status':'partial_not_decision_grade','book_value_per_share':B,'price':P,'scenarios':{},'assumptions':'Hipótesis ilustrativas, no guidance; capital distribuible pendiente. Sin caja excedente ni deuda restada de nuevo; SBC permanece en beneficio.'}
for name,r,k,g in [('adverso',.08,.11,.02),('central',.10,.10,.025),('favorable',.12,.095,.03)]:
 book=B; rows=[]
 for y in range(1,11):
  earn=book*r; retain=book*g; dist=earn-retain; ri=earn-k*book
  rows.append(dict(year=y,opening_book=book,roe=r,earnings=earn,retention=retain,distribution=dist,residual_income=ri,pv_ri=ri/(1+k)**y))
  book+=retain
 terminal=book*(r-k)/(k-g); pvterminal=terminal/(1+k)**10
 value=B+sum(x['pv_ri'] for x in rows)+pvterminal
 ddm=sum(x['distribution']/(1+k)**x['year'] for x in rows)+book*(r-g)/(k-g)/(1+k)**10
 assert abs(value-ddm)<1e-8
 out['scenarios'][name]=dict(roe=r,ke=k,g=g,payout=1-g/r,value=value,pv_terminal_residual=pvterminal,ddm_crosscheck=ddm,rows=rows)
out['inverse']=[dict(ke=k,g=g,required_sustainable_roe=g+(P/B)*(k-g)) for k,g in [(.095,.02),(.10,.025),(.11,.025)]]
discount=json.loads((p/'discount_evidence.json').read_text())
out['discount_reference']=discount
out['sensitivity']=[dict(ke=k,roe=r,g=.025,value=B*(r-.025)/(k-.025)) for k in [discount['raw_CAPM'],.09,.095,.10,.11,.12] for r in [.08,.10,.12]]
json.dump(out,open(p/'model.json','w'),indent=2,ensure_ascii=False)
# Las series contables verificadas se conservan como entradas; el motor no las sobrescribe.
financials=json.loads((p/'financials.json').read_text())
normalization=json.loads((p/'normalization_v2.json').read_text())
for period, key in [('2025-09-30','ttm_to_20250930'),('2026-09-30','ttm_to_20260930')]:
 assert financials[key]['normalized_continuing_common'] == normalization['paired_ttm'][period]['normalized_continuing_common']
print({k:round(v['value'],2) for k,v in out['scenarios'].items()})
