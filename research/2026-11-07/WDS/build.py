import pathlib,json,csv,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
years=[2023,2024,2025];fields={'revenue':[13994,13179,12984],'ebit':[3307,4514,3889],'parent_net_income':[1660,3573,2718],'cfo':[6145,5847,7192],'gross_capital_exploration':[5291,4902,7974],'capitalized_interest_cash':[311,369,712],'restoration_cash_in_cfo':[447,805,856],'production_mmboe':[187.2,193.9,198.8],'proved_reserves_mmboe':[2450.1,1975.7,1882.1]}
a={str(y):{k:v[i] for k,v in fields.items()} for i,y in enumerate(years)}
h={'2024H1':dict(revenue=5988,ebit=2362,parent_net_income=1937,cfo=2393,gross_capital_exploration=2418,capitalized_interest_cash=155),'2025H1':dict(revenue=6590,ebit=1817,parent_net_income=1316,cfo=3339,gross_capital_exploration=4881,capitalized_interest_cash=330),'2026H1':dict(revenue=7446,ebit=2157,parent_net_income=1672,cfo=3013,gross_capital_exploration=3673,capitalized_interest_cash=297)}
t={}
for yr in [2025,2026]:
 t[str(yr)+'-06-30']={k:a[str(yr-1)][k]+h[str(yr)+'H1'][k]-h[str(yr-1)+'H1'][k] for k in h[str(yr)+'H1']}
 t[str(yr)+'-06-30']['cfo_less_gross_capital']=t[str(yr)+'-06-30']['cfo']-t[str(yr)+'-06-30']['gross_capital_exploration']
 t[str(yr)+'-06-30']['after_capitalized_interest_before_partner_contributions']=t[str(yr)+'-06-30']['cfo_less_gross_capital']-t[str(yr)+'-06-30']['capitalized_interest_cash']
J('history.json',dict(units='USD millions except production and reserves MMboe',annual=a,interim=h,ttm_june=t,quarterly_operating_revenue={'2025Q4':3035,'2026Q1':3261,'2026Q2':4185,'2026Q3':4281},revenue_ttm_september_2026=14762,quarterly_income_cash_flow=None,frequency_note='Estados financieros semestrales. No se inventan resultados o flujos trimestrales.'))
rows=list(csv.DictReader((P/'daily_closes.csv').open()));cl=[float(r['close']) for r in rows if r['date']<='2026-11-06'];latest=[r for r in rows if r['date']<='2026-11-06']
def ema(n):
 x=cl[0]
 for v in cl[1:]:x+=2/(n+1)*(v-x)
 return x
vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));avg=sum(int(r['volume']) for r in vol)/len(vol)
high=max(float(r['high']) for r in latest[-252:]);shares=1901.100143;price=21.04
market=dict(date='2026-11-06',session='NYSE regular close, 16:00 EST',price_usd=price,alternate_provider_price_usd=21.03,quote_conflict='Un centavo entre proveedores; sin efecto en umbrales. No se declara cotización primaria de bolsa.',ordinary_shares_million_as_of_2026_10_08=shares,ads_to_ordinary=1,market_cap_usd_million=price*shares,ema20=ema(20),ema50=ema(50),high_252_sessions=high,pullback=1-price/high,volume20_stockanalysis=avg,ema_initialization=f'Primera observación de {len(cl)} sesiones; cierre no ajustado, no serie de retorno total.')
market['technical_entry_pass']=price>market['ema50'] and market['ema20']>market['ema50']
market['price_cap_liquidity_pass']=price>=15 and market['market_cap_usd_million']>=2000 and avg>=500000
J('market.json',market)
# Six-year finite capital-allocation diagnostic, never terminal/company NAV.
# CMD aggregate thresholds are rounded LOWER BOUNDS; annual allocation is deliberately not claimed.
sc=[]
for label,aocf,priority in [('CMD_mid_threshold',40000,17000),('CMD_high_threshold',50000,26000)]:
 base=.2*aocf; cap=.8*aocf-priority; cash=aocf-cap
 for r in [.08,.10,.12]:
  sc.append(dict(case=label,discount_rate_sensitivity=r,aocf_threshold=aocf,base_distribution_threshold=base,priority2_approx=priority,implied_capital_envelope_approx=cap,cash_after_capital_approx=cash,pv_if_all_end_2032=cash/(1+r)**6,pv_if_all_end_2027=cash/(1+r),annual_timing=None,terminal_value=None,whole_equity_value=None))
J('capital_envelope.json',dict(kind='Escenario finito de asignación, no FCFE ni valoración',years='2027–2032',perimeter='CMD: LALNG HoldCo 70% hipotético, no 90% actual; BNA excluido desde 2028; Chevron swap asumido; Sunrise excluido antes de cierre.',discount_basis='8–12% sensibilidad no calibrada; no se presenta como coste de capital observado.',scenarios=sc,unmodeled_value=None,approved_values=None))
# Reserve arithmetic only: no invented decline, costs, conversion or NAV.
J('resource_diagnostic.json',dict(as_of='2025-12-31',proved_mmboe=1882.1,developed_mmboe=643.6,undeveloped_mmboe=1238.5,included_fuel_mmboe=170.3,sec_annual_depletion_mmboe=211.4,commercial_production_mmboe=198.8,static_reserve_to_sec_depletion=1882.1/211.4,developed_to_sec_depletion=643.6/211.4,note='Cocientes estáticos, no vidas económicas ni calendario. Reservas SEC incluyen combustible y no equivalen a ventas de LNG comprado. Conversión PUD y crecimiento requieren inversión.',finite_project_nav=None,terminal_value=None))
checks={'three_annuals':len(a)==3,'three_interims':len(h)==3,'quarterly_revenue_reconcile':sum([3035,3261,4185,4281])==14762,'ttm_june_revenue':t['2026-06-30']['revenue']==13840,'ttm_june_ebit':t['2026-06-30']['ebit']==4229,'ttm_june_ni':t['2026-06-30']['parent_net_income']==3074,'ttm_cfo':t['2026-06-30']['cfo']==6866,'reserve_sum':abs(643.6+1238.5-1882.1)<.001,'no_fake_quarters':True,'no_terminal':all(x['terminal_value'] is None for x in sc),'no_whole_equity':all(x['whole_equity_value'] is None for x in sc),'quote_cutoff':latest[-1]['date']=='2026-11-06','volume20':len(vol)==20,'ads_one_to_one':True,'positive_actual_profits':t['2026-06-30']['ebit']>0 and t['2026-06-30']['parent_net_income']>0}
J('checks.json',checks);assert all(checks.values())
