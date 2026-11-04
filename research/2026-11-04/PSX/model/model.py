"""PSX current-fleet operating FCFF + affiliate equity cash flow. USD millions."""
import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent
INPUT=json.loads((P/'inputs.json').read_text())
def run(name='base', changes=None):
 d=copy.deepcopy(INPUT); s=d['scenarios'][name]; c=d['common']; b=d['capital']
 for key,value in (changes or {}).items():
  group,k=key.split('.',1); {'scenario':s,'common':c,'capital':b}[group][k]=value
 assert s['wacc']>s['g'] and s['jvKe']>s['g'] and s['g']<min(s['roic'],s['jvRoe'])
 rows=[]; prevnop=c['priorOperatingNopatAnchor']; prevjv=c['priorJvAfterParentTaxAnchor']; prevrev=c['revenue2026Anchor']; op_pv=0; jv_pv=0; previous_segments=None
 for i in range(10):
  year=2027+i; fade=min(i/4,1); infl=(1+c['costInflation'])**i
  vol=s['volume2027']*(1+s['volumeAnnualChange'])**i
  margin=(s['margin2027']+(s['margin2031Real2027']-s['margin2027'])*fade)*infl
  refining_da=1000*infl
  refining_ebit=vol*margin-s['refiningCashCost2027']*infl-refining_da
  mid=s['midstreamEbit2027']*((1+c['costInflation'])*(1+s['midstreamRealGrowth']))**i
  marketing=s['marketingEbit2027']*((1+c['costInflation'])*(1+s['marketingRealGrowth']))**i
  renewable=(s['renewableEbit2027']+(s['renewableEbit2031Real2027']-s['renewableEbit2027'])*min(i/3,1))*infl
  corporate=s['corporateEbit2027']*infl
  ebit=refining_ebit+mid+marketing+renewable+corporate
  nopat=ebit*(1-c['tax']) # no tax asset for aggregate losses below zero
  if ebit<0: nopat=ebit
  da=c['da2027']*infl
  revenue=c['revenue2027Proxy']*(1+c['revenueNominalGrowth'])**i
  wc=max(revenue-prevrev,0)*c['workingCapitalIncrementalRevenueFraction']
  replacement_net=da*c['netReplacementFloorDaFraction']
  segment_nopats=[v*(1-c['tax']) if v>=0 else v for v in [refining_ebit,mid,marketing,renewable,corporate]]
  growth_investment=(sum(max(now-old,0) for now,old in zip(segment_nopats,previous_segments))/s['roic'] if previous_segments is not None else max(nopat-prevnop,0)/s['roic'])
  net_invest=max(replacement_net+wc,growth_investment,c['capitalSpendingFloor2027']*infl-da+wc)
  capex=da+net_invest-wc
  fcff=nopat+da-capex-wc
  jve=(s['jvEarnings2027']+(s['jvEarnings2031Real2027']-s['jvEarnings2027'])*fade)*infl
  jv_tax=jve*s['jvParentTax']; jv_after=jve-jv_tax
  project_retention=jve*(s['jvProjectRetention2027'] if i==0 else s['jvProjectRetention2028'] if i==1 else 0)
  jv_reinvest=max(project_retention,max(jv_after-prevjv,0)/s['jvRoe'])
  jv_cash=jve-jv_tax-jv_reinvest
  t=c['year1DiscountDays']/365+i
  pv=fcff/(1+s['wacc'])**t; jvpv=jv_cash/(1+s['jvKe'])**t
  op_pv+=pv;jv_pv+=jvpv
  rows.append(dict(year=year,phase='normalization' if i<5 else 'mature',revenueProxy=revenue,processedMillionBarrels=vol,refiningMarginUsdBarrel=margin,refiningEbit=refining_ebit,midstreamEbit=mid,marketingEbit=marketing,renewableEbit=renewable,corporateEbit=corporate,operatingEbitExJv=ebit,nopat=nopat,da=da,capex=capex,workingCapitalInvestment=wc,growthInvestmentFloor=growth_investment,netReinvestment=net_invest,fcff=fcff,jvEquityIncome=jve,jvIncrementalParentTax=jv_tax,jvRetainedCapital=jv_reinvest,jvEquityCashFlow=jv_cash,discountYears=t,fcffPv=pv,jvPv=jvpv))
  prevnop=nopat;prevjv=jv_after;prevrev=revenue;previous_segments=segment_nopats
 last=rows[-1]; nextnop=last['nopat']*(1+s['g']); nextda=last['da']*(1+s['g']); nextwc=last['revenueProxy']*s['g']*c['workingCapitalIncrementalRevenueFraction']
 terminal_capex_floor=c['capitalSpendingFloor2027']*(1+c['costInflation'])**9*(1+s['g'])
 terminal_reinvest=max(nextnop*s['g']/s['roic'],nextda*c['netReplacementFloorDaFraction']+nextwc,terminal_capex_floor-nextda+nextwc)
 terminal_fcff=nextnop-terminal_reinvest
 terminal_jv_after=last['jvEquityIncome']*(1+s['g'])*(1-s['jvParentTax'])
 terminal_jv_reinvest=terminal_jv_after*s['g']/s['jvRoe']
 terminal_jv_cash=terminal_jv_after-terminal_jv_reinvest
 tvop=terminal_fcff/(s['wacc']-s['g']);tvjv=terminal_jv_cash/(s['jvKe']-s['g'])
 tvoppv=tvop/(1+s['wacc'])**last['discountYears'];tvjvpv=tvjv/(1+s['jvKe'])**last['discountYears']
 stubop=rows[0]['fcff']*c['stubDays']/365/(1+s['wacc'])**(c['stubDays']/365) if c['stubEnabled'] else 0
 stubjv=rows[0]['jvEquityCashFlow']*c['stubDays']/365/(1+s['jvKe'])**(c['stubDays']/365) if c['stubEnabled'] else 0
 operations_value=op_pv+tvoppv+stubop; jv_value=jv_pv+tvjvpv+stubjv
 debtlike=sum(b[k] for k in ['debtCarrying','operatingCashReserve','nciEconomicProxy','employeeNoncurrentReserve','employeeCurrentStaleProxy','aroEnvironmentalNoncurrent','aroEnvironmentalCurrentStaleProxy','propelAccrued','taxUtbStaleReserve','receivableRemittancePrudence','additionalHistoricalTaxWcReserve'])
 bridge=b['cash']-debtlike+b['unknownPostSeptemberNetCapital']+b['otherNoncoreAssetsAdded']
 shares=b['sharesActual']+b['vestedUnissuedProxy']+b['incrementalDilutionProxy']
 equity=operations_value+jv_value+bridge
 return {'scenario':name,'assumptions':s,'rows':rows,'operatingExplicitPv':op_pv,'jvExplicitPv':jv_pv,'operatingTerminalPv':tvoppv,'jvTerminalPv':tvjvpv,'operatingStubPv':stubop,'jvStubPv':stubjv,'operationsValue':operations_value,'jvEquityValue':jv_value,'capitalBridge':bridge,'equityValue':equity,'sharesMillions':shares,'valuePerShare':equity/shares,'terminalOperatingNopat':nextnop,'terminalOperatingReinvestment':terminal_reinvest,'terminalOperatingFcff':terminal_fcff,'terminalJvAfterParentTax':terminal_jv_after,'terminalJvReinvestment':terminal_jv_reinvest,'terminalJvCash':terminal_jv_cash,'terminalShareGrossValues':(tvoppv+tvjvpv)/(operations_value+jv_value),'upsideToReferenceClose':equity/shares/INPUT['price']-1}
if __name__=='__main__':
 out={k:run(k) for k in INPUT['scenarios']}
 (P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for n,x in out.items():
  with (P/f'{n}_10_years.csv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(x['rows'][0]));w.writeheader();w.writerows(x['rows'])
 print({k:round(v['valuePerShare'],4) for k,v in out.items()})
