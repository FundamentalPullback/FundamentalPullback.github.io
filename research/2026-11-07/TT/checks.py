import pathlib,json
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text());c={}
for k in h['TTM2026']:c['TTM_'+k]=abs(sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][k])<.0001
for n,x in r['cases'].items():
 c[n+'_stock']=all(abs(y['physical_end']-y['physical_start']-y['physical_capex']+y['physical_depreciation'])<1e-8 for y in x['years'])
 c[n+'_FCFF']=all(abs(y['fcff']-y['nopat']-y['physical_depreciation']-y['intangible_amortization']+y['physical_capex']+y['nwc_investment'])<1e-8 for y in x['years'])
 t=x['terminal'];g=t['g'];c[n+'_terminal_funded']=abs(t['physical_capex']-t['physical_depreciation']-g*x['years'][-1]['physical_end'])<1e-8
 c[n+'_ROIC']=abs(t['reinvestment']-t['nopat']*g/t['implied_incremental_roic'])<1e-8
 c[n+'_tail_1000']=abs(sum(t['fcff']*(1+g)**(i-1)/(1+x['wacc'])**i for i in range(1,1001))-t['fcff']/(x['wacc']-g))<.01
c['approved_null']=r['approved_value'] is None and r['approved_entry'] is None
(p/'checks.json').write_text(json.dumps(c,indent=2));assert all(c.values());print(len(c),'passed')
