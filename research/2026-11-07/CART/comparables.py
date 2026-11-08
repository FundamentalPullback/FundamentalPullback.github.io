import pathlib,json,csv
p=pathlib.Path(__file__).parent
# Prices: 2026-11-06 regular session; Q3 weighted diluted proxies explicitly not spot cap.
a=[dict(ticker='CART',price=58.12,shares=246.05709,sales_ttm=4149,ebit_ttm=596,cfo_ttm=1268,capex_cash_ttm=58,sales_q3=1095,ebit_q3=174,cash_securities=935,debt=0,nci=0),dict(ticker='DASH',price=179.67,shares=440,sales_ttm=3955+4036+4454+4616,ebit_ttm=147+749,cfo_ttm=2953,capex_cash_ttm=262+488,sales_q3=4616,ebit_q3=442,cash_securities=5053+929+805,debt=2728,nci=10)]
for x in a:
 x['equity_proxy']=x['price']*x['shares'];x['ev_simple_proxy']=x['equity_proxy']+x['debt']+x['nci']-x['cash_securities'];x['ev_sales']=x['ev_simple_proxy']/x['sales_ttm'];x['ev_ebit']=x['ev_simple_proxy']/x['ebit_ttm'];x['q3_ebit_margin']=x['ebit_q3']/x['sales_q3'];x['reported_cash_yield']=(x['cfo_ttm']-x['capex_cash_ttm'])/x['equity_proxy']
json.dump({'method':'EV simple con proxy de acciones diluidas, no EV normalizado ni precio objetivo. Caja sin ajuste operativo; leases omitidos simétricamente. DASH no incluye la adquisición pendiente de CART.','valuation_comparison':a,'uber_operating_only':{'sales_q3':14766,'ebit_q3':1447,'margin':1447/14766,'cfo_q3':2639,'capex_q3':104,'sbc_cashflow_q3':591,'price':68.59,'diluted_weighted_shares_q3':2050.324,'reason_no_equity_multiple':'Movilidad, Freight, seguros, inversiones cotizadas y por puesta en equivalencia; no múltiplo puro de grocery o publicidad. No atribuir su EV a Delivery.'}},open(p/'comparables.json','w'),indent=2)
with open(p/'comparables.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(a[0]));w.writeheader();w.writerows(a)
print([(x['ticker'],x['ev_sales'],x['ev_ebit']) for x in a])
