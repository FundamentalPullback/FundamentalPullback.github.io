import pathlib,json
import model
P=pathlib.Path(__file__).parent;c=model.CFG['central'];d={}
for n,v in [('margin_25',.25),('margin_29',.29)]:d[n]=model.run(dict(c,m=v))['conditional_per_share']
for n,v in [('beta_075',.75),('beta_115',1.15)]:d[n]=model.run(dict(c,beta=v))['conditional_per_share']
(P/'sensitivity.json').write_text(json.dumps(d,indent=2));print(d)
