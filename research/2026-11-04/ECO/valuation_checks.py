import json,pathlib,copy
from model import *
P=pathlib.Path(__file__).parent
def solve(f,target=PRICE,lo=-30000,hi=200000):
 for _ in range(100):
  mid=(lo+hi)/2
  if f(mid)>target:hi=mid
  else:lo=mid
 return (lo+hi)/2

def finite(s=BASE):
 rows=[];previous=0;infl=1;life=s['life']
 for i in range(1,life+1):
  if i>1:infl*=1.02 if i<=5 else 1+s['g']
  year=2026+i;active=[(n,k,y)for n,k,y in FLEET if year<=y+life]
  if not active:continue
  rates={k:v[i-1]if i<=5 else v[-1]*(1+s['g'])**(i-5)for k,v in s['rates'].items()}
  tce=sum(365*s['util']*rates[k]/1e6 for _,k,_ in active)
  if i==1:tce+=(90000-rates['VLCC'])*s.get('charter_days',106)/1e6
  n=len(active)
  opex=n*365*10000*infl*s['opex_scale']/1e6;ga=20*infl*n/18;da=60*infl*n/18;ebit=tce-opex-ga-da;tax=max(0,ebit)*s['tax'];dry=8*infl*n/18;wc=0 if i==1 else .08*(tce-previous)
  scrap=sum(SCRAP[k]*infl for _,k,y in active if year==y+life);fcff=ebit-tax+da-dry-wc+scrap
  rows.append({'year':i,'vessels':n,'TCE':tce,'FCFF':fcff,'scrap':scrap,'PV':fcff/(1+s['wacc'])**i});previous=tce
 # Release modeled final operating working capital, but no residual operating reserve credit.
 release=.08*previous/(1+s['wacc'])**life;ev=sum(x['PV']for x in rows)+release
 return {'value':(ev-capital(s['cfo'])['net_claims'])/SHARES,'EV':ev,'working_capital_release_PV':release,'rows':rows,'scope':'Existing18 vessels to20years then scrap, no replacements or perpetuity. Revenue and cost scale with surviving ships; this does not certify ship-sale NAV.'}

def main():
 sens={}
 for k,vals in {'charter_days':[0,60,106,180],'life':[20,25],'cfo':[0,150,200,300,400,450],'opex_scale':[1,1.2,1.4],'replacement_scale':[.8,1,1.2],'tax':[0,.01,.05],'util':[.94,.97,.985],'roic':[.08,.10,.12,.15]}.items():
  for v in vals:sens[f'{k}_{v}']=calculate(dict(BASE,**{k:v}))['value']
 shift=solve(lambda a:calculate(BASE,normal_shift=a)['value'])
 r={'sensitivity':sens,'grid':[{'wacc':w,'g':g,'value':calculate(dict(BASE,wacc=w,g=g))['value']}for w in [.09,.10,.105,.11,.12]for g in [.01,.02,.025]],'reverse':{'normalized_VLCC_shift':shift,'normalized_Suezmax_shift':shift*.75,'year5_VLCC':62500+shift,'year5_Suezmax':45000+shift*.75,'value':calculate(BASE,normal_shift=shift)['value'],'not_unique_market_implied_path':True},'finite_fleet_crosscheck':finite(),'wacc':{'rf':.0495,'ERP_monthly':.0441,'normalized_beta_assumed':1.35,'cost_equity':.0495+.0441*1.35,'debt_cost_assumed':.06,'tax':.01,'equity_weight_assumed':.85,'computed':(.0495+.0441*1.35)*.85+.06*.99*.15,'chosen':.105,'provider_beta_observed':-.06,'provider_beta_weighted_cost':(.0495-.06*.0441)*.85+.06*.99*.15,'provider_beta_same_cashflows_value':calculate(dict(BASE,wacc=(.0495-.06*.0441)*.85+.06*.99*.15))['value'],'provider_beta_not_used_reason':'Short NYSE history and commodity/geopolitical countercyclicality do not establish low intrinsic cyclical cash-flow risk. Normalized beta is judgment, not observation.'}}
 (P/'valuation_checks.json').write_text(json.dumps(r,indent=2));print('reverse',r['reverse']);print('finite',r['finite_fleet_crosscheck']['value']);print('sens',sens)
if __name__=='__main__':main()
