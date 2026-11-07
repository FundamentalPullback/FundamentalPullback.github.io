#!/usr/bin/env python3
"""Fail-closed preflight for an after-close import; does not fetch or publish.
Official scheduled calendar checked 2026-11-07 at https://www.nyse.com/trade/hours-calendars.
Exceptional exchange closures still require checking current official notices before a run.
"""
import argparse,datetime,json,math
from zoneinfo import ZoneInfo
HOLIDAYS={2026:'01-01 01-19 02-16 04-03 05-25 06-19 07-03 09-07 11-26 12-25',2027:'01-01 01-18 02-15 03-26 05-31 06-18 07-05 09-06 11-25 12-24',2028:'01-17 02-21 04-14 05-29 06-19 07-04 09-04 11-23 12-25'}
EARLY={'2026-11-27','2026-12-24','2027-11-26','2028-07-03','2028-11-24'}
def trading(d):
    assert d.year in HOLIDAYS,'Calendar year unsupported; verify official calendar before extending'
    return d.weekday()<5 and d.strftime('%m-%d') not in HOLIDAYS[d.year].split()
def validate(batch,last,now):
    ny=now.astimezone(ZoneInfo('America/New_York'));target=ny.date()
    if not trading(target):return {'status':'no_session','date':target.isoformat()}
    hour=13 if target.isoformat() in EARLY else 16
    assert ny>=datetime.datetime.combine(target,datetime.time(hour,30),ZoneInfo('America/New_York')),'Session not closed plus30-minute settlement/publication buffer'
    assert batch['asOf']==target.isoformat(),'Batch does not reach the latest regular session'
    start=datetime.date.fromisoformat(last)+datetime.timedelta(days=1);expected=[]
    while start<=target:
        if trading(start):expected.append(start.isoformat())
        start+=datetime.timedelta(days=1)
    assert expected,'Already current; no import required'
    assert sorted(batch['sessions'])==expected,'Missing/extra sessions; do not skip a market day'
    for day,quotes in batch['sessions'].items():
        for ticker,p in quotes.items():
            assert isinstance(p,(float,int)) and not isinstance(p,bool) and math.isfinite(p) and p>0
            e=batch['evidence'][day][ticker]
            assert e['sessionDate']==day and e['priceType']=='regular-close','Price must be same-date regular close, not last/afterhours/adjusted close'
            assert e['url'].startswith('https://') and e['sourceType'] in ['official','dated-vendor-history','sheet-historical-series']
            fetched=datetime.datetime.fromisoformat(e['retrievedAt'].replace('Z','+00:00'))
            assert fetched.tzinfo and now-datetime.timedelta(hours=24)<=fetched<=now+datetime.timedelta(minutes=5),'Stale/future source retrieval'
    return {'status':'ready','asOf':batch['asOf'],'sessions':expected}
def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--last-published',required=True);p.add_argument('--now');a=p.parse_args()
    now=datetime.datetime.fromisoformat(a.now.replace('Z','+00:00')) if a.now else datetime.datetime.now(datetime.timezone.utc)
    print(json.dumps(validate(json.load(open(a.input)),a.last_published,now)))
if __name__=='__main__':main()
