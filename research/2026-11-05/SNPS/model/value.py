from pathlib import Path
import json,copy,csv
P=Path(__file__).resolve().parent;A=json.loads((P/'assumptions.json').read_text())
def calc(case='base',overrides=None):
 p=copy.deepcopy(A['cases'][case]);p.update(overrides or {});M=A['market'];C=A['capital'];w=(M['rf']+M['beta']*M['erp'])*(1-M['debt_weight'])+M['cost_debt']*(1-M['tax'])*M['debt_weight']+p['wacc_delta'];w=p.get('wacc',w);seg=A['segments'].copy();prior=sum(seg.values());rows=[]
 for i in range(10):
  growth={k:p['growth'][k][i] if i<5 else p['growth'][k][-1]+(p['g']-p['growth'][k][-1])*(i-4)/5 for k in seg}
  if 'constant_growth' in p:growth={k:p['constant_growth'] if i<5 else p['constant_growth']+(p['g']-p['constant_growth'])*(i-4)/5 for k in seg}
  seg={k:v*(1+growth[k]) for k,v in seg.items()};r=sum(seg.values());m=p['margin'][min(i,4)]+p.get('margin_shift',0);ebit=r*m;nop=ebit*(1-p['tax']);da=r*p['da'];capex=r*p['capex'][min(i,4)];wc=(r-prior)*p['wc_increment'];strategic=r*p['strategic'];raw=capex+wc+strategic-da;fade=0 if i<5 else (i-4)/5;net=raw*(1-fade)+nop*p['g']/p['roic']*fade;adjust=net-raw;fcff=nop-net;pv=fcff/(1+w)**(i+1);rows.append(dict(year=2027+i,segments=seg.copy(),revenue=r,growth=r/prior-1,margin=m,ebit=ebit,tax=ebit-nop,nopat=nop,da=da,capex=capex,dnwc=wc,strategic=strategic,transition_adjust=adjust,net_reinvestment=net,fcff=fcff,pv=pv));prior=r
 tnop=rows[-1]['nopat']*(1+p['g']);tri=tnop*p['g']/p['roic'];tfcf=tnop-tri;tv=tfcf/(w-p['g']);tvpv=tv/(1+w)**10;ev=sum(x['pv'] for x in rows)+tvpv;cash=C['cash_july']+C['q4_fcf_rollforward']-C['asr_cash_paid']-C['operating_cash_reserve'];shares=C['fully_diluted_pre_asr']-C['initial_asr_shares'];bridge=cash-C['debt_principal_and_lock'];value=(ev+bridge)/shares
 return dict(case=case,wacc=w,rows=rows,terminal_nopat=tnop,terminal_reinvestment=tri,terminal_fcff=tfcf,terminal_value=tv,terminal_pv=tvpv,terminal_weight=tvpv/ev,ev=ev,excess_cash=cash,bridge=bridge,shares=shares,value=value,upside=value/A['price']-1)
def bisect(fn,target,lo,hi):
 for _ in range(100):
  md=(lo+hi)/2
  if fn(md)<target:lo=md
  else:hi=md
 return (lo+hi)/2
if __name__=='__main__':
 R={k:calc(k) for k in A['cases']};g=bisect(lambda x:calc(overrides={'constant_growth':x})['value'],A['price'],.0,.50);margin=bisect(lambda x:calc(overrides={'margin_shift':x})['value'],A['price'],-.15,.30)
 B=R['base'];stress=calc(overrides={'growth':{k:[x-.02 for x in v] for k,v in A['cases']['base']['growth'].items()},'margin_shift':-.02,'wacc_delta':.005,'g':.025})
 rates=[B['wacc']-.01,B['wacc']-.005,B['wacc'],B['wacc']+.005,B['wacc']+.01];sens=[{'wacc':w,'g':gg,'value':calc(overrides={'wacc':w,'g':gg})['value']} for w in rates for gg in [.02,.025,.03,.035,.04]]
 O={'cases':R,'reverse_constant_growth':g,'reverse_margin_shift':margin,'moderate_combined_stress':stress,'sensitivity':sens,'management_delivery':calc(overrides={'constant_growth':.15,'margin':[.353,.38,.405,.425,.43]})}
 (P/'results.json').write_text(json.dumps(O,indent=2))
 for k,v in R.items():
  with (P/(k+'_annual.csv')).open('w') as f:
   fields=[x for x in v['rows'][0] if x!='segments'];wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows({x:r[x] for x in fields} for r in v['rows'])
 print(json.dumps({k:{x:v[x] for x in ['value','wacc','upside','terminal_weight']} for k,v in R.items()},indent=2));print('Reverse',g,margin,'stress',stress['value'],'management',O['management_delivery']['value'])
