import datetime,importlib.util,pathlib,copy
p=pathlib.Path(__file__).with_name('validate-close-batch.py');spec=importlib.util.spec_from_file_location('guard',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=lambda s:datetime.datetime.fromisoformat(s);b={'asOf':'2026-11-09','sessions':{'2026-11-09':{'SPY':1}},'evidence':{'2026-11-09':{'SPY':{'sessionDate':'2026-11-09','priceType':'regular-close','url':'https://example.com/test-fixture','sourceType':'dated-vendor-history','retrievedAt':'2026-11-09T22:00:00+00:00'}}}}
assert m.validate(b,'2026-11-06',D('2026-11-09T23:00:00+00:00'))['status']=='ready'
for dt in ['2026-11-07T23:00:00+00:00','2026-11-26T23:00:00+00:00']:assert m.validate({},'2026-11-06',D(dt))['status']=='no_session'
def fails(x,last,now):
 try:m.validate(x,last,D(now))
 except (AssertionError,KeyError):return
 raise AssertionError('expected rejection')
fails(b,'2026-11-06','2026-11-09T20:00:00+00:00');fails(b,'2026-11-06','2026-11-10T23:00:00+00:00');fails(b,'2026-11-09','2026-11-09T23:00:00+00:00')
c=copy.deepcopy(b);c['evidence']['2026-11-09']['SPY']['retrievedAt']='2026-11-01T22:00:00+00:00';fails(c,'2026-11-06','2026-11-09T23:00:00+00:00')
c=copy.deepcopy(b);c['evidence']['2026-11-09']['SPY']['priceType']='last';fails(c,'2026-11-06','2026-11-09T23:00:00+00:00')
assert m.trading(datetime.date(2026,11,27));assert '2026-11-27' in m.EARLY
fails({},'2028-12-29','2029-01-02T23:00:00+00:00')
print('PASS weekend/holiday skips, early-close calendar, after-close buffer, stale and wrong-date prices, missing sessions, already-current and unsupported-year guards.')
