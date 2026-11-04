import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent;INPUT=json.loads((P/'inputs.json').read_text())
def run(name='base',changes=None):
 x=copy.deepcopy(INPUT);s=x['scenarios'][name];c=x['common'];b=x['capital']
 for key,val in (changes or {}).items():
  group,k=key.split('.',1);{'scenario':s,'common':c,'capital':b,'root':x}[group][k]=val
 assert s['wacc']>s['g']>=0 and s['roic']>s['g']
 rows=[];prevrev=x['revenueAnchor2026'];prevnop=prevrev*x['normalizedMarginAnchor']*(1-c['cashTaxRate']);pv=0
 for z in range(10):
  year=2027+z;rev=prevrev*(1+s['growth'][z]);margin=s['margin2027']+(s['margin2031']-s['margin2027'])*z/4 if z<=4 else s['margin2031']+(s['margin2036']-s['margin2031'])*(z-4)/5
  sbc_memo_ratio=s['sbcMemo2027']+(s['sbcMemo2036']-s['sbcMemo2027'])*z/9
  leadership=c['newLeadershipTargetChargeTotal']/len(c['newLeadershipChargeYears']) if year in c['newLeadershipChargeYears'] else 0
  ebit_pre_acq=rev*margin-leadership;memo_amort=c['acquiredAmortMemo'][z];ebit_gaap_memo=ebit_pre_acq-memo_amort
  tax=ebit_pre_acq*c['cashTaxRate'];nopat=ebit_pre_acq-tax
  da=rev*c['ppeDaRevenueRatio'];capex_floor=max(rev*c['cashCapexRevenueRatio'],da);comm=max(rev-prevrev,0)*c['netCommissionPerIncrementalRevenue'];wc=max(rev-prevrev,0)*c['otherWcPerIncrementalRevenue']
  physical_net=max(capex_floor-da,0);growth_floor=max(nopat-prevnop,0)/s['roic'];investment=max(physical_net+comm+wc,growth_floor)
  extra=investment-physical_net-comm-wc;fcff=nopat+da-capex_floor-comm-wc-extra
  t=c['firstDiscountDays']/365+z;discount=fcff/(1+s['wacc'])**t;pv+=discount
  rows.append(dict(year=year,phase='growth' if z<5 else 'fade',revenue=rev,revenueGrowth=s['growth'][z],marginBeforeNewLeadership=margin,sbcEconomicCostMemo=rev*sbc_memo_ratio,marginBeforeSbcMemo=margin+sbc_memo_ratio,newLeadershipCost=leadership,ebitBeforeAcquiredAmortAfterSbc=ebit_pre_acq,acquiredAmortMemo=memo_amort,gaapEbitMemo=ebit_gaap_memo,cashTax=tax,nopat=nopat,ppeDepreciation=da,cashPpeCapexFloor=capex_floor,netCommissionInvestment=comm,otherWcInvestment=wc,additionalGrowthInvestment=extra,netReinvestment=investment,growthInvestmentFloor=growth_floor,fcff=fcff,discountYears=t,pv=discount))
  prevrev=rev;prevnop=nopat
 last=rows[-1];nextrev=last['revenue']*(1+s['g']);nextnop=last['nopat']*(1+s['g']);td=nextrev*c['ppeDaRevenueRatio'];tc=max(nextrev*c['cashCapexRevenueRatio'],td);tcomm=(nextrev-last['revenue'])*c['netCommissionPerIncrementalRevenue'];twc=(nextrev-last['revenue'])*c['otherWcPerIncrementalRevenue'];ti=max(nextnop*s['g']/s['roic'],max(tc-td,0)+tcomm+twc);tfcff=nextnop-ti;tv=tfcff/(s['wacc']-s['g']);tvpv=tv/(1+s['wacc'])**last['discountYears']
 # Stub based on normalized anchor and explicit maintenance/commission proxy, not seasonally inflated Q4 CFO.
 anchor=x['revenueAnchor2026'];anchor_growth=anchor/15431-1;stub_annual=anchor*x['normalizedMarginAnchor']*(1-c['cashTaxRate'])-max(anchor*(c['cashCapexRevenueRatio']-c['ppeDaRevenueRatio']),0)-max(anchor-15431,0)*(c['netCommissionPerIncrementalRevenue']+c['otherWcPerIncrementalRevenue'])
 stub=stub_annual*c['stubDays']/365/(1+s['wacc'])**(c['stubDays']/365) if c['stubEnabled'] else 0
 enterprise=pv+tvpv+stub;cash=b['cash']+b['marketableCurrent']+b['marketableNoncurrent'];private=b['strategicPrivateBook']*b['strategicRecoveryAfterTaxLiquidityFraction'];bridge=cash+private-b['debtPrincipal']-b['operatingCashReserve']-b['utbRecorded']-b['severanceRecorded']+b['unknownPostSeptemberNetCapital']-b['additionalContingencyReserve'];equity=enterprise+bridge
 return {'scenario':name,'assumptions':s,'rows':rows,'explicitPv':pv,'terminalPv':tvpv,'stubPv':stub,'enterpriseValue':enterprise,'capitalBridge':bridge,'equityValue':equity,'sharesMillions':x['sharesMillions'],'valuePerShare':equity/x['sharesMillions'],'terminalNopat':nextnop,'terminalReinvestment':ti,'terminalFcff':tfcff,'terminalFractionEnterprise':tvpv/enterprise,'upsideToReferenceClose':equity/x['sharesMillions']/x['price']-1}
if __name__=='__main__':
 out={n:run(n) for n in INPUT['scenarios']};(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for n,r in out.items():
  with (P/f'{n}_10_years.csv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=r['rows'][0].keys());w.writeheader();w.writerows(r['rows'])
 print({n:round(r['valuePerShare'],4) for n,r in out.items()})
