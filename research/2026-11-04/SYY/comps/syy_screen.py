import json
from pathlib import Path
P=Path(__file__).resolve().parent
x={'close':74.11,'closeDate':'2026-11-03','actualSharesMillions':492.270756,'shareDate':'2026-10-16','debtCarryingSeptember':13820,'cashSeptember':3171,'estimatedOctGrossNetProceedsDifference':222,'gaapEbitTtm':3012,'acquiredAmortTtm':168,'exactPrincipalEv':None,'meaning':'SYY standalone EV proxy; excludes JRD operations/seller shares. October debt proceeds assumed retained pending deal, so incremental principal and cash largely offset; gross/net cost estimate included separately. Not observed November net debt.'}
ev=x['close']*x['actualSharesMillions']+x['debtCarryingSeptember']-x['cashSeptember']
out={'inputs':x,'septemberCarryingEv':ev,'septemberEvGaapEbit':ev/3012,'septemberEvBeforeAcquiredAmort':ev/3180,'octoberCostAdjustedEvProxy':ev+222,'octoberProxyEvGaapEbit':(ev+222)/3012,'octoberProxyEvBeforeAcquiredAmort':(ev+222)/3180,'sources':['https://www.sec.gov/Archives/edgar/data/96021/000009602126000050/syy-20260926.htm','https://www.sec.gov/Archives/edgar/data/96021/000110465926114079/tm2625144d27_8k.htm','https://stockanalysis.com/stocks/syy/history/']}
(P/'syy_screen.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
