"""HNI: illustrative conditional FCFF, NOT an approved valuation or entry.
All financial amounts USD millions. Inputs distinguish assumptions from filings.
Run python model.py to reproduce model_results.json next to this file.
"""
import json
from pathlib import Path
PRICE=47.26
SHARES=73.373322  # Oct3 actual72.273322 +0.8 participating +0.2 dilutive +0.1 antidilutive proxy; final awards audit pending
DEBT=1373.9+13.4 # nominal financing plus finance lease; operating leases left in EBIT
CASH_EXCESS=0.0 # operating cash reserve conservatively absorbs110.3 cash+3.7 investments
BENEFITS=69.4 # Jan3 legacy15.3+Steelcase pension29.6+retiree24.5, stale proxy
NCI=6.4
RF=.0486; ERP=.0441; KD=.054 # approximate weighted observed financing rates
TAX=.25

def wacc(beta):
    e=SHARES*PRICE;d=DEBT
    return (RF+beta*ERP)*e/(e+d)+KD*(1-TAX)*d/(e+d)

CASES={
 'adverse':dict(beta=1.20,growth=.00,margin_start=.048,margin5=.058,margin10=.058,sales_capital=2.0,terminal_roic=.10,g=.02),
 'central':dict(beta=.94,growth=.03,margin_start=.053,margin5=.075,margin10=.075,sales_capital=2.5,terminal_roic=.12,g=.025),
 'favorable':dict(beta=.80,growth=.05,margin_start=.058,margin5=.085,margin10=.085,sales_capital=3.0,terminal_roic=.14,g=.025)}

def value(c, growth_override=None, margin_shift=0):
    r=wacc(c['beta']); growth=c['growth'] if growth_override is None else growth_override
    sales=6000. # analyst pro forma annual starting scale, not reported annual revenue
    rows=[];pv=0
    for t in range(1,11):
        k=max(0,t-5)/5
        growth_t=growth+(c['g']-growth)*k
        prev=sales;sales*=1+growth_t
        margin=(c['margin_start']+(c['margin5']-c['margin_start'])*t/5 if t<=5 else c['margin5']+(c['margin10']-c['margin5'])*k)+margin_shift
        nopat=sales*margin*(1-TAX)
        explicit=max(0,sales-prev)/c['sales_capital']
        sustainable=nopat*c['g']/c['terminal_roic']
        reinvest=explicit*(1-k)+sustainable*k
        fcff=nopat-reinvest;discounted=fcff/(1+r)**t;pv+=discounted
        rows.append(dict(year=t,revenue=sales,ebit_margin=margin,nopat=nopat,net_reinvestment=reinvest,fcff=fcff,pv=discounted))
    terminal_nopat=sales*(1+c['g'])*(c['margin10']+margin_shift)*(1-TAX)
    tv=terminal_nopat*(1-c['g']/c['terminal_roic'])/(r-c['g'])
    tvpv=tv/(1+r)**10;ev=pv+tvpv
    eq=ev-DEBT-BENEFITS-NCI+CASH_EXCESS
    return dict(wacc=r,enterprise_value=ev,equity_value=eq,value_per_share=eq/SHARES,terminal_share_ev=tvpv/ev,years=rows)

def inverse(c):
    lo=-.10;hi=.20
    for _ in range(100):
        mid=(lo+hi)/2
        if value(c,mid)['value_per_share']<PRICE:lo=mid
        else:hi=mid
    return (lo+hi)/2

out={'status':'illustrative_not_approved','price_reference':PRICE,'price_date':'2026-11-06','scenarios':{k:value(v) for k,v in CASES.items()},'inverse_central_initial_growth':inverse(CASES['central']),'central_margin_sensitivity':{str(s):value(CASES['central'],margin_shift=s)['value_per_share'] for s in [-.01,0,.01]},'limitations':['Starting annual pro forma sales and normalized margin are assumptions, not audited recurring guidance.','Q2 refunds quantified35.3376m; additional Q3 refunds not separately quantified. Tax normalized25% rather than actual benefit.','Jan3 benefit obligations stale; no credit for COLI, affiliates or excess cash.','Published beta0.94 used centrally; acquisition-related beta range0.80–1.20 stressed, not peer-derived.','Awards proxy includes participating, incremental dilution and antidilutive shares; not grant-by-grant valuation.','Net reinvestment sales/capital model includes maintenance implicitly; no positive D&A addback.','No technical eligibility or historical multiple study completed.']}
out['bridge_sensitivities_per_share']={'benefits_zero_vs_proxy':BENEFITS/SHARES,'benefits_plus50':-50/SHARES,'all_cash_and_investments_excess':114/SHARES,'extra_1m_awards':out['scenarios']['central']['equity_value']/(SHARES+1)-out['scenarios']['central']['value_per_share']}
out['normalization_bridge_9m']={'reported_ebit':192.4,'inventory_purchaseaccounting_addback':36.4,'acquisition_cost_addback':8.6,'restructuring_addback':55.0,'retained_recurring_restructuring_assumption':-15.0,'q2_gross_refund_removed':-1472.4*.024,'normalized_before_unknown_q3_refunds':192.4+36.4+8.6+55-15-1472.4*.024,'additional_q3_refund_stress_not_estimate':[0,10,25]}
out['unknown_refund_persistent_margin_stress']={str(a):value(CASES['central'],margin_shift=-(a*4/3)/6000)['value_per_share'] for a in [0,10,25]}
out['central_tax28_operating_only']=(out['scenarios']['central']['enterprise_value']*(.72/.75)-DEBT-BENEFITS-NCI)/SHARES
Path(__file__).with_name('model_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:round(v['value_per_share'],2) for k,v in out['scenarios'].items()}));print('inverse',out['inverse_central_initial_growth'])
