#!/usr/bin/env python3
"""Import a verified market-close snapshot, not private account/transaction exports.
Run manually after source review. No network, credentials, scheduling or deployment.
Input: {asOf, source, retrievedAt, sessions:{YYYY-MM-DD:{TICKER:close}}}.
Preserves existing dates, validates all held symbols on every appended date and derives
saved account prices from the same closes. Explicit corrections need separate review.
"""
import argparse,datetime,json,re,math
from pathlib import Path

def read(root,name):
    text=(root/'data'/f'{name}.js').read_text()
    prefix='window.FP=window.FP||{};FP.'+name+'='
    return json.loads(text[len(prefix):].strip().rstrip(';'))
def num(x): return float(str(x).replace('.','').replace(',','.'))
def day(x): return (datetime.datetime(1899,12,30)+datetime.timedelta(days=int(num(x)))).date().isoformat()
def fmt(x): return f'{x:.2f}'.replace('.',',')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--site-root',type=Path,required=True);ap.add_argument('--input',type=Path,required=True);a=ap.parse_args()
    source=json.loads(a.input.read_text());root=a.site_root
    assert source.get('source') and source.get('retrievedAt') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',source['asOf'])
    rows=read(root,'hist'); tickers=[x for x in rows[0] if x];hist={}
    for i,t in enumerate(tickers):
        hist[t]={day(r[i*2]):num(r[i*2+1]) for r in rows[2:] if len(r)>i*2+1 and r[i*2] and r[i*2+1]}
    ops=read(root,'ops')[1:];last=max(hist['SPY']);sessions=source['sessions'];assert max(sessions)==source['asOf']
    for d,quotes in sorted(sessions.items()):
        assert d>last, 'Existing dates are immutable; review corrections separately'
        held={}
        for r in ops:
            if r[0][:10]<=d:held[r[1]]=held.get(r[1],0)+num(r[4])*(-1 if r[3].lower() in ['venta','sell'] else 1)
        required={'SPY'}|{t for t,n in held.items() if n>1e-6}
        assert required<=set(quotes),f'{d}: missing closes {required-set(quotes)}'
        for t,p in quotes.items():
            assert re.fullmatch(r'[A-Z][A-Z0-9.\-]{0,9}',t) and isinstance(p,(int,float)) and not isinstance(p,bool) and math.isfinite(p) and p>0
            hist.setdefault(t,{})[d]=p
    ticks=list(hist);days=sorted(set().union(*(set(x) for x in hist.values())))
    out=[[x for t in ticks for x in (t,'')],[x for t in ticks for x in ('Date','Close')]]
    for d in days:
        serial=str((datetime.date.fromisoformat(d)-datetime.date(1899,12,30)).days)+',67'
        out.append([x for t in ticks for x in ((serial,fmt(hist[t][d])) if d in hist[t] else ('',''))])
    acct=read(root,'acct');asof=source['asOf'];prev=sorted(sessions)[-2] if len(sessions)>1 else last
    prices=sorted((t,h[asof],h.get(prev)) for t,h in hist.items() if t!='SPY' and asof in h)
    for r in acct:
        while len(r)<6:r.append('')
        r[3:6]=['','','']
        if r[0]=='SPY actual':r[1]=fmt(hist['SPY'][asof])
    acct[0][3:6]=['Ticker','Precio actual','Cierre anterior']
    for i,(t,p,q) in enumerate(prices,1):
        if i>=len(acct):acct.append(['']*6)
        acct[i][3:6]=[t,fmt(p),fmt(q) if q else '']
    for name,data in [('hist',out),('acct',acct)]:
        (root/'data'/f'{name}.js').write_text('window.FP=window.FP||{};FP.'+name+'='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
    p=root/'data/manifest.js';prefix='window.FP_MANIFEST=';m=json.loads(p.read_text()[len(prefix):].strip().rstrip(';'));m['asOf']=asof;p.write_text(prefix+json.dumps(m,separators=(',',':'))+';\n')
    print('Validated historical import through '+asof+'. Not published or scheduled. Review sources and run tests.')
if __name__=='__main__':main()
