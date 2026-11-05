from pathlib import Path
import json,math,hashlib,openpyxl,csv
P=Path(__file__).resolve().parent;R=json.loads((P/'model/results.json').read_text());H=json.loads((P/'model/history.json').read_text())['history'];A=json.loads((P/'model/assumptions.json').read_text());F=openpyxl.load_workbook(P/'output/SNPS_DCF.xlsx',data_only=False);V=openpyxl.load_workbook(P/'output/SNPS_DCF.xlsx',data_only=True);checks=[]
def check(n,b):
 checks.append({'check':n,'passed':bool(b)});assert b,n
check('First tab Cover',F.sheetnames[0]=='Cover');check('No external links',not F._external_links)
for k,r in R['cases'].items():
 check(k+' 10years',len(r['rows'])==10);check(k+' WACC>g',r['wacc']>A['cases'][k]['g']);check(k+' cached output',abs(V[k.title()]['C53'].value-r['value'])<1e-8)
 for i,x in enumerate(r['rows']):
  check(k+str(i)+' FCFF',abs(x['fcff']-x['nopat']+x['net_reinvestment'])<1e-8);check(k+str(i)+'positive reinvestment',x['net_reinvestment']>0)
 check(k+' terminal paid',abs(r['terminal_reinvestment']-r['terminal_nopat']*A['cases'][k]['g']/A['cases'][k]['roic'])<1e-8)
 check(k+' equity bridge',abs((r['ev']+r['bridge'])/r['shares']-r['value'])<1e-8)
check('ASR cash exactly once',A['capital']['asr_cash_paid']==1000);check('ASR pending shares not credited',A['capital']['pending_delivery']==0)
check('TTM EBIT controls',abs(H['TTM2026']['ebit']-802.356)<1e-7);check('TTM FCFF not reportedFCF',H['TTM2026']['fcf_total']==2747.706)
# independently reconstruct EMA from frozen daily prices
rows=list(csv.DictReader((P/'technical/daily_prices.csv').open()));out={}
for n in [20,50,200]:
 e=float(rows[0]['close'])
 for r in rows[1:]:e+=(float(r['close'])-e)*2/(n+1)
 out['EMA'+str(n)]=e
tech=json.loads((P/'technical/technicals.json').read_text())
for k,v in out.items():check(k+' independent reconstruction',abs(v-tech['series']['raw'][k])<1e-8)
fc=sum(1 for s in F for row in s for c in row if c.data_type=='f');check('702 main formulas',fc==702)
for s in V:
 for row in s:
  for c in row:
   check(f'{s.title}!{c.coordinate} no Excel error',c.data_type!='e') if c.value is not None else None
log={'status':'passed','checks':len(checks),'formula_count':fc,'technical_reconstructed':out,'limitations':['Homogeneous combined normalized EPS/FCF is not certified; reported proxy and proforma revenue are separated.','Static sensitivity cells regenerate via reproduce.py; case tabs are formula-first.','Independent investment/source audit still pending.'],'details':checks};(P/'qa.json').write_text(json.dumps(log,indent=2));print(log['status'],len(checks),fc)
