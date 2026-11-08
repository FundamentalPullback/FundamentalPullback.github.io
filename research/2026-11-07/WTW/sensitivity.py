import pathlib,json
import model
P=pathlib.Path(__file__).parent;c=model.CFG['central'];d={}
for name,val in [('margin_26pct',.26),('margin_30pct',.30)]:d[name]=model.run(dict(c,margin=val))['per_share_residual_conditional']
for name,val in [('beta_08',.8),('beta_12',1.2)]:d[name]=model.run(dict(c,beta=val))['per_share_residual_conditional']
for name,val in [('float_95',95),('float_155',155)]:d[name]=model.run(dict(c,float_income=val))['per_share_residual_conditional']
(P/'sensitivity.json').write_text(json.dumps(d,indent=2));print(d)
