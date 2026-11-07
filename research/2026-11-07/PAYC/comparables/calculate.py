from pathlib import Path
import json
p=Path(__file__).resolve().parent
x={'PAYC':{'quarterEnd':'2026-09-30','revenue':543.8,'priorRevenue':493.3,'reportedOperatingIncome':195.8,'priorOperatingIncome':112.6,'floatInterest':24.5,'priorFloatInterest':26.8,'source':'https://www.sec.gov/Archives/edgar/data/1590955/000119312526449828/payc-20260930.htm'},'PAYX':{'quarterEnd':'2026-08-31','revenue':1630.5,'priorRevenue':1540.0,'reportedOperatingIncome':619.2,'priorOperatingIncome':541.9,'floatInterest':49.8,'priorFloatInterest':47.6,'source':'https://www.sec.gov/Archives/edgar/data/723531/000072353126000004/payx-ex99_1.htm'},'ADP':{'quarterEnd':'2026-09-30','revenue':5490.7,'priorRevenue':5175.2,'reportedOperatingIncome':None,'priorOperatingIncome':None,'floatInterest':329.3,'priorFloatInterest':286.8,'reportedPretax':1454.9,'priorPretax':1307.5,'source':'https://www.sec.gov/Archives/edgar/data/8670/000000867026000033/q1fy27exhibit99.htm'}}
for d in x.values():
 d['revenueGrowth']=d['revenue']/d['priorRevenue']-1;d['floatGrowth']=d['floatInterest']/d['priorFloatInterest']-1
 if d['reportedOperatingIncome']is not None:d['operatingMargin']=d['reportedOperatingIncome']/d['revenue'];d['operatingIncomeGrowth']=d['reportedOperatingIncome']/d['priorOperatingIncome']-1
x['limitations']=['Operational comparison only. PAYX includes Paycor and PEO; ADP includes substantial PEO pass-through and a different client-funds funding strategy.','ADP pretax earnings are not relabeled comparable EBIT. No quarter annualization or peer multiple used as target.','Current homogeneous EV/multiples and full peer capital bridges not completed, so relative-valuation requirement remains open.']
(p/'outputs.json').write_text(json.dumps(x,indent=2)+'\n')
