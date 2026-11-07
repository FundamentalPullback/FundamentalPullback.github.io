"""Bank residual-income sensitivity; not an approved valuation or capital plan."""
import json
B0=15.65; PRICE=32.57
# Explicit analyst assumptions, not management guidance. No automatic AOCI recovery.
CASES={'adverse':(.14,.11,.03,.02,.105),'central':(.18,.145,.045,.025,.095),'favorable':(.20,.17,.055,.03,.09)}
def calc(r0,rt,g0,gt,ke):
 b=B0; pv=0.; ri=0.; rows=[]
 for y in range(1,11):
  w=max(0,(y-5)/5);r=r0+(rt-r0)*w;g=g0+(gt-g0)*w
  earnings=b*r;retention=b*g;distribution=earnings-retention
  pv+=distribution/(1+ke)**y;ri+=(earnings-ke*b)/(1+ke)**y
  rows.append(dict(year=y,opening_tangible_book=b,rote=r,growth=g,earnings=earnings,retention=retention,potential_distribution=distribution));b+=retention
 tv=b*(rt-gt)/(ke-gt);v=pv+tv/(1+ke)**10
 rv=B0+ri+b*(rt-ke)/(ke-gt)/(1+ke)**10
 assert abs(v-rv)<1e-8
 return dict(value=v,price=PRICE,discount_to_value=1-PRICE/v,terminal_value_share=tv/(1+ke)**10/v,rows=rows)
def main():
 out={k:calc(*v) for k,v in CASES.items()}
 out['reverse_static']={'price_to_tbv':PRICE/B0,'ke':.095,'g':.025,'required_perpetual_rote':.025+(PRICE/B0)*(.095-.025),'note':'Static identity, not a forecast.'}
 out['ke_sensitivity_central']={str(k):calc(.18,.145,.045,.025,k)['value'] for k in [.085,.09,.095,.10,.105]}
 out['sourced_capm_contrast']={'rf':.0486,'monthly_erp':.0441,'published_beta':.96,'ke':.0486+.0441*.96,'central_value_at_this_ke':calc(.18,.145,.045,.025,.0486+.0441*.96)['value'],'not_final_regulatory_capital_valuation':True}
 out['status']='provisional sensitivity; regulatory distributability and merger reconciliation outstanding'
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
