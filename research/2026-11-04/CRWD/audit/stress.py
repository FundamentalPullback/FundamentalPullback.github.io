import pathlib,json,copy,math
P=pathlib.Path(__file__).resolve().parent.parent;s=(P/'model.py').read_text();ns={'__file__':str(P/'model.py')};exec(s[:s.index('out={k:calc')],ns);calc=ns['calc'];base=ns['cases']['base'];bull=ns['cases']['bull']
sets={
 'original_base':base,
 'original_bull':bull,
 'base_no_capitalized_sbc':dict(base,capsbc=[0]*10),
 'base_no_net_commissions':dict(base,commission=[0]*10),
 'base_capex_5pct_all_years':dict(base,capex=[.05]*10),
 'base_pretend_no_SBC_opex':dict(base,margin=[.25,.28,.30,.32,.33,.34,.35,.35,.35,.35]),
 'higher_growth_30five_fade':dict(bull,growth=[.30]*5+[.25,.20,.15,.10,.06],margin=[.10,.15,.20,.25,.30,.32,.34,.35,.35,.35],wacc=.085,g=.035,roic=.35),
 'sustained_25_ten_32_margin':dict(bull,growth=[.25]*10,margin=[.10,.15,.20,.24,.27,.30,.32,.32,.32,.32],wacc=.09,g=.03,roic=.35),
 'sustained_25_ten_35_margin':dict(bull,growth=[.25]*10,margin=[.10,.15,.20,.25,.30,.32,.34,.35,.35,.35],wacc=.085,g=.035,roic=.35),
 'sustained_30_ten_35_margin':dict(bull,growth=[.30]*10,margin=[.10,.15,.20,.25,.30,.32,.34,.35,.35,.35],wacc=.085,g=.035,roic=.35),
}
res={k:dict(inputs=v,**calc(v)) for k,v in sets.items()}
for k,z in res.items():print(k,round(z['per_share'],2),round(z['rows'][-1]['revenue']/1000,2),round(z['rows'][-1]['FCFF']/1000,2))
# Reverse constant growth ten years, not forced rapid fade.
a=dict(sets['sustained_25_ten_35_margin']);lo=.1;hi=.5
for _ in range(100):
 m=(lo+hi)/2;a['growth']=[m]*10
 if calc(a)['per_share']<244.68:lo=m
 else:hi=m
print('REVERSE_CONSTANT10',m,calc(a)['per_share']);res['reverse_constant10']=dict(growth=m,inputs=a,**calc(a))
(P/'audit'/'stress_results.json').write_text(json.dumps(res,indent=2))
