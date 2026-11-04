import json
from pathlib import Path
P=Path(__file__).resolve().parent
inputs={'price':109.16,'priceDate':'2026-11-03','balanceDate':'2026-09-30','actualSharesMillions':1037.917,'debtPrincipal':7600,'cashMarketables':6961,'strategicPrivateBook':2050,'gaapEbitTtm':1493,'acquiredAmortTtm':535,'priceSource':'https://stockanalysis.com/stocks/now/history/','financialSource':'https://www.sec.gov/Archives/edgar/data/1373715/000137371526000096/now-20260930.htm'}
ev=inputs['price']*inputs['actualSharesMillions']+inputs['debtPrincipal']-inputs['cashMarketables']
out={'inputs':inputs,'evCashMarketablesOnly':ev,'evGaapEbit':ev/1493,'evBeforeAcquiredAmortAfterSbc':ev/2028,'privateRecovery50PctAdjustedEv':ev-1025,'privateRecovery50PctAdjustedMultiple':(ev-1025)/2028,'limitations':'September capital and actual shares, November close; operating leases retained in operating costs. Private investments excluded from main EV deduction, shown separately. Not current exact capital or a valuation target.'}
(P/'now_screen.json').write_text(json.dumps(out,indent=2)+'\n')
print('NOW screen',out['evGaapEbit'],out['evBeforeAcquiredAmortAfterSbc'])
