#!/usr/bin/env python3
"""Reproduce continuation from published A547 exact frozen seeds; no retroactive revisions."""
import json, pathlib
p=pathlib.Path(__file__).with_name('calculations.json'); data=json.loads(p.read_text())
stops={'ASO':50.30,'ULTA':522,'DOCU':62.50,'EXLS':33.50}
for t,v in data['results'].items():
 tr=max(v['high']-v['low'],abs(v['high']-v['previous_close']),abs(v['low']-v['previous_close']))
 atr=(13*v['previous_atr']+tr)/14
 highest=max(v['highest_close'],v['close']); candidate=highest-3*atr
 nxt=max(v['previous_floor_raw'],stops[t],candidate)
 assert abs(atr-v['atr14'])<1e-10 and abs(nxt-v['next_reference_raw'])<1e-10
 assert not v['close_below_previous'] and v['close']>v['previous_floor_raw']
 print(t,'ATR14',atr,'next',round(nxt,2))
