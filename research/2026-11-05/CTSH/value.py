from pathlib import Path
import json,csv,copy
P=Path(__file__).parent
I=json.loads((P/'model/inputs.json').read_text());B=json.loads((P/'beta_estimate.json').read_text())
shares=I['shares_actual_oct23']+I['incremental_dilution']; E=shares*I['price'];dw=I['debt']/(I['debt']+E);beta=(2*B['beta']+1)/3;ke=I['risk_free']+beta*I['erp'];wacc=ke*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw
capital=dict(beta_raw=B['beta'],beta_normalized=beta,equity_market=E,debt_weight=dw,cost_equity=ke,cost_debt=I['cost_debt'],wacc=wacc,shares=shares)
def value(name='base',overrides=None,owned=False,bridge_overrides=None):
 c=copy.deepcopy(I['cases'][name]);c.update(overrides or {});br=copy.deepcopy(I);br.update(bridge_overrides or {});w=c.get('wacc',wacc+c['wacc_spread']);g=c['terminal_g'];assert w>g
 R=I['base_revenue'];prior_new=0;rows=[];stub_t=I['stub_days']/I['stub_year_days'];pv=0
 for t in range(1,11):
  prev=R
  if t<=5:
   org=prev*c['organic_growth'];inherit=I['base_revenue']*c['inherited_growth_2027'] if t==1 else 0
   carry=prior_carry*(1+c['organic_growth']) if t>1 else 0
   dyflex_run=I['dyflex_cash']/c['acquisition_multiple'] if t==1 else 0
   new_run=dyflex_run if owned else prev*c['new_acquired_runrate']
   other_run=max(0,new_run-dyflex_run)
   new_rec=other_run*c['recognition_fraction']+dyflex_run*I['dyflex_first_year_recognition']
   R=prev+org+inherit+carry+new_rec;growth=R/prev-1
   acq=other_run*c['acquisition_multiple']+(I['dyflex_cash'] if t==1 else 0)
   capex=R*c['capex_pct'];wc=org*c['nwc_incremental'];contract=R*c['contract_capitalization'];dso=c['dso_cash_stress_2027'] if t==1 else 0
   if owned:
    da=R*I['owned_ppe_depreciation_pct']+I['owned_intangible_amortization'][t-1]+I['dyflex_cash']*I['dyflex_new_intangibles_share']/I['dyflex_intangible_life']*(I['dyflex_first_year_recognition'] if t==1 else 1)
    ebitda=R*(c['margins'][t-1]+c['da_pct']);ebit=ebitda-da
   else:
    da=R*c['da_pct'];ebit=R*c['margins'][t-1]
   margin=ebit/R;nopat=ebit*(1-c['tax']);reinv=capex+acq+wc+contract+dso-da;fcff=nopat-reinv
   prior_carry=other_run*(1-c['recognition_fraction'])+dyflex_run*(1-I['dyflex_first_year_recognition']);fade=0
   if t==5:g5=growth;reinv_rate5=reinv/R;wc_rate5=(wc+contract)/R;cap_margin5=margin;da_rate5=da/R
  else:
   fade=(t-5)/5;growth=g5+(g-g5)*fade;R=prev*(1+growth);margin=cap_margin5+(c['terminal_margin']-cap_margin5)*fade;ebit=R*margin;nopat=ebit*(1-c['tax']);da=R*(da_rate5+(I['owned_ppe_depreciation_pct']-da_rate5)*fade)
   # Aggregate transition: net reinvestment fades to NOPAT*g/ROIC. No separate promised deal pipeline after year5.
   target=nopat*g/c['terminal_roic'];reinv=(1-fade)*R*reinv_rate5+fade*target;wc=R*wc_rate5*(1-fade);contract=0;dso=0;acq=None;capex=da+reinv-wc;org=inherit=carry=new_rec=new_run=None;fcff=nopat-reinv
  time=t+stub_t;disc=(1+w)**time
  dyflex_cash=I['dyflex_cash'] if t==1 else 0;other_acq_cash=(acq-dyflex_cash) if acq is not None else 0
  pv_acq=dyflex_cash/(1+w)**(time-I['dyflex_first_year_recognition'])+other_acq_cash/(1+w)**(time-c['recognition_fraction'])
  pvf=(fcff+(acq or 0))/disc-pv_acq;pv+=pvf
  rows.append(dict(year=2026+t,t=t,organic_revenue_increment=org,inherited_revenue_increment=inherit,prior_deal_carryover=carry,new_deal_full_runrate=new_run,new_deal_recognized=new_rec,revenue=R,growth=growth,ebit_margin=margin,ebit=ebit,nopat=nopat,da=da,ppe_or_aggregate_capex=capex,acquisition_cash=acq,nwc_increment=wc,contract_capitalization=contract,dso_stress=dso,net_reinvestment=reinv,fcff=fcff,discount_time=time,discount_factor=disc,pv_acquisition_cash=pv_acq,dyflex_cash=dyflex_cash,other_acquisition_cash=other_acq_cash,pv_fcff=pvf,fade_weight=fade))
 terminal_rev=R*(1+g);terminal_nopat=terminal_rev*c['terminal_margin']*(1-c['tax']);terminal_reinv=terminal_nopat*g/c['terminal_roic'];terminal_fcff=terminal_nopat-terminal_reinv;tv=terminal_fcff/(w-g);pv_tv=tv/(1+w)**(10+stub_t)
 stub=c['stub_issuer_fcf']-I['stub_sbc']+I['stub_net_interest_expense']*(1-c['tax']);pvstub=stub/(1+w)**stub_t
 ev=pv+pv_tv+pvstub;excess=br['cash']+br['short_investments']-br['operating_cash'];claims=br['debt']+br['pension_deficit']+br['contingent_consideration']+br['post_september_buyback_cash'];equity=ev+excess-claims;ss=br['shares_actual_oct23']+br['incremental_dilution'];ps=equity/ss
 return dict(case=name,owned_business=owned,wacc=w,inputs=c,rows=rows,pv_explicit=pv,pv_stub=pvstub,stub_fcff=stub,terminal_revenue=terminal_rev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,terminal_fcff=terminal_fcff,terminal_value=tv,pv_terminal=pv_tv,terminal_pct_ev=pv_tv/ev,enterprise_value=ev,excess_cash=excess,financial_claims=claims,equity_value=equity,shares=ss,per_share=ps,upside=ps/I['price']-1)
def main():
 o={n:value(n)for n in I['cases']};o['owned_business_crosscheck']=value(owned=True);o['capital']=capital;(P/'results.json').write_text(json.dumps(o,indent=2))
 with (P/'model/forecast_rows.csv').open('w')as f:
  wr=csv.DictWriter(f,fieldnames=['case']+list(o['base']['rows'][0]));wr.writeheader()
  for n,z in o.items():
   if 'rows'in z:
    for r in z['rows']:wr.writerow(dict(case=n,**r))
 print({n:{k:z[k]for k in ['per_share','wacc','terminal_pct_ev','stub_fcff']}for n,z in o.items()if'rows'in z});print(capital)
if __name__=='__main__':main()
