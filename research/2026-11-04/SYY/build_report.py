"""Rebuild report from frozen research JSON; does not modify research inputs."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
load=lambda s:json.loads((P/s).read_text())
I=load('model/inputs.json'); R=load('model/results.json'); H=load('history/history.json'); S=load('model/sensitivities.json'); C=load('capital/facts.json'); J=load('jrd/facts.json'); peers=load('comps/outputs.json')['peers']
num=lambda x,n=0: 'n/d' if x is None else f'{x:,.{n}f}'
def table(headers,rows):
 return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])
hist=table(['Periodo','Ventas','EBIT GAAP','Beneficio neto','CFO','Capex bruto','D&A¹','SBC','CFO−capex'],[[p]+[num(H['periods'][p]['metrics'][k]['value']) for k in ['revenue','ebit','net_income','cfo','ppe_capex','da_ex_financing','sbc','fcf_gross_capex']] for p in ['FY24','FY25','FY26','Q2FY26','Q3FY26','Q4FY26','Q1FY27','TTM']])
forecast={}
for who in ['syy','jrd']:
 forecast[who]=table(['Fin 3 noviembre','Ventas','Margen','NOPAT','D&A físico','Capex','ΔWC','Otra inversión','FCFF'],[[x['endDate'][:4],num(x['revenue']),f"{x['margin']*100:.2f}%"]+[num(x[k]) for k in ['nopat','daPhysical','grossCapitalSpending','wcInvestment','otherGrowthInvestment','fcff']] for x in R['base'][who]['rows']])
scenario=table(['Supuesto','Bajista','Central','Alcista'],[[label]+[fmt(I['scenarios'][c][who][key]) for c in ['bear','base','bull']] for label,who,key,fmt in [('SYY margen año 1','syy','margin1',lambda x:f'{x:.1%}'),('SYY margen año 10','syy','margin10',lambda x:f'{x:.1%}'),('SYY WACC','syy','wacc',lambda x:f'{x:.1%}'),('SYY ROIC incremental','syy','roic',lambda x:f'{x:.1%}'),('JRD margen año 1','jrd','margin1',lambda x:f'{x:.1%}'),('JRD margen año 10','jrd','margin10',lambda x:f'{x:.1%}'),('JRD WACC','jrd','wacc',lambda x:f'{x:.1%}'),('JRD ROIC incremental','jrd','roic',lambda x:f'{x:.1%}'),('Crecimiento terminal ambos','syy','g',lambda x:f'{x:.1%}')]])
values=table(['Caso operativo','EV SYY','EV JRD','Sinergias netas VP','Fracaso regulatorio $/acc.','Cierre $/acc.'],[[c]+[num(R[k][b]['enterpriseValue']) for b in ['syy','jrd']]+[num(R[k]['synergyValue']),num(R[k]['conditionalFailureValuePerShare'],2),num(R[k]['conditionalImmediateCloseValuePerShare'],2)] for c,k in [('Bajista','bear'),('Central','base'),('Alcista','bull')]])
bridgerows=[('EV SYY',R['base']['syy']['enterpriseValue']),('Caja septiembre',3171),('Deuda contable septiembre',-13820),('Colchón principal y coberturas',-200),('Caja operativa reservada',-1500),('Déficit pensiones bruto junio',-401),('UTB e intereses',-92),('Reserva temporal fiscal',-126),('Costo financiación octubre aproximado',-222),('Equity antes de costos de fracaso',R['base']['syy']['enterpriseValue']+R['base']['capitalBridgeProxy'])]
bridge=table(['Puente SYY central','USD millones'],[[a,num(b,1)] for a,b in bridgerows])
compstable=table(['Empresa','EV/EBIT GAAP','EV/(EBIT + amortización adquirida)','Fecha capital','Calificación'],[[x['ticker'],num(x['principal_based_ev_to_gaap_ebit'] or x['carrying_debt_ev_proxy_to_gaap_ebit'],2)+'x',num(x['principal_based_ev_to_ebit_plus_amortization'] or x['carrying_debt_ev_proxy_to_ebit_plus_amortization'],2)+'x',x['capital_date'],'Principal histórico' if x['ticker']=='USFD' else 'Proxy deuda contable'] for x in peers])
ctx={'EFFICIENCY_CLOSE':num(S['marginEfficiencyNoExtraCapitalSensitivity']['close'],2),'EFFICIENCY_FAILURE':num(S['marginEfficiencyNoExtraCapitalSensitivity']['failure'],2),'HISTORY':hist,'FORECAST_SYY':forecast['syy'],'FORECAST_JRD':forecast['jrd'],'SCENARIOS':scenario,'VALUES':values,'BRIDGE':bridge,'COMPS':compstable,'FAILURE':num(R['base']['conditionalFailureValuePerShare'],2),'CLOSE':num(R['base']['conditionalImmediateCloseValuePerShare'],2),'REVERSE':num(S['conditionalCloseReverse']['roots'][0]['parallelMarginIncrease']*100,2)}
t=(P/'report_template.md').read_text()
for k,v in ctx.items():t=t.replace('{{'+k+'}}',v)
assert '{{' not in t
(P/'report.md').write_text(t)
print('Report words:',len(t.split()))
