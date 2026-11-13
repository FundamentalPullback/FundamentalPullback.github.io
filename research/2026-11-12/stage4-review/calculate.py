import json,pathlib,math
p=pathlib.Path(__file__).parent
v=json.loads((p/'calculations.json').read_text())['results']
for t,x in v.items():
 tr=max(x['high']-x['low'],abs(x['high']-x['previous_close']),abs(x['low']-x['previous_close']))
 atr=(13*x['previous_atr']+tr)/14
 candidate=x['highest_close']-3*atr
 assert math.isclose(atr,x['atr14'],abs_tol=1e-10)
 assert math.isclose(candidate,x['candidate'],abs_tol=1e-10)
 assert x['next_reference_raw']>=x['previous_floor_raw']
 assert round(max(candidate,x['previous_floor_raw']),2)==x['next_display']
 print(t,x['next_display'])
