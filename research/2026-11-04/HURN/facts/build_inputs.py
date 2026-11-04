from pathlib import Path
import json
p=Path(__file__).parent
f=dict(cutoff='2026-11-04 22:56 UTC',scanner_date='2026-11-04',scanner_price=173.015,price=173.015,price_alternative=172.30,price_timestamp='2026-11-04 21:00 UTC (Yahoo regular market)',next_earnings_date=None,
q3_rbr=482.518,q3_rbr_prior=432.361,q3_revenue=491.451,q3_revenue_prior=441.284,q3_ebit=58.830,q3_ebit_prior=50.000,q3_ni=28.403,q3_ni_prior=30.420,q3_eps=1.75,q3_eps_prior=1.71,q3_shares_diluted=16.265,q3_shares_prior=17.794,
ytd_rbr=1391.866,ytd_rbr_prior=1230.556,ytd_revenue=1418.260,ytd_revenue_prior=1257.180,ytd_ebit=145.661,ytd_ebit_prior=128.386,ytd_ni=82.884,ytd_ni_prior=74.386,
cfo=15.329,cfo_prior=66.987,ppe=14.673,software=14.246,sbc=40.027,receivables_cash=-26.251,unbilled_cash=-64.004,
cash=25.618,cash_prior=24.508,debt_principal=815.0,debt_prior=511.0,debt_carrying=813.886,debt_issuance=1.114,revolver=440.,termloan=375.,annual_amortization=20.,revolver_available=259.6,letter_credit=.4,leverage_covenant_ratio=2.64,leverage_ratio_prior=1.93,leverage_limit=3.75,interest_coverage=7.58,coverage_limit=3.,interest_rate_including_swaps=.055,
buybacks_consideration=234.9,buybacks_cash=233.7,employee_tax_withholding=21.1,excise_accrual_in_buybacks=1.9,remaining_authorization_sept=65.9,oct_authorization_increment=200.,
earnout=27.947,earnout_prior=23.274,earnout_acquisition=3.423,earnout_payments=11.253,earnout_remeasurement=12.590,earnout_fx=-.087,earnout_max=44.3,earnout_current=18.6,earnout_noncurrent=9.3,earnout_cash_financing=8.7,earnout_cash_operating=2.3,
receivables=218.893,receivables_prior=186.506,unbilled=263.196,unbilled_prior=195.464,contract_assets_subset=123.0,contract_assets_prior=91.7,deferred_revenues=38.3,deferred_revenues_prior=31.7,rpo=327.7,rpo2026=33.9,rpo2027=105.3,rpo_later=188.5,
prior_obligations_revenue_ytd=17.1,prior_obligations_revenue_prior=27.8,variable_estimate_ytd=15.2,variable_estimate_prior=25.9,
organic_growth_q3=.067,organic_growth_ytd=.082,incremental_acquired_rbr_q3=21.1,incremental_acquired_rbr_ytd=59.8,relatecare_q3_revenue=13.9,relatecare_ytd_revenue=18.3,relatecare_goodwill=22.,relatecare_intangible=12.1,relatecare_earnout_max=11.6,
shorelight_fv=22.290,shorelight_prior=34.079,shorelight_oci_loss=6.928,shorelight_pnl_loss=4.861,shorelight_cost=40.9,shorelight_allowance=15.2,shorelight_q3_loss=5.928,equity_investment_impairment_ytd=2.2,longterm_investment_total=22.405,
deferred_comp_assets=53.184,derivative_assets=4.340,derivative_liabilities=.231,deferred_comp_liability=None,lease_liability_current=None,utb_fy2025=0.,utb_current=None,
restructuring=2.301,restructuring_prior=5.419,lease_gain=4.0,severance_rounded=3.9,rent_exit_rounded=2.2,restructuring_liability=.929,restructuring_cash=5.110,tax_rate_ytd=.262,tax_rate_prior=.190,statutory_including_state=.260,
capex_software_guidance_low=40.,capex_software_guidance_high=50.)
f['deferred_acquisition_payment_accrued']=8.728
f['sources']={'q3':'https://www.sec.gov/Archives/edgar/data/1289848/000162828026069514/hurn-20260930.htm','annual':'https://www.sec.gov/Archives/edgar/data/1289848/000162828026011093/hurn-20251231.htm','release':'https://huronconsultinggroup.gcs-web.com/news-releases/news-release-details/huron-announces-third-quarter-2026-financial-results-and-raises','calendar':'https://ir.huronconsultinggroup.com/events-and-presentations','price_alternative':'https://stockanalysis.com/stocks/hurn/history/','price_yahoo':'https://query1.finance.yahoo.com/v8/finance/chart/HURN?range=1mo&interval=1d'}
(p/'inputs.json').write_text(json.dumps(f,indent=2)+'\n')
