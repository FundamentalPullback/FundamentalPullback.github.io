import model,json,pathlib
P=pathlib.Path(__file__).parent;a=[]
for cap in [.02,.03,.04]:
 model.cap_phys=cap*2/3;model.cap_ip=cap/3
 for w in [.10,.113725,.13]:
  beta=(w-.0486-.01)/.0441
  v=model.calc(.18,.12,.21,.22,beta)
  a.append({'physical_plus_ip_capex_ratio':cap,'wacc':w,'conditional_basic_value_before_claims':v['value_per_basic_share_before_unknown_claims']})
(P/'sensitivity.json').write_text(json.dumps(a,indent=2))
