import pathlib,json
P=pathlib.Path(__file__).parent;H=json.loads((P/'history.json').read_text());h=H['paired_ttm']['2026'];R0=h['revenue'];M0=(h['ebit']+39+51+h['depreciation']+h['amortization'])/R0
CFG={'stress':dict(g0=.035,g=.02,m=.245,beta=1.15,tax=.25,wc=.18,program=90,legal=75,tax_reserve=200,pension=50,new_g=.07,new_m=.19,tax_benefit=0),'central':dict(g0=.06,g=.025,m=.27,beta=.95,tax=.23,wc=.15,program=80,legal=35,tax_reserve=175,pension=36,new_g=.11,new_m=.22,tax_benefit=6.5),'upside':dict(g0=.085,g=.03,m=.29,beta=.8,tax=.21,wc=.12,program=70,legal=10,tax_reserve=125,pension=30,new_g=.14,new_m=.25,tax_benefit=13)}
def operating(c,new=False,g_override=None):
 R=135. if new else R0;S={'physical_internal_software':27. if new else 307.,'economic_intangibles':54. if new else 820.};life={'physical_internal_software':7.5,'economic_intangibles':12.};floor={'physical_internal_software':.025 if new else .012,'economic_intangibles':.012};mi=452/17/135-.01 if new else M0;mt=c['new_m'] if new else c['m'];g0=c['new_g'] if new else c['g0'];g0=g0 if g_override is None else g_override
 ke=.0486+c['beta']*.0441;w=.9*ke+.1*.055*(1-c['tax']);pv=tail=0;rows=[]
 for y in range(1,1011):
  g=g0+(c['g']-g0)*min(y-1,9)/9;Rn=R*(1+g);m=mi+(mt-mi)*min(y,5)/5;I={};D={};Sn={}
  for k,s in S.items():
   I[k]=max((s/life[k]+g*s)/(1-.5/life[k]),floor[k]*Rn);D[k]=(s+.5*I[k])/life[k];Sn[k]=s+I[k]-D[k]
  prog=(c['program']*.5 if y in [1,2] else 0) if not new else 0;ebit=m*Rn-sum(D.values())-prog;nopat=ebit*(1-c['tax']);dw=c['wc']*(Rn-R);fcf=nopat+sum(D.values())-sum(I.values())-dw
  if y<=10:pv+=fcf/(1+w)**y
  else:tail+=fcf/(1+w)**y
  if y<=11:rows.append(dict(year=y,g=g,revenue=Rn,cash_margin=m,opening_stock=S,investment=I,da=D,closing_stock=Sn,program_cash=prog,ebit=ebit,nopat=nopat,delta_wc=dw,fcff=fcf))
  S=Sn;R=Rn
 return dict(ev=pv+tail,pv_explicit=pv,pv_tail=tail,tail_share=tail/(pv+tail),ke=ke,wacc=w,years=rows)
def run(c,g_override=None):
 core=operating(c,g_override=g_override);cw=operating(c,new=True);bridge=1785-465-2920-350-27-31.6-c['pension']-c['tax_reserve']-c['legal']-5+c['tax_benefit'];eq=core['ev']+cw['ev']+bridge;shares=243.141824+1.5
 return dict(assumptions=c,core=core,cleanwater1=cw,bridge=bridge,conditional_equity=eq,conditional_per_share=eq/shares,shares_proxy=shares,approved_value=None)
r={k:run(v) for k,v in CFG.items()};lo,hi=0,.4
for _ in range(70):
 mid=(lo+hi)/2
 if run(CFG['central'],mid)['conditional_per_share']<117.09:lo=mid
 else:hi=mid
j={'as_of':'2026-11-08','units':'USD millions except per share','cases':r,'inverse_core_initial_growth':(lo+hi)/2,'initial_core_cash_margin':M0,'approved_values':None,'scope':'Conditional core plus separately funded acquired Cleanwater1; historical core TTM is not pro forma full-year all acquisitions. Sidecar capital stocks and adjusted-EBITDA-to-owner margin are assumptions, not acquired GAAP statements.','unknowns':{'Cleanwater1_purchase_allocation_and_actual_maintenance':None,'current_pension_net_deficit':None,'net_tax_claim_after_Danaher_indemnities':None,'legal_loss_above_normal_reserves':None,'commercial_paper_rollover_after_October2':None},'anti_double_count':['250 commercial paper already included in October2 debt and cash; subtract full465 cash once, add acquired business EV once','39 indemnity asset reduction reversed in EBIT, corresponding discrete tax benefit removed via normalized tax rate; do not add47 to normal profit','51 restructuring expense reversed at base, future cash70/80/90 includes36 unpaid recorded provision; no additional36 bridge deduction','Expensed RD and SBC remain costs; intangible renewal budget may overlap RD and is not certified']}
(P/'model_results.json').write_text(json.dumps(j,indent=2));print({k:(round(v['conditional_per_share'],2),round(v['cleanwater1']['ev'],1)) for k,v in r.items()},j['inverse_core_initial_growth'])
