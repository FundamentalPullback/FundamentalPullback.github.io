import json,pathlib,copy
P=pathlib.Path(__file__).parent; H={r['period']:r for r in json.loads((P/'history/financial_history.json').read_text())}; X=json.loads((P/'facts/capital.json').read_text());T=next(r for k,r in H.items() if k.startswith('TTM') and r['end']=='2026-10-02');R=T['revenue'];E=T['ebit'];SH=X['q1_diluted_average_shares']
C={'bear':{'growth':[-.10,-.05,0,.02,.03,.03,.025,.02,.02,.02],'margin':[.30,.25,.22,.20,.20,.20,.20,.20,.20,.20],'tax':.24,'rate':.12,'g':.02,'roi':.15},'base':{'growth':[.20,.15,.10,.08,.06,.05,.04,.035,.03,.03],'margin':[.40,.39,.38,.37,.35,.34,.33,.32,.31,.30],'tax':.21,'rate':.11,'g':.025,'roi':.20},'bull':{'growth':[.30,.25,.20,.15,.12,.10,.08,.06,.05,.04],'margin':[.48,.48,.47,.46,.45,.44,.43,.42,.41,.40],'tax':.18,'rate':.10,'g':.03,'roi':.25}}
def calc(c,opcash=.08,utb=156,extra=81,shares=SH,capex_override=None,margin_delta=0,nwc=.12,cap_value=0):
 rev=R;prev=E*(1-c['tax']);rows=[]
 for i,(gr,m) in enumerate(zip(c['growth'],c['margin'])):
  old=rev;rev*=1+gr;m=max(0,m+margin_delta);nopat=rev*m*(1-c['tax']);capratio=capex_override if capex_override is not None else .055-i*.01/9;daratio=.02+i*.01/9;capex=rev*capratio;da=rev*daratio;dnwc=(rev-old)*nwc;physical=capex-da+dnwc;econ=max(0,nopat-prev)/c['roi'];reinv=max(physical,econ,0);fcff=nopat-reinv;row={'year':i+1,'revenue':rev,'margin':m,'nopat':nopat,'capex':capex,'da':da,'delta_nwc':dnwc,'physical_reinvestment':physical,'economic_reinvestment':econ,'additional_reinvestment_reserve':reinv-physical,'reinvestment':reinv,'fcff':fcff,'pv':fcff/(1+c['rate'])**(i+1)};rows.append(row);prev=nopat
 termrev=rev*(1+c['g']);termnopat=termrev*rows[-1]['margin']*(1-c['tax']);physical_t=termrev*(capratio-daratio)+(termrev-rev)*nwc;econ_t=termnopat*c['g']/c['roi'];reinv_t=max(0,physical_t,econ_t);fcff_t=termnopat-reinv_t;tv=fcff_t/(c['rate']-c['g']);tpv=tv/(1+c['rate'])**10;ev=sum(r['pv'] for r in rows)+tpv;bridge=X['cash']-X['debt_principal']-X['bis_current']-X['bis_long']-X['dividends_payable_oct2']-utb-R*opcash-extra+cap_value;eq=ev+bridge
 return {'assumptions':c,'years':rows,'terminal':{'revenue':termrev,'nopat':termnopat,'physical_reinvestment':physical_t,'economic_reinvestment':econ_t,'reinvestment':reinv_t,'fcff':fcff_t,'value':tv,'pv':tpv},'ev':ev,'bridge':bridge,'equity':eq,'shares':shares,'value':eq/shares,'terminal_fraction_ev':tpv/ev}
o={'anchor':T,'capital':X,'model_status':'screen-grade, conditional deterministic scenarios; not current balance certification or execution','capital_convention':'Historical net debt; Oct15 principal cancels cash and debt, expected loss81 only analyst stress proxy for net economic cost, not reported cash premium. Restricted112 excluded separately; capped calls not monetized. No quantified complete pension/contingency bridge.','cases':{k:calc(v) for k,v in C.items()},'sensitivities':{}}
b=C['base'];o['sensitivities']={k:v['value'] for k,v in {'redemption_cost_zero':calc(b,extra=0),'redemption_cost_162':calc(b,extra=162),'utb_historical_recognized43':calc(b,utb=43),'utb_zero':calc(b,utb=0),'utb_double':calc(b,utb=312),'opcash_15pct':calc(b,opcash=.15),'capex_8pct':calc(b,capex_override=.08),'shares_plus5pct':calc(b,shares=SH*1.05),'other_unresolved_claims_200':calc(b,extra=281),'capped_call_assumed_value_100':calc(b,cap_value=100),'margins_minus10pp':calc(b,margin_delta=-.10),'nwc_20pct':calc(b,nwc=.20)}.items()}
low=copy.deepcopy(b);low['margin']=[.07]*10;o['sensitivities']['7pct_operating_margin_all_years']=calc(low)['value']
o['rate_growth_grid']=[{'rate':w,'g':g,'value':calc(dict(b,rate=w,g=g))['value']} for w in [.10,.11,.12,.13] for g in [.02,.025,.03]]
# bounded reverse scan; keep all explicit and terminal margins shifted together
scan=[{'margin_delta':i/1000,'value':calc(b,margin_delta=i/1000)['value']} for i in range(-200,401,5)];roots=[]
for a,z in zip(scan,scan[1:]):
 if (a['value']-X['price'])*(z['value']-X['price'])<=0:
  lo=a['margin_delta'];hi=z['margin_delta']
  for _ in range(70):
   mid=(lo+hi)/2
   if (calc(b,margin_delta=lo)['value']-X['price'])*(calc(b,margin_delta=mid)['value']-X['price'])<=0:hi=mid
   else:lo=mid
  roots.append({'margin_delta':(lo+hi)/2,'value':calc(b,margin_delta=(lo+hi)/2)['value']})
o['reverse_margin']={'scan':scan,'roots':roots,'domain':[-.20,.40],'note':'All10years and terminal shifted; no root forced outside bounds; not an economic forecast.'}
(P/'model.json').write_text(json.dumps(o,indent=2)+'\n');print({k:round(v['value'],4) for k,v in o['cases'].items()})
