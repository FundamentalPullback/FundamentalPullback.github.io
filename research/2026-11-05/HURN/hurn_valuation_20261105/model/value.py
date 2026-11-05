from pathlib import Path
import json,csv,copy,math
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
A=json.loads((P/'assumptions.json').read_text())
VAL=2026+307/365

def calc(case,overrides=None):
 p=copy.deepcopy(A['cases'][case]);p.update(overrides or {});c=A['current'];m=A['market'];h=A['history'];cap=A['capital_treatment']
 beta=m['selected_beta_unlevered']*(1+(1-m['tax'])*m['target_debt']/(1-m['target_debt']))
 ke=m['risk_free']+beta*m['erp']+m['company_premium'];w=(1-m['target_debt'])*ke+m['target_debt']*m['cost_debt']*(1-m['tax'])+p['wacc_adjustment']
 if 'wacc' in p:w=p['wacc']
 opening_nwc=c['receivables']+c['unbilled']+c['prepaid_operating']-c['ap']-c['accrued_other']-c['payroll']-c['deferred_revenue']
 cash_ratio=cap['cash_reserve']/h['ttm_rbr'];opening_nwc+=cap['cash_reserve']
 q4r=p['fy26_rbr']-c['rbr_9m'];q4ebit=q4r*p['q4_ebit_margin'];endwc=(p['fy26_nwc_ratio']+cash_ratio)*p['fy26_rbr'];q4capex=p['fy26_capex']-28.919
 q4fcff=q4ebit*(1-p['tax'])+p['q4_da']-q4capex-(endwc-opening_nwc)
 q4_reported_fcf=None
 if p.get('q4_fcf_anchor_enabled'):
  q4_reported_fcf=p['fy26_reported_fcf_guidance_case']-A['guidance_bridge']['nine_months_reported_fcf']
  q4fcff=q4_reported_fcf+p['q4_cash_interest']*(1-p['q4_interest_tax_shield'])-p['q4_sbc']
  endwc=opening_nwc+q4ebit*(1-p['tax'])+p['q4_da']-q4capex-q4fcff
 q4pv=q4fcff/(1+w)**(2026.875-VAL)
 seg={k:c['rbr_9m_segments'][k]+q4r*c['q3_mix'][k] for k in c['q3_mix']}
 rows=[];prior_rbr=p['fy26_rbr'];prior_nwc=endwc;g=p['terminal_growth'];strategic={'base':.01,'bear':.012,'bull':.008}[case]
 strategic=p.get('strategic_reinvestment_ratio',strategic)
 for i,y in enumerate(range(2027,2037)):
  growth={k:(p['growth_detailed'][k][i] if i<5 else p['growth_detailed'][k][-1]+(g-p['growth_detailed'][k][-1])*(i-4)/5) for k in seg}
  seg={k:seg[k]*(1+growth[k]) for k in seg};r=sum(seg.values());margin=p['ebit_margin'][i];ebit=r*margin;nopat=ebit*(1-p['tax']);da=r*p['da_ratio'];nwc=r*(p['nwc_ratio'][i]+cash_ratio);dnwc=nwc-prior_nwc
  ordinary_capex=r*p['capex_ratio'][i];strategic_cash=r*strategic
  # In years6-10 fade the sustainable total net reinvestment to g/ROIC*NOPAT.
  # This is explicit paid strategic/intangible capital, not an unexplained free terminal growth adjustment.
  target_net=nopat*g/p['terminal_roic'];ordinary_net=ordinary_capex+strategic_cash-da+dnwc
  transition_weight=0 if i<5 else (i-4)/5
  strategic_adjust=(target_net-ordinary_net)*transition_weight
  total_capex=ordinary_capex+strategic_cash+strategic_adjust
  loss=p['oneoff_unbilled_loss'] if i==0 else 0
  fcff=nopat+da-total_capex-dnwc-loss
  pv=fcff/(1+w)**(y+.5-VAL)
  rows.append(dict(year=y,phase='detailed' if i<5 else 'transition',segments=seg.copy(),segment_growth=growth,rbr=r,rbr_growth=r/prior_rbr-1,ebit_margin=margin,ebit=ebit,tax=nopat and ebit-nopat,nopat=nopat,da=da,ordinary_ppe_software=ordinary_capex,strategic_reinvestment=strategic_cash,transition_reinvestment_adjustment=strategic_adjust,total_capex=total_capex,nwc=nwc,dnwc=dnwc,unbilled_impairment_cash=loss,fcff=fcff,pv=pv))
  prior_rbr=r;prior_nwc=nwc
 terminal_nopat=rows[-1]['nopat']*(1+g);terminal_reinvestment=terminal_nopat*g/p['terminal_roic'];terminal_fcff=terminal_nopat-terminal_reinvestment
 tv=terminal_fcff/(w-g);tvpv=tv/(1+w)**(2036.5-VAL);ev=q4pv+sum(x['pv'] for x in rows)+tvpv
 # Bucket contains noncurrent earnout, deferredcomp and otheritems: net against earmarked assets ONCE.
 # Do not also deduct the entire earnout and its noncurrent component a second time.
 reserve=c['current_earnout']+cap['noncurrent_bucket_net_reserve']+cap['additional_deferred_acquisition_reserve']
 nonop=c['shorelight_book']*p['shorelight_recovery_fraction']
 cash_excess=max(0,c['cash']-cap['cash_reserve']);bridge=cash_excess+nonop-c['debt']-reserve
 equity=ev+bridge;v=equity/p['shares']
 return dict(case=case,assumptions=p,wacc=w,beta=beta,ke=ke,opening_nwc=opening_nwc,stub=dict(reported_fcf=q4_reported_fcf,implied_nwc_ratio_ex_cash=endwc/p['fy26_rbr']-cash_ratio,rbr=q4r,ebit=q4ebit,da=p['q4_da'],capex=q4capex,end_nwc=endwc,dnwc=endwc-opening_nwc,fcff=q4fcff,pv=q4pv),rows=rows,terminal=dict(nopat=terminal_nopat,roic=p['terminal_roic'],growth=g,reinvestment=terminal_reinvestment,fcff=terminal_fcff,unlevered_value=tv,pv=tvpv,implied_invested_capital=terminal_nopat/p['terminal_roic']),operating_ev=ev,bridge=dict(cash_excess=cash_excess,shorelight=nonop,debt=c['debt'],current_earnout=c['current_earnout'],net_noncurrent_comp_and_other=cap['noncurrent_bucket_net_reserve'],additional_deferred_acquisition_reserve=cap['additional_deferred_acquisition_reserve'],total=bridge),equity=equity,per_share=v,upside=v/A['price']-1,terminal_weight=tvpv/ev)

def main():
 R={k:calc(k) for k in A['cases']};(P/'results.json').write_text(json.dumps(R,indent=2))
 for k,r in R.items():
  keys=[k for k in r['rows'][0] if k not in ['segments','segment_growth']]
  with (P/f'{k}_annual.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:x[k] for k in keys} for x in r['rows'])
 print(json.dumps({k:{q:r[q] for q in ['wacc','per_share','upside','operating_ev','terminal_weight']} for k,r in R.items()},indent=2))
if __name__=='__main__':main()
