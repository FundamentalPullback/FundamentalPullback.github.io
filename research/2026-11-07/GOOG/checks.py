import pathlib,json,math
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());r=json.loads((P/'model_results.json').read_text());checks={}
for k in h['TTM2026']:checks['TTM_'+k]=abs(sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][k])<.01
for n,c in r['cases'].items():
 checks[n+'_stock']=all(abs(y['physical_end']-y['physical_start']-y['cip_activated']-y['physical_capex']+y['physical_da'])<1e-7 for y in c['years'])
 checks[n+'_fcff']=all(abs(y['fcff']-y['nopat']-y['physical_da']-y['intangible_amort']+y['physical_capex']+y['intangible_capex']+y['nwc_investment'])<1e-7 for y in c['years'])
 checks[n+'_replacement']=all(y['physical_capex']>=y['physical_da']-1e-7 for y in c['years'])
 checks[n+'_CIP_no_free']=abs(c['years'][-1]['cip_end'])<1e-7
 t=c['terminal'];last=c['years'][-1];g=t['g']
 checks[n+'_terminal_stock_funded']=abs(t['physical_capex']-t['physical_da']-last['physical_end']*g)<1e-7
 checks[n+'_terminal_IP_funded']=t['intangible_capex']-t['intangible_amort']>=last['intangible_end']*g-1e-7
 checks[n+'_RI_ROIC_identity']=abs(t['reinvestment']-t['nopat']*g/t['implied_incremental_roic'])<1e-7
 S=last['physical_end'];I=last['intangible_end'];R=last['revenue'];tail=0;rate=c['physical_decay_rate'];tax=r['config'][n]['tax'];cm=r['config'][n]['cm']
 for year in range(1,1201):
  nr=R*(1+g);cap=(rate*S+g*S)/(1-rate/2);da=rate*S+rate*cap/2;ic=max(.005*nr,(I/5+g*I)/.9);ia=I/5+.1*ic
  eb=cm*nr-da-ia;cash=eb-max(eb,0)*tax+da+ia-cap-ic-.03*(nr-R);tail+=cash/(1+c['wacc'])**year;S+=cap-da;I+=ic-ia;R=nr
 checks[n+'_terminal_1200year_dynamic_stocks']=abs(tail-c['terminal_value_at_year10'])<.01
 checks[n+'_terminal_IP_floor']=t['intangible_capex']>=.005*t['revenue']-1e-7

checks['no_double_preferred']=all(c['conditional_share_denominator']>12294 and abs(c['conditional_bridge']-(174714-30000+90384*(1-r['config'][n]['equity_haircut'])+135230*(1-r['config'][n]['private_haircut'])-127485-3705-13807-12219-26375-35921-6900*r['config'][n]['nci_multiple']))<1e-7 for n,c in r['cases'].items())
checks['approved_null']=r['approved_value'] is None and r['approved_entry'] is None
(P/'checks.json').write_text(json.dumps(checks,indent=2));assert all(checks.values()),checks;print(len(checks),'checks passed')
