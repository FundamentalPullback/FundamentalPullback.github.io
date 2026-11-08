import pathlib,json,csv,math
P=pathlib.Path(__file__).parent;H=json.loads((P/'history.json').read_text());shares=(298484548+40529390)/1e6;price=68.11;book=5751.244
rf=.0486;erp=.0441
# Conditional clean-surplus RI / FCFE equivalence. No corporate debt subtraction from equity value.
def scenario(terminal_roe,g0,beta,book0=book):
 ke=rf+beta*erp;gterm=.03;B=book0;rows=[];pvri=0;pvdiv=0
 start_roe=(65_250*.0849*.1475+(H['TTM2026']['pretax']-H['TTM2026']['ebit']))*.75/book
 for y in range(1,11):
  weight=(y-1)/9;roe=start_roe+(terminal_roe-start_roe)*weight;g=g0+(gterm-g0)*weight
  earnings=B*roe;retained=B*g;distribution=earnings-retained;ri=earnings-ke*B
  rows.append(dict(year=y,book_start=B,roe=roe,book_growth=g,earnings=earnings,retention=retained,fcfe=distribution,residual_income=ri,book_end=B+retained))
  pvri+=ri/(1+ke)**y;pvdiv+=distribution/(1+ke)**y;B+=retained
 tailri=(terminal_roe-ke)*B/(ke-gterm);taildiv=(terminal_roe-gterm)*B/(ke-gterm)
 value=book0+pvri+tailri/(1+ke)**10;ddm=pvdiv+taildiv/(1+ke)**10
 return dict(ke=ke,terminal_roe=terminal_roe,terminal_growth=gterm,conditional_equity_value=value,conditional_per_share=value/shares,fcfe_crosscheck=ddm,years=rows)
cases={n:scenario(r,g,b) for n,r,g,b in [('stress',.10,.08,2.0),('central',.16,.12,1.75),('upside',.22,.16,1.5)]}
# Price-implied sustained ROE, same convergence and retained-capital architecture, not a forecast.
lo,hi=-1,2
for _ in range(100):
 mid=(lo+hi)/2
 if scenario(mid,.12,1.75)['conditional_per_share']<price:lo=mid
 else:hi=mid
bars=list(csv.DictReader((P/'daily_closes.csv').open()));bars=[r for r in bars if r['date']<='2026-11-06'];ema={}
for period in [20,50]:
 e=float(bars[0]['close']);a=2/(period+1)
 for r in bars[1:]:e=a*float(r['close'])+(1-a)*e
 ema[str(period)]=e
volume=sum(float(x['volume']) for x in csv.DictReader((P/'volume_screen_input.csv').open()))/20
out={'as_of':'2026-11-08','units':'USD millions except per-share, ratios','price':price,'price_session':'2026-11-06 regular close','shares_million':shares,'equity_market_value':shares*price,'book_equity':book,'price_book':price*shares/book,'normalized_tax_rate_assumption':.25,'normalized_ttm_earnings':H['TTM2026']['pretax']*.75,'normalized_pe':price*shares/(H['TTM2026']['pretax']*.75),'reported_ttm_pe':price*shares/H['TTM2026']['net'],'ema':ema,'volume20':volume,'pullback_252':1-price/max(float(r['high']) for r in bars[-252:]),'technical_pass':price>ema['50'] and ema['20']>ema['50'],'risk_free_date':'2026-11-06','risk_free':rf,'erp_date':'2026-11-01','erp':erp,'cases':cases,'inverse_terminal_roe':(lo+hi)/2,'dta_full_haircut_sensitivity':{n:scenario(r,g,b,book-1433.080)['conditional_per_share'] for n,r,g,b in [('stress',.10,.08,2),('central',.16,.12,1.75),('upside',.22,.16,1.5)]},'gross_ecr_carrying_debt':10114.596-2904.541-6221.183,'stress_ecr_8pct_platform':21600*.08,'incremental_ecr_stress':21600*.08-(10114.596-2904.541-6221.183),'approved_value':None,'approved_entry':None,'unquantified_litigation':None,'unvalued_incremental_convertible_warrant_claim':None,'capital_distribution_permission_validated':False,'distributable_excess_cash':None,'status':'partial_conditional_RI_not_approved'}
(P/'model_results.json').write_text(json.dumps(out,indent=2))
with (P/'scenarios.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['scenario']+list(cases['central']['years'][0]));w.writeheader();w.writerows(dict(scenario=n,**r) for n,c in cases.items() for r in c['years'])
print({n:c['conditional_per_share'] for n,c in cases.items()});print('Inverse ROE',out['inverse_terminal_roe'])
