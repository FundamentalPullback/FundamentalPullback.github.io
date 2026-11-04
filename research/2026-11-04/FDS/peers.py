from pathlib import Path
import json
P=Path(__file__).parent
m={'ticker':'MSCI','price':639.78,'shares':72.3,'period':'TTM September2026','net_income':1202.305+1099-917.6,'cfo':1588.446+1113.7-1087.3,'physical_capex':39.319+27.2-26.9,'software_capex':90.542+96.7-66.7,'sbc':111.343+100.6-85.8}
f={'ticker':'FDS','price':332.59,'shares':35.572,'period':'FY/TTM August2026','net_income':533.481,'cfo':822.2,'capex_including_software':114.720,'sbc':84.099}
m['capex_including_software']=m['physical_capex']+m['software_capex']
for d in [m,f]:
 d['equity_proxy']=d['price']*d['shares'];d['fcf']=d['cfo']-d['capex_including_software'];d['owner_cash']=d['fcf']-d['sbc'];d['p_e']=d['equity_proxy']/d['net_income'];d['p_fcf']=d['equity_proxy']/d['fcf'];d['p_owner']=d['equity_proxy']/d['owner_cash']
json.dump([f,m],open(P/'peers.json','w'),indent=2);print([f,m])
