from pathlib import Path
import json,math,hashlib
import model
P=Path(__file__).parent;j=json.loads((P/'results.json').read_text());t=json.loads((P/'technical.json').read_text());checks=[]
def ck(name,ok,detail=None):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));assert ok,name
ck('nominal_not_carrying_debt',model.R['nominal_debt_sep27_rounded']==21700 and model.R['carrying_debt_sep27']==20498)
ck('post_acquisition_excess_cash',model.R['cash_sep27']-model.R['ultra_purchase']-model.C['minimum_operating_cash']==1010)
ck('current_plus_dilutive_award_shares',abs(model.SH-232.00464)<1e-8)
ck('core_guidance_reconciliation',model.R['operating_profit_2026_guidance_mid']-model.R['cas_2026_guidance']==7835)
ck('date_alignment',model.M['first_cashflow_time']>1)
for n in model.D['cases']:
 c=model.valuation(n);saved=j['cases'][n];ck(n+'replay',abs(c['value_per_share']-saved['value_per_share'])<1e-8)
 for key in ['core_forecast','ultra_forecast']:
  rs=c[key];ck(n+key+'10years',len(rs)==10 and rs[0]['year']==2027 and rs[-1]['year']==2036)
  for i,r in enumerate(rs):
   ck(n+key+str(i)+'cash',abs(r['fcff']-(r['nopat']-r['reinvestment']-r['additional_wc']-(r['prior_program_cash']+r['integration_cash']+r['environment_cash'])*(1-r['cash_tax_rate'])-r['ula_cash_support']))<1e-8)
   ck(n+key+str(i)+'tax',0<=r['cash_tax_rate']<=.30)
  x=model.D['cases'][n]['ultra'] if key=='ultra_forecast' else model.D['cases'][n]
  ck(n+key+'terminal_reinvestment',abs(rs[-1]['reinvestment']-rs[-1]['nopat']*rs[-1]['growth']/x['terminal_roic'])<1e-8)
  ck(n+key+'wacc_g',c['wacc']>x['terminal_growth'])
 ck(n+'program_reserves_no_shortfall',abs(sum(r['prior_program_cash']for r in c['core_forecast'])-1754)<1e-8)
 ck(n+'recovery_finite',c['pension_recovery_schedule'][-1]['pretax_recovery']==0)
 ck(n+'pension_bridge_once',abs(c['equity_value']-(c['core']['ev']+c['ultra']['ev']+c['cas_recovery_pv']-c['pension_claim_aftertax']-c['nominal_debt']+c['net_excess_cash_proforma']))<1e-8)
ck('higher_wacc_lower_value',model.valuation(wacc=.08)['value_per_share']<model.valuation(wacc=.07)['value_per_share']<model.valuation(wacc=.06)['value_per_share'])
ck('higher_g_higher_value',model.valuation(terminal_g=.02)['value_per_share']<model.valuation(terminal_g=.03)['value_per_share'])
ck('higher_cash_linear',abs((model.valuation(cash_shift=1000)['value_per_share']-model.valuation()['value_per_share'])-1000/model.SH)<1e-8)
for k,v in j['reverse'].items():ck('reverse_'+k,v is not None)
ck('reverse_wacc_tieout',abs(model.valuation(wacc=j['reverse']['wacc_at_current_price'])['value_per_share']-model.M['price'])<1e-6)
ck('reverse_margin_tieout',abs(model.valuation(margin_shift=j['reverse']['margin_shift_at_current_price'])['value_per_share']-model.M['price'])<1e-6)
ck('reverse_growth_tieout',abs(model.valuation(growth_shift=j['reverse']['first5_growth_shift_at_current_price'])['value_per_share']-model.M['price'])<1e-6)
ck('technical_regular_close',t['date']=='2026-11-04'and t['close']==595.04)
ck('technical_same_basis_overlap',t['overlap_rows']==49 and t['max_overlap_ohlc_difference']<=.011)
ck('technical_long_trend',t['close']>t['ema50']>t['ema200'] and t['ema200_slope_20_pct']>0)
ck('research_not_entry',not j['entry_approved'] and not t['technical_entry_approved'])
(P/'QA.json').write_text(json.dumps(dict(checks=checks,count=len(checks),passed=all(x['passed']for x in checks),scope='Author deterministic controls; independent audit separately required.'),indent=2));print(len(checks),'checks passed')
