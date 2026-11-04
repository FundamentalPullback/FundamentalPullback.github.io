from pathlib import Path
import json
p=Path(__file__).resolve().parent;x=json.loads((p/'inputs.json').read_text());out=[]
for a in x['quarterlyOperating']:
 b=dict(a);b['normalizedEbitPartial']=a['ebit']-a['refund_ebit'];b['priorNormalizedEbitPartial']=a['prior_ebit']-a['prior_nonrecurring_operating_gain']+a.get('prior_charges_added',0);b['normalizedMarginPct']=100*b['normalizedEbitPartial']/a['revenue'];b['revenueGrowthPct']=100*(a['revenue']/a['prior_revenue']-1);out.append(b)
a=x['kssRelative'];ev=a['price']*a['coverShares']+a['notesBook']-a['cash'];rel={'evExAllLeasesBookNotes':ev,'multipleBeforeFullCashRent':ev/a['normalizedEbitBeforeAllRent'],'multipleAfterFullCashRent':ev/a['normalizedEbitAfterAllRent'],'warning':'Accounting/book-note capital proxy, dated shares and balances, no selected reserves. M comparator not fully reconciled after-cash-rent; no target median.'}
(p/'results.json').write_text(json.dumps({'operating':out,'kssRelative':rel},indent=2)+'\n')
assert out[0]['normalizedEbitPartial']==out[0]['priorNormalizedEbitPartial']==161
print('Operating and relative arithmetic PASS')
