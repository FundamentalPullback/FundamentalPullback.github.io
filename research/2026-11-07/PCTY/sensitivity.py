import json,pathlib
import model
P=pathlib.Path(__file__).parent;c=model.cfg['central'];d={}
for n,y in [('float_low',.02),('float_high',.04)]:d[n]=model.run(dict(c,yield_=y))['conditional_per_share']
for n,L in [('contracts_short',4.4),('contracts_long',6.4)]:model.lives['contracts']=L;d[n]=model.run(c)['conditional_per_share']
(P/'sensitivity.json').write_text(json.dumps(d,indent=2))
