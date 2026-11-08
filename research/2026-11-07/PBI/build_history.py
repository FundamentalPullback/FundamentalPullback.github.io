import pathlib,json,re
P=pathlib.Path(__file__).parent
labels={'revenue':['Total revenue'],'pbt':['Income before taxes','Income (loss) from continuing operations before income taxes','Income (loss) from continuing operations before taxes'],'net_income':['Net income','Net income (loss)'],'continuing_income':['Income (loss) from continuing operations','Income from continuing operations'],'finance_revenue':['Financing and other'],'cfo':['Net cash from operating activities'],'cfo_cont':['Net cash from operating activities: continuing operations'],'da':['Depreciation and amortization'],'sbc':['Stock-based compensation'],'capex':['Capital expenditures'],'finance_asset_release':['Finance receivables'],'loan_cash':['Net investment in loan receivables'],'deposit_change':['Customer deposits at Pitney Bowes Bank'],'interest':['Interest expense, net'],'pension_nonservice':['Other components of net pension and postretirement cost'],'other_expense':['Other expense (income)','Other (income) expense','Other expense'],'restructuring':['Restructuring charges'],'restructuring_cash':['Restructuring payments'],'rd':['Research and development']}
def get(f,n=None):
 lines=json.loads((P/'financial_source_inputs.json').read_text())[f];o={}
 if n==3:
  st=max(i for i,x in enumerate(lines) if x.startswith('Services | $ | 1,206,031'));lines=lines[st:st+180]
 for k,ls in labels.items():
  for s in (lines[next(i for i,x in enumerate(lines) if x=='Cash flows from financing activities:'):] if k=='deposit_change' else lines):
   if s.split(' | ')[0] not in ls:continue
   v=[]
   for x in s.split(' | ')[1:]:
    if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):v.append((-float(x[1:-1].replace(',','')) if x.startswith('(') else float(x.replace(',','').replace('—','0')))/1000)
   if len(v)==n or(n is None and len(v)in[2,4]):o[k]=v;break
 return o
an=get('2026-02-20_pbi-20251231.htm.rows',3);a={str(y):{k:v[i] for k,v in an.items()}for i,y in enumerate([2025,2024,2023])};files={'q3_26':'q3.htm.rows','q2_26':'2026-07-30_pbi-20260630.htm.rows','q1_26':'2026-05-06_pbi-20260331.htm.rows','q3_25':'2025-10-30_pbi-20250930.htm.rows'};raw={k:get(f)for k,f in files.items()};q={k:{z:v[0]for z,v in d.items()}for k,d in raw.items()}
flows=['cfo','cfo_cont','da','sbc','capex','finance_asset_release','loan_cash','deposit_change','restructuring_cash']
for k in flows:
 for x,y in [('q3_26','q2_26'),('q2_26','q1_26')]:
  if k in q[x]and k in raw[y]:q[x][k]-=raw[y][k][0]
q['q4_25']={k:a['2025'][k]-raw['q3_26'][k][3 if len(raw['q3_26'][k])==4 else 1]for k in a['2025']if k in raw['q3_26']};ttm={}
for yr,tag in [(2026,'q3_26'),(2025,'q3_25')]:ttm[str(yr)]={k:a[str(yr-1)][k]+v[2 if len(v)==4 else 0]-v[3 if len(v)==4 else 1]for k,v in raw[tag].items()if k in a[str(yr-1)]}
for d in list(a.values())+list(q.values())+list(ttm.values()):
 if all(k in d for k in ['pbt','interest','pension_nonservice','other_expense']):d['operating_before_nonservice_pension_other_interest']=d['pbt']+d['interest']+d['pension_nonservice']+d['other_expense']
 if all(k in d for k in ['cfo','capex','sbc','finance_asset_release']):d['reported_cfo_less_capex_sbc']=d['cfo']+d['capex']-d['sbc'];d['cash_ex_finance_receivable_release']=d['reported_cfo_less_capex_sbc']-d['finance_asset_release']
j={'units':'USD millions; cash outflows negative','annual':a,'quarters':{k:v for k,v in q.items()if k!='q3_25'},'paired_ttm':ttm,'raw':raw,'sources':files,'limitations':['Annual revenue and PBT continuing operations; net income includes discontinued2023/24. Historical net CFO includes discontinued outflows; cfo_cont separate.','2026 adjustment excludes certain pension costs without recasting2025; no assumption identical segment EBIT definition.','10-K/A corrects auditor office location, not financial restatement.']};(P/'history.json').write_text(json.dumps(j,indent=2));print(json.dumps({'annual':a,'quarters':j['quarters'],'ttm':ttm},indent=2))
