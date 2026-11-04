"""Ten annual-period unlevered models. USD millions. Own assumptions, not forecasts."""
def operating(p, common):
    rows=[];prev=p['priorNopatAnchor'];ev=0
    for n in range(1,11):
        fade=min((n-1)/4,1)
        inflation=(1+common['inflation'])**(n-1)
        scale=(1+p.get('realVolumeChange',0))**(n-1)
        ebitda=(p['ebitdaYear1']+(p['ebitdaNormalizedYear5']-p['ebitdaYear1'])*fade)*inflation*scale
        corporate=p.get('corporateCashCostYear1',0)*inflation
        da=p['daYear1']*inflation
        ebit=ebitda-corporate-da
        # No immediate cash refund assumed when operations lose money.
        nopat=ebit-max(ebit,0)*common['tax']
        physical=p['physicalCapexYear1']*inflation
        turnaround=p['turnaroundCapexYear1']*inflation
        wc=p['annualWorkingCapitalInvestmentYear1']*inflation
        maintenance_net=max(0,physical+turnaround-da)+wc
        growth_net=(max(0,nopat-prev) if p.get('fundAllPositiveNopatGrowth',True) else min(max(0,nopat-prev),max(0,nopat)*max(0,common['inflation']+p.get('realVolumeChange',0))))/p['roic']
        reinvest=max(maintenance_net,growth_net)
        gross_capex=da+reinvest-wc
        fcff=nopat-reinvest
        df=(1+p['wacc'])**n
        row=dict(year=n,periodEnd=f'{2026+n}-11-03',ebitdaBeforeTurnaroundCash=ebitda,corporateCashCost=corporate,daIncludingTurnaround=da,ebit=ebit,nopat=nopat,physicalCapexFloor=physical,turnaroundCapexFloor=turnaround,workingCapitalInvestment=wc,maintenanceNetReinvestment=maintenance_net,growthNetReinvestment=growth_net,netReinvestment=reinvest,grossCapitalInvestment=gross_capex,fcff=fcff,discountFactor=df,pv=fcff/df)
        rows.append(row);ev+=row['pv'];prev=nopat
    z=rows[-1];g=p['g']; assert p['wacc']>g
    nt=z['nopat']*(1+g)
    terminal_floor=max(0,(z['physicalCapexFloor']+z['turnaroundCapexFloor']-z['daIncludingTurnaround'])*(1+g))+z['workingCapitalInvestment']*(1+g)
    terminal_growth=max(0,nt)*g/p['roic']
    reinvest=max(terminal_floor,terminal_growth)
    tf=nt-reinvest;tv=tf/(p['wacc']-g);pv=tv/(1+p['wacc'])**10
    return {'operatingEV':ev+pv,'pvExplicit':ev,'pvTerminal':pv,'terminal':{'nopat':nt,'maintenanceNetReinvestment':terminal_floor,'growthNetReinvestment':terminal_growth,'netReinvestment':reinvest,'fcff':tf,'undiscountedValue':tv},'rows':rows}
