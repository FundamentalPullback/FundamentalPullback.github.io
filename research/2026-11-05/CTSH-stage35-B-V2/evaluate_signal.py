"""Research-only candidate evaluator. No data feed, broker action, order or entry approval.
Synthetic fixtures test exact boundaries; they are not observed market data.
"""
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import json
TZ=ZoneInfo('America/New_York');DAY='2026-11-05'
def candidate(bars,asof,context):
 if not context.get('last_daily_above_ema50') or not context.get('long_trend_supportive'):return {'status':'blocked','reason':'daily structure'}
 if context.get('prior_ctsh_order_active_or_uncertain'):return {'status':'blocked','reason':'possible CTSH duplicate'}
 eligible=[]
 for b in sorted(bars,key=lambda x:x['end']):
  end=datetime.fromisoformat(b['end']).astimezone(TZ);start=end-timedelta(minutes=15)
  if end.date().isoformat()!=DAY or start.hour<9 or (start.hour==9 and start.minute<30) or end.hour>=16:continue
  if end.minute%15 or end.second or end.microsecond or end>asof or not b.get('complete',False):continue
  if b['low']<61.55:return {'status':'suspended','reason':'M regular breach; new proposal required'}
  if b['high']>66.50:return {'status':'suspended','reason':'fundamental cap exceeded; documented new review required'}
  if 65.26<b['close']<=65.78:
   deadline=end+timedelta(minutes=15)
   expired=asof>=deadline
   return {'status':'historical_candidate_expired' if expired else 'candidate_only','historical_only':expired,'execution_window_current':not expired,'signal_end':end.isoformat(),'manual_cancel_deadline':deadline.isoformat(),'entry_approved':False,'requires_current_quote_interval':'(65.26,65.78]','requires_account_risk_and_manual_supervision_check':True}
 return {'status':'no_candidate'}
def bar(end='2026-11-05T09:45:00-05:00',close=65.70,low=65.4,high=65.75,complete=True):return dict(end=end,close=close,low=low,high=high,complete=complete)
if __name__=='__main__':
 now=datetime.fromisoformat('2026-11-05T09:46:00-05:00');ctx={'last_daily_above_ema50':True,'long_trend_supportive':True,'prior_ctsh_order_active_or_uncertain':False};tests={}
 tests['inside']=candidate([bar()],now,ctx)['status']=='candidate_only'
 tests['floor_equal_rejected']=candidate([bar(close=65.26,low=65.20)],now,ctx)['status']=='no_candidate'
 tests['ceiling_equal_allowed']=candidate([bar(close=65.78,high=65.78)],now,ctx)['status']=='candidate_only'
 tests['above_technical_rejected']=candidate([bar(close=65.79,high=65.8)],now,ctx)['status']=='no_candidate'
 tests['premarket_excluded']=candidate([bar(end='2026-11-05T09:30:00-05:00')],now,ctx)['status']=='no_candidate'
 tests['close16_excluded']=candidate([bar(end='2026-11-05T16:00:00-05:00')],now,ctx)['status']=='no_candidate'
 tests['last1545_allowed']=candidate([bar(end='2026-11-05T15:45:00-05:00')],datetime.fromisoformat('2026-11-05T15:46:00-05:00'),ctx)['manual_cancel_deadline']=='2026-11-05T16:00:00-05:00'
 tests['incomplete_excluded']=candidate([bar(complete=False)],now,ctx)['status']=='no_candidate'
 tests['future_unobserved_excluded']=candidate([bar()],datetime.fromisoformat('2026-11-05T09:44:59-05:00'),ctx)['status']=='no_candidate'
 tests['M_equality_allowed']=candidate([bar(low=61.55)],now,ctx)['status']=='candidate_only'
 tests['M_breach_suspends']=candidate([bar(low=61.54)],now,ctx)['status']=='suspended'
 tests['fundamental_price_review']=candidate([bar(high=66.51)],now,ctx)['status']=='suspended'
 tests['first_qualifying_selected']=candidate([bar(end='2026-11-05T10:00:00-05:00'),bar()],now,ctx)['signal_end']=='2026-11-05T09:45:00-05:00'
 tests['duplicates_blocked']=candidate([bar()],now,{**ctx,'prior_ctsh_order_active_or_uncertain':True})['status']=='blocked'
 tests['ema50_required']=candidate([bar()],now,{**ctx,'last_daily_above_ema50':False})['status']=='blocked'
 tests['candidate_never_entry_approval']=candidate([bar()],now,ctx)['entry_approved'] is False
 tests['off_grid_seconds_rejected']=candidate([bar(end='2026-11-05T09:45:30-05:00')],now,ctx)['status']=='no_candidate'
 tests['off_grid_microseconds_rejected']=candidate([bar(end='2026-11-05T09:45:00.000001-05:00')],now,ctx)['status']=='no_candidate'
 tests['historical_candidate_labeled']=candidate([bar()],datetime.fromisoformat('2026-11-05T16:00:00-05:00'),ctx)['status']=='historical_candidate_expired'
 tests['deadline_exact_expired']=candidate([bar()],datetime.fromisoformat('2026-11-05T10:00:00-05:00'),ctx)['execution_window_current'] is False
 tests['before_deadline_current']=candidate([bar()],datetime.fromisoformat('2026-11-05T09:59:59-05:00'),ctx)['execution_window_current'] is True
 tests['end_session_expired']=candidate([bar(end='2026-11-05T15:45:00-05:00')],datetime.fromisoformat('2026-11-05T16:00:00-05:00'),ctx)['historical_only'] is True
 result={'pass':all(tests.values()),'count':len(tests),'synthetic_data_only':True,'no_market_signal_observed_or_order_generated':True,'checks':tests};print(json.dumps(result,indent=2));(Path(__file__).parent/'signal_tests.json').write_text(json.dumps(result,indent=2));assert all(tests.values())
