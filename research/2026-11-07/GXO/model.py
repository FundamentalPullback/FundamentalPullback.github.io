"""Modelo FCFF previsto, NO calibrado ni aprobado para GXO.
Uso sin argumentos: verifica históricos y conserva valuation=null.
Con JSON revisado: 10 filas, cinco explícitas y cinco transición; no defaults económicos.
"""
import json, pathlib, sys
P=pathlib.Path(__file__).parent

def value(plan):
    if plan.get('core_bridges_reviewed') is not True:
        raise ValueError('Puentes fundamentales sin revisar; no calcular valor.')
    rows=plan['years']; assert len(rows)==10
    assert [x['stage'] for x in rows]==['explicit']*5+['transition']*5
    w=plan['wacc'];g=plan['terminal_growth'];r=plan['terminal_roic']
    assert 0<=g<w and r>g and plan['diluted_shares']>0
    flows=[]
    for i,x in enumerate(rows,1):
        # EBIT conserva SBC y alquiler operativo. D&A incluye depreciación finance-lease.
        # Cash capex contiene software: NO añadirlo por segunda vez.
        # Las altas finance-lease se tratan como inversión y su deuda se resta una sola vez.
        nopat=x['ebit_after_sbc']*(1-x['operating_tax'])
        investment=x['cash_capex_including_software']+x['finance_lease_asset_additions']
        fcff=nopat+x['da']-investment-x['change_operating_nwc']
        flows.append(dict(year=i,nopat=nopat,investment=investment,fcff=fcff,pv=fcff/(1+w)**i))
    terminal_nopat=plan['terminal_revenue']*plan['terminal_ebit_margin_after_sbc']*(1-plan['terminal_tax'])
    reinvestment=terminal_nopat*g/r
    terminal_fcff=terminal_nopat-reinvestment
    tv=terminal_fcff/(w-g);pvtv=tv/(1+w)**10
    ev=sum(x['pv'] for x in flows)+pvtv
    # Operating leases stay expense-based, therefore NOT deducted again from EV.
    equity=ev-plan['financial_debt_including_finance_leases']-plan['other_claims']+plan['excess_cash']
    return dict(years=flows,terminal_reinvestment=reinvestment,terminal_fcff=terminal_fcff,terminal_value=tv,ev=ev,equity=equity,value_per_share=equity/plan['diluted_shares'],terminal_pv_weight=pvtv/ev)

if __name__=='__main__':
    if len(sys.argv)>1:
        p=json.load(open(sys.argv[1])); print(json.dumps(value(p),indent=2))
    else:
        r=json.load(open(P/'results.json'))
        assert r['historical_calculations']['TTM_current']['fcf_company']==229
        assert r['historical_calculations']['TTM_previous']['fcf_company']==223
        assert r['historical_calculations']['investment_9m2026_cash_plus_finance_lease_additions']==411
        assert r['valuation']['fair_value'] is None
        print('Históricos verificados. DCF no calibrado: faltan puentes materiales; ningún precio objetivo generado.')
