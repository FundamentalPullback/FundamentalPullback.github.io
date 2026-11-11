"""Conditional operating value: no trading instruction. USD millions except shares/prices.
Sources and assumptions separately documented in report and source ledger.
"""
import json
from pathlib import Path
B=Path(__file__).parent
P=dict(price=21.73,mk=2767.,jc=632.,cash=125.,reserve=125.,debt=461.,hedge=763.,nci=5.,shares=103.349705+2.957367+0.235043,tax=.25,g=.025,roic=.12,capex=.035,da=.03,nwc=.15)
PATHS={
'central':dict(mkg=[-.01,.01,.02,.02,.02],jcg=[.05,.05,.04,.04,.03],mkm=[.108,.115,.12,.125,.13],jcm=[.02,.03,.04,.045,.05],corp=[.042,.042,.041,.04,.04]),
'recovery':dict(mkg=[0,.03,.04,.04,.03],jcg=[.07,.07,.06,.05,.04],mkm=[.11,.125,.14,.15,.16],jcm=[.03,.05,.07,.09,.10],corp=[.042,.04,.038,.036,.035]),
'adverse':dict(mkg=[-.10,-.06,-.03,0,.01],jcg=[-.03,0,.01,.02,.02],mkm=[.075,.07,.075,.08,.085],jcm=[-.02,0,.01,.02,.03],corp=[.05,.05,.05,.048,.045])}
def calc(path='central',rate=.10,shift=0,hedge=None,reserve=None,fx=1.,claims=0,shares=None,capex=None,nwc=None,tax=None):
 q=PATHS[path];mk=P['mk']*fx;jc=P['jc']*fx;prev=mk+jc;rows=[];cashcum=0;peak=0;tax=P['tax'] if tax is None else tax;capex=P['capex'] if capex is None else capex;nwc=P['nwc'] if nwc is None else nwc
 for y in range(1,11):
  k=min(y-1,4);fade=max(0,y-5)/5
  gm=q['mkg'][k]*(1-fade)+P['g']*fade;gj=q['jcg'][k]*(1-fade)+P['g']*fade
  mk*=1+gm;jc*=1+gj;rev=mk+jc;ebit=mk*q['mkm'][k]+jc*q['jcm'][k]-rev*q['corp'][k]+rev*shift
  nopat=ebit*(1-tax) if ebit>0 else ebit
  investment=(capex-P['da'])*rev+nwc*max(0,rev-prev);fcff=nopat-investment;cashcum+=fcff;peak=max(peak,-cashcum)
  rows.append(dict(year=y,mk_sales=mk,jc_sales=jc,revenue=rev,ebit=ebit,nopat=nopat,net_investment=investment,fcff=fcff,pv=fcff/(1+rate)**y));prev=rev
 n=rows[-1]['nopat']*(1+P['g']);ti=max((capex-P['da'])*rev*(1+P['g'])+nwc*rev*P['g'],max(0,n)*P['g']/P['roic']);tf=n-ti;tv=tf/(rate-P['g']);pv=tv/(1+rate)**10;ev=sum(r['pv'] for r in rows)+pv
 hedge=P['hedge'] if hedge is None else hedge;reserve=P['reserve'] if reserve is None else reserve;shares=P['shares'] if shares is None else shares
 bridge=P['cash']-reserve-P['debt']-hedge-P['nci']-claims;equity=ev+bridge
 return dict(path=path,rate=rate,shift=shift,fx=fx,hedge=hedge,reserve=reserve,claims=claims,shares=shares,capex=capex,nwc=nwc,tax=tax,rows=rows,terminal_fcff=tf,terminal_reinvestment=ti,terminal_pv=pv,terminal_fraction=pv/ev,ev=ev,bridge=bridge,equity=equity,value_raw=equity/shares,value=max(0,equity/shares),peak_operating_deficit=peak)
def inverse(path,rate):
 lo=-.15;hi=.50
 for _ in range(100):
  m=(lo+hi)/2
  if calc(path,rate,shift=m)['value_raw']<P['price']:lo=m
  else:hi=m
 x=calc(path,rate,shift=(lo+hi)/2)
 return dict(path=path,rate=rate,required_incremental_margin=x['shift'],terminal_group_margin=x['rows'][-1]['ebit']/x['rows'][-1]['revenue'],first_fcff=x['rows'][0]['fcff'],value=x['value_raw'])
if __name__=='__main__':
 cases={name:calc(**kw) for name,kw in {'central10':{},'central12':{'rate':.12},'central14':{'rate':.14},'recovery10':{'path':'recovery'},'recovery12':{'path':'recovery','rate':.12},'recovery8':{'path':'recovery','rate':.08},'adverse14':{'path':'adverse','rate':.14,'claims':100}}.items()}
 sens={f'{key}_{v}':calc(**{key:v}) for key,vs in {'hedge':[139,563,963,1387],'reserve':[75,150],'shares':[103.349705,106.777158],'capex':[.03,.04],'nwc':[.10,.20],'tax':[.20,.30]}.items() for v in vs}
 # Joint FX stresses are illustrative, not calibrated hedge effectiveness: move BOTH operating USD values and claim.
 sens.update(higher_corporate_burden=calc(shift=-.014),receivable_credit19=calc(claims=-19),inventory_credit25_stress=calc(claims=25),fx_up_claim_up=calc(fx=1.1,hedge=963),fx_down_claim_down=calc(fx=.9,hedge=563))
 out=dict(inputs=P,paths=PATHS,cases=cases,sensitivities=sens,inverses=[inverse(p,r) for p,r in [('central',.10),('central',.12),('recovery',.10)]],limitations=['Borrowing capacity and settlement schedules are not certified','Positive consolidated FCFF is not contractual cash available to settle hedges','No perpetual interest income or free subsidiary book assets','Amounts before tax consequences of hedge settlement; separate scenario claims, not tax credits'])
 (B/'results.json').write_text(json.dumps(out,indent=2))
 print({k:round(v['value'],2) for k,v in cases.items()});print(out['inverses'])
