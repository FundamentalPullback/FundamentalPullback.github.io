import json,csv
from pathlib import Path
P=Path(__file__).parent
rows=[]
for ticker,price,shares,date,book,bdate,annual,cur,prior,cfoann,cfocur,cfoprior in [
('PHM',132.49,184.086754,'2026-10-15',13095.961,'2026-09-30',2218.730,1294.726,1717.115,1871.249,636.966,1100.122),
('DHI',152.28,279.701267,'2026-07-16',23819.5,'2026-06-30',3585.2,2147.6,2679.9,3420.9,880.8,949.1),
('TOL',152.56,92.147,'2026-08-26',8530.770,'2026-07-31',1346.486,751.668,899.771,1112.411,392.060,312.381)]:
 ni=annual+cur-prior;cap=price*shares;cfo=cfoann+cfocur-cfoprior
 rows.append(dict(ticker=ticker,close_date='2026-11-06',price=price,shares=shares,share_date=date,book_equity=book,ttm_and_balance_date=bdate,common_netincome_ttm=ni,marketcap=cap,p_book=cap/book,p_earnings=cap/ni,netincome_on_closing_book=ni/book,cfo_ttm=cfo,cfo_yield=cfo/cap))
(P/'comparables.json').write_text(json.dumps({'definition':'Marketcap=regularcloseNov6 * latest cover basic shares; P/B parent equity excludes NCI. NI TTM=FY2025+9M2026−9M2025. NI/currentbook is not average-equity ROE. CFO includes inventory/warehouse movements; not distributable FCFE. No EV/EBIT mixing capitalized interest.','rows':rows},indent=2))
with (P/'comparables.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))
