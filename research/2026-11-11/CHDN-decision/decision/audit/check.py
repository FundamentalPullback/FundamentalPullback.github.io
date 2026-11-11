import json,pathlib
p=pathlib.Path(__file__).resolve().parents[1];r=json.loads((p/'results.json').read_text());a=json.loads((p/'actuals.json').read_text())['TTM2026']
def value(c):
    rev=a['revenue'];old_profit=a['ebit']*.74;start=a['ebit']/rev;v=0;j=0;dist=c['jv_cash'];caps=[]
    for t in range(1,11):
        fade=max(0,(t-5)/5);growth=c['growth']*(1-fade)+c['g']*fade
        old=rev;rev*=1+growth;mar=start+(c['margin']-start)*min(t/5,1);profit=rev*mar*.74
        investment=max(0,old_profit*growth if c.get('growth_only_capital') else profit-old_profit)/c['roic'];wc=(rev-old)*.02;da=rev*.078
        cap=max(da+investment-wc,c['project_caps'][t-1] if t<=len(c['project_caps']) else -1e100);caps.append(cap)
        v+=(profit+da-cap-wc)/(1+c['wacc'])**t
        dist*=1+c['jv_growth']*(1-fade)+c['g']*fade
        net=dist*(1-c['jv_parent_tax']/c['jv_cash']) if c['jv_cash'] else 0
        j+=net/(1+c['ke'])**t;old_profit=profit
    v+=profit*(1+c['g'])*(1-c['g']/c['roic'])/((c['wacc']-c['g'])*(1+c['wacc'])**10)
    j+=net*(1+c['g'])/((c['ke']-c['g'])*(1+c['ke'])**10)
    b=c['bridge'];eq=v+j+b['excess_cash']-sum(b[k] for k in ['debt','minority','finance_lease_proxy','liability_awards'])
    return max(0,eq/b['shares']),caps
checks=[]
for k,q in r['cases'].items():
 x,c=value(q['assumptions']);assert abs(x-q['result']['per_share'])<1e-9;checks.append(dict(case=k,value=x,first_two_capex=c[:2]))
b=r['cases']['central_normalized']['assumptions'];sweeps=[]
for w,target in r['inverse_year5_margin'].items():
 vals=[value(b|dict(wacc=float(w),margin=.1+i*.0005))[0] for i in range(1001)]
 monotonic=all(y>=x-1e-9 for x,y in zip(vals,vals[1:])); mx=max(vals)
 if target is not None:assert abs(value(b|dict(wacc=float(w),margin=target))[0]-101.96)<1e-8
 else:assert mx<101.96
 sweeps.append(dict(wacc=float(w),target=target,monotonic=monotonic,max_value=mx,end_value=vals[-1],min_value=min(vals)))
e=101.96*68.548342;w=(.0939*e+.065*.74*4748)/(e+4748);assert abs(w-r['inputs']['wacc'])<1e-12
out=dict(cases=checks,inverse_grid=sweeps,wacc=w,status='PASS');(pathlib.Path(__file__).parent/'output.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
# Independently reconstruct all published sensitivity parameter mappings.
s={}
s['zero_incremental_parent_tax']=value(b|dict(jv_parent_tax=0))[0]
s['tax_distributions_instead_of_earnings']=value(b|dict(jv_parent_tax=130.3*.9*.26))[0]
for name,kd in [('kd_6',.06),('kd_7',.07),('kd_8',.08)]:s[name]=value(b|dict(wacc=(.0939*e+kd*.74*4748)/(e+4748)))[0]
for x in [100,200,300]:s['extra_project_year1_'+str(x)]=value(b|dict(project_caps=[350+x,320]))[0]
for x in [100,130.3,149,175]:s['jv_cash_'+str(x)]=value(b|dict(jv_cash=x))[0]
for z in [.12,.15,.20]:s['central_roic_'+str(z)]=value(b|dict(roic=z,growth_only_capital=True))[0]
for name,x in s.items(): assert abs(x-r['sensitivity'][name])<1e-9
out['sensitivities']=s;(pathlib.Path(__file__).parent/'output.json').write_text(json.dumps(out,indent=2))
