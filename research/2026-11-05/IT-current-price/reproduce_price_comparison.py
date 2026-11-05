"""Archived IT FCFF definitions, unchanged; price-comparison replay only. Original valuation 4 Nov 2026. Run offline."""
import json,csv,pathlib,itertools,math
P=pathlib.Path(__file__).parent
PRICE=204.22; SHARES=64.0; CASH=1633.137; RESERVE=500; DEBT=3000
CLAIMS={'tax_cash_reserve':149.765,'pension_funded_deficit':36.960,'net_deferred_compensation':7.336}
E=PRICE*SHARES; RF=.0495; ERP=.0441; BETA_OBS=.91; BETA_BASE=1.0; KD=.0625
WACC=(RF+BETA_BASE*ERP)*E/(E+DEBT)+KD*(1-.24)*DEBT/(E+DEBT)
OLD_WACC=.105*E/(E+DEBT)+.055*.76*DEBT/(E+DEBT)
def dcf(growth=.03,margin=.252,wacc=WACC,g=.025,roic=.20,sbc=177/6405,da=181/6405,tax=.24,capex=.017,wc=.02,transition=True,claims=sum(CLAIMS.values()),excess_cash=CASH-RESERVE):
 r=6405.; m0=1615/6405; rows=[]
 for y in range(1,11):
  gr=growth if y<=5 else growth+(g-growth)*(y-5)/5
  prev=r;r*=1+gr;m=m0+(margin-m0)*min(y/5,1)
  ebitda=r*m; sb=r*sbc; d=r*da; ebit=ebitda-sb-d; nopat=ebit*(1-tax)
  inv=r*capex; dwc=(r-prev)*wc; raw=inv-d+dwc; weight=max(0,(y-5)/5) if transition else 0
  terminal_like=nopat*gr/roic; netinv=(1-weight)*raw+weight*terminal_like; fcff=nopat-netinv
  rows.append(dict(year=y,revenue=r,growth=gr,ebitda_margin=m,ebitda=ebitda,sbc=sb,da=d,ebit=ebit,nopat=nopat,capex=inv,delta_wc=dwc,explicit_net_reinvestment=raw,transition_weight=weight,net_reinvestment=netinv,fcff=fcff,pv_fcff=fcff/(1+wacc)**y))
 n11=rows[-1]['nopat']*(1+g); f11=n11*(1-g/roic);tv=f11/(wacc-g);pvtv=tv/(1+wacc)**10;ev=sum(x['pv_fcff'] for x in rows)+pvtv;eq=ev+excess_cash-DEBT-claims
 return dict(value=eq/SHARES,ev=ev,equity=eq,terminal_pv_share=pvtv/ev,terminal_fcff=f11,claims=claims,inputs=dict(growth=growth,margin=margin,wacc=wacc,g=g,roic=roic,sbc=sbc,da=da,tax=tax,capex=capex,wc=wc,transition=transition,excess_cash=excess_cash),forecast=rows)
def solve(fn,target=PRICE,lo=-.1,hi=.5):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2

if __name__ == '__main__':
 data=json.loads((P/'current_price_calculations.json').read_text()); comparisons=data['comparisons'];checks=0
 vals={'base':dcf()['value'],'bear':dcf(growth=.01,margin=.24,wacc=.105,g=.02,roic=.15,sbc=.03,tax=.25,capex=.02,wc=.05)['value'],'bull':dcf(growth=.06,margin=.27,wacc=.085,g=.03,roic=.25,sbc=.025,tax=.23)['value'],'recovery':dcf(growth=.045,margin=.26)['value'],'preserve_NYU_market_return':dcf(wacc=.097*E/(E+DEBT)+KD*.76*DEBT/(E+DEBT))['value'],'base_no_excess_cash':dcf(excess_cash=0)['value']}
 for k,v in vals.items():
  assert abs(v-data['cases'][k])<1e-8;checks+=1
 for label,c in comparisons.items():
  price=c['price']
  for k,v in vals.items():
   assert abs((v/price-1)-c['scenario_returns'][k])<1e-10;checks+=1
  assert abs(dcf(wacc=c['reverse_wacc_base_flows'])['value']-price)<1e-8;checks+=1
  assert abs(dcf(growth=c['growth_at_base_wacc'])['value']-price)<1e-8;checks+=1
  assert abs((vals['base']-price)/(price-183)-c['base_reward_risk'])<1e-10;checks+=1
 print(json.dumps({'checks':checks,'failed':0,'scope':'unchanged FCFF and new price comparisons; not independent economic approval'}))
