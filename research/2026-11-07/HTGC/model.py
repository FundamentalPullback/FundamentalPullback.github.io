"""BDC dividend/RI model: every dollar of growth is funded; all assumptions conditional."""
import pathlib,json,csv
p=pathlib.Path(__file__).parent;B0=12.26;L=4845.903/2324.713;rf=.0486;erp=.0441
cases={'adverso':{'nii_start':.135,'nii5':.125,'nii_terminal':.12,'loss':.012,'beta':1.8,'stress':.04},'central':{'nii_start':.15,'nii5':.145,'nii_terminal':.14,'loss':.006,'beta':1.5,'stress':0},'favorable':{'nii_start':.16,'nii5':.16,'nii_terminal':.155,'loss':.003,'beta':1.2,'stress':0}}
def run(c,flat=None):
 ke=rf+c['beta']*erp+.01;b=B0*(1-c['stress']);initialloss=B0-b;pv=0;ri=B0-initialloss;rows=[]
 for y in range(1,11):
  n=(c['nii_start']+(c['nii5']-c['nii_start'])*(y-1)/4) if y<=5 else c['nii5']+(c['nii_terminal']-c['nii5'])*(y-5)/5
  if flat is not None:n=flat
  assets=L*b;nii=n*b;loss=c['loss']*assets;profit=nii-loss;div=.9*nii;end=b+profit-div;da=L*(end-b);dn=(L-1)*(end-b)
  pik=.14*nii # near TTM PIK/NII, timing proxy; not a second permanent loss
  repayments=.25*assets;originations=da+repayments-pik+loss
  cash=nii-pik+dn+repayments-originations-div
  assert abs(cash)<1e-10 and originations>0 and end>0
  discount=(1+ke)**y;pv+=div/discount;ri+=(profit-ke*b)/discount
  rows.append({'year':y,'nav_open':b,'nii_roe':n,'nii':nii,'loss':loss,'dividend':div,'nav_end':end,'portfolio_open':assets,'portfolio_change':da,'net_borrowing_change':dn,'pik':pik,'repayments':repayments,'originations':originations,'cash_residual':cash,'ri':profit-ke*b});b=end
 n=flat if flat is not None else c['nii_terminal'];g=.1*n-c['loss']*L;divnext=.9*n*b;roe=n-c['loss']*L
 tv=divnext/(ke-g);pv+=tv/(1+ke)**10;ri+=(roe-ke)*b/(ke-g)/(1+ke)**10
 assert abs(pv-ri)<1e-8
 return {'conditional_value':pv,'ri_crosscheck':ri,'ke':ke,'terminal_g_funded':g,'terminal_net_roe':roe,'initial_stress_loss_per_share':initialloss,'terminal_value_fraction':tv/(1+ke)**10/pv},rows
out={};rows=[]
for name,c in cases.items():
 out[name],a=run(c);out[name]['assumptions']=c;rows.extend({'case':name,**r} for r in a)
lo,hi=.05,.30
for _ in range(80):
 mid=(lo+hi)/2
 if run(cases['central'],mid)[0]['conditional_value']<16.16:lo=mid
 else:hi=mid
result={'as_of':'2026-11-08','nav_anchor':'2026-09-30','quote_date':'2026-11-06','price':16.16,'nav':B0,'assets_nav':L,'cases':out,'inverse_flat_nii_roe_central_loss_ke':(lo+hi)/2,'unvalued_convertible_option_adjustment':None,'regulatory_funding_validated':False,'approved_value':None,'approved_entry':None,'caveats':['Beta and additional 1% risk premium are explicit underwriting assumptions, not estimated market betas.','90% NII distribution is a financing proxy, not exact taxable-income forecast.','No continuing ATM premium assumed; SBC remains in NII.','All claims already reflected in NAV are not deducted twice. No unquantified claim set to zero.']}
(p/'results.json').write_text(json.dumps(result,indent=2));w=csv.DictWriter((p/'model_schedule.csv').open('w'),fieldnames=rows[0]);w.writeheader();w.writerows(rows);print(json.dumps(result,indent=2))
