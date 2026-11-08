"""USD millions. Funding sensitivities, NOT corporate or common-equity valuation."""
import pathlib,json,csv
p=pathlib.Path(__file__).parent
h=json.loads((p/'history.json').read_text());a=list(csv.DictReader((p/'daily_closes.csv').open()));a=[x for x in a if x['date']<='2026-11-06'];v=list(csv.DictReader((p/'volume_screen_input.csv').open()))
def ema(n):
 z=float(a[0]['close'])
 for x in a[1:]:z+=(float(x['close'])-z)*2/(n+1)
 return z
price=124.8; peak=max(float(x['high']) for x in a[-252:]);tt=h['TTM2026']
screen={'date':'2026-11-06','regular_close':price,'after_hours_excluded':124.65,'shares_m_rounded_2026_11_02':339,'indicative_cap_m':price*339,'ema20':ema(20),'ema50':ema(50),'initialization':'First daily close in archived two-year series; unadjusted closes','pullback_252_high_pct':100*(1-price/peak),'volume20':sum(float(x['volume']) for x in v)/len(v),'ttm_operating_margin':tt['ebit']/tt['revenue'],'ttm_net_common_margin':tt['net_common']/tt['revenue'],'cash_less_capex_per_rounded_current_share':tt['cfo_less_capex']/339}
rows=[]
# Guided operating cash already includes interest, cash tax, reclamation and other operating uses.
# Remove temporary working-capital release; charge all investing, economic SBC; do not add back merger costs.
for label,ebitda in [('low',7625),('mid',8025),('high',8425)]:
 cfo=ebitda-1353-117+704-217-190
 guided_before_growth_pref=cfo-704-1750-10-155
 # Guidance investment line is net of 74 of one-off Martin Lake insurance proceeds.
 sustainable_before_growth_pref=guided_before_growth_pref-74
 for growth in [500,1000,1500,2000]:
  for extra_tax in [0,400,800]:
   rows.append({'guidance_case':label,'consolidated_ebitda':ebitda,'guided_cfo':cfo,'guided_cash_ceiling_including_insurance':guided_before_growth_pref,'nonrecurring_property_insurance_removed':74,'cash_before_growth_preferred_principal_and_extra_tax':sustainable_before_growth_pref,'assumed_growth_capex':growth,'assumed_extra_cash_tax':extra_tax,'conditional_cash_before_preferred_and_financing':sustainable_before_growth_pref-growth-extra_tax})
# Explicit equity discount sensitivity only. No calibrated beta, WACC, terminal, or equity target claimed.
rates=[{'assumed_beta':b,'rf_2026_11_06':.0486,'erp_2026_11_01':.0441,'conditional_ke':.0486+b*.0441} for b in [1,1.25,1.5]]
result={'scope':'2027 funding sensitivity, not valuation; future plant cash allocation and growth budgets unresolved','screen':screen,'funding_grid':rows,'conditional_equity_discount_rates':rates,'current_debt_cash_bridge':None,'preferred_cash_dividends_2027':None,'current_total_legal_claims':None,'whole_equity_value':None,'terminal_value':None,'approved_value':None,'approved_entry':None,'inverse':'At midpoint, growth capex plus additional cash tax plus preferred distributions and debt principal must not exceed 4159 before common distributions, assuming guided operating cash and removing 74 of one-off insurance proceeds. This is a funding ceiling, not a stock-price inverse.'}
(p/'model_results.json').write_text(json.dumps(result,indent=2));(p/'screen.json').write_text(json.dumps(screen,indent=2))
with (p/'funding_sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(screen,indent=2));print('Midpoint funding ceiling:',[x for x in rows if x['guidance_case']=='mid'][0]['cash_before_growth_preferred_principal_and_extra_tax'])
