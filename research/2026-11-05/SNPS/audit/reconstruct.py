from pathlib import Path
import json,math,copy,hashlib
P=Path(__file__).resolve().parent
A=json.loads((P/'inputs_reviewed.json').read_text());S=json.loads((P/'results_reviewed.json').read_text());checks=[]
def ck(name,got,expected,tol=1e-7):
 error=abs(got-expected);checks.append({'name':name,'actual':got,'expected':expected,'error':error,'passed':error<=tol});assert error<=tol,(name,got,expected)
def independent(case='base',**changes):
 a=copy.deepcopy(A['cases'][case]);a.update(changes);m=A['market'];c=A['capital'];wacc=changes.get('wacc',(m['rf']+m['beta']*m['erp'])*(1-m['debt_weight'])+m['cost_debt']*(1-m['tax'])*m['debt_weight']+a['wacc_delta'])
 start=A['segments'];revs=dict(start);last_total=sum(start.values());annual=[]
 for yr in range(1,11):
  rates={}
  for key in revs:
   rate=(a['growth'][key][yr-1] if yr<=5 else (a['growth'][key][4]*(10-yr)+a['g']*(yr-5))/5)
   if 'constant_growth' in a:rate=a['constant_growth'] if yr<=5 else (a['constant_growth']*(10-yr)+a['g']*(yr-5))/5
   rates[key]=rate;revs[key]*=1+rate
  revenue=sum(revs.values());margin=a['margin'][min(yr,5)-1]+a.get('margin_shift',0);ebit=revenue*margin;nopat=ebit*(1-a['tax']);da=revenue*a['da'];capex=revenue*a['capex'][min(yr,5)-1];dnwc=(revenue-last_total)*a['wc_increment'];strategic=revenue*a['strategic'];ordinary=capex+dnwc+strategic-da;target=nopat*a['g']/a['roic'];weight=max(0,yr-5)/5;net=ordinary+(target-ordinary)*weight;fcff=nopat-net
  annual.append({'year':2026+yr,'segments':dict(revs),'revenue':revenue,'growth':revenue/last_total-1,'margin':margin,'ebit':ebit,'tax':ebit*a['tax'],'nopat':nopat,'da':da,'capex':capex,'dnwc':dnwc,'strategic':strategic,'transition_adjust':net-ordinary,'net_reinvestment':net,'fcff':fcff,'pv':fcff*math.exp(-yr*math.log1p(wacc))});last_total=revenue
 tnop=annual[-1]['nopat']*(1+a['g']);treinv=tnop*a['g']/a['roic'];tfcff=tnop-treinv;tv=tfcff/(wacc-a['g']);tpv=tv*(1+wacc)**-10;ev=sum(x['pv'] for x in annual)+tpv;cash=c['cash_july']+c['q4_fcf_rollforward']-c['asr_cash_paid']-c['operating_cash_reserve'];bridge=cash-c['debt_principal_and_lock'];shares=c['fully_diluted_pre_asr']-c['initial_asr_shares'];per=(ev+bridge)/shares
 return {'wacc':wacc,'rows':annual,'terminal_nopat':tnop,'terminal_reinvestment':treinv,'terminal_fcff':tfcff,'terminal_value':tv,'terminal_pv':tpv,'terminal_weight':tpv/ev,'ev':ev,'excess_cash':cash,'bridge':bridge,'shares':shares,'value':per,'upside':per/A['price']-1}
def compare(label,mine,theirs):
 for k,v in mine.items():
  if k=='rows':
   for i,row in enumerate(v):
    for field,num in row.items():
     if field=='segments':
      for seg,num2 in num.items():ck(f'{label}.Y{i+1}.{seg}',num2,theirs[k][i][field][seg])
     else:ck(f'{label}.Y{i+1}.{field}',num,theirs[k][i][field])
  else:ck(label+'.'+k,v,theirs[k])
R={n:independent(n) for n in A['cases']}
for case,res in R.items():compare(case,res,S['cases'][case])
mod=independent(growth={k:[v-.02 for v in vs] for k,vs in A['cases']['base']['growth'].items()},margin_shift=-.02,wacc_delta=.005,g=.025);compare('moderate',mod,S['moderate_combined_stress'])
mgmt=independent(constant_growth=.15,margin=[.353,.38,.405,.425,.43]);compare('management',mgmt,S['management_delivery'])
for row in S['sensitivity']:ck(f"sensitivity.{row['wacc']}.{row['g']}",independent(wacc=row['wacc'],g=row['g'])['value'],row['value'])
for key,kw in [('reverse_constant_growth','constant_growth'),('reverse_margin_shift','margin_shift')]:ck(key,independent(**{kw:S[key]})['value'],A['price'])
(P/'independent_results.json').write_text(json.dumps(R,indent=2));(P/'checks.json').write_text(json.dumps({'passed':all(c['passed'] for c in checks),'count':len(checks),'max_error':max(c['error'] for c in checks),'checks':checks},indent=2))
print(len(checks),'passed; max',max(c['error'] for c in checks));print({k:r['value'] for k,r in R.items()})
