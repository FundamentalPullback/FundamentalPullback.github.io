import pathlib,json
P=pathlib.Path(__file__).parent;out={}
for t in ['GOOG','GOOGL']:
 z=json.loads((P/'quote_inputs.json').read_text())[t];cs=z['closes'];em={}
 for n in [20,50]:
  e=cs[0]
  for c in cs[1:]:e=2/(n+1)*c+(1-2/(n+1))*e
  em[n]=e
 p=z['regular_price'];vol=sum(z['volumes20'])/20
 out[t]={'date':'2026-11-06','price':p,'ema20':em[20],'ema50':em[50],'volume20':vol,'technical_pass':p>em[50] and em[20]>em[50]}
(P/'quotes.json').write_text(json.dumps(out,indent=2));print(out)
