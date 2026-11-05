from pathlib import Path
import json,xlsxwriter
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from readability import spaced
from xlsxwriter.utility import xl_col_to_name as col
P=Path(__file__).resolve().parent;A=json.loads((P/'assumptions.json').read_text());R=json.loads((P/'results.json').read_text());H=json.loads((P/'history.json').read_text());out=P.parent/'output/SNPS_DCF.xlsx';w=xlsxwriter.Workbook(out);w.set_calc_mode('auto');F={'title':w.add_format({'bold':1,'font_size':20,'font_color':'#16364a'}),'head':w.add_format({'bold':1,'bg_color':'#16364a','font_color':'white','text_wrap':1}),'num':w.add_format({'num_format':'#,##0.00','font_color':'#111111'}),'input':w.add_format({'num_format':'#,##0.00','font_color':'#0055cc','bg_color':'#eaf3fa'}),'pct':w.add_format({'num_format':'0.0%'}),'ipct':w.add_format({'num_format':'0.0%','font_color':'#0055cc','bg_color':'#eaf3fa'}),'text':w.add_format({'text_wrap':1,'valign':'top'}),'note':w.add_format({'text_wrap':1,'font_color':'#52616b','font_size':10})};sheets={};cit=[]
def sheet(n):
 s=w.add_worksheet(n);sheets[n]=s;s.hide_gridlines(2);s.set_column('A:A',3);s.set_column('B:B',45);s.set_column('C:M',14);s.freeze_panes(4,2);s.set_row(1,34);return s
def put(s,cell,v,fmt='num'):s.write(cell,v,F[fmt])
def formula(s,cell,f,v,fmt='num'):s.write_formula(cell,f,F[fmt],v);cit.append({'sheet':s.name,'cell':cell,'formula':f,'value':v,'source':'assumptions.json / results.json; sources ledger'})
def note(s,row,t):s.merge_range(row,1,row+1,11,spaced(t),F['note']);s.set_row(row,22)
cover=sheet('Cover');cover.merge_range('B2:H2','SNPS | Valoración Fundamental Pullback',F['title']);note(cover,3,'5 noviembre 2026. Investigación auditada con salvedades, no aprobación de compra. Modelo FCFF 5+5; SBC retenida. USD millones salvo precio/acción.');put(cover,'B7','Cierre regular 4 nov','text');put(cover,'C7',A['price'],'input')
I=sheet('Inputs');I.merge_range('B2:H2','Inputs, fuentes y convenciones',F['title']);inputs={};row=5
for group in ['market','capital','segments']:
 for k,v in A[group].items():
  inputs[group+'.'+k]=row+1;put(I,f'B{row+1}',group+'.'+k,'text');put(I,f'C{row+1}',v,'ipct' if group=='market' and k!='beta' else 'input');row+=1
note(I,row+2,'Market: Rf Treasury Nov4; ERP Damodaran Nov1, mixed dates disclosed; beta StockAnalysis5Y. Financing weight10%, Kd5.6% analyst estimate. Capital: July10Q principal incl lock; Q4 FCF guidance rollforward; paid October ASR; $500m operating cash reserve.');
def ic(k):return f"Inputs!$C${inputs[k]}"
for case in ['bear','base','bull']:
 p=A['cases'][case];r=R['cases'][case];s=sheet(case.title());s.merge_range('B2:H2','SNPS | '+case.title()+' | FCFF 2027–2036',F['title']);put(s,'B5','WACC','text');m=A['market'];formula(s,'C5',f'=({ic("market.rf")}+{ic("market.beta")}*{ic("market.erp")})*(1-{ic("market.debt_weight")})+{ic("market.cost_debt")}*(1-{ic("market.tax")})*{ic("market.debt_weight")}+C6',r['wacc'],'pct');put(s,'B6','WACC adjustment','text');put(s,'C6',p['wacc_delta'],'ipct')
 for rr,k in [(7,'tax'),(8,'g'),(9,'roic'),(10,'da'),(11,'wc_increment'),(12,'strategic')]:put(s,f'B{rr}',k,'text');put(s,f'C{rr}',p[k],'ipct')
 labels={15:'Fiscal year',16:'EDA / other growth',17:'Simulation growth',18:'IP growth',19:'EDA / other revenue',20:'Simulation revenue',21:'IP revenue',22:'Total revenue',23:'Total growth',24:'Economic EBIT margin, SBC retained',25:'Economic EBIT',26:'Taxes',27:'NOPAT',28:'D&A, excludes acquired amortization',29:'Ordinary capex / revenue',30:'Ordinary capex',31:'Incremental operating working capital',32:'Strategic / intangible reinvestment',33:'Ordinary net reinvestment',34:'Transition weight',35:'Paid terminal reinvestment target',36:'Transition reinvestment adjustment',37:'Total net reinvestment',38:'FCFF',39:'Discount factor',40:'PV FCFF'}
 for rr,txt in labels.items():put(s,f'B{rr}',txt,'text')
 for i,rr in enumerate(r['rows']):
  c=col(i+2);prev=col(i+1);year=i+1;put(s,f'{c}15',rr['year'],'head')
  for kr,k in enumerate(A['segments']):
   gr=p['growth'][k][i] if i<5 else p['growth'][k][-1]+(p['g']-p['growth'][k][-1])*(i-4)/5
   if i<5:put(s,f'{c}{16+kr}',gr,'ipct')
   else:formula(s,f'{c}{16+kr}',f'=$G${16+kr}+($C$8-$G${16+kr})*({year}-5)/5',gr,'pct')
   ref=ic('segments.'+k) if i==0 else f'{prev}{19+kr}'
   formula(s,f'{c}{19+kr}',f'={ref}*(1+{c}{16+kr})',rr['segments'][k])
  formula(s,f'{c}22',f'=SUM({c}19:{c}21)',rr['revenue']);prior='SUM('+','.join(ic('segments.'+k) for k in A['segments'])+')' if i==0 else f'{prev}22';formula(s,f'{c}23',f'={c}22/{prior}-1',rr['growth'],'pct');put(s,f'{c}24',rr['margin'],'ipct');formula(s,f'{c}25',f'={c}22*{c}24',rr['ebit']);formula(s,f'{c}26',f'={c}25*$C$7',rr['tax']);formula(s,f'{c}27',f'={c}25-{c}26',rr['nopat']);formula(s,f'{c}28',f'={c}22*$C$10',rr['da']);put(s,f'{c}29',p['capex'][min(i,4)],'ipct');formula(s,f'{c}30',f'={c}22*{c}29',rr['capex']);formula(s,f'{c}31',f'=({c}22-{prior})*$C$11',rr['dnwc']);formula(s,f'{c}32',f'={c}22*$C$12',rr['strategic']);formula(s,f'{c}33',f'={c}30+{c}31+{c}32-{c}28',rr['net_reinvestment']-rr['transition_adjust']);formula(s,f'{c}34',f'=MAX(0,({year}-5)/5)',max(0,(year-5)/5),'pct');formula(s,f'{c}35',f'={c}27*$C$8/$C$9',rr['nopat']*p['g']/p['roic']);formula(s,f'{c}36',f'=({c}35-{c}33)*{c}34',rr['transition_adjust']);formula(s,f'{c}37',f'={c}33+{c}36',rr['net_reinvestment']);formula(s,f'{c}38',f'={c}27-{c}37',rr['fcff']);formula(s,f'{c}39',f'=1/(1+$C$5)^{year}',1/(1+r['wacc'])**year);formula(s,f'{c}40',f'={c}38*{c}39',rr['pv'])
 for rr,txt in [(43,'Terminal NOPAT'),(44,'Terminal reinvestment'),(45,'Terminal FCFF'),(46,'Terminal enterprise value'),(47,'PV terminal'),(48,'Operating EV'),(49,'Excess cash, Q4 rollforward net paid ASR'),(50,'Debt principal + treasury lock'),(51,'Equity value'),(52,'Fully diluted shares net initial ASR'),(53,'Value / share'),(54,'Upside to reference close'),(55,'Terminal % EV')]:put(s,f'B{rr}',txt,'text')
 for cell,f,val in [('C43','=L27*(1+C8)',r['terminal_nopat']),('C44','=C43*C8/C9',r['terminal_reinvestment']),('C45','=C43-C44',r['terminal_fcff']),('C46','=C45/(C5-C8)',r['terminal_value']),('C47','=C46/(1+C5)^10',r['terminal_pv']),('C48','=SUM(C40:L40)+C47',r['ev']),('C49','='+ic('capital.cash_july')+'+'+ic('capital.q4_fcf_rollforward')+'-'+ic('capital.asr_cash_paid')+'-'+ic('capital.operating_cash_reserve'),r['excess_cash']),('C50','='+ic('capital.debt_principal_and_lock'),A['capital']['debt_principal_and_lock']),('C51','=C48+C49-C50',r['ev']+r['bridge']),('C52','='+ic('capital.fully_diluted_pre_asr')+'-'+ic('capital.initial_asr_shares'),r['shares']),('C53','=C51/C52',r['value']),('C54','=C53/Cover!C7-1',r['upside']),('C55','=C47/C48',r['terminal_weight'])]:formula(s,cell,f,val,'pct' if cell in ['C54','C55'] else 'num')
 note(s,57,'Acquired amortization is not a cash addback here: EBIT already excludes it. R&D/SBC stay expensed. Strategic investment + ordinary capex + working capital pay for renewal/growth. Years6–10 converge to NOPAT×g/ROIC. No tax shield on unverified deductible PPA.')
for i,c in enumerate(['bear','base','bull'],10):
 put(cover,f'B{i}',c.title(),'head');formula(cover,f'C{i}',f'={c.title()}!C53',R['cases'][c]['value']);formula(cover,f'D{i}',f'={c.title()}!C54',R['cases'][c]['upside'],'pct')
note(cover,14,'NO APROBADA A ESTE PRECIO. El caso de cumplimiento del plan de dirección vale ~423, y un WACC menor puede acercarlo al precio: eso no deja compensación robusta por integración, reinversión y ejecución. Estrés combinado moderado ~262.');note(cover,18,'Lectura: report.html → Inputs → Base/Bear/Bull → History → Sensitivities → Checks. Precios, hipótesis y conclusiones condicionales. EPS normalizado publicado no es EPS proforma orgánico. Auditoría independiente completada: apto con salvedades para observación, no aprobación de compra. Véase audit/report.md.');note(cover,22,'Modelo editable de diez años. Los casos principales contienen fórmulas. Las sensibilidades estáticas requieren regeneración mediante el script después de modificar las hipótesis.');
s=sheet('History');s.merge_range('B2:H2','Historia publicada y normalización explícita',F['title']);fields=['period','revenue','ebit','net_income_cont','cfo_total','capex','sbc_cont','normalized_eps','fcf_total','diluted_shares'];
for j,k in enumerate(fields,1):put(s,f'{col(j)}5',k,'head')
for i,(period,data) in enumerate(H['history'].items(),5):
 for j,k in enumerate(fields,1):put(s,f'{col(j)}{i+1}',period if k=='period' else data[k],'text' if k=='period' else 'num')
note(s,26,H['normalization']);note(s,30,H['cash_limitation']);
s=sheet('Sensitivities');s.merge_range('B2:H2','Sensibilidad y expectativas implícitas',F['title']);
for j,k in enumerate(['WACC','g','Valor'],1):put(s,f'{col(j)}5',k,'head')
for i,d in enumerate(R['sensitivity'],6):
 for j,k in enumerate(['wacc','g','value'],1):put(s,f'{col(j)}{i}',d[k],'pct' if k!='value' else 'num')
for rr,t,v in [(33,'Crecimiento constante implícito5 años',R['reverse_constant_growth']),(34,'Incremento margen implícito',R['reverse_margin_shift']),(35,'Estrés combinado moderado',R['moderate_combined_stress']['value']),(36,'Entrega plan dirección',R['management_delivery']['value'])]:put(s,f'B{rr}',t,'text');put(s,f'C{rr}',v,'pct' if rr<35 else 'num')
note(s,38,'Sensibilidades y reversa son salidas calculadas por value.py, no fórmulas de escenarios enlazadas. Reejecutar reproduce.py tras editar assumptions.json. Los tres casos principales sí recalculan en Excel.');
s=sheet('Checks');s.merge_range('B2:H2','Controles del modelo',F['title']);rr=5
for c in ['Bear','Base','Bull']:
 for label,formula_,val in [('WACC > g',f'={c}!C5>{c}!C8',True),('Terminal reinvestment paid',f'=ABS({c}!L37-{c}!L35)<0.000001',True),('FCFF bridge',f'=ABS({c}!C38-({c}!C27-{c}!C37))<0.000001',True)]:put(s,f'B{rr}',c+' '+label,'text');formula(s,f'C{rr}',formula_,val);rr+=1
note(s,rr+2,'SBC remains expensed. Operating leases stay in operating costs; no second debt deduction. No future free buybacks. Pending ASR delivery=0. No unsupported PPA tax shield. Price reconciled across two sources. Independent audit complete with qualifications; exact proforma economic EPS remains a disclosed limitation.');
s=sheet('Sources');s.merge_range('B2:H2','Fuentes y trazabilidad',F['title']);row=5
for x in json.loads((P.parent/'source_ledger.json').read_text()):
 s.merge_range(row,1,row,11,x['id']+' | '+x['name'],F['head']);s.merge_range(row+1,1,row+2,11,x['url'],F['note']);s.merge_range(row+3,1,row+4,11,x['scope'],F['text']);row+=6
w.close();(P.parent/'output/model_citations.json').write_text(json.dumps(cit,indent=2));print(out.relative_to(P.parent),len(cit))
