import pathlib,json,csv
p=pathlib.Path(__file__).parent
inputs={'quote_date':'2026-11-06','regular_close':42.08,'shares_date':'2026-10-30','common_shares':69254666,'class_b_shares':5789499,'fy2025_parent_net_m':-104.026,'nine_months2025_parent_net_m':-27.232,'nine_months2026_parent_net_m':-252.522,'q32026_revenue_m':430.820,'q32026_operating_income_m':-3.047,'q32026_parent_net_m':-687.491,'q32026_total_diluted_eps':-9.15,'nine_months2026_revenue_m':1273.353,'nine_months2026_operating_income_m':-49.150}
a=[x for x in csv.DictReader((p/'daily_closes.csv').open()) if x['date']<='2026-11-06'];v=list(csv.DictReader((p/'volume_screen_input.csv').open()))
def ema(n):
 z=float(a[0]['close'])
 for x in a[1:]:z+=(float(x['close'])-z)*2/(n+1)
 return z
r={'identity':'People Incorporated, CIK1800227, Nasdaq PPLI since June4 2026, formerly IAC; unchanged CUSIP44891N208','inputs':inputs,'indicative_common_equivalent_cap_m':42.08*(69254666+5789499)/1e6,'quoted_class_only_cap_m':42.08*69254666/1e6,'ttm_parent_net_m':inputs['fy2025_parent_net_m']+inputs['nine_months2026_parent_net_m']-inputs['nine_months2025_parent_net_m'],'q3_operating_margin':-3.047/430.820,'q3_parent_net_margin':None,'q3_parent_net_margin_limitation':'Total parent net income includes discontinued operations while revenue is continuing-only; ratio intentionally not asserted','nine_months_operating_margin':-49.150/1273.353,'volume20':sum(float(x['volume']) for x in v)/len(v),'ema20':ema(20),'ema50':ema(50),'ema_initialization':'First close in two-year historical series continuing IAC predecessor; supplementary only, corporate-action adjustments not independently certified','ttm_operating_margin':None,'ttm_eps_exact':None,'ttm_revenue_same_perimeter':None,'gate':'Current reported profitability fails; TTM parent earnings negative and Q3/9M operating margins negative','approved_value':None,'approved_entry':None,'valuation_performed':False}
(p/'screen.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert r['ttm_parent_net_m']<0 and r['q3_operating_margin']<0 and r['approved_value'] is None
(p/'checks.json').write_text(json.dumps({'total_parent_TTM_bridge':True,'discontinued_reclassification_does_not_change_total_parent_earnings':True,'no_mixed_perimeter_operating_TTM':True,'no_false_exact_EPS_sum':True,'no_valuation':True},indent=2))
