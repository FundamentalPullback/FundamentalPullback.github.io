from pathlib import Path
import json,itertools,math
p=Path(__file__).resolve().parents[1];x=json.loads((p/'facts/inputs.json').read_text());c=x['capital'];q=x['q3'];a=x['economicBreakEvenAssumptions'];checks=[]
commit=sum(t['amount'] for t in x['commitments']['schedule'])
assert math.isclose(commit,1295.9);checks.append('remaining capex includes JV and totals1295.9')
convert=c['convertiblePrincipal']*c['conversionSharesPer1000']/1000
assert math.isclose(convert,6.0978555);checks.append('conversion uses USD millions consistently')
def hypothetical_claims(gross_asset_value):
 # The asset value is an input illustration, not this company's estimated EV.
 debt_res=(gross_asset_value-c['debtPrincipal'])/c['sharesOct26']
 physical=(gross_asset_value-c['bankDebt'])/(c['sharesOct26']+convert)
 # combination price solves N*P + max(C*P-605,0) = assets - all principal.
 combo=debt_res if debt_res<=c['convertiblePrincipal']/convert else physical
 incr=max(convert-c['convertiblePrincipal']/combo,0) if combo>0 else 0
 assert abs(c['sharesOct26']*combo+max(convert*combo-c['convertiblePrincipal'],0)-(gross_asset_value-c['debtPrincipal']))<1e-7
 return {'hypotheticalGrossAssetValue':gross_asset_value,'notAnEstimatedEV':True,'parOnlyPerShare':debt_res,'fullConversionPerShare':physical,'defaultCombinationPerShare':combo,'incrementalSharesUnderCombination':incr,'optionTimeValueIncluded':False}

def econ(fleet,rates,gna=160,life=25,salvage=.1,days=350,tax=.02,cost_scale=1,opex_scale=1):
 n=sum(fleet.values());cash_opex=0;rev=0;renewal=0
 for cls,count in fleet.items():
  operating=count-(1 if cls=='MR' else 0)
  rev+=operating*days*rates[cls]/1e6
  cash_opex+=operating*365*a['opexPerDay'][cls]*opex_scale/1e6
  renewal+=count*a['replacementCost'][cls]*cost_scale*(1-salvage)/life
 rev+=a['bareboatRate']*a['bareboatDays']/1e6
 drydock=n*a['drydockPerVessel']
 # Replacement reserve is an economic proxy, not a contemporaneous GAAP deduction or actual capex.
 pre_tax_economic=rev-cash_opex-gna-drydock-renewal
 diagnostic_tax=max(pre_tax_economic,0)*tax
 return {'fleetCount':n,'TCERevenue':rev,'operatingCost':cash_opex,'GNAIncludingSBC':gna,'drydockProxy':drydock,'annualEconomicReplacementCharge':renewal,'preTaxEconomicSurplus':pre_tax_economic,'selectedTaxStress':diagnostic_tax,'economicSurplusAfterSelectedTax':pre_tax_economic-diagnostic_tax,'uniformDailyTCEBreakEven':(cash_opex+gna+drydock+renewal-a['bareboatRate']*a['bareboatDays']/1e6)*1e6/((n-1)*days),'notActualFCFF':True,'notOwnerCash':True,'notFairValue':True}
post=x['fleet']['postPendingSales'];grown=dict(post)
for k,v in x['fleet']['newbuilds'].items():grown[k]=grown.get(k,0)+v
assert sum(post.values())==72 and sum(grown.values())==89;checks.append('conditional fleet72 plus17 equals89')
cases={k:{'postSale72':econ(post,rates),'afterAllDirectNewbuild89':econ(grown,rates)} for k,rates in a['selectedClassRates'].items()}
sens=[]
for gna,life in itertools.product(a['GNASensitivity'],a['lifeSensitivity']):
 e=econ(post,a['selectedClassRates']['base'],gna=gna,life=life)
 sens.append({'GNA':gna,'lifeYears':life,'breakEvenDailyTCE':e['uniformDailyTCEBreakEven'],'surplus':e['economicSurplusAfterSelectedTax']})
other_sens=[]
for var,vals in [('salvage',[0,.1,.2]),('days',[330,350,360]),('cost_scale',[.8,1,1.2]),('opex_scale',[.9,1,1.15]),('tax',[0,.02,.1])]:
 for val in vals:
  e=econ(post,a['selectedClassRates']['base'],**{var:val});other_sens.append({'variable':var,'value':val,'breakEvenDailyTCE':e['uniformDailyTCEBreakEven'],'surplus':e['economicSurplusAfterSelectedTax']})

book=x['q4Bookings']
# Q4 blended rate calculator only: no annualization and no incremental equity value.
q4=[]
for label,unbooked in [('zero_unfixed',{'LR2':0,'MR':0,'Handy':0}),('weaker',{'LR2':35000,'MR':22000,'Handy':18000}),('q3_spot_reference',{'LR2':72283,'MR':31183,'Handy':24253}),('booked_rates_persist',{'LR2':181000,'MR':56000,'Handy':40000})]:
 vals={}
 for cls,b in book.items():
  if not isinstance(b,dict):continue
  vals[cls]=(b['spotExpectedDays']*(b['spotCoverage']*b['spotRate']+(1-b['spotCoverage'])*unbooked[cls])+b['tcDays']*b['tcRate']+b.get('bareboatDays',0)*b.get('bareboatRate',0))/1e6
 q4.append({'case':label,'unfixedSpotDailyRates':unbooked,'TCEByClass':vals,'TCERevenue':sum(vals.values()),'notGuidance':True,'notGuaranteedMinimum':True})

out={'valuation':None,'bear':None,'base':None,'bull':None,'ownerFCF':None,'certifiedEquityBridge':None,'entryApproved':False,'historicalCashBridge':{'Oct26Cash':c['cashOct26'],'principalDebt':c['debtPrincipal'],'netCash':c['cashOct26']-c['debtPrincipal'],'remainingCapexIncludingJV':commit,'cashLessDebtAndAllCommitments':c['cashOct26']-c['debtPrincipal']-commit,'declaredDividendProxy':c['sharesOct26']*c['dividendPerShare'],'selectedOperatingReserve':c['operatingReserveSelected'],'afterDividendAndSelectedReserve':c['cashOct26']-c['debtPrincipal']-commit-c['sharesOct26']*c['dividendPerShare']-c['operatingReserveSelected'],'pendingSalesGross':c['pendingVesselSalesGross'],'notNAV':True,'notAvailableCashCertification':True},'convertible':{'conversionPrice':1000/c['conversionSharesPer1000'],'fullConversionShares':convert,'physicalTotalShares':c['sharesOct26']+convert,'examples':[hypothetical_claims(v) for v in [4000,6000,8000]]},'earningsQuality':{'reportedEBIT':q['ebitReported'],'vesselGain':q['gainVessel'],'EBITExVesselGain':q['ebitReported']-q['gainVessel'],'EBITDAPostSBCExVesselGain':q['ebitReported']-q['gainVessel']+q['da'],'reportedNI':q['niReported'],'lessVesselGain':-q['gainVessel'],'addFinancialLiabilityFairValueLoss':q['fairValueLiabilityLoss'],'issuerAdjustedNIRebuilt':q['niReported']-q['gainVessel']+q['fairValueLiabilityLoss'],'issuerAdjustedDilutedEPSRebuilt':q['adjustedIfConvertedNumerator']/q['adjustedIfConvertedShares'],'adjustedEPSUsesDifferentDenominator':True},'economicBreakEvenCases':cases,'breakEvenSensitivity':sens,'otherSensitivity':other_sens,'q4BookingArithmetic':q4,'limits':['No ten-year FCFF DCF or reverse valuation: fleet cohort replacement schedule, normalized forward rates, JV ownership economics and award dilution are not closed.','Economic replacement charge is an analytical smoothing proxy. It is not actual capex or a certified economic life; do not deduct it a second time on top of scheduled newbuild/replacement capex.','All total valuation fields stay null. Scenario labels refer to daily-rate diagnostics, never equity prices.','Two sales are pending;72vessel scope is conditional. Existing time-charter contracts are not repriced by these normalized uniform-rate exercises. They are neither next-year guidance nor cash forecasts.','G&A and tax estimates are analyst stress assumptions. US shipping tax exemptions and their potential loss require separate modeling.','Price date is November4. Draft completed November5 UTC using sources through November4.']}
assert abs(out['earningsQuality']['issuerAdjustedNIRebuilt']-q['issuerAdjustedNI'])<1e-9
assert abs(out['earningsQuality']['EBITDAPostSBCExVesselGain']-151.758)<1e-9
checks+=['NI bridge127.359','postSBC operating EBITDA151.758','no DCF or price encoded']
(p/'model/results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(p/'model/qa.json').write_text(json.dumps({'pass':True,'checks':checks},indent=2)+'\n')
print('Capital, earnings and economic sensitivity checks PASS')
