import json,csv,copy
from pathlib import Path
P=Path(__file__).parent
F={k:json.loads((P/'sources'/f'{k}_facts.json').read_text()) for k in ['fy25','q3','q2','q1','q325']}
def fact(k,n,c):
 a=[x for x in F[k] if x['name']==n and x['context']==c]
 if not a:return None
 x=a[0];v=x['value'].replace(',','').replace('—','0');return float(v)*10**int(x['scale'] or 0)/1e6*(-1 if x['sign']=='-' else 1)
T={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','cfo':'NetCashProvidedByUsedInOperatingActivities','ppe':'PaymentsToAcquirePropertyPlantAndEquipment','software':'PaymentsToAcquireIntangibleAssets','acquisitions':'PaymentsToAcquireBusinessesNetOfCashAcquired','sbc':'ShareBasedCompensation','dep':'Depreciation','amort':'AmortizationOfIntangibleAssets','interest_net':'InterestIncomeExpenseNonoperatingNet','dividends':'PaymentsOfDividendsCommonStock','lease_payment':'FinanceLeasePrincipalPayments','shares_diluted':'WeightedAverageNumberOfDilutedSharesOutstanding'}
def row(k,c):return {n:fact(k,'us-gaap:'+t,c) for n,t in T.items()}
def sub(a,b):return {k:a[k]-b[k] if a[k]!=None and b[k]!=None else None for k in a}
def add(a,b):return {k:a[k]+b[k] if a[k]!=None and b[k]!=None else None for k in a}
h={f'FY20{y}':row('fy25',c) for y,c in [('23','c-7'),('24','c-8'),('25','c-1')]}
h['9M2025']=row('q3','c-7');h['9M2026']=row('q3','c-1');h['Q42025']=sub(h['FY2025'],h['9M2025']);h['Q12026']=row('q1','c-1');h['Q22026']=sub(row('q2','c-1'),h['Q12026']);h['Q32026']=sub(h['9M2026'],row('q2','c-1'));h['TTM2026Q3']=add(h['Q42025'],h['9M2026']);h['TTM2025Q3']=add(sub(h['FY2024'],row('q325','c-7')),h['9M2025'])
# Weighted average shares are NOT additive. Q4 share-years subtract; current quarters read directly.
h['Q42025']['shares_diluted']=h['FY2025']['shares_diluted']*4-h['9M2025']['shares_diluted']*3
h['Q22026']['shares_diluted']=fact('q2','us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding','c-5')
h['Q32026']['shares_diluted']=fact('q3','us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding','c-5')
for name in ['TTM2026Q3','TTM2025Q3']:h[name]['shares_diluted']=None
for name,r in h.items():
 r['strict_fcf']=r['cfo']-r['ppe']-r['software'];r['owner_cash_diagnostic']=r['strict_fcf']-r['sbc'];r['nopat25']=r['ebit']*.75;r['normalized_net25']=(r['ebit']+r['interest_net'])*.75;r['normalized_eps25']=r['normalized_net25']/r['shares_diluted'] if r['shares_diluted'] else None
# debt principal: term 430.625, notes 400+350. Lease debt retained; operating lease cost remains in EBIT.
bridge={'debt_principal':1180.625,'finance_leases':15.455,'cash':499.053,'operating_cash_reserve':300.,'diluted_shares':169.627481,'scanner_price':43.07,'regular_close':None}
bridge['net_claims']=bridge['debt_principal']+bridge['finance_leases']-bridge['cash']+bridge['operating_cash_reserve']
cases={
 'bear':dict(growth=[.02]*5,margin=[.13]*5,wacc=.115,g=.02,roic=.10,wc=.30,investment=.035,release=[-100.,0,0,0,0]),
 'base':dict(growth=[.07,.06,.05,.04,.04],margin=[.152,.154,.156,.158,.16],wacc=.10,g=.025,roic=.15,wc=.20,investment=.03,release=[100.,100.,0,0,0]),
 'bull':dict(growth=[.09,.08,.07,.06,.05],margin=[.16,.165,.17,.175,.18],wacc=.09,g=.03,roic=.20,wc=.20,investment=.03,release=[300.,100.,0,0,0])}
def calc(c):
 rev=h['TTM2026Q3']['revenue'];rows=[]
 for i in range(1,11):
  gr=c['growth'][i-1] if i<=5 else c['growth'][-1]+(c['g']-c['growth'][-1])*(i-5)/5
  margin=c['margin'][i-1] if i<=5 else c['margin'][-1]
  old=rev;rev*=1+gr;nopat=rev*margin*.75;da=rev*.016;cap=rev*c['investment'];wc=(rev-old)*c['wc'];reinvestment=cap-da+wc
  if i==5:rate5=reinvestment/nopat
  if i>5:reinvestment=nopat*(rate5+(c['g']/c['roic']-rate5)*(i-5)/5)
  release=c['release'][i-1] if i<=5 else 0
  fcff=nopat-reinvestment+release
  rows.append(dict(year=i,revenue=rev,growth=gr,margin=margin,nopat=nopat,reinvestment=reinvestment,receivables_release_or_incremental_drain=release,fcff=fcff,pv=fcff/(1+c['wacc'])**i))
 terminal=rows[-1]['nopat']*(1+c['g'])*(1-c['g']/c['roic'])/(c['wacc']-c['g']);tpv=terminal/(1+c['wacc'])**10;ev=sum(r['pv'] for r in rows)+tpv
 return dict(rows=rows,terminal_pv=tpv,terminal_share=tpv/ev,ev=ev,equity=ev-bridge['net_claims'],value=(ev-bridge['net_claims'])/bridge['diluted_shares'])
results={k:calc(v) for k,v in cases.items()}
lo,hi=.05,.30
for _ in range(80):
 m=(lo+hi)/2;c=copy.deepcopy(cases['base']);c['margin']=[m]*5
 if calc(c)['value']<bridge['scanner_price']:lo=m
 else:hi=m
reverse=(lo+hi)/2
sensitivity=[]
for w in [.09,.095,.10,.105,.11]:
 for g in [.02,.025,.03]:
  c=copy.deepcopy(cases['base']);c.update(wacc=w,g=g);sensitivity.append(dict(wacc=w,g=g,value=calc(c)['value']))
no=copy.deepcopy(cases['base']);no['release']=[0]*5
out=dict(history=h,bridge=bridge,assumptions=cases,results=results,base_without_catchup=calc(no)['value'],reverse_constant_margin=reverse,sensitivity=sensitivity,canonical_value=None,status='conditional_research_not_entry_approved')
(P/'model_results.json').write_text(json.dumps(out,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values()))));w.writeheader();[w.writerow(dict(period=k,**v)) for k,v in h.items()]
print(json.dumps({k:round(v['value'],3) for k,v in results.items()}));print('reverse',reverse,'no recovery',out['base_without_catchup']);print('TTM',h['TTM2026Q3'])
