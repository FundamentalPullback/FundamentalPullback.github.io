import json,csv,pathlib
P=pathlib.Path(__file__).parent
keys=['sales','ebit','netincome_parent','cfo','capex','depreciation','amortization','sbc']
v={'FY2023':[15320.2,1992.3,1372.3,2411.8,774.8,616.7,306.9,95.1],'FY2024':[15741.4,2802.4,2112.4,2813.9,994.5,634.9,300.5,134.8],'FY2025':[16081.2,2737.6,2075.6,2952.6,1048.3,672.6,303.8,136.6],'9M2024':[11736.2,2219.6,1639.5,2047.2,634.8,473.7,226.2,109.5],'9M2025':[11885.2,2025.6,1511.7,1862.5,716.2,493.8,226.5,109.5],'9M2026':[13176.3,2190.4,1518.8,1939.1,902,545.4,273.9,116],'Q12026':[4066.1,622,432.6,445.9,348.5,180.5,82.6,40.3],'H12026':[8481.5,1379.9,967.5,1175.4,588.6,364.3,167.7,75.1]}
h={k:dict(zip(keys,a)) for k,a in v.items()}
for p,a,b in [('Q42025','FY2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:h[p]={k:h[a][k]-h[b][k] for k in keys}
for yr,fy,sub in [('2025','FY2024','9M2024'),('2026','FY2025','9M2025')]:h['TTM'+yr]={k:h[fy][k]+h['9M'+yr][k]-h[sub][k] for k in keys}
for a in h.values():a['fcf_reported']=a['cfo']-a['capex'];a['margin_ebit']=a['ebit']/a['sales']
with open(P/'financial_history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2025']));w.writeheader();w.writerows(dict(period=p,**a) for p,a in h.items())
price=300.68;shares=282.1;base=h['TTM2026']['sales']
bridge={'debt_book_including_finance_leases':13192,'pension_noncurrent':530.9,'pension_current_fy2025_proxy':46.8,'restructure_accrued':70.3,'uncertain_tax_gross':66.1,'dividend_declared':204.8,'interest_accrued':145.1,'nci':30.6,'cash':-722.3,'operating_cash':base*.03}
claims=sum(bridge.values())
cases={'prudente':dict(sales1=18500,g=.03,gt=.02,margin1=.175,margin=.19,wacc=.10,physical_maintenance=1000,growth_fixed=.30,wc=.18,rd_replacement_credit=0,legal_stress=100),'intermedio':dict(sales1=19500,g=.06,gt=.025,margin1=.19,margin=.23,wacc=.09,physical_maintenance=950,growth_fixed=.25,wc=.15,rd_replacement_credit=.25,legal_stress=0),'favorable':dict(sales1=20500,g=.09,gt=.03,margin1=.205,margin=.27,wacc=.08,physical_maintenance=900,growth_fixed=.20,wc=.12,rd_replacement_credit=.50,legal_stress=0)}
def run(c):
 rows=[];sales=base
 for y in range(1,12):
  g=c['g'] if y<=5 else c['g']+(c['gt']-c['g'])*min((y-5)/5,1);new=c['sales1'] if y==1 else sales*(1+g)
  d=new-sales;organic=max(0,d-600) if y==1 else d
  margin=c['margin1']+(c['margin']-c['margin1'])*min((y-1)/5,1);ebit=new*margin;nopat=ebit*.79
  phyda=750*new/19500;intangda=400*new/19500;rd=.013*new
  maint=c['physical_maintenance']*new/19500;intangreplace=max(0,intangda-c['rd_replacement_credit']*rd)
  capacity=c['growth_fixed']*organic;wc=c['wc']*organic;fcff=nopat+phyda+intangda-maint-intangreplace-capacity-wc
  rows.append(dict(year=y,sales=new,margin=margin,ebit=ebit,nopat=nopat,physical_da=phyda,intangible_da=intangda,physical_replacement=maint,intangible_replacement=intangreplace,rd_expensed=rd,rd_credit=c['rd_replacement_credit']*rd,growth_fixed=capacity,delta_wc=wc,acquired_annualization_excluded=600 if y==1 else 0,fcff=fcff,net_reinvestment=maint+intangreplace+capacity+wc-phyda-intangda,calibrated_funding=False));sales=new
 pv=sum(r['fcff']/(1+c['wacc'])**r['year'] for r in rows[:10]);tv=rows[10]['fcff']/(c['wacc']-c['gt']);ptv=tv/(1+c['wacc'])**10;ev=pv+ptv;eq=ev-claims-c['legal_stress']
 return dict(assumptions=c,years=rows,ev=ev,equity=eq,price=eq/shares,terminal_ev_weight=ptv/ev)
out={k:run(v) for k,v in cases.items()};lo,hi=0,.5
for _ in range(100):
 mid=(lo+hi)/2
 if run(dict(cases['intermedio'],g=mid))['price']<price:lo=mid
 else:hi=mid
market_equity=price*280.467785;debt=13192;ke=.0486+1.1*.0441;kd=.0539
res=dict(asof='2026-11-08',price=price,shares_diluted_proxy=shares,history=h,bridge=bridge,net_claims=claims,ke_anchor=ke,wacc_anchor=(market_equity*ke+debt*kd*.79)/(market_equity+debt),cases=out,inverse_growth_years2to5=(lo+hi)/2,sensitivity=[dict(wacc=w,gt=g,price=run(dict(cases['intermedio'],wacc=w,gt=g))['price']) for w in [.08,.09,.10] for g in [.02,.025,.03]],intangible_credit_sensitivity=[dict(credit=c,price=run(dict(cases['intermedio'],rd_replacement_credit=c))['price']) for c in [0,.25,.5]],approved_values=None,approved_price=None,entry_approved=False,stage3_complete=False,capital_calibration_validated=False,cost_capital_metadata=dict(rf_date="2026-11-06",erp_date="2026-11-01",erp_source_rf=.0529,beta_assumed=1.1,debt_cost_is_issue_effective_rate=True,date_basis_mismatch=True),unresolved_economics=["Acquired annualization600 not disclosed proforma; no new acquisition price deducted", "R&D renewal overlap and physical/growth allocation uncalibrated; tax amortization shield not separately forecast", "Margin productivity/opex costs not independently verified; no automatic extra capital charge", "Current pension proxy, claim payment dates, tax settlements and residual acquisition compensation require reconciliation", "Annual normalized periods; September balance to November price stub not modeled"])
json.dump(res,open(P/'results.json','w'),indent=2);print('claims',claims,'wacc',res['wacc_anchor'],'cases',{k:v['price'] for k,v in out.items()},'inverse',res['inverse_growth_years2to5'])
