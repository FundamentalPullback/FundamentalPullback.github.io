import pathlib,json
P=pathlib.Path(__file__).resolve().parent
i=json.loads((P/'public_inputs.json').read_text());q='\n'.join(i['q2_primary_rows'])
checks={'primary_gics_table':i['sector_row']=='May 7, 2026 | S&P 500 | Addition | Veeva Systems | VEEV | Health Care','actual_q2_income':'275,018' in q and '273,429' in q,'actual_q2_revenue':'927,963' in q,'current_update_not_actual':'expects to report' in i['november_guidance_statement'] and 'meet or exceed' in i['november_guidance_statement']}
assert all(checks.values())
(P/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(P/'status.json').write_text(json.dumps(dict(ticker='VEEV',as_of='2026-11-08',status='STAGE1_SECTOR_INELIGIBLE',sector='Health Care',classification_effective_date='2026-05-07',source_date='2026-04-30',sector_eligibility=False,approved_values=None,approved_entry=None,full_fundamental_research_completed=False,next_earnings_date_confirmed=None,latest_actual_period='2026-07-31',latest_primary_update='2026-11-06',decision='Exclusión sectorial del plan, no juicio de valor ni rechazo por pérdidas.'),indent=2,ensure_ascii=False)+'\n')
