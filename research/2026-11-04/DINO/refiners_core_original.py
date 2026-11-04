"""PBF/DINO Stage 3. USD billions; volume million barrels; margins $/bbl.
Research 2026-11-03 23:35 ET, Nov3 scanner. Explicit assumptions, no price fitting.
Run: python refiners_model.py -> inputs_and_results.json and model_tables.txt.
"""
from pathlib import Path
from copy import deepcopy
import json, math
OUT=Path(__file__).parent

def extend(first,g=.02):return first+[first[-1]*(1+g)**i for i in range(1,6)]
def ddm(d,k=.12,g=.02):return d/(k-g)  # next-year distribution; perpetuity reference

def jv_value(c):
    # equity distributions AFTER JV tax, debt service, maintenance and partner claims
    k=c['jv_ke']; pv=0; rows=[]
    for i in range(10):
        old=c['jv_dist']*(1+c['jv_growth'])**i
        contribution=c['jv_contributions'][i] if i<len(c['jv_contributions']) else 0
        new=(c['new_jv_dist']*(1+c['jv_growth'])**(i-c['new_jv_start'])) if i>=c['new_jv_start'] else 0
        flow=old+new-contribution
        pv+=flow/(1+k)**(i+1.16);rows.append(flow)
    terminal=(old+new)*(1+c['jv_growth'])/(k-c['jv_growth'])
    return pv+terminal/(1+k)**10.16,rows

def calc(c,delta_margin=0,wacc=None,terminal_g=None,rin=0,extra_capex=0,claim=0,volume_mult=1):
    w=c['wacc'] if wacc is None else wacc;tg=c['terminal_g'] if terminal_g is None else terminal_g
    assert w>tg and c['terminal_roic']>tg
    years=[];pv=0
    for i in range(10):
        factor=(1+c['inflation'])**i
        volume=c['volume']*volume_mult*(1+c['volume_growth'])**i
        margin=c['margins'][i]+delta_margin
        opex=c['opex']*factor
        ref=volume*(margin-opex)/1000-c['ref_sga']*factor
        other=sum(c['other_ebitda'].values())*(1+c['other_growth'])**i
        corporate=c['corporate']*factor
        ebitda=ref+other-corporate-rin
        da=c['da']*factor;ebit=ebitda-da
        tax=max(ebit,0)*c['tax'];nopat=ebit-tax
        maintain=c['maintain'][i] if i<len(c['maintain']) else c['maintain'][-1]*(1+c['inflation'])**(i-len(c['maintain'])+1)
        growth_capex=c['growth_capex']*factor
        wc=c['wc'][i] if i<len(c['wc']) else c['wc'][-1]*factor
        special=c['special_cash'][i] if i<len(c['special_cash']) else 0
        fcff=nopat+da-maintain-growth_capex-wc-special-extra_capex
        disc=(1+w)**(i+1.16);pv+=fcff/disc
        years.append(dict(year=2027+i,volume=volume,gross_margin=margin,opex=opex,refining_ebitda=ref,other_ebitda=other,corporate=corporate,ebitda=ebitda,da=da,ebit=ebit,tax=tax,nopat=nopat,maintenance=maintain,growth_capex=growth_capex,wc=wc,special_cash=special,fcff=fcff,pv_fcff=fcff/disc))
    # Terminal g/ROIC reinvestment cannot erase recurring maintenance > depreciation.
    terminal_nopat=years[-1]['nopat']*(1+tg)
    recurring_floor=max(0,years[-1]['maintenance']*(1+tg)-years[-1]['da']*(1+tg))+extra_capex
    reinvest=max(0,terminal_nopat*tg/c['terminal_roic'],recurring_floor)
    terminal_fcff=terminal_nopat-reinvest
    tv=max(0,terminal_fcff)/(w-tg);pvtv=tv/(1+w)**10.16
    # Q4 bridge: estimates for full unreported Q4 against Sep30 cash/debt, adjusted for known redemption.
    s=c['stub'];stub_ebitda=s['volume']*(s['gross_margin']-s['opex'])/1000+s['net_other']
    stub_ebit=stub_ebitda-s['da'];stub_fcff=stub_ebit-max(stub_ebit,0)*c['tax']+s['da']-s['capex']-s['wc']-s['opening_tax_settlement']
    stubpv=stub_fcff/(1+w)**.16
    jv,jvrows=jv_value(c)
    ev=pv+pvtv+stubpv;equity=ev+jv-c['net_claims']-claim
    # PBF convertible principal stays debt. Capped call offsets spread until $123.20.
    basic_price=equity/c['shares']
    price=basic_price
    if c['ticker']=='PBF' and basic_price>c['convert_cap']:
        n=c['convert_principal']/c['convert_strike']
        price=(equity+n*c['convert_cap'])/(c['shares']+n)
    return dict(price=max(0,price),raw_price=price,core_ev=ev,equity=equity,explicit_pv=pv,terminal_pv=pvtv,terminal_percent=pvtv/ev if ev else 0,terminal_fcff=terminal_fcff,terminal_reinvestment=reinvest,stub_fcff=stub_fcff,stub_pv=stubpv,jv_value=jv,jv_cash_flows=jvrows,net_claims=c['net_claims']+claim,years=years)

COMMON=dict(volume_growth=0,inflation=.02,other_growth=.02,terminal_g=.015,terminal_roic=.10,jv_growth=.02,jv_ke=.12,jv_contributions=[],new_jv_dist=0,new_jv_start=99,special_cash=[],wc=[.10,.05,.025],growth_capex=.10)
P=dict(COMMON,ticker='PBF',price=77.81,scanner_price=77.81,shares=.124,volume=335,opex=8.0,ref_sga=0,other_ebitda={'logistics':.25},corporate=.40,da=.70,tax=.26,wacc=.1125,margins=extend([23,19,16.5,15.5,15]),maintain=[1.05,.95,.969,.98838,1.0081476],jv_dist=.05,net_claims=(1.390+.0289+.070+.1062+.1496+.030-(2.5443-.8534-.010-.700)-(.1682/.85-.1682)/(1.1125**5)),convert_principal=.55,convert_strike=96.8,convert_cap=123.2,stub=dict(volume=87,gross_margin=30,opex=8,net_other=-.05,da=.175,capex=.24,wc=.1,opening_tax_settlement=.3612))
D=dict(COMMON,ticker='DINO',price=113.36,scanner_price=113.56,shares=.174,volume=238,opex=8.7,ref_sga=.25,other_ebitda={'renewables':.15,'marketing':.12,'lubricants':.35,'midstream_ex_jvs_before_nci':.40},corporate=.12,da=.90,tax=.25,wacc=.105,margins=extend([35,28,23,20,19]),maintain=[.80,.816,.83232,.8489664,.865945728],growth_capex=.15,terminal_roic=.12,jv_dist=.025,jv_ke=.115,jv_contributions=[.24,.245,.245],new_jv_dist=.065,new_jv_start=3,special_cash=[.288,.05],net_claims=.833,stub=dict(volume=61,gross_margin=42,opex=8.8,net_other=.225,da=.225,capex=.229,wc=.10,opening_tax_settlement=.445))
PB=deepcopy(P);PB.update(margins=extend([18,15,13.5,13.5,13.5],.015),volume=320,opex=8.2,corporate=.43,wacc=.125,terminal_g=0,terminal_roic=.08,maintain=[1.10,1.0,1.02,1.0404,1.061208],growth_capex=.075,jv_dist=.01,jv_contributions=[.05],net_claims=P['net_claims']+.30,special_cash=[.20]);PB['stub']['gross_margin']=22
PU=deepcopy(P);PU.update(margins=extend([29,25,21,19,18],.025),volume=350,opex=7.7,corporate=.36,wacc=.10,terminal_g=.02,terminal_roic=.15,maintain=[1.05,.95,.969,.98838,1.0081476],growth_capex=.15,jv_dist=.08);PU['stub']['gross_margin']=34
DB=deepcopy(D);DB.update(margins=extend([25,20,16,15,15],.015),volume=225,opex=9.0,ref_sga=.27,corporate=.15,wacc=.1175,terminal_g=0,terminal_roic=.09,other_ebitda={'renewables':0,'marketing':.09,'lubricants':.23,'midstream_ex_jvs_before_nci':.36},maintain=[.90,.918,.93636,.9550872,.974188944],growth_capex=.15,special_cash=[.438,.15],new_jv_start=4,new_jv_dist=.04,jv_contributions=[.29,.295,.295],net_claims=D['net_claims']+.25);DB['stub']['gross_margin']=30
DU=deepcopy(D);DU.update(margins=extend([42,36,29,25,23],.025),volume=250,opex=8.4,ref_sga=.23,corporate=.10,wacc=.095,terminal_g=.02,terminal_roic=.15,other_ebitda={'renewables':.25,'marketing':.15,'lubricants':.45,'midstream_ex_jvs_before_nci':.44},growth_capex=.20,other_growth=.03,new_jv_dist=.09,special_cash=[.218,.025]);DU['stub']['gross_margin']=46
CASES={'PBF':{'bear':PB,'base':P,'bull':PU},'DINO':{'bear':DB,'base':D,'bull':DU}}
def solve(func,target,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if func(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2

def steady_shift(c,delta,wacc=None):
    q=deepcopy(c)
    q['margins']=[m if i<4 else m+delta*(1+c['inflation'])**(i-4) for i,m in enumerate(c['margins'])]
    return calc(q,wacc=wacc)

def equity_return(c, purchase_price=None):
    """Illustrative shareholder cash IRR, NOT a predicted realized return.
    Maintain opening gross financial debt, refinance at assumed pretax cost, distribute
    all available FCFE, and sell at year10 core terminal DCF plus JV terminal less debt.
    Pay legacy nonfinancial net claims from opening excess cash; taxes already in stub.
    Negative FCFE is a shareholder contribution rather than a free funding assumption.
    """
    r=calc(c); debt=c['financial_debt']; interest=debt*c['cost_debt']*(1-c['tax'])
    flows=[(.16,c['excess_cash']+r['stub_fcff']-(c['net_claims']-debt+c['excess_cash'])-interest/4)]
    for i,row in enumerate(r['years']):
        flow=row['fcff']-interest+r['jv_cash_flows'][i]
        if i==9:
            old=c['jv_dist']*(1+c['jv_growth'])**9
            new=c['new_jv_dist']*(1+c['jv_growth'])**(9-c['new_jv_start']) if 9>=c['new_jv_start'] else 0
            exit_equity=max(0,r['terminal_fcff'])/(c['wacc']-c['terminal_g'])+(old+new)*(1+c['jv_growth'])/(c['jv_ke']-c['jv_growth'])-debt
            flow+=exit_equity
        flows.append((i+1.16,flow))
    capital=(c['price'] if purchase_price is None else purchase_price)*c['shares']
    lo,hi=-.05,.75
    def npv(k):return sum(f/(1+k)**t for t,f in flows)-capital
    # Avoid reporting a unique IRR if negative cash flows create nonmonotonic roots.
    roots=[];lastx=lo;last=npv(lo)
    for j in range(1,801):
        x=lo+(hi-lo)*j/800;y=npv(x)
        if last*y<0:
            l,h=lastx,x
            for _ in range(80):
                m=(l+h)/2
                if npv(l)*npv(m)<=0:h=m
                else:l=m
            roots.append((l+h)/2)
        lastx,last=x,y
    return dict(irr=roots[0] if len(roots)==1 else None,root_count=len(roots),cash_flows=flows,assumed_annual_aftertax_interest=interest)

P.update(financial_debt=1.390+.0289+.070,excess_cash=2.5443-.8534-.010-.700,cost_debt=.075)
D.update(financial_debt=2.8+.09+.107,excess_cash=3.333-.800,cost_debt=.063)
# Cases created before these funding attributes; propagate the fixed opening bridge.
for ticker,cases in CASES.items():
    for c in cases.values():
        for key in ['financial_debt','excess_cash','cost_debt']:c[key]=cases['base'][key]

def build():
 results={};lines=[]
 for ticker,cases in CASES.items():
  base=cases['base'];rr={name:calc(c) for name,c in cases.items()};results[ticker]={'inputs':cases,'results':rr}
  lines.append('\n'+ticker)
  for name,r in rr.items():lines.append(f"{name}: price {r['price']:.4f}; coreEV {r['core_ev']:.4f}; JV {r['jv_value']:.4f}; claims {r['net_claims']:.4f}; stub {r['stub_fcff']:.4f}; TV% {r['terminal_percent']:.1%}")
  lines.append('Base years:')
  for row in rr['base']['years']:lines.append(' '.join(f'{k}={v:.4f}' if isinstance(v,float) else f'{k}={v}' for k,v in row.items()))
  sens=[]
  for delta in [-2,0,2]:
   for w in [base['wacc']-.01,base['wacc'],base['wacc']+.01]:
    for rin,capex in [(0,0),(.15,.1)]:
     row=dict(margin_delta=delta,wacc=w,extra_RIN_net_cost=rin,extra_annual_capex=capex,price=calc(base,delta_margin=delta,wacc=w,rin=rin,extra_capex=capex)['price']);sens.append(row)
  results[ticker]['joint_sensitivity']=sens
  lines.append('joint sensitivity: '+json.dumps(sens))
  reverse=[]
  for w in [base['wacc']-.01,base['wacc'],base['wacc']+.01]:
   delta=solve(lambda d:calc(base,delta_margin=d,wacc=w)['price'],base['price'],-10,20)
   reverse.append(dict(wacc=w,all_year_margin_shift=delta,required_2031_margin=base['margins'][4]+delta))
  results[ticker]['reverse']=reverse;lines.append('reverse:'+json.dumps(reverse))
  revsteady=[]
  for w in [base['wacc']-.01,base['wacc'],base['wacc']+.01]:
   delta=solve(lambda d:steady_shift(base,d,w)['price'],base['price'],-10,20)
   revsteady.append(dict(wacc=w,steady_only_margin_shift=delta,required_2031_margin=base['margins'][4]+delta))
  results[ticker]['reverse_steady_only']=revsteady;lines.append('reverse steady only:'+json.dumps(revsteady))
  extras={
   'volume_minus_5pct':calc(base,volume_mult=.95)['price'],
   'diluted_shares_plus_5pct':calc(dict(base,shares=base['shares']*1.05))['price'],
   'diluted_shares_plus_10pct':calc(dict(base,shares=base['shares']*1.10))['price'],
   'flat_normal_from_2027':calc(dict(base,margins=[base['margins'][4]*(1+base['inflation'])**(i-4) for i in range(10)]))['price'],
   'extra500mclaim':calc(base,claim=.5)['price'],
   'tax_plus_5pct':calc(dict(base,tax=base['tax']+.05))['price'],
   'terminal_growth':{str(g):calc(base,terminal_g=g)['price'] for g in [0,.015,.025]}
  }
  results[ticker]['additional_sensitivity']=extras;lines.append('additional sensitivity:'+json.dumps(extras))
  eq=equity_return(base);results[ticker]['illustrative_equity_return_base']=eq;lines.append('equity cash IRR '+str(eq['irr']))
  moderate=[]
  for name,delta,dw,rin,cap in [('moderately_cautious',-.5,.005,.075,.05),('moderately_constructive',.5,-.005,0,0)]:
   q=deepcopy(base);q['margins']=[m+delta for m in q['margins']];q['wacc']+=dw
   # Apply incremental RIN cost as recurring corporate expense; separate capital floor.
   value=calc(base,delta_margin=delta,wacc=q['wacc'],rin=rin,extra_capex=cap)['price']
   moderate.append(dict(name=name,margin_delta=delta,wacc=q['wacc'],incremental_RIN_cost=rin,incremental_annual_capex=cap,price=value))
  results[ticker]['moderate_joint_scenarios']=moderate;lines.append('moderate joint:'+json.dumps(moderate))
  assert all(math.isfinite(r['price']) and r['price']>=0 for r in rr.values())
  assert rr['bear']['price']<rr['base']['price']<rr['bull']['price']
  assert calc(base,delta_margin=1)['price']>calc(base)['price']
  assert calc(base,claim=.1)['price']<calc(base)['price']
  assert calc(base,wacc=base['wacc']+.01)['price']<calc(base)['price']
  # WACC-equivalent return on specified cash flows; not realized equity CAGR
  irr=solve(lambda negw:calc(base,wacc=-negw)['price'],base['price'],-.30,-.02)
  results[ticker]['implied_WACC_on_base_path']=-irr;lines.append('implied WACC '+str(-irr))
  for termg in [0,.015,.025]:lines.append(f"terminalg {termg}: {calc(base,terminal_g=termg)['price']:.3f}")
  lines.append('immediate real normalization: '+str(extras['flat_normal_from_2027']))
  lines.append('extra500mclaim: '+str(calc(base,claim=.5)['price']))
  lines.append('plus5pcttax: '+str(calc(dict(base,tax=base['tax']+.05))['price']))
 (OUT/'inputs_and_results.json').write_text(json.dumps(results,indent=2));(OUT/'model_tables.txt').write_text('\n'.join(lines));print('\n'.join(lines))
if __name__=='__main__':build()
